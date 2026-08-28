#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.ipel.adjudication_distribution import (
    ROOT,
    append_intake,
    guard_private_destination,
    new_intake_ledger,
    normalize_external_response,
    parse_key_hex,
    verify_intake_ledger,
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest one completed Stage-008 adjudication response document")
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--private-mapping", required=True, type=Path)
    parser.add_argument("--response", required=True, type=Path)
    parser.add_argument("--ledger", type=Path, default=ROOT / ".private-stage008" / "intake_ledger.json")
    parser.add_argument("--allow-synthetic", action="store_true", help="Software tests only; never use for real adjudication")
    args = parser.parse_args()

    key_hex = os.environ.get("IPEL_STAGE008_KEY_HEX")
    if not key_hex:
        raise SystemExit("IPEL_STAGE008_KEY_HEX is required")
    key = parse_key_hex(key_hex)
    ledger_path = args.ledger.resolve()
    guard_private_destination(ledger_path, ROOT)

    bundle = load_json(args.bundle)
    manifest = load_json(args.manifest)
    mapping = load_json(args.private_mapping)
    response = load_json(args.response)
    normalized = normalize_external_response(
        response, bundle, manifest, mapping, key, allow_synthetic=args.allow_synthetic
    )

    if ledger_path.exists():
        ledger = load_json(ledger_path)
        verify_intake_ledger(ledger)
    else:
        ledger = new_intake_ledger(normalized["data_origin"])
    updated = append_intake(ledger, normalized)
    write_json(ledger_path, updated)

    print(json.dumps({
        "status": "INGESTED_RAW_RESPONSES_ONLY",
        "data_origin": updated["data_origin"],
        "intake_events": len(updated["events"]),
        "response_rows": len(updated["responses"]),
        "ledger": str(ledger_path),
        "lock_promoted": False,
        "warning": "Ingestion records responses and post-intake integrity only. It does not establish human identity or promote a Stage-007 lock.",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
