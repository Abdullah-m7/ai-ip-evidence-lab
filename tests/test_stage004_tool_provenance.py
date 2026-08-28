import unittest

from experiments.stage004_conformant_c2pa import PINNED_ARCHIVES, PINNED_RELEASE, validate_tool_provenance


class Stage004ToolProvenanceTests(unittest.TestCase):
    def valid(self):
        asset = "c2patool-v0.27.16-x86_64-unknown-linux-gnu.tar.gz"
        return {
            "repository": "contentauth/c2pa-rs",
            "release": PINNED_RELEASE,
            "version": "0.27.16",
            "asset": asset,
            "archive_sha256": PINNED_ARCHIVES[asset],
            "archive_digest_verified": True,
            "download_url": f"https://github.com/contentauth/c2pa-rs/releases/download/{PINNED_RELEASE}/{asset}",
        }

    def test_pinned_provenance_is_accepted(self):
        validate_tool_provenance(self.valid())

    def test_boolean_without_matching_digest_is_rejected(self):
        data = self.valid(); data["archive_sha256"] = "0" * 64
        with self.assertRaises(SystemExit):
            validate_tool_provenance(data)

    def test_wrong_download_origin_is_rejected(self):
        data = self.valid(); data["download_url"] = "https://example.org/c2patool.tar.gz"
        with self.assertRaises(SystemExit):
            validate_tool_provenance(data)


if __name__ == "__main__":
    unittest.main()
