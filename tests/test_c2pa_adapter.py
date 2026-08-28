import copy
import unittest

from src.ipel.c2pa_adapter import extract_c2pa_evidence, coupled_evaluation


def report(*, state="Valid", success=None, failure=None, tdm="allowed"):
    if success is None:
        success = [
        "claimSignature.validated",
        "claimSignature.insideValidity",
        "assertion.hashedURI.match",
        "assertion.dataHash.match",
    ]
    if failure is None:
        failure = ["signingCredential.untrusted"]
    active = "urn:c2pa:test"
    return {
        "active_manifest": active,
        "manifests": {
            active: {
                "assertions": [
                    {
                        "label": "cawg.training-mining",
                        "data": {"entries": {"cawg.ai_training": {"use": tdm}}},
                    },
                    {
                        "label": "c2pa.actions.v2",
                        "data": {"actions": [{"action": "c2pa.created", "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"}]},
                    },
                ]
            }
        },
        "validation_state": state,
        "validation_results": {
            "activeManifest": {
                "success": [{"code": x} for x in success],
                "informational": [],
                "failure": [{"code": x} for x in failure],
            }
        },
    }


def valid_record():
    return {
        "record_version": "0.1.0",
        "record_id": "adapter-test",
        "work": {"type": "literary", "source": "synthetic://x", "publication_status": "verified", "acquisition_status": "verified"},
        "use": {"purpose": "AI evaluation", "date": "2026-08-28", "necessity_status": "supported", "republication": False, "distribution": False, "direct_commercial_exploitation": False, "purely_commercial_context": False},
        "rights_context": {"legitimate_interests_prejudice": "none", "exploitation_opportunity_effect": "none", "independent_elements_status": "none_identified", "impact_assessment_basis": ["evidence://impact"], "independent_elements_basis": ["evidence://rights"]},
        "output_context": {"transformed": False, "republished": False, "made_public": False, "included_in_final_product": False, "inclusion_necessary": "not_applicable", "permission_status": "not_applicable", "public_domain_status": "no"},
        "evidence": {"publication": ["evidence://pub"], "acquisition": ["evidence://acq"], "use_event": ["evidence://use"]},
    }


class C2PAAdapterTests(unittest.TestCase):
    def test_valid_signature_can_have_untrusted_signer(self):
        ev = extract_c2pa_evidence(report())
        self.assertEqual(ev.validation_state, "valid")
        self.assertEqual(ev.claim_signature, "valid")
        self.assertEqual(ev.asset_binding, "valid")
        self.assertEqual(ev.signer_trust, "untrusted")

    def test_explicit_trust_requires_success_code(self):
        ev = extract_c2pa_evidence(report(failure=[], success=["claimSignature.validated", "assertion.dataHash.match", "assertion.hashedURI.match", "signingCredential.trusted"]))
        self.assertEqual(ev.signer_trust, "trusted")

    def test_asset_hash_mismatch_is_invalid_binding(self):
        ev = extract_c2pa_evidence(report(state="Invalid", failure=["signingCredential.untrusted", "assertion.dataHash.mismatch"]))
        self.assertEqual(ev.asset_binding, "invalid")

    def test_signature_mismatch_is_invalid_signature(self):
        ev = extract_c2pa_evidence(report(state="Invalid", failure=["signingCredential.untrusted", "claimSignature.mismatch"]))
        self.assertEqual(ev.claim_signature, "invalid")

    def test_malformed_tdm_is_warning_not_crash(self):
        r = report()
        r["manifests"][r["active_manifest"]]["assertions"][0]["data"]["entries"]["cawg.ai_training"]["use"] = "aLlowed"
        ev = extract_c2pa_evidence(r)
        self.assertEqual(ev.tdm_entries, {})
        self.assertIn("invalid TDM use: cawg.ai_training", ev.semantic_warnings)

    def test_conflicting_tdm_is_machine_visible(self):
        r = report(tdm="allowed")
        r["manifests"][r["active_manifest"]]["assertions"].append({"label":"cawg.training-mining","data":{"entries":{"cawg.ai_training":{"use":"notAllowed"}}}})
        ev = extract_c2pa_evidence(r)
        self.assertIn("cawg.ai_training", ev.tdm_conflicts)
        self.assertNotIn("cawg.ai_training", ev.tdm_entries)

    def test_allowed_signal_does_not_cure_unlawful_acquisition(self):
        rec = valid_record(); rec["work"]["acquisition_status"] = "false"
        before = copy.deepcopy(rec)
        result = coupled_evaluation(report(tdm="allowed"), rec)
        self.assertEqual(result["legal_gate"]["outcome"], "FAIL_EVIDENCE_GATE")
        self.assertEqual(result["c2pa_evidence"]["tdm_entries"]["cawg.ai_training"], "allowed")
        self.assertFalse(result["legal_fields_overwritten"])
        self.assertEqual(rec, before)

    def test_c2pa_evidence_contains_no_legal_status_fields(self):
        data = extract_c2pa_evidence(report()).to_dict()
        forbidden = {"publication_status", "acquisition_status", "permission_status", "legal_compliance"}
        self.assertTrue(forbidden.isdisjoint(data))


if __name__ == "__main__":
    unittest.main()
