"""C2PA-aligned IPEL profile experiment for Stage 003.

This module does not emit a conformant C2PA Manifest and does not perform C2PA
validation or signing. It models which IPEL facts can be carried by stable C2PA/
CAWG semantics and which facts must remain jurisdiction-specific legal evidence.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

PROFILE_VERSION = "0.1.0"
PROFILE_KIND = "c2pa-aligned-ipel-profile"
C2PA_VERSION = "2.4"
CAWG_TDM_VERSION = "1.1"
TDM_USES = {"allowed", "notAllowed", "constrained"}
TDM_KEYS = {
    "cawg.data_mining",
    "cawg.ai_inference",
    "cawg.ai_training",
    "cawg.ai_generative_training",
}

# Only fields with a sufficiently stable generic provenance semantic are removed
# from the jurisdictional payload. Everything else remains IPEL-owned.
GENERIC_FIELD_MAP: dict[str, str] = {
    "work.title": "c2pa.ingredient.dc:title",
}

INTERPRETATION_BARRIERS = [
    "c2pa_validation_does_not_prove_lawful_publication",
    "c2pa_validation_does_not_prove_lawful_acquisition",
    "tdm_signal_does_not_prove_permission_or_license_validity",
    "identity_or_signature_does_not_prove_rights_ownership",
]


class ProfileError(ValueError):
    """Raised when a Stage-003 profile fails its experimental contract."""


@dataclass(frozen=True)
class RoundTripMetrics:
    original_gate: str
    reconstructed_gate: str
    gate_preserved: bool
    article_30_3_preserved: bool
    semantic_loss_count: int
    duplicate_generic_field_count: int
    mapped_generic_field_count: int
    jurisdictional_leaf_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def _get(obj: dict[str, Any], dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _pop(obj: dict[str, Any], dotted: str) -> Any:
    parts = dotted.split(".")
    cur: Any = obj
    for part in parts[:-1]:
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    if not isinstance(cur, dict):
        return None
    return cur.pop(parts[-1], None)


def _set(obj: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = obj
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def _prune_empty(obj: Any) -> Any:
    if isinstance(obj, dict):
        for key in list(obj):
            obj[key] = _prune_empty(obj[key])
            if obj[key] == {}:
                del obj[key]
    return obj


def to_profile(
    record: dict[str, Any],
    *,
    manifest_ref: str = "urn:c2pa:manifest:synthetic",
    tdm_key: str = "cawg.ai_training",
    tdm_use: str = "constrained",
    manifest_state: str = "unknown",
    trust_state: str = "unknown",
) -> dict[str, Any]:
    """Split one IPEL record into generic C2PA-carried and legal-specific facts."""
    if not isinstance(record, dict):
        raise ProfileError("record must be an object")
    if tdm_key not in TDM_KEYS:
        raise ProfileError("unsupported CAWG TDM key")
    if tdm_use not in TDM_USES:
        raise ProfileError("unsupported CAWG TDM use value")

    jurisdictional = copy.deepcopy(record)
    ingredient: dict[str, Any] = {"relationship": "inputTo"}

    title = _pop(jurisdictional, "work.title")
    if title is not None:
        ingredient["dc:title"] = title
    _prune_empty(jurisdictional)

    profile = {
        "profile_version": PROFILE_VERSION,
        "profile_kind": PROFILE_KIND,
        "c2pa": {
            "spec_version": C2PA_VERSION,
            "representation": "aligned-intermediate-not-a-manifest",
            "manifest_ref": manifest_ref,
            "ingredient": ingredient,
            "tdm_assertion": {
                "label": "cawg.training-mining",
                "version": CAWG_TDM_VERSION,
                "entries": {tdm_key: {"use": tdm_use}},
            },
            "validation_signals": {
                "manifest_state": manifest_state,
                "trust_state": trust_state,
            },
        },
        "ipel_jurisdictional": jurisdictional,
        "field_map": copy.deepcopy(GENERIC_FIELD_MAP),
        "interpretation_barriers": list(INTERPRETATION_BARRIERS),
    }
    errors = validate_profile(profile)
    if errors:
        raise ProfileError("; ".join(errors))
    return profile


def validate_profile(profile: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(profile, dict):
        return ["profile must be an object"]
    if profile.get("profile_version") != PROFILE_VERSION:
        errors.append("unsupported profile_version")
    if profile.get("profile_kind") != PROFILE_KIND:
        errors.append("unexpected profile_kind")
    c2pa = profile.get("c2pa")
    if not isinstance(c2pa, dict):
        return errors + ["c2pa must be an object"]
    if c2pa.get("spec_version") != C2PA_VERSION:
        errors.append("unexpected C2PA version")
    if c2pa.get("representation") != "aligned-intermediate-not-a-manifest":
        errors.append("representation must disclaim Manifest conformance")
    ingredient = c2pa.get("ingredient")
    if not isinstance(ingredient, dict):
        errors.append("c2pa.ingredient must be an object")
    else:
        if ingredient.get("relationship") != "inputTo":
            errors.append("c2pa.ingredient.relationship must be inputTo")
    tdm = c2pa.get("tdm_assertion")
    if not isinstance(tdm, dict) or tdm.get("label") != "cawg.training-mining":
        errors.append("CAWG TDM assertion label is required")
    else:
        entries = tdm.get("entries")
        if not isinstance(entries, dict) or not entries:
            errors.append("CAWG TDM entries are required")
        else:
            for key, entry in entries.items():
                if key not in TDM_KEYS:
                    errors.append(f"unsupported TDM key: {key}")
                if not isinstance(entry, dict) or entry.get("use") not in TDM_USES:
                    errors.append(f"invalid TDM use for {key}")
    if not isinstance(profile.get("ipel_jurisdictional"), dict):
        errors.append("ipel_jurisdictional must be an object")
    else:
        jurisdictional = profile["ipel_jurisdictional"]
        for path in ("record_version", "record_id", "work.type", "work.source", "use.purpose", "use.date"):
            value = _get(jurisdictional, path)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"missing jurisdictional core field: {path}")
        for original in GENERIC_FIELD_MAP:
            if _get(jurisdictional, original) is not None:
                errors.append(f"duplicate generic field retained: {original}")
    barriers = profile.get("interpretation_barriers")
    if barriers != INTERPRETATION_BARRIERS:
        errors.append("interpretation barriers are missing or modified")
    return errors


def from_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct IPEL without inferring legal status from C2PA/CAWG signals."""
    errors = validate_profile(profile)
    if errors:
        raise ProfileError("; ".join(errors))
    record = copy.deepcopy(profile["ipel_jurisdictional"])
    ingredient = profile["c2pa"]["ingredient"]
    if "dc:title" in ingredient:
        _set(record, "work.title", ingredient["dc:title"])
    return record


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    leaves: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else key
            leaves.update(_flatten(value[key], child))
    elif isinstance(value, list):
        if not value:
            leaves[prefix] = []
        else:
            for index, item in enumerate(value):
                leaves.update(_flatten(item, f"{prefix}[{index}]"))
    else:
        leaves[prefix] = value
    return leaves


