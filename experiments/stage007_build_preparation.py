#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from src.ipel.adjudication import aggregate_adjudication, build_adjudication_packet

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "benchmarks/stage006/case_spec.json"
OUT = ROOT / "benchmarks/stage007/generated"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def synthetic_consensus(mapping: dict[str, dict]) -> list[dict]:
    rows = []
    for adjudicator in ("SYN-A", "SYN-B", "SYN-C"):
        for pseudo, meta in sorted(mapping.items()):
            decision = "READY" if meta["stage006_author_readiness"] == "READY_FOR_LEGAL_EVALUATION" else "NOT_READY"
            rows.append({
                "data_origin": "SYNTHETIC_NON_HUMAN",
                "synthetic_fixture": True,
                "adjudicator_id": adjudicator,
                "adjudication_case_id": pseudo,
                "decision": decision,
                "missing_information_codes": list(meta["stage006_author_missing_fact_codes"]),
                "confidence_0_to_100": 90,
                "rationale": "Synthetic software-test fixture; not a human judgment.",
                "prior_exposure": False,
                "conflict_of_interest": False,
            })
    return rows


def synthetic_unresolved(case_id: str) -> list[dict]:
    decisions = (("SYN-U1", "READY"), ("SYN-U2", "NOT_READY"), ("SYN-U3", "UNSURE"))
    return [{
        "data_origin": "SYNTHETIC_NON_HUMAN",
        "synthetic_fixture": True,
        "adjudicator_id": adjudicator,
        "adjudication_case_id": case_id,
        "decision": decision,
        "missing_information_codes": ["WORK_SOURCE"] if decision == "NOT_READY" else [],
        "confidence_0_to_100": 60,
        "rationale": "Synthetic disagreement fixture; not a human judgment.",
        "prior_exposure": False,
        "conflict_of_interest": False,
    } for adjudicator, decision in decisions]


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    base = json.loads((ROOT / spec["base_record"]).read_text(encoding="utf-8"))
    packet, hidden = build_adjudication_packet(spec, base)
    mapping = hidden["mapping"]
    valid_ids = set(mapping)

    visible = json.dumps(packet, ensure_ascii=False)
    stage006_ids = [case["case_id"] for case in spec["cases"]]
    forbidden = stage006_ids + [
        "READY_FOR_LEGAL_EVALUATION", "NOT_READY_FOR_LEGAL_EVALUATION",
        "PASS_EVIDENCE_GATE", "REVIEW_REQUIRED", "FAIL_EVIDENCE_GATE",
        "judgment_sensitive", '"stratum"', '"presentation"', '"stage006_author_"',
    ]
    leakage = sorted(token for token in forbidden if token in visible)

    consensus_rows = synthetic_consensus(mapping)
    synthetic_aggregate = aggregate_adjudication(consensus_rows, valid_ids, allow_synthetic=True)
    one_case = sorted(valid_ids)[0]
    unresolved_rows = synthetic_unresolved(one_case)
    unresolved_aggregate = aggregate_adjudication(unresolved_rows, {one_case}, allow_synthetic=True)

    write_json(OUT / "adjudication_packet.json", packet)
    write_json(OUT / "hidden_case_map.json", hidden)
    write_json(OUT / "synthetic_adjudication/consensus_responses.json", {
        "warning": "SYNTHETIC_NON_HUMAN software-test data only.",
        "responses": consensus_rows,
    })
    write_json(OUT / "synthetic_adjudication/consensus_aggregate.json", {
        "warning": "SYNTHETIC_NON_HUMAN software-test result only.",
        "aggregate": synthetic_aggregate,
    })
    write_json(OUT / "synthetic_adjudication/unresolved_responses.json", {
        "warning": "SYNTHETIC_NON_HUMAN software-test data only.",
        "responses": unresolved_rows,
    })
    write_json(OUT / "synthetic_adjudication/unresolved_aggregate.json", {
        "warning": "SYNTHETIC_NON_HUMAN software-test result only.",
        "aggregate": unresolved_aggregate,
    })

    acceptance = {
        "neutral_packet_has_24_cases": packet["case_count"] == 24,
        "pseudonymous_ids_unique": len(valid_ids) == 24,
        "hidden_mapping_one_to_one": len({v["stage006_case_id"] for v in mapping.values()}) == 24,
        "no_stage006_answer_or_condition_leakage": not leakage,
        "synthetic_consensus_fixture_resolves_all_cases": synthetic_aggregate["all_cases_resolved"] is True,
        "synthetic_disagreement_fixture_stays_unresolved": unresolved_aggregate["all_cases_resolved"] is False,
        "real_adjudication_absent": packet["real_adjudication_collected"] is False,
    }
    report = {
        "stage": "007",
        "status": "PRE_ADJUDICATION_PREPARATION_READY",
        "REAL_ADJUDICATION_COLLECTED": False,
        "FINAL_SAMPLE_SIZE_LOCKED": False,
        "lock_state_target": "PRE_ADJUDICATION_LOCK",
        "case_count": 24,
        "minimum_independent_adjudicators_per_case": 3,
        "decision_consensus_fraction": 2 / 3,
        "leakage_hits": leakage,
        "synthetic_fixture_warning": "All generated adjudication responses are NON-HUMAN software tests.",
        "acceptance": acceptance,
        "all_acceptance_gates_pass": all(acceptance.values()),
    }
    write_json(OUT / "stage007_preparation_report.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_acceptance_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
