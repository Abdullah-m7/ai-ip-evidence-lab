import json
import unittest
from pathlib import Path

from src.ipel.reviewer_benchmark import (
    NOT_READY,
    READY,
    audit_benchmark,
    available_facts,
    build_form,
    decision_matrix,
    render_baseline,
    render_ipel,
    score_responses,
)

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "benchmarks/stage006/case_spec.json"


class ReviewerBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        cls.base = json.loads((ROOT / cls.spec["base_record"]).read_text(encoding="utf-8"))
        cls.form_a, cls.manifest_a, cls.latent_a = build_form(cls.spec, cls.base, "A")
        cls.form_b, cls.manifest_b, cls.latent_b = build_form(cls.spec, cls.base, "B")
        cls.audit = audit_benchmark(
            cls.spec,
            {"A": cls.form_a, "B": cls.form_b},
            cls.manifest_a + cls.manifest_b,
            {"A": cls.latent_a, "B": cls.latent_b},
        )
        cls.answer_key = {
            entry.packet_id: entry.to_dict() for entry in cls.manifest_a + cls.manifest_b
        }

    def test_structural_audit_passes(self):
        self.assertTrue(self.audit["all_acceptance_gates_pass"])
        self.assertTrue(all(self.audit["acceptance"].values()))
        self.assertEqual(self.audit["case_count"], 24)

    def test_every_case_swaps_presentation_between_forms(self):
        a = {entry.case_id: entry.presentation for entry in self.manifest_a}
        b = {entry.case_id: entry.presentation for entry in self.manifest_b}
        self.assertEqual(set(a), set(b))
        self.assertTrue(all(a[case] != b[case] for case in a))

    def test_forms_are_balanced(self):
        self.assertEqual(self.audit["form_a_readiness_counts"], {READY: 12, NOT_READY: 12})
        self.assertEqual(self.audit["form_a_stratum_counts"], {"objective": 12, "judgment_sensitive": 12})
        self.assertEqual(self.audit["form_a_presentation_counts"], {"BASELINE": 12, "IPEL": 12})
        self.assertTrue(all(value == 3 for value in self.audit["form_a_cell_counts"].values()))

    def test_article_30_3_missingness_dimensions_are_covered(self):
        missing = {code for case in self.spec["cases"] for code in case["missing_fact_codes"]}
        self.assertTrue({"WORK_TYPE", "WORK_SOURCE", "USE_PURPOSE", "USE_DATE"}.issubset(missing))

    def test_ready_is_not_machine_compliance(self):
        self.assertGreaterEqual(len(self.audit["ready_cases_with_machine_fail"]), 1)
        ready_fail = next(
            entry for entry in self.manifest_a
            if entry.readiness == READY and entry.machine_gate_outcome == "FAIL_EVIDENCE_GATE"
        )
        response = [{
            "packet_id": ready_fail.packet_id,
            "decision": "READY",
            "missing_information_codes": [],
            "confidence_0_to_100": 90,
            "assessment_seconds": 30,
        }]
        scored = score_responses(response, self.answer_key)
        self.assertTrue(scored["rows"][0]["readiness_correct"])
        self.assertFalse(scored["rows"][0]["false_ready"])

    def test_renderer_factual_parity_is_exact(self):
        for case_id, record in self.latent_a.items():
            facts = available_facts(record)
            baseline = render_baseline(facts)
            ipel = render_ipel(facts)
            self.assertEqual(baseline["represented_fact_paths"], sorted(facts), case_id)
            self.assertEqual(ipel["represented_fact_paths"], sorted(facts), case_id)

    def test_visible_packets_contain_no_answer_labels(self):
        visible = json.dumps({"A": self.form_a, "B": self.form_b}, ensure_ascii=False)
        for forbidden in (READY, NOT_READY, '"case_id"', '"missing_fact_codes"', "judgment_sensitive", "objective"):
            self.assertNotIn(forbidden, visible)
        self.assertIn("missing_information_codes", visible)

    def test_perfect_synthetic_fixture_scores_perfectly(self):
        fixture = json.loads(
            (ROOT / "benchmarks/stage006/generated/synthetic_responses/perfect_form_a.json").read_text(encoding="utf-8")
        )
        self.assertTrue(fixture["synthetic_nonhuman"])
        scored = score_responses(fixture["responses"], self.answer_key)
        self.assertEqual(scored["overall"]["readiness_accuracy"], 1.0)
        self.assertEqual(scored["overall"]["false_ready_rate"], 0.0)
        self.assertEqual(scored["overall"]["missing_information_recall_micro"], 1.0)
        self.assertEqual(scored["overall"]["missing_information_precision_micro"], 1.0)
        self.assertEqual(scored["overall"]["mean_missing_fact_recall_not_ready"], 1.0)

    def test_duplicate_packet_response_is_rejected(self):
        entry = self.manifest_a[0]
        response = {
            "packet_id": entry.packet_id,
            "decision": "READY",
            "missing_information_codes": [],
            "confidence_0_to_100": 80,
            "assessment_seconds": 20,
        }
        from src.ipel.reviewer_benchmark import BenchmarkError
        with self.assertRaises(BenchmarkError):
            score_responses([response, dict(response)], self.answer_key)

    def test_invalid_timing_and_confidence_are_rejected(self):
        entry = self.manifest_a[0]
        from src.ipel.reviewer_benchmark import BenchmarkError
        base = {"packet_id": entry.packet_id, "decision": "READY", "missing_information_codes": []}
        with self.assertRaises(BenchmarkError):
            score_responses([{**base, "confidence_0_to_100": 101}], self.answer_key)
        with self.assertRaises(BenchmarkError):
            score_responses([{**base, "assessment_seconds": -1}], self.answer_key)

    def test_decision_matrix_supports_agreement_analysis(self):
        perfect = json.loads(
            (ROOT / "benchmarks/stage006/generated/synthetic_responses/perfect_form_a.json").read_text(encoding="utf-8")
        )["responses"]
        noisy = json.loads(
            (ROOT / "benchmarks/stage006/generated/synthetic_responses/noisy_form_a.json").read_text(encoding="utf-8")
        )["responses"]
        matrix = decision_matrix({"synthetic-perfect": perfect, "synthetic-noisy": noisy}, self.answer_key)
        self.assertEqual(len(matrix["matrix"]), 24)
        self.assertEqual(len(matrix["pairwise_agreement"]), 1)
        self.assertEqual(matrix["pairwise_agreement"][0]["shared_packets"], 24)


if __name__ == "__main__":
    unittest.main()
