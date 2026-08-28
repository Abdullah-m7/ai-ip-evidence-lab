import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Stage004ReportTests(unittest.TestCase):
    def test_source_fixture_hash_is_frozen(self):
        raw = (ROOT / "examples/stage004/source.jpg").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "652c561108a2961573a7dd10f720033359f650453ef33694f7dbc5fee29aae5e")
        self.assertIn(b"STAGE004-MUTATION-ANCHOR", raw)

    def test_committed_report_passes_all_acceptance_gates(self):
        report = json.loads((ROOT / "reports/stage004_conformant_c2pa.json").read_text())
        self.assertTrue(report["all_acceptance_gates_pass"])
        self.assertTrue(all(report["acceptance"].values()))
        self.assertEqual(report["article_30_3_fields_newly_delegated"], [])

    def test_committed_report_preserves_legal_boundary(self):
        report = json.loads((ROOT / "reports/stage004_conformant_c2pa.json").read_text())
        self.assertEqual(report["allowed_plus_unlawful_acquisition"]["legal_gate"]["outcome"], "FAIL_EVIDENCE_GATE")
        self.assertEqual(report["allowed_plus_no_output_permission"]["legal_gate"]["outcome"], "FAIL_EVIDENCE_GATE")
        self.assertFalse(report["allowed_plus_unlawful_acquisition"]["legal_fields_overwritten"])


if __name__ == "__main__":
    unittest.main()
