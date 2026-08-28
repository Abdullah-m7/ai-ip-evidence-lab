import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from src.ipel.adjudication_distribution import (
    BUNDLE_VERSION,
    RESPONSE_VERSION,
    DistributionError,
    ROOT,
    _hmac_hex,
    append_intake,
    build_distribution,
    canonical_bytes,
    guard_bundle_destination,
    guard_private_destination,
    new_intake_ledger,
    normalize_external_response,
    object_sha256,
    scan_external_leakage,
    validate_bundle,
    validate_private_mapping,
    verify_intake_ledger,
)


class Stage008DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            (ROOT / "benchmarks/stage007/generated/adjudication_packet.json").read_text(encoding="utf-8")
        )
        cls.key = bytes.fromhex("11" * 32)  # TEST-ONLY deterministic key; never a real distribution key.
        cls.wrong_key = bytes.fromhex("22" * 32)
        cls.bundle, cls.manifest, cls.mapping = build_distribution(
            cls.source, "TEST-DIST-001", cls.key
        )

    def synthetic_response(self, *, count=24):
        rows = []
        for packet in self.bundle["packets"][:count]:
            rows.append({
                "external_case_id": packet["external_case_id"],
                "decision": "READY",
                "missing_information_codes": [],
                "confidence_0_to_100": 75,
                "rationale": "Synthetic software-test response only.",
                "prior_exposure": False,
                "conflict_of_interest": False,
            })
        return {
            "response_version": RESPONSE_VERSION,
            "bundle_id": self.bundle["bundle_id"],
            "distribution_id": self.bundle["distribution_id"],
            "bundle_sha256": self.manifest["bundle_sha256"],
            "data_origin": "SYNTHETIC_NON_HUMAN",
            "synthetic_fixture": True,
            "adjudicator_id": "SYNTHETIC-TEST-ADJUDICATOR",
            "responses": rows,
        }

    def normalized(self, *, count=3):
        return normalize_external_response(
            self.synthetic_response(count=count), self.bundle, self.manifest, self.mapping,
            self.key, allow_synthetic=True,
        )

    def synthetic_ledger(self, *, count=3):
        return append_intake(
            new_intake_ledger("SYNTHETIC_NON_HUMAN", self.key),
            self.normalized(count=count), self.key,
        )

    def test_bundle_is_clean_and_has_per_distribution_ids(self):
        self.assertEqual(self.bundle["bundle_version"], BUNDLE_VERSION)
        self.assertEqual(self.bundle["case_count"], 24)
        self.assertEqual(scan_external_leakage(self.bundle), [])
        ids = [p["external_case_id"] for p in self.bundle["packets"]]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(set(ids)), 24)
        self.assertTrue(all(case_id.startswith("CASE-") for case_id in ids))
        other, _, _ = build_distribution(self.source, "TEST-DIST-002", self.key)
        self.assertNotEqual(set(ids), {p["external_case_id"] for p in other["packets"]})

    def test_wrong_key_fails_bundle_mapping_and_ledger(self):
        with self.assertRaises(DistributionError):
            validate_bundle(self.bundle, self.manifest, self.wrong_key)
        with self.assertRaises(DistributionError):
            validate_private_mapping(self.mapping, self.manifest, self.wrong_key)
        with self.assertRaises(DistributionError):
            verify_intake_ledger(self.synthetic_ledger(), self.wrong_key)

    def test_one_field_bundle_tamper_is_detected(self):
        tampered = copy.deepcopy(self.bundle)
        tampered["packets"][0]["material"]["format_name"] = "tampered"
        with self.assertRaises(DistributionError):
            validate_bundle(tampered, self.manifest, self.key)

    def test_private_mapping_tamper_is_detected(self):
        tampered = copy.deepcopy(self.mapping)
        first = next(iter(tampered["external_to_internal"]))
        tampered["external_to_internal"][first] = "ADJ-000000000000"
        with self.assertRaises(DistributionError):
            validate_private_mapping(tampered, self.manifest, self.key)

    def test_private_mapping_source_binding_survives_recomputed_mac(self):
        tampered = copy.deepcopy(self.mapping)
        tampered["source_packet_sha256"] = "0" * 64
        payload = {k: copy.deepcopy(v) for k, v in tampered.items() if k != "mapping_hmac_sha256"}
        # Even an actor with the HMAC key cannot make a mapping for a different source packet
        # pass the frozen-source check merely by recomputing mapping authentication.
        tampered["mapping_hmac_sha256"] = _hmac_hex(
            self.key, "mapping-auth", canonical_bytes(payload)
        )
        with self.assertRaises(DistributionError):
            validate_private_mapping(tampered, self.manifest, self.key)

    def test_private_and_distribution_path_guards(self):
        with self.assertRaises(DistributionError):
            guard_private_destination(ROOT / "tracked-private-map.json", ROOT)
        guard_private_destination(ROOT / ".private-stage008" / "x" / "map.json", ROOT)
        with self.assertRaises(DistributionError):
            guard_bundle_destination(ROOT / "public-real-bundle", ROOT)
        guard_bundle_destination(ROOT / ".stage008-distributions" / "x", ROOT)
        with tempfile.TemporaryDirectory() as td:
            guard_private_destination(Path(td) / "mapping.json", ROOT)
            guard_bundle_destination(Path(td) / "bundle", ROOT)

    def test_private_output_roots_are_untracked_and_gitignored(self):
        tracked = subprocess.check_output(
            ["git", "ls-files", ".private-stage008", ".stage008-distributions"],
            cwd=ROOT, text=True,
        ).strip()
        self.assertEqual(tracked, "")
        for probe in (
            ".private-stage008/PROBE/private_case_mapping.json",
            ".stage008-distributions/PROBE/adjudication_bundle.json",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", probe], cwd=ROOT
            )
            self.assertEqual(result.returncode, 0, probe)

    def test_synthetic_roundtrip_requires_explicit_synthetic_lane(self):
        response = self.synthetic_response()
        with self.assertRaises(DistributionError):
            normalize_external_response(
                response, self.bundle, self.manifest, self.mapping, self.key,
                allow_synthetic=False,
            )
        normalized = normalize_external_response(
            response, self.bundle, self.manifest, self.mapping, self.key,
            allow_synthetic=True,
        )
        self.assertEqual(normalized["data_origin"], "SYNTHETIC_NON_HUMAN")
        self.assertEqual(normalized["bundle_sha256"], self.manifest["bundle_sha256"])
        self.assertEqual(len(normalized["normalized_responses"]), 24)
        self.assertTrue(all(row["adjudication_case_id"].startswith("ADJ-") for row in normalized["normalized_responses"]))
        ledger = append_intake(
            new_intake_ledger("SYNTHETIC_NON_HUMAN", self.key), normalized, self.key
        )
        verify_intake_ledger(ledger, self.key)
        self.assertEqual(len(ledger["events"]), 1)
        self.assertEqual(len(ledger["responses"]), 24)
        self.assertEqual(ledger["events"][0]["bundle_sha256"], self.manifest["bundle_sha256"])
        self.assertNotIn("POST_ADJUDICATION_LOCK", json.dumps(ledger))

    def test_duplicate_external_response_is_rejected(self):
        response = self.synthetic_response(count=2)
        response["responses"][1]["external_case_id"] = response["responses"][0]["external_case_id"]
        with self.assertRaises(DistributionError):
            normalize_external_response(
                response, self.bundle, self.manifest, self.mapping, self.key,
                allow_synthetic=True,
            )

    def test_direct_append_revalidates_internal_rows(self):
        normalized = self.normalized(count=1)
        normalized["normalized_responses"][0]["adjudication_case_id"] = "ADJ-000000000000"
        with self.assertRaises(DistributionError):
            append_intake(
                new_intake_ledger("SYNTHETIC_NON_HUMAN", self.key),
                normalized, self.key,
            )

    def test_post_intake_response_tampering_is_detected(self):
        ledger = self.synthetic_ledger()
        tampered = copy.deepcopy(ledger)
        tampered["responses"][0]["decision"] = "NOT_READY"
        with self.assertRaises(DistributionError):
            verify_intake_ledger(tampered, self.key)

    def test_public_rehash_cannot_repair_keyed_receipt(self):
        ledger = self.synthetic_ledger()
        tampered = copy.deepcopy(ledger)
        tampered["responses"][0]["decision"] = "NOT_READY"
        event = tampered["events"][0]
        start = event["response_start"]
        end = start + event["response_count"]
        # An attacker can recompute every public/unkeyed hash after changing a response...
        event["normalized_responses_sha256"] = object_sha256(tampered["responses"][start:end])
        # ...but cannot recompute receipt_hmac_sha256 without the private distribution key.
        with self.assertRaises(DistributionError):
            verify_intake_ledger(tampered, self.key)

    def test_intake_ledger_refuses_duplicate_adjudicator_case(self):
        normalized = self.normalized(count=2)
        ledger = append_intake(
            new_intake_ledger("SYNTHETIC_NON_HUMAN", self.key), normalized, self.key
        )
        with self.assertRaises(DistributionError):
            append_intake(ledger, normalized, self.key)


if __name__ == "__main__":
    unittest.main()
