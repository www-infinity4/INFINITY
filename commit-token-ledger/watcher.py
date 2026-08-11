#!/usr/bin/env python3
"""Infinity Commit Token Watcher.

Zero-dependency GitHub polling watcher. It observes commits, derives stable token IDs,
stores provenance in SQLite, and reclassifies existing tokens without reminting them.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from classify import classify, is_administrative, load_config

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "commit_tokens.sqlite3"
SCHEMA_PATH = ROOT / "schema.sql"
CONFIG_PATH = ROOT / "config.json"


def utcnow():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def token_id(repository, sha):
    source_key = f"{repository}@{sha.lower()}"
    digest = hashlib.sha256(source_key.encode("utf-8")).hexdigest()[:32]
    return f"ICT-{digest}", source_key


class GitHubClient:
    def __init__(self, token=None):
        self.token = token

    def get(self, url):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Infinity-Commit-Token-Watcher/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8")), response.headers

    def paged(self, url, max_pages=20):
        page = 1
        while page <= max_pages:
            sep = "&" if "?" in url else "?"
            payload, _ = self.get(f"{url}{sep}per_page=100&page={page}")
            if not payload:
                break
            for item in payload:
                yield item
            if len(payload) < 100:
                break
            page += 1

    def repositories(self, owner):
        url = f"https://api.github.com/users/{urllib.parse.quote(owner)}/repos?sort=updated&direction=desc"
        return list(self.paged(url, max_pages=20))

    def commits(self, repository, limit=30):
        encoded = "/".join(urllib.parse.quote(x) for x in repository.split("/"))
        url = f"https://api.github.com/repos/{encoded}/commits?per_page={min(limit, 100)}"
        payload, _ = self.get(url)
        return payload[:limit]

    def readme(self, repository):
        encoded = "/".join(urllib.parse.quote(x) for x in repository.split("/"))
        url = f"https://api.github.com/repos/{encoded}/readme"
        try:
            payload, _ = self.get(url)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return ""
            raise
        import base64
        if payload.get("encoding") == "base64":
            return base64.b64decode(payload.get("content", "")).decode("utf-8", errors="replace")
        return ""


def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return db


def upsert_repository(db, repo):
    now = utcnow()
    db.execute(
        """
        INSERT INTO repositories(full_name, html_url, default_branch, first_seen_at, last_seen_at)
        VALUES(?,?,?,?,?)
        ON CONFLICT(full_name) DO UPDATE SET
          html_url=excluded.html_url,
          default_branch=excluded.default_branch,
          last_seen_at=excluded.last_seen_at
        """,
        (repo["full_name"], repo.get("html_url"), repo.get("default_branch"), now, now),
    )


def extract_commit(commit):
    c = commit.get("commit", {})
    author = c.get("author") or {}
    committer = c.get("committer") or {}
    return {
        "sha": commit["sha"],
        "url": commit.get("html_url"),
        "message": c.get("message", ""),
        "authored_at": author.get("date"),
        "committed_at": committer.get("date"),
        "author_name": author.get("name"),
        "author_email": author.get("email"),
        "committer_name": committer.get("name"),
        "committer_email": committer.get("email"),
        "parents": [p.get("sha") for p in commit.get("parents", []) if p.get("sha")],
    }


def record_event(db, tid, event_type, old_class, new_class, result, reason, level=None):
    db.execute(
        """INSERT INTO token_events
        (token_id,event_type,from_classification,to_classification,score,evidence,reason,evidence_level,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        (
            tid,
            event_type,
            old_class,
            new_class,
            result.get("score", 0),
            json.dumps(result.get("evidence", []), sort_keys=True),
            reason,
            level or result.get("evidence_level", "INFERRED"),
            utcnow(),
        ),
    )


