"""Stage-005 normalization across two C2PA validation surfaces.

The two current surfaces share c2pa-rs lineage, so this module reports
cross-surface/cross-version agreement and never claims implementation diversity.
It also never translates C2PA trust or CAWG usage signals into IPEL legal facts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.ipel.c2pa_adapter import TDM_KEYS, TDM_USES, extract_c2pa_evidence


class CrossCheckError(ValueError):
    pass


@dataclass(frozen=True)
class CommonValidation:
    surface: str
    engine_lineage: str
    engine_version: str
    cryptographic_validity: str
    asset_binding: str
    claim_signature: str
    assertion_references: str
    signer_trust: str
    tdm_entries: dict[str, str]
    semantic_warnings: list[str]
    success_codes: list[str]
    failure_codes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _crypto_state(binding: str, signature: str, refs: str) -> str:
    states = {binding, signature, refs}
    if "invalid" in states:
        return "invalid"
    if states == {"valid"}:
        return "valid"
    return "unknown"


def _reader_engine_version(report: dict[str, Any]) -> str:
    active = report.get("active_manifest")
    manifests = report.get("manifests")
    if not isinstance(active, str) or not isinstance(manifests, dict):
        return "unknown"
    manifest = manifests.get(active, {})
    infos = manifest.get("claim_generator_info", []) if isinstance(manifest, dict) else []
    if isinstance(infos, list):
        for info in infos:
            if isinstance(info, dict) and isinstance(info.get("org.contentauth.c2pa_rs"), str):
                return info["org.contentauth.c2pa_rs"]
    return "unknown"


def normalize_c2patool(report: dict[str, Any]) -> CommonValidation:
    evidence = extract_c2pa_evidence(report)
    return CommonValidation(
        surface="c2patool-reader",
        engine_lineage="c2pa-rs",
        engine_version=_reader_engine_version(report),
        cryptographic_validity=_crypto_state(
            evidence.asset_binding, evidence.claim_signature, evidence.assertion_references
        ),
        asset_binding=evidence.asset_binding,
        claim_signature=evidence.claim_signature,
        assertion_references=evidence.assertion_references,
        signer_trust=evidence.signer_trust,
        tdm_entries=evidence.tdm_entries,
        semantic_warnings=evidence.semantic_warnings,
        success_codes=evidence.success_codes,
        failure_codes=evidence.issue_codes,
    )


def _coded(bucket: Any) -> list[str]:
    if not isinstance(bucket, list):
        raise CrossCheckError("validation bucket must be an array")
    result: list[str] = []
    for item in bucket:
        if not isinstance(item, dict) or not isinstance(item.get("code"), str):
            raise CrossCheckError("validation item requires code")
        result.append(item["code"])
    return sorted(set(result))


def _classify(success: list[str], failure: list[str], ok: str, bad: str) -> str:
    if bad in failure:
        return "invalid"
    if ok in success:
        return "valid"
    return "unknown"


def _cross_manifest(report: dict[str, Any]) -> dict[str, Any]:
    manifests = report.get("manifests")
    if not isinstance(manifests, list) or len(manifests) != 1 or not isinstance(manifests[0], dict):
        raise CrossCheckError("Stage 005 expects exactly one crJSON manifest")
    return manifests[0]


def _cross_tdm(manifest: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    assertions = manifest.get("assertions")
    if not isinstance(assertions, dict):
        raise CrossCheckError("crJSON assertions must be an object")
    tdm = assertions.get("cawg.training-mining")
    if tdm is None:
        return {}, []
    if not isinstance(tdm, dict) or not isinstance(tdm.get("entries"), dict):
        return {}, ["malformed cawg.training-mining assertion"]
    entries: dict[str, str] = {}
    warnings: list[str] = []
    for key, value in sorted(tdm["entries"].items()):
        if key not in TDM_KEYS:
            warnings.append(f"unsupported TDM key: {key}")
            continue
        use = value.get("use") if isinstance(value, dict) else None
        if use not in TDM_USES:
            warnings.append(f"invalid TDM use: {key}")
            continue
        entries[key] = use
    return entries, sorted(set(warnings))


def normalize_cross_validator(report: dict[str, Any]) -> CommonValidation:
    if not isinstance(report, dict):
        raise CrossCheckError("crJSON report must be an object")
    manifest = _cross_manifest(report)
    vr = manifest.get("validationResults")
    if not isinstance(vr, dict):
        raise CrossCheckError("manifest validationResults missing")
    success = _coded(vr.get("success", []))
    failure = _coded(vr.get("failure", []))
    binding = _classify(success, failure, "assertion.dataHash.match", "assertion.dataHash.mismatch")
    signature = _classify(success, failure, "claimSignature.validated", "claimSignature.mismatch")
    if "assertion.hashedURI.mismatch" in failure:
        refs = "invalid"
    elif "assertion.hashedURI.match" in success:
        refs = "valid"
    else:
        refs = "unknown"
    if "signingCredential.trusted" in success:
        trust = "trusted"
    elif "signingCredential.untrusted" in failure:
        trust = "untrusted"
    else:
        trust = "not_established"
    entries, warnings = _cross_tdm(manifest)
    generator = report.get("jsonGenerator", {})
    engine_version = generator.get("version", "unknown") if isinstance(generator, dict) else "unknown"
    return CommonValidation(
        surface="c2pa-conformance-tool-cli",
        engine_lineage="c2pa-rs",
        engine_version=str(engine_version),
        cryptographic_validity=_crypto_state(binding, signature, refs),
        asset_binding=binding,
        claim_signature=signature,
        assertion_references=refs,
        signer_trust=trust,
        tdm_entries=entries,
        semantic_warnings=warnings,
        success_codes=success,
        failure_codes=failure,
    )


def agreement(left: CommonValidation, right: CommonValidation) -> dict[str, Any]:
    fields = (
        "cryptographic_validity",
        "asset_binding",
        "claim_signature",
        "assertion_references",
        "signer_trust",
        "tdm_entries",
        "semantic_warnings",
    )
    comparisons = {field: getattr(left, field) == getattr(right, field) for field in fields}
    return {
        "fields": comparisons,
        "all_common_semantics_agree": all(comparisons.values()),
        "shared_engine_lineage": left.engine_lineage == right.engine_lineage == "c2pa-rs",
        "different_engine_versions": left.engine_version != right.engine_version,
        "implementation_diversity_established": False,
    }


def validate_cross_tool_provenance(provenance: Any) -> None:
    required = {
        "repository": "contentauth/c2pa-conformance-tool-cli",
        "commit": "c09f0340524b088a81475f7b7eaab5ba7042772f",
        "version": "0.2.0",
        "source_archive_sha256": "3571355b1a83d7150393d070e7b4a5b5c0f32d8524b6d7a41f740395c9cefc85",
        "rust": "1.98.0",
        "cargo_lock_sha256": "80dcab12a2773a6cffd3c6c8794640d0be9cff3a9227d7abd44143e963fa6fd0",
        "c2pa_rs_commit": "61f2e676043c1d22fa60f4fe5d09d3874c7c8a10",
        "c2pa_rs_archive_sha256": "4a27ab5cceb4ea4e42b1e629808a0895f2c91a0fea5cd71c5827665d8f7e8bc7",
        "declared_profile_commit_unavailable": "c43d11162c27c5e992c7010fc75b72bb3e5520e1",
        "profile_repair_repository": "adobe/profile-evaluator-rs",
        "profile_repair_commit": "40c4201933e3b4760932b65913e2a9c57413f8ac",
        "profile_repair_archive_sha256": "2c51d6aafdc67f075a5ce31d6700ab031df214789bdb9a893dc60b48391b7e6a",
        "declared_json_formula_commit": "1ff483f15157521503a0ce79c123333ecd14ce08",
        "json_formula_repair_repository": "adobe/json-formula-rs",
        "json_formula_repair_commit": "90ee7f44ded98c657a410a0bf1248a9e3f6f1627",
        "json_formula_repair_commit_verified": True,
        "compatibility_repair": True,
        "shared_engine_lineage": "c2pa-rs",
        "implementation_diversity_established": False,
    }
    if not isinstance(provenance, dict):
        raise CrossCheckError("cross-validator provenance must be an object")
    for key, expected in required.items():
        if provenance.get(key) != expected:
            raise CrossCheckError(f"cross-validator provenance mismatch: {key}")
