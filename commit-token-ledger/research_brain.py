#!/usr/bin/env python3
"""Infinity two-stream research generator.

Creates actual authored research-library entries from the existing token ledger:

1. PROJECT_RESEARCH: a synthesized project brief grounded in recorded token facts.
2. INFINITY_DISCOVERY_RESEARCH: a controlled-serendipity brief pairing the token
   with another ledgered token and explaining candidate connection paths.

This zero-dependency worker does not have an Internet research provider. It never
labels generated prose as EXTERNALLY_VERIFIED unless sourced research is later
ingested with citations. It is designed so an AI/web research service can append
verified sources to the same durable stream.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sqlite3
from pathlib import Path

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


def cols(conn: sqlite3.Connection, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def rowdict(row: sqlite3.Row) -> dict:
    return {k: row[k] for k in row.keys()}


def best(token: dict, *names: str, default: str = "") -> str:
    for name in names:
        value = token.get(name)
        if value not in (None, ""):
            return str(value)
    return default


def token_label(token: dict) -> str:
    return best(token, "repo_full_name", "repository", "repo_name", default=best(token, "token_id", default="Unknown token"))


def token_sha(token: dict) -> str:
    return best(token, "commit_sha", "sha", "full_sha", default="unknown")


def token_message(token: dict) -> str:
    return best(token, "message", "commit_message", default="No explicit commit message recorded")


def categories(conn: sqlite3.Connection, token_id: str) -> list[str]:
    if "token_categories" not in {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}:
        return []
    return [r[0] for r in conn.execute(
        "SELECT category FROM token_categories WHERE token_id=? AND active=1 ORDER BY confidence DESC",
        (token_id,),
    ).fetchall()]


def relationships(conn: sqlite3.Connection, token_id: str) -> list[dict]:
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "token_relationships" not in tables:
        return []
    rows = conn.execute(
        """SELECT source_token_id,target_token_id,relationship_type,evidence_level,confidence,reason
           FROM token_relationships
           WHERE source_token_id=? OR target_token_id=?
           ORDER BY confidence DESC LIMIT 20""",
        (token_id, token_id),
    ).fetchall()
    return [dict(r) for r in rows]


def next_version(conn: sqlite3.Connection, token_id: str, stream: str) -> int:
    row = conn.execute(
        "SELECT COALESCE(MAX(version),0)+1 FROM research_stream_entries WHERE token_id=? AND stream_type=?",
        (token_id, stream),
    ).fetchone()
    return int(row[0])


def project_research(conn: sqlite3.Connection, token: dict) -> tuple[str, str, dict]:
    tid = best(token, "token_id")
    cats = categories(conn, tid)
    rels = relationships(conn, tid)
    repo = token_label(token)
    sha = token_sha(token)
    msg = token_message(token)
    classif = best(token, "classification", "current_classification", default="UNCLASSIFIED")

    lines = [
        f"# Project Research — {repo}",
        "",
        f"This research entry is centered on Commit Token `{tid}` and source commit `{sha}`.",
        "",
        "## What is recorded",
        f"The ledger records the project/repository as **{repo}**. The commit message is: **{msg}**. "
        f"The current internal classification recorded for the token is **{classif}**.",
    ]
    if cats:
        lines += ["", "## Current semantic map", "The research system currently places this token in: " + ", ".join(cats) + ". "
                  "These categories are machine-inferred unless separately verified."]
    if rels:
        lines += ["", "## Existing lineage and connections"]
        for rel in rels[:8]:
            other = rel["target_token_id"] if rel["source_token_id"] == tid else rel["source_token_id"]
            lines.append(f"- `{rel['relationship_type']}` with `{other}` — {rel['evidence_level']}, confidence {rel['confidence']:.2f}. {rel.get('reason') or ''}")
    lines += [
        "",
        "## Working interpretation",
        "This token is treated as a versioned project state rather than a finished artifact. Its useful research surface includes the change represented by the commit, reusable components, unresolved requirements, descendant implementations, alternative routes, and evidence that could strengthen or contradict the current project model.",
        "",
        "## Next research/build pass",
        "The next pass should compare this commit with its parent and descendants, inspect the actual changed files, identify concrete missing capabilities, and attach externally verified sources where outside factual claims are relevant. Any resulting project modification should produce a new ordinary Git commit and therefore a new Commit Token; research updates remain versioned around this token.",
    ]
    structured = {
        "token_id": tid, "repository": repo, "commit_sha": sha, "commit_message": msg,
        "categories": cats, "relationships": rels, "classification": classif,
        "research_status": "AUTHORED_FROM_LEDGER; EXTERNAL_VERIFICATION_PENDING",
    }
    return f"Project research for {repo}", "\n".join(lines), structured


def choose_discovery(conn: sqlite3.Connection, token: dict) -> dict | None:
    tid = best(token, "token_id")
    rows = conn.execute("SELECT * FROM tokens WHERE token_id<>?", (tid,)).fetchall()
    if not rows:
        return None
    candidates = [rowdict(r) for r in rows]
    # Stable within a source-token generation while still spreading choices across corpus.
    version = next_version(conn, tid, "INFINITY_DISCOVERY_RESEARCH")
    seed_bytes = hashlib.sha256(f"{tid}:{version}".encode()).digest()
    rng = random.Random(int.from_bytes(seed_bytes[:8], "big"))
    return rng.choice(candidates)


def shared_terms(a: dict, b: dict) -> list[str]:
    def words(t: dict) -> set[str]:
        raw = " ".join([token_label(t), token_message(t)]).lower()
        out = set()
        for word in raw.replace("/", " ").replace("-", " ").split():
            word = "".join(ch for ch in word if ch.isalnum())
            if len(word) >= 5:
                out.add(word)
        return out
    return sorted(words(a) & words(b))[:12]


def discovery_research(conn: sqlite3.Connection, token: dict, other: dict) -> tuple[str, str, dict, str, float]:
    tid = best(token, "token_id")
    oid = best(other, "token_id")
    a, b = token_label(token), token_label(other)
    common = shared_terms(token, other)
    reason = "shared commit/repository terms: " + ", ".join(common) if common else "controlled-serendipity selection; no textual connection established yet"
    confidence = min(0.75, 0.25 + 0.08 * len(common)) if common else 0.15

    lines = [
        f"# Infinity Discovery Research — {a} × {b}", "",
        f"Source token: `{tid}`", f"Discovery candidate: `{oid}`", "",
        "## Why this candidate appeared",
        "This candidate was selected by the controlled-serendipity stream. Random selection by itself does **not** establish a factual relationship.",
        f"Current connection signal: **{reason}**.", "",
        "## Connection experiments",
        "- **Yellow / Research:** compare terminology, files, methods and evidence to determine whether either token explains the other.",
        "- **Blue / Import:** look for a concrete capability, form, interface, dataset or method in the candidate that the source lacks.",
        "- **Green / Engineer:** if a reusable component is found, form a build plan describing how it changes the source project.",
        "- **Red / Route:** test whether the candidate represents a legitimate alternate path, modernization route or replacement architecture.",
        "- **Purple / Assimilate:** only after concrete compatible pieces are identified, propose a synthesis retaining provenance to both tokens.",
        "- **Orange / Decide:** when research produces competing viable paths, package the evidence and tradeoffs into a decision state.", "",
        "## Research state",
        "This entry begins as `EXPLORATORY_LINK`. It should be promoted only when later research, action paths, file comparison or external sources support a specific relationship. If the pairing proves irrelevant, that negative result remains useful library evidence and the discovery stream moves on.",
    ]
    structured = {
        "source_token_id": tid, "candidate_token_id": oid, "shared_terms": common,
        "reason": reason, "relationship_status": "EXPLORATORY_LINK", "confidence": confidence,
    }
    return f"Discovery: {a} × {b}", "\n".join(lines), structured, reason, confidence


def insert_entry(conn: sqlite3.Connection, token_id: str, stream: str, title: str, body: str,
                 structured: dict, evidence: str, source_token_id: str | None = None) -> int:
    version = next_version(conn, token_id, stream)
    prev = conn.execute(
        "SELECT entry_id FROM research_stream_entries WHERE token_id=? AND stream_type=? AND active=1 ORDER BY version DESC LIMIT 1",
        (token_id, stream),
    ).fetchone()
    if prev:
        conn.execute("UPDATE research_stream_entries SET active=0 WHERE entry_id=?", (prev[0],))
    cur = conn.execute(
        """INSERT INTO research_stream_entries
           (token_id,stream_type,version,title,body,structured_json,evidence_level,source_token_id,model_or_engine,supersedes_entry_id)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (token_id, stream, version, title, body, json.dumps(structured, sort_keys=True), evidence,
         source_token_id, "infinity-two-stream-research-v1", prev[0] if prev else None),
    )
    return int(cur.lastrowid)


