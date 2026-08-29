import copy
import json
import unittest
from pathlib import Path

from src.ipel.semantic_equivalence import (
    NO_CANDIDATE,
    NOT_SAFE,
    PARTIAL,
    SAFE,
    SemanticEquivalenceError,
    canonical_sha256,
    classify_assessment,
    validate_assessment,
)

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = json.loads((ROOT / "benchmarks/stage013/rubric_definition.json").read_text(encoding="utf-8"))
REGISTRY = json.loads((ROOT / "benchmarks/stage013/candidate_registry.json").read_text(encoding="utf-8"))


def candidate(cid: str):
    return next(item for item in REGISTRY["candidates"] if item["candidate_id"] == cid)


def assessment_for(cand, *, status="PASS", roundtrip=True, support=False, deps=None):
    if cand["candidate_kind"] == "NO_CANDIDATE":
        return {
            "rubric_version": "1.0.0",
            "candidate_id": cand["candidate_id"],
            "proposition_class": cand["proposition_class"],
            "candidate_kind": cand["candidate_kind"],
            "dimension_assessments": {},
            "roundtrip_tested": False,
            "roundtrip_pass": None,
            "support_relevance": False,
            "inference_dependencies": [],
            "assessment_notes": "synthetic unit-test no-candidate assessment",
        }
    na = set(RUBRIC["proposition_classes"][cand["proposition_class"]]["not_applicable_allowed"])
    dims = {}
    for item in RUBRIC["dimensions"]:
        dim_status = "NOT_APPLICABLE" if item["id"] in na else status
        dims[item["id"]] = {"status": dim_status, "rationale": "synthetic unit-test rationale", "evidence_refs": ["spec://unit-test"]}
    return {
        "rubric_version": "1.0.0",
        "candidate_id": cand["candidate_id"],
        "proposition_class": cand["proposition_class"],
        "candidate_kind": cand["candidate_kind"],
        "dimension_assessments": dims,
        "roundtrip_tested": roundtrip,
        "roundtrip_pass": True if roundtrip else None,
        "support_relevance": support,
        "inference_dependencies": deps or [],
        "assessment_notes": "synthetic unit-test assessment",
    }


class SemanticEquivalenceRubricTests(unittest.TestCase):
    def test_registry_is_preregistered_without_outcomes(self):
        self.assertFalse(REGISTRY["benchmark_executed"])
        self.assertGreaterEqual(len(REGISTRY["candidates"]), 10)
        self.assertTrue(all(c["assessment_status"] == "NOT_RUN" for c in REGISTRY["candidates"]))

    def test_missing_dimension_fails_closed(self):
        cand = candidate("use-date__c2pa-action-when")
        a = assessment_for(cand)
        del a["dimension_assessments"]["temporal_semantics"]
        with self.assertRaises(SemanticEquivalenceError):
            validate_assessment(a, RUBRIC, cand)

    def test_not_applicable_cannot_be_invented_for_event_attribute(self):
        cand = candidate("use-date__c2pa-action-when")
        a = assessment_for(cand)
        a["dimension_assessments"]["temporal_semantics"]["status"] = "NOT_APPLICABLE"
        with self.assertRaises(SemanticEquivalenceError):
            validate_assessment(a, RUBRIC, cand)

    def test_all_passed_normative_mapping_with_roundtrip_can_be_safe(self):
        cand = candidate("work-title__c2pa-dc-title")
        result = classify_assessment(assessment_for(cand), RUBRIC, cand)
        self.assertEqual(result["decision"], SAFE)
        self.assertFalse(result["ipel_field_retained"])

    def test_single_critical_failure_can_never_be_safe(self):
        cand = candidate("use-date__c2pa-action-when")
        a = assessment_for(cand, support=True)
        a["dimension_assessments"]["temporal_semantics"]["status"] = "FAIL"
        result = classify_assessment(a, RUBRIC, cand)
        self.assertEqual(result["decision"], PARTIAL)
        self.assertTrue(result["ipel_field_retained"])

    def test_prohibited_trust_inference_blocks_safe_delegation(self):
        cand = candidate("work-title__c2pa-dc-title")
        a = assessment_for(cand, support=True, deps=["SIGNER_TRUST"])
        result = classify_assessment(a, RUBRIC, cand)
        self.assertNotEqual(result["decision"], SAFE)
        self.assertTrue(result["ipel_field_retained"])

    def test_rights_preference_inference_blocks_safe_delegation(self):
        cand = candidate("use-purpose__cawg-training-mining")
        a = assessment_for(cand, support=True, deps=["RIGHTS_PREFERENCE"])
        result = classify_assessment(a, RUBRIC, cand)
        self.assertNotEqual(result["decision"], SAFE)
        self.assertTrue(result["ipel_field_retained"])

    def test_custom_assertion_never_establishes_generic_delegation(self):
        cand = copy.deepcopy(candidate("work-title__c2pa-dc-title"))
        cand["candidate_kind"] = "CUSTOM_ASSERTION"
        a = assessment_for(cand, support=True)
        result = classify_assessment(a, RUBRIC, cand)
        self.assertEqual(result["decision"], PARTIAL)
        self.assertTrue(result["ipel_field_retained"])

    def test_roundtrip_is_mandatory_for_safe_delegation(self):
        cand = candidate("work-title__c2pa-dc-title")
        result = classify_assessment(assessment_for(cand, roundtrip=False), RUBRIC, cand)
        self.assertEqual(result["decision"], NOT_SAFE)

    def test_no_candidate_has_distinct_fail_closed_class(self):
        cand = candidate("art37-normal-exploitation__none")
        result = classify_assessment(assessment_for(cand), RUBRIC, cand)
        self.assertEqual(result["decision"], NO_CANDIDATE)
        self.assertTrue(result["ipel_field_retained"])

    def test_canonical_hash_is_order_independent(self):
        self.assertEqual(canonical_sha256({"b": 2, "a": 1}), canonical_sha256({"a": 1, "b": 2}))


if __name__ == "__main__":
    unittest.main()
