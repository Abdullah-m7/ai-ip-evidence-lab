import json
import unittest
from pathlib import Path

from src.ipel.validator import FAIL, PASS, REVIEW, evaluate

ROOT = Path(__file__).resolve().parents[1]


def load_example(name: str):
    return json.loads((ROOT / "examples" / "records" / name).read_text(encoding="utf-8"))


class EvidenceGateTests(unittest.TestCase):
    def test_complete_synthetic_record_passes_evidence_gate(self):
        self.assertEqual(evaluate(load_example("valid.json")).outcome, PASS)

    def test_missing_article_30_3_source_fails(self):
        self.assertEqual(evaluate(load_example("invalid_missing_source.json")).outcome, FAIL)

    def test_unverified_acquisition_requires_review(self):
        record = load_example("valid.json")
        record["work"]["acquisition_status"] = "unverified"
        record["evidence"]["acquisition"] = []
        self.assertEqual(evaluate(record).outcome, REVIEW)

    def test_unknown_publication_state_requires_review(self):
        record = load_example("valid.json")
        record["work"]["publication_status"] = "unknown"
        self.assertEqual(evaluate(record).outcome, REVIEW)

    def test_explicit_unlawful_acquisition_fails(self):
        record = load_example("valid.json")
        record["work"]["acquisition_status"] = "false"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_direct_distribution_fails(self):
        record = load_example("valid.json")
        record["use"]["distribution"] = True
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_purely_commercial_uncertain_case_requires_review(self):
        record = load_example("valid.json")
        record["use"]["purely_commercial_context"] = True
        record["use"]["materiality_to_work"] = "uncertain"
        record["use"]["normal_exploitation_impact"] = "uncertain"
        self.assertEqual(evaluate(record).outcome, REVIEW)

    def test_unnecessary_final_output_inclusion_fails(self):
        record = load_example("valid.json")
        record["output_context"]["included_in_final_product"] = True
        record["output_context"]["inclusion_necessary"] = "no"
        record["output_context"]["permission_status"] = "not_granted"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_verified_claim_without_evidence_requires_review(self):
        record = load_example("valid.json")
        record["evidence"]["publication"] = []
        self.assertEqual(evaluate(record).outcome, REVIEW)


if __name__ == "__main__":
    unittest.main()
