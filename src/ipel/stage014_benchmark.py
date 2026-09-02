"""Stage 014 corrected-profile (0.2.0) condition-coverage and delegation benchmark.

The module builds the deterministic Copyright Law Article 26(4) + Copyright Law
Article 37(1) + Implementing Regulations Article 30(1)-(6) condition x state
benchmark on record profile ``0.2.0``, executes the controlled delegation
round-trips used as measured evidence for the frozen Stage 013 rubric, and
implements the naive provenance-mapping baseline used as an explicit comparator.

It *applies* the frozen Stage 013 rubric. It does not define, weaken, or extend
it, and it produces no legal conclusion. Legacy profile ``0.1.0`` artifacts are
not touched: this module never writes into the Stage 001-005 outputs.
"""

from __future__ import annotations

import copy
import datetime
from typing import Any, Dict, List, Optional, Tuple

from src.ipel.c2pa_profile import (
    ProfileError,
    from_profile,
    roundtrip_metrics,
    semantic_loss,
    to_profile,
)
from src.ipel.semantic_equivalence import classify_assessment
from src.ipel.validator import (
    CURRENT_PROFILE_ID,
    CURRENT_RECORD_VERSION,
    FAIL,
    PASS,
    REVIEW,
    evaluate,
)

BENCHMARK_VERSION = "stage014-corrected-profile-benchmark-v1"
RUBRIC_VERSION = "1.0.0"

OUTCOME_SEVERITY = {PASS: 0, REVIEW: 1, FAIL: 2}

FAVORABLE = "FAVORABLE_EVIDENCE_READY"
UNRESOLVED = "UNRESOLVED_REVIEW"
ADVERSE = "ADVERSE_FAIL"

STATE_BY_OUTCOME = {PASS: FAVORABLE, REVIEW: UNRESOLVED, FAIL: ADVERSE}
SEVERITY_BY_OUTCOME = {REVIEW: "REVIEW", FAIL: "FAIL"}

# Synthetic, spec-shaped provenance values for the single benchmark asset. They
# are fixtures for a controlled substitution experiment, not observations about
# any real asset, and no assessment turns on the particular token chosen.
SYNTHETIC_MANIFEST_REF = "urn:c2pa:manifest:stage014-synthetic"
SYNTHETIC_FORMAT = "text/plain"
SYNTHETIC_DATA_TYPE = "c2pa.types.dataset"
SYNTHETIC_INFORMATIONAL_URI = "https://example.org/about/synthetic-art37-001"
SYNTHETIC_DATA_REFERENCE_URL = "self#jumbf=c2pa.databoxes/c2pa.metadata"
SYNTHETIC_ACTION = "c2pa.converted"
SYNTHETIC_ACTION_TIME_OF_DAY = "T10:15:00Z"
SYNTHETIC_TIMESTAMP_OFFSET_DAYS = 1
SYNTHETIC_TDM_KEY = "cawg.ai_training"

PROVENANCE_SIGNAL_PROFILES = {
    "favorable_provenance": {"manifest_state": "valid", "trust_state": "trusted", "tdm_use": "allowed"},
    "unknown_provenance": {"manifest_state": "unknown", "trust_state": "unknown", "tdm_use": "constrained"},
}


# --------------------------------------------------------------------------
# dotted-path helpers
# --------------------------------------------------------------------------

