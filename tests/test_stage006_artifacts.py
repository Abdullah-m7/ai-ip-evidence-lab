import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "benchmarks/stage006/generated"


class Stage006ArtifactTests(unittest.TestCase):
    def test_build_report_disclaims_human_results(self):
        report = json.loads((GENERATED / "stage006_build_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "BENCHMARK_READY_NOT_HUMAN_RESULTS")
        self.assertFalse(report["human_data_collected"])
        self.assertIsNone(report["human_effect_estimates"])
        self.assertTrue(report["all_acceptance_gates_pass"])

    def test_synthetic_score_artifacts_are_explicitly_nonhuman(self):
        for name in ("perfect_score.json", "noisy_score.json"):
            data = json.loads((GENERATED / "synthetic_responses" / name).read_text(encoding="utf-8"))
            self.assertTrue(data["synthetic_nonhuman"])
            self.assertIn("not study results", data["purpose"].lower())

    def test_hidden_answer_key_is_not_embedded_in_reviewer_forms(self):
        for form in ("form_a.json", "form_b.json"):
            text = (GENERATED / form).read_text(encoding="utf-8")
            self.assertNotIn("READY_FOR_LEGAL_EVALUATION", text)
            self.assertNotIn("NOT_READY_FOR_LEGAL_EVALUATION", text)
            self.assertNotIn('"case_id"', text)
            self.assertNotIn('"missing_fact_codes"', text)

    def test_committed_artifacts_reproduce_byte_for_byte(self):
        with tempfile.TemporaryDirectory(prefix="ipel-stage006-test-") as td:
            out = Path(td)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "experiments/stage006_build_benchmark.py"),
                    "--output-dir",
                    str(out),
                ],
                cwd=ROOT,
                env={**__import__("os").environ, "PYTHONPATH": str(ROOT)},
                check=True,
                stdout=subprocess.DEVNULL,
            )
            committed = sorted(p.relative_to(GENERATED) for p in GENERATED.rglob("*") if p.is_file())
            rebuilt = sorted(p.relative_to(out) for p in out.rglob("*") if p.is_file())
            self.assertEqual(committed, rebuilt)
            for relative in committed:
                self.assertEqual((GENERATED / relative).read_bytes(), (out / relative).read_bytes(), relative)


if __name__ == "__main__":
    unittest.main()
