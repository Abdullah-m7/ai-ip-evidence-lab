import json
import tempfile
import unittest
from pathlib import Path

from experiments.stage007_power_simulation import build_grid
from src.ipel.study_lock import (
    StudyLockError,
    build_freeze_manifest,
    validate_freeze_manifest,
    validate_study_design,
)

ROOT = Path(__file__).resolve().parents[1]


class Stage007PowerLockTests(unittest.TestCase):
    def test_power_grid_is_deterministic_and_not_a_final_n(self):
        a = build_grid(30)
        b = build_grid(30)
        self.assertEqual(a, b)
        self.assertEqual(len(a["scenarios"]), 16)
        self.assertFalse(a["human_outcomes_used"])
        self.assertFalse(a["final_sample_size_locked"])

    def test_committed_power_grid_has_no_human_outcomes(self):
        grid = json.loads((ROOT / "benchmarks/stage007/generated/power_design_grid.json").read_text())
        self.assertEqual(grid["artifact"], "POWER_DESIGN_GRID_NOT_FINAL_SAMPLE_SIZE")
        self.assertFalse(grid["human_outcomes_used"])
        self.assertFalse(grid["final_sample_size_locked"])

    def test_pre_adjudication_manifest_can_be_built_now(self):
        manifest = build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="a" * 40)
        self.assertFalse(manifest["real_adjudication_collected"])
        self.assertFalse(manifest["final_sample_size_locked"])
        validate_freeze_manifest(ROOT, manifest)

    def test_post_adjudication_lock_requires_raw_and_summary(self):
        with self.assertRaises(StudyLockError):
            build_freeze_manifest(ROOT, state="POST_ADJUDICATION_LOCK", source_commit_sha="a" * 40)

    def test_synthetic_response_set_cannot_promote_post_lock(self):
        raw = ROOT / "benchmarks/stage007/generated/synthetic_adjudication/consensus_responses.json"
        summary = ROOT / "benchmarks/stage007/generated/synthetic_adjudication/consensus_aggregate.json"
        with self.assertRaises(StudyLockError):
            build_freeze_manifest(
                ROOT, state="POST_ADJUDICATION_LOCK", source_commit_sha="a" * 40,
                real_adjudication_responses_path=raw, real_adjudication_summary_path=summary,
            )

    def test_primary_design_validator_rejects_unresolved_ethics(self):
        with self.assertRaises(StudyLockError):
            validate_study_design({
                "reviewer_population":"copyright researchers",
                "inclusion_criteria":["qualified reviewer"],
                "target_n":48,
                "power_rationale":"design grid",
                "recruitment_constraints":"to be recruited",
                "ethics_consent_status":"TBD",
                "assignment_procedure":"balanced A/B",
            })

    def test_source_commit_must_be_full_lowercase_hex_sha(self):
        with self.assertRaises(StudyLockError):
            build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="Z" * 40)

    def test_falsified_prelock_claim_is_rejected(self):
        manifest = build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="a" * 40)
        manifest["real_adjudication_collected"] = True
        with self.assertRaises(StudyLockError):
            validate_freeze_manifest(ROOT, manifest)

    def test_incomplete_hash_set_is_rejected(self):
        manifest = build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="a" * 40)
        manifest["file_sha256"].pop(next(iter(manifest["file_sha256"])))
        with self.assertRaises(StudyLockError):
            validate_freeze_manifest(ROOT, manifest)

    def test_manually_forged_post_adjudication_flags_are_rejected(self):
        manifest = build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="a" * 40)
        manifest["state"] = "POST_ADJUDICATION_LOCK"
        manifest["real_adjudication_collected"] = True
        with self.assertRaises(StudyLockError):
            validate_freeze_manifest(ROOT, manifest)

    def test_manually_forged_primary_lock_is_rejected(self):
        manifest = build_freeze_manifest(ROOT, state="PRE_ADJUDICATION_LOCK", source_commit_sha="a" * 40)
        manifest["state"] = "PRE_PRIMARY_STUDY_LOCK"
        manifest["real_adjudication_collected"] = True
        manifest["study_design_locked"] = True
        manifest["final_sample_size_locked"] = True
        manifest["target_n"] = 24
        with self.assertRaises(StudyLockError):
            validate_freeze_manifest(ROOT, manifest)


if __name__ == "__main__":
    unittest.main()
