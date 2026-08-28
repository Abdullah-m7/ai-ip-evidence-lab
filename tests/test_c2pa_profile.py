import copy
import json
import unittest
from pathlib import Path

from src.ipel.c2pa_profile import (
    INTERPRETATION_BARRIERS,
    ProfileError,
    article_30_3_tuple,
    from_profile,
    roundtrip_metrics,
    semantic_loss,
    to_profile,
    validate_profile,
)
from src.ipel.validator import FAIL, PASS, REVIEW, evaluate

ROOT = Path(__file__).resolve().parents[1]
VALID = json.loads((ROOT / "examples/records/valid.json").read_text())


class C2PAProfileTests(unittest.TestCase):
    def test_clean_roundtrip_is_lossless_and_gate_preserving(self):
        profile = to_profile(VALID)
        rebuilt = from_profile(profile)
        metrics = roundtrip_metrics(VALID, profile)
        self.assertEqual(semantic_loss(VALID, rebuilt), [])
        self.assertTrue(metrics.article_30_3_preserved)
        self.assertTrue(metrics.gate_preserved)
        self.assertEqual(metrics.original_gate, PASS)
        self.assertEqual(metrics.duplicate_generic_field_count, 0)

    def test_article_30_3_tuple_crosses_both_layers(self):
        profile = to_profile(VALID)
        rebuilt = from_profile(profile)
        self.assertEqual(article_30_3_tuple(rebuilt), article_30_3_tuple(VALID))
        self.assertIn("source", profile["ipel_jurisdictional"]["work"])
        self.assertIn("date", profile["ipel_jurisdictional"]["use"])
        self.assertNotIn("title", profile["ipel_jurisdictional"]["work"])
        self.assertIn("sha256", profile["ipel_jurisdictional"]["work"])

    def test_trusted_allowed_does_not_cure_unlawful_acquisition(self):
        record = copy.deepcopy(VALID)
        record["work"]["acquisition_status"] = "false"
        profile = to_profile(record, tdm_use="allowed", manifest_state="valid", trust_state="trusted")
        rebuilt = from_profile(profile)
        self.assertEqual(rebuilt["work"]["acquisition_status"], "false")
        self.assertEqual(evaluate(rebuilt).outcome, FAIL)

    def test_trusted_manifest_does_not_verify_publication(self):
        record = copy.deepcopy(VALID)
        record["work"]["publication_status"] = "unverified"
        profile = to_profile(record, tdm_use="allowed", manifest_state="valid", trust_state="trusted")
        rebuilt = from_profile(profile)
        self.assertEqual(rebuilt["work"]["publication_status"], "unverified")
        self.assertEqual(evaluate(rebuilt).outcome, REVIEW)

    def test_allowed_tdm_does_not_grant_output_permission(self):
        record = copy.deepcopy(VALID)
        record["output_context"]["permission_status"] = "not_granted"
        profile = to_profile(record, tdm_use="allowed")
        rebuilt = from_profile(profile)
        self.assertEqual(rebuilt["output_context"]["permission_status"], "not_granted")

    def test_barriers_are_contractual(self):
        profile = to_profile(VALID)
        self.assertEqual(profile["interpretation_barriers"], INTERPRETATION_BARRIERS)
        profile["interpretation_barriers"] = []
        self.assertTrue(validate_profile(profile))
        with self.assertRaises(ProfileError):
            from_profile(profile)

    def test_duplicate_generic_field_is_rejected(self):
        profile = to_profile(VALID)
        profile["ipel_jurisdictional"]["work"]["title"] = "Duplicated title"
        self.assertTrue(any("duplicate generic field" in e for e in validate_profile(profile)))

    def test_field_map_tampering_is_rejected(self):
        profile = to_profile(VALID)
        profile["field_map"] = {"work.source": "c2pa.ingredient.informationalURI"}
        with self.assertRaises(ProfileError):
            from_profile(profile)

    def test_manifest_and_signal_contract_fails_closed(self):
        profile = to_profile(VALID)
        profile["c2pa"]["manifest_ref"] = ""
        profile["c2pa"]["validation_signals"]["trust_state"] = None
        errors = validate_profile(profile)
        self.assertTrue(any("manifest_ref" in e for e in errors))
        self.assertTrue(any("trust_state" in e for e in errors))

    def test_missing_jurisdictional_source_fails_closed(self):
        profile = to_profile(VALID)
        del profile["ipel_jurisdictional"]["work"]["source"]
        with self.assertRaises(ProfileError):
            from_profile(profile)

    def test_fail_outcome_survives_roundtrip(self):
        record = copy.deepcopy(VALID)
        record["use"]["distribution"] = True
        profile = to_profile(record)
        metrics = roundtrip_metrics(record, profile)
        self.assertEqual(metrics.original_gate, FAIL)
        self.assertEqual(metrics.reconstructed_gate, FAIL)
        self.assertTrue(metrics.gate_preserved)


if __name__ == "__main__":
    unittest.main()
