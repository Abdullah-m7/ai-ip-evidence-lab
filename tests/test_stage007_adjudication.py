import json
import unittest
from pathlib import Path

from src.ipel.adjudication import (
    AdjudicationError,
    aggregate_adjudication,
    aggregate_case,
    build_adjudication_packet,
    validate_adjudication_response,
)
from src.ipel.reviewer_benchmark import available_facts, build_case_record, fact_digest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "benchmarks/stage007/generated"


class Stage007AdjudicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / "benchmarks/stage006/case_spec.json").read_text())
        cls.base = json.loads((ROOT / cls.spec["base_record"]).read_text())
        cls.packet = json.loads((OUT / "adjudication_packet.json").read_text())
        cls.hidden = json.loads((OUT / "hidden_case_map.json").read_text())
        cls.valid_ids = set(cls.hidden["mapping"])

    def test_neutral_packet_is_blinded(self):
        visible = json.dumps(self.packet)
        self.assertEqual(self.packet["case_count"], 24)
        self.assertEqual(len({p["adjudication_case_id"] for p in self.packet["packets"]}), 24)
        for case in self.spec["cases"]:
            self.assertNotIn(case["case_id"], visible)
        for token in ("READY_FOR_LEGAL_EVALUATION", "NOT_READY_FOR_LEGAL_EVALUATION", "FAIL_EVIDENCE_GATE", "judgment_sensitive", '"stratum"', '"presentation"'):
            self.assertNotIn(token, visible)

    def test_hidden_map_preserves_author_labels_without_overwriting(self):
        labels = {v["stage006_author_readiness"] for v in self.hidden["mapping"].values()}
        self.assertEqual(labels, {"READY_FOR_LEGAL_EVALUATION", "NOT_READY_FOR_LEGAL_EVALUATION"})
        self.assertEqual(len({v["stage006_case_id"] for v in self.hidden["mapping"].values()}), 24)

    def test_neutral_fact_digests_match_latent_cases(self):
        by_case = {v["stage006_case_id"]: v for v in self.hidden["mapping"].values()}
        for index, case in enumerate(self.spec["cases"]):
            record = build_case_record(self.base, case, index)
            self.assertEqual(by_case[case["case_id"]]["fact_digest"], fact_digest(available_facts(record)))

    def test_synthetic_data_rejected_by_real_path(self):
        fixture = json.loads((OUT / "synthetic_adjudication/consensus_responses.json").read_text())["responses"][0]
        with self.assertRaises(AdjudicationError):
            validate_adjudication_response(fixture, self.valid_ids, allow_synthetic=False)

    def test_synthetic_consensus_fixture_resolves_all(self):
        rows = json.loads((OUT / "synthetic_adjudication/consensus_responses.json").read_text())["responses"]
        result = aggregate_adjudication(rows, self.valid_ids, allow_synthetic=True)
        self.assertTrue(result["all_cases_resolved"])
        self.assertEqual(result["resolved_cases"], 24)
        self.assertEqual(result["data_origin"], "SYNTHETIC_NON_HUMAN")

    def test_disagreement_is_unresolved(self):
        doc = json.loads((OUT / "synthetic_adjudication/unresolved_responses.json").read_text())
        case_id = doc["responses"][0]["adjudication_case_id"]
        result = aggregate_adjudication(doc["responses"], {case_id}, allow_synthetic=True)
        self.assertFalse(result["all_cases_resolved"])
        self.assertEqual(result["cases"][case_id]["status"], "UNRESOLVED")
        self.assertEqual(result["cases"][case_id]["unresolved_reason"], "DECISION_CONSENSUS_NOT_MET")

    def test_conflict_exclusion_can_make_case_insufficient(self):
        case_id = sorted(self.valid_ids)[0]
        rows = []
        for i in range(3):
            rows.append({
                "data_origin":"SYNTHETIC_NON_HUMAN", "synthetic_fixture":True,
                "adjudicator_id":f"X{i}", "adjudication_case_id":case_id,
                "decision":"READY", "missing_information_codes":[], "confidence_0_to_100":80,
                "rationale":"test", "prior_exposure":False, "conflict_of_interest": i == 2,
            })
        result = aggregate_case(case_id, rows)
        self.assertEqual(result.status, "UNRESOLVED")
        self.assertEqual(result.unresolved_reason, "INSUFFICIENT_INDEPENDENT_ADJUDICATORS")

    def test_not_ready_requires_missing_information_consensus(self):
        case_id = sorted(self.valid_ids)[0]
        codes = ["WORK_TYPE", "WORK_SOURCE", "USE_DATE"]
        rows = [{
            "data_origin":"SYNTHETIC_NON_HUMAN", "synthetic_fixture":True,
            "adjudicator_id":f"M{i}", "adjudication_case_id":case_id,
            "decision":"NOT_READY", "missing_information_codes":[code], "confidence_0_to_100":80,
            "rationale":"test", "prior_exposure":False, "conflict_of_interest":False,
        } for i, code in enumerate(codes)]
        result = aggregate_case(case_id, rows)
        self.assertEqual(result.status, "UNRESOLVED")
        self.assertEqual(result.unresolved_reason, "NOT_READY_WITHOUT_MISSING_INFORMATION_CONSENSUS")


if __name__ == "__main__":
    unittest.main()
