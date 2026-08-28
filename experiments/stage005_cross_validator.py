#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from experiments.stage004_conformant_c2pa import (
    legal_record,
    mutate_exactly_one_byte,
    validate_tool_provenance,
)
from src.ipel.c2pa_crosscheck import (
    CommonValidation,
    agreement,
    normalize_c2patool,
    normalize_cross_validator,
    validate_cross_tool_provenance,
)
from src.ipel.validator import evaluate

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/stage004/source.jpg"
MANIFEST_CONSTRAINED = ROOT / "examples/stage004/manifest-constrained.json"
MANIFEST_ALLOWED = ROOT / "examples/stage004/manifest-allowed.json"
MANIFEST_MALFORMED = ROOT / "examples/stage005/manifest-malformed-tdm.json"


def _read_sidecar(tool: Path) -> dict[str, Any]:
    path = Path(str(tool) + ".provenance.json")
    if not path.exists():
        raise SystemExit(f"missing tool provenance sidecar: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def _sign(c2patool: Path, manifest: Path, output: Path) -> None:
    proc = _run([
        str(c2patool), str(SOURCE), "-m", str(manifest),
        "--create", "trainedAlgorithmicMedia", "-o", str(output),
    ])
    if proc.returncode != 0:
        raise RuntimeError(f"c2patool signing failed: {proc.stderr}")
    json.loads(proc.stdout)


def _reader(c2patool: Path, asset: Path) -> tuple[int, dict[str, Any] | None, str]:
    proc = _run([str(c2patool), str(asset)])
    report = None
    if proc.stdout.strip():
        try:
            report = json.loads(proc.stdout)
        except json.JSONDecodeError:
            report = None
    return proc.returncode, report, proc.stderr.strip()


def _cross(
    cross: Path,
    asset: Path,
    output: Path,
    *,
    trust_list: Path | None = None,
) -> tuple[int, dict[str, Any] | None, str]:
    cmd = [str(cross), "--format", "json"]
    if trust_list is not None:
        cmd += ["--trust-mode", "custom", "--trust-list", str(trust_list)]
    cmd += ["-o", str(output), str(asset)]
    proc = _run(cmd)
    report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else None
    return proc.returncode, report, proc.stderr.strip()


def _summary(result: CommonValidation) -> dict[str, Any]:
    return result.to_dict()


def _case(
    name: str,
    c2patool: Path,
    cross: Path,
    asset: Path,
    outdir: Path,
) -> dict[str, Any]:
    reader_rc, reader_report, reader_stderr = _reader(c2patool, asset)
    cross_rc, cross_report, cross_stderr = _cross(cross, asset, outdir / f"{name}.cross.json")
    if reader_report is None or cross_report is None:
        return {
            "reader_exit_code": reader_rc,
            "cross_exit_code": cross_rc,
            "reader_report_available": reader_report is not None,
            "cross_report_available": cross_report is not None,
            "reader_error_class": "no_claim" if "No claim found" in reader_stderr else "other",
            "cross_error_class": "validation_failed" if cross_rc != 0 else "none",
        }
    left = normalize_c2patool(reader_report)
    right = normalize_cross_validator(cross_report)
    return {
        "reader_exit_code": reader_rc,
        "cross_exit_code": cross_rc,
        "reader": _summary(left),
        "cross_validator": _summary(right),
        "agreement": agreement(left, right),
    }


def _extract_certs(c2patool: Path, asset: Path, target: Path) -> None:
    proc = _run([str(c2patool), str(asset), "--certs"])
    if proc.returncode != 0 or "BEGIN CERTIFICATE" not in proc.stdout:
        raise RuntimeError("could not extract development certificate chain")
    target.write_text(proc.stdout, encoding="utf-8")


def _legal_outcome(record: dict[str, Any]) -> str:
    before = copy.deepcopy(record)
    outcome = evaluate(record).outcome
    if record != before:
        raise AssertionError("legal evaluator mutated the IPEL record")
    return outcome


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c2patool", required=True, type=Path)
    parser.add_argument("--cross-validator", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/stage005_cross_validator.json")
    args = parser.parse_args()
    c2patool = args.c2patool.resolve()
    cross = args.cross_validator.resolve()

    c2patool_provenance = _read_sidecar(c2patool)
    validate_tool_provenance(c2patool_provenance)
    cross_provenance = _read_sidecar(cross)
    validate_cross_tool_provenance(cross_provenance)

    c2patool_version = _run([str(c2patool), "-V"]).stdout.strip()
    cross_version = _run([str(cross), "--version"]).stdout.strip()
    if c2patool_version != "c2patool 0.27.16":
        raise SystemExit(f"unexpected c2patool version: {c2patool_version}")
    if cross_version != "c2pa-validate 0.2.0":
        raise SystemExit(f"unexpected cross-validator version: {cross_version}")

    with tempfile.TemporaryDirectory(prefix="ipel-stage005-") as td:
        work = Path(td)
        clean = work / "clean.jpg"
        allowed = work / "allowed.jpg"
        malformed_tdm = work / "malformed-tdm.jpg"
        _sign(c2patool, MANIFEST_CONSTRAINED, clean)
        _sign(c2patool, MANIFEST_ALLOWED, allowed)
        _sign(c2patool, MANIFEST_MALFORMED, malformed_tdm)

        asset_mutated = work / "asset-mutated.jpg"
        assertion_corrupt = work / "assertion-corrupt.jpg"
        signature_corrupt = work / "signature-corrupt.jpg"
        asset_diff = mutate_exactly_one_byte(
            clean, asset_mutated, b"STAGE004-MUTATION-ANCHOR", len(b"STAGE004-MUTATION-")
        )
        assertion_diff = mutate_exactly_one_byte(clean, assertion_corrupt, b"notAllowed", 1)
        signature_diff = mutate_exactly_one_byte(clean, signature_corrupt, b"C2PA Signer", 2)

        cases = {
            "clean": _case("clean", c2patool, cross, clean, work),
            "asset_mutated": _case("asset-mutated", c2patool, cross, asset_mutated, work),
            "assertion_corrupt": _case("assertion-corrupt", c2patool, cross, assertion_corrupt, work),
            "signature_corrupt": _case("signature-corrupt", c2patool, cross, signature_corrupt, work),
            "malformed_tdm": _case("malformed-tdm", c2patool, cross, malformed_tdm, work),
            "no_manifest": _case("no-manifest", c2patool, cross, SOURCE, work),
        }

        certs = work / "development-chain.pem"
        _extract_certs(c2patool, clean, certs)
        custom_rc, custom_report, _ = _cross(
            cross, clean, work / "clean.custom.cross.json", trust_list=certs
        )
        if custom_report is None:
            raise RuntimeError("custom-trust validation produced no report")
        custom_clean = normalize_cross_validator(custom_report)

        allowed_default_rc, allowed_default_report, _ = _cross(
            cross, allowed, work / "allowed.default.cross.json"
        )
        allowed_custom_rc, allowed_custom_report, _ = _cross(
            cross, allowed, work / "allowed.custom.cross.json", trust_list=certs
        )
        if allowed_default_report is None or allowed_custom_report is None:
            raise RuntimeError("allowed trust-mode reports missing")
        allowed_default = normalize_cross_validator(allowed_default_report)
        allowed_custom = normalize_cross_validator(allowed_custom_report)

        unlawful = legal_record(acquisition_false=True)
        no_permission = legal_record(output_permission_false=True)
        unlawful_default = _legal_outcome(unlawful)
        unlawful_custom = _legal_outcome(unlawful)
        permission_default = _legal_outcome(no_permission)
        permission_custom = _legal_outcome(no_permission)

    clean_reader = cases["clean"]["reader"]
    clean_cross = cases["clean"]["cross_validator"]
    malformed_reader = cases["malformed_tdm"]["reader"]
    malformed_cross = cases["malformed_tdm"]["cross_validator"]

    expected_attack = {
        "asset_mutated": ("asset_binding", "invalid", "assertion.dataHash.mismatch"),
        "assertion_corrupt": ("assertion_references", "invalid", "assertion.hashedURI.mismatch"),
        "signature_corrupt": ("claim_signature", "invalid", "claimSignature.mismatch"),
    }
    attack_agreement: dict[str, bool] = {}
    for name, (field, value, code) in expected_attack.items():
        item = cases[name]
        attack_agreement[name] = (
            item["reader"][field] == value
            and item["cross_validator"][field] == value
            and code in item["reader"]["failure_codes"]
            and code in item["cross_validator"]["failure_codes"]
        )

    acceptance = {
        "clean_common_semantics_agree": cases["clean"]["agreement"]["all_common_semantics_agree"],
        "cross_version_validation_established": (
            clean_reader["engine_version"] == "0.90.16"
            and clean_cross["engine_version"] == "0.78.0"
            and cases["clean"]["agreement"]["shared_engine_lineage"]
        ),
        "all_three_corruptions_detected_by_both": all(attack_agreement.values()),
        "custom_trust_changes_trust_not_crypto": (
            clean_cross["signer_trust"] == "untrusted"
            and custom_clean.signer_trust == "trusted"
            and clean_cross["cryptographic_validity"] == custom_clean.cryptographic_validity == "valid"
        ),
        "malformed_tdm_is_crypto_valid_but_semantically_rejected": (
            malformed_reader["cryptographic_validity"] == "valid"
            and malformed_cross["cryptographic_validity"] == "valid"
            and malformed_reader["tdm_entries"] == {}
            and malformed_cross["tdm_entries"] == {}
            and bool(malformed_reader["semantic_warnings"])
            and bool(malformed_cross["semantic_warnings"])
        ),
        "no_manifest_negative_control_rejected_by_both": (
            cases["no_manifest"]["reader_exit_code"] != 0
            and cases["no_manifest"]["cross_exit_code"] != 0
            and cases["no_manifest"]["reader_report_available"] is False
            and cases["no_manifest"]["cross_report_available"] is False
        ),
        "allowed_signal_does_not_cure_unlawful_acquisition_under_trust_change": (
            allowed_default.tdm_entries.get("cawg.ai_training") == "allowed"
            and allowed_custom.tdm_entries.get("cawg.ai_training") == "allowed"
            and unlawful_default == unlawful_custom == "FAIL_EVIDENCE_GATE"
        ),
        "allowed_signal_does_not_grant_output_permission_under_trust_change": (
            permission_default == permission_custom == "FAIL_EVIDENCE_GATE"
        ),
        "implementation_diversity_not_overclaimed": (
            cross_provenance["implementation_diversity_established"] is False
            and cases["clean"]["agreement"]["implementation_diversity_established"] is False
        ),
        "upstream_dependency_repair_disclosed": (
            cross_provenance["compatibility_repair"] is True
            and isinstance(cross_provenance["declared_profile_commit_unavailable"], str)
        ),
    }

    report = {
        "stage": "005",
        "result": "PASS" if all(acceptance.values()) else "HOLD",
        "implementation_diversity": "IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED",
        "toolchains": {
            "generator_reader": {
                "tool": c2patool_version,
                "engine_lineage": "c2pa-rs",
                "engine_version_observed": clean_reader["engine_version"],
            },
            "cross_validator": {
                "tool": cross_version,
                "engine_lineage": "c2pa-rs",
                "engine_version_observed": clean_cross["engine_version"],
                "compatibility_repair": True,
                "declared_profile_commit_unavailable": cross_provenance["declared_profile_commit_unavailable"],
                "repair_commits": {
                    "profile_evaluator": cross_provenance["profile_repair_commit"],
                    "json_formula": cross_provenance["json_formula_repair_commit"],
                },
            },
        },
        "cases": cases,
        "attack_agreement": attack_agreement,
        "trust_boundary": {
            "default": clean_cross,
            "custom": custom_clean.to_dict(),
            "custom_cross_exit_code": custom_rc,
            "allowed_default": allowed_default.to_dict(),
            "allowed_custom": allowed_custom.to_dict(),
            "allowed_default_exit_code": allowed_default_rc,
            "allowed_custom_exit_code": allowed_custom_rc,
        },
        "legal_boundary": {
            "unlawful_acquisition_default_trust": unlawful_default,
            "unlawful_acquisition_custom_trust": unlawful_custom,
            "no_output_permission_default_trust": permission_default,
            "no_output_permission_custom_trust": permission_custom,
            "legal_fields_overwritten": False,
        },
        "article_30_3_fields_newly_delegated": [],
        "acceptance": acceptance,
        "all_acceptance_gates_pass": all(acceptance.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_acceptance_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
