import json
import unittest
from pathlib import Path

from src.ipel.study_lock import PRE_ADJUDICATION_PATHS, validate_freeze_manifest

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "benchmarks/stage007/generated/pre_adjudication_lock.json"
SOURCE_COMMIT = "f4455f47963b3fc58e6fb0d4f915483adc74a257"


class Stage007PrelockTests(unittest.TestCase):
    def test_committed_pre_adjudication_lock_is_valid(self):
        manifest = json.loads(LOCK.read_text())
        validate_freeze_manifest(ROOT, manifest)
        self.assertEqual(manifest["state"], "PRE_ADJUDICATION_LOCK")
        self.assertEqual(manifest["source_commit_sha"], SOURCE_COMMIT)
        self.assertFalse(manifest["real_adjudication_collected"])
        self.assertFalse(manifest["final_sample_size_locked"])
        self.assertFalse(manifest["study_design_locked"])

    def test_lock_covers_all_declared_pre_adjudication_inputs(self):
        manifest = json.loads(LOCK.read_text())
        self.assertEqual(set(manifest["file_sha256"]), set(PRE_ADJUDICATION_PATHS))
        self.assertNotIn("benchmarks/stage007/generated/pre_adjudication_lock.json", manifest["file_sha256"])


if __name__ == "__main__":
    unittest.main()
