"""Preregistered semantic-equivalence classifier for Stage 013.

This module freezes the decision logic used later to decide whether a generic
C2PA/CAWG semantic can replace an IPEL jurisdiction-specific field. It does not
contain or generate candidate outcomes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SAFE = "SAFE_DELEGATION"
PARTIAL = "PARTIAL_SUPPORT"
NOT_SAFE = "NOT_SAFE_TO_DELEGATE"
NO_CANDIDATE = "NO_CANDIDATE"

PROHIBITED_INFERENCE = {"VALIDATION_STATE", "SIGNER_TRUST", "RIGHTS_PREFERENCE", "LEGAL_CONCLUSION"}
NORMATIVE_KINDS = {"NORMATIVE_FIELD", "NORMATIVE_ASSERTION"}


class SemanticEquivalenceError(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dimension_map(rubric: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in rubric["dimensions"]}


def validate_assessment(assessment: dict[str, Any], rubric: dict[str, Any], candidate: dict[str, Any]) -> None:
    if assessment.get("rubric_version") != rubric.get("rubric_version"):
        raise SemanticEquivalenceError("rubric_version mismatch")
    if assessment.get("candidate_id") != candidate.get("candidate_id"):
        raise SemanticEquivalenceError("candidate_id mismatch")
    if assessment.get("proposition_class") != candidate.get("proposition_class"):
        raise SemanticEquivalenceError("proposition_class mismatch")
    if assessment.get("candidate_kind") != candidate.get("candidate_kind"):
        raise SemanticEquivalenceError("candidate_kind mismatch")

    kind = candidate["candidate_kind"]
    dims = assessment.get("dimension_assessments")
    if not isinstance(dims, dict):
        raise SemanticEquivalenceError("dimension_assessments must be an object")

    if kind == "NO_CANDIDATE":
        if dims:
            raise SemanticEquivalenceError("NO_CANDIDATE must not fabricate dimension assessments")
        if assessment.get("roundtrip_tested") is not False or assessment.get("roundtrip_pass") is not None:
            raise SemanticEquivalenceError("NO_CANDIDATE cannot claim a roundtrip")
        if assessment.get("support_relevance") is not False:
            raise SemanticEquivalenceError("NO_CANDIDATE cannot claim support relevance")
        if assessment.get("inference_dependencies") not in ([], tuple()):
            raise SemanticEquivalenceError("NO_CANDIDATE cannot rely on inference dependencies")
        return

    required_dims = _dimension_map(rubric)
    if set(dims) != set(required_dims):
        missing = sorted(set(required_dims) - set(dims))
        extra = sorted(set(dims) - set(required_dims))
        raise SemanticEquivalenceError(f"dimension set mismatch: missing={missing}, extra={extra}")

    prop_class = assessment["proposition_class"]
    allowed_na = set(rubric["proposition_classes"][prop_class]["not_applicable_allowed"])
    allowed_status = set(rubric["dimension_statuses"])
    for dim_id, item in dims.items():
        if not isinstance(item, dict):
            raise SemanticEquivalenceError(f"dimension {dim_id} must be an object")
        status = item.get("status")
        if status not in allowed_status:
            raise SemanticEquivalenceError(f"invalid status for {dim_id}: {status!r}")
        if status == "NOT_APPLICABLE" and dim_id not in allowed_na:
            raise SemanticEquivalenceError(f"NOT_APPLICABLE is not preregistered for {dim_id} / {prop_class}")
        if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
            raise SemanticEquivalenceError(f"missing rationale for {dim_id}")
        refs = item.get("evidence_refs")
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
            raise SemanticEquivalenceError(f"invalid evidence_refs for {dim_id}")

    if not isinstance(assessment.get("roundtrip_tested"), bool):
        raise SemanticEquivalenceError("roundtrip_tested must be boolean")
    roundtrip_pass = assessment.get("roundtrip_pass")
    if assessment["roundtrip_tested"] and not isinstance(roundtrip_pass, bool):
        raise SemanticEquivalenceError("tested roundtrip requires boolean roundtrip_pass")
    if not assessment["roundtrip_tested"] and roundtrip_pass is not None:
        raise SemanticEquivalenceError("untested roundtrip requires null roundtrip_pass")
    if not isinstance(assessment.get("support_relevance"), bool):
        raise SemanticEquivalenceError("support_relevance must be boolean")
    deps = assessment.get("inference_dependencies")
    if not isinstance(deps, list) or len(deps) != len(set(deps)):
        raise SemanticEquivalenceError("inference_dependencies must be a unique list")
    if not isinstance(assessment.get("assessment_notes"), str) or not assessment["assessment_notes"].strip():
        raise SemanticEquivalenceError("assessment_notes required")


def classify_assessment(assessment: dict[str, Any], rubric: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return a fail-closed delegation class and explicit reasons."""
    validate_assessment(assessment, rubric, candidate)
    kind = candidate["candidate_kind"]
    if kind == "NO_CANDIDATE":
        return {"decision": NO_CANDIDATE, "ipel_field_retained": True, "reasons": ["no normative generic candidate registered"]}

    dims = assessment["dimension_assessments"]
    dim_defs = _dimension_map(rubric)
    applicable = {k: v for k, v in dims.items() if v["status"] != "NOT_APPLICABLE"}
    failures = [k for k, v in applicable.items() if v["status"] == "FAIL"]
    critical_failures = [k for k in failures if dim_defs[k]["critical"]]
    prohibited_deps = sorted(set(assessment["inference_dependencies"]) & PROHIBITED_INFERENCE)
    all_applicable_pass = all(v["status"] == "PASS" for v in applicable.values())
    normative_kind = kind in NORMATIVE_KINDS
    roundtrip_ok = assessment["roundtrip_tested"] and assessment["roundtrip_pass"] is True
    custom_block = kind == "CUSTOM_ASSERTION"

    safe = all_applicable_pass and not critical_failures and not prohibited_deps and normative_kind and roundtrip_ok and not custom_block
    if safe:
        return {"decision": SAFE, "ipel_field_retained": False, "reasons": ["all preregistered applicable dimensions passed and controlled roundtrip passed"]}

    reasons: list[str] = []
    if critical_failures:
        reasons.append("critical_failures=" + ",".join(sorted(critical_failures)))
    if failures and not critical_failures:
        reasons.append("noncritical_failures=" + ",".join(sorted(failures)))
    if prohibited_deps:
        reasons.append("prohibited_inference_dependencies=" + ",".join(prohibited_deps))
    if not normative_kind:
        reasons.append("candidate is not a maintained normative generic semantic")
    if not roundtrip_ok:
        reasons.append("controlled roundtrip not passed")
    if custom_block:
        reasons.append("custom assertion cannot establish generic-standard equivalence")

    if assessment["support_relevance"]:
        return {"decision": PARTIAL, "ipel_field_retained": True, "reasons": reasons or ["support only"]}
    return {"decision": NOT_SAFE, "ipel_field_retained": True, "reasons": reasons or ["safe-delegation criteria not met"]}
