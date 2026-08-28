from __future__ import annotations

import copy
import json
from pathlib import Path

from src.ipel.c2pa_profile import (
    GENERIC_FIELD_MAP,
    from_profile,
    roundtrip_metrics,
    semantic_loss,
    to_profile,
    validate_profile,
)
from src.ipel.validator import evaluate

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "examples/records/valid.json").read_text())


def cases():
    result = []
    result.append(("pass_clean", copy.deepcopy(BASE), {}))

    review = copy.deepcopy(BASE)
    review["work"]["publication_status"] = "unverified"
    result.append(("review_unverified_publication", review, {"tdm_use": "allowed", "manifest_state": "valid", "trust_state": "trusted"}))

    fail = copy.deepcopy(BASE)
    fail["use"]["distribution"] = True
    result.append(("fail_distribution", fail, {}))

    unlawful = copy.deepcopy(BASE)
    unlawful["work"]["acquisition_status"] = "false"
    result.append(("false_equivalence_allowed_unlawful_acquisition", unlawful, {"tdm_use": "allowed", "manifest_state": "valid", "trust_state": "trusted"}))

    permission = copy.deepcopy(BASE)
    permission["output_context"]["transformed"] = True
    permission["output_context"]["permission_status"] = "not_granted"
    result.append(("false_equivalence_allowed_no_output_permission", permission, {"tdm_use": "allowed", "manifest_state": "valid", "trust_state": "trusted"}))
    return result


def main() -> None:
    rows = []
    clean_profile = None
    adversarial_profile = None
    for name, record, kwargs in cases():
        profile = to_profile(record, **kwargs)
        rebuilt = from_profile(profile)
        metrics = roundtrip_metrics(record, profile)
        rows.append({
            "case": name,
            **metrics.to_dict(),
            "semantic_loss_paths": semantic_loss(record, rebuilt),
            "profile_validation_errors": validate_profile(profile),
            "tdm_use": next(iter(profile["c2pa"]["tdm_assertion"]["entries"].values()))["use"],
            "manifest_state": profile["c2pa"]["validation_signals"]["manifest_state"],
            "trust_state": profile["c2pa"]["validation_signals"]["trust_state"],
        })
        if name == "pass_clean":
            clean_profile = profile
        if name == "false_equivalence_allowed_unlawful_acquisition":
            adversarial_profile = profile

    assert clean_profile is not None and adversarial_profile is not None
    missing_source = copy.deepcopy(clean_profile)
    del missing_source["ipel_jurisdictional"]["work"]["source"]

    profile_dir = ROOT / "examples/profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "stage003_clean.json").write_text(json.dumps(clean_profile, indent=2, ensure_ascii=False) + "\n")
    (profile_dir / "stage003_allowed_unlawful_acquisition.json").write_text(json.dumps(adversarial_profile, indent=2, ensure_ascii=False) + "\n")
    (profile_dir / "stage003_missing_source.json").write_text(json.dumps(missing_source, indent=2, ensure_ascii=False) + "\n")

    report = {
        "stage": "003",
        "profile_kind": "c2pa-aligned-ipel-profile",
        "c2pa_version": "2.4",
        "cawg_tdm_version": "1.1",
        "representation_is_conformant_manifest": False,
        "case_count": len(rows),
        "mapped_generic_fields": GENERIC_FIELD_MAP,
        "article_30_3_fields_carried_by_c2pa": [],
        "article_30_3_fields_retained_jurisdictionally": ["work.type", "work.source", "use.purpose", "use.date"],
        "all_valid_profiles_zero_duplicate_generic_fields": all(r["duplicate_generic_field_count"] == 0 for r in rows),
        "all_roundtrips_zero_semantic_loss": all(r["semantic_loss_count"] == 0 for r in rows),
        "all_article_30_3_tuples_preserved": all(r["article_30_3_preserved"] for r in rows),
        "all_gate_outcomes_preserved": all(r["gate_preserved"] for r in rows),
        "false_equivalence_cases_preserved": {
            r["case"]: r["reconstructed_gate"]
            for r in rows if r["case"].startswith("false_equivalence")
        },
        "invalid_missing_source_profile_errors": validate_profile(missing_source),
        "cases": rows,
    }
    (ROOT / "reports/stage003_semantic_roundtrip.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
