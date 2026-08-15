#!/usr/bin/env python3
"""Infinity two-stream research generator with local-runtime and novelty support."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sqlite3
from pathlib import Path

from infinity_ai_client import InfinityAIClient, InfinityAIError
from research_contract import ResearchFingerprint, record_fingerprint, validate_record

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "tokens.sqlite3"
LANES = {
    "GREEN_ENGINEER": ("Engineer", "Use target material to build or advance the source project."),
    "BLUE_IMPORT": ("Import", "Bring a missing capability, form, interface, method or dataset into the source."),
    "YELLOW_RESEARCH": ("Research", "Extract information that improves understanding or evidence for the source."),
    "ORANGE_DECIDE": ("Decide", "Use research and alternatives to create a concrete decision point."),
    "RED_ROUTE": ("Route", "Expose an alternate path, modernization, preservation route or replacement path."),
    "PURPLE_ASSIMILATE": ("Assimilate", "Combine multiple compatible ideas into a broader architecture."),
}


def rowdict(row: sqlite3.Row) -> dict:
    return {key: row[key] for key in row.keys()}


def best(token: dict, *names: str, default=None):
    for name in names:
        if token.get(name) not in (None, ""):
            return str(token[name])
    return default


def token_label(token: dict) -> str:
    return best(token, "repo_full_name", "repository", "repo_name", default=best(token, "token_id", default="Unknown token"))


def token_sha(token: dict) -> str:
    return best(token, "commit_sha", "sha", "full_sha", default="unknown")


def token_message(token: dict) -> str:
    return best(token, "message", "commit_message", default="No explicit commit message recorded")


def categories(conn: sqlite3.Connection, token_id: str) -> list[str]:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "token_categories" not in tables:
        return []
    return [row[0] for row in conn.execute(
        "SELECT category FROM token_categories WHERE token_id=? AND active=1 ORDER BY confidence DESC", (token_id,)
    )]


def relationships(conn: sqlite3.Connection, token_id: str) -> list[dict]:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "token_relationships" not in tables:
        return []
    return [dict(row) for row in conn.execute(
        """SELECT source_token_id,target_token_id,relationship_type,evidence_level,confidence,reason
           FROM token_relationships WHERE source_token_id=? OR target_token_id=?
           ORDER BY confidence DESC LIMIT 20""", (token_id, token_id)
    )]


def next_version(conn: sqlite3.Connection, token_id: str, stream: str) -> int:
    return int(conn.execute(
        "SELECT COALESCE(MAX(version),0)+1 FROM research_stream_entries WHERE token_id=? AND stream_type=?",
        (token_id, stream),
    ).fetchone()[0])


def project_research(conn: sqlite3.Connection, token: dict) -> tuple[str, str, dict]:
    token_id = best(token, "token_id")
    cats, rels = categories(conn, token_id), relationships(conn, token_id)
    repo, sha, message = token_label(token), token_sha(token), token_message(token)
    classification = best(token, "classification", "current_classification", default="UNCLASSIFIED")
    lines = [
        f"# Project Research — {repo}", "",
        f"This research entry is centered on Commit Token `{token_id}` and source commit `{sha}`.", "",
        "## What is recorded",
        f"The ledger records the project/repository as **{repo}**. The commit message is: **{message}**. "
        f"The current internal classification is **{classification}**.",
    ]
    if cats:
        lines += ["", "## Current semantic map", "Machine-inferred categories: " + ", ".join(cats) + "."]
    if rels:
        lines += ["", "## Existing lineage and connections"]
        for rel in rels[:8]:
            other = rel["target_token_id"] if rel["source_token_id"] == token_id else rel["source_token_id"]
            lines.append(f"- `{rel['relationship_type']}` with `{other}` — {rel['evidence_level']}, confidence {rel['confidence']:.2f}.")
    lines += [
        "", "## Working interpretation",
        "This token is a versioned project state. Research may inspect its change, reusable components, open requirements, descendants, alternatives, and evidence that strengthens or contradicts the current model.",
        "", "## Next research/build pass",
        "Compare this commit with its lineage, inspect changed files, identify concrete missing capabilities, and capture sources for outside factual claims. Project changes create ordinary Git commits and descendant Commit Tokens.",
    ]
    return f"Project research for {repo}", "\n".join(lines), {
        "token_id": token_id, "repository": repo, "commit_sha": sha, "commit_message": message,
        "categories": cats, "relationships": rels, "classification": classification,
        "research_status": "AUTHORED_FROM_LEDGER; EXTERNAL_VERIFICATION_PENDING",
    }


def choose_discovery(conn: sqlite3.Connection, token: dict) -> dict | None:
    token_id = best(token, "token_id")
    rows = conn.execute("SELECT * FROM tokens WHERE token_id<>?", (token_id,)).fetchall()
    if not rows:
        return None
    version = next_version(conn, token_id, "INFINITY_DISCOVERY_RESEARCH")
    seed = hashlib.sha256(f"{token_id}:{version}".encode()).digest()
    return rowdict(random.Random(int.from_bytes(seed[:8], "big")).choice(rows))


def shared_terms(a: dict, b: dict) -> list[str]:
    def words(token: dict) -> set[str]:
        raw = f"{token_label(token)} {token_message(token)}".lower().replace("/", " ").replace("-", " ")
        return {"".join(ch for ch in word if ch.isalnum()) for word in raw.split() if len(word) >= 5}
    return sorted(words(a) & words(b))[:12]


def discovery_research(token: dict, other: dict) -> tuple[str, str, dict, str, float]:
    token_id, other_id = best(token, "token_id"), best(other, "token_id")
    a, b, common = token_label(token), token_label(other), shared_terms(token, other)
    reason = "shared commit/repository terms: " + ", ".join(common) if common else "controlled-serendipity selection; no textual connection established yet"
    confidence = min(0.75, 0.25 + 0.08 * len(common)) if common else 0.15
    body = "\n".join([
        f"# Infinity Discovery Research — {a} × {b}", "", f"Source token: `{token_id}`",
        f"Discovery candidate: `{other_id}`", "", "## Why this candidate appeared",
        "Controlled serendipity selected this candidate; selection alone does not establish a factual relationship.",
        f"Current connection signal: **{reason}**.", "", "## Connection experiments",
        "- Research the terminology, files, methods, and evidence.",
        "- Import only a concrete capability the source lacks.",
        "- Engineer a build plan only after finding a reusable component.",
        "- Test alternate routes before proposing assimilation.", "", "## Research state",
        "This begins as `EXPLORATORY_LINK` and remains `INFERRED` until captured evidence supports promotion.",
    ])
    return f"Discovery: {a} × {b}", body, {
        "source_token_id": token_id, "candidate_token_id": other_id, "shared_terms": common,
        "reason": reason, "relationship_status": "EXPLORATORY_LINK", "confidence": confidence,
    }, reason, confidence


def runtime_enrich(client: InfinityAIClient | None, title: str, draft: str, context: dict) -> tuple[str, str, dict | None]:
    if client is None:
        return draft, "infinity-two-stream-research-v2/deterministic", None
    try:
        result = client.reason(
            "Improve the supplied draft as a concise research entry. Preserve recorded facts and explicit evidence labels. "
            "Do not claim outside facts or external verification without supplied sources.\n\n" + draft,
            context,
        )
        tool = client.propose_research_tool(f"Propose the next research action for {title}", context["token_id"])
        return result["output"], f"infinity-ai-runtime/REASONER:{result.get('model', 'local')}", tool
    except InfinityAIError as exc:
        return draft, "infinity-two-stream-research-v2/deterministic-fallback", {"error": str(exc), "executed": False}


def insert_entry(conn: sqlite3.Connection, token_id: str, stream: str, title: str, body: str,
                 structured: dict, evidence: str, engine: str, source_token_id: str | None = None) -> int:
    validate_record(stream, evidence, [])
    version = next_version(conn, token_id, stream)
    previous = conn.execute(
        "SELECT entry_id FROM research_stream_entries WHERE token_id=? AND stream_type=? AND active=1 ORDER BY version DESC LIMIT 1",
        (token_id, stream),
    ).fetchone()
    if previous:
        conn.execute("UPDATE research_stream_entries SET active=0 WHERE entry_id=?", (previous[0],))
    cursor = conn.execute(
        """INSERT INTO research_stream_entries
           (token_id,stream_type,version,title,body,structured_json,evidence_level,source_token_id,model_or_engine,supersedes_entry_id)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (token_id, stream, version, title, body, json.dumps(structured, sort_keys=True), evidence,
         source_token_id, engine, previous[0] if previous else None),
    )
    entry_id = int(cursor.lastrowid)
    lineage = [token_id] + ([source_token_id] if source_token_id else [])
    novelty = record_fingerprint(conn, entry_id, token_id, stream, ResearchFingerprint.build(
        query=title, sources=[], article=body, token_lineage=lineage,
    ))
    structured["novelty"] = novelty
    conn.execute("UPDATE research_stream_entries SET structured_json=? WHERE entry_id=?", (json.dumps(structured, sort_keys=True), entry_id))
    return entry_id


