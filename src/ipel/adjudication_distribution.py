"""Stage 008 contamination-resistant adjudication distribution and intake.

This module reduces casual/accidental deblinding by remapping public Stage-007 case
identifiers to per-distribution HMAC-derived external IDs. It also provides keyed
bundle/mapping integrity checks and a keyed post-intake receipt chain. It does NOT
prove human identity, adjudicator qualification, or pre-intake response authenticity.
"""
from __future__ import annotations

import copy
import hashlib
import hmac
import json
import random
import re
from pathlib import Path
from typing import Any

from src.ipel.adjudication import AdjudicationError, validate_adjudication_response

ROOT = Path(__file__).resolve().parents[2]
PRIVATE_ROOT = ROOT / ".private-stage008"
DISTRIBUTION_ROOT = ROOT / ".stage008-distributions"
BUNDLE_VERSION = "stage008-distribution-v1"
MAPPING_VERSION = "stage008-private-mapping-v1"
RESPONSE_VERSION = "stage008-external-response-v1"
LEDGER_VERSION = "stage008-keyed-intake-ledger-v1"
EXTERNAL_CASE_RE = re.compile(r"^CASE-[A-F0-9]{16}$")
DISTRIBUTION_ID_RE = re.compile(r"^[A-Za-z0-9._-]{3,80}$")
FORBIDDEN_EXTERNAL_TOKENS = (
    "ADJ-",
    "OBJ-",
    "JDG-",
    "READY_FOR_LEGAL_EVALUATION",
    "NOT_READY_FOR_LEGAL_EVALUATION",
    "PASS_EVIDENCE_GATE",
    "REVIEW_REQUIRED",
    "FAIL_EVIDENCE_GATE",
    "hidden_case_map",
    "stage006_author_",
    "github.com",
    "Abdullah-m7",
)


class DistributionError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256_hex(canonical_bytes(value))


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise DistributionError("distribution key must contain at least 32 bytes")


def parse_key_hex(value: str) -> bytes:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-fA-F]{64,}", value) is None or len(value) % 2:
        raise DistributionError("distribution key must be an even-length hex string of at least 64 characters")
    key = bytes.fromhex(value)
    _validate_key(key)
    return key


def _hmac_hex(key: bytes, message: str | bytes) -> str:
    _validate_key(key)
    raw = message.encode("utf-8") if isinstance(message, str) else message
    return hmac.new(key, raw, hashlib.sha256).hexdigest()


def key_fingerprint(key: bytes) -> str:
    _validate_key(key)
    return sha256_hex(key)[:24]


def _external_case_id(key: bytes, distribution_id: str, internal_id: str) -> str:
    digest = _hmac_hex(key, f"case|{distribution_id}|{internal_id}")
    return "CASE-" + digest[:16].upper()


def _bundle_id(key: bytes, distribution_id: str) -> str:
    return "BND-" + _hmac_hex(key, f"bundle|{distribution_id}")[:16].upper()


def _sanitized_instructions(source: dict[str, Any]) -> dict[str, Any]:
    construct = source.get("construct") or source.get("task")
    if not isinstance(construct, str) or not construct.strip():
        raise DistributionError("source packet instructions are missing the adjudication construct")
    decision_options = source.get("decision_options")
    missing_options = source.get("missing_information_options") or source.get("missing_fact_options")
    if not isinstance(decision_options, list) or not isinstance(missing_options, list):
        raise DistributionError("source packet instructions are incomplete")
    return {
        "construct": construct,
        "blinding_instruction": (
            "Procedural blinding only: do not consult project repositories, prior case versions, "
            "answer materials, or other project artifacts while adjudicating. If you have seen the "
            "underlying cases or labels previously, set prior_exposure=true."
        ),
        "decision_options": copy.deepcopy(decision_options),
        "missing_information_options": copy.deepcopy(missing_options),
        "response_fields": [
            "external_case_id",
            "decision",
            "missing_information_codes",
            "confidence_0_to_100",
            "rationale",
            "prior_exposure",
            "conflict_of_interest",
        ],
    }