def create_action_candidates(conn: sqlite3.Connection, token: dict, other: dict | None) -> None:
    tid = best(token, "token_id")
    oid = best(other or {}, "token_id", default="") or None
    for lane, (verb, purpose) in LANES.items():
        plan = {
            "operation": lane,
            "source_token_id": tid,
            "target_token_id": oid,
            "purpose": purpose,
            "steps": [
                "Open the source token and preserve its canonical commit facts.",
                "Open the target/related evidence selected for this viewer.",
                f"Apply the {verb.lower()} operation as a proposal first.",
                "Record assumptions, evidence and the relationship produced.",
                "If project files actually change, create a normal Git commit and descendant Commit Token.",
            ],
        }
        conn.execute(
            """INSERT INTO render_action_candidates
               (source_token_id,target_token_id,lane,anchor_text,display_text,plan_json,evidence_level,score)
               VALUES (?,?,?,?,?,?,?,?)""",
            (tid, oid, lane, verb.lower(), f"{verb}: {token_label(token)}", json.dumps(plan, sort_keys=True), "INFERRED", 0.5),
        )


def generate(conn: sqlite3.Connection, token_id: str) -> dict:
    row = conn.execute("SELECT * FROM tokens WHERE token_id=?", (token_id,)).fetchone()
    if not row:
        raise ValueError(f"unknown token {token_id}")
    token = rowdict(row)
    ptitle, pbody, pdata = project_research(conn, token)
    project_entry = insert_entry(conn, token_id, "PROJECT_RESEARCH", ptitle, pbody, pdata, "INFERRED")

    other = choose_discovery(conn, token)
    discovery_entry = None
    if other:
        dtitle, dbody, ddata, reason, confidence = discovery_research(conn, token, other)
        discovery_entry = insert_entry(
            conn, token_id, "INFINITY_DISCOVERY_RESEARCH", dtitle, dbody, ddata,
            "INFERRED", source_token_id=best(other, "token_id"),
        )
        conn.execute(
            """INSERT INTO discovery_links
               (source_token_id,candidate_token_id,research_entry_id,status,confidence,reason)
               VALUES (?,?,?,'EXPLORATORY_LINK',?,?)""",
            (token_id, best(other, "token_id"), discovery_entry, confidence, reason),
        )
    create_action_candidates(conn, token, other)
    conn.commit()
    return {"token_id": token_id, "project_entry": project_entry, "discovery_entry": discovery_entry,
            "discovery_token": best(other or {}, "token_id", default=None)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--token")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.executescript((ROOT / "enrichment_schema.sql").read_text())
    conn.executescript((ROOT / "research_streams_schema.sql").read_text())

    if args.token:
        result = [generate(conn, args.token)]
    else:
        ids = [r[0] for r in conn.execute("SELECT token_id FROM tokens ORDER BY rowid DESC LIMIT ?", (args.limit,)).fetchall()]
        result = [generate(conn, tid) for tid in ids]
    print(json.dumps({"generated": len(result), "results": result}, indent=2))


if __name__ == "__main__":
    main()
