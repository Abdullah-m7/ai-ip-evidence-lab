import json
import unittest
from pathlib import Path

from src.ipel.c2pa_profile import ProfileError, from_profile, roundtrip_metrics, validate_profile
from src.ipel.validator import FAIL, PASS, evaluate

ROOT = Path(__file__).resolve().parents[1]


class Stage003FixtureTests(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / "examples/profiles" / name).read_text())

    def test_committed_clean_profile_is_lossless(self):
        profile = self.load("stage003_clean.json")
        rebuilt = from_profile(profile)
        self.assertEqual(evaluate(rebuilt).outcome, PASS)
        self.assertEqual(roundtrip_metrics(rebuilt, profile).semantic_loss_count, 0)

    def test_allowed_signal_does_not_cure_unlawful_acquisition_fixture(self):
        profile = self.load("stage003_allowed_unlawful_acquisition.json")
        rebuilt = from_profile(profile)
        self.assertEqual(profile["c2pa"]["tdm_assertion"]["entries"]["cawg.ai_training"]["use"], "allowed")
        self.assertEqual(profile["c2pa"]["validation_signals"]["trust_state"], "trusted")
        self.assertEqual(rebuilt["work"]["acquisition_status"], "false")
        self.assertEqual(evaluate(rebuilt).outcome, FAIL)

    def test_missing_jurisdictional_source_fixture_fails_profile_contract(self):
        profile = self.load("stage003_missing_source.json")
        self.assertTrue(validate_profile(profile))
        with self.assertRaises(ProfileError):
            from_profile(profile)

    def test_machine_report_meets_stage003_acceptance_gates(self):
        report = json.loads((ROOT / "reports/stage003_semantic_roundtrip.json").read_text())
        self.assertTrue(report["all_valid_profiles_zero_duplicate_generic_fields"])
        self.assertTrue(report["all_roundtrips_zero_semantic_loss"])
        self.assertTrue(report["all_article_30_3_tuples_preserved"])
        self.assertTrue(report["all_gate_outcomes_preserved"])
        self.assertEqual(report["article_30_3_fields_carried_by_c2pa"], [])
        self.assertEqual(len(report["article_30_3_fields_retained_jurisdictionally"]), 4)
        self.assertFalse(report["representation_is_conformant_manifest"])


if __name__ == "__main__":
    unittest.main()