def _get(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _set(obj: Dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = obj
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _delete(obj: Dict[str, Any], dotted: str) -> None:
    parts = dotted.split(".")
    cur: Any = obj
    for part in parts[:-1]:
        if not isinstance(cur, dict) or part not in cur:
            return
        cur = cur[part]
    if isinstance(cur, dict):
        cur.pop(parts[-1], None)


def apply_mutations(base: Dict[str, Any], mutations: List[Dict[str, Any]]) -> Dict[str, Any]:
    record = copy.deepcopy(base)
    for mutation in mutations:
        if mutation["op"] == "set":
            _set(record, mutation["path"], copy.deepcopy(mutation["value"]))
        elif mutation["op"] == "delete":
            _delete(record, mutation["path"])
        else:  # pragma: no cover - guarded by the case table
            raise ValueError("unsupported mutation op: {0!r}".format(mutation["op"]))
    return record


def _set_op(path: str, value: Any) -> Dict[str, Any]:
    return {"op": "set", "path": path, "value": value}


def _del_op(path: str) -> Dict[str, Any]:
    return {"op": "delete", "path": path}


# --------------------------------------------------------------------------
# condition x state benchmark
# --------------------------------------------------------------------------

# Each condition declares which gate rule id and message marker must carry the
# expected finding, so a case cannot silently be satisfied by an unrelated rule.
CONDITIONS: List[Dict[str, Any]] = [
    {
        "condition_id": "LAW-26(4)-publication",
        "legal_source": "Copyright Law Article 26(4)",
        "description": "Work was lawfully published.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "LAW-26(4)-acquisition",
        "legal_source": "Copyright Law Article 26(4)",
        "description": "Original copy was lawfully acquired.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "LAW-26(4)/IR-30(1)-necessity",
        "legal_source": "Copyright Law Article 26(4) with Implementing Regulations Article 30(1)",
        "description": "Copying/analysis is limited to what AI development requires.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "LAW-37(1)-normal-exploitation",
        "legal_source": "Copyright Law Article 37(1)",
        "description": "Use must not conflict with normal exploitation of the work.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "LAW-37(1)-rightsholder-interests",
        "legal_source": "Copyright Law Article 37(1)",
        "description": "Use must not cause unjustified prejudice to legitimate interests of rightsholders.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "IR-30(1)-prohibited-uses",
        "legal_source": "Implementing Regulations Article 30(1)",
        "description": "No republication, distribution, or direct commercial exploitation.",
        "adverse_state_available": True,
        "unresolved_state_available": False,
        "state_absence_note": "The encoded predicates are booleans, so the profile admits no unresolved state.",
    },
    {
        "condition_id": "IR-30(2)-commercial-context",
        "legal_source": "Implementing Regulations Article 30(2)",
        "description": "Purely commercial use has a narrow qualifying condition.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "IR-30(3)-retained-record",
        "legal_source": "Implementing Regulations Article 30(3)",
        "description": "Developer retains work type, source, purpose of use, and date of use.",
        "adverse_state_available": True,
        "unresolved_state_available": False,
        "state_absence_note": "Retention is modelled as presence/absence, so the profile admits no unresolved state.",
    },
    {
        "condition_id": "IR-30(4)-author-interests",
        "legal_source": "Implementing Regulations Article 30(4)",
        "description": "No unjustified prejudice to author interests or exploitation opportunity.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "IR-30(5)-output-configuration",
        "legal_source": "Implementing Regulations Article 30(5)",
        "description": "No prohibited transformation/republication/public availability or unnecessary inclusion.",
        "adverse_state_available": True,
        "unresolved_state_available": True,
    },
    {
        "condition_id": "IR-30(6)-independent-elements",
        "legal_source": "Implementing Regulations Article 30(6)",
        "description": "Independently protected elements must be respected.",
        "adverse_state_available": False,
        "unresolved_state_available": True,
        "state_absence_note": (
            "Profile 0.2.0 encodes no mechanically detectable adverse state for this condition; "
            "it can only escalate to review. Reported as an observed coverage limit, not as compliance."
        ),
    },
    {
        "condition_id": "EVIDENCE-references",
        "legal_source": "Evidence-quality check (project abstraction, not a distinct legal provision)",
        "description": "Assertions marked verified and the use event carry evidence references.",
        "adverse_state_available": False,
        "unresolved_state_available": True,
        "state_absence_note": "Missing evidence references escalate to review only; they never fail closed on their own.",
    },
    {
        "condition_id": "PROFILE-0.2.0-integrity",
        "legal_source": "IPEL legal-profile versioning policy",
        "description": "Profile 0.2.0 records must carry Article 37 context and a supported record version.",
        "adverse_state_available": True,
        "unresolved_state_available": False,
        "state_absence_note": "Profile integrity is modelled as fail-closed; there is no intermediate state.",
    },
]


def _cases() -> List[Dict[str, Any]]:
    """Preregistered condition x state cases for the corrected 0.2.0 profile."""
    cases: List[Dict[str, Any]] = []

    def add(case_id, condition_id, variant, expected_outcome, rule_id, marker, mutations):
        cases.append(
            {
                "case_id": case_id,
                "condition_id": condition_id,
                "variant": variant,
                "expected_outcome": expected_outcome,
                "expected_state": STATE_BY_OUTCOME[expected_outcome],
                "expected_rule_id": rule_id,
                "expected_message_marker": marker,
                "mutations": mutations,
            }
        )

    # --- Copyright Law Article 26(4): lawful publication -------------------
    add("law26_4_publication_favorable", "LAW-26(4)-publication", "verified_with_evidence", PASS, None, None, [])
    add(
        "law26_4_publication_unresolved", "LAW-26(4)-publication", "unverified", REVIEW,
        "LAW-26(4)", "Lawful publication is not verified",
        [_set_op("work.publication_status", "unverified")],
    )
    add(
        "law26_4_publication_adverse", "LAW-26(4)-publication", "explicitly_false", FAIL,
        "LAW-26(4)", "lawful publication is false",
        [_set_op("work.publication_status", "false")],
    )
    add(
        "law26_4_publication_favorable_without_evidence", "LAW-26(4)-publication",
        "verified_without_evidence_reference", REVIEW,
        "EVIDENCE", "Publication is marked verified but has no evidence reference",
        [_set_op("evidence.publication", [])],
    )

    # --- Copyright Law Article 26(4): lawful acquisition -------------------
    add("law26_4_acquisition_favorable", "LAW-26(4)-acquisition", "verified_with_evidence", PASS, None, None, [])
    add(
        "law26_4_acquisition_unresolved", "LAW-26(4)-acquisition", "unverified", REVIEW,
        "LAW-26(4)", "Lawful acquisition is not verified",
        [_set_op("work.acquisition_status", "unverified")],
    )
    add(
        "law26_4_acquisition_adverse", "LAW-26(4)-acquisition", "explicitly_false", FAIL,
        "LAW-26(4)", "lawful acquisition is false",
        [_set_op("work.acquisition_status", "false")],
    )
    add(
        "law26_4_acquisition_favorable_without_evidence", "LAW-26(4)-acquisition",
        "verified_without_evidence_reference", REVIEW,
        "EVIDENCE", "Acquisition is marked verified but has no evidence reference",
        [_set_op("evidence.acquisition", [])],
    )

    # --- Necessity / proportionality --------------------------------------
    add("necessity_favorable", "LAW-26(4)/IR-30(1)-necessity", "supported", PASS, None, None, [])
    add(
        "necessity_unresolved", "LAW-26(4)/IR-30(1)-necessity", "uncertain", REVIEW,
        "LAW-26(4)/IR-30(1)", "Necessity/proportionality requires review",
        [_set_op("use.necessity_status", "uncertain")],
    )
    add(
        "necessity_adverse", "LAW-26(4)/IR-30(1)-necessity", "unsupported", FAIL,
        "LAW-26(4)/IR-30(1)", "necessity is recorded as unsupported",
        [_set_op("use.necessity_status", "unsupported")],
    )

    # --- Copyright Law Article 37(1): normal exploitation ------------------
    art37_ne_marker_fail = "conflict with normal exploitation"
    add("art37_normal_exploitation_favorable", "LAW-37(1)-normal-exploitation", "no_conflict_with_basis", PASS, None, None, [])
    add(
        "art37_normal_exploitation_unresolved_uncertain", "LAW-37(1)-normal-exploitation", "uncertain", REVIEW,
        "LAW-37(1)", "Conflict with normal exploitation is unresolved",
        [_set_op("article37_context.normal_exploitation_conflict", "uncertain")],
    )
    add(
        "art37_normal_exploitation_unresolved_not_assessed", "LAW-37(1)-normal-exploitation", "not_assessed", REVIEW,
        "LAW-37(1)", "Conflict with normal exploitation is unresolved",
        [_set_op("article37_context.normal_exploitation_conflict", "not_assessed")],
    )
    add(
        "art37_normal_exploitation_favorable_without_basis", "LAW-37(1)-normal-exploitation",
        "no_conflict_without_basis", REVIEW,
        "LAW-37(1)", "No-conflict assessment under Article 37(1) has no recorded basis",
        [_set_op("article37_context.normal_exploitation_basis", [])],
    )
    add(
        "art37_normal_exploitation_adverse", "LAW-37(1)-normal-exploitation", "explicit_conflict", FAIL,
        "LAW-37(1)", art37_ne_marker_fail,
        [_set_op("article37_context.normal_exploitation_conflict", "conflict")],
    )
    add(
        "art37_normal_exploitation_adverse_with_favorable_ir30", "LAW-37(1)-normal-exploitation",
        "explicit_conflict_with_favorable_regulation_fields", FAIL,
        "LAW-37(1)", art37_ne_marker_fail,
        [
            _set_op("article37_context.normal_exploitation_conflict", "conflict"),
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "non_substantial"),
            _set_op("use.normal_exploitation_impact", "none"),
        ],
    )

    # --- Copyright Law Article 37(1): rightsholder legitimate interests ----
    art37_rh_marker_fail = "legitimate interests of rightsholders"
    add("art37_rightsholder_favorable", "LAW-37(1)-rightsholder-interests", "none_with_basis", PASS, None, None, [])
    add(
        "art37_rightsholder_unresolved_uncertain", "LAW-37(1)-rightsholder-interests", "uncertain", REVIEW,
        "LAW-37(1)", "Rightsholder legitimate-interests prejudice is unresolved",
        [_set_op("article37_context.rightsholder_legitimate_interests_prejudice", "uncertain")],
    )
    add(
        "art37_rightsholder_unresolved_not_assessed", "LAW-37(1)-rightsholder-interests", "not_assessed", REVIEW,
        "LAW-37(1)", "Rightsholder legitimate-interests prejudice is unresolved",
        [_set_op("article37_context.rightsholder_legitimate_interests_prejudice", "not_assessed")],
    )
    add(
        "art37_rightsholder_favorable_without_basis", "LAW-37(1)-rightsholder-interests",
        "none_without_basis", REVIEW,
        "LAW-37(1)", "Favorable rightsholder-interests assessment under Article 37(1) has no recorded basis",
        [_set_op("article37_context.rightsholder_interests_basis", [])],
    )
    add(
        "art37_rightsholder_adverse", "LAW-37(1)-rightsholder-interests", "explicit_unjustified_prejudice", FAIL,
        "LAW-37(1)", art37_rh_marker_fail,
        [_set_op("article37_context.rightsholder_legitimate_interests_prejudice", "unjustified")],
    )
    add(
        "art37_rightsholder_adverse_with_favorable_ir30_4", "LAW-37(1)-rightsholder-interests",
        "explicit_unjustified_prejudice_with_favorable_author_interest_fields", FAIL,
        "LAW-37(1)", art37_rh_marker_fail,
        [
            _set_op("article37_context.rightsholder_legitimate_interests_prejudice", "unjustified"),
            _set_op("rights_context.legitimate_interests_prejudice", "none"),
            _set_op("rights_context.exploitation_opportunity_effect", "none"),
        ],
    )

    # --- Implementing Regulations Article 30(1) ---------------------------
    add("ir30_1_favorable", "IR-30(1)-prohibited-uses", "no_prohibited_use", PASS, None, None, [])
    add(
        "ir30_1_adverse_republication", "IR-30(1)-prohibited-uses", "republication", FAIL,
        "IR-30(1)", "Record indicates republication",
        [_set_op("use.republication", True)],
    )
    add(
        "ir30_1_adverse_distribution", "IR-30(1)-prohibited-uses", "distribution", FAIL,
        "IR-30(1)", "Record indicates distribution",
        [_set_op("use.distribution", True)],
    )
    add(
        "ir30_1_adverse_direct_commercial", "IR-30(1)-prohibited-uses", "direct_commercial_exploitation", FAIL,
        "IR-30(1)", "Record indicates direct commercial exploitation",
        [_set_op("use.direct_commercial_exploitation", True)],
    )

    # --- Implementing Regulations Article 30(2) ---------------------------
    add(
        "ir30_2_favorable_non_substantial", "IR-30(2)-commercial-context",
        "commercial_but_non_substantial", PASS, None, None,
        [
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "non_substantial"),
            _set_op("use.normal_exploitation_impact", "uncertain"),
        ],
    )
    add(
        "ir30_2_favorable_no_impact", "IR-30(2)-commercial-context",
        "commercial_but_no_recorded_impact", PASS, None, None,
        [
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "uncertain"),
            _set_op("use.normal_exploitation_impact", "none"),
        ],
    )
    add(
        "ir30_2_unresolved", "IR-30(2)-commercial-context", "commercial_without_qualifying_condition", REVIEW,
        "IR-30(2)", "Purely commercial context lacks a clearly recorded qualifying condition",
        [
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "uncertain"),
            _set_op("use.normal_exploitation_impact", "uncertain"),
        ],
    )
    add(
        "ir30_2_adverse", "IR-30(2)-commercial-context", "substantial_and_adverse_impact", FAIL,
        "IR-30(2)", "Purely commercial use is substantial and recorded as adversely affecting normal exploitation",
        [
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "substantial"),
            _set_op("use.normal_exploitation_impact", "adverse"),
        ],
    )
    add(
        "ir30_2_adverse_with_favorable_art37", "IR-30(2)-commercial-context",
        "regulation_adverse_with_favorable_article37_fields", FAIL,
        "IR-30(2)", "Purely commercial use is substantial and recorded as adversely affecting normal exploitation",
        [
            _set_op("use.purely_commercial_context", True),
            _set_op("use.materiality_to_work", "substantial"),
            _set_op("use.normal_exploitation_impact", "adverse"),
            _set_op("article37_context.normal_exploitation_conflict", "no_conflict"),
        ],
    )

    # --- Implementing Regulations Article 30(3) ---------------------------
    add("ir30_3_favorable", "IR-30(3)-retained-record", "full_core_tuple", PASS, None, None, [])
    for field in ("type", "source"):
        add(
            "ir30_3_adverse_missing_work_{0}".format(field), "IR-30(3)-retained-record",
            "missing_work_{0}".format(field), FAIL,
            "IR-30(3)", "Missing core retained-record field: work.{0}".format(field),
            [_del_op("work.{0}".format(field))],
        )
    for field in ("purpose", "date"):
        add(
            "ir30_3_adverse_missing_use_{0}".format(field), "IR-30(3)-retained-record",
            "missing_use_{0}".format(field), FAIL,
            "IR-30(3)", "Missing core retained-record field: use.{0}".format(field),
            [_del_op("use.{0}".format(field))],
        )

    # --- Implementing Regulations Article 30(4) ---------------------------
    add("ir30_4_favorable", "IR-30(4)-author-interests", "no_prejudice_with_basis", PASS, None, None, [])
    add(
        "ir30_4_unresolved", "IR-30(4)-author-interests", "uncertain_assessment", REVIEW,
        "IR-30(4)", "Author-interest/market-effect assessment is incomplete or uncertain",
        [_set_op("rights_context.legitimate_interests_prejudice", "uncertain")],
    )
    add(
        "ir30_4_favorable_without_basis", "IR-30(4)-author-interests", "favorable_without_basis", REVIEW,
        "IR-30(4)", "Favorable author-interest/market-effect assessment has no recorded basis",
        [_set_op("rights_context.impact_assessment_basis", [])],
    )
    add(
        "ir30_4_adverse_prejudice", "IR-30(4)-author-interests", "unjustified_author_prejudice", FAIL,
        "IR-30(4)", "Record indicates prejudice or adverse exploitation-opportunity effect",
        [_set_op("rights_context.legitimate_interests_prejudice", "unjustified")],
    )
    add(
        "ir30_4_adverse_opportunity", "IR-30(4)-author-interests", "adverse_exploitation_opportunity", FAIL,
        "IR-30(4)", "Record indicates prejudice or adverse exploitation-opportunity effect",
        [_set_op("rights_context.exploitation_opportunity_effect", "adverse")],
    )
    add(
        "ir30_4_adverse_with_favorable_art37", "IR-30(4)-author-interests",
        "regulation_adverse_with_favorable_article37_fields", FAIL,
        "IR-30(4)", "Record indicates prejudice or adverse exploitation-opportunity effect",
        [
            _set_op("rights_context.legitimate_interests_prejudice", "unjustified"),
            _set_op("article37_context.rightsholder_legitimate_interests_prejudice", "none"),
        ],
    )

    # --- Implementing Regulations Article 30(5) ---------------------------
    add("ir30_5_favorable", "IR-30(5)-output-configuration", "no_protected_output_action", PASS, None, None, [])
    add(
        "ir30_5_favorable_transformed_with_permission", "IR-30(5)-output-configuration",
        "transformed_with_recorded_permission", PASS, None, None,
        [_set_op("output_context.transformed", True), _set_op("output_context.permission_status", "granted")],
    )
    add(
        "ir30_5_unresolved_inclusion", "IR-30(5)-output-configuration", "inclusion_necessity_uncertain", REVIEW,
        "IR-30(5)", "Final-product inclusion necessity is uncertain",
        [
            _set_op("output_context.included_in_final_product", True),
            _set_op("output_context.inclusion_necessary", "uncertain"),
        ],
    )
    add(
        "ir30_5_adverse_transformed", "IR-30(5)-output-configuration", "transformed_without_permission", FAIL,
        "IR-30(5)", "Output transformation/republication/public availability is recorded without permission",
        [_set_op("output_context.transformed", True), _set_op("output_context.permission_status", "not_granted")],
    )
    add(
        "ir30_5_adverse_made_public", "IR-30(5)-output-configuration", "made_public_without_permission", FAIL,
        "IR-30(5)", "Output transformation/republication/public availability is recorded without permission",
        [_set_op("output_context.made_public", True)],
    )
    add(
        "ir30_5_adverse_unnecessary_inclusion", "IR-30(5)-output-configuration",
        "unnecessary_final_product_inclusion", FAIL,
        "IR-30(5)", "Work is unnecessarily included in the final product",
        [
            _set_op("output_context.included_in_final_product", True),
            _set_op("output_context.inclusion_necessary", "no"),
        ],
    )

    # --- Implementing Regulations Article 30(6) ---------------------------
    add("ir30_6_favorable_none_identified", "IR-30(6)-independent-elements", "none_identified_with_basis", PASS, None, None, [])
    add(
        "ir30_6_favorable_assessed", "IR-30(6)-independent-elements", "assessed_with_basis", PASS, None, None,
        [_set_op("rights_context.independent_elements_status", "assessed")],
    )
    add(
        "ir30_6_unresolved_requires_review", "IR-30(6)-independent-elements", "requires_review", REVIEW,
        "IR-30(6)", "Independently protected elements are not fully assessed",
        [_set_op("rights_context.independent_elements_status", "requires_review")],
    )
    add(
        "ir30_6_unresolved_not_assessed", "IR-30(6)-independent-elements", "not_assessed", REVIEW,
        "IR-30(6)", "Independently protected elements are not fully assessed",
        [_set_op("rights_context.independent_elements_status", "not_assessed")],
    )
    add(
        "ir30_6_favorable_without_basis", "IR-30(6)-independent-elements", "assessed_without_basis", REVIEW,
        "IR-30(6)", "Independent-elements assessment has no recorded basis",
        [
            _set_op("rights_context.independent_elements_status", "assessed"),
            _set_op("rights_context.independent_elements_basis", []),
        ],
    )

    # --- Evidence references ----------------------------------------------
    add("evidence_favorable", "EVIDENCE-references", "all_evidence_present", PASS, None, None, [])
    add(
        "evidence_unresolved_missing_use_event", "EVIDENCE-references", "missing_use_event_reference", REVIEW,
        "EVIDENCE", "No use-event evidence reference is recorded",
        [_set_op("evidence.use_event", [])],
    )

    # --- Profile integrity -------------------------------------------------
    add("profile_favorable", "PROFILE-0.2.0-integrity", "supported_version_with_article37_context", PASS, None, None, [])
    add(
        "profile_adverse_missing_article37_context", "PROFILE-0.2.0-integrity", "article37_context_omitted", FAIL,
        "IPEL-CONTRACT", "Missing/invalid object: article37_context",
        [_del_op("article37_context")],
    )
    add(
        "profile_adverse_unsupported_version", "PROFILE-0.2.0-integrity", "unsupported_record_version", FAIL,
        "IPEL-CONTRACT", "Unsupported record_version",
        [_set_op("record_version", "0.3.0")],
    )

    return cases


