#!/usr/bin/env python3
import json
import sqlite3
import unittest
from pathlib import Path

from infinity_ai_client import InfinityAIClient, InfinityAIError
from research_brain import generate
from research_contract import ResearchFingerprint, validate_record

ROOT = Path(__file__).resolve().parent


class StubRuntime:
    def reason(self, _prompt, _context):
        return {
            "schema": "infinity/reason-result/v1", "role": "REASONER",
            "model": "fake-local-gemma", "output": "Local Gemma research.",
            "evidenceState": "INFERRED",
        }

    def propose_research_tool(self, _prompt, token_id):
        return {
            "proposal": {"name": "research.expand_token", "arguments": {"token_id": token_id}},
            "executed": False, "requiresApplicationValidation": True,
        }


class ResearchBrainTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
            PRAGMA foreign_keys=ON;
            CREATE TABLE tokens (
                token_id TEXT PRIMARY KEY, repository TEXT, commit_sha TEXT,
                commit_message TEXT, current_classification TEXT
            );
        """)
        self.conn.executescript((ROOT / "research_streams_schema.sql").read_text())
        self.conn.executemany(
            "INSERT INTO tokens VALUES (?,?,?,?,?)",
            [
                ("ICT-A", "www-infinity4/Bitcoin-Crusher", "a" * 40, "Add novelty research", "NON_SPACEX"),
                ("ICT-B", "www-infinity4/Octave", "b" * 40, "Add research portal", "NON_SPACEX"),
            ],
        )

    def tearDown(self):
        self.conn.close()

    def test_generates_both_streams_and_fingerprints(self):
        result = generate(self.conn, "ICT-A")
        self.assertIsNotNone(result["project_entry"])
        self.assertIsNotNone(result["discovery_entry"])
        rows = self.conn.execute(
            "SELECT stream_type,evidence_level,model_or_engine FROM research_stream_entries ORDER BY entry_id"
        ).fetchall()
        self.assertEqual({row["stream_type"] for row in rows}, {"PROJECT_RESEARCH", "INFINITY_DISCOVERY_RESEARCH"})
        self.assertTrue(all(row["evidence_level"] == "INFERRED" for row in rows))
        self.assertTrue(all("deterministic" in row["model_or_engine"] for row in rows))
        hashes = self.conn.execute("SELECT * FROM research_novelty_fingerprints").fetchall()
        self.assertEqual(len(hashes), 2)
        self.assertTrue(all(row["query_hash"] and row["article_hash"] and row["token_lineage_hash"] for row in hashes))

    def test_repeated_project_query_is_marked_duplicate(self):
        generate(self.conn, "ICT-A")
        generate(self.conn, "ICT-A")
        row = self.conn.execute(
            """SELECT novelty_status,duplicate_of_entry_id,matched_on
               FROM research_novelty_fingerprints
               WHERE stream_type='PROJECT_RESEARCH' ORDER BY entry_id DESC LIMIT 1"""
        ).fetchone()
        self.assertEqual(row["novelty_status"], "DUPLICATE")
        self.assertIsNotNone(row["duplicate_of_entry_id"])
        self.assertEqual(row["matched_on"], "query_hash")

    def test_runtime_output_stays_inferred_and_tool_is_not_executed(self):
        result = generate(self.conn, "ICT-A", StubRuntime())
        row = self.conn.execute(
            "SELECT body,evidence_level,model_or_engine,structured_json FROM research_stream_entries WHERE entry_id=?",
            (result["project_entry"],),
        ).fetchone()
        self.assertEqual(row["body"], "Local Gemma research.")
        self.assertEqual(row["evidence_level"], "INFERRED")
        self.assertIn("REASONER:fake-local-gemma", row["model_or_engine"])
        self.assertFalse(json.loads(row["structured_json"])["tool_proposal"]["executed"])

    def test_external_verification_requires_sources(self):
        with self.assertRaises(ValueError):
            validate_record("PROJECT_RESEARCH", "EXTERNALLY_VERIFIED", [])
        validate_record("PROJECT_RESEARCH", "EXTERNALLY_VERIFIED", ["https://example.test/source"])

    def test_source_set_hash_is_order_independent(self):
        left = ResearchFingerprint.build("Q", ["B", "A"], "Article", ["T"])
        right = ResearchFingerprint.build("q", ["a", "b"], "article", ["t"])
        self.assertEqual(left, right)

    def test_client_rejects_evidence_escalation(self):
        client = InfinityAIClient()
        client._post = lambda *_args: {
            "schema": "infinity/reason-result/v1", "role": "REASONER",
            "model": "bad", "output": "claim", "evidenceState": "EXTERNALLY_VERIFIED",
        }
        with self.assertRaises(InfinityAIError):
            client.reason("prompt", {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
