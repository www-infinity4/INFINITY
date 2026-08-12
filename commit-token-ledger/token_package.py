#!/usr/bin/env python3
"""Build a useful, provenance-rich package around each immutable commit token."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable

from research_brain import generate

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "tokens.sqlite3"
STOPWORDS = frozenset({
    "about", "after", "again", "also", "been", "before", "build", "commit", "from", "have",
    "into", "more", "only", "project", "that", "their", "there", "these", "this", "token", "with",
})
RIGHTS_PATTERNS = (
    "public domain", "creativecommons.org/publicdomain/zero", "creativecommons.org/licenses/by/",
    "creativecommons.org/licenses/by-sa/",
)
MEDIA_EXTENSIONS = {
    "MOVIE": (".mp4", ".ogv", ".webm"),
    "SONG": (".mp3", ".ogg", ".flac", ".wav"),
}
REFERENCE_VALUES = {
    "COMMIT_CONTEXT": 100_000,
    "PR_CONTEXT": 200_000,
    "PROJECT_RESEARCH": 1_000_000,
    "DISCOVERY_RESEARCH": 200_000,
    "MOVIE_ACCESS": 1_000_000,
    "SONG_ACCESS": 100_000,
}


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_keyword(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(value).casefold())).strip()


def extract_keywords(text: str, limit: int = 16) -> list[str]:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9+#.-]{2,}", text or "")
    counts: dict[str, tuple[str, int]] = {}
    for display in words:
        normalized = normalize_keyword(display)
        if len(normalized) < 4 or normalized in STOPWORDS:
            continue
        prior = counts.get(normalized, (display, 0))
        counts[normalized] = (prior[0], prior[1] + 1)
    return [item[0] for _, item in sorted(counts.items(), key=lambda pair: (-pair[1][1], pair[0]))[:limit]]


def add_keyword(conn: sqlite3.Connection, token_id: str, keyword: str, source_type: str,
                source_ref: str | None, confidence: float = 1.0) -> None:
    normalized = normalize_keyword(keyword)
    if not normalized:
        return
    evidence = "USER_DEFINED" if source_type == "USER" else "OBSERVED" if source_type in {"COMMIT", "PR"} else "INFERRED"
    conn.execute(
        """INSERT OR IGNORE INTO token_keywords
           (token_id,keyword,normalized_keyword,source_type,source_ref,confidence,evidence_level)
           VALUES (?,?,?,?,?,?,?)""",
        (token_id, keyword.strip(), normalized, source_type, source_ref, confidence, evidence),
    )


def seed_keywords(conn: sqlite3.Connection, token: dict, user_keywords: Iterable[str],
                  history_texts: Iterable[str], cross_input_texts: Iterable[str]) -> None:
    token_id = token["token_id"]
    commit_text = f"{token.get('repository', '')} {token.get('commit_message', '')}"
    for keyword in extract_keywords(commit_text):
        add_keyword(conn, token_id, keyword, "COMMIT", token.get("commit_sha"), 0.9)
    for keyword in user_keywords:
        add_keyword(conn, token_id, keyword, "USER", "token-keyword-input", 1.0)
    for index, text in enumerate(history_texts):
        source_ref = "history-sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
        for keyword in extract_keywords(text, 8):
            add_keyword(conn, token_id, keyword, "HISTORY", source_ref, 0.65)
    for index, text in enumerate(cross_input_texts):
        source_ref = "cross-input-sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
        for keyword in extract_keywords(text, 8):
            add_keyword(conn, token_id, keyword, "CROSS_INPUT", source_ref, 0.7)


class GitHubContextClient:
    def __init__(self, token: str | None = None):
        self.token = token

    def get(self, url: str):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "Infinity-Token-Package/1.0"}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def pull_requests_for_commit(self, repository: str, sha: str) -> list[dict]:
        repo = "/".join(urllib.parse.quote(part) for part in repository.split("/"))
        return self.get(f"https://api.github.com/repos/{repo}/commits/{urllib.parse.quote(sha)}/pulls")

    def pull_request_details(self, repository: str, number: int) -> dict:
        repo = "/".join(urllib.parse.quote(part) for part in repository.split("/"))
        return self.get(f"https://api.github.com/repos/{repo}/pulls/{number}")

    def pull_request_reviews(self, repository: str, number: int) -> list[dict]:
        repo = "/".join(urllib.parse.quote(part) for part in repository.split("/"))
        return self.get(f"https://api.github.com/repos/{repo}/pulls/{number}/reviews")

    def check_runs(self, repository: str, sha: str) -> list[dict]:
        repo = "/".join(urllib.parse.quote(part) for part in repository.split("/"))
        result = self.get(f"https://api.github.com/repos/{repo}/commits/{urllib.parse.quote(sha)}/check-runs")
        return result.get("check_runs") or []


def record_pull_requests(conn: sqlite3.Connection, token: dict, client: GitHubContextClient) -> int:
    pull_requests = client.pull_requests_for_commit(token["repository"], token["commit_sha"])
    for pr in pull_requests:
        if hasattr(client, "pull_request_details"):
            pr = client.pull_request_details(token["repository"], int(pr["number"]))
        reviews = client.pull_request_reviews(token["repository"], int(pr["number"])) if hasattr(client, "pull_request_reviews") else []
        checks = client.check_runs(token["repository"], token["commit_sha"]) if hasattr(client, "check_runs") else []
        review_summary = [{
            "id": review.get("id"), "state": review.get("state"),
            "body": review.get("body") or "", "html_url": review.get("html_url"),
            "submitted_at": review.get("submitted_at"),
        } for review in reviews]
        check_summary = [{
            "name": check.get("name"), "status": check.get("status"),
            "conclusion": check.get("conclusion"), "details_url": check.get("details_url"),
        } for check in checks]
        body = pr.get("body") or ""
        conn.execute(
            """INSERT INTO token_pr_context
               (token_id,repository,pr_number,title,body,html_url,state,base_ref,head_ref,merge_commit_sha,
                changed_files,additions,deletions,review_summary_json,check_summary_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(token_id,repository,pr_number) DO UPDATE SET
                 title=excluded.title,body=excluded.body,html_url=excluded.html_url,state=excluded.state,
                 base_ref=excluded.base_ref,head_ref=excluded.head_ref,merge_commit_sha=excluded.merge_commit_sha,
                 changed_files=excluded.changed_files,additions=excluded.additions,deletions=excluded.deletions,
                 retrieved_at=CURRENT_TIMESTAMP""",
            (token["token_id"], token["repository"], pr["number"], pr.get("title") or "Untitled PR", body,
             pr.get("html_url") or "", pr.get("state"), (pr.get("base") or {}).get("ref"),
             (pr.get("head") or {}).get("ref"), pr.get("merge_commit_sha"), pr.get("changed_files"),
             pr.get("additions"), pr.get("deletions"), canonical_json(review_summary), canonical_json(check_summary)),
        )
        for keyword in extract_keywords(f"{pr.get('title', '')} {body}"):
            add_keyword(conn, token["token_id"], keyword, "PR", pr.get("html_url"), 0.85)
    return len(pull_requests)


class ArchiveClient:
    def get_json(self, url: str) -> dict:
        request = urllib.request.Request(url, headers={"User-Agent": "Infinity-Token-Package/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def search(self, query: str, mediatype: str, rows: int = 5) -> list[dict]:
        params = urllib.parse.urlencode([
            ("q", f"({query}) AND mediatype:{mediatype}"), ("fl[]", "identifier"),
            ("fl[]", "title"), ("fl[]", "description"), ("fl[]", "licenseurl"),
            ("fl[]", "rights"), ("fl[]", "downloads"), ("sort[]", "downloads desc"),
            ("rows", str(rows)), ("page", "1"), ("output", "json"),
        ])
        result = self.get_json("https://archive.org/advancedsearch.php?" + params)
        return (result.get("response") or {}).get("docs") or []

    def metadata(self, identifier: str) -> dict:
        return self.get_json("https://archive.org/metadata/" + urllib.parse.quote(identifier))


def rights_status(metadata: dict) -> tuple[str, str | None, str]:
    fields = metadata.get("metadata") or metadata
    license_url = fields.get("licenseurl") or fields.get("license_url")
    if isinstance(license_url, list):
        license_url = license_url[0] if license_url else None
    rights = fields.get("rights") or fields.get("usage") or ""
    if isinstance(rights, list):
        rights = " ".join(str(item) for item in rights)
    combined = f"{license_url or ''} {rights}".casefold()
    status = "VERIFIED_REUSE" if any(pattern in combined for pattern in RIGHTS_PATTERNS) else "REVIEW_REQUIRED"
    return status, license_url, str(rights)


def playable_file(metadata: dict, media_type: str) -> str | None:
    extensions = MEDIA_EXTENSIONS[media_type]
    files = metadata.get("files") or []
    choices = [item.get("name") for item in files if item.get("name", "").casefold().endswith(extensions)]
    if not choices:
        return None
    identifier = (metadata.get("metadata") or {}).get("identifier")
    return f"https://archive.org/download/{urllib.parse.quote(str(identifier))}/{urllib.parse.quote(choices[0])}"


def scan_archive(conn: sqlite3.Connection, token_id: str, client: ArchiveClient, limit: int = 3) -> int:
    keywords = [row[0] for row in conn.execute(
        "SELECT keyword FROM token_keywords WHERE token_id=? AND accepted=1 ORDER BY confidence DESC,keyword_id LIMIT 6",
        (token_id,),
    )]
    if not keywords:
        return 0
    query = " OR ".join('title:"' + word.replace('"', '') + '"' for word in keywords[:4])
    count = 0
    for media_type, archive_type in (("MOVIE", "movies"), ("SONG", "audio")):
        for item in client.search(query, archive_type, limit):
            identifier = str(item.get("identifier") or "")
            if not identifier:
                continue
            metadata = client.metadata(identifier)
            status, license_url, rights = rights_status(metadata)
            playable = playable_file(metadata, media_type)
            availability = "PLAYABLE" if playable else "METADATA_ONLY"
            raw_hash = digest(metadata)
            conn.execute(
                """INSERT OR REPLACE INTO token_media_candidates
                   (token_id,provider,provider_identifier,media_type,title,details_url,playable_url,
                    license_url,rights_statement,rights_status,availability_status,source_metadata_json,source_metadata_sha256)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (token_id, "Internet Archive", identifier, media_type, str(item.get("title") or identifier),
                 "https://archive.org/details/" + urllib.parse.quote(identifier), playable, license_url, rights,
                 status, availability, canonical_json(metadata), raw_hash),
            )
            count += 1
    return count


