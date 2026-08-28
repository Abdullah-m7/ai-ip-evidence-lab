#!/usr/bin/env bash
set -euo pipefail
VERSION="0.27.16"
DEST="${1:-.tools/c2patool}"
OS="$(uname -s)"
ARCH="$(uname -m)"
case "$OS/$ARCH" in
  Darwin/arm64|Darwin/x86_64)
    ASSET="c2patool-v${VERSION}-universal-apple-darwin.zip"
    SHA256="2c2cd9f949c7231a71bce26b0d4f7e7b45db2128bf93cd0e3189ad0172e9039e"
    KIND="zip"
    ;;
  Linux/x86_64)
    ASSET="c2patool-v${VERSION}-x86_64-unknown-linux-gnu.tar.gz"
    SHA256="62eed34f0c90a24b696b1969c8aad4340e11ec7264e1cf6fc375ad15c1db7663"
    KIND="tar"
    ;;
  *) echo "unsupported platform: $OS/$ARCH" >&2; exit 2 ;;
esac
URL="https://github.com/contentauth/c2pa-rs/releases/download/c2patool-v${VERSION}/${ASSET}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -L --fail --silent --show-error -o "$TMP/$ASSET" "$URL"
python3 - "$TMP/$ASSET" "$SHA256" <<'PY'
import hashlib, pathlib, sys
p=pathlib.Path(sys.argv[1]); expected=sys.argv[2]
actual=hashlib.sha256(p.read_bytes()).hexdigest()
if actual != expected: raise SystemExit(f"digest mismatch: {actual} != {expected}")
print(f"verified {p.name}: {actual}")
PY
mkdir -p "$TMP/unpack"
if [[ "$KIND" == zip ]]; then unzip -q "$TMP/$ASSET" -d "$TMP/unpack"; else tar -xzf "$TMP/$ASSET" -C "$TMP/unpack"; fi
BIN="$(find "$TMP/unpack" -type f -name c2patool | head -1)"
test -n "$BIN"
mkdir -p "$(dirname "$DEST")"
cp "$BIN" "$DEST"
chmod +x "$DEST"
"$DEST" -V
python3 - "$DEST.provenance.json" "$VERSION" "$ASSET" "$SHA256" "$URL" "$OS" "$ARCH" <<'PYMETA'
import json, pathlib, sys
out, version, asset, sha256, url, os_name, arch = sys.argv[1:]
data = {
    "repository": "contentauth/c2pa-rs",
    "release": f"c2patool-v{version}",
    "version": version,
    "asset": asset,
    "archive_sha256": sha256,
    "archive_digest_verified": True,
    "download_url": url,
    "platform": {"os": os_name, "arch": arch},
}
pathlib.Path(out).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
PYMETA
