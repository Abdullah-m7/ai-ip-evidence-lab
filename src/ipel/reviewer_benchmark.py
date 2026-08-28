"""Blinded reviewer-utility benchmark machinery for IPEL Stage 006.

The benchmark distinguishes evidence readiness from legal compliance. Reviewer-facing
packets never contain answer labels. Baseline and IPEL representations are rendered
from the same latent fact map; IPEL may expose empty schema slots as structural cues,
but it may not add underlying facts.
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

READY = "READY_FOR_LEGAL_EVALUATION"
NOT_READY = "NOT_READY_FOR_LEGAL_EVALUATION"
DECISIONS = {"READY", "NOT_READY", "UNSURE"}
PRESENTATIONS = {"BASELINE", "IPEL"}

MISSING_FACT_CODEBOOK: dict[str, str] = {
    "WORK_TYPE": "Type/category of the work is not sufficiently recorded.",
    "WORK_SOURCE": "Source from which the work was obtained is not sufficiently recorded.",
    "USE_PURPOSE": "Purpose of the AI-development use is not sufficiently recorded.",
    "USE_DATE": "Date of the AI-development use is not sufficiently recorded.",
    "PUBLICATION": "Whether the work was lawfully published is unresolved or unsupported.",
    "ACQUISITION": "Whether the relevant copy was lawfully acquired is unresolved or unsupported.",
    "NECESSITY": "Necessity/proportionality of the copying or analysis is unresolved.",
    "PROHIBITED_USE_STATUS": "Republication/distribution/direct-exploitation status is unresolved.",
    "COMMERCIAL_EFFECT": "Commercial materiality or effect on normal exploitation is unresolved.",
    "AUTHOR_INTERESTS": "Effect on legitimate author interests lacks a sufficient assessment or basis.",
    "OUTPUT_CONTEXT": "Final-output use / transformation / permission context is unresolved.",
    "INDEPENDENT_ELEMENTS": "Independently protected elements are unresolved or lack assessment basis.",
    "USE_EVENT_EVIDENCE": "Contemporaneous evidence of the use event is not recorded.",
}

# Every fact path shown in either presentation. Missing values are structural slots in
# IPEL, not extra facts. Baseline includes only available facts.
FIELD_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Work", (
        "work.title", "work.type", "work.source", "work.sha256",
        "work.publication_status", "work.acquisition_status", "work.acquisition_method",
    )),
    ("AI-development use", (
        "use.purpose", "use.date", "use.extent_description", "use.necessity_status",
        "use.republication", "use.distribution", "use.direct_commercial_exploitation",
        "use.purely_commercial_context", "use.materiality_to_work", "use.normal_exploitation_impact",
    )),
    ("Rights / market assessment", (
        "rights_context.legitimate_interests_prejudice",
        "rights_context.exploitation_opportunity_effect",
        "rights_context.independent_elements_status",
        "rights_context.impact_assessment_basis",
        "rights_context.independent_elements_basis",
    )),
    ("Output context", (
        "output_context.transformed", "output_context.republished", "output_context.made_public",
        "output_context.included_in_final_product", "output_context.inclusion_necessary",
        "output_context.permission_status", "output_context.public_domain_status",
    )),
    ("Evidence references", (
        "evidence.publication", "evidence.acquisition", "evidence.use_event",
    )),
)

FIELD_LABELS: dict[str, str] = {
    path: path.split(".")[-1].replace("_", " ").title()
    for _, paths in FIELD_GROUPS for path in paths
}
FIELD_LABELS.update({
    "work.sha256": "Content SHA-256",
    "rights_context.legitimate_interests_prejudice": "Legitimate-interests prejudice",
    "rights_context.exploitation_opportunity_effect": "Exploitation-opportunity effect",
    "rights_context.impact_assessment_basis": "Impact-assessment basis",
    "rights_context.independent_elements_basis": "Independent-elements assessment basis",
})

TITLE_VARIANTS = (
    "Synthetic Maintenance Handbook", "Synthetic Policy Guide", "Synthetic Technical Note",
    "Synthetic Safety Manual", "Synthetic Training Memo", "Synthetic Reference Chapter",
)
ACQUISITION_VARIANTS = (
    "licensed repository copy", "purchased digital copy", "institutional subscription copy",
    "author-distributed licensed copy", "licensed archive copy", "documented vendor copy",
)
EXTENT_VARIANTS = (
    "a short machine-readable excerpt required for the declared evaluation",
    "selected paragraphs needed for the declared model-development test",
    "a bounded excerpt used only for the stated analysis task",
    "a small portion necessary for the documented evaluation run",
)


class BenchmarkError(ValueError):
    pass


@dataclass(frozen=True)
class PacketManifestEntry:
    packet_id: str
    form: str
    case_id: str
    presentation: str
    stratum: str
    readiness: str
    missing_fact_codes: list[str]
    fact_digest: str
    machine_gate_outcome: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _get(obj: dict[str, Any], dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _set(obj: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = obj
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _delete(obj: dict[str, Any], dotted: str) -> None:
    parts = dotted.split(".")
    cur: Any = obj
    for part in parts[:-1]:
        if not isinstance(cur, dict) or part not in cur:
            return
        cur = cur[part]
    if isinstance(cur, dict):
        cur.pop(parts[-1], None)


def apply_mutations(record: dict[str, Any], mutations: Iterable[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    for mutation in mutations:
        op = mutation.get("op")
        path = mutation.get("path")
        if not isinstance(path, str) or not path:
            raise BenchmarkError("mutation path must be a non-empty string")
        if op == "set":
            _set(result, path, copy.deepcopy(mutation.get("value")))
        elif op == "delete":
            _delete(result, path)
        else:
            raise BenchmarkError(f"unsupported mutation operation: {op}")
    return result


def decorate_record(record: dict[str, Any], case_id: str, index: int) -> dict[str, Any]:
    """Add deterministic nuisance variation before the case-defining mutation."""
    result = copy.deepcopy(record)
    token = hashlib.sha256(case_id.encode("utf-8")).hexdigest()[:10]
    result["record_id"] = f"latent-{token}"
    result["work"]["title"] = f"{TITLE_VARIANTS[index % len(TITLE_VARIANTS)]} {token[:4].upper()}"
    result["work"]["source"] = f"https://synthetic.example/{token}/source"
    result["work"]["acquisition_method"] = ACQUISITION_VARIANTS[index % len(ACQUISITION_VARIANTS)]
    result["use"]["date"] = f"2026-0{(index % 8) + 1}-{((index * 3) % 27) + 1:02d}"
    result["use"]["extent_description"] = EXTENT_VARIANTS[index % len(EXTENT_VARIANTS)]
    result["evidence"]["publication"] = [f"evidence://publication/{token}"]
    result["evidence"]["acquisition"] = [f"evidence://acquisition/{token}"]
    result["evidence"]["use_event"] = [f"evidence://use-event/{token}"]
    result["rights_context"]["impact_assessment_basis"] = [f"evidence://impact/{token}"]
    result["rights_context"]["independent_elements_basis"] = [f"evidence://independent-elements/{token}"]
    return result


def available_facts(record: dict[str, Any]) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    for _, paths in FIELD_GROUPS:
        for path in paths:
            value = _get(record, path)
            if value is not None:
                facts[path] = copy.deepcopy(value)
    return facts


def fact_digest(facts: dict[str, Any]) -> str:
    raw = json.dumps(facts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _human_value(value: Any) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) if value else "None recorded"
    return str(value).replace("_", " ")


def render_baseline(facts: dict[str, Any]) -> dict[str, Any]:
    """Strong narrative/dataset-card-style baseline using all available facts."""
    sections: list[dict[str, Any]] = []
    represented: list[str] = []
    for title, paths in FIELD_GROUPS:
        items: list[str] = []
        for path in paths:
            if path not in facts:
                continue
            represented.append(path)
            items.append(f"{FIELD_LABELS[path]}: {_human_value(facts[path])}")
        sections.append({"heading": title, "items": items})
    return {
        "format_name": "Provenance review note",
        "sections": sections,
        "represented_fact_paths": sorted(represented),
    }


def render_ipel(facts: dict[str, Any]) -> dict[str, Any]:
    """IPEL structured view. Empty slots are cues, not additional latent facts."""
    sections: list[dict[str, Any]] = []
    represented: list[str] = []
    for title, paths in FIELD_GROUPS:
        rows: list[dict[str, Any]] = []
        for path in paths:
            if path in facts:
                represented.append(path)
                value: Any = copy.deepcopy(facts[path])
                status = "RECORDED"
            else:
                value = "NOT_RECORDED"
                status = "MISSING_SLOT"
            rows.append({"field": FIELD_LABELS[path], "value": value, "slot_status": status})
        sections.append({"heading": title, "rows": rows})
    return {
        "format_name": "Structured evidence record",
        "sections": sections,
        "represented_fact_paths": sorted(represented),
    }


def response_instructions() -> dict[str, Any]:
    return {
        "task": (
            "Decide only whether the available record is sufficiently complete and evidenced for a qualified "
            "legal reviewer to evaluate the scoped copyright questions. Do not decide whether the conduct is lawful."
        ),
        "decision_options": ["READY", "NOT_READY", "UNSURE"],
        "missing_fact_options": [
            {"code": code, "description": description}
            for code, description in MISSING_FACT_CODEBOOK.items()
        ],
        "response_fields": ["decision", "missing_information_codes", "confidence_0_to_100", "assessment_seconds"],
    }


def _packet_id(seed: int, form: str, case_id: str, presentation: str) -> str:
    payload = f"{seed}|{form}|{case_id}|{presentation}".encode("utf-8")
    return "PKT-" + hashlib.sha256(payload).hexdigest()[:12].upper()


def assign_presentations(cases: list[dict[str, Any]], form: str) -> dict[str, str]:
    """Within each stratum×readiness cell, alternate 3/3 and swap in Form B."""
    if form not in {"A", "B"}:
        raise BenchmarkError("form must be A or B")
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[(case["stratum"], case["readiness"])].append(case)
    assignments: dict[str, str] = {}
    for _, group in sorted(grouped.items()):
        for i, case in enumerate(sorted(group, key=lambda item: item["case_id"])):
            baseline_in_a = i % 2 == 0
            baseline = baseline_in_a if form == "A" else not baseline_in_a
            assignments[case["case_id"]] = "BASELINE" if baseline else "IPEL"
    return assignments


def build_case_record(base_record: dict[str, Any], case: dict[str, Any], index: int) -> dict[str, Any]:
    decorated = decorate_record(base_record, case["case_id"], index)
    return apply_mutations(decorated, case.get("mutations", []))


def build_form(
    spec: dict[str, Any], base_record: dict[str, Any], form: str
) -> tuple[dict[str, Any], list[PacketManifestEntry], dict[str, dict[str, Any]]]:
    from src.ipel.validator import evaluate

    seed = int(spec["seed"])
    cases = list(spec["cases"])
    assignments = assign_presentations(cases, form)
    packets: list[dict[str, Any]] = []
    manifest_entries: list[PacketManifestEntry] = []
    latent_records: dict[str, dict[str, Any]] = {}

    for index, case in enumerate(cases):
        case_id = case["case_id"]
        record = build_case_record(base_record, case, index)
        latent_records[case_id] = record
        facts = available_facts(record)
        digest = fact_digest(facts)
        presentation = assignments[case_id]
        rendered = render_baseline(facts) if presentation == "BASELINE" else render_ipel(facts)
        represented = rendered.pop("represented_fact_paths")
        if represented != sorted(facts):
            raise BenchmarkError(f"factual parity failure while rendering {case_id}/{presentation}")
        packet_id = _packet_id(seed, form, case_id, presentation)
        packets.append({
            "packet_id": packet_id,
            "material": rendered,
            "instructions": response_instructions(),
        })
        manifest_entries.append(PacketManifestEntry(
            packet_id=packet_id,
            form=form,
            case_id=case_id,
            presentation=presentation,
            stratum=case["stratum"],
            readiness=case["readiness"],
            missing_fact_codes=list(case["missing_fact_codes"]),
            fact_digest=digest,
            machine_gate_outcome=evaluate(record).outcome,
        ))

    rng = random.Random(seed + (1000 if form == "B" else 0))
    rng.shuffle(packets)
    return {
        "benchmark_version": spec["benchmark_version"],
        "form": form,
        "packet_count": len(packets),
        "packets": packets,
    }, manifest_entries, latent_records


def audit_benchmark(
    spec: dict[str, Any], forms: dict[str, dict[str, Any]], manifests: list[PacketManifestEntry],
    latent_by_form: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    cases = list(spec["cases"])
    case_ids = {case["case_id"] for case in cases}
    by_form_case: dict[tuple[str, str], PacketManifestEntry] = {
        (entry.form, entry.case_id): entry for entry in manifests
    }

    parity: dict[str, bool] = {}
    latent_identity: dict[str, bool] = {}
    counterbalanced: dict[str, bool] = {}
    for case_id in sorted(case_ids):
        a = by_form_case[("A", case_id)]
        b = by_form_case[("B", case_id)]
        parity[case_id] = a.fact_digest == b.fact_digest
        latent_identity[case_id] = latent_by_form["A"][case_id] == latent_by_form["B"][case_id]
        counterbalanced[case_id] = a.presentation != b.presentation

    visible_text = json.dumps(forms, ensure_ascii=False)
    forbidden_labels = [READY, NOT_READY, "judgment_sensitive", "objective", '"case_id"', '"missing_fact_codes"']
    leakage_hits = [token for token in forbidden_labels if token in visible_text]

    cell_counts = Counter((entry.stratum, entry.readiness, entry.presentation) for entry in manifests if entry.form == "A")
    readiness_counts = Counter(entry.readiness for entry in manifests if entry.form == "A")
    stratum_counts = Counter(entry.stratum for entry in manifests if entry.form == "A")
    format_counts = Counter(entry.presentation for entry in manifests if entry.form == "A")

    ready_machine_fail = [
        entry.case_id for entry in manifests
        if entry.form == "A" and entry.readiness == READY and entry.machine_gate_outcome == "FAIL_EVIDENCE_GATE"
    ]
    benign_single_missing = [
        case["case_id"] for case in cases
        if case["readiness"] == NOT_READY and len(case["missing_fact_codes"]) == 1
        and case["case_id"] in {"OBJ-N01", "OBJ-N02", "OBJ-N03"}
    ]

    form_packet_ids = {
        form: [packet["packet_id"] for packet in forms[form]["packets"]]
        for form in ("A", "B")
    }
    duplicate_packet_ids = len(set(form_packet_ids["A"] + form_packet_ids["B"])) != 48

    acceptance = {
        "factual_parity_100_percent": all(parity.values()) and len(parity) == len(case_ids),
        "latent_records_identical_across_forms": all(latent_identity.values()) and len(latent_identity) == len(case_ids),
        "counterbalanced_every_case": all(counterbalanced.values()) and len(counterbalanced) == len(case_ids),
        "no_answer_label_leakage": not leakage_hits,
        "unique_packet_ids": not duplicate_packet_ids,
        "balanced_readiness": readiness_counts == Counter({READY: 12, NOT_READY: 12}),
        "balanced_strata": stratum_counts == Counter({"objective": 12, "judgment_sensitive": 12}),
        "balanced_presentations": format_counts == Counter({"BASELINE": 12, "IPEL": 12}),
        "three_per_cell_presentation": all(value == 3 for value in cell_counts.values()) and len(cell_counts) == 8,
        "readiness_not_compliance_construct_proven": bool(ready_machine_fail),
        "benign_single_missing_cases_present": bool(benign_single_missing),
    }

    return {
        "benchmark_version": spec["benchmark_version"],
        "case_count": len(cases),
        "form_packet_counts": {form: forms[form]["packet_count"] for form in ("A", "B")},
        "factual_parity_by_case": parity,
        "latent_record_identity_by_case": latent_identity,
        "counterbalanced_by_case": counterbalanced,
        "leakage_hits": leakage_hits,
        "form_a_readiness_counts": dict(readiness_counts),
        "form_a_stratum_counts": dict(stratum_counts),
        "form_a_presentation_counts": dict(format_counts),
        "form_a_cell_counts": {"|".join(key): value for key, value in sorted(cell_counts.items())},
        "ready_cases_with_machine_fail": sorted(set(ready_machine_fail)),
        "benign_single_missing_cases": sorted(benign_single_missing),
        "acceptance": acceptance,
        "all_acceptance_gates_pass": all(acceptance.values()),
    }


def score_responses(
    responses: list[dict[str, Any]], answer_key: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for response in responses:
        packet_id = response.get("packet_id")
        if packet_id not in answer_key:
            raise BenchmarkError(f"unknown packet_id: {packet_id}")
        decision = response.get("decision")
        if decision not in DECISIONS:
            raise BenchmarkError(f"invalid decision for {packet_id}: {decision}")
        predicted_missing = response.get("missing_information_codes", [])
        if not isinstance(predicted_missing, list) or any(code not in MISSING_FACT_CODEBOOK for code in predicted_missing):
            raise BenchmarkError(f"invalid missing_information_codes for {packet_id}")
        predicted = set(predicted_missing)
        truth = answer_key[packet_id]
        expected = set(truth["missing_fact_codes"])
        expected_decision = "READY" if truth["readiness"] == READY else "NOT_READY"
        tp = len(predicted & expected)
        fp = len(predicted - expected)
        fn = len(expected - predicted)
        recall = tp / len(expected) if expected else None
        precision = tp / (tp + fp) if (tp + fp) else (1.0 if not expected else None)
        rows.append({
            "packet_id": packet_id,
            "presentation": truth["presentation"],
            "stratum": truth["stratum"],
            "truth_readiness": truth["readiness"],
            "decision": decision,
            "readiness_correct": decision == expected_decision,
            "uncertain": decision == "UNSURE",
            "false_ready": truth["readiness"] == NOT_READY and decision == "READY",
            "false_not_ready": truth["readiness"] == READY and decision == "NOT_READY",
            "missing_tp": tp,
            "missing_fp": fp,
            "missing_fn": fn,
            "missing_recall": recall,
            "missing_precision": precision,
            "assessment_seconds": response.get("assessment_seconds"),
        })

    def summarize(group: list[dict[str, Any]]) -> dict[str, Any]:
        if not group:
            return {}
        recall_rows = [row["missing_recall"] for row in group if row["missing_recall"] is not None]
        precision_rows = [row["missing_precision"] for row in group if row["missing_precision"] is not None]
        times = [row["assessment_seconds"] for row in group if isinstance(row["assessment_seconds"], (int, float))]
        return {
            "n": len(group),
            "readiness_accuracy": sum(row["readiness_correct"] for row in group) / len(group),
            "false_ready_rate": sum(row["false_ready"] for row in group) / max(1, sum(row["truth_readiness"] == NOT_READY for row in group)),
            "uncertainty_rate": sum(row["uncertain"] for row in group) / len(group),
            "mean_missing_fact_recall_not_ready": sum(recall_rows) / len(recall_rows) if recall_rows else None,
            "mean_missing_fact_precision": sum(precision_rows) / len(precision_rows) if precision_rows else None,
            "mean_assessment_seconds": sum(times) / len(times) if times else None,
        }

    by_presentation = {
        presentation: summarize([row for row in rows if row["presentation"] == presentation])
        for presentation in sorted(PRESENTATIONS)
    }
    by_stratum = {
        stratum: summarize([row for row in rows if row["stratum"] == stratum])
        for stratum in sorted({row["stratum"] for row in rows})
    }
    return {
        "n": len(rows),
        "overall": summarize(rows),
        "by_presentation": by_presentation,
        "by_stratum": by_stratum,
        "rows": rows,
    }


def decision_matrix(
    reviewer_responses: dict[str, list[dict[str, Any]]], answer_key: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Prepare per-packet decision counts and pairwise agreement for later H2 analysis."""
    per_packet: dict[str, dict[str, str]] = defaultdict(dict)
    for reviewer_id, responses in reviewer_responses.items():
        for response in responses:
            packet_id = response.get("packet_id")
            if packet_id not in answer_key:
                raise BenchmarkError(f"unknown packet_id: {packet_id}")
            decision = response.get("decision")
            if decision not in DECISIONS:
                raise BenchmarkError(f"invalid decision: {decision}")
            per_packet[packet_id][reviewer_id] = decision

    reviewers = sorted(reviewer_responses)
    pairwise: list[dict[str, Any]] = []
    for i, left in enumerate(reviewers):
        for right in reviewers[i + 1:]:
            shared = [
                packet for packet, values in per_packet.items()
                if left in values and right in values
            ]
            agreement_count = sum(per_packet[p][left] == per_packet[p][right] for p in shared)
            pairwise.append({
                "reviewer_a": left,
                "reviewer_b": right,
                "shared_packets": len(shared),
                "percent_agreement": agreement_count / len(shared) if shared else None,
            })
    matrix = {
        packet_id: {
            "presentation": answer_key[packet_id]["presentation"],
            "stratum": answer_key[packet_id]["stratum"],
            "decisions": dict(sorted(values.items())),
            "counts": dict(Counter(values.values())),
        }
        for packet_id, values in sorted(per_packet.items())
    }
    return {"reviewers": reviewers, "pairwise_agreement": pairwise, "matrix": matrix}
