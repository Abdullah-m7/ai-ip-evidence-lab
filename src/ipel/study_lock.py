"""Stage 007 preregistration/freeze-manifest state machine."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

LOCK_STATES = {
    "PRE_ADJUDICATION_LOCK",
    "POST_ADJUDICATION_LOCK",
    "PRE_PRIMARY_STUDY_LOCK",
}

PRE_ADJUDICATION_PATHS = (
    "benchmarks/stage006/case_spec.json",
    "benchmarks/stage006/generated/form_a.json",
    "benchmarks/stage006/generated/form_b.json",
    "src/ipel/reviewer_benchmark.py",
    "docs/STAGE_006_PREREGISTRATION.md",
    "benchmarks/stage007/generated/adjudication_packet.json",
    "benchmarks/stage007/generated/hidden_case_map.json",
    "schemas/stage007-adjudication-response.schema.json",
    "src/ipel/adjudication.py",
    "experiments/stage007_build_preparation.py",
    "experiments/stage007_power_simulation.py",
    "benchmarks/stage007/generated/power_design_grid.json",
    "docs/STAGE_007_ADJUDICATION_PROTOCOL.md",
    "docs/STAGE_007_STUDY_LOCK_PROTOCOL.md",
    "src/ipel/study_lock.py",
)


class StudyLockError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_paths(root: Path, paths: tuple[str, ...]) -> dict[str, str]:
    out: dict[str, str] = {}
    for relative in paths:
        path = root / relative
        if not path.is_file():
            raise StudyLockError(f"required lock input missing: {relative}")
        out[relative] = sha256_file(path)
    return dict(sorted(out.items()))



def _repo_relative(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError as exc:
        raise StudyLockError("lock inputs must live inside the repository") from exc


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise StudyLockError(f"cannot read JSON: {path}") from exc


def validate_real_adjudication_summary(summary: Any) -> None:
    if not isinstance(summary, dict):
        raise StudyLockError("real adjudication summary must be an object")
    if summary.get("data_origin") != "REAL_HUMAN":
        raise StudyLockError("POST_ADJUDICATION_LOCK requires REAL_HUMAN data")
    if summary.get("all_cases_resolved") is not True:
        raise StudyLockError("POST_ADJUDICATION_LOCK requires all cases resolved")
    if summary.get("case_count") != 24:
        raise StudyLockError("POST_ADJUDICATION_LOCK requires all 24 benchmark cases")


def recompute_real_adjudication(root: Path, responses_path: Path) -> dict[str, Any]:
    from src.ipel.adjudication import aggregate_adjudication

    document = _load_json(responses_path)
    if not isinstance(document, dict) or document.get("data_origin") != "REAL_HUMAN":
        raise StudyLockError("raw adjudication document must declare data_origin=REAL_HUMAN")
    responses = document.get("responses")
    if not isinstance(responses, list) or not responses:
        raise StudyLockError("raw adjudication document requires a non-empty responses array")
    hidden = _load_json(root / "benchmarks/stage007/generated/hidden_case_map.json")
    mapping = hidden.get("mapping") if isinstance(hidden, dict) else None
    if not isinstance(mapping, dict) or len(mapping) != 24:
        raise StudyLockError("hidden adjudication case map is invalid")
    try:
        aggregate = aggregate_adjudication(responses, set(mapping), allow_synthetic=False)
    except Exception as exc:
        raise StudyLockError("raw adjudication responses failed real-data validation") from exc
    validate_real_adjudication_summary(aggregate)
    return aggregate


def validate_study_design(design: Any) -> None:
    if not isinstance(design, dict):
        raise StudyLockError("study design must be an object")
    required_text = (
        "reviewer_population", "power_rationale", "recruitment_constraints",
        "ethics_consent_status", "assignment_procedure",
    )
    for key in required_text:
        if not isinstance(design.get(key), str) or not design[key].strip():
            raise StudyLockError(f"study design missing {key}")
    if design["ethics_consent_status"].strip().upper() in {"UNSPECIFIED", "TBD", "UNKNOWN"}:
        raise StudyLockError("ethics/consent status must be explicitly resolved before primary-study lock")
    criteria = design.get("inclusion_criteria")
    if not isinstance(criteria, list) or not criteria or not all(isinstance(x, str) and x.strip() for x in criteria):
        raise StudyLockError("inclusion_criteria must be a non-empty list")
    n = design.get("target_n")
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise StudyLockError("target_n must be an integer >=2")


def build_freeze_manifest(
    root: Path,
    *,
    state: str,
    source_commit_sha: str,
    real_adjudication_responses_path: Path | None = None,
    real_adjudication_summary_path: Path | None = None,
    study_design_path: Path | None = None,
) -> dict[str, Any]:
    if state not in LOCK_STATES:
        raise StudyLockError(f"unknown lock state: {state}")
    if not isinstance(source_commit_sha, str) or re.fullmatch(r"[0-9a-f]{40}", source_commit_sha) is None:
        raise StudyLockError("source_commit_sha must be a full lowercase 40-character Git SHA")
    file_hashes = _hash_paths(root, PRE_ADJUDICATION_PATHS)
    manifest: dict[str, Any] = {
        "lock_version": "stage007-lock-v1",
        "state": state,
        "source_commit_sha": source_commit_sha,
        "file_sha256": file_hashes,
        "real_adjudication_collected": False,
        "final_sample_size_locked": False,
        "study_design_locked": False,
    }
    if state in {"POST_ADJUDICATION_LOCK", "PRE_PRIMARY_STUDY_LOCK"}:
        if real_adjudication_responses_path is None or not real_adjudication_responses_path.is_file():
            raise StudyLockError(f"{state} requires the raw real-adjudication response file")
        if real_adjudication_summary_path is None or not real_adjudication_summary_path.is_file():
            raise StudyLockError(f"{state} requires a real adjudication summary file")
        responses_rel = _repo_relative(root, real_adjudication_responses_path)
        summary_rel = _repo_relative(root, real_adjudication_summary_path)
        recomputed = recompute_real_adjudication(root, real_adjudication_responses_path)
        summary = _load_json(real_adjudication_summary_path)
        if summary != recomputed:
            raise StudyLockError("real adjudication summary does not match recomputed raw responses")
        manifest["real_adjudication_collected"] = True
        manifest["real_adjudication_responses"] = responses_rel
        manifest["real_adjudication_responses_sha256"] = sha256_file(real_adjudication_responses_path)
        manifest["real_adjudication_summary"] = summary_rel
        manifest["real_adjudication_summary_sha256"] = sha256_file(real_adjudication_summary_path)
    if state == "PRE_PRIMARY_STUDY_LOCK":
        if study_design_path is None or not study_design_path.is_file():
            raise StudyLockError("PRE_PRIMARY_STUDY_LOCK requires a selected study-design file")
        design = _load_json(study_design_path)
        validate_study_design(design)
        rel = _repo_relative(root, study_design_path)
        manifest["study_design_locked"] = True
        manifest["final_sample_size_locked"] = True
        manifest["study_design"] = rel
        manifest["study_design_sha256"] = sha256_file(study_design_path)
        manifest["target_n"] = design["target_n"]
    return manifest


def validate_freeze_manifest(root: Path, manifest: Any) -> None:
    if not isinstance(manifest, dict) or manifest.get("state") not in LOCK_STATES:
        raise StudyLockError("invalid freeze manifest")
    if manifest.get("lock_version") != "stage007-lock-v1":
        raise StudyLockError("unexpected lock version")
    source_sha = manifest.get("source_commit_sha")
    if not isinstance(source_sha, str) or re.fullmatch(r"[0-9a-f]{40}", source_sha) is None:
        raise StudyLockError("invalid source_commit_sha")

    hashes = manifest.get("file_sha256")
    if not isinstance(hashes, dict) or set(hashes) != set(PRE_ADJUDICATION_PATHS):
        raise StudyLockError("freeze manifest must hash the complete pre-adjudication input set")
    for relative, expected in hashes.items():
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise StudyLockError(f"invalid SHA-256 value: {relative}")
        path = root / relative
        if not path.is_file() or sha256_file(path) != expected:
            raise StudyLockError(f"frozen input drift: {relative}")

    state = manifest["state"]
    real = manifest.get("real_adjudication_collected")
    design_locked = manifest.get("study_design_locked")
    final_n = manifest.get("final_sample_size_locked")

    if state == "PRE_ADJUDICATION_LOCK":
        if (real, design_locked, final_n) != (False, False, False):
            raise StudyLockError("PRE_ADJUDICATION_LOCK flags are inconsistent")
        forbidden = {
            "real_adjudication_responses", "real_adjudication_responses_sha256",
            "real_adjudication_summary", "real_adjudication_summary_sha256",
            "study_design", "study_design_sha256", "target_n",
        }
        if forbidden & set(manifest):
            raise StudyLockError("PRE_ADJUDICATION_LOCK contains premature higher-state fields")
        return

    if real is not True:
        raise StudyLockError("post-adjudication states require real adjudication")
    responses_rel = manifest.get("real_adjudication_responses")
    responses_hash = manifest.get("real_adjudication_responses_sha256")
    summary_rel = manifest.get("real_adjudication_summary")
    summary_hash = manifest.get("real_adjudication_summary_sha256")
    if not all(isinstance(x, str) for x in (responses_rel, responses_hash, summary_rel, summary_hash)):
        raise StudyLockError("real adjudication raw/summary provenance is missing")
    responses_path = root / responses_rel
    summary_path = root / summary_rel
    _repo_relative(root, responses_path); _repo_relative(root, summary_path)
    if not responses_path.is_file() or sha256_file(responses_path) != responses_hash:
        raise StudyLockError("real adjudication raw-response hash mismatch")
    if not summary_path.is_file() or sha256_file(summary_path) != summary_hash:
        raise StudyLockError("real adjudication summary hash mismatch")
    recomputed = recompute_real_adjudication(root, responses_path)
    if _load_json(summary_path) != recomputed:
        raise StudyLockError("real adjudication summary does not match recomputed raw responses")

    if state == "POST_ADJUDICATION_LOCK":
        if (design_locked, final_n) != (False, False):
            raise StudyLockError("POST_ADJUDICATION_LOCK cannot claim a locked primary design/sample size")
        forbidden = {"study_design", "study_design_sha256", "target_n"}
        if forbidden & set(manifest):
            raise StudyLockError("POST_ADJUDICATION_LOCK contains premature primary-study fields")
        return

    if (design_locked, final_n) != (True, True):
        raise StudyLockError("PRE_PRIMARY_STUDY_LOCK requires locked design and final sample size")
    design_rel = manifest.get("study_design")
    design_hash = manifest.get("study_design_sha256")
    if not isinstance(design_rel, str) or not isinstance(design_hash, str):
        raise StudyLockError("selected study-design provenance is missing")
    design_path = root / design_rel
    _repo_relative(root, design_path)
    if not design_path.is_file() or sha256_file(design_path) != design_hash:
        raise StudyLockError("study-design hash mismatch")
    design = _load_json(design_path)
    validate_study_design(design)
    if manifest.get("target_n") != design["target_n"]:
        raise StudyLockError("target_n does not match the locked study design")
