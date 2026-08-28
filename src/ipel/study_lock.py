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
        if real_adjudication_summary_path is None or not real_adjudication_summary_path.is_file():
            raise StudyLockError(f"{state} requires a real adjudication summary file")
        summary = _load_json(real_adjudication_summary_path)
        validate_real_adjudication_summary(summary)
        rel = _repo_relative(root, real_adjudication_summary_path)
        manifest["real_adjudication_collected"] = True
        manifest["real_adjudication_summary"] = rel
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
    state = manifest["state"]
    if state == "PRE_ADJUDICATION_LOCK":
        if manifest.get("real_adjudication_collected") is not False:
            raise StudyLockError("pre-adjudication lock cannot claim real adjudication")
        if manifest.get("final_sample_size_locked") is not False:
            raise StudyLockError("pre-adjudication lock cannot claim final sample size")
    if state in {"POST_ADJUDICATION_LOCK", "PRE_PRIMARY_STUDY_LOCK"} and manifest.get("real_adjudication_collected") is not True:
        raise StudyLockError("post-adjudication states require real adjudication")
    if state == "PRE_PRIMARY_STUDY_LOCK" and manifest.get("final_sample_size_locked") is not True:
        raise StudyLockError("primary-study lock requires a final sample size")
    hashes = manifest.get("file_sha256")
    if not isinstance(hashes, dict):
        raise StudyLockError("freeze manifest missing file hashes")
    for relative, expected in hashes.items():
        path = root / relative
        if not path.is_file() or sha256_file(path) != expected:
            raise StudyLockError(f"frozen input drift: {relative}")
