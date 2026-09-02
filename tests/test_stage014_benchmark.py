import copy
import json
import unittest
from pathlib import Path

from src.ipel.semantic_equivalence import canonical_sha256
from src.ipel.stage014_benchmark import (
    ADVERSE,
    FAVORABLE,
    UNRESOLVED,
    apply_rubric,
    build_condition_benchmark,
    compare_against_naive_baseline,
    corrected_profile_roundtrip,
    run_delegation_roundtrips,
)

ROOT = Path(__file__).resolve().parents[1]
STAGE013 = ROOT / "benchmarks/stage013"
STAGE014 = ROOT / "benchmarks/stage014"
GENERATED = STAGE014 / "generated"


def _read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _rebuild():
    rubric = _read("benchmarks/stage013/rubric_definition.json")
    registry = _read("benchmarks/stage013/candidate_registry.json")
    assessments = _read("benchmarks/stage014/candidate_assessments.json")
    base = _read("examples/records/valid_v020_art37.json")

    benchmark = build_condition_benchmark(base)
    roundtrips = run_delegation_roundtrips(base)
    index = {row["candidate_id"]: row for row in roundtrips["roundtrips"]}
    delegation = apply_rubric(rubric, registry, assessments, index)
    comparison = compare_against_naive_baseline(
        base, benchmark, delegation["safe_delegation_candidate_ids"]
    )
    mapping = corrected_profile_roundtrip(base, benchmark)
    return {
        "condition_state_benchmark.json": benchmark,
        "delegation_roundtrip.json": roundtrips,
        "delegation_assessment_results.json": delegation,
        "naive_baseline_comparison.json": comparison,
        "corrected_profile_roundtrip.json": mapping,
    }


class Stage014FrozenInputTests(unittest.TestCase):
    def test_frozen_stage013_inputs_are_unmodified_by_stage014(self):
        lock = _read("benchmarks/stage013/rubric_lock.json")
        rubric = _read("benchmarks/stage013/rubric_definition.json")
        registry = _read("benchmarks/stage013/candidate_registry.json")
        self.assertEqual(lock["rubric_definition_canonical_sha256"], canonical_sha256(rubric))
        self.assertEqual(lock["candidate_registry_canonical_sha256"], canonical_sha256(registry))
        self.assertFalse(registry["benchmark_executed"])
        self.assertTrue(all(row["assessment_status"] == "NOT_RUN" for row in registry["candidates"]))

    def test_stage014_assesses_exactly_the_preregistered_candidates(self):
        registry = _read("benchmarks/stage013/candidate_registry.json")
        assessments = _read("benchmarks/stage014/candidate_assessments.json")
        self.assertEqual(
            sorted(row["candidate_id"] for row in registry["candidates"]),
            sorted(row["candidate_id"] for row in assessments["assessments"]),
        )
        self.assertEqual(assessments["rubric_version"], "1.0.0")

    def test_assessments_match_the_committed_assessment_schema_shape(self):
        schema = _read("schemas/semantic-equivalence-assessment.schema.json")
        assessments = _read("benchmarks/stage014/candidate_assessments.json")
        allowed = set(schema["properties"])
        required = set(schema["required"])
        allowed_dims = set(schema["properties"]["dimension_assessments"]["properties"])
        for assessment in assessments["assessments"]:
            self.assertEqual(set(assessment) - allowed, set())
            self.assertEqual(required - set(assessment), set())
            self.assertEqual(set(assessment["dimension_assessments"]) - allowed_dims, set())


class Stage014DeterminismTests(unittest.TestCase):
    def test_committed_artifacts_are_reproducible(self):
        for name, payload in _rebuild().items():
            committed = json.loads((GENERATED / name).read_text(encoding="utf-8"))
            self.assertEqual(committed, payload, name)

    def test_result_summary_matches_the_detailed_artifacts(self):
        result = _read("benchmarks/stage014/generated/stage014_result.json")
        benchmark = _read("benchmarks/stage014/generated/condition_state_benchmark.json")
        delegation = _read("benchmarks/stage014/generated/delegation_assessment_results.json")
        self.assertEqual(result["condition_benchmark"]["case_count"], benchmark["case_count"])
        self.assertEqual(
            result["delegation_assessment"]["decision_counts"], delegation["decision_counts"]
        )
        self.assertFalse(result["legal_conclusion"])
        self.assertEqual(result["controller_decision"], "NOT_MADE_BY_THIS_STAGE")


