import json
import unittest
from pathlib import Path

from src.ipel.validator import CURRENT_PROFILE_ID, LEGACY_PROFILE_ID, evaluate

ROOT = Path(__file__).resolve().parents[1]


class LegalProfileScopeTests(unittest.TestCase):
    def test_schema_versions_and_article37_conditional_are_declared(self):
        schema = json.loads((ROOT / "schemas/ipel-record.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["properties"]["record_version"]["enum"]), {"0.1.0", "0.2.0"})
        self.assertIn("article37_context", schema["properties"])
        self.assertTrue(schema.get("allOf"))
        conditional = json.dumps(schema["allOf"], sort_keys=True)
        self.assertIn('"const": "0.2.0"', conditional)
        self.assertIn('"article37_context"', conditional)

    def test_matrix_declares_current_scope_and_semantic_separation(self):
        text = (ROOT / "docs/LEGAL_REQUIREMENTS_MATRIX.md").read_text(encoding="utf-8")
        self.assertIn("Copyright Law Article 37(1)", text)
        self.assertIn("LEGACY / INCOMPLETE FOR THE FULL PATHWAY", text)
        self.assertIn("IR-30(2) normal-exploitation impact != automatically identical to LAW-37(1)", text)
        self.assertIn("IR-30(4) author-interest assessment != automatically identical to LAW-37(1)", text)

    def test_versioning_policy_blocks_retroactive_relabelling(self):
        text = (ROOT / "docs/LEGAL_PROFILE_VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("Do not transform a 0.1.0 record into 0.2.0 merely by changing `record_version`", text)
        self.assertIn("Stages 001–005 remain historical 0.1.0 evidence", text)
        self.assertIn("SCIENTIFIC HOLD / MAJOR REVISION", text)

    def test_report_preserves_no_legal_conclusion_boundary(self):
        report = (ROOT / "reports/STAGE_012_ART37_REMEDIATION.md").read_text(encoding="utf-8")
        self.assertIn("rehabilitate the old Paper A experiments automatically", report)
        current = json.loads((ROOT / "examples/records/valid_v020_art37.json").read_text(encoding="utf-8"))
        legacy = json.loads((ROOT / "examples/records/valid.json").read_text(encoding="utf-8"))
        current_result = evaluate(current)
        legacy_result = evaluate(legacy)
        self.assertEqual(current_result.legal_profile_id, CURRENT_PROFILE_ID)
        self.assertEqual(legacy_result.legal_profile_id, LEGACY_PROFILE_ID)
        self.assertFalse(current_result.to_dict()["legal_conclusion"])
        self.assertFalse(legacy_result.to_dict()["legal_conclusion"])

    def test_legacy_serialization_stays_byte_shape_compatible_by_default(self):
        legacy = json.loads((ROOT / "examples/records/valid.json").read_text(encoding="utf-8"))
        result = evaluate(legacy)
        payload = result.to_dict()
        self.assertEqual(set(payload), {"outcome", "findings", "legal_conclusion"})
        self.assertNotIn("legal_profile_id", payload)
        self.assertNotIn("declared_scope_complete", payload)

    def test_profile_metadata_is_explicitly_available_for_new_outputs(self):
        current = json.loads((ROOT / "examples/records/valid_v020_art37.json").read_text(encoding="utf-8"))
        payload = evaluate(current).to_dict(include_profile_metadata=True)
        self.assertEqual(payload["legal_profile_id"], CURRENT_PROFILE_ID)
        self.assertTrue(payload["declared_scope_complete"])
        self.assertFalse(payload["legal_conclusion"])


if __name__ == "__main__":
    unittest.main()
