#!/usr/bin/env python3
import json
import sqlite3
import unittest
from pathlib import Path

from token_package import build_package

ROOT = Path(__file__).resolve().parent


class FakeGitHub:
    def pull_requests_for_commit(self, _repository, _sha):
        return [{
            "number": 20, "title": "Connect research package", "body": "Adds keywords and archive media.",
            "html_url": "https://github.test/repo/pull/20", "state": "closed",
            "base": {"ref": "main"}, "head": {"ref": "agent/package"},
            "merge_commit_sha": "c" * 40, "changed_files": 4, "additions": 200, "deletions": 3,
        }]

    def pull_request_details(self, _repository, _number):
        return self.pull_requests_for_commit(None, None)[0]

    def pull_request_reviews(self, _repository, _number):
        return [{"id": 1, "state": "APPROVED", "body": "Validated", "html_url": "https://github.test/review/1"}]

    def check_runs(self, _repository, _sha):
        return [{"name": "tests", "status": "completed", "conclusion": "success", "details_url": "https://github.test/check/1"}]


class FakeArchive:
    def search(self, _query, mediatype, _rows):
        if mediatype == "movies":
            return [{"identifier": "public-movie", "title": "Public Movie"}]
        return [{"identifier": "unclear-song", "title": "Unclear Song"}]

    def metadata(self, identifier):
        if identifier == "public-movie":
            return {
                "metadata": {"identifier": identifier, "rights": "Public Domain"},
                "files": [{"name": "movie.mp4", "format": "MPEG4"}],
            }
        return {
            "metadata": {"identifier": identifier, "rights": "Uploader supplied no reusable license"},
            "files": [{"name": "song.mp3", "format": "VBR MP3"}],
        }


class TokenPackageTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
            CREATE TABLE tokens (
                token_id TEXT PRIMARY KEY, repository TEXT, commit_sha TEXT,
                commit_url TEXT, commit_message TEXT, parent_shas TEXT,
                current_classification TEXT
            );
        """)
        self.conn.executescript((ROOT / "research_streams_schema.sql").read_text())
        self.conn.executescript((ROOT / "token_package_schema.sql").read_text())
        self.conn.executemany("INSERT INTO tokens VALUES (?,?,?,?,?,?,?)", [
            ("ICT-A", "www-infinity4/INFINITY", "a" * 40, "https://github.test/a", "Add token research package", "[]", "NON_SPACEX"),
            ("ICT-B", "www-infinity4/Octave", "b" * 40, "https://github.test/b", "Build research portal", "[]", "NON_SPACEX"),
        ])

    def tearDown(self):
        self.conn.close()

    def test_builds_complete_provenance_package(self):
        package = build_package(
            self.conn, "ICT-A",
            user_keywords=["hydrogen doorway"],
            history_texts=["electron cloud logic and quantum research"],
            cross_input_texts=["movie archive research article"],
            github=FakeGitHub(), archive=FakeArchive(),
        )
        self.assertEqual(package["schema"], "infinity/token-package/v1")
        self.assertTrue(package["research"]["project_entry_id"])
        self.assertTrue(package["research"]["discovery_entry_id"])
        self.assertEqual(package["pull_request_count"], 1)
        self.assertEqual(package["media_candidate_count"], 2)
        self.assertRegex(package["manifest_sha256"], r"^[a-f0-9]{64}$")
        self.assertIsNone(package["utility"]["market_value_microunits"])
        self.assertGreaterEqual(package["utility"]["reference_microunits"], 2_000_000)
        pr = self.conn.execute("SELECT * FROM token_pr_context WHERE token_id='ICT-A'").fetchone()
        self.assertEqual(pr["changed_files"], 4)
        self.assertEqual(json.loads(pr["review_summary_json"])[0]["state"], "APPROVED")
        self.assertEqual(json.loads(pr["check_summary_json"])[0]["conclusion"], "success")

    def test_keywords_keep_explainable_sources(self):
        build_package(
            self.conn, "ICT-A", user_keywords=["hydrogen doorway"],
            history_texts=["electron cloud logic"], cross_input_texts=["archive movie"],
        )
        rows = self.conn.execute(
            "SELECT source_type,source_ref,evidence_level FROM token_keywords WHERE token_id='ICT-A'"
        ).fetchall()
        sources = {row["source_type"] for row in rows}
        self.assertTrue({"USER", "COMMIT", "HISTORY", "CROSS_INPUT"}.issubset(sources))
        self.assertTrue(all(row["source_ref"] for row in rows))
        self.assertIn("USER_DEFINED", {row["evidence_level"] for row in rows})

    def test_unlicensed_media_cannot_add_usable_reference(self):
        package = build_package(self.conn, "ICT-A", user_keywords=["archive"], archive=FakeArchive())
        media = self.conn.execute(
            "SELECT media_type,rights_status FROM token_media_candidates ORDER BY media_type"
        ).fetchall()
        self.assertEqual(dict(media)["MOVIE"], "VERIFIED_REUSE")
        self.assertEqual(dict(media)["SONG"], "REVIEW_REQUIRED")
        song = self.conn.execute(
            "SELECT usable FROM token_utility_components WHERE component_type='SONG_ACCESS'"
        ).fetchone()
        self.assertEqual(song["usable"], 0)
        self.assertEqual(package["status"], "REVIEW_REQUIRED")

    def test_manifest_is_deterministic_for_same_database_state(self):
        first = build_package(self.conn, "ICT-A", user_keywords=["research"])
        second = build_package(self.conn, "ICT-A", user_keywords=["research"])
        self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
        self.assertEqual(json.loads(self.conn.execute(
            "SELECT manifest_json FROM token_packages WHERE token_id='ICT-A'"
        ).fetchone()[0])["canonical_identity"], "ICT|www-infinity4/INFINITY|" + "a" * 40)


if __name__ == "__main__":
    unittest.main(verbosity=2)