class Stage014ConditionCoverageTests(unittest.TestCase):
    def setUp(self):
        self.benchmark = _read("benchmarks/stage014/generated/condition_state_benchmark.json")

    def test_every_case_matches_its_declared_expectation(self):
        self.assertTrue(self.benchmark["all_outcomes_match_expectation"])
        self.assertTrue(self.benchmark["all_expected_findings_present"])
        for row in self.benchmark["cases"]:
            self.assertEqual(row["observed_outcome"], row["expected_outcome"], row["case_id"])
            self.assertFalse(row["legal_conclusion"], row["case_id"])

    def test_all_declared_provisions_are_covered_by_at_least_one_state(self):
        conditions = {entry["condition_id"] for entry in self.benchmark["condition_coverage"]}
        for required in (
            "LAW-26(4)-publication",
            "LAW-26(4)-acquisition",
            "LAW-26(4)/IR-30(1)-necessity",
            "LAW-37(1)-normal-exploitation",
            "LAW-37(1)-rightsholder-interests",
            "IR-30(1)-prohibited-uses",
            "IR-30(2)-commercial-context",
            "IR-30(3)-retained-record",
            "IR-30(4)-author-interests",
            "IR-30(5)-output-configuration",
            "IR-30(6)-independent-elements",
        ):
            self.assertIn(required, conditions)

    def test_state_coverage_is_reported_honestly_where_a_state_does_not_exist(self):
        for entry in self.benchmark["condition_coverage"]:
            self.assertTrue(entry["favorable_state_covered"], entry["condition_id"])
            self.assertEqual(
                entry["adverse_state_covered"],
                entry["adverse_state_available_in_profile"],
                entry["condition_id"],
            )
            self.assertEqual(
                entry["unresolved_state_covered"],
                entry["unresolved_state_available_in_profile"],
                entry["condition_id"],
            )
            if not entry["adverse_state_available_in_profile"] or not entry[
                "unresolved_state_available_in_profile"
            ]:
                self.assertIn("state_absence_note", entry)

    def test_profile_metadata_is_exposed_for_every_supported_case(self):
        for row in self.benchmark["cases"]:
            if row["case_id"] == "profile_adverse_unsupported_version":
                self.assertEqual(row["legal_profile_id"], "unsupported-record-profile")
                self.assertFalse(row["declared_scope_complete"])
                self.assertEqual(row["observed_outcome"], "FAIL_EVIDENCE_GATE")
            else:
                self.assertEqual(
                    row["legal_profile_id"], "sa-copyright-2026-art26-4-art37-1-ir30-v0.2", row["case_id"]
                )
                self.assertTrue(row["declared_scope_complete"], row["case_id"])

    def test_article37_survives_favorable_regulation_fields_and_is_not_conflated(self):
        cases = {row["case_id"]: row for row in self.benchmark["cases"]}

        masked_art37 = [
            cases["art37_normal_exploitation_adverse_with_favorable_ir30"],
            cases["art37_rightsholder_adverse_with_favorable_ir30_4"],
        ]
        for row in masked_art37:
            self.assertEqual(row["observed_outcome"], "FAIL_EVIDENCE_GATE", row["case_id"])
            self.assertIn("LAW-37(1)", row["rule_ids"], row["case_id"])
            self.assertNotIn("IR-30(2)", row["rule_ids"], row["case_id"])
            self.assertNotIn("IR-30(4)", row["rule_ids"], row["case_id"])

        regulation_only = [
            ("ir30_2_adverse_with_favorable_art37", "IR-30(2)"),
            ("ir30_4_adverse_with_favorable_art37", "IR-30(4)"),
        ]
        for case_id, rule in regulation_only:
            row = cases[case_id]
            self.assertEqual(row["observed_outcome"], "FAIL_EVIDENCE_GATE", case_id)
            self.assertIn(rule, row["rule_ids"], case_id)
            self.assertNotIn("LAW-37(1)", row["rule_ids"], case_id)

    def test_states_cover_adverse_unresolved_and_favorable(self):
        self.assertGreater(self.benchmark["state_counts"][ADVERSE], 0)
        self.assertGreater(self.benchmark["state_counts"][UNRESOLVED], 0)
        self.assertGreater(self.benchmark["state_counts"][FAVORABLE], 0)


