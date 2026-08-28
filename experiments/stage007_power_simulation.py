#!/usr/bin/env python3
"""Simulation-based design grid for the future Stage-006 reviewer study.

This is planning output only. It does not choose a final N and does not use human outcomes.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
) -> tuple[bool, bool, int]:
    retained = [i for i in range(n_reviewers) if rng.random() >= attrition]
    if len(retained) < 4:
        return False, False, len(retained)
    case_effects = [rng.gauss(0.0, case_sd) for _ in range(12)]
    recall_diffs: list[float] = []
    false_ready_diffs: list[float] = []
    for reviewer in retained:
        ability = rng.gauss(0.0, reviewer_sd)
        form_flip = reviewer % 2
        rec_base: list[int] = []
        rec_ipel: list[int] = []
        fr_base: list[int] = []
        fr_ipel: list[int] = []
        for case_idx in range(12):
            ipel = ((case_idx % 2) ^ form_flip) == 1
            p_recall = baseline_recall + (recall_delta if ipel else 0.0)
            p_recall = min(0.97, max(0.03, p_recall))
            p_recall = logistic(logit(p_recall) + ability + case_effects[case_idx])
            detected = int(rng.random() < p_recall)
            p_false = baseline_false_ready + (false_ready_delta if ipel else 0.0)
            p_false = min(0.97, max(0.01, p_false))
            p_false = logistic(logit(p_false) - 0.35 * ability - 0.5 * case_effects[case_idx])
            false_ready = int(rng.random() < p_false)
            if ipel:
                rec_ipel.append(detected)
                fr_ipel.append(false_ready)
            else:
                rec_base.append(detected)
                fr_base.append(false_ready)
        recall_diffs.append(sum(rec_ipel) / len(rec_ipel) - sum(rec_base) / len(rec_base))
        false_ready_diffs.append(sum(fr_ipel) / len(fr_ipel) - sum(fr_base) / len(fr_base))
    recall_sig = z_from_paired(recall_diffs) > 1.96
    false_ready_sig = z_from_paired(false_ready_diffs) < -1.96
    return recall_sig, false_ready_sig, len(retained)


def scenario_power(
    *,
    n_reviewers: int,
    recall_delta: float,
    false_ready_delta: float,
    replicates: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    recall_hits = 0
    false_hits = 0
    retained_total = 0
    for _ in range(replicates):
        h1, hfr, retained = simulate_once(
            rng,
            n_reviewers=n_reviewers,
            baseline_recall=0.65,
            recall_delta=recall_delta,
            baseline_false_ready=0.20,
            false_ready_delta=false_ready_delta,
            attrition=0.10,
            reviewer_sd=0.55,
            case_sd=0.45,
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
        "test_note": (
            "Approximate planning power uses reviewer-level paired differences and a |z|>1.96 rule. "
            "It is a design-sensitivity grid, not the final inferential model."
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
