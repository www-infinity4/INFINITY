#!/usr/bin/env python3
"""Zero-dependency Infinity wallet entitlement engine.

This is the authoritative deterministic allocation core intended to sit behind
HTTP/API adapters. It uses SQLite transactions, server timestamps supplied by
the caller, idempotency keys, account-wide source limits, and a system overflow
pool. Front-end localStorage is never authoritative for balances.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "wallet_schema.sql"


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def account_day(timestamp: str) -> str:
    # v1 account-day policy is UTC; change only by policy version migration.
    return dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(dt.timezone.utc).date().isoformat()


def stable_hash(*parts: object) -> str:
    body = json.dumps(parts, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    return hashlib.sha256(body.encode()).hexdigest()


def connect(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA.read_text())
    return con


def qualify(con: sqlite3.Connection, *, user_id: str, source_key: str, action_key: str,
            idempotency_key: str, occurred_at: str | None = None,
            source_token_id: str | None = None, optional_input: str | None = None,
            evidence: dict | None = None) -> dict:
    occurred_at = occurred_at or iso_now()
    evidence = evidence or {}
    day = account_day(occurred_at)

    prior = con.execute(
        "SELECT e.*, t.token_id, t.canonical_hash, a.owner_type, a.owner_id "
        "FROM generation_events e "
        "LEFT JOIN economy_tokens t ON t.generation_event_id=e.event_id "
        "LEFT JOIN token_allocations a ON a.token_id=t.token_id "
        "WHERE e.idempotency_key=? ORDER BY a.allocated_at DESC LIMIT 1",
        (idempotency_key,),
    ).fetchone()
    if prior:
        return {"duplicate": True, **dict(prior)}

    policy = con.execute("SELECT * FROM source_policies WHERE source_key=?", (source_key,)).fetchone()
    if not policy:
        raise ValueError(f"unknown source_key: {source_key}")

    # Radio rolling-hour qualification happens before generation.
    if int(policy["min_interval_seconds"]) > 0:
        last = con.execute(
            "SELECT occurred_at FROM generation_events WHERE user_id=? AND source_key=? "
            "ORDER BY occurred_at DESC LIMIT 1",
            (user_id, source_key),
        ).fetchone()
        if last:
            previous = dt.datetime.fromisoformat(last["occurred_at"].replace("Z", "+00:00"))
            current = dt.datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
            elapsed = (current - previous).total_seconds()
            if elapsed < int(policy["min_interval_seconds"]):
                next_at = previous + dt.timedelta(seconds=int(policy["min_interval_seconds"]))
                return {"qualified": False, "reason": "MIN_INTERVAL", "next_eligible_at": next_at.isoformat()}

    with con:
        con.execute(
            "INSERT OR IGNORE INTO wallet_accounts(user_id,created_at,updated_at) VALUES(?,?,?)",
            (user_id, occurred_at, occurred_at),
        )
        con.execute("UPDATE wallet_accounts SET updated_at=? WHERE user_id=?", (occurred_at, user_id))

        ordinal = con.execute(
            "SELECT COUNT(*)+1 AS n FROM generation_events WHERE user_id=? AND source_key=? AND account_day=?",
            (user_id, source_key, day),
        ).fetchone()["n"]

        # Mint stops after ten. Crusher/Mario continue to generate into system pool.
        if source_key == "INFINITY_MINT" and ordinal > int(policy["user_daily_limit"]):
            return {"qualified": False, "reason": "DAILY_LIMIT", "user_daily_limit": int(policy["user_daily_limit"])}
        if source_key == "ALIEN_RADIO" and ordinal > int(policy["user_daily_limit"]):
            return {"qualified": False, "reason": "DAILY_LIMIT", "user_daily_limit": int(policy["user_daily_limit"])}

        event_id = "EVT-" + uuid.uuid4().hex
        event_hash = stable_hash(user_id, source_key, action_key, occurred_at, day, ordinal, source_token_id, optional_input, evidence)
        con.execute(
            "INSERT INTO generation_events(event_id,idempotency_key,user_id,source_key,action_key,source_token_id,optional_input,occurred_at,account_day,source_day_ordinal,evidence_json,event_hash) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (event_id, idempotency_key, user_id, source_key, action_key, source_token_id, optional_input,
             occurred_at, day, ordinal, json.dumps(evidence, sort_keys=True), event_hash),
        )

        token_hash = stable_hash("INFINITY_TOKEN_V1", event_hash, source_key, ordinal)
        token_id = "ICT-" + token_hash[:24].upper()
        con.execute(
            "INSERT INTO economy_tokens(token_id,generation_event_id,canonical_denomination,denomination_unit,canonical_hash,created_at) VALUES(?,?,1,'INFINITY',?,?)",
            (token_id, event_id, token_hash, occurred_at),
        )

        if ordinal <= int(policy["user_daily_limit"]):
            owner_type, owner_id, reason = "USER", user_id, "WITHIN_USER_SOURCE_LIMIT"
        else:
            owner_type, owner_id, reason = "INFINITY_SYSTEM_POOL", "INFINITY_SYSTEM_POOL", "SOURCE_OVERFLOW"

        allocation_id = "ALLOC-" + uuid.uuid4().hex
        con.execute(
            "INSERT INTO token_allocations(allocation_id,token_id,owner_type,owner_id,reason,allocated_at) VALUES(?,?,?,?,?,?)",
            (allocation_id, token_id, owner_type, owner_id, reason, occurred_at),
        )

    return {
        "qualified": True,
        "event_id": event_id,
        "token_id": token_id,
        "canonical_hash": token_hash,
        "denomination": 1,
        "unit": "INFINITY",
        "allocation": owner_type,
        "owner_id": owner_id,
        "source_day_ordinal": ordinal,
        "user_daily_limit": int(policy["user_daily_limit"]),
        "account_day": day,
    }


def balance(con: sqlite3.Connection, user_id: str) -> dict:
    row = con.execute(
        "SELECT COUNT(*) AS tokens, COALESCE(SUM(t.canonical_denomination),0) AS balance "
        "FROM token_allocations a JOIN economy_tokens t ON t.token_id=a.token_id "
        "WHERE a.owner_type='USER' AND a.owner_id=?",
        (user_id,),
    ).fetchone()
    by_source = [dict(r) for r in con.execute(
        "SELECT e.source_key, COUNT(*) AS tokens FROM token_allocations a "
        "JOIN economy_tokens t ON t.token_id=a.token_id "
        "JOIN generation_events e ON e.event_id=t.generation_event_id "
        "WHERE a.owner_type='USER' AND a.owner_id=? GROUP BY e.source_key ORDER BY e.source_key",
        (user_id,),
    )]
    return {"user_id": user_id, "tokens": row["tokens"], "balance": row["balance"], "unit": "INFINITY", "by_source": by_source}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="infinity-wallet.sqlite3")
    sub = p.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("qualify")
    q.add_argument("--user", required=True)
    q.add_argument("--source", required=True)
    q.add_argument("--action", required=True)
    q.add_argument("--idempotency", required=True)
    q.add_argument("--input")
    q.add_argument("--at")
    b = sub.add_parser("balance")
    b.add_argument("--user", required=True)
    args = p.parse_args()
    con = connect(args.db)
    if args.cmd == "qualify":
        out = qualify(con, user_id=args.user, source_key=args.source, action_key=args.action,
                      idempotency_key=args.idempotency, occurred_at=args.at, optional_input=args.input)
    else:
        out = balance(con, args.user)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