class Stage014DelegationTests(unittest.TestCase):
    def setUp(self):
        self.rubric = _read("benchmarks/stage013/rubric_definition.json")
        self.registry = _read("benchmarks/stage013/candidate_registry.json")
        self.assessments = _read("benchmarks/stage014/candidate_assessments.json")
        self.roundtrips = _read("benchmarks/stage014/generated/delegation_roundtrip.json")
        self.index = {row["candidate_id"]: row for row in self.roundtrips["roundtrips"]}
        self.delegation = _read("benchmarks/stage014/generated/delegation_assessment_results.json")

    def test_safe_delegation_satisfies_every_locked_criterion(self):
        safe = [row for row in self.delegation["assessments"] if row["decision"] == "SAFE_DELEGATION"]
        for row in safe:
            self.assertIn(row["candidate_kind"], {"NORMATIVE_FIELD", "NORMATIVE_ASSERTION"})
            self.assertEqual(row["failed_dimensions"], [])
            self.assertEqual(row["inference_dependencies"], [])
            self.assertTrue(row["roundtrip_tested"])
            self.assertTrue(row["roundtrip_pass_declared"])
            self.assertTrue(row["roundtrip_pass_measured"])
            self.assertFalse(row["ipel_field_retained"])

    def test_no_article_30_3_or_article_37_field_is_safely_delegable(self):
        self.assertEqual(self.delegation["article_30_3_fields_safely_delegable"], [])
        self.assertEqual(self.delegation["article_37_fields_safely_delegable"], [])
        self.assertEqual(self.delegation["article_30_3_safe_delegation_ratio"], "0/4")
        self.assertEqual(self.delegation["article_37_safe_delegation_ratio"], "0/2")

    def test_partial_support_and_no_candidate_always_retain_the_ipel_field(self):
        for row in self.delegation["assessments"]:
            if row["decision"] in {"PARTIAL_SUPPORT", "NOT_SAFE_TO_DELEGATE", "NO_CANDIDATE"}:
                self.assertTrue(row["ipel_field_retained"], row["candidate_id"])

    def test_declared_roundtrip_state_must_match_the_measurement(self):
        tampered = copy.deepcopy(self.assessments)
        for row in tampered["assessments"]:
            if row["candidate_id"] == "work-type__c2pa-dc-format":
                row["roundtrip_pass"] = True
        with self.assertRaises(ValueError):
            apply_rubric(self.rubric, self.registry, tampered, self.index)

    def test_no_candidate_rows_cannot_claim_a_roundtrip(self):
        tampered = copy.deepcopy(self.assessments)
        for row in tampered["assessments"]:
            if row["candidate_id"] == "art37-normal-exploitation__none":
                row["roundtrip_tested"] = True
                row["roundtrip_pass"] = True
        with self.assertRaises(ValueError):
            apply_rubric(self.rubric, self.registry, tampered, self.index)

    def test_safe_delegation_collapses_when_any_locked_criterion_is_removed(self):
        for mutation in ("fail_critical_dimension", "add_prohibited_dependency", "fail_roundtrip"):
            tampered = copy.deepcopy(self.assessments)
            index = copy.deepcopy(self.index)
            for row in tampered["assessments"]:
                if row["candidate_id"] != "work-title__c2pa-dc-title":
                    continue
                if mutation == "fail_critical_dimension":
                    row["dimension_assessments"]["normative_maintained_spec_status"]["status"] = "FAIL"
                elif mutation == "add_prohibited_dependency":
                    row["inference_dependencies"] = ["SIGNER_TRUST"]
                else:
                    row["roundtrip_pass"] = False
                    index["work-title__c2pa-dc-title"]["roundtrip_pass"] = False
            result = apply_rubric(self.rubric, self.registry, tampered, index)
            self.assertEqual(result["decision_counts"]["SAFE_DELEGATION"], 0, mutation)

    def test_candidate_set_cannot_be_changed_after_the_lock(self):
        tampered = copy.deepcopy(self.assessments)
        tampered["assessments"] = tampered["assessments"][:-1]
        with self.assertRaises(ValueError):
            apply_rubric(self.rubric, self.registry, tampered, self.index)

    def test_roundtrip_harness_separates_value_recovery_from_semantic_equivalence(self):
        rows = {row["candidate_id"]: row for row in self.roundtrips["roundtrips"]}
        action_when = rows["use-date__c2pa-action-when"]
        self.assertTrue(action_when["value_preserved"])
        self.assertTrue(action_when["inference_required"])
        self.assertFalse(action_when["roundtrip_pass"])
        self.assertGreater(self.roundtrips["gate_silent_semantic_corruption_count"], 0)


