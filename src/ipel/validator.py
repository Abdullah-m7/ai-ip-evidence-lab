"""Deterministic IPEL evidence gate.

The gate evaluates evidence readiness and encoded contradictions. It does not
produce legal advice or a legal conclusion of copyright compliance.

Record profile 0.1.0 is retained as a historical/legacy profile so Stages
001-005 remain reproducible. Record profile 0.2.0 adds the cross-cutting
Copyright Law Article 37(1) conditions to the declared Saudi AI-development
pathway and is the required profile for new legal-completeness experiments.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

PASS = "PASS_EVIDENCE_GATE"
REVIEW = "REVIEW_REQUIRED"
FAIL = "FAIL_EVIDENCE_GATE"

LEGACY_RECORD_VERSION = "0.1.0"
CURRENT_RECORD_VERSION = "0.2.0"
SUPPORTED_RECORD_VERSIONS = {LEGACY_RECORD_VERSION, CURRENT_RECORD_VERSION}

LEGACY_PROFILE_ID = "sa-copyright-2026-art26-4-ir30-legacy-v0.1"
CURRENT_PROFILE_ID = "sa-copyright-2026-art26-4-art37-1-ir30-v0.2"


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    message: str


@dataclass(frozen=True)
class GateResult:
    outcome: str
    findings: list[Finding]
    legal_profile_id: str
    declared_scope_complete: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "findings": [asdict(finding) for finding in self.findings],
            "legal_conclusion": False,
            "legal_profile_id": self.legal_profile_id,
            "declared_scope_complete": self.declared_scope_complete,
        }


def _get(record: dict[str, Any], *path: str) -> Any:
    cur: Any = record
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def _profile_metadata(record: dict[str, Any]) -> tuple[str, bool]:
    version = _get(record, "record_version")
    if version == CURRENT_RECORD_VERSION:
        return CURRENT_PROFILE_ID, True
    if version == LEGACY_RECORD_VERSION:
        # Historical experiments intentionally preserve their original scope.
        return LEGACY_PROFILE_ID, False
    return "unsupported-record-profile", False


def _contract_findings(record: dict[str, Any]) -> list[Finding]:
    """Validate the safety-critical subset of the evidence record contract.

    The JSON Schema remains the portable contract. This local check exists so the
    evidence gate fails closed even when callers do not run a JSON-Schema validator.
    """
    findings: list[Finding] = []

    required_strings = (
        ("record_version",),
        ("record_id",),
        ("work", "type"),
        ("work", "source"),
        ("use", "purpose"),
        ("use", "date"),
    )
    for path in required_strings:
        value = _get(record, *path)
        if not isinstance(value, str) or not value.strip():
            findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid required string: {'.'.join(path)}"))

    record_version = _get(record, "record_version")
    if record_version not in SUPPORTED_RECORD_VERSIONS:
        findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Unsupported record_version: {record_version!r}"))

    enum_fields = {
        ("work", "publication_status"): {"verified", "unverified", "false"},
        ("work", "acquisition_status"): {"verified", "unverified", "false"},
        ("use", "necessity_status"): {"supported", "uncertain", "unsupported"},
        ("rights_context", "legitimate_interests_prejudice"): {"none", "unjustified", "uncertain", "not_assessed"},
        ("rights_context", "exploitation_opportunity_effect"): {"none", "adverse", "uncertain", "not_assessed"},
        ("rights_context", "independent_elements_status"): {"none_identified", "assessed", "requires_review", "not_assessed"},
        ("output_context", "inclusion_necessary"): {"yes", "no", "uncertain", "not_applicable"},
        ("output_context", "permission_status"): {"granted", "not_granted", "uncertain", "not_applicable"},
        ("output_context", "public_domain_status"): {"yes", "no", "uncertain"},
    }
    for path, allowed in enum_fields.items():
        value = _get(record, *path)
        if value not in allowed:
            findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid enum: {'.'.join(path)}"))

    boolean_fields = (
        ("use", "republication"),
        ("use", "distribution"),
        ("use", "direct_commercial_exploitation"),
        ("use", "purely_commercial_context"),
        ("output_context", "transformed"),
        ("output_context", "republished"),
        ("output_context", "made_public"),
        ("output_context", "included_in_final_product"),
    )
    for path in boolean_fields:
        if not isinstance(_get(record, *path), bool):
            findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid boolean: {'.'.join(path)}"))

    for key in ("publication", "acquisition", "use_event"):
        value = _get(record, "evidence", key)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid evidence list: evidence.{key}"))

    for key in ("impact_assessment_basis", "independent_elements_basis"):
        value = _get(record, "rights_context", key)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid assessment-basis list: rights_context.{key}"))

    # Profile 0.2.0 explicitly models the two cross-cutting Article 37(1)
    # propositions instead of re-labelling superficially similar IR-30 fields.
    if record_version == CURRENT_RECORD_VERSION:
        article37 = _get(record, "article37_context")
        if not isinstance(article37, dict):
            findings.append(Finding("IPEL-CONTRACT", "FAIL", "Missing/invalid object: article37_context"))
        else:
            art37_enums = {
                "normal_exploitation_conflict": {"no_conflict", "conflict", "uncertain", "not_assessed"},
                "rightsholder_legitimate_interests_prejudice": {"none", "unjustified", "uncertain", "not_assessed"},
            }
            for key, allowed in art37_enums.items():
                if article37.get(key) not in allowed:
                    findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid enum: article37_context.{key}"))
            for key in ("normal_exploitation_basis", "rightsholder_interests_basis"):
                value = article37.get(key)
                if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                    findings.append(Finding("IPEL-CONTRACT", "FAIL", f"Missing/invalid assessment-basis list: article37_context.{key}"))

    return findings


def _evaluate_article37(record: dict[str, Any], findings: list[Finding]) -> None:
    """Evaluate the bounded Article 37(1) evidence abstraction for profile 0.2.0.

    Article 37(1) applies across uses in Articles 26-36. The project therefore
    models it separately from IR 30(2)'s commercial-context normal-exploitation
    field and IR 30(4)'s author-interest/opportunity fields.
    """
    article37 = _get(record, "article37_context") or {}

    conflict = article37.get("normal_exploitation_conflict")
    conflict_basis = article37.get("normal_exploitation_basis") or []
    if conflict == "conflict":
        findings.append(Finding("LAW-37(1)", "FAIL", "Record indicates conflict with normal exploitation of the work."))
    elif conflict in (None, "uncertain", "not_assessed"):
        findings.append(Finding("LAW-37(1)", "REVIEW", "Conflict with normal exploitation is unresolved or not assessed."))
    elif conflict == "no_conflict" and not conflict_basis:
        findings.append(Finding("LAW-37(1)", "REVIEW", "No-conflict assessment under Article 37(1) has no recorded basis."))

    prejudice = article37.get("rightsholder_legitimate_interests_prejudice")
    prejudice_basis = article37.get("rightsholder_interests_basis") or []
    if prejudice == "unjustified":
        findings.append(Finding("LAW-37(1)", "FAIL", "Record indicates unjustified prejudice to the legitimate interests of rightsholders."))
    elif prejudice in (None, "uncertain", "not_assessed"):
        findings.append(Finding("LAW-37(1)", "REVIEW", "Rightsholder legitimate-interests prejudice is unresolved or not assessed."))
    elif prejudice == "none" and not prejudice_basis:
        findings.append(Finding("LAW-37(1)", "REVIEW", "Favorable rightsholder-interests assessment under Article 37(1) has no recorded basis."))


def evaluate(record: dict[str, Any]) -> GateResult:
    findings: list[Finding] = _contract_findings(record)
    record_version = _get(record, "record_version")

    # Implementing Regulations Art. 30(3): retained record core.
    core = {
        "work.type": _get(record, "work", "type"),
        "work.source": _get(record, "work", "source"),
        "use.purpose": _get(record, "use", "purpose"),
        "use.date": _get(record, "use", "date"),
    }
    for field, value in core.items():
        if value is None or value == "":
            findings.append(Finding("IR-30(3)", "FAIL", f"Missing core retained-record field: {field}"))

    # Copyright Law Art. 26(4): publication and acquisition predicates.
    publication = _get(record, "work", "publication_status")
    acquisition = _get(record, "work", "acquisition_status")
    if publication == "false":
        findings.append(Finding("LAW-26(4)", "FAIL", "Record states that lawful publication is false."))
    elif publication not in ("verified", "false"):
        findings.append(Finding("LAW-26(4)", "REVIEW", "Lawful publication is not verified."))

    if acquisition == "false":
        findings.append(Finding("LAW-26(4)", "FAIL", "Record states that lawful acquisition is false."))
    elif acquisition != "verified":
        findings.append(Finding("LAW-26(4)", "REVIEW", "Lawful acquisition is not verified."))

    necessity = _get(record, "use", "necessity_status")
    if necessity == "unsupported":
        findings.append(Finding("LAW-26(4)/IR-30(1)", "FAIL", "Copying/analysis necessity is recorded as unsupported."))
    elif necessity != "supported":
        findings.append(Finding("LAW-26(4)/IR-30(1)", "REVIEW", "Necessity/proportionality requires review."))

    # Profile 0.2.0 adds the cross-cutting statutory safeguard. Legacy 0.1.0
    # results are left unchanged for reproducibility and are machine-labelled as
    # incomplete in GateResult metadata.
    if record_version == CURRENT_RECORD_VERSION:
        _evaluate_article37(record, findings)

    # IR 30(1): direct prohibited uses under the encoded exception pathway.
    for field, label in (
        ("republication", "republication"),
        ("distribution", "distribution"),
        ("direct_commercial_exploitation", "direct commercial exploitation"),
    ):
        if _get(record, "use", field) is True:
            findings.append(Finding("IR-30(1)", "FAIL", f"Record indicates {label}."))

    # IR 30(2): purely commercial context requires a qualifying path.
    if _get(record, "use", "purely_commercial_context") is True:
        materiality = _get(record, "use", "materiality_to_work")
        impact = _get(record, "use", "normal_exploitation_impact")
        qualifies = materiality == "non_substantial" or impact == "none"
        if impact == "adverse" and materiality == "substantial":
            findings.append(Finding("IR-30(2)", "FAIL", "Purely commercial use is substantial and recorded as adversely affecting normal exploitation."))
        elif not qualifies:
            findings.append(Finding("IR-30(2)", "REVIEW", "Purely commercial context lacks a clearly recorded qualifying condition."))

    prejudice = _get(record, "rights_context", "legitimate_interests_prejudice")
    opportunity = _get(record, "rights_context", "exploitation_opportunity_effect")
    impact_basis = _get(record, "rights_context", "impact_assessment_basis") or []
    if prejudice == "unjustified" or opportunity == "adverse":
        findings.append(Finding("IR-30(4)", "FAIL", "Record indicates prejudice or adverse exploitation-opportunity effect."))
    elif prejudice in (None, "uncertain", "not_assessed") or opportunity in (None, "uncertain", "not_assessed"):
        findings.append(Finding("IR-30(4)", "REVIEW", "Author-interest/market-effect assessment is incomplete or uncertain."))
    elif not impact_basis:
        findings.append(Finding("IR-30(4)", "REVIEW", "Favorable author-interest/market-effect assessment has no recorded basis."))

    # IR 30(5): some output configurations can be detected mechanically.
    out = _get(record, "output_context") or {}
    protected_output_action = any(out.get(k) is True for k in ("transformed", "republished", "made_public"))
    permission = out.get("permission_status") == "granted"
    public_domain = out.get("public_domain_status") == "yes"
    if protected_output_action and not (permission or public_domain):
        findings.append(Finding("IR-30(5)", "FAIL", "Output transformation/republication/public availability is recorded without permission or public-domain status."))

    if out.get("included_in_final_product") is True and out.get("inclusion_necessary") == "no" and not (permission or public_domain):
        findings.append(Finding("IR-30(5)", "FAIL", "Work is unnecessarily included in the final product without recorded permission/public-domain status."))
    elif out.get("included_in_final_product") is True and out.get("inclusion_necessary") in ("uncertain", None):
        findings.append(Finding("IR-30(5)", "REVIEW", "Final-product inclusion necessity is uncertain."))

    independent = _get(record, "rights_context", "independent_elements_status")
    independent_basis = _get(record, "rights_context", "independent_elements_basis") or []
    if independent in (None, "requires_review", "not_assessed"):
        findings.append(Finding("IR-30(6)", "REVIEW", "Independently protected elements are not fully assessed."))
    elif not independent_basis:
        findings.append(Finding("IR-30(6)", "REVIEW", "Independent-elements assessment has no recorded basis."))

    # Evidence quality: assertions marked verified should have references.
    if publication == "verified" and not (_get(record, "evidence", "publication") or []):
        findings.append(Finding("EVIDENCE", "REVIEW", "Publication is marked verified but has no evidence reference."))
    if acquisition == "verified" and not (_get(record, "evidence", "acquisition") or []):
        findings.append(Finding("EVIDENCE", "REVIEW", "Acquisition is marked verified but has no evidence reference."))
    if not (_get(record, "evidence", "use_event") or []):
        findings.append(Finding("EVIDENCE", "REVIEW", "No use-event evidence reference is recorded."))

    severities = {finding.severity for finding in findings}
    if "FAIL" in severities:
        outcome = FAIL
    elif "REVIEW" in severities:
        outcome = REVIEW
    else:
        outcome = PASS

    profile_id, scope_complete = _profile_metadata(record)
    return GateResult(
        outcome=outcome,
        findings=findings,
        legal_profile_id=profile_id,
        declared_scope_complete=scope_complete,
    )


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("usage: python -m src.ipel.validator <record.json>", file=sys.stderr)
        return 2
    record = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    result = evaluate(record)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 1 if result.outcome == FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
