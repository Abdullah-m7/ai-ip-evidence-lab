#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.ipel.reviewer_benchmark import (
    NOT_READY,
    READY,
    audit_benchmark,
    build_form,
    score_responses,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "benchmarks/stage006/case_spec.json"
DEFAULT_OUTPUT = ROOT / "benchmarks/stage006/generated"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def hidden_answer_key(entries: list[Any]) -> dict[str, dict[str, Any]]:
    return {
        entry.packet_id: {
            "form": entry.form,
            "case_id": entry.case_id,
            "presentation": entry.presentation,
            "stratum": entry.stratum,
            "readiness": entry.readiness,
            "missing_fact_codes": entry.missing_fact_codes,
            "fact_digest": entry.fact_digest,
            "machine_gate_outcome": entry.machine_gate_outcome,
        }
        for entry in entries
    }


def synthetic_responses(
    form_packet_ids: list[str], answer_key: dict[str, dict[str, Any]], *, noisy: bool
) -> list[dict[str, Any]]:
    """Generate NON-HUMAN fixtures only to test the scoring implementation."""
    responses: list[dict[str, Any]] = []
    for i, packet_id in enumerate(form_packet_ids):
        truth = answer_key[packet_id]
        correct = "READY" if truth["readiness"] == READY else "NOT_READY"
        expected_missing = list(truth["missing_fact_codes"])
        if not noisy:
            decision = correct
            missing = expected_missing
            confidence = 94
        else:
            if i % 5 == 0:
                decision = "UNSURE"
            elif i % 4 == 0:
                decision = "NOT_READY" if correct == "READY" else "READY"
            else:
                decision = correct
            if i % 3 == 0:
                missing = []
            elif expected_missing:
                missing = expected_missing[:1]
            else:
                missing = ["WORK_SOURCE"] if i % 2 == 0 else []
            confidence = 55 + (i % 4) * 7
        responses.append({
            "packet_id": packet_id,
            "decision": decision,
            "missing_information_codes": missing,
            "confidence_0_to_100": confidence,
            "assessment_seconds": 28 + (i % 7) * 4,
        })
    return responses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    base_path = ROOT / spec["base_record"]
    base_record = json.loads(base_path.read_text(encoding="utf-8"))

    form_a, manifest_a, latent_a = build_form(spec, base_record, "A")
    form_b, manifest_b, latent_b = build_form(spec, base_record, "B")
    manifests = manifest_a + manifest_b
    forms = {"A": form_a, "B": form_b}
    latent = {"A": latent_a, "B": latent_b}
    key = hidden_answer_key(manifests)
    audit = audit_benchmark(spec, forms, manifests, latent)

    if not audit["all_acceptance_gates_pass"]:
        raise SystemExit("Stage 006 structural audit failed")

    output = args.output_dir
    write_json(output / "form_a.json", form_a)
    write_json(output / "form_b.json", form_b)
    write_json(output / "hidden_answer_key.json", {
        "warning": "EXPERIMENTER-ONLY. Do not distribute with reviewer packets.",
        "benchmark_version": spec["benchmark_version"],
        "answers": key,
    })
    write_json(output / "audit.json", audit)
    write_json(output / "case_provenance_manifest.json", {
        "benchmark_version": spec["benchmark_version"],
        "seed": spec["seed"],
        "base_record": spec["base_record"],
        "entries": [entry.to_dict() for entry in manifests],
    })

    form_a_ids = [packet["packet_id"] for packet in form_a["packets"]]
    perfect = synthetic_responses(form_a_ids, key, noisy=False)
    noisy = synthetic_responses(form_a_ids, key, noisy=True)
    write_json(output / "synthetic_responses/perfect_form_a.json", {
        "synthetic_nonhuman": True,
        "purpose": "Scoring implementation test only; not study data.",
        "responses": perfect,
    })
    write_json(output / "synthetic_responses/noisy_form_a.json", {
        "synthetic_nonhuman": True,
        "purpose": "Scoring implementation test only; not study data.",
        "responses": noisy,
    })
    write_json(output / "synthetic_responses/perfect_score.json", {
        "synthetic_nonhuman": True,
        "purpose": "Scoring implementation test only; not study results.",
        "score": score_responses(perfect, key),
    })
    write_json(output / "synthetic_responses/noisy_score.json", {
        "synthetic_nonhuman": True,
        "purpose": "Scoring implementation test only; not study results.",
        "score": score_responses(noisy, key),
    })

    report = {
        "stage": "006",
        "status": "BENCHMARK_READY_NOT_HUMAN_RESULTS",
        "case_count": len(spec["cases"]),
        "forms": {"A": form_a["packet_count"], "B": form_b["packet_count"]},
        "acceptance": audit["acceptance"],
        "all_acceptance_gates_pass": audit["all_acceptance_gates_pass"],
        "ready_cases_with_machine_fail": audit["ready_cases_with_machine_fail"],
        "human_data_collected": False,
        "human_effect_estimates": None,
    }
    write_json(output / "stage006_build_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
