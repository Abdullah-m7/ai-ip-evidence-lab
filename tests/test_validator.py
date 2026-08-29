import copy
import json
import unittest
from pathlib import Path

from src.ipel.validator import (
    CURRENT_PROFILE_ID,
    FAIL,
    LEGACY_PROFILE_ID,
    PASS,
    REVIEW,
    evaluate,
)

ROOT = Path(__file__).resolve().parents[1]


def load_example(name: str):
    return json.loads((ROOT / "examples" / "records" / name).read_text(encoding="utf-8"))


class EvidenceGateTests(unittest.TestCase):
    # Historical 0.1 behavior remains reproducible, but is now machine-labelled
    # as a legacy/incomplete legal profile rather than silently described as the
    # complete Saudi AI-development pathway.
    def test_complete_synthetic_legacy_record_preserves_historical_gate(self):
        result = evaluate(load_example("valid.json"))
        self.assertEqual(result.outcome, PASS)
        self.assertEqual(result.legal_profile_id, LEGACY_PROFILE_ID)
        self.assertFalse(result.declared_scope_complete)

    def test_current_art37_profile_passes_with_supported_assessments(self):
        result = evaluate(load_example("valid_v020_art37.json"))
        self.assertEqual(result.outcome, PASS)
        self.assertEqual(result.legal_profile_id, CURRENT_PROFILE_ID)
        self.assertTrue(result.declared_scope_complete)
        self.assertFalse(result.to_dict()["legal_conclusion"])

    def test_current_profile_missing_article37_context_fails_contract(self):
        record = load_example("valid_v020_art37.json")
        del record["article37_context"]
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertTrue(any(f.rule == "IPEL-CONTRACT" and "article37_context" in f.message for f in result.findings))

    def test_art37_normal_exploitation_conflict_fails(self):
        record = load_example("valid_v020_art37.json")
        record["article37_context"]["normal_exploitation_conflict"] = "conflict"
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertTrue(any(f.rule == "LAW-37(1)" and f.severity == "FAIL" for f in result.findings))

    def test_art37_unjustified_rightsholder_prejudice_fails(self):
        record = load_example("valid_v020_art37.json")
        record["article37_context"]["rightsholder_legitimate_interests_prejudice"] = "unjustified"
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertTrue(any(f.rule == "LAW-37(1)" and f.severity == "FAIL" for f in result.findings))

    def test_art37_unresolved_assessment_requires_review(self):
        record = load_example("valid_v020_art37.json")
        record["article37_context"]["normal_exploitation_conflict"] = "uncertain"
        result = evaluate(record)
        self.assertEqual(result.outcome, REVIEW)
        self.assertTrue(any(f.rule == "LAW-37(1)" and f.severity == "REVIEW" for f in result.findings))

    def test_art37_favorable_assertion_without_basis_requires_review(self):
        record = load_example("valid_v020_art37.json")
        record["article37_context"]["normal_exploitation_basis"] = []
        result = evaluate(record)
        self.assertEqual(result.outcome, REVIEW)
        self.assertTrue(any(f.rule == "LAW-37(1)" and "no recorded basis" in f.message for f in result.findings))

    def test_art37_rightsholder_favorable_assertion_without_basis_requires_review(self):
        record = load_example("valid_v020_art37.json")
        record["article37_context"]["rightsholder_interests_basis"] = []
        result = evaluate(record)
        self.assertEqual(result.outcome, REVIEW)
        self.assertTrue(any(f.rule == "LAW-37(1)" and "no recorded basis" in f.message for f in result.findings))

    def test_art37_is_not_inferred_from_ir30_commercial_impact_field(self):
        record = load_example("valid_v020_art37.json")
        # A favorable IR-30(2) field must not cure an explicit Art. 37 conflict.
        record["use"]["normal_exploitation_impact"] = "none"
        record["article37_context"]["normal_exploitation_conflict"] = "conflict"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_art37_rightsholder_interest_is_not_inferred_from_author_interest_field(self):
        record = load_example("valid_v020_art37.json")
        record["rights_context"]["legitimate_interests_prejudice"] = "none"
        record["article37_context"]["rightsholder_legitimate_interests_prejudice"] = "unjustified"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_unknown_record_version_fails_contract(self):
        record = load_example("valid_v020_art37.json")
        record["record_version"] = "9.9.9"
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertEqual(result.legal_profile_id, "unsupported-record-profile")
        self.assertFalse(result.declared_scope_complete)

    def test_missing_article_30_3_source_fails(self):
        self.assertEqual(evaluate(load_example("invalid_missing_source.json")).outcome, FAIL)

    def test_unverified_acquisition_requires_review(self):
        record = load_example("valid.json")
        record["work"]["acquisition_status"] = "unverified"
        record["evidence"]["acquisition"] = []
        self.assertEqual(evaluate(record).outcome, REVIEW)

    def test_unknown_publication_state_fails_contract(self):
        record = load_example("valid.json")
        record["work"]["publication_status"] = "unknown"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_explicit_unlawful_acquisition_fails(self):
        record = load_example("valid.json")
        record["work"]["acquisition_status"] = "false"
        self.assertEqual(evaluate(record).outcome, FAIL)

    def test_unknown_acquisition_state_fails_contract(self):
        record = load_example("valid.json")
        record["work"]["acquisition_status"] = "unknown"
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertTrue(any(f.rule == "IPEL-CONTRACT" for f in result.findings))

    def test_missing_prohibited_use_flag_fails_contract(self):
        record = load_example("valid.json")
        del record["use"]["distribution"]
        result = evaluate(record)
        self.assertEqual(result.outcome, FAIL)
        self.assertTrue(any(f.rule == "IPEL-CONTRACT" for f in result.findings))

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

    def test_favorable_market_assessment_without_basis_requires_review(self):
        record = load_example("valid.json")
        record["rights_context"]["impact_assessment_basis"] = []
        self.assertEqual(evaluate(record).outcome, REVIEW)

    def test_independent_rights_assessment_without_basis_requires_review(self):
        record = load_example("valid.json")
        record["rights_context"]["independent_elements_basis"] = []
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
