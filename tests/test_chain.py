import copy
import unittest

from src.ipel.chain import build_chain, make_checkpoint, verify_chain


def inputs():
    z = "0" * 64
    o = "1" * 64
    return [
        {
            "event_id": "evt-acquire-001",
            "event_type": "WORK_ACQUIRED",
            "occurred_at": "2026-08-28T12:00:00Z",
            "actor": {"id": "developer-1", "type": "organization"},
            "payload": {"work_id": "work-001", "source": "https://example.org/work", "acquisition_status": "verified"},
            "evidence_refs": [{"uri": "urn:receipt:1", "sha256": z}],
        },
        {
            "event_id": "evt-use-001",
            "event_type": "WORK_USED_FOR_AI_DEVELOPMENT",
            "occurred_at": "2026-08-28T13:00:00Z",
            "actor": {"id": "pipeline-7", "type": "software"},
            "payload": {"work_id": "work-001", "purpose": "evaluation corpus construction", "extent": "excerpt"},
            "evidence_refs": [{"uri": "urn:run:7", "sha256": o}],
        },
        {
            "event_id": "evt-assess-001",
            "event_type": "RIGHTS_ASSESSMENT_RECORDED",
            "occurred_at": "2026-08-28T14:00:00Z",
            "actor": {"id": "reviewer-2", "type": "human"},
            "payload": {"work_id": "work-001", "assessment": "reviewed"},
            "evidence_refs": [],
        },
    ]


class ChainTests(unittest.TestCase):
    def setUp(self):
        self.chain = build_chain("chain-001", inputs())
        self.checkpoint = make_checkpoint(self.chain)

    def test_clean_chain_verifies_against_checkpoint(self):
        result = verify_chain(self.chain, self.checkpoint)
        self.assertTrue(result.integrity_verified)
        self.assertTrue(result.boundary_verified)
        self.assertFalse(result.claim_truth_verified)

    def test_payload_mutation_is_detected(self):
        attacked = copy.deepcopy(self.chain)
        attacked[1]["payload"]["purpose"] = "commercial model training"
        result = verify_chain(attacked, self.checkpoint)
        self.assertFalse(result.integrity_verified)
        self.assertIn("EVENT_HASH_MISMATCH", {x.code for x in result.findings})

    def test_evidence_digest_mutation_is_detected(self):
        attacked = copy.deepcopy(self.chain)
        attacked[0]["evidence_refs"][0]["sha256"] = "f" * 64
        self.assertFalse(verify_chain(attacked, self.checkpoint).integrity_verified)

    def test_middle_deletion_is_detected(self):
        attacked = [self.chain[0], self.chain[2]]
        codes = {x.code for x in verify_chain(attacked, self.checkpoint).findings}
        self.assertTrue({"SEQUENCE_MISMATCH", "PREVIOUS_HASH_MISMATCH", "CHECKPOINT_COUNT_MISMATCH"} & codes)

    def test_reordering_is_detected(self):
        attacked = [self.chain[1], self.chain[0], self.chain[2]]
        self.assertFalse(verify_chain(attacked, self.checkpoint).integrity_verified)

    def test_insertion_is_detected(self):
        fake = copy.deepcopy(self.chain[1])
        attacked = [self.chain[0], fake, self.chain[1], self.chain[2]]
        self.assertFalse(verify_chain(attacked, self.checkpoint).integrity_verified)

    def test_rehashed_rewrite_needs_external_checkpoint(self):
        forged_inputs = inputs()
        forged_inputs[1]["payload"]["purpose"] = "commercial model training"
        forged = build_chain("chain-001", forged_inputs)
        self.assertTrue(verify_chain(forged).integrity_verified)
        with_anchor = verify_chain(forged, self.checkpoint)
        self.assertFalse(with_anchor.integrity_verified)
        self.assertIn("CHECKPOINT_HEAD_MISMATCH", {x.code for x in with_anchor.findings})

    def test_tail_deletion_requires_known_boundary(self):
        shortened = self.chain[:-1]
        self.assertTrue(verify_chain(shortened).integrity_verified)
        anchored = verify_chain(shortened, self.checkpoint)
        self.assertFalse(anchored.integrity_verified)
        self.assertIn("CHECKPOINT_COUNT_MISMATCH", {x.code for x in anchored.findings})

    def test_float_payload_is_rejected(self):
        bad = inputs()
        bad[0]["payload"]["score"] = 0.5
        with self.assertRaises(TypeError):
            build_chain("chain-001", bad)

    def test_non_object_first_event_fails_closed(self):
        attacked = copy.deepcopy(self.chain)
        attacked[0] = "not-an-event"
        result = verify_chain(attacked, self.checkpoint)
        self.assertFalse(result.integrity_verified)
        self.assertIn("EVENT_NOT_OBJECT", {x.code for x in result.findings})

    def test_non_object_tail_event_fails_closed(self):
        attacked = copy.deepcopy(self.chain)
        attacked[-1] = ["not-an-event"]
        result = verify_chain(attacked, self.checkpoint)
        self.assertFalse(result.integrity_verified)
        self.assertIn("EVENT_NOT_OBJECT", {x.code for x in result.findings})

    def test_malformed_checkpoint_fails_closed(self):
        result = verify_chain(self.chain, ["not-a-checkpoint"])
        self.assertFalse(result.integrity_verified)
        self.assertFalse(result.boundary_verified)
        self.assertIn("CHECKPOINT_CONTRACT_ERROR", {x.code for x in result.findings})


if __name__ == "__main__":
    unittest.main()