def add_utility(conn: sqlite3.Connection, token_id: str, component_type: str, reference: str,
                usable: bool, note: str) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO token_utility_components
           (token_id,component_type,component_ref,reference_microunits,usable,note)
           VALUES (?,?,?,?,?,?)""",
        (token_id, component_type, reference, REFERENCE_VALUES[component_type], int(usable), note),
    )


def ensure_research(conn: sqlite3.Connection, token_id: str) -> tuple[int, int | None]:
    rows = {row["stream_type"]: row["entry_id"] for row in conn.execute(
        "SELECT entry_id,stream_type FROM research_stream_entries WHERE token_id=? AND active=1", (token_id,)
    )}
    if "PROJECT_RESEARCH" not in rows:
        generate(conn, token_id)
        rows = {row["stream_type"]: row["entry_id"] for row in conn.execute(
            "SELECT entry_id,stream_type FROM research_stream_entries WHERE token_id=? AND active=1", (token_id,)
        )}
    return rows["PROJECT_RESEARCH"], rows.get("INFINITY_DISCOVERY_RESEARCH")


def build_package(conn: sqlite3.Connection, token_id: str, user_keywords: Iterable[str] = (),
                  history_texts: Iterable[str] = (), cross_input_texts: Iterable[str] = (),
                  github: GitHubContextClient | None = None, archive: ArchiveClient | None = None) -> dict:
    row = conn.execute("SELECT * FROM tokens WHERE token_id=?", (token_id,)).fetchone()
    if not row:
        raise ValueError(f"unknown token {token_id}")
    token = dict(row)
    project_entry, discovery_entry = ensure_research(conn, token_id)
    seed_keywords(conn, token, user_keywords, history_texts, cross_input_texts)
    pr_count = record_pull_requests(conn, token, github) if github else 0
    media_count = scan_archive(conn, token_id, archive) if archive else 0

    add_utility(conn, token_id, "COMMIT_CONTEXT", token["commit_sha"], True,
                "User-defined Infinity utility reference; not a cash or market appraisal.")
    add_utility(conn, token_id, "PROJECT_RESEARCH", str(project_entry), True,
                "Required project article is present; uniqueness and evidence remain separately recorded.")
    if discovery_entry:
        add_utility(conn, token_id, "DISCOVERY_RESEARCH", str(discovery_entry), True,
                    "Controlled discovery article is present.")
    for pr in conn.execute("SELECT pr_number,html_url FROM token_pr_context WHERE token_id=?", (token_id,)):
        add_utility(conn, token_id, "PR_CONTEXT", pr["html_url"], True,
                    "Observed PR explanation is attached to the commit package.")
    for media in conn.execute("SELECT * FROM token_media_candidates WHERE token_id=?", (token_id,)):
        usable = media["rights_status"] == "VERIFIED_REUSE" and media["availability_status"] == "PLAYABLE"
        component = "MOVIE_ACCESS" if media["media_type"] == "MOVIE" else "SONG_ACCESS"
        add_utility(conn, token_id, component, media["details_url"], usable,
                    "Reference counts only when reuse rights and a playable file are verified.")

    utility = int(conn.execute(
        "SELECT COALESCE(SUM(reference_microunits),0) FROM token_utility_components WHERE token_id=? AND usable=1",
        (token_id,),
    ).fetchone()[0])
    keywords = [dict(row) for row in conn.execute(
        "SELECT keyword,source_type,source_ref,confidence,evidence_level FROM token_keywords WHERE token_id=? AND accepted=1 ORDER BY confidence DESC,keyword",
        (token_id,),
    )]
    manifest = {
        "schema": "infinity/token-package/v1", "token_id": token_id,
        "canonical_identity": f"ICT|{token['repository']}|{token['commit_sha']}",
        "commit": {key: token.get(key) for key in ("repository", "commit_sha", "commit_url", "commit_message", "parent_shas")},
        "research": {"project_entry_id": project_entry, "discovery_entry_id": discovery_entry},
        "keywords": keywords, "pull_request_count": pr_count, "media_candidate_count": media_count,
        "utility": {
            "unit": "INFINITY", "target_microunits": 1_000_000,
            "reference_microunits": utility, "market_value_microunits": None,
            "basis": "USER_DEFINED_REFERENCE; NOT_A_CASH_OR_MARKET_APPRAISAL",
        },
    }
    manifest_hash = digest(manifest)
    review_count = conn.execute(
        "SELECT COUNT(*) FROM token_media_candidates WHERE token_id=? AND rights_status!='VERIFIED_REUSE'",
        (token_id,),
    ).fetchone()[0]
    status = "REVIEW_REQUIRED" if review_count else "READY"
    conn.execute(
        """INSERT INTO token_packages
           (token_id,status,project_research_entry_id,discovery_research_entry_id,
            utility_reference_microunits,manifest_json,manifest_sha256)
           VALUES (?,?,?,?,?,?,?)
           ON CONFLICT(token_id) DO UPDATE SET status=excluded.status,
             project_research_entry_id=excluded.project_research_entry_id,
             discovery_research_entry_id=excluded.discovery_research_entry_id,
             utility_reference_microunits=excluded.utility_reference_microunits,
             manifest_json=excluded.manifest_json,manifest_sha256=excluded.manifest_sha256,
             updated_at=CURRENT_TIMESTAMP""",
        (token_id, status, project_entry, discovery_entry, utility, canonical_json(manifest), manifest_hash),
    )
    conn.commit()
    return {**manifest, "status": status, "manifest_sha256": manifest_hash}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--token", required=True)
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--history-text", action="append", default=[])
    parser.add_argument("--cross-input", action="append", default=[])
    parser.add_argument("--github", action="store_true")
    parser.add_argument("--archive", action="store_true")
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    for schema in ("enrichment_schema.sql", "research_streams_schema.sql", "token_package_schema.sql"):
        conn.executescript((ROOT / schema).read_text(encoding="utf-8"))
    result = build_package(
        conn, args.token, args.keyword, args.history_text, args.cross_input,
        GitHubContextClient(os.environ.get("GITHUB_TOKEN")) if args.github else None,
        ArchiveClient() if args.archive else None,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
