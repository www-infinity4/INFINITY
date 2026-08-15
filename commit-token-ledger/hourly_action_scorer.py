#!/usr/bin/env python3
"""Infinity hourly Action Token scorer.

Zero-dependency SQLite worker. It summarizes unbatched high-volume interaction
records into one hourly batch without creating one Git commit per click.

The script does not push to GitHub. It produces a deterministic JSON report
that a checkpoint publisher can include in a single hourly commit.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

LANES = {
    "ENGINEERING": "ENGINEER",
    "ASSIMILATION": "ASSIMILATE",
    "IMPORT": "IMPORT",
    "RESEARCH": "RESEARCH",
    "DECISION": "DECIDE",
    "REPAIR": "REPAIR",
}


def utc_now():
    return dt.datetime.now(dt.timezone.utc)


def iso(value):
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def batch_id(start, end):
    raw = f"{iso(start)}|{iso(end)}".encode()
    return "IAB-" + hashlib.sha256(raw).hexdigest()[:24].upper()


def rows_for_window(db, start, end):
    return db.execute(
        """
        SELECT action_token_id,user_id,session_id,action_type,lane,
               source_token_id,destination_token_id,observed_at,payload_json
        FROM action_tokens
        WHERE hourly_batch_id IS NULL
          AND observed_at >= ? AND observed_at < ?
        ORDER BY user_id,session_id,observed_at,action_token_id
        """,
        (iso(start), iso(end)),
    ).fetchall()


def derive_paths(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r[1], r[2] or "NO_SESSION")].append(r)
    result = []
    for (user, session), items in groups.items():
        if not items:
            continue
        action_ids = [x[0] for x in items]
        token_ids = [items[0][5]]
        lanes = []
        for item in items:
            lanes.append(item[4])
            if item[6] and (not token_ids or token_ids[-1] != item[6]):
                token_ids.append(item[6])
        digest = hashlib.sha256("|".join(action_ids).encode()).hexdigest()[:24].upper()
        result.append({
            "path_id": "IAP-" + digest,
            "user_id": user,
            "session_id": session,
            "action_ids": action_ids,
            "token_ids": token_ids,
            "lanes": lanes,
        })
    return result


def derive_relationships(rows):
    counts = Counter()
    for r in rows:
        user, lane, src, dst = r[1], r[4], r[5], r[6]
        if dst:
            counts[(user, src, dst, lane)] += 1
    rels = []
    for (user, src, dst, lane), count in counts.items():
        relationship = LANES.get(lane.upper(), lane.upper())
        rels.append({
            "user_id": user,
            "source_token_id": src,
            "destination_token_id": dst,
            "relationship_type": relationship,
            "action_count": count,
            "confidence": min(0.95, 0.50 + (0.08 * max(0, count - 1))),
            "evidence_level": "INFERRED",
            "explanation": (
                f"{count} observed {lane} action(s) connected these tokens in this hourly window. "
                "The click relationship is observed; its project meaning remains an inference until accepted or evidenced."
            ),
        })
    return rels


def score(db, start, end, output):
    rows = rows_for_window(db, start, end)
    bid = batch_id(start, end)
    lanes = Counter((r[4] or "").upper() for r in rows)
    users = {r[1] for r in rows}
    tokens = set()
    for r in rows:
        tokens.add(r[5])
        if r[6]:
            tokens.add(r[6])

    paths = derive_paths(rows)
    relationships = derive_relationships(rows)
    report = {
        "batch_id": bid,
        "window_start": iso(start),
        "window_end": iso(end),
        "total_actions": len(rows),
        "unique_users": len(users),
        "unique_tokens": len(tokens),
        "lane_counts": {k.lower(): lanes.get(k, 0) for k in LANES},
        "paths": paths,
        "relationships": relationships,
        "action_ids": [r[0] for r in rows],
    }

    with db:
        db.execute(
            """
            INSERT OR REPLACE INTO hourly_action_batches
            (batch_id,window_start,window_end,total_actions,unique_users,unique_tokens,
             engineering_count,assimilation_count,import_count,research_count,
             decision_count,repair_count,report_json)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                bid, iso(start), iso(end), len(rows), len(users), len(tokens),
                lanes.get("ENGINEERING", 0), lanes.get("ASSIMILATION", 0),
                lanes.get("IMPORT", 0), lanes.get("RESEARCH", 0),
                lanes.get("DECISION", 0), lanes.get("REPAIR", 0),
                json.dumps(report, separators=(",", ":")),
            ),
        )
        for p in paths:
            db.execute(
                """INSERT OR IGNORE INTO action_paths
                (path_id,batch_id,user_id,session_id,ordered_action_ids_json,
                 ordered_token_ids_json,lane_sequence_json)
                VALUES (?,?,?,?,?,?,?)""",
                (p["path_id"], bid, p["user_id"], p["session_id"],
                 json.dumps(p["action_ids"]), json.dumps(p["token_ids"]), json.dumps(p["lanes"])),
            )
        for r in relationships:
            db.execute(
                """INSERT OR IGNORE INTO action_relationships
                (batch_id,user_id,source_token_id,destination_token_id,relationship_type,
                 action_count,confidence,evidence_level,explanation)
                VALUES (?,?,?,?,?,?,?,?,?)""",
                (bid,r["user_id"],r["source_token_id"],r["destination_token_id"],
                 r["relationship_type"],r["action_count"],r["confidence"],
                 r["evidence_level"],r["explanation"]),
            )
        db.execute(
            "UPDATE action_tokens SET hourly_batch_id=? WHERE hourly_batch_id IS NULL AND observed_at>=? AND observed_at<?",
            (bid, iso(start), iso(end)),
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/commit_tokens.sqlite3")
    parser.add_argument("--output", default="data/hourly/latest-action-batch.json")
    parser.add_argument("--hours", type=int, default=1)
    args = parser.parse_args()
    end = utc_now().replace(minute=0, second=0, microsecond=0)
    start = end - dt.timedelta(hours=args.hours)
    db = sqlite3.connect(args.db)
    try:
        report = score(db, start, end, Path(args.output))
        print(json.dumps({"batch_id": report["batch_id"], "actions": report["total_actions"]}))
    finally:
        db.close()


if __name__ == "__main__":
    main()