def create_action_candidates(conn: sqlite3.Connection, token: dict, other: dict | None) -> None:
    token_id, other_id = best(token, "token_id"), best(other or {}, "token_id")
    for lane, (verb, purpose) in LANES.items():
        plan = {"operation": lane, "source_token_id": token_id, "target_token_id": other_id,
                "purpose": purpose, "proposal_only": True}
        conn.execute(
            """INSERT INTO render_action_candidates
               (source_token_id,target_token_id,lane,anchor_text,display_text,plan_json,evidence_level,score)
               VALUES (?,?,?,?,?,?,?,?)""",
            (token_id, other_id, lane, verb.lower(), f"{verb}: {token_label(token)}", json.dumps(plan, sort_keys=True), "INFERRED", 0.5),
        )


def generate(conn: sqlite3.Connection, token_id: str, runtime: InfinityAIClient | None = None) -> dict:
    row = conn.execute("SELECT * FROM tokens WHERE token_id=?", (token_id,)).fetchone()
    if not row:
        raise ValueError(f"unknown token {token_id}")
    token = rowdict(row)
    title, draft, data = project_research(conn, token)
    body, engine, tool = runtime_enrich(runtime, title, draft, {"token_id": token_id, "stream_type": "PROJECT_RESEARCH", "ledger_record": data})
    if tool:
        data["tool_proposal"] = tool
    project_entry = insert_entry(conn, token_id, "PROJECT_RESEARCH", title, body, data, "INFERRED", engine)
    other, discovery_entry = choose_discovery(conn, token), None
    if other:
        title, draft, data, reason, confidence = discovery_research(token, other)
        body, engine, tool = runtime_enrich(runtime, title, draft, {"token_id": token_id, "stream_type": "INFINITY_DISCOVERY_RESEARCH", "ledger_record": data})
        if tool:
            data["tool_proposal"] = tool
        other_id = best(other, "token_id")
        discovery_entry = insert_entry(conn, token_id, "INFINITY_DISCOVERY_RESEARCH", title, body, data, "INFERRED", engine, other_id)
        conn.execute(
            "INSERT INTO discovery_links (source_token_id,candidate_token_id,research_entry_id,status,confidence,reason) VALUES (?,?,?,'EXPLORATORY_LINK',?,?)",
            (token_id, other_id, discovery_entry, confidence, reason),
        )
    create_action_candidates(conn, token, other)
    conn.commit()
    return {"token_id": token_id, "project_entry": project_entry, "discovery_entry": discovery_entry,
            "discovery_token": best(other or {}, "token_id")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--token")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--runtime", action="store_true", help="Use the local Infinity AI runtime; deterministic fallback remains available")
    parser.add_argument("--runtime-url")
    args = parser.parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.executescript((ROOT / "enrichment_schema.sql").read_text())
    conn.executescript((ROOT / "research_streams_schema.sql").read_text())
    runtime = InfinityAIClient(args.runtime_url) if args.runtime else None
    ids = [args.token] if args.token else [row[0] for row in conn.execute("SELECT token_id FROM tokens ORDER BY rowid DESC LIMIT ?", (args.limit,))]
    result = [generate(conn, token_id, runtime) for token_id in ids]
    print(json.dumps({"generated": len(result), "results": result}, indent=2))


if __name__ == "__main__":
    main()
