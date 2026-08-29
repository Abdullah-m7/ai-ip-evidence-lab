import json
import unittest
from pathlib import Path

from src.ipel.semantic_equivalence import canonical_sha256

ROOT = Path(__file__).resolve().parents[1]


class Stage013RubricLockTests(unittest.TestCase):
    def test_pre_outcome_lock_matches_frozen_sources(self):
        rubric = json.loads((ROOT / "benchmarks/stage013/rubric_definition.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "benchmarks/stage013/candidate_registry.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "benchmarks/stage013/rubric_lock.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["status"], "PRE_OUTCOME_RUBRIC_LOCK")
        self.assertTrue(lock["locked_before_candidate_assessment"])
        self.assertFalse(lock["benchmark_executed"])
        self.assertFalse(lock["candidate_outcomes_present"])
        self.assertEqual(lock["rubric_definition_canonical_sha256"], canonical_sha256(rubric))
        self.assertEqual(lock["candidate_registry_canonical_sha256"], canonical_sha256(registry))
        self.assertEqual(lock["source_commit_sha"], "037070dae5a93a1ef58c806a537784f378226998")

    def test_registry_contains_no_outcomes(self):
        registry = json.loads((ROOT / "benchmarks/stage013/candidate_registry.json").read_text(encoding="utf-8"))
        self.assertFalse(registry["benchmark_executed"])
        forbidden = {"SAFE_DELEGATION", "PARTIAL_SUPPORT", "NOT_SAFE_TO_DELEGATE", "NO_CANDIDATE_RESULT"}
        text = json.dumps(registry)
        self.assertFalse(any(token in text for token in forbidden))
        self.assertTrue(all(row["assessment_status"] == "NOT_RUN" for row in registry["candidates"]))

    def test_report_disclaims_new_delegation_result(self):
        text = (ROOT / "reports/STAGE_013_RUBRIC_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("produces **no replacement for the historical `0/4` result**", text)
        self.assertIn("legacy v0.1 result", text)


if __name__ == "__main__":
    unittest.main()
