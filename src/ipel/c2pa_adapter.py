"""Neutral adapter for real c2patool validation reports.

Stage 004 deliberately keeps C2PA cryptographic/provenance observations separate
from IPEL legal-evidence fields. Nothing in this module upgrades publication,
acquisition, ownership, permission, or legal-compliance status.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, asdict
from typing import Any

TDM_KEYS = {
    "cawg.data_mining",
    "cawg.ai_inference",
    "cawg.ai_training",
    "cawg.ai_generative_training",
}
TDM_USES = {"allowed", "notAllowed", "constrained"}


class C2PAReportError(ValueError):
    pass


@dataclass(frozen=True)
class C2PAEvidence:
    validation_state: str
    asset_binding: str
    claim_signature: str
    assertion_references: str
    signer_trust: str
    tdm_entries: dict[str, str]
    tdm_conflicts: list[str]
    digital_source_types: list[str]
    issue_codes: list[str]
    success_codes: list[str]
    semantic_warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validation_buckets(report: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    vr = report.get("validation_results")
    if not isinstance(vr, dict):
        raise C2PAReportError("validation_results must be an object")
    active = vr.get("activeManifest")
    if not isinstance(active, dict):
        raise C2PAReportError("validation_results.activeManifest must be an object")
    success = active.get("success", [])
    failure = active.get("failure", [])
    if not isinstance(success, list) or not isinstance(failure, list):
        raise C2PAReportError("validation result buckets must be arrays")
    return success, failure


def _codes(items: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("code"), str):
            raise C2PAReportError("validation entries require string code")
        out.append(item["code"])
    return sorted(set(out))


def _classify_pair(success_codes: list[str], issue_codes: list[str], ok: str, bad: str) -> str:
    if bad in issue_codes:
        return "invalid"
    if ok in success_codes:
        return "valid"
    return "unknown"


def _active_manifest(report: dict[str, Any]) -> dict[str, Any]:
    active = report.get("active_manifest")
    manifests = report.get("manifests")
    if not isinstance(active, str) or not isinstance(manifests, dict):
        raise C2PAReportError("active manifest metadata missing")
    manifest = manifests.get(active)
    if not isinstance(manifest, dict):
        raise C2PAReportError("active manifest not found")
    return manifest


def _extract_assertions(manifest: dict[str, Any]) -> tuple[dict[str, str], list[str], list[str], list[str]]:
    assertions = manifest.get("assertions", [])
    if not isinstance(assertions, list):
        raise C2PAReportError("manifest assertions must be an array")
    tdm_seen: dict[str, set[str]] = {}
    source_types: set[str] = set()
    warnings: list[str] = []
    for assertion in assertions:
        if not isinstance(assertion, dict):
            raise C2PAReportError("assertion must be an object")
        label = assertion.get("label")
        data = assertion.get("data")
        if label == "cawg.training-mining" and isinstance(data, dict):
            entries = data.get("entries", {})
            if not isinstance(entries, dict):
                raise C2PAReportError("TDM entries must be an object")
            for key, value in entries.items():
                if key not in TDM_KEYS:
                    warnings.append(f"unsupported TDM key: {key}")
                    continue
                if not isinstance(value, dict) or value.get("use") not in TDM_USES:
                    warnings.append(f"invalid TDM use: {key}")
                    continue
                tdm_seen.setdefault(key, set()).add(value["use"])
        if label == "c2pa.actions.v2" and isinstance(data, dict):
            actions = data.get("actions", [])
            if isinstance(actions, list):
                for action in actions:
                    if isinstance(action, dict) and isinstance(action.get("digitalSourceType"), str):
                        source_types.add(action["digitalSourceType"])
    conflicts = sorted(key for key, values in tdm_seen.items() if len(values) > 1)
    entries = {key: next(iter(values)) for key, values in sorted(tdm_seen.items()) if len(values) == 1}
    return entries, conflicts, sorted(source_types), sorted(set(warnings))


def extract_c2pa_evidence(report: dict[str, Any]) -> C2PAEvidence:
    if not isinstance(report, dict):
        raise C2PAReportError("report must be an object")
    state = report.get("validation_state")
    if state not in {"Valid", "Invalid", "Unknown", None}:
        raise C2PAReportError("unexpected validation_state")
    success, failure = _validation_buckets(report)
    success_codes = _codes(success)
    issue_codes = _codes(failure)
    manifest = _active_manifest(report)
    tdm_entries, conflicts, source_types, semantic_warnings = _extract_assertions(manifest)

    binding = _classify_pair(success_codes, issue_codes, "assertion.dataHash.match", "assertion.dataHash.mismatch")
    signature = _classify_pair(success_codes, issue_codes, "claimSignature.validated", "claimSignature.mismatch")
    if "assertion.hashedURI.mismatch" in issue_codes:
        refs = "invalid"
    elif "assertion.hashedURI.match" in success_codes:
        refs = "valid"
    else:
        refs = "unknown"
    if "signingCredential.untrusted" in issue_codes:
        trust = "untrusted"
    elif "signingCredential.trusted" in success_codes:
        trust = "trusted"
    else:
        trust = "not_established"

    return C2PAEvidence(
        validation_state=(state or "Unknown").lower(),
        asset_binding=binding,
        claim_signature=signature,
        assertion_references=refs,
        signer_trust=trust,
        tdm_entries=tdm_entries,
        tdm_conflicts=conflicts,
        digital_source_types=source_types,
        issue_codes=issue_codes,
        success_codes=success_codes,
        semantic_warnings=semantic_warnings,
    )


def coupled_evaluation(report: dict[str, Any], ipel_record: dict[str, Any]) -> dict[str, Any]:
    """Return parallel provenance and legal evaluations without cross-over inference."""
    from src.ipel.validator import evaluate

    before = copy.deepcopy(ipel_record)
    evidence = extract_c2pa_evidence(report)
    legal = evaluate(ipel_record)
    if ipel_record != before:
        raise AssertionError("C2PA adapter mutated IPEL legal record")
    return {
        "c2pa_evidence": evidence.to_dict(),
        "legal_gate": legal.to_dict(),
        "legal_fields_overwritten": False,
    }
