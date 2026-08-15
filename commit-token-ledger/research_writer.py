#!/usr/bin/env python3
"""Infinity commit-token research writer.

Zero-dependency enrichment worker for the commit token ledger. It creates a
structured factual research packet from ledgered commit data, records semantic
categories, links ordinary parent commits when those parents are already
ledgered, and leaves a durable queue/result trail for later AI or human
expansion.

This module deliberately distinguishes OBSERVED Git facts from INFERRED
interpretation. It does not rewrite Git history or change token identity.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable

DEFAULT_DB = Path(__file__).resolve().parent / "data" / "tokens.sqlite3"

CATEGORY_TERMS = {
    "CORE_ORCHESTRATION": ("infinity", "core", "agent", "system", "orchestr", "index"),
    "IDENTITY_SECURITY": ("identity", "security", "crypt", "wallet", "auth", "boron", "privacy"),
    "ECONOMY_LEDGER": ("coin", "token", "ledger", "mint", "trade", "payment", "asset"),
    "ATOMIC_MATERIALS": ("atomic", "electron", "oxide", "metal", "alloy", "quantum", "element"),
    "STATIC_COHERENCE_SENSING": ("coherence", "phonon", "microphone", "sensor", "resonance"),
    "FABRICATION": ("printer", "fabricat", "assembly", "manufactur", "build"),
    "RENDERING_INTERFACE": ("render", "screen", "display", "interface", "visual", "light-field"),
    "ROBOTICS": ("robot", "humanoid", "actuator", "skeleton"),
    "PROPULSION_SPACE": ("space", "spacecraft", "propulsion", "orbital", "rocket", "plasma shield", "starship"),
    "RESEARCH_DOCUMENTATION": ("readme", "research", "document", "article", "source", "citation"),
    "LEDGER_RECURSIVE": ("commit-token-ledger", "research_writer", "enrichment", "watcher", "classif"),
}


def columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def row_dict(row: sqlite3.Row) -> dict:
    return {k: row[k] for k in row.keys()}


def token_text(token: dict) -> str:
    keys = (
        "repo_full_name", "repository", "repo_name", "message", "commit_message",
        "classification", "current_classification", "html_url", "url"
    )
    return "\n".join(str(token.get(k, "")) for k in keys).lower()


def infer_categories(text: str) -> list[tuple[str, float, str]]:
    found = []
    for category, terms in CATEGORY_TERMS.items():
        hits = [term for term in terms if term in text]
        if hits:
            confidence = min(0.95, 0.45 + 0.1 * len(hits))
            found.append((category, confidence, "matched terms: " + ", ".join(hits)))
    return sorted(found, key=lambda x: x[1], reverse=True)


def parse_parents(token: dict) -> list[str]:
    for key in ("parents_json", "parent_shas_json", "parents"):
        value = token.get(key)
        if not value:
            continue
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = [p for p in re.split(r"[,\s]+", value) if p]
        result = []
        for p in value or []:
            if isinstance(p, dict):
                p = p.get("sha")
            if p:
                result.append(str(p))
        return result
    return []


def lookup_parent_token(conn: sqlite3.Connection, token: dict, sha: str) -> str | None:
    cols = columns(conn, "tokens")
    sha_col = next((x for x in ("commit_sha", "sha", "full_sha") if x in cols), None)
    repo_col = next((x for x in ("repo_full_name", "repository", "repo_name") if x in cols), None)
    if not sha_col:
        return None
    if repo_col:
        repo = token.get(repo_col)
        row = conn.execute(
            f"SELECT token_id FROM tokens WHERE {sha_col}=? AND {repo_col}=? LIMIT 1",
            (sha, repo),
        ).fetchone()
    else:
        row = conn.execute(f"SELECT token_id FROM tokens WHERE {sha_col}=? LIMIT 1", (sha,)).fetchone()
    return row[0] if row else None


def build_packet(token: dict, categories: Iterable[tuple[str, float, str]]) -> dict:
    observed = {
        k: token.get(k)
        for k in token
        if token.get(k) not in (None, "")
        and k not in {"classification_evidence", "evidence_json"}
    }
    category_rows = [
        {"category": c, "confidence": conf, "reason": reason, "evidence_level": "INFERRED"}
        for c, conf, reason in categories
    ]
    return {
        "token_id": token.get("token_id"),
        "observed_commit_record": observed,
        "semantic_categories": category_rows,
        "research_questions": [
            "What changed relative to the parent commit?",
            "What explicit reason is given by the commit message or changed documentation?",
            "Does this continue, repair, repurpose, or fork an earlier project idea?",
            "Which older commit tokens supplied reusable concepts or components?",
            "What factual external research would improve understanding of this commit?",
            "What later commits implement or reinterpret this token?",
        ],
        "evidence_policy": {
            "git_metadata": "OBSERVED",
            "semantic_categories": "INFERRED",
            "project_owner_meaning": "USER_DEFINED",
            "outside_research": "EXTERNALLY_VERIFIED only when sources are recorded",
        },
    }


def enrich_one(conn: sqlite3.Connection, token_id: str) -> None:
    token_row = conn.execute("SELECT * FROM tokens WHERE token_id=?", (token_id,)).fetchone()
    if not token_row:
        raise ValueError(f"unknown token: {token_id}")
    token = row_dict(token_row)
    text = token_text(token)
    categories = infer_categories(text)

    for category, confidence, reason in categories:
        conn.execute(
            """INSERT INTO token_categories
               (token_id, category, evidence_level, confidence, reason, active)
               VALUES (?, ?, 'INFERRED', ?, ?, 1)""",
            (token_id, category, confidence, reason),
        )

    for parent_sha in parse_parents(token):
        parent_token = lookup_parent_token(conn, token, parent_sha)
        if parent_token:
            conn.execute(
                """INSERT OR IGNORE INTO token_relationships
                   (source_token_id, target_token_id, relationship_type,
                    evidence_level, confidence, reason)
                   VALUES (?, ?, 'PARENT_COMMIT', 'OBSERVED', 1.0, ?)""",
                (token_id, parent_token, f"Git parent SHA {parent_sha}"),
            )

    is_recursive = any(cat == "LEDGER_RECURSIVE" for cat, _, _ in categories)
    if is_recursive:
        conn.execute(
            """INSERT INTO recursive_events
               (token_id, generator, operation, recursion_depth, details_json)
               VALUES (?, 'commit-token-ledger', 'SELF_DOCUMENTATION_OR_ENRICHMENT', 1, ?)""",
            (token_id, json.dumps({"reason": "commit text matched ledger/enrichment subsystem"})),
        )

    packet = build_packet(token, categories)
    body = (
        "Commit research packet. Git metadata is preserved as OBSERVED evidence; "
        "semantic categories are machine-generated INFERRED labels pending deeper research."
    )
    conn.execute(
        """INSERT INTO token_annotations
           (token_id, annotation_type, evidence_level, title, body,
            structured_json, author_type, author_id, model_or_engine, confidence)
           VALUES (?, 'COMMIT_RESEARCH_PACKET', 'OBSERVED', ?, ?, ?,
                   'AI_RESEARCH_WRITER', 'infinity-research-writer-v1',
                   'deterministic-context-builder', 1.0)""",
        (token_id, f"Research packet for {token_id}", body, json.dumps(packet, sort_keys=True)),
    )
    conn.execute(
        """UPDATE research_queue SET status='COMPLETED', completed_at=CURRENT_TIMESTAMP,
           attempts=attempts+1, last_error=NULL
           WHERE token_id=? AND job_type='COMMIT_RESEARCH'""",
        (token_id,),
    )


def run_queue(conn: sqlite3.Connection, limit: int) -> int:
    rows = conn.execute(
        """SELECT token_id FROM research_queue
           WHERE status IN ('PENDING','RETRY')
           ORDER BY priority DESC, requested_at ASC LIMIT ?""",
        (limit,),
    ).fetchall()
    completed = 0
    for row in rows:
        token_id = row[0]
        try:
            conn.execute(
                "UPDATE research_queue SET status='RUNNING', started_at=CURRENT_TIMESTAMP WHERE token_id=? AND job_type='COMMIT_RESEARCH'",
                (token_id,),
            )
            enrich_one(conn, token_id)
            conn.commit()
            completed += 1
        except Exception as exc:
            conn.rollback()
            conn.execute(
                """UPDATE research_queue SET status='RETRY', attempts=attempts+1,
                   last_error=? WHERE token_id=? AND job_type='COMMIT_RESEARCH'""",
                (str(exc), token_id),
            )
            conn.commit()
    return completed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parent / "enrichment_schema.sql")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--token")
    args = parser.parse_args()

    args.db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.executescript(args.schema.read_text(encoding="utf-8"))
    if args.token:
        enrich_one(conn, args.token)
        conn.commit()
        print(json.dumps({"enriched": 1, "token_id": args.token}))
    else:
        count = run_queue(conn, args.limit)
        print(json.dumps({"enriched": count}))


if __name__ == "__main__":
    main()
