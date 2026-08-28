"""Stage 007 independent-adjudication primitives.

This module creates neutral case packets and aggregates real or explicitly synthetic
adjudication responses. It never fabricates human judgments and never overwrites the
Stage-006 author labels.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from src.ipel.reviewer_benchmark import (
    FIELD_GROUPS,
    FIELD_LABELS,
    MISSING_FACT_CODEBOOK,
    available_facts,
    build_case_record,
    fact_digest,
)

DECISIONS = {"READY", "NOT_READY", "UNSURE"}
DATA_ORIGINS = {"REAL_HUMAN", "SYNTHETIC_NON_HUMAN"}
DEFAULT_MIN_ADJUDICATORS = 3
DEFAULT_CONSENSUS_FRACTION = 2 / 3


class AdjudicationError(ValueError):
    pass


@dataclass(frozen=True)
class ConsensusResult:
    adjudication_case_id: str
    status: str
    decision: str | None
    missing_information_codes: list[str]
    eligible_adjudicators: int
    excluded_adjudicators: int
    decision_counts: dict[str, int]
    decision_fraction: float | None
    unresolved_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _human_value(value: Any) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) if value else "None recorded"
    return str(value).replace("_", " ")


def pseudonymous_case_id(seed: int, stage006_case_id: str) -> str:
    payload = f"stage007|{seed}|{stage006_case_id}".encode("utf-8")
    return "ADJ-" + hashlib.sha256(payload).hexdigest()[:12].upper()


def render_neutral_fact_sheet(facts: dict[str, Any]) -> dict[str, Any]:
    """Render only available facts; no IPEL slots, Stage-006 labels, or condition cues."""
    sections: list[dict[str, Any]] = []
    represented: list[str] = []
    for title, paths in FIELD_GROUPS:
        items: list[dict[str, str]] = []
        for path in paths:
            if path not in facts:
                continue
            represented.append(path)
            items.append({"fact": FIELD_LABELS[path], "value": _human_value(facts[path])})
        sections.append({"heading": title, "facts": items})
    return {
        "format_name": "Neutral factual inventory",
        "sections": sections,
        "represented_fact_paths": sorted(represented),
    }


def adjudication_instructions() -> dict[str, Any]:
    return {
        "construct": (
            "Classify only whether the available record is sufficiently complete and evidenced "
            "for a qualified legal reviewer to evaluate the scoped copyright questions. "
            "Do not decide whether the conduct is lawful."
        ),
        "decision_options": ["READY", "NOT_READY", "UNSURE"],
        "missing_information_options": [
            {"code": code, "description": description}
            for code, description in MISSING_FACT_CODEBOOK.items()
        ],
        "blinding_instruction": (
            "This is procedural blinding, not cryptographic secrecy. Do not consult the project repository, "
            "Stage-006 case materials, answer keys, or other project artifacts while adjudicating. If you "
            "have previously seen the underlying cases or labels, set prior_exposure=true."
        ),
        "response_fields": [
            "adjudicator_id", "adjudication_case_id", "decision",
            "missing_information_codes", "confidence_0_to_100", "rationale",
            "prior_exposure", "conflict_of_interest",
        ],
    }


def build_adjudication_packet(
    spec: dict[str, Any], base_record: dict[str, Any], *, seed: int = 20260829
) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = list(spec.get("cases", []))
    if not cases:
        raise AdjudicationError("Stage-006 case spec has no cases")
    packets: list[dict[str, Any]] = []
    provenance: dict[str, Any] = {}
    for index, case in enumerate(cases):
        stage006_id = case["case_id"]
        record = build_case_record(base_record, case, index)
        facts = available_facts(record)
        pseudo = pseudonymous_case_id(seed, stage006_id)
        rendered = render_neutral_fact_sheet(facts)
        represented = rendered.pop("represented_fact_paths")
        if represented != sorted(facts):
            raise AdjudicationError(f"neutral-render parity failure: {stage006_id}")
        packets.append({
            "adjudication_case_id": pseudo,
            "material": rendered,
            "instructions": adjudication_instructions(),
        })
        provenance[pseudo] = {
            "stage006_case_id": stage006_id,
            "fact_digest": fact_digest(facts),
            "stage006_author_readiness": case["readiness"],
            "stage006_author_missing_fact_codes": list(case["missing_fact_codes"]),
            "stage006_stratum": case["stratum"],
        }
    rng = random.Random(seed)
    rng.shuffle(packets)
    packet = {
        "benchmark_version": "stage007-adjudication-v1",
        "seed": seed,
        "case_count": len(packets),
        "real_adjudication_collected": False,
        "packets": packets,
    }
    hidden = {
        "benchmark_version": "stage007-adjudication-v1",
        "warning": "HIDDEN PROVENANCE. Never provide this mapping to adjudicators.",
        "mapping": dict(sorted(provenance.items())),
    }
    return packet, hidden


def validate_adjudication_response(
    response: Any,
    valid_case_ids: set[str],
    *,
    allow_synthetic: bool = False,
) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise AdjudicationError("response must be an object")
    required = {
        "data_origin", "adjudicator_id", "adjudication_case_id", "decision",
        "missing_information_codes", "confidence_0_to_100", "prior_exposure",
        "conflict_of_interest",
    }
    missing = sorted(required - set(response))
    if missing:
        raise AdjudicationError(f"missing response fields: {missing}")
    origin = response["data_origin"]
    if origin not in DATA_ORIGINS:
        raise AdjudicationError("invalid data_origin")
    if origin == "SYNTHETIC_NON_HUMAN":
        if not allow_synthetic:
            raise AdjudicationError("synthetic adjudication not allowed in real-data path")
        if response.get("synthetic_fixture") is not True:
            raise AdjudicationError("synthetic response requires synthetic_fixture=true")
    elif response.get("synthetic_fixture") is True:
        raise AdjudicationError("REAL_HUMAN response cannot be marked synthetic_fixture")
    adjudicator_id = response["adjudicator_id"]
    if not isinstance(adjudicator_id, str) or not adjudicator_id.strip():
        raise AdjudicationError("adjudicator_id must be a non-empty pseudonym")
    case_id = response["adjudication_case_id"]
    if case_id not in valid_case_ids:
        raise AdjudicationError(f"unknown adjudication_case_id: {case_id}")
    if response["decision"] not in DECISIONS:
        raise AdjudicationError("invalid decision")
    codes = response["missing_information_codes"]
    if not isinstance(codes, list) or any(code not in MISSING_FACT_CODEBOOK for code in codes):
        raise AdjudicationError("invalid missing_information_codes")
    if len(codes) != len(set(codes)):
        raise AdjudicationError("duplicate missing-information code")
    confidence = response["confidence_0_to_100"]
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 100:
        raise AdjudicationError("confidence must be numeric in [0,100]")
    for flag in ("prior_exposure", "conflict_of_interest"):
        if not isinstance(response[flag], bool):
            raise AdjudicationError(f"{flag} must be boolean")
    rationale = response.get("rationale", "")
    if rationale is not None and not isinstance(rationale, str):
        raise AdjudicationError("rationale must be a string or null")
    return copy.deepcopy(response)


def validate_response_set(
    responses: Iterable[dict[str, Any]],
    valid_case_ids: set[str],
    *,
    allow_synthetic: bool = False,
) -> list[dict[str, Any]]:
    validated: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    origins: set[str] = set()
    for response in responses:
        item = validate_adjudication_response(response, valid_case_ids, allow_synthetic=allow_synthetic)
        key = (item["adjudicator_id"], item["adjudication_case_id"])
        if key in seen:
            raise AdjudicationError(f"duplicate adjudicator/case response: {key}")
        seen.add(key)
        origins.add(item["data_origin"])
        validated.append(item)
    if len(origins) > 1:
        raise AdjudicationError("real and synthetic adjudication data cannot be mixed")
    return validated


def aggregate_case(
    adjudication_case_id: str,
    responses: list[dict[str, Any]],
    *,
    min_adjudicators: int = DEFAULT_MIN_ADJUDICATORS,
    consensus_fraction: float = DEFAULT_CONSENSUS_FRACTION,
) -> ConsensusResult:
    adjudicator_ids = [r.get("adjudicator_id") for r in responses]
    if len(adjudicator_ids) != len(set(adjudicator_ids)):
        raise AdjudicationError("aggregate_case refuses duplicate adjudicator IDs")
    eligible = [r for r in responses if not r["prior_exposure"] and not r["conflict_of_interest"]]
    excluded = len(responses) - len(eligible)
    if len(eligible) < min_adjudicators:
        return ConsensusResult(
            adjudication_case_id, "UNRESOLVED", None, [], len(eligible), excluded,
            dict(Counter(r["decision"] for r in eligible)), None,
            "INSUFFICIENT_INDEPENDENT_ADJUDICATORS",
        )
    threshold = math.ceil(consensus_fraction * len(eligible) - 1e-12)
    counts = Counter(r["decision"] for r in eligible)
    candidate, count = counts.most_common(1)[0]
    if candidate == "UNSURE" or count < threshold:
        return ConsensusResult(
            adjudication_case_id, "UNRESOLVED", None, [], len(eligible), excluded,
            dict(counts), count / len(eligible), "DECISION_CONSENSUS_NOT_MET",
        )
    code_counts: Counter[str] = Counter()
    for response in eligible:
        code_counts.update(response["missing_information_codes"])
    consensus_codes = sorted(code for code, n in code_counts.items() if n >= threshold)
    if candidate == "READY" and consensus_codes:
        return ConsensusResult(
            adjudication_case_id, "UNRESOLVED", None, consensus_codes, len(eligible), excluded,
            dict(counts), count / len(eligible), "READY_WITH_CONSENSUS_MISSING_INFORMATION_CONFLICT",
        )
    if candidate == "NOT_READY" and not consensus_codes:
        return ConsensusResult(
            adjudication_case_id, "UNRESOLVED", None, [], len(eligible), excluded,
            dict(counts), count / len(eligible), "NOT_READY_WITHOUT_MISSING_INFORMATION_CONSENSUS",
        )
    return ConsensusResult(
        adjudication_case_id, "RESOLVED", candidate, consensus_codes, len(eligible), excluded,
        dict(counts), count / len(eligible), None,
    )


def aggregate_adjudication(
    responses: Iterable[dict[str, Any]],
    valid_case_ids: set[str],
    *,
    allow_synthetic: bool = False,
    min_adjudicators: int = DEFAULT_MIN_ADJUDICATORS,
    consensus_fraction: float = DEFAULT_CONSENSUS_FRACTION,
) -> dict[str, Any]:
    validated = validate_response_set(responses, valid_case_ids, allow_synthetic=allow_synthetic)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for response in validated:
        grouped[response["adjudication_case_id"]].append(response)
    results: dict[str, Any] = {}
    for case_id in sorted(valid_case_ids):
        results[case_id] = aggregate_case(
            case_id, grouped.get(case_id, []),
            min_adjudicators=min_adjudicators,
            consensus_fraction=consensus_fraction,
        ).to_dict()
    resolved = sum(item["status"] == "RESOLVED" for item in results.values())
    origin = validated[0]["data_origin"] if validated else None
    return {
        "data_origin": origin,
        "case_count": len(valid_case_ids),
        "resolved_cases": resolved,
        "unresolved_cases": len(valid_case_ids) - resolved,
        "all_cases_resolved": resolved == len(valid_case_ids),
        "min_adjudicators": min_adjudicators,
        "consensus_fraction": consensus_fraction,
        "cases": results,
    }