def semantic_loss(original: dict[str, Any], reconstructed: dict[str, Any]) -> list[str]:
    left = _flatten(original)
    right = _flatten(reconstructed)
    paths = sorted(set(left) | set(right))
    return [path for path in paths if left.get(path) != right.get(path)]


def duplicate_generic_fields(profile: dict[str, Any]) -> list[str]:
    jurisdictional = profile.get("ipel_jurisdictional", {})
    return [path for path in GENERIC_FIELD_MAP if _get(jurisdictional, path) is not None]


def article_30_3_tuple(record: dict[str, Any]) -> tuple[Any, Any, Any, Any]:
    return (
        _get(record, "work.type"),
        _get(record, "work.source"),
        _get(record, "use.purpose"),
        _get(record, "use.date"),
    )


def roundtrip_metrics(record: dict[str, Any], profile: dict[str, Any]) -> RoundTripMetrics:
    # Local import avoids coupling the profile representation into the Stage-001 gate.
    from src.ipel.validator import evaluate

    reconstructed = from_profile(profile)
    original_gate = evaluate(record).outcome
    reconstructed_gate = evaluate(reconstructed).outcome
    return RoundTripMetrics(
        original_gate=original_gate,
        reconstructed_gate=reconstructed_gate,
        gate_preserved=original_gate == reconstructed_gate,
        article_30_3_preserved=article_30_3_tuple(record) == article_30_3_tuple(reconstructed),
        semantic_loss_count=len(semantic_loss(record, reconstructed)),
        duplicate_generic_field_count=len(duplicate_generic_fields(profile)),
        mapped_generic_field_count=sum(1 for path in GENERIC_FIELD_MAP if _get(record, path) is not None),
        jurisdictional_leaf_count=len(_flatten(profile["ipel_jurisdictional"])),
    )
