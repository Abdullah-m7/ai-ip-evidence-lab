import copy
import unittest

from src.ipel.c2pa_crosscheck import (
    CommonValidation,
    CrossCheckError,
    agreement,
    normalize_c2patool,
    normalize_cross_validator,
    validate_cross_tool_provenance,
)


def reader_report(*, failures=None, tdm_use="constrained", engine="0.90.16"):
    failures = failures if failures is not None else [{"code": "signingCredential.untrusted"}]
    successes = [
        {"code": "claimSignature.validated"},
        {"code": "assertion.hashedURI.match"},
        {"code": "assertion.dataHash.match"},
    ]
    return {
        "validation_state": "Valid",
        "validation_results": {"activeManifest": {"success": successes, "failure": failures}},
        "active_manifest": "m",
        "manifests": {
            "m": {
                "claim_generator_info": [{"org.contentauth.c2pa_rs": engine}],
                "assertions": [
                    {"label": "cawg.training-mining", "data": {"entries": {"cawg.ai_training": {"use": tdm_use}}}},
                    {"label": "c2pa.actions.v2", "data": {"actions": []}},
                ],
            }
        },
    }


def cross_report(*, failures=None, tdm_use="constrained", engine="0.78.0", trusted=False):
    failures = failures if failures is not None else ([] if trusted else [{"code": "signingCredential.untrusted"}])
    successes = [
        {"code": "claimSignature.validated"},
        {"code": "assertion.hashedURI.match"},
        {"code": "assertion.dataHash.match"},
    ]
    if trusted:
        successes.append({"code": "signingCredential.trusted"})
    return {
        "manifests": [{
            "assertions": {"cawg.training-mining": {"entries": {"cawg.ai_training": {"use": tdm_use}}}},
            "validationResults": {"success": successes, "failure": failures, "informational": []},
        }],
        "jsonGenerator": {"name": "c2pa-rs", "version": engine, "date": "ignored"},
    }


class CrossCheckTests(unittest.TestCase):
    def test_cross_version_common_semantics_agree_without_implementation_claim(self):
        left = normalize_c2patool(reader_report())
        right = normalize_cross_validator(cross_report())
        result = agreement(left, right)
        self.assertTrue(result["all_common_semantics_agree"])
        self.assertTrue(result["different_engine_versions"])
        self.assertFalse(result["implementation_diversity_established"])
        self.assertEqual((left.engine_version, right.engine_version), ("0.90.16", "0.78.0"))

    def test_trusted_signer_does_not_change_crypto_classification(self):
        default = normalize_cross_validator(cross_report())
        trusted = normalize_cross_validator(cross_report(trusted=True))
        self.assertEqual(default.cryptographic_validity, "valid")
        self.assertEqual(trusted.cryptographic_validity, "valid")
        self.assertEqual(default.signer_trust, "untrusted")
        self.assertEqual(trusted.signer_trust, "trusted")

    def test_malformed_tdm_is_semantic_warning_not_crypto_failure(self):
        left = normalize_c2patool(reader_report(tdm_use="maybe"))
        right = normalize_cross_validator(cross_report(tdm_use="maybe"))
        self.assertEqual(left.cryptographic_validity, "valid")
        self.assertEqual(right.cryptographic_validity, "valid")
        self.assertEqual(left.tdm_entries, {})
        self.assertEqual(right.tdm_entries, {})
        self.assertIn("invalid TDM use: cawg.ai_training", left.semantic_warnings)
        self.assertIn("invalid TDM use: cawg.ai_training", right.semantic_warnings)

    def test_data_hash_mismatch_normalizes_on_both_surfaces(self):
        failure = [{"code": "signingCredential.untrusted"}, {"code": "assertion.dataHash.mismatch"}]
        l = reader_report(failures=failure)
        l["validation_results"]["activeManifest"]["success"] = [
            x for x in l["validation_results"]["activeManifest"]["success"] if x["code"] != "assertion.dataHash.match"
        ]
        r = cross_report(failures=failure)
        r["manifests"][0]["validationResults"]["success"] = [
            x for x in r["manifests"][0]["validationResults"]["success"] if x["code"] != "assertion.dataHash.match"
        ]
        self.assertEqual(normalize_c2patool(l).asset_binding, "invalid")
        self.assertEqual(normalize_cross_validator(r).asset_binding, "invalid")

    def test_common_evidence_has_no_legal_status_fields(self):
        forbidden = {"publication_status", "acquisition_status", "ownership", "permission_status", "legal_compliance"}
        self.assertTrue(forbidden.isdisjoint(CommonValidation.__dataclass_fields__))

    def test_provenance_gate_rejects_paper_trust(self):
        good = {
            "repository": "contentauth/c2pa-conformance-tool-cli",
            "commit": "c09f0340524b088a81475f7b7eaab5ba7042772f",
            "version": "0.2.0",
            "source_archive_sha256": "3571355b1a83d7150393d070e7b4a5b5c0f32d8524b6d7a41f740395c9cefc85",
            "rust": "1.98.0",
            "cargo_lock_sha256": "80dcab12a2773a6cffd3c6c8794640d0be9cff3a9227d7abd44143e963fa6fd0",
            "c2pa_rs_commit": "61f2e676043c1d22fa60f4fe5d09d3874c7c8a10",
            "c2pa_rs_archive_sha256": "4a27ab5cceb4ea4e42b1e629808a0895f2c91a0fea5cd71c5827665d8f7e8bc7",
            "declared_profile_commit_unavailable": "c43d11162c27c5e992c7010fc75b72bb3e5520e1",
            "profile_repair_repository": "adobe/profile-evaluator-rs",
            "profile_repair_commit": "40c4201933e3b4760932b65913e2a9c57413f8ac",
            "profile_repair_archive_sha256": "2c51d6aafdc67f075a5ce31d6700ab031df214789bdb9a893dc60b48391b7e6a",
            "declared_json_formula_commit": "1ff483f15157521503a0ce79c123333ecd14ce08",
            "json_formula_repair_repository": "adobe/json-formula-rs",
            "json_formula_repair_commit": "90ee7f44ded98c657a410a0bf1248a9e3f6f1627",
            "json_formula_repair_commit_verified": True,
            "compatibility_repair": True,
            "shared_engine_lineage": "c2pa-rs",
            "implementation_diversity_established": False,
        }
        validate_cross_tool_provenance(good)
        bad = copy.deepcopy(good)
        bad["c2pa_rs_commit"] = "0" * 40
        with self.assertRaises(CrossCheckError):
            validate_cross_tool_provenance(bad)


if __name__ == "__main__":
    unittest.main()
