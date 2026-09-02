"""Stage 014 — corrected-profile (0.2.0) benchmark execution.

Runs, in order:

1. verification that the frozen Stage 013 rubric, lock, and candidate registry
   are unmodified;
2. the Article 26(4) + Article 37(1) + Implementing Regulations Article
   30(1)-(6) condition x state benchmark on record profile 0.2.0;
3. the controlled delegation round-trips for every preregistered candidate;
4. application of the locked rubric v1.0.0 to the preregistered candidates;
5. the naive provenance-mapping baseline comparison;
6. the corrected-profile semantic mapping/round-trip coverage check.

Every artifact is written deterministically. Historical Stage 001-005 outputs
are never rewritten by this script.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ipel.semantic_equivalence import canonical_sha256  # noqa: E402
from src.ipel.stage014_benchmark import (  # noqa: E402
    BENCHMARK_VERSION,
    apply_rubric,
    build_condition_benchmark,
    compare_against_naive_baseline,
    corrected_profile_roundtrip,
    run_delegation_roundtrips,
)

STAGE013_DIR = ROOT / "benchmarks/stage013"
STAGE014_DIR = ROOT / "benchmarks/stage014"
GENERATED = STAGE014_DIR / "generated"
BASE_RECORD = ROOT / "examples/records/valid_v020_art37.json"


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def verify_frozen_inputs(rubric, registry, lock):
    """Fail closed if any frozen Stage 013 input drifted from its lock."""
    rubric_hash = canonical_sha256(rubric)
    registry_hash = canonical_sha256(registry)
    verification = {
        "rubric_definition_canonical_sha256": rubric_hash,
        "candidate_registry_canonical_sha256": registry_hash,
        "rubric_matches_lock": rubric_hash == lock["rubric_definition_canonical_sha256"],
        "registry_matches_lock": registry_hash == lock["candidate_registry_canonical_sha256"],
        "lock_status": lock["status"],
        "lock_source_commit_sha": lock["source_commit_sha"],
        "rubric_version": rubric["rubric_version"],
        "registry_candidates_still_marked_not_run": all(
            candidate["assessment_status"] == "NOT_RUN" for candidate in registry["candidates"]
        ),
        "registry_benchmark_executed_flag_unchanged": registry["benchmark_executed"] is False,
    }
    if not (
        verification["rubric_matches_lock"]
        and verification["registry_matches_lock"]
        and verification["registry_candidates_still_marked_not_run"]
        and verification["registry_benchmark_executed_flag_unchanged"]
    ):
        raise SystemExit("frozen Stage 013 inputs do not match the pre-outcome lock; refusing to run")
    return verification


def check_assessment_shape(assessments, schema) -> None:
    """Dependency-free structural check against the committed assessment schema."""
    allowed = set(schema["properties"])
    required = set(schema["required"])
    allowed_dims = set(schema["properties"]["dimension_assessments"]["properties"])
    for assessment in assessments["assessments"]:
        keys = set(assessment)
        extra = sorted(keys - allowed)
        missing = sorted(required - keys)
        if extra or missing:
            raise SystemExit(
                "assessment {0} violates the schema shape: missing={1} extra={2}".format(
                    assessment.get("candidate_id"), missing, extra
                )
            )
        unknown_dims = sorted(set(assessment["dimension_assessments"]) - allowed_dims)
        if unknown_dims:
            raise SystemExit(
                "assessment {0} declares unknown dimensions: {1}".format(
                    assessment.get("candidate_id"), unknown_dims
                )
            )


def main() -> int:
    rubric = _read(STAGE013_DIR / "rubric_definition.json")
    registry = _read(STAGE013_DIR / "candidate_registry.json")
    lock = _read(STAGE013_DIR / "rubric_lock.json")
    assessments = _read(STAGE014_DIR / "candidate_assessments.json")
    schema = _read(ROOT / "schemas/semantic-equivalence-assessment.schema.json")
    base = _read(BASE_RECORD)

    frozen_input_verification = verify_frozen_inputs(rubric, registry, lock)
    check_assessment_shape(assessments, schema)

    benchmark = build_condition_benchmark(base)
    roundtrips = run_delegation_roundtrips(base)
    roundtrip_index = {row["candidate_id"]: row for row in roundtrips["roundtrips"]}
    delegation = apply_rubric(rubric, registry, assessments, roundtrip_index)
    safe_candidate_ids = delegation["safe_delegation_candidate_ids"]
    comparison = compare_against_naive_baseline(base, benchmark, safe_candidate_ids)
    mapping = corrected_profile_roundtrip(base, benchmark)

    _write(GENERATED / "condition_state_benchmark.json", benchmark)
    _write(GENERATED / "delegation_roundtrip.json", roundtrips)
    _write(GENERATED / "delegation_assessment_results.json", delegation)
    _write(GENERATED / "naive_baseline_comparison.json", comparison)
    _write(GENERATED / "corrected_profile_roundtrip.json", mapping)

    favorable = comparison["signal_profiles"]["favorable_provenance"]
    unknown = comparison["signal_profiles"]["unknown_provenance"]
    result = {
        "benchmark_version": BENCHMARK_VERSION,
        "stage": "014",
        "record_profile_version": "0.2.0",
        "legal_profile_id": benchmark["expected_legal_profile_id"],
        "rubric_version": delegation["rubric_version"],
        "rubric_reused_without_modification": True,
        "candidate_selection_unchanged_after_lock": True,
        "frozen_input_verification": frozen_input_verification,
        "legal_conclusion": False,
        "condition_benchmark": {
            "case_count": benchmark["case_count"],
            "condition_count": len(benchmark["condition_coverage"]),
            "all_outcomes_match_expectation": benchmark["all_outcomes_match_expectation"],
            "all_expected_findings_present": benchmark["all_expected_findings_present"],
            "state_counts": benchmark["state_counts"],
            "conditions_without_adverse_state_in_profile": sorted(
                entry["condition_id"]
                for entry in benchmark["condition_coverage"]
                if not entry["adverse_state_available_in_profile"]
            ),
            "conditions_without_unresolved_state_in_profile": sorted(
                entry["condition_id"]
                for entry in benchmark["condition_coverage"]
                if not entry["unresolved_state_available_in_profile"]
            ),
        },
        "delegation_assessment": {
            "candidate_count": delegation["candidate_count"],
            "decision_counts": delegation["decision_counts"],
            "safe_delegation_ipel_paths": delegation["safe_delegation_ipel_paths"],
            "article_30_3_safe_delegation_ratio": delegation["article_30_3_safe_delegation_ratio"],
            "article_37_safe_delegation_ratio": delegation["article_37_safe_delegation_ratio"],
            "ipel_fields_retained_count": delegation["ipel_fields_retained_count"],
        },
        "delegation_roundtrip": {
            "executed_candidate_count": roundtrips["executed_candidate_count"],
            "roundtrip_pass_count": roundtrips["roundtrip_pass_count"],
            "gate_silent_semantic_corruption_count": roundtrips["gate_silent_semantic_corruption_count"],
            "inference_required_count": roundtrips["inference_required_count"],
        },
        "naive_baseline_comparison": {
            "naive_delegated_path_count": comparison["naive_delegated_path_count"],
            "naive_inferred_path_count": comparison["naive_inferred_path_count"],
            "rubric_governed_delegated_path_count": comparison["rubric_governed_delegated_path_count"],
            "delegation_difference": comparison["delegation_difference"],
            "favorable_provenance": {
                "case_count": favorable["case_count"],
                "naive_outcome_preserved_count": favorable["naive_outcome_preserved_count"],
                "naive_false_equivalence_count": favorable["naive_false_equivalence_count"],
                "naive_spurious_escalation_count": favorable["naive_spurious_escalation_count"],
                "rubric_governed_outcome_preserved_count": favorable["rubric_governed_outcome_preserved_count"],
            },
            "unknown_provenance": {
                "case_count": unknown["case_count"],
                "naive_outcome_preserved_count": unknown["naive_outcome_preserved_count"],
                "naive_false_equivalence_count": unknown["naive_false_equivalence_count"],
                "naive_spurious_escalation_count": unknown["naive_spurious_escalation_count"],
                "rubric_governed_outcome_preserved_count": unknown["rubric_governed_outcome_preserved_count"],
            },
            "naive_outcome_unstable_across_provenance_signal_count": comparison[
                "naive_outcome_unstable_across_provenance_signal_count"
            ],
        },
        "corrected_profile_roundtrip": {
            "case_count": mapping["case_count"],
            "profile_constructed_count": mapping["profile_constructed_count"],
            "profile_failed_closed_count": mapping["profile_failed_closed_count"],
            "all_constructed_gate_outcomes_preserved": mapping["all_constructed_gate_outcomes_preserved"],
            "all_constructed_article_30_3_tuples_preserved": mapping[
                "all_constructed_article_30_3_tuples_preserved"
            ],
            "all_constructed_article_37_tuples_preserved": mapping[
                "all_constructed_article_37_tuples_preserved"
            ],
            "all_constructed_roundtrips_zero_semantic_loss": mapping[
                "all_constructed_roundtrips_zero_semantic_loss"
            ],
            "supersedes_legacy_stage003_evidence_for": mapping["supersedes_legacy_stage003_evidence_for"],
            "legacy_stage003_artifacts_preserved": mapping["legacy_stage003_artifacts_preserved"],
        },
        "artifacts": [
            "benchmarks/stage014/generated/condition_state_benchmark.json",
            "benchmarks/stage014/generated/corrected_profile_roundtrip.json",
            "benchmarks/stage014/generated/delegation_assessment_results.json",
            "benchmarks/stage014/generated/delegation_roundtrip.json",
            "benchmarks/stage014/generated/naive_baseline_comparison.json",
        ],
        "controller_decision": "NOT_MADE_BY_THIS_STAGE",
    }
    _write(GENERATED / "stage014_result.json", result)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
