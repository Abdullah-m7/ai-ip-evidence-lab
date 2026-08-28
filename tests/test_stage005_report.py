import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/stage005_cross_validator.json"


class Stage005ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_stage_passes_all_acceptance_gates(self):
        self.assertEqual(self.report["result"], "PASS")
        self.assertTrue(self.report["all_acceptance_gates_pass"])
        self.assertTrue(all(self.report["acceptance"].values()))
        self.assertTrue(all(isinstance(v, bool) for v in self.report["acceptance"].values()))

    def test_cross_version_not_cross_implementation(self):
        self.assertEqual(self.report["toolchains"]["generator_reader"]["engine_version_observed"], "0.90.16")
        self.assertEqual(self.report["toolchains"]["cross_validator"]["engine_version_observed"], "0.78.0")
        self.assertEqual(self.report["implementation_diversity"], "IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED")

    def test_three_corruptions_agree(self):
        self.assertEqual(self.report["attack_agreement"], {
            "assertion_corrupt": True,
            "asset_mutated": True,
            "signature_corrupt": True,
        })

    def test_trust_boundary_is_independent_of_crypto(self):
        default = self.report["trust_boundary"]["default"]
        custom = self.report["trust_boundary"]["custom"]
        self.assertEqual(default["signer_trust"], "untrusted")
        self.assertEqual(custom["signer_trust"], "trusted")
        self.assertEqual(default["cryptographic_validity"], "valid")
        self.assertEqual(custom["cryptographic_validity"], "valid")

    def test_legal_failures_survive_trust_change(self):
        legal = self.report["legal_boundary"]
        self.assertFalse(legal["legal_fields_overwritten"])
        for key, value in legal.items():
            if key != "legal_fields_overwritten":
                self.assertEqual(value, "FAIL_EVIDENCE_GATE")

    def test_reproducibility_repair_is_disclosed(self):
        cross = self.report["toolchains"]["cross_validator"]
        self.assertTrue(cross["compatibility_repair"])
        self.assertEqual(cross["declared_profile_commit_unavailable"], "c43d11162c27c5e992c7010fc75b72bb3e5520e1")

    def test_no_article_30_3_delegation(self):
        self.assertEqual(self.report["article_30_3_fields_newly_delegated"], [])


if __name__ == "__main__":
    unittest.main()
