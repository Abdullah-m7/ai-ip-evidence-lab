#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.ipel.adjudication_distribution import (
    ROOT,
    build_distribution,
    guard_bundle_destination,
    guard_private_destination,
    parse_key_hex,
    response_template,
)

SOURCE_PACKET = ROOT / "benchmarks/stage007/generated/adjudication_packet.json"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a contamination-resistant Stage-008 adjudication bundle")
    parser.add_argument("--distribution-id", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--private-dir", type=Path)
    args = parser.parse_args()

    key_hex = os.environ.get("IPEL_STAGE008_KEY_HEX")
    if not key_hex:
        raise SystemExit("IPEL_STAGE008_KEY_HEX is required; do not place the distribution key in Git")
    key = parse_key_hex(key_hex)
    source = json.loads(SOURCE_PACKET.read_text(encoding="utf-8"))
    bundle, manifest, mapping = build_distribution(source, args.distribution_id, key)

    output_dir = (args.output_dir or (ROOT / ".stage008-distributions" / args.distribution_id)).resolve()
    private_dir = (args.private_dir or (ROOT / ".private-stage008" / args.distribution_id)).resolve()
    guard_bundle_destination(output_dir, ROOT)
    guard_private_destination(private_dir, ROOT)

    write_json(output_dir / "adjudication_bundle.json", bundle)
    write_json(output_dir / "bundle_manifest.json", manifest)
    write_json(output_dir / "response_template.json", response_template(bundle, manifest))
    write_json(private_dir / "private_case_mapping.json", mapping)

    print(json.dumps({
        "status": "EXPORTED",
        "distribution_id": args.distribution_id,
        "bundle_id": bundle["bundle_id"],
        "case_count": bundle["case_count"],
        "public_output_dir": str(output_dir),
        "private_mapping_dir": str(private_dir),
        "warning": "Private mapping and distribution key must not be committed. Procedural blinding is not cryptographic human-identity proof.",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
