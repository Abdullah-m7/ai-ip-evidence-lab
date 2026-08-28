import json
import unittest
from pathlib import Path

from src.ipel.chain import verify_chain

ROOT = Path(__file__).resolve().parents[1]


class Stage002FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean = json.loads((ROOT / "examples/chains/stage002_clean.json").read_text())
        cls.checkpoint = cls.clean["checkpoint"]

    def test_committed_clean_fixture_verifies(self):
        result = verify_chain(self.clean["events"], self.checkpoint)
        self.assertTrue(result.integrity_verified)
        self.assertTrue(result.boundary_verified)

    def test_all_committed_attacks_are_detected_with_checkpoint(self):
        paths = sorted((ROOT / "examples/chains/attacks").glob("*.json"))
        self.assertGreaterEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path.name):
                events = json.loads(path.read_text())["events"]
                self.assertFalse(verify_chain(events, self.checkpoint).integrity_verified)

    def test_boundary_sensitive_attacks_can_pass_internal_only_verification(self):
        for name in ("rehashed_forgery.json", "tail_deletion.json"):
            events = json.loads((ROOT / "examples/chains/attacks" / name).read_text())["events"]
            with self.subTest(name=name):
                result = verify_chain(events)
                self.assertTrue(result.integrity_verified)
                self.assertFalse(result.boundary_verified)
                self.assertFalse(result.claim_truth_verified)


if __name__ == "__main__":
    unittest.main()
