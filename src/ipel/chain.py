"""Tamper-evident event chaining for IPEL Stage 002.

The chain proves only integrity relative to a known checkpoint. It does not prove
that an event's claims are true, that an actor was authorized, or that a legal
condition was satisfied.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from typing import Any, Iterable

EVENT_VERSION = "ipel-event-v1"
CHECKPOINT_VERSION = "ipel-checkpoint-v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ChainFinding:
    code: str
    message: str
    sequence: int | None = None


@dataclass(frozen=True)
class VerificationResult:
    integrity_verified: bool
    boundary_verified: bool
    claim_truth_verified: bool
    findings: list[ChainFinding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "integrity_verified": self.integrity_verified,
            "boundary_verified": self.boundary_verified,
            "claim_truth_verified": self.claim_truth_verified,
            "findings": [asdict(item) for item in self.findings],
        }


def canonical_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for hashing.

    Stage 002 intentionally uses a narrow JSON canonicalization profile rather
    than claiming compatibility with JCS/RFC 8785. Floats are disallowed so
    platform-specific number normalization cannot silently change commitments.
    """
    _reject_floats(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _reject_floats(value: Any) -> None:
    if isinstance(value, float):
        raise TypeError("floats are not allowed in Stage-002 canonical records")
    if isinstance(value, dict):
        for item in value.values():
            _reject_floats(item)
    elif isinstance(value, list):
        for item in value:
            _reject_floats(item)


def _hash_event_body(event: dict[str, Any]) -> str:
    body = {k: v for k, v in event.items() if k != "event_hash"}
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def build_chain(chain_id: str, event_inputs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(chain_id, str) or not chain_id.strip():
        raise ValueError("chain_id must be a non-empty string")

    events: list[dict[str, Any]] = []
    previous_hash: str | None = None
    for sequence, raw in enumerate(event_inputs):
        if not isinstance(raw, dict):
            raise TypeError("each event input must be an object")
        forbidden = {"version", "chain_id", "sequence", "previous_hash", "event_hash"} & set(raw)
        if forbidden:
            raise ValueError(f"event input contains chain-controlled fields: {sorted(forbidden)}")
        event = copy.deepcopy(raw)
        _validate_semantic_core(event)
        event.update(
            {
                "version": EVENT_VERSION,
                "chain_id": chain_id,
                "sequence": sequence,
                "previous_hash": previous_hash,
            }
        )
        event["event_hash"] = _hash_event_body(event)
        events.append(event)
        previous_hash = event["event_hash"]
    return events


def make_checkpoint(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        raise ValueError("cannot checkpoint an empty chain")
    chain_id = events[0].get("chain_id")
    result = verify_chain(events)
    if not result.integrity_verified:
        raise ValueError("cannot checkpoint an invalid chain")
    return {
        "version": CHECKPOINT_VERSION,
        "chain_id": chain_id,
        "event_count": len(events),
        "head_hash": events[-1]["event_hash"],
    }


def verify_chain(
    events: list[dict[str, Any]], checkpoint: dict[str, Any] | None = None
) -> VerificationResult:
    findings: list[ChainFinding] = []
    if not isinstance(events, list) or not events:
        return VerificationResult(False, False, False, [ChainFinding("EMPTY_CHAIN", "Chain must contain at least one event.")])

    expected_chain_id = events[0].get("chain_id") if isinstance(events[0], dict) else None
    previous_hash: str | None = None

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            findings.append(ChainFinding("EVENT_NOT_OBJECT", "Event is not a JSON object.", index))
            continue
        if event.get("version") != EVENT_VERSION:
            findings.append(ChainFinding("VERSION_MISMATCH", "Unexpected event version.", index))
        if event.get("chain_id") != expected_chain_id:
            findings.append(ChainFinding("CHAIN_ID_MISMATCH", "Event changed chain identity.", index))
        if event.get("sequence") != index:
            findings.append(ChainFinding("SEQUENCE_MISMATCH", f"Expected sequence {index}.", index))
        if event.get("previous_hash") != previous_hash:
            findings.append(ChainFinding("PREVIOUS_HASH_MISMATCH", "Previous-event binding is invalid.", index))

        claimed_hash = event.get("event_hash")
        if not isinstance(claimed_hash, str) or not HEX64.fullmatch(claimed_hash):
            findings.append(ChainFinding("INVALID_EVENT_HASH", "event_hash must be lowercase SHA-256 hex.", index))
        else:
            try:
                calculated = _hash_event_body(event)
            except (TypeError, ValueError) as exc:
                findings.append(ChainFinding("CANONICALIZATION_ERROR", str(exc), index))
            else:
                if calculated != claimed_hash:
                    findings.append(ChainFinding("EVENT_HASH_MISMATCH", "Event content no longer matches its hash.", index))

        try:
            _validate_semantic_core(event)
        except (TypeError, ValueError) as exc:
            findings.append(ChainFinding("EVENT_CONTRACT_ERROR", str(exc), index))
        previous_hash = claimed_hash if isinstance(claimed_hash, str) else None

    boundary_verified = False
    if checkpoint is not None:
        if not isinstance(checkpoint, dict):
            findings.append(ChainFinding("CHECKPOINT_CONTRACT_ERROR", "Checkpoint must be a JSON object."))
            return VerificationResult(False, False, False, findings)
        if checkpoint.get("version") != CHECKPOINT_VERSION:
            findings.append(ChainFinding("CHECKPOINT_VERSION_MISMATCH", "Unexpected checkpoint version."))
        if checkpoint.get("chain_id") != expected_chain_id:
            findings.append(ChainFinding("CHECKPOINT_CHAIN_MISMATCH", "Checkpoint belongs to a different chain."))
        if checkpoint.get("event_count") != len(events):
            findings.append(ChainFinding("CHECKPOINT_COUNT_MISMATCH", "Event count differs from checkpoint."))
        observed_head = events[-1].get("event_hash") if isinstance(events[-1], dict) else None
        if checkpoint.get("head_hash") != observed_head:
            findings.append(ChainFinding("CHECKPOINT_HEAD_MISMATCH", "Chain head differs from checkpoint."))
        boundary_verified = not any(f.code.startswith("CHECKPOINT_") for f in findings)

    return VerificationResult(
        integrity_verified=not findings,
        boundary_verified=boundary_verified,
        claim_truth_verified=False,
        findings=findings,
    )


def _validate_semantic_core(event: dict[str, Any]) -> None:
    required_strings = ("event_id", "event_type", "occurred_at")
    for field in required_strings:
        if not isinstance(event.get(field), str) or not event[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    actor = event.get("actor")
    if not isinstance(actor, dict) or not isinstance(actor.get("id"), str) or not actor["id"].strip():
        raise ValueError("actor.id must be a non-empty string")
    if not isinstance(event.get("payload"), dict):
        raise ValueError("payload must be an object")
    refs = event.get("evidence_refs")
    if not isinstance(refs, list):
        raise ValueError("evidence_refs must be an array")
    for ref in refs:
        if not isinstance(ref, dict):
            raise ValueError("each evidence reference must be an object")
        digest = ref.get("sha256")
        if digest is not None and (not isinstance(digest, str) or not HEX64.fullmatch(digest)):
            raise ValueError("evidence_refs[].sha256 must be lowercase SHA-256 hex")
