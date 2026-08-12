#!/usr/bin/env python3
"""Typed evidence and novelty contract shared by Infinity research adapters."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import unicodedata
from dataclasses import asdict, dataclass
from typing import Iterable

EVIDENCE_LEVELS = frozenset({"OBSERVED", "INFERRED", "EXTERNALLY_VERIFIED", "USER_DEFINED"})
STREAM_TYPES = frozenset({"PROJECT_RESEARCH", "INFINITY_DISCOVERY_RESEARCH"})


def normalize_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value or "").casefold().split())


def stable_hash(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ResearchFingerprint:
    query_hash: str
    source_set_hash: str | None
    article_hash: str
    token_lineage_hash: str
    user_path_hash: str | None

    @classmethod
    def build(
        cls,
        query: str,
        sources: Iterable[str],
        article: str,
        token_lineage: Iterable[str],
        user_path: Iterable[str] = (),
    ) -> "ResearchFingerprint":
        normalized_sources = sorted({normalize_text(source) for source in sources if normalize_text(source)})
        normalized_path = [normalize_text(item) for item in user_path if normalize_text(item)]
        return cls(
            query_hash=stable_hash(normalize_text(query)),
            source_set_hash=stable_hash(normalized_sources) if normalized_sources else None,
            article_hash=stable_hash(normalize_text(article)),
            token_lineage_hash=stable_hash([normalize_text(item) for item in token_lineage]),
            user_path_hash=stable_hash(normalized_path) if normalized_path else None,
        )


def validate_record(stream_type: str, evidence_level: str, source_urls: Iterable[str]) -> None:
    if stream_type not in STREAM_TYPES:
        raise ValueError(f"unsupported research stream: {stream_type}")
    if evidence_level not in EVIDENCE_LEVELS:
        raise ValueError(f"unsupported evidence level: {evidence_level}")
    if evidence_level == "EXTERNALLY_VERIFIED" and not list(source_urls):
        raise ValueError("EXTERNALLY_VERIFIED research requires captured source URLs")


def record_fingerprint(
    conn: sqlite3.Connection,
    entry_id: int,
    token_id: str,
    stream_type: str,
    fingerprint: ResearchFingerprint,
) -> dict:
    candidates = [
        ("query_hash", fingerprint.query_hash),
        ("article_hash", fingerprint.article_hash),
        ("source_set_hash", fingerprint.source_set_hash),
    ]
    duplicate = None
    matched_on = None
    for column, value in candidates:
        if value is None:
            continue
        duplicate = conn.execute(
            f"""SELECT entry_id FROM research_novelty_fingerprints
                WHERE token_id=? AND stream_type=? AND {column}=?
                ORDER BY entry_id LIMIT 1""",
            (token_id, stream_type, value),
        ).fetchone()
        if duplicate:
            matched_on = column
            break
    status = "DUPLICATE" if duplicate else "UNIQUE"
    duplicate_of = int(duplicate[0]) if duplicate else None
    conn.execute(
        """INSERT INTO research_novelty_fingerprints
           (entry_id,token_id,stream_type,query_hash,source_set_hash,article_hash,
            token_lineage_hash,user_path_hash,novelty_status,duplicate_of_entry_id,matched_on)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (entry_id, token_id, stream_type, *asdict(fingerprint).values(), status, duplicate_of, matched_on),
    )
    return {"status": status, "duplicate_of_entry_id": duplicate_of, "matched_on": matched_on}
