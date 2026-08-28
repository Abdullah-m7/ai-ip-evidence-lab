#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from src.ipel.c2pa_adapter import coupled_evaluation, extract_c2pa_evidence

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples/stage004/source.jpg"
MANIFEST_CONSTRAINED = ROOT / "examples/stage004/manifest-constrained.json"
MANIFEST_ALLOWED = ROOT / "examples/stage004/manifest-allowed.json"
BASE_RECORD = ROOT / "examples/records/valid.json"
EXPECTED_SOURCE_SHA256 = "652c561108a2961573a7dd10f720033359f650453ef33694f7dbc5fee29aae5e"
PINNED_RELEASE = "c2patool-v0.27.16"
PINNED_ARCHIVES = {
    "c2patool-v0.27.16-universal-apple-darwin.zip": "2c2cd9f949c7231a71bce26b0d4f7e7b45db2128bf93cd0e3189ad0172e9039e",
    "c2patool-v0.27.16-x86_64-unknown-linux-gnu.tar.gz": "62eed34f0c90a24b696b1969c8aad4340e11ec7264e1cf6fc375ad15c1db7663",
}


def validate_tool_provenance(provenance: dict) -> None:
    if not isinstance(provenance, dict):
        raise SystemExit("c2patool provenance must be an object")
    if provenance.get("repository") != "contentauth/c2pa-rs":
        raise SystemExit("unexpected c2patool repository provenance")
    if provenance.get("release") != PINNED_RELEASE or provenance.get("version") != "0.27.16":
        raise SystemExit("unexpected c2patool release provenance")
    asset = provenance.get("asset")
    if asset not in PINNED_ARCHIVES:
        raise SystemExit("unrecognized pinned c2patool release asset")
    if provenance.get("archive_sha256") != PINNED_ARCHIVES[asset] or provenance.get("archive_digest_verified") is not True:
        raise SystemExit("c2patool archive digest provenance mismatch")
    expected_url = f"https://github.com/contentauth/c2pa-rs/releases/download/{PINNED_RELEASE}/{asset}"
    if provenance.get("download_url") != expected_url:
        raise SystemExit("unexpected c2patool download provenance")