def build_condition_benchmark(base: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate every preregistered condition x state case on profile 0.2.0."""
    rows: List[Dict[str, Any]] = []
    for case in _cases():
        record = apply_mutations(base, case["mutations"])
        result = evaluate(record)
        findings = [
            {"rule": f.rule, "severity": f.severity, "message": f.message} for f in result.findings
        ]
        rule_id = case["expected_rule_id"]
        marker = case["expected_message_marker"]
        if rule_id is None:
            # A favorable/evidence-ready state must produce no finding at all.
            expected_finding_present = not findings
        else:
            severity = SEVERITY_BY_OUTCOME[case["expected_outcome"]]
            expected_finding_present = any(
                item["rule"] == rule_id and item["severity"] == severity and marker in item["message"]
                for item in findings
            )
        rows.append(
            {
                "case_id": case["case_id"],
                "condition_id": case["condition_id"],
                "variant": case["variant"],
                "expected_state": case["expected_state"],
                "expected_outcome": case["expected_outcome"],
                "observed_outcome": result.outcome,
                "outcome_matches_expectation": result.outcome == case["expected_outcome"],
                "expected_rule_id": rule_id,
                "expected_message_marker": marker,
                "expected_finding_present": expected_finding_present,
                "legal_profile_id": result.legal_profile_id,
                "declared_scope_complete": result.declared_scope_complete,
                "legal_conclusion": result.to_dict()["legal_conclusion"],
                "mutations": case["mutations"],
                "findings": findings,
                "rule_ids": sorted({item["rule"] for item in findings}),
            }
        )

    coverage = []
    for condition in CONDITIONS:
        matching = [row for row in rows if row["condition_id"] == condition["condition_id"]]
        observed_states = sorted({row["expected_state"] for row in matching})
        entry = {
            "condition_id": condition["condition_id"],
            "legal_source": condition["legal_source"],
            "description": condition["description"],
            "case_count": len(matching),
            "observed_states": observed_states,
            "favorable_state_covered": FAVORABLE in observed_states,
            "unresolved_state_covered": UNRESOLVED in observed_states,
            "adverse_state_covered": ADVERSE in observed_states,
            "adverse_state_available_in_profile": condition["adverse_state_available"],
            "unresolved_state_available_in_profile": condition["unresolved_state_available"],
        }
        if "state_absence_note" in condition:
            entry["state_absence_note"] = condition["state_absence_note"]
        coverage.append(entry)

    return {
        "benchmark_version": BENCHMARK_VERSION,
        "record_profile_version": CURRENT_RECORD_VERSION,
        "expected_legal_profile_id": CURRENT_PROFILE_ID,
        "case_count": len(rows),
        "all_outcomes_match_expectation": all(row["outcome_matches_expectation"] for row in rows),
        "all_expected_findings_present": all(row["expected_finding_present"] for row in rows),
        "state_counts": {
            FAVORABLE: sum(1 for row in rows if row["expected_state"] == FAVORABLE),
            UNRESOLVED: sum(1 for row in rows if row["expected_state"] == UNRESOLVED),
            ADVERSE: sum(1 for row in rows if row["expected_state"] == ADVERSE),
        },
        "condition_coverage": coverage,
        "cases": rows,
    }


# --------------------------------------------------------------------------
# controlled delegation round-trips (measured evidence for the frozen rubric)
# --------------------------------------------------------------------------

def _date_part(value: Any) -> Optional[str]:
    if not isinstance(value, str) or "T" not in value:
        return None
    return value.split("T")[0]


def _action_when(record: Dict[str, Any]) -> Optional[str]:
    date = _get(record, "use.date")
    if not isinstance(date, str) or not date.strip():
        return None
    return date + SYNTHETIC_ACTION_TIME_OF_DAY


def _signed_time(record: Dict[str, Any]) -> Optional[str]:
    date = _get(record, "use.date")
    if not isinstance(date, str) or not date.strip():
        return None
    try:
        parsed = datetime.date(*(int(part) for part in date.split("-")))
    except (TypeError, ValueError):
        return None
    shifted = parsed + datetime.timedelta(days=SYNTHETIC_TIMESTAMP_OFFSET_DAYS)
    return shifted.isoformat() + "T00:00:00Z"


CANDIDATE_ROUNDTRIPS: Dict[str, Dict[str, Any]] = {
    "work-title__c2pa-dc-title": {
        "ipel_path": "work.title",
        "generic_target": "c2pa.ingredient.dc:title",
        "encode": lambda record: _get(record, "work.title"),
        "decode": lambda generic: generic,
        "inference_required": False,
        "bridging_assumption": None,
    },
    "work-type__c2pa-dc-format": {
        "ipel_path": "work.type",
        "generic_target": "c2pa.ingredient.dc:format",
        "encode": lambda record: SYNTHETIC_FORMAT,
        "decode": lambda generic: generic,
        "inference_required": True,
        "bridging_assumption": "the IANA media type of the byte stream is the legal category of the work",
    },
    "work-type__c2pa-dataTypes": {
        "ipel_path": "work.type",
        "generic_target": "c2pa.ingredient.dataTypes",
        "encode": lambda record: [SYNTHETIC_DATA_TYPE],
        "decode": lambda generic: generic[0] if isinstance(generic, list) and generic else None,
        "inference_required": True,
        "bridging_assumption": "the provenance data-type classification is the legal category of the work",
    },
    "work-source__c2pa-informationalURI": {
        "ipel_path": "work.source",
        "generic_target": "c2pa.ingredient.informationalURI",
        "encode": lambda record: SYNTHETIC_INFORMATIONAL_URI,
        "decode": lambda generic: generic,
        "inference_required": True,
        "bridging_assumption": "an informational page about the ingredient is the source the copy was obtained from",
    },
    "work-source__c2pa-data-reference": {
        "ipel_path": "work.source",
        "generic_target": "c2pa.ingredient.data",
        "encode": lambda record: {
            "url": SYNTHETIC_DATA_REFERENCE_URL,
            "alg": "sha256",
            "hash": _get(record, "work.sha256"),
        },
        "decode": lambda generic: generic.get("url") if isinstance(generic, dict) else None,
        "inference_required": True,
        "bridging_assumption": "a hashed reference to a data box in the manifest store is the acquisition source",
    },
    "use-purpose__c2pa-inputTo": {
        "ipel_path": "use.purpose",
        "generic_target": "c2pa.ingredient.relationship",
        "encode": lambda record: "inputTo",
        "decode": lambda generic: generic,
        "inference_required": True,
        "bridging_assumption": "being an input to a computational process states the declared purpose of the use",
    },
    "use-purpose__cawg-training-mining": {
        "ipel_path": "use.purpose",
        "generic_target": "cawg.training-mining.entries.{0}.use".format(SYNTHETIC_TDM_KEY),
        "encode": lambda record: "allowed",
        "decode": lambda generic: generic,
        "inference_required": True,
        "bridging_assumption": "a rightsholder usage declaration states the developer's actual purpose of use",
    },
    "use-date__c2pa-action-when": {
        "ipel_path": "use.date",
        "generic_target": "c2pa.actions[0].when",
        "encode": _action_when,
        "decode": _date_part,
        "inference_required": True,
        "bridging_assumption": "the timestamped C2PA action is the legally relevant use event",
    },
    "use-date__c2pa-trusted-timestamp": {
        "ipel_path": "use.date",
        "generic_target": "c2pa.claim_signature.rfc3161_timestamp",
        "encode": lambda record: {"rfc3161": True, "signed_time": _signed_time(record)},
        "decode": lambda generic: _date_part(generic.get("signed_time")) if isinstance(generic, dict) else None,
        "inference_required": True,
        "bridging_assumption": "the countersigned claim time is the date the work was used",
    },
}


def delegation_roundtrip(record: Dict[str, Any], candidate_id: str) -> Dict[str, Any]:
    """Substitute one IPEL leaf with its candidate generic semantic and read it back.

    The harness measures three separable observables: whether the IPEL value is
    recovered byte-identically, whether the evidence gate can still detect the
    difference, and whether recovery needs a declared bridging assumption. Under
    the frozen rubric a round-trip passes only when the value survives, the gate
    outcome survives, and no bridging assumption is needed.
    """
    spec = CANDIDATE_ROUNDTRIPS[candidate_id]
    path = spec["ipel_path"]
    source_value = _get(record, path)
    generic_value = spec["encode"](record)
    recovered = spec["decode"](generic_value)

    reconstructed = copy.deepcopy(record)
    if recovered is None:
        _delete(reconstructed, path)
    else:
        _set(reconstructed, path, recovered)

    original_gate = evaluate(record).outcome
    reconstructed_gate = evaluate(reconstructed).outcome
    value_preserved = recovered == source_value
    gate_preserved = original_gate == reconstructed_gate
    inference_required = bool(spec["inference_required"])
    return {
        "candidate_id": candidate_id,
        "ipel_path": path,
        "generic_target": spec["generic_target"],
        "source_value": source_value,
        "generic_value": generic_value,
        "recovered_value": recovered,
        "value_preserved": value_preserved,
        "original_gate_outcome": original_gate,
        "reconstructed_gate_outcome": reconstructed_gate,
        "gate_preserved": gate_preserved,
        "inference_required": inference_required,
        "bridging_assumption": spec["bridging_assumption"],
        "gate_silent_semantic_corruption": (not value_preserved) and gate_preserved,
        "roundtrip_pass": value_preserved and gate_preserved and not inference_required,
    }


def run_delegation_roundtrips(record: Dict[str, Any]) -> Dict[str, Any]:
    rows = [delegation_roundtrip(record, candidate_id) for candidate_id in sorted(CANDIDATE_ROUNDTRIPS)]
    return {
        "benchmark_version": BENCHMARK_VERSION,
        "record_profile_version": _get(record, "record_version"),
        "synthetic_provenance_values_are_fixtures": True,
        "executed_candidate_count": len(rows),
        "roundtrip_pass_count": sum(1 for row in rows if row["roundtrip_pass"]),
        "gate_silent_semantic_corruption_count": sum(1 for row in rows if row["gate_silent_semantic_corruption"]),
        "value_preserved_count": sum(1 for row in rows if row["value_preserved"]),
        "inference_required_count": sum(1 for row in rows if row["inference_required"]),
        "roundtrips": rows,
    }


# --------------------------------------------------------------------------
# rubric application (frozen Stage 013 rubric v1.0.0)
# --------------------------------------------------------------------------

def apply_rubric(
    rubric: Dict[str, Any],
    registry: Dict[str, Any],
    assessments: Dict[str, Any],
    roundtrip_index: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Classify every frozen candidate with the locked rubric.

    Declared round-trip outcomes are cross-checked against the measured harness
    result. A mismatch is reported and forced to fail closed rather than being
    silently reconciled.
    """
    if assessments.get("rubric_version") != rubric["rubric_version"]:
        raise ValueError("assessment file targets a different rubric version")
    by_id = {item["candidate_id"]: item for item in assessments["assessments"]}
    registry_ids = [candidate["candidate_id"] for candidate in registry["candidates"]]
    if sorted(by_id) != sorted(registry_ids):
        raise ValueError("assessment set does not match the frozen candidate registry")

    rows: List[Dict[str, Any]] = []
    for candidate in registry["candidates"]:
        candidate_id = candidate["candidate_id"]
        assessment = by_id[candidate_id]
        measured = roundtrip_index.get(candidate_id)
        declared_pass = assessment.get("roundtrip_pass")
        if measured is None:
            consistent = assessment.get("roundtrip_tested") is False and declared_pass is None
            measured_pass = None
        else:
            measured_pass = measured["roundtrip_pass"]
            consistent = assessment.get("roundtrip_tested") is True and declared_pass == measured_pass
        if not consistent:
            raise ValueError(
                "declared round-trip state for {0} does not match the measured harness result".format(candidate_id)
            )
        classification = classify_assessment(assessment, rubric, candidate)
        dims = assessment.get("dimension_assessments") or {}
        rows.append(
            {
                "candidate_id": candidate_id,
                "ipel_path": candidate["ipel_path"],
                "candidate_kind": candidate["candidate_kind"],
                "candidate_semantic": candidate["candidate_semantic"],
                "candidate_standard": candidate["candidate_standard"],
                "candidate_version": candidate["candidate_version"],
                "proposition_class": candidate["proposition_class"],
                "decision": classification["decision"],
                "ipel_field_retained": classification["ipel_field_retained"],
                "reasons": classification["reasons"],
                "failed_dimensions": sorted(k for k, v in dims.items() if v["status"] == "FAIL"),
                "not_applicable_dimensions": sorted(k for k, v in dims.items() if v["status"] == "NOT_APPLICABLE"),
                "inference_dependencies": list(assessment["inference_dependencies"]),
                "roundtrip_tested": assessment["roundtrip_tested"],
                "roundtrip_pass_declared": declared_pass,
                "roundtrip_pass_measured": measured_pass,
                "roundtrip_declaration_matches_measurement": True,
                "assessment_notes": assessment["assessment_notes"],
            }
        )

    decisions = [row["decision"] for row in rows]
    safe_ids = sorted(row["candidate_id"] for row in rows if row["decision"] == "SAFE_DELEGATION")
    safe_paths = sorted({row["ipel_path"] for row in rows if row["decision"] == "SAFE_DELEGATION"})
    ir30_3_paths = ["work.type", "work.source", "use.purpose", "use.date"]
    art37_paths = [
        "article37_context.normal_exploitation_conflict",
        "article37_context.rightsholder_legitimate_interests_prejudice",
    ]
    return {
        "rubric_version": rubric["rubric_version"],
        "registry_version": registry["registry_version"],
        "candidate_count": len(rows),
        "decision_counts": {
            decision: decisions.count(decision)
            for decision in ("SAFE_DELEGATION", "PARTIAL_SUPPORT", "NOT_SAFE_TO_DELEGATE", "NO_CANDIDATE")
        },
        "safe_delegation_candidate_ids": safe_ids,
        "safe_delegation_ipel_paths": safe_paths,
        "ipel_fields_retained_count": sum(1 for row in rows if row["ipel_field_retained"]),
        "article_30_3_core_fields": ir30_3_paths,
        "article_30_3_fields_safely_delegable": sorted(set(safe_paths) & set(ir30_3_paths)),
        "article_30_3_safe_delegation_ratio": "{0}/{1}".format(
            len(set(safe_paths) & set(ir30_3_paths)), len(ir30_3_paths)
        ),
        "article_37_propositions": art37_paths,
        "article_37_fields_safely_delegable": sorted(set(safe_paths) & set(art37_paths)),
        "article_37_safe_delegation_ratio": "{0}/{1}".format(
            len(set(safe_paths) & set(art37_paths)), len(art37_paths)
        ),
        "assessments": rows,
    }


# --------------------------------------------------------------------------
# naive provenance-mapping baseline
# --------------------------------------------------------------------------

NAIVE_DELEGATED_PATHS = {
    "work.title": "c2pa.ingredient.dc:title",
    "work.type": "c2pa.ingredient.dc:format",
    "work.source": "c2pa.ingredient.informationalURI",
    "use.purpose": "c2pa.ingredient.relationship",
    "use.date": "c2pa.actions[0].when",
}

NAIVE_INFERRED_PATHS = {
    "work.publication_status": "manifest validation state and signer trust state",
    "work.acquisition_status": "CAWG training/mining usage declaration",
    "use.necessity_status": "CAWG training/mining usage declaration",
    "article37_context.normal_exploitation_conflict": "CAWG training/mining usage declaration",
    "article37_context.rightsholder_legitimate_interests_prejudice": "CAWG training/mining usage declaration",
    "article37_context.normal_exploitation_basis": "CAWG training/mining usage declaration",
    "article37_context.rightsholder_interests_basis": "CAWG training/mining usage declaration",
    "rights_context.legitimate_interests_prejudice": "CAWG training/mining usage declaration",
    "rights_context.exploitation_opportunity_effect": "CAWG training/mining usage declaration",
    "rights_context.impact_assessment_basis": "CAWG training/mining usage declaration",
    "evidence.publication": "presence of a valid provenance manifest",
    "evidence.acquisition": "presence of a valid provenance manifest",
    "evidence.use_event": "presence of a valid provenance manifest",
}

NAIVE_BASELINE_DESCRIPTION = (
    "The naive provenance-mapping baseline is the comparator an engineer would build from field-name "
    "similarity alone: every IPEL leaf with a superficially similar C2PA/CAWG semantic is delegated to "
    "that semantic, and every remaining legally operative proposition is inferred from provenance "
    "signals (manifest validity, signer trust, and the CAWG training/mining declaration). Fields with "
    "no provenance analogue are retained unchanged. The baseline is defined before outcomes are read "
    "and is never presented as an IPEL result."
)


def naive_provenance_view(record: Dict[str, Any], signals: Dict[str, str]) -> Dict[str, Any]:
    return {
        "c2pa": {
            "spec_version": "2.4",
            "representation": "aligned-intermediate-not-a-manifest",
            "manifest_ref": SYNTHETIC_MANIFEST_REF,
            "ingredient": {
                "relationship": "inputTo",
                "dc:title": _get(record, "work.title"),
                "dc:format": SYNTHETIC_FORMAT,
                "dataTypes": [SYNTHETIC_DATA_TYPE],
                "informationalURI": SYNTHETIC_INFORMATIONAL_URI,
                "data": {"url": SYNTHETIC_DATA_REFERENCE_URL, "alg": "sha256", "hash": _get(record, "work.sha256")},
            },
            "actions": [{"action": SYNTHETIC_ACTION, "when": _action_when(record)}],
            "validation_signals": {
                "manifest_state": signals["manifest_state"],
                "trust_state": signals["trust_state"],
            },
        },
        "cawg": {
            "tdm_assertion": {
                "label": "cawg.training-mining",
                "version": "1.1",
                "entries": {SYNTHETIC_TDM_KEY: {"use": signals["tdm_use"]}},
            }
        },
    }


def naive_reconstruct(record: Dict[str, Any], signals: Dict[str, str]) -> Dict[str, Any]:
    view = naive_provenance_view(record, signals)
    ingredient = view["c2pa"]["ingredient"]
    out = copy.deepcopy(record)

    decoded = {
        "work.title": ingredient.get("dc:title"),
        "work.type": ingredient.get("dc:format"),
        "work.source": ingredient.get("informationalURI"),
        "use.purpose": ingredient.get("relationship"),
        "use.date": _date_part(view["c2pa"]["actions"][0].get("when")),
    }
    for path, value in decoded.items():
        if value is None:
            _delete(out, path)
        else:
            _set(out, path, value)

    manifest_ok = signals["manifest_state"] == "valid" and signals["trust_state"] == "trusted"
    tdm_allowed = signals["tdm_use"] == "allowed"
    manifest_evidence = "c2pa://manifest/{0}".format(SYNTHETIC_MANIFEST_REF)

    _set(out, "work.publication_status", "verified" if manifest_ok else "unverified")
    _set(out, "work.acquisition_status", "verified" if tdm_allowed else "unverified")
    _set(out, "use.necessity_status", "supported" if tdm_allowed else "uncertain")
    _set(out, "article37_context.normal_exploitation_conflict", "no_conflict" if tdm_allowed else "uncertain")
    _set(
        out,
        "article37_context.rightsholder_legitimate_interests_prejudice",
        "none" if tdm_allowed else "uncertain",
    )
    _set(out, "article37_context.normal_exploitation_basis", [manifest_evidence] if tdm_allowed else [])
    _set(out, "article37_context.rightsholder_interests_basis", [manifest_evidence] if tdm_allowed else [])
    _set(out, "rights_context.legitimate_interests_prejudice", "none" if tdm_allowed else "uncertain")
    _set(out, "rights_context.exploitation_opportunity_effect", "none" if tdm_allowed else "uncertain")
    _set(out, "rights_context.impact_assessment_basis", [manifest_evidence] if tdm_allowed else [])
    for key in ("publication", "acquisition", "use_event"):
        _set(out, "evidence." + key, [manifest_evidence] if manifest_ok else [])
    return out


def rubric_governed_reconstruct(record: Dict[str, Any], safe_candidate_ids: List[str]) -> Dict[str, Any]:
    """Delegate only the candidates the frozen rubric classified SAFE_DELEGATION.

    Every other IPEL leaf is retained, and no legally operative proposition is
    inferred from a provenance signal.
    """
    out = copy.deepcopy(record)
    for candidate_id in safe_candidate_ids:
        spec = CANDIDATE_ROUNDTRIPS[candidate_id]
        generic_value = spec["encode"](record)
        recovered = spec["decode"](generic_value)
        if recovered is None:
            _delete(out, spec["ipel_path"])
        else:
            _set(out, spec["ipel_path"], recovered)
    return out


def compare_against_naive_baseline(
    base: Dict[str, Any], benchmark: Dict[str, Any], safe_candidate_ids: List[str]
) -> Dict[str, Any]:
    per_profile: Dict[str, Any] = {}
    for profile_name in sorted(PROVENANCE_SIGNAL_PROFILES):
        signals = PROVENANCE_SIGNAL_PROFILES[profile_name]
        rows: List[Dict[str, Any]] = []
        for case in benchmark["cases"]:
            record = apply_mutations(base, case["mutations"])
            true_outcome = case["observed_outcome"]
            naive = naive_reconstruct(record, signals)
            governed = rubric_governed_reconstruct(record, safe_candidate_ids)
            naive_outcome = evaluate(naive).outcome
            governed_outcome = evaluate(governed).outcome
            naive_severity = OUTCOME_SEVERITY[naive_outcome]
            true_severity = OUTCOME_SEVERITY[true_outcome]
            rows.append(
                {
                    "case_id": case["case_id"],
                    "condition_id": case["condition_id"],
                    "true_outcome": true_outcome,
                    "naive_outcome": naive_outcome,
                    "rubric_governed_outcome": governed_outcome,
                    "naive_outcome_preserved": naive_outcome == true_outcome,
                    "rubric_governed_outcome_preserved": governed_outcome == true_outcome,
                    "naive_false_equivalence": true_severity > 0 and naive_severity < true_severity,
                    "naive_spurious_escalation": naive_severity > true_severity,
                    "naive_semantic_loss_path_count": len(semantic_loss(record, naive)),
                    "rubric_governed_semantic_loss_path_count": len(semantic_loss(record, governed)),
                }
            )
        per_profile[profile_name] = {
            "provenance_signals": signals,
            "case_count": len(rows),
            "naive_outcome_preserved_count": sum(1 for row in rows if row["naive_outcome_preserved"]),
            "rubric_governed_outcome_preserved_count": sum(
                1 for row in rows if row["rubric_governed_outcome_preserved"]
            ),
            "naive_false_equivalence_count": sum(1 for row in rows if row["naive_false_equivalence"]),
            "naive_false_equivalence_case_ids": sorted(
                row["case_id"] for row in rows if row["naive_false_equivalence"]
            ),
            "naive_spurious_escalation_count": sum(1 for row in rows if row["naive_spurious_escalation"]),
            "naive_total_semantic_loss_paths": sum(row["naive_semantic_loss_path_count"] for row in rows),
            "rubric_governed_total_semantic_loss_paths": sum(
                row["rubric_governed_semantic_loss_path_count"] for row in rows
            ),
            "cases": rows,
        }

    favorable = per_profile["favorable_provenance"]
    unknown = per_profile["unknown_provenance"]
    unstable = sorted(
        {
            row["case_id"]
            for row in favorable["cases"]
            for other in unknown["cases"]
            if other["case_id"] == row["case_id"] and other["naive_outcome"] != row["naive_outcome"]
        }
    )
    return {
        "benchmark_version": BENCHMARK_VERSION,
        "baseline_description": NAIVE_BASELINE_DESCRIPTION,
        "naive_delegated_paths": NAIVE_DELEGATED_PATHS,
        "naive_delegated_path_count": len(NAIVE_DELEGATED_PATHS),
        "naive_inferred_paths": NAIVE_INFERRED_PATHS,
        "naive_inferred_path_count": len(NAIVE_INFERRED_PATHS),
        "rubric_governed_delegated_candidate_ids": sorted(safe_candidate_ids),
        "rubric_governed_delegated_path_count": len(
            {CANDIDATE_ROUNDTRIPS[cid]["ipel_path"] for cid in safe_candidate_ids}
        ),
        "rubric_governed_inferred_path_count": 0,
        "delegation_difference": len(NAIVE_DELEGATED_PATHS)
        - len({CANDIDATE_ROUNDTRIPS[cid]["ipel_path"] for cid in safe_candidate_ids}),
        "naive_outcome_unstable_across_provenance_signal_case_ids": unstable,
        "naive_outcome_unstable_across_provenance_signal_count": len(unstable),
        "rubric_governed_outcome_invariant_to_provenance_signals": True,
        "signal_profiles": per_profile,
    }


# --------------------------------------------------------------------------
# corrected-profile mapping / round-trip coverage
# --------------------------------------------------------------------------

def article37_tuple(record: Dict[str, Any]) -> Tuple[Any, Any, Any, Any]:
    return (
        _get(record, "article37_context.normal_exploitation_conflict"),
        _get(record, "article37_context.rightsholder_legitimate_interests_prejudice"),
        _get(record, "article37_context.normal_exploitation_basis"),
        _get(record, "article37_context.rightsholder_interests_basis"),
    )


def corrected_profile_roundtrip(base: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
    """Rerun the Stage-003-style mapping/round-trip check on profile 0.2.0.

    This replaces only the part of the legacy Stage 003 evidence that was
    generated under profile 0.1.0. The historical 0.1.0 artifacts are left in
    place and are not re-derived here.
    """
    rows: List[Dict[str, Any]] = []
    for case in benchmark["cases"]:
        record = apply_mutations(base, case["mutations"])
        row: Dict[str, Any] = {
            "case_id": case["case_id"],
            "condition_id": case["condition_id"],
            "gate_outcome": case["observed_outcome"],
        }
        try:
            profile = to_profile(record, manifest_ref=SYNTHETIC_MANIFEST_REF)
        except ProfileError as error:
            row.update(
                {
                    "profile_constructed": False,
                    "profile_construction_error": str(error),
                    "fails_closed": True,
                }
            )
            rows.append(row)
            continue
        metrics = roundtrip_metrics(record, profile)
        rebuilt = from_profile(profile)
        row.update(
            {
                "profile_constructed": True,
                "profile_construction_error": None,
                "fails_closed": False,
                "original_gate": metrics.original_gate,
                "reconstructed_gate": metrics.reconstructed_gate,
                "gate_preserved": metrics.gate_preserved,
                "article_30_3_preserved": metrics.article_30_3_preserved,
                "article_37_preserved": article37_tuple(record) == article37_tuple(rebuilt),
                "semantic_loss_count": metrics.semantic_loss_count,
                "duplicate_generic_field_count": metrics.duplicate_generic_field_count,
                "mapped_generic_field_count": metrics.mapped_generic_field_count,
            }
        )
        rows.append(row)

    constructed = [row for row in rows if row["profile_constructed"]]
    failed = [row for row in rows if not row["profile_constructed"]]
    return {
        "benchmark_version": BENCHMARK_VERSION,
        "record_profile_version": CURRENT_RECORD_VERSION,
        "supersedes_legacy_stage003_evidence_for": "record profile 0.2.0 only",
        "legacy_stage003_artifacts_preserved": True,
        "case_count": len(rows),
        "profile_constructed_count": len(constructed),
        "profile_failed_closed_count": len(failed),
        "profile_failed_closed_case_ids": sorted(row["case_id"] for row in failed),
        "all_constructed_gate_outcomes_preserved": all(row["gate_preserved"] for row in constructed),
        "all_constructed_article_30_3_tuples_preserved": all(
            row["article_30_3_preserved"] for row in constructed
        ),
        "all_constructed_article_37_tuples_preserved": all(
            row["article_37_preserved"] for row in constructed
        ),
        "all_constructed_roundtrips_zero_semantic_loss": all(
            row["semantic_loss_count"] == 0 for row in constructed
        ),
        "cases": rows,
    }
