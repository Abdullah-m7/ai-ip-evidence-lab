from __future__ import annotations

import unittest
from pathlib import Path

from scripts.audit_paper_a import audit_files, audit_texts


ROOT = Path(__file__).resolve().parents[1]


class PaperAAuditTests(unittest.TestCase):
    def test_committed_manuscript_passes_claim_citation_audit(self) -> None:
        report = audit_files(
            ROOT / "manuscript/PAPER_A_DRAFT.md",
            ROOT / "manuscript/PAPER_A_REFERENCES.md",
            ROOT / "manuscript/PAPER_A_CLAIM_EVIDENCE_MATRIX.md",
        )
        self.assertTrue(report["passed"], report)
        self.assertGreaterEqual(report["word_count"], 4500)

    def test_affirmative_legal_overclaim_fails_closed(self) -> None:
        draft = (ROOT / "manuscript/PAPER_A_DRAFT.md").read_text(encoding="utf-8")
        references = (ROOT / "manuscript/PAPER_A_REFERENCES.md").read_text(encoding="utf-8")
        matrix = (ROOT / "manuscript/PAPER_A_CLAIM_EVIDENCE_MATRIX.md").read_text(encoding="utf-8")
        poisoned = draft + "\nIPEL proves legal compliance for all recorded uses.\n"
        report = audit_texts(poisoned, references, matrix)
        self.assertFalse(report["passed"])
        self.assertIn("forbidden_overclaims_absent", report["failed_checks"])

    def test_missing_implementation_limitation_fails_closed(self) -> None:
        draft = (ROOT / "manuscript/PAPER_A_DRAFT.md").read_text(encoding="utf-8")
        references = (ROOT / "manuscript/PAPER_A_REFERENCES.md").read_text(encoding="utf-8")
        matrix = (ROOT / "manuscript/PAPER_A_CLAIM_EVIDENCE_MATRIX.md").read_text(encoding="utf-8")
        poisoned = draft.replace("IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED", "LIMIT_REMOVED")
        report = audit_texts(poisoned, references, matrix)
        self.assertFalse(report["passed"])
        self.assertIn("mandatory_boundaries", report["failed_checks"])


if __name__ == "__main__":
    unittest.main()
