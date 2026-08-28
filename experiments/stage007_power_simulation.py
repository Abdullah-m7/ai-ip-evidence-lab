#!/usr/bin/env python3
"""Simulation-based design grid for the future Stage-006 reviewer study.

Planning only: uses prespecified assumptions and the actual Stage-006 NOT_READY case/
missing-information opportunity structure. It does not choose a final N or use human outcomes.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from src.ipel.reviewer_benchmark import NOT_READY, assign_presentations

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "benchmarks/stage006/case_spec.json"
DEFAULT_OUTPUT = ROOT / "benchmarks/stage007/generated/power_design_grid.json"
BASE_SEED = 2026082907


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def z_from_paired(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1)
    if var <= 1e-15:
        return 0.0 if abs(mean) <= 1e-15 else math.copysign(float("inf"), mean)
    return mean / math.sqrt(var / n)


def load_not_ready_plan() -> dict[str, list[dict]]:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    cases = list(spec["cases"])
    assignments = {form: assign_presentations(cases, form) for form in ("A", "B")}
    plans: dict[str, list[dict]] = {"A": [], "B": []}
    for form in ("A", "B"):
        for case in cases:
            if case["readiness"] != NOT_READY:
                continue
            plans[form].append({
                "case_id": case["case_id"],
                "stratum": case["stratum"],
                "presentation": assignments[form][case["case_id"]],
                "missing_opportunities": len(case["missing_fact_codes"]),
            })
    return plans


CASE_PLANS = load_not_ready_plan()
TOTAL_NOT_READY_CASES = len(CASE_PLANS["A"])
TOTAL_MISSING_OPPORTUNITIES = sum(x["missing_opportunities"] for x in CASE_PLANS["A"])


def simulate_once(
    rng: random.Random,
    n_reviewers: int,
    baseline_recall: float,
    recall_delta: float,
    baseline_false_ready: float,
    false_ready_delta: float,
    attrition: float,
    reviewer_sd: float,
    case_sd: float,
    judgment_penalty: float,
) -> tuple[bool, bool, int]:
    retained = [i for i in range(n_reviewers) if rng.random() >= attrition]
    if len(retained) < 4:
        return False, False, len(retained)
    case_effects = {
        case["case_id"]: rng.gauss(0.0, case_sd)
        for case in CASE_PLANS["A"]
    }
    recall_diffs: list[float] = []
    false_ready_diffs: list[float] = []
    for reviewer in retained:
        ability = rng.gauss(0.0, reviewer_sd)
        form = "A" if reviewer % 2 == 0 else "B"
        rec = {"BASELINE": [], "IPEL": []}
        false_ready = {"BASELINE": [], "IPEL": []}
        for case in CASE_PLANS[form]:
            presentation = case["presentation"]
            stratum_shift = judgment_penalty if case["stratum"] == "judgment_sensitive" else 0.0
            p_recall = min(0.97, max(0.03, baseline_recall + (recall_delta if presentation == "IPEL" else 0.0)))
            recall_logit = logit(p_recall) + ability + case_effects[case["case_id"]] + stratum_shift
            for _ in range(case["missing_opportunities"]):
                rec[presentation].append(int(rng.random() < logistic(recall_logit)))

            p_false = min(0.97, max(0.01, baseline_false_ready + (false_ready_delta if presentation == "IPEL" else 0.0)))
            false_logit = logit(p_false) - 0.35 * ability - 0.5 * case_effects[case["case_id"]] - 0.5 * stratum_shift
            false_ready[presentation].append(int(rng.random() < logistic(false_logit)))

        recall_diffs.append(
            sum(rec["IPEL"]) / len(rec["IPEL"]) - sum(rec["BASELINE"]) / len(rec["BASELINE"])
        )
        false_ready_diffs.append(
            sum(false_ready["IPEL"]) / len(false_ready["IPEL"]) -
            sum(false_ready["BASELINE"]) / len(false_ready["BASELINE"])
        )
    return z_from_paired(recall_diffs) > 1.96, z_from_paired(false_ready_diffs) < -1.96, len(retained)


def scenario_power(*, n_reviewers: int, recall_delta: float, false_ready_delta: float, replicates: int, seed: int) -> dict:
    rng = random.Random(seed)
    recall_hits = false_hits = retained_total = 0
    for _ in range(replicates):
        h1, hfr, retained = simulate_once(
            rng, n_reviewers, 0.65, recall_delta, 0.20, false_ready_delta,
            0.10, 0.55, 0.45, -0.25,
        )
        recall_hits += h1
        false_hits += hfr
        retained_total += retained
    return {
        "n_recruited": n_reviewers,
        "mean_n_retained": retained_total / replicates,
        "assumed_baseline_missing_recall": 0.65,
        "assumed_ipel_recall_improvement": recall_delta,
        "assumed_baseline_false_ready_rate": 0.20,
        "assumed_ipel_false_ready_change": false_ready_delta,
        "attrition": 0.10,
        "reviewer_logit_sd": 0.55,
        "case_logit_sd": 0.45,
        "judgment_sensitive_logit_penalty": -0.25,
        "not_ready_cases_per_form": TOTAL_NOT_READY_CASES,
        "missing_information_opportunities": TOTAL_MISSING_OPPORTUNITIES,
        "replicates": replicates,
        "approx_power_h1_missing_recall": recall_hits / replicates,
        "approx_power_false_ready_reduction": false_hits / replicates,
    }


def build_grid(replicates: int = 400) -> dict:
    scenarios = []
    index = 0
    for n in (24, 36, 48, 72):
        for recall_delta, false_delta in ((0.05, -0.03), (0.10, -0.05), (0.15, -0.08), (0.20, -0.10)):
            index += 1
            scenarios.append(scenario_power(
                n_reviewers=n,
                recall_delta=recall_delta,
                false_ready_delta=false_delta,
                replicates=replicates,
                seed=BASE_SEED + index * 1009,
            ))
    return {
        "stage": "007",
        "artifact": "POWER_DESIGN_GRID_NOT_FINAL_SAMPLE_SIZE",
        "human_outcomes_used": False,
        "final_sample_size_locked": False,
        "seed": BASE_SEED,
        "stage006_structure": {
            "not_ready_cases": TOTAL_NOT_READY_CASES,
            "missing_information_opportunities": TOTAL_MISSING_OPPORTUNITIES,
            "forms": ["A", "B"],
            "strata": ["objective", "judgment_sensitive"],
        },
        "test_note": (
            "Approximate planning power uses the actual Stage-006 Form A/B assignment and 13 missing-information "
            "opportunities, reviewer/case heterogeneity, a prespecified judgment-sensitive penalty, reviewer-level "
            "paired differences, and a |z|>1.96 rule. It is a sensitivity grid, not the final inferential model."
        ),
        "scenarios": scenarios,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--replicates", type=int, default=400)
    args = parser.parse_args()
    report = build_grid(args.replicates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