def scan_external_leakage(value: Any) -> list[str]:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return [token for token in FORBIDDEN_EXTERNAL_TOKENS if token in text]


def build_distribution(
    source_packet: dict[str, Any], distribution_id: str, key: bytes
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _validate_key(key)
    if DISTRIBUTION_ID_RE.fullmatch(distribution_id or "") is None:
        raise DistributionError("invalid distribution_id")
    packets = source_packet.get("packets")
    if source_packet.get("case_count") != 24 or not isinstance(packets, list) or len(packets) != 24:
        raise DistributionError("expected the frozen 24-case Stage-007 adjudication packet")

    mapping: dict[str, str] = {}
    external_packets: list[dict[str, Any]] = []
    seen_internal: set[str] = set()
    for item in packets:
        if not isinstance(item, dict):
            raise DistributionError("source packet row must be an object")
        internal_id = item.get("adjudication_case_id")
        if not isinstance(internal_id, str) or not internal_id.startswith("ADJ-"):
            raise DistributionError("source packet contains an invalid internal case ID")
        if internal_id in seen_internal:
            raise DistributionError("duplicate internal case ID")
        seen_internal.add(internal_id)
        external_id = _external_case_id(key, distribution_id, internal_id)
        if external_id in mapping:
            raise DistributionError("external case-ID collision")
        mapping[external_id] = internal_id
        external_packets.append(
            {
                "external_case_id": external_id,
                "material": copy.deepcopy(item.get("material")),
                "instructions": _sanitized_instructions(item.get("instructions", {})),
            }
        )

    order_seed = int(_hmac_hex(key, f"order|{distribution_id}")[:16], 16)
    random.Random(order_seed).shuffle(external_packets)
    bundle_id = _bundle_id(key, distribution_id)
    bundle = {
        "bundle_version": BUNDLE_VERSION,
        "bundle_id": bundle_id,
        "distribution_id": distribution_id,
        "blinding_model": "PROCEDURAL_NOT_CRYPTOGRAPHIC",
        "human_identity_verified_by_software": False,
        "case_count": 24,
        "packets": external_packets,
    }
    leaks = scan_external_leakage(bundle)
    if leaks:
        raise DistributionError(f"external bundle leakage detected: {leaks}")

    bundle_sha = object_sha256(bundle)
    manifest = {
        "manifest_version": "stage008-bundle-manifest-v1",
        "bundle_version": BUNDLE_VERSION,
        "bundle_id": bundle_id,
        "distribution_id": distribution_id,
        "case_count": 24,
        "bundle_sha256": bundle_sha,
        "bundle_hmac_sha256": _hmac_hex(key, bundle_sha),
    }
    mapping_payload = {
        "mapping_version": MAPPING_VERSION,
        "distribution_id": distribution_id,
        "bundle_id": bundle_id,
        "bundle_sha256": bundle_sha,
        "key_fingerprint": key_fingerprint(key),
        "source_packet_sha256": object_sha256(source_packet),
        "external_to_internal": dict(sorted(mapping.items())),
        "do_not_commit": True,
    }
    private_mapping = dict(mapping_payload)
    private_mapping["mapping_hmac_sha256"] = _hmac_hex(key, canonical_bytes(mapping_payload))
    return bundle, manifest, private_mapping


def validate_bundle(bundle: Any, manifest: Any, key: bytes) -> None:
    _validate_key(key)
    if not isinstance(bundle, dict) or not isinstance(manifest, dict):
        raise DistributionError("bundle and manifest must be objects")
    if bundle.get("bundle_version") != BUNDLE_VERSION:
        raise DistributionError("unexpected bundle version")
    if manifest.get("manifest_version") != "stage008-bundle-manifest-v1":
        raise DistributionError("unexpected bundle-manifest version")
    if bundle.get("bundle_id") != manifest.get("bundle_id") or bundle.get("distribution_id") != manifest.get("distribution_id"):
        raise DistributionError("bundle/manifest identity mismatch")
    if bundle.get("case_count") != 24 or manifest.get("case_count") != 24:
        raise DistributionError("bundle must contain 24 cases")
    actual_sha = object_sha256(bundle)
    if actual_sha != manifest.get("bundle_sha256"):
        raise DistributionError("bundle SHA-256 mismatch")
    if not hmac.compare_digest(
        str(manifest.get("bundle_hmac_sha256", "")), _hmac_hex(key, actual_sha)
    ):
        raise DistributionError("bundle HMAC mismatch")
    packets = bundle.get("packets")
    if not isinstance(packets, list) or len(packets) != 24:
        raise DistributionError("bundle packet count mismatch")
    external_ids = [item.get("external_case_id") for item in packets if isinstance(item, dict)]
    if len(external_ids) != 24 or len(set(external_ids)) != 24 or any(
        not isinstance(case_id, str) or EXTERNAL_CASE_RE.fullmatch(case_id) is None
        for case_id in external_ids
    ):
        raise DistributionError("invalid or duplicate external case IDs")
    leaks = scan_external_leakage(bundle)
    if leaks:
        raise DistributionError(f"external bundle leakage detected: {leaks}")


def validate_private_mapping(mapping: Any, manifest: dict[str, Any], key: bytes) -> dict[str, str]:
    _validate_key(key)
    if not isinstance(mapping, dict):
        raise DistributionError("private mapping must be an object")
    mac = mapping.get("mapping_hmac_sha256")
    payload = {key_: copy.deepcopy(value) for key_, value in mapping.items() if key_ != "mapping_hmac_sha256"}
    expected_mac = _hmac_hex(key, canonical_bytes(payload))
    if not isinstance(mac, str) or not hmac.compare_digest(mac, expected_mac):
        raise DistributionError("private mapping HMAC mismatch")
    if payload.get("mapping_version") != MAPPING_VERSION or payload.get("do_not_commit") is not True:
        raise DistributionError("unexpected private-mapping metadata")
    if payload.get("key_fingerprint") != key_fingerprint(key):
        raise DistributionError("private mapping key fingerprint mismatch")
    for field in ("bundle_id", "distribution_id", "bundle_sha256"):
        if payload.get(field) != manifest.get(field):
            raise DistributionError(f"private mapping/manifest mismatch: {field}")
    table = payload.get("external_to_internal")
    if not isinstance(table, dict) or len(table) != 24:
        raise DistributionError("private mapping must contain 24 cases")
    if any(EXTERNAL_CASE_RE.fullmatch(str(ext)) is None or not isinstance(internal, str) or not internal.startswith("ADJ-") for ext, internal in table.items()):
        raise DistributionError("private mapping contains invalid case IDs")
    return dict(table)


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def guard_private_destination(path: Path, repo_root: Path = ROOT) -> None:
    resolved = path.resolve()
    if _inside(resolved, repo_root) and not _inside(resolved, repo_root / ".private-stage008"):
        raise DistributionError("private mapping/ledger may only be written under .private-stage008 inside the repository")


def guard_bundle_destination(path: Path, repo_root: Path = ROOT) -> None:
    resolved = path.resolve()
    if _inside(resolved, repo_root) and not _inside(resolved, repo_root / ".stage008-distributions"):
        raise DistributionError("real distribution bundles may only be written under .stage008-distributions inside the repository")


def response_template(bundle: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    if bundle.get("bundle_id") != manifest.get("bundle_id"):
        raise DistributionError("bundle/manifest identity mismatch")
    return {
        "response_version": RESPONSE_VERSION,
        "bundle_id": bundle["bundle_id"],
        "distribution_id": bundle["distribution_id"],
        "bundle_sha256": manifest["bundle_sha256"],
        "data_origin": "FILL_REAL_HUMAN_OR_SYNTHETIC_NON_HUMAN",
        "adjudicator_id": "FILL_PSEUDONYMOUS_ID",
        "synthetic_fixture": False,
        "responses": [
            {
                "external_case_id": item["external_case_id"],
                "decision": "FILL_READY_NOT_READY_OR_UNSURE",
                "missing_information_codes": [],
                "confidence_0_to_100": None,
                "rationale": "",
                "prior_exposure": False,
                "conflict_of_interest": False,
            }
            for item in bundle["packets"]
        ],
    }


def normalize_external_response(
    document: Any,
    bundle: dict[str, Any],
    manifest: dict[str, Any],
    private_mapping: dict[str, Any],
    key: bytes,
    *,
    allow_synthetic: bool = False,
) -> dict[str, Any]:
    validate_bundle(bundle, manifest, key)
    mapping = validate_private_mapping(private_mapping, manifest, key)
    if not isinstance(document, dict):
        raise DistributionError("external response document must be an object")
    if document.get("response_version") != RESPONSE_VERSION:
        raise DistributionError("unexpected external-response version")
    for field in ("bundle_id", "distribution_id", "bundle_sha256"):
        if document.get(field) != manifest.get(field):
            raise DistributionError(f"response/bundle mismatch: {field}")
    origin = document.get("data_origin")
    if origin not in {"REAL_HUMAN", "SYNTHETIC_NON_HUMAN"}:
        raise DistributionError("invalid external-response data_origin")
    if origin == "SYNTHETIC_NON_HUMAN" and (not allow_synthetic or document.get("synthetic_fixture") is not True):
        raise DistributionError("synthetic external response is not allowed on the real-data path")
    if origin == "REAL_HUMAN" and document.get("synthetic_fixture") is True:
        raise DistributionError("REAL_HUMAN external response cannot be marked synthetic")
    adjudicator_id = document.get("adjudicator_id")
    if not isinstance(adjudicator_id, str) or not adjudicator_id.strip():
        raise DistributionError("adjudicator_id must be a non-empty pseudonym")
    rows = document.get("responses")
    if not isinstance(rows, list) or not rows or len(rows) > 24:
        raise DistributionError("external response must contain between 1 and 24 rows")
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    valid_internal = set(mapping.values())
    for row in rows:
        if not isinstance(row, dict):
            raise DistributionError("external response row must be an object")
        external_id = row.get("external_case_id")
        if external_id not in mapping:
            raise DistributionError(f"unknown external case ID: {external_id}")
        if external_id in seen:
            raise DistributionError(f"duplicate external case response: {external_id}")
        seen.add(external_id)
        internal = {
            "data_origin": origin,
            "adjudicator_id": adjudicator_id,
            "adjudication_case_id": mapping[external_id],
            "decision": row.get("decision"),
            "missing_information_codes": copy.deepcopy(row.get("missing_information_codes", [])),
            "confidence_0_to_100": row.get("confidence_0_to_100"),
            "rationale": row.get("rationale", ""),
            "prior_exposure": row.get("prior_exposure"),
            "conflict_of_interest": row.get("conflict_of_interest"),
        }
        if origin == "SYNTHETIC_NON_HUMAN":
            internal["synthetic_fixture"] = True
        try:
            validated = validate_adjudication_response(
                internal, valid_internal, allow_synthetic=allow_synthetic
            )
        except AdjudicationError as exc:
            raise DistributionError("external response failed Stage-007 validation") from exc
        normalized.append(validated)
    return {
        "data_origin": origin,
        "bundle_id": manifest["bundle_id"],
        "distribution_id": manifest["distribution_id"],
        "adjudicator_id": adjudicator_id,
        "submission_sha256": object_sha256(document),
        "normalized_responses": normalized,
    }


def new_intake_ledger(data_origin: str, key: bytes) -> dict[str, Any]:
    _validate_key(key)
    if data_origin not in {"REAL_HUMAN", "SYNTHETIC_NON_HUMAN"}:
        raise DistributionError("invalid ledger data origin")
    return {
        "ledger_version": LEDGER_VERSION,
        "data_origin": data_origin,
        "key_fingerprint": key_fingerprint(key),
        "events": [],
        "responses": [],
    }


def append_intake(
    ledger: dict[str, Any], normalized: dict[str, Any], key: bytes
) -> dict[str, Any]:
    _validate_key(key)
    verify_intake_ledger(ledger, key)
    if ledger.get("data_origin") != normalized.get("data_origin"):
        raise DistributionError("real and synthetic intake data cannot be mixed")
    out = copy.deepcopy(ledger)
    existing_pairs = {
        (row.get("adjudicator_id"), row.get("adjudication_case_id"))
        for row in out.get("responses", []) if isinstance(row, dict)
    }
    rows = copy.deepcopy(normalized.get("normalized_responses"))
    if not isinstance(rows, list) or not rows:
        raise DistributionError("normalized intake contains no responses")
    for row in rows:
        pair = (row.get("adjudicator_id"), row.get("adjudication_case_id"))
        if pair in existing_pairs:
            raise DistributionError(f"duplicate adjudicator/case intake: {pair}")
        existing_pairs.add(pair)
    start = len(out["responses"])
    response_sha = object_sha256(rows)
    previous_hmac = out["events"][-1]["receipt_hmac_sha256"] if out["events"] else None
    payload = {
        "receipt_index": len(out["events"]),
        "bundle_id": normalized["bundle_id"],
        "distribution_id": normalized["distribution_id"],
        "adjudicator_id": normalized["adjudicator_id"],
        "submission_sha256": normalized["submission_sha256"],
        "normalized_responses_sha256": response_sha,
        "response_start": start,
        "response_count": len(rows),
        "previous_receipt_hmac": previous_hmac,
    }
    event = dict(payload)
    event["receipt_hmac_sha256"] = _hmac_hex(key, canonical_bytes(payload))
    out["events"].append(event)
    out["responses"].extend(rows)
    verify_intake_ledger(out, key)
    return out


def verify_intake_ledger(ledger: Any, key: bytes) -> None:
    _validate_key(key)
    if not isinstance(ledger, dict) or ledger.get("ledger_version") != LEDGER_VERSION:
        raise DistributionError("invalid intake ledger")
    if ledger.get("key_fingerprint") != key_fingerprint(key):
        raise DistributionError("intake ledger key fingerprint mismatch")
    origin = ledger.get("data_origin")
    if origin not in {"REAL_HUMAN", "SYNTHETIC_NON_HUMAN"}:
        raise DistributionError("invalid intake ledger origin")
    events = ledger.get("events")
    responses = ledger.get("responses")
    if not isinstance(events, list) or not isinstance(responses, list):
        raise DistributionError("intake ledger arrays are missing")
    cursor = 0
    previous_hmac = None
    pairs: set[tuple[Any, Any]] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise DistributionError("invalid intake receipt")
        payload = {k: copy.deepcopy(v) for k, v in event.items() if k != "receipt_hmac_sha256"}
        if event.get("receipt_index") != index or event.get("previous_receipt_hmac") != previous_hmac:
            raise DistributionError("intake receipt chain mismatch")
        if event.get("response_start") != cursor or not isinstance(event.get("response_count"), int) or event["response_count"] <= 0:
            raise DistributionError("intake receipt range mismatch")
        end = cursor + event["response_count"]
        rows = responses[cursor:end]
        if len(rows) != event["response_count"] or object_sha256(rows) != event.get("normalized_responses_sha256"):
            raise DistributionError("post-intake response tampering detected")
        expected_hmac = _hmac_hex(key, canonical_bytes(payload))
        actual_hmac = event.get("receipt_hmac_sha256")
        if not isinstance(actual_hmac, str) or not hmac.compare_digest(actual_hmac, expected_hmac):
            raise DistributionError("intake receipt HMAC mismatch")
        for row in rows:
            if not isinstance(row, dict) or row.get("data_origin") != origin:
                raise DistributionError("intake response origin mismatch")
            pair = (row.get("adjudicator_id"), row.get("adjudication_case_id"))
            if pair in pairs:
                raise DistributionError("duplicate adjudicator/case pair in intake ledger")
            pairs.add(pair)
        previous_hmac = actual_hmac
        cursor = end
    if cursor != len(responses):
        raise DistributionError("unreceipted responses found in intake ledger")