def observe_commit(db, repository, commit, readme_text, config):
    meta = extract_commit(commit)
    tid, source_key = token_id(repository, meta["sha"])
    result = classify(repository, meta["message"], readme_text, config)
    admin = 1 if is_administrative(meta["message"], config) else 0

    existing = db.execute("SELECT * FROM tokens WHERE token_id=?", (tid,)).fetchone()
    if existing is None:
        initial = "ADMINISTRATIVE" if admin else "NON_SPACEX"
        current = "ADMINISTRATIVE" if admin else result["classification"]
        level = "OBSERVED" if admin else result.get("evidence_level", "INFERRED")
        db.execute(
            """INSERT INTO tokens(
              token_id,source_key,repository,commit_sha,commit_url,commit_message,
              authored_at,committed_at,author_name,author_email,committer_name,committer_email,
              parent_shas,discovered_at,initial_classification,current_classification,
              classification_score,classification_evidence,evidence_level,administrative)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                tid, source_key, repository, meta["sha"], meta["url"], meta["message"],
                meta["authored_at"], meta["committed_at"], meta["author_name"], meta["author_email"],
                meta["committer_name"], meta["committer_email"], json.dumps(meta["parents"]), utcnow(),
                initial, current, result.get("score", 0), json.dumps(result.get("evidence", []), sort_keys=True),
                level, admin,
            ),
        )
        record_event(db, tid, "TOKEN_DISCOVERED", None, current, result,
                     "GitHub commit observed and token identity derived", level)
        return "created", tid, current

    if existing["administrative"]:
        return "unchanged", tid, existing["current_classification"]

    old_class = existing["current_classification"]
    new_class = result["classification"]
    evidence_json = json.dumps(result.get("evidence", []), sort_keys=True)
    db.execute(
        """UPDATE tokens SET classification_score=?, classification_evidence=?, evidence_level=?
           WHERE token_id=?""",
        (result.get("score", 0), evidence_json, result.get("evidence_level", "INFERRED"), tid),
    )
    if new_class != old_class:
        db.execute("UPDATE tokens SET current_classification=? WHERE token_id=?", (new_class, tid))
        record_event(db, tid, "CLASSIFICATION_CHANGED", old_class, new_class, result,
                     "Classifier evaluation changed token state")
        return "reclassified", tid, new_class
    return "unchanged", tid, old_class


def scan_once(client, db, config, commit_limit):
    owner = config["owner"]
    stats = {"repos": 0, "created": 0, "reclassified": 0, "unchanged": 0, "errors": 0}
    repositories = client.repositories(owner)
    for repo in repositories:
        full_name = repo["full_name"]
        stats["repos"] += 1
        upsert_repository(db, repo)
        try:
            readme_text = client.readme(full_name)
            commits = client.commits(full_name, commit_limit)
            for commit in commits:
                status, tid, classification = observe_commit(db, full_name, commit, readme_text, config)
                stats[status] += 1
                if status != "unchanged":
                    print(f"{status:12} {classification:14} {tid} {full_name}@{commit['sha'][:12]}")
            db.commit()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            stats["errors"] += 1
            print(f"ERROR {full_name}: {exc}", file=sys.stderr)
            db.rollback()
    return stats


def export_jsonl(db, destination):
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = db.execute("SELECT * FROM tokens ORDER BY discovered_at, repository, commit_sha")
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            obj = dict(row)
            for field in ("parent_shas", "classification_evidence"):
                try:
                    obj[field] = json.loads(obj[field])
                except Exception:
                    pass
            fh.write(json.dumps(obj, sort_keys=True) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description="Watch GitHub commits and derive Infinity commit tokens")
    parser.add_argument("--once", action="store_true", help="scan once and exit")
    parser.add_argument("--interval", type=int, help="poll interval in seconds")
    parser.add_argument("--backfill", type=int, metavar="N", help="inspect up to N recent commits per repository")
    parser.add_argument("--export", metavar="PATH", help="export current token table as JSONL after each scan")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    args = parser.parse_args()

    config = load_config(args.config)
    limit = args.backfill or int(config.get("recent_commits_per_repo", 30))
    interval = args.interval or int(config.get("poll_interval_seconds", 300))
    client = GitHubClient(os.environ.get("GITHUB_TOKEN"))
    db = connect_db()

    while True:
        started = utcnow()
        try:
            stats = scan_once(client, db, config, limit)
            if args.export:
                export_jsonl(db, args.export)
            print(json.dumps({"scan_started": started, **stats}, sort_keys=True))
        except KeyboardInterrupt:
            break
        if args.once or args.backfill:
            break
        time.sleep(max(interval, 60))

    db.close()


if __name__ == "__main__":
    main()