class Stage014NaiveBaselineTests(unittest.TestCase):
    def setUp(self):
        self.comparison = _read("benchmarks/stage014/generated/naive_baseline_comparison.json")

    def test_rubric_governed_mapping_preserves_every_gate_outcome(self):
        for name, profile in self.comparison["signal_profiles"].items():
            self.assertEqual(
                profile["rubric_governed_outcome_preserved_count"], profile["case_count"], name
            )
            self.assertEqual(profile["rubric_governed_total_semantic_loss_paths"], 0, name)

    def test_naive_baseline_produces_false_equivalences_the_rubric_mapping_does_not(self):
        for name, profile in self.comparison["signal_profiles"].items():
            self.assertGreater(profile["naive_false_equivalence_count"], 0, name)
            self.assertLess(
                profile["naive_outcome_preserved_count"], profile["case_count"], name
            )

    def test_naive_baseline_masks_article37_and_article_26_4_adverse_facts(self):
        favorable = self.comparison["signal_profiles"]["favorable_provenance"]
        masked = set(favorable["naive_false_equivalence_case_ids"])
        for case_id in (
            "art37_normal_exploitation_adverse",
            "art37_rightsholder_adverse",
            "law26_4_acquisition_adverse",
            "law26_4_publication_adverse",
        ):
            self.assertIn(case_id, masked)

    def test_naive_outcomes_track_provenance_signals_rather_than_legal_facts(self):
        self.assertGreater(
            self.comparison["naive_outcome_unstable_across_provenance_signal_count"], 0
        )
        self.assertTrue(self.comparison["rubric_governed_outcome_invariant_to_provenance_signals"])
        favorable = self.comparison["signal_profiles"]["favorable_provenance"]
        unknown = self.comparison["signal_profiles"]["unknown_provenance"]
        governed_favorable = {
            row["case_id"]: row["rubric_governed_outcome"] for row in favorable["cases"]
        }
        governed_unknown = {
            row["case_id"]: row["rubric_governed_outcome"] for row in unknown["cases"]
        }
        self.assertEqual(governed_favorable, governed_unknown)

    def test_naive_baseline_delegates_and_infers_more_than_the_rubric_allows(self):
        self.assertGreater(
            self.comparison["naive_delegated_path_count"],
            self.comparison["rubric_governed_delegated_path_count"],
        )
        self.assertGreater(self.comparison["naive_inferred_path_count"], 0)
        self.assertEqual(self.comparison["rubric_governed_inferred_path_count"], 0)


class Stage014MappingCoverageTests(unittest.TestCase):
    def setUp(self):
        self.mapping = _read("benchmarks/stage014/generated/corrected_profile_roundtrip.json")

    def test_corrected_profile_roundtrip_preserves_gate_and_article37_state(self):
        self.assertTrue(self.mapping["all_constructed_gate_outcomes_preserved"])
        self.assertTrue(self.mapping["all_constructed_article_30_3_tuples_preserved"])
        self.assertTrue(self.mapping["all_constructed_article_37_tuples_preserved"])
        self.assertTrue(self.mapping["all_constructed_roundtrips_zero_semantic_loss"])

    def test_missing_core_record_fields_fail_closed_in_the_profile_contract(self):
        self.assertEqual(
            self.mapping["profile_failed_closed_case_ids"],
            [
                "ir30_3_adverse_missing_use_date",
                "ir30_3_adverse_missing_use_purpose",
                "ir30_3_adverse_missing_work_source",
                "ir30_3_adverse_missing_work_type",
            ],
        )
        for row in self.mapping["cases"]:
            if not row["profile_constructed"]:
                self.assertTrue(row["fails_closed"], row["case_id"])
                self.assertTrue(row["profile_construction_error"], row["case_id"])


class Stage014LegacyPreservationTests(unittest.TestCase):
    def test_legacy_stage003_artifacts_are_untouched_0_1_0_evidence(self):
        legacy_profile = _read("examples/profiles/stage003_clean.json")
        self.assertEqual(legacy_profile["ipel_jurisdictional"]["record_version"], "0.1.0")
        legacy_report = _read("reports/stage003_semantic_roundtrip.json")
        self.assertEqual(legacy_report["stage"], "003")
        self.assertEqual(legacy_report["case_count"], 5)

    def test_stage014_claims_replacement_only_for_the_corrected_profile(self):
        mapping = _read("benchmarks/stage014/generated/corrected_profile_roundtrip.json")
        self.assertEqual(mapping["supersedes_legacy_stage003_evidence_for"], "record profile 0.2.0 only")
        self.assertTrue(mapping["legacy_stage003_artifacts_preserved"])
        self.assertEqual(mapping["record_profile_version"], "0.2.0")


class Stage014ReportTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "reports/STAGE_014_REPORT.md").read_text(encoding="utf-8")
        self.result = _read("benchmarks/stage014/generated/stage014_result.json")

    def test_report_states_the_measured_delegation_result(self):
        counts = self.result["delegation_assessment"]["decision_counts"]
        self.assertIn("SAFE_DELEGATION | {0}".format(counts["SAFE_DELEGATION"]), self.text)
        self.assertIn("PARTIAL_SUPPORT | {0}".format(counts["PARTIAL_SUPPORT"]), self.text)
        self.assertIn("NO_CANDIDATE | {0}".format(counts["NO_CANDIDATE"]), self.text)
        self.assertIn("0/4", self.text)
        self.assertIn("0/2", self.text)

    def test_report_reserves_the_controller_decision_and_disclaims_legal_conclusions(self):
        self.assertIn("KEEP/NARROW/WITHDRAW", self.text)
        self.assertIn("Controller", self.text)
        self.assertIn("not a legal conclusion", self.text)

    def test_report_records_negative_and_unresolved_results(self):
        self.assertIn("Negative and unresolved results", self.text)
        self.assertIn("IR-30(6)-independent-elements", self.text)


if __name__ == "__main__":
    unittest.main()