def run_json(tool: Path, *args: str) -> dict:
    proc = subprocess.run([str(tool), *args], check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def sign(tool: Path, source: Path, manifest: Path, output: Path) -> dict:
    return run_json(
        tool,
        str(source),
        "-m",
        str(manifest),
        "--create",
        "trainedAlgorithmicMedia",
        "-o",
        str(output),
    )


def verify(tool: Path, asset: Path) -> dict:
    return run_json(tool, str(asset))


def mutate_exactly_one_byte(src: Path, dst: Path, needle: bytes, relative_offset: int) -> int:
    raw = src.read_bytes()
    data = bytearray(raw)
    start = raw.find(needle)
    if start < 0:
        raise RuntimeError(f"mutation anchor not found: {needle!r}")
    pos = start + relative_offset
    data[pos] ^= 1
    dst.write_bytes(data)
    if len(data) != len(raw):
        raise AssertionError("mutation changed file length")
    diff_count = sum(a != b for a, b in zip(raw, data))
    if diff_count != 1:
        raise AssertionError(f"expected one-byte mutation, found {diff_count}")
    return diff_count


def legal_record(*, acquisition_false: bool = False, output_permission_false: bool = False) -> dict:
    record = json.loads(BASE_RECORD.read_text(encoding="utf-8"))
    record["record_id"] = "stage004-real-c2pa-case"
    record["work"]["title"] = "Stage 004 Synthetic C2PA Asset"
    record["work"]["source"] = "synthetic://stage004/source.jpg"
    record["work"]["sha256"] = EXPECTED_SOURCE_SHA256
    if acquisition_false:
        record["work"]["acquisition_status"] = "false"
    if output_permission_false:
        record["output_context"]["transformed"] = True
        record["output_context"]["permission_status"] = "not_granted"
        record["output_context"]["public_domain_status"] = "no"
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c2patool", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/stage004_conformant_c2pa.json")
    args = parser.parse_args()
    tool = args.c2patool.resolve()
    provenance_path = Path(str(tool) + ".provenance.json")
    if not provenance_path.exists():
        raise SystemExit(f"missing tool provenance sidecar: {provenance_path}")
    tool_provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    validate_tool_provenance(tool_provenance)

    version = subprocess.run([str(tool), "-V"], check=True, capture_output=True, text=True).stdout.strip()
    if version != "c2patool 0.27.16":
        raise SystemExit(f"unexpected c2patool version: {version}")
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source hash drift: {source_sha}")

    with tempfile.TemporaryDirectory(prefix="ipel-stage004-") as td:
        work = Path(td)
        clean_asset = work / "clean-signed.jpg"
        allowed_asset = work / "allowed-signed.jpg"
        sign(tool, SOURCE, MANIFEST_CONSTRAINED, clean_asset)
        sign(tool, SOURCE, MANIFEST_ALLOWED, allowed_asset)

        clean_report = verify(tool, clean_asset)
        allowed_report = verify(tool, allowed_asset)
        clean = extract_c2pa_evidence(clean_report).to_dict()
        allowed = extract_c2pa_evidence(allowed_report).to_dict()

        mutated_asset = work / "mutated-one-byte.jpg"
        asset_diff_count = mutate_exactly_one_byte(
            clean_asset,
            mutated_asset,
            b"STAGE004-MUTATION-ANCHOR",
            len(b"STAGE004-MUTATION-"),
        )
        mutated = extract_c2pa_evidence(verify(tool, mutated_asset)).to_dict()

        assertion_asset = work / "assertion-corrupt.jpg"
        assertion_diff_count = mutate_exactly_one_byte(clean_asset, assertion_asset, b"notAllowed", 1)
        assertion_corrupt = extract_c2pa_evidence(verify(tool, assertion_asset)).to_dict()

        signature_asset = work / "signature-corrupt.jpg"
        signature_diff_count = mutate_exactly_one_byte(clean_asset, signature_asset, b"C2PA Signer", 2)
        signature_corrupt = extract_c2pa_evidence(verify(tool, signature_asset)).to_dict()

        unlawful_acquisition = coupled_evaluation(allowed_report, legal_record(acquisition_false=True))
        no_output_permission = coupled_evaluation(allowed_report, legal_record(output_permission_false=True))

    acceptance = {
        "real_c2pa_artifact_validates": (
            clean["validation_state"] == "valid"
            and clean["asset_binding"] == "valid"
            and clean["claim_signature"] == "valid"
            and clean["assertion_references"] == "valid"
        ),
        "one_byte_asset_mutation_detected": (
            asset_diff_count == 1
            and mutated["asset_binding"] == "invalid"
            and "assertion.dataHash.mismatch" in mutated["issue_codes"]
        ),
        "assertion_corruption_detected": (
            assertion_diff_count == 1
            and assertion_corrupt["assertion_references"] == "invalid"
            and "assertion.hashedURI.mismatch" in assertion_corrupt["issue_codes"]
        ),
        "claim_signature_corruption_detected": (
            signature_diff_count == 1
            and signature_corrupt["claim_signature"] == "invalid"
            and "claimSignature.mismatch" in signature_corrupt["issue_codes"]
        ),
        "signature_validity_separate_from_signer_trust": (
            clean["claim_signature"] == "valid" and clean["signer_trust"] == "untrusted"
        ),
        "allowed_tdm_does_not_cure_unlawful_acquisition": (
            allowed["tdm_entries"].get("cawg.ai_training") == "allowed"
            and unlawful_acquisition["legal_gate"]["outcome"] == "FAIL_EVIDENCE_GATE"
            and unlawful_acquisition["legal_fields_overwritten"] is False
        ),
        "allowed_tdm_does_not_grant_output_permission": (
            allowed["tdm_entries"].get("cawg.ai_training") == "allowed"
            and no_output_permission["legal_gate"]["outcome"] == "FAIL_EVIDENCE_GATE"
            and no_output_permission["legal_fields_overwritten"] is False
        ),
    }

    report = {
        "stage": "004",
        "toolchain": {
            "repository": "contentauth/c2pa-rs",
            "release": "c2patool-v0.27.16",
            "version_output": version,
            "pinned_release_archive_verified": True,
            "development_signer": True,
        },
        "synthetic_source": {
            "sha256": source_sha,
            "copyright_ambiguity": False,
        },
        "clean_artifact": clean,
        "one_byte_asset_mutation": {"diff_count": asset_diff_count, "evidence": mutated},
        "assertion_corruption": {"diff_count": assertion_diff_count, "evidence": assertion_corrupt},
        "signing_credential_corruption": {"diff_count": signature_diff_count, "evidence": signature_corrupt},
        "allowed_signal": allowed,
        "allowed_plus_unlawful_acquisition": unlawful_acquisition,
        "allowed_plus_no_output_permission": no_output_permission,
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
