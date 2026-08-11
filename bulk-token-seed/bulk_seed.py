#!/usr/bin/env python3
"""Fast zero-dependency Infinity bulk token seed compiler.

Input format: JSON Lines. Each non-empty line may contain:
  source_key      stable key for the source (optional; derived from payload if absent)
  source_type     e.g. REPO, COMMIT, ARTICLE, MEDIA, IDEA, GENERIC
  source_pointer  URL/path/repository pointer
  payload         arbitrary JSON-compatible material used to seed the token
  base_value      canonical viewer-independent base value (default "1")
  birth_at        ISO timestamp; defaults to current UTC

This compiler deliberately does NOT perform AI research, web research, rendering,
or Git writes. It creates the inexpensive canonical skeleton and queues later
enrichment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def bricks(identity_hash: str) -> tuple[str, str, str, str]:
    # Four compact 16-hex-character display segments. Full hash remains canonical.
    return tuple(identity_hash[i:i+16] for i in range(0, 64, 16))  # type: ignore[return-value]


def derive_record(namespace: str, row: dict[str, Any], ordinal: int) -> dict[str, str]:
    payload = row.get("payload", row)
    normalized_payload = canonical_json(payload)
    source_pointer = str(row.get("source_pointer") or "")
    source_type = str(row.get("source_type") or "GENERIC").upper()
    source_key = str(row.get("source_key") or sha(f"{source_type}\n{source_pointer}\n{normalized_payload}"))
    base_value = str(row.get("base_value", "1"))
    value_policy = str(row.get("value_policy_version", "v1"))
    birth_at = str(row.get("birth_at") or utc_now())

    identity_hash = sha(f"INFINITY:TOKEN:v1\n{namespace}\n{source_key}")
    b1, b2, b3, b4 = bricks(identity_hash)
    value_hash = sha(f"INFINITY:VALUE:{value_policy}\n{identity_hash}\n{base_value}")
    provenance_hash = sha(
        f"INFINITY:PROVENANCE:v1\n{identity_hash}\n{source_type}\n{source_pointer}\n{normalized_payload}"
    )
    interaction_root = sha(f"INFINITY:INTERACTION-ROOT:v1\n{identity_hash}\n{birth_at}")
    token_id = "ICT-" + identity_hash[:24].upper()

    return {
        "token_id": token_id,
        "namespace": namespace,
        "source_key": source_key,
        "source_type": source_type,
        "source_pointer": source_pointer,
        "normalized_payload": normalized_payload,
        "identity_hash": identity_hash,
        "identity_brick_1": b1,
        "identity_brick_2": b2,
        "identity_brick_3": b3,
        "identity_brick_4": b4,
        "base_value": base_value,
        "value_policy_version": value_policy,
        "value_hash": value_hash,
        "provenance_hash": provenance_hash,
        "interaction_root_hash": interaction_root,
        "birth_at": birth_at,
    }


def open_db(path: Path, schema: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(schema.read_text(encoding="utf-8"))
    return conn


def insert_batch(conn: sqlite3.Connection, records: list[dict[str, str]]) -> tuple[int, int]:
    created = 0
    existing = 0
    sql = """INSERT OR IGNORE INTO bulk_tokens
      (token_id, namespace, source_key, source_type, source_pointer, normalized_payload,
       identity_hash, identity_brick_1, identity_brick_2, identity_brick_3, identity_brick_4,
       base_value, value_policy_version, value_hash, provenance_hash,
       interaction_root_hash, birth_at, lifecycle_state)
      VALUES
      (:token_id, :namespace, :source_key, :source_type, :source_pointer, :normalized_payload,
       :identity_hash, :identity_brick_1, :identity_brick_2, :identity_brick_3, :identity_brick_4,
       :base_value, :value_policy_version, :value_hash, :provenance_hash,
       :interaction_root_hash, :birth_at, 'BRICKED')"""
    for record in records:
        before = conn.total_changes
        conn.execute(sql, record)
        if conn.total_changes > before:
            created += 1
            conn.execute(
                "INSERT OR IGNORE INTO bulk_enrichment_queue(token_id, reason, priority) VALUES(?, 'NEW_SEED', 0.0)",
                (record["token_id"],),
            )
        else:
            existing += 1
    return created, existing


def run(args: argparse.Namespace) -> dict[str, Any]:
    conn = open_db(args.db, args.schema)
    created = existing = failed = read = 0
    buffer: list[dict[str, str]] = []

    with args.input.open("r", encoding="utf-8") as handle:
        for ordinal, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            read += 1
            try:
                row = json.loads(raw)
                if not isinstance(row, dict):
                    row = {"payload": row}
                buffer.append(derive_record(args.namespace, row, ordinal))
            except Exception as exc:
                failed += 1
                if args.verbose:
                    print(json.dumps({"line": ordinal, "error": str(exc)}))
                continue

            if len(buffer) >= args.batch_size:
                c, e = insert_batch(conn, buffer)
                created += c
                existing += e
                conn.commit()
                buffer.clear()

    if buffer:
        c, e = insert_batch(conn, buffer)
        created += c
        existing += e
        conn.commit()

    pending = conn.execute("SELECT COUNT(*) FROM bulk_enrichment_queue WHERE status='PENDING'").fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM bulk_tokens").fetchone()[0]
    conn.close()
    return {
        "read": read,
        "created": created,
        "existing": existing,
        "failed": failed,
        "total_tokens": total,
        "pending_enrichment": pending,
        "namespace": args.namespace,
        "database": str(args.db),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk seed bricked Infinity token skeletons")
    parser.add_argument("--input", type=Path, required=True, help="JSONL source records")
    parser.add_argument("--db", type=Path, default=ROOT / "data" / "bulk_tokens.sqlite3")
    parser.add_argument("--schema", type=Path, default=ROOT / "schema.sql")
    parser.add_argument("--namespace", default="infinity-library")
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
