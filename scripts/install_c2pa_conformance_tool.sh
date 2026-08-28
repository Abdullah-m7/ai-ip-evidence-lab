#!/usr/bin/env bash
set -euo pipefail

DEST="${1:-.tools/c2pa-validate}"
RUST_VERSION="1.98.0"
CLI_COMMIT="c09f0340524b088a81475f7b7eaab5ba7042772f"
CLI_VERSION="0.2.0"
CLI_ARCHIVE_SHA256="3571355b1a83d7150393d070e7b4a5b5c0f32d8524b6d7a41f740395c9cefc85"
C2PA_COMMIT="61f2e676043c1d22fa60f4fe5d09d3874c7c8a10"
C2PA_ARCHIVE_SHA256="4a27ab5cceb4ea4e42b1e629808a0895f2c91a0fea5cd71c5827665d8f7e8bc7"
DECLARED_PROFILE_COMMIT="c43d11162c27c5e992c7010fc75b72bb3e5520e1"
PROFILE_REPAIR_COMMIT="40c4201933e3b4760932b65913e2a9c57413f8ac"
PROFILE_ARCHIVE_SHA256="2c51d6aafdc67f075a5ce31d6700ab031df214789bdb9a893dc60b48391b7e6a"
DECLARED_JSON_COMMIT="1ff483f15157521503a0ce79c123333ecd14ce08"
JSON_REPAIR_COMMIT="90ee7f44ded98c657a410a0bf1248a9e3f6f1627"
LOCK_SHA256="80dcab12a2773a6cffd3c6c8794640d0be9cff3a9227d7abd44143e963fa6fd0"

for cmd in curl git python3 rustup shasum tar; do
  command -v "$cmd" >/dev/null || { echo "$cmd is required" >&2; exit 2; }
done
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

fetch_archive() {
  local url="$1" expected="$2" dest="$3" archive="$4"
  curl -L --fail --retry 3 --connect-timeout 10 -sS -o "$archive" "$url"
  echo "$expected  $archive" | shasum -a 256 -c -
  mkdir -p "$dest"
  tar -xzf "$archive" -C "$dest" --strip-components=1
}

if ! rustup toolchain list | grep -q "^${RUST_VERSION}-"; then
  rustup toolchain install "$RUST_VERSION" --profile minimal --no-self-update >/dev/null
fi

fetch_archive \
  "https://github.com/contentauth/c2pa-conformance-tool-cli/archive/${CLI_COMMIT}.tar.gz" \
  "$CLI_ARCHIVE_SHA256" "$WORK/cli" "$WORK/cli.tar.gz"
rm -rf "$WORK/cli/vendor/c2pa-rs" "$WORK/cli/vendor/profile-evaluator-rs" "$WORK/cli/vendor/json-formula-rs"
fetch_archive \
  "https://github.com/contentauth/c2pa-rs/archive/${C2PA_COMMIT}.tar.gz" \
  "$C2PA_ARCHIVE_SHA256" "$WORK/cli/vendor/c2pa-rs" "$WORK/c2pa.tar.gz"
fetch_archive \
  "https://github.com/adobe/profile-evaluator-rs/archive/${PROFILE_REPAIR_COMMIT}.tar.gz" \
  "$PROFILE_ARCHIVE_SHA256" "$WORK/cli/vendor/profile-evaluator-rs" "$WORK/profile.tar.gz"

# json-formula-rs contains large unrelated tracked material; fetch only native build paths.
git init -q "$WORK/cli/vendor/json-formula-rs"
git -C "$WORK/cli/vendor/json-formula-rs" remote add origin https://github.com/adobe/json-formula-rs.git
git -C "$WORK/cli/vendor/json-formula-rs" sparse-checkout init --cone
git -C "$WORK/cli/vendor/json-formula-rs" sparse-checkout set src Cargo.toml LICENSE README.md
git -C "$WORK/cli/vendor/json-formula-rs" fetch -q --depth=1 --filter=blob:none origin "$JSON_REPAIR_COMMIT"
git -C "$WORK/cli/vendor/json-formula-rs" checkout -q --detach FETCH_HEAD
test "$(git -C "$WORK/cli/vendor/json-formula-rs" rev-parse HEAD)" = "$JSON_REPAIR_COMMIT"

echo "$LOCK_SHA256  $WORK/cli/Cargo.lock" | shasum -a 256 -c -
python3 - "$WORK/cli" <<'PY2'
from pathlib import Path
import sys
root=Path(sys.argv[1])
profile=root/'vendor/profile-evaluator-rs/Cargo.toml'
s=profile.read_text()
s=s.replace('version = "0.2.0"','version = "0.1.0"',1)
marker='\n[target.\'cfg(target_arch = "wasm32")\'.dependencies]\n'
if marker in s:
    s=s.split(marker,1)[0].rstrip()+'\n'
profile.write_text(s)
formula=root/'vendor/json-formula-rs/Cargo.toml'
formula.write_text(formula.read_text().replace('version = "0.2.0"','version = "0.1.0"',1))
PY2

(
  cd "$WORK/cli"
  cargo +"$RUST_VERSION" build --locked --release -p c2pa-validate
)
mkdir -p "$(dirname "$DEST")"
cp "$WORK/cli/target/release/c2pa-validate" "$DEST"
chmod +x "$DEST"
VERSION_OUTPUT="$("$DEST" --version)"
test "$VERSION_OUTPUT" = "c2pa-validate 0.2.0"

cat > "${DEST}.provenance.json" <<JSON
{
  "repository": "contentauth/c2pa-conformance-tool-cli",
  "commit": "$CLI_COMMIT",
  "version": "$CLI_VERSION",
  "version_output": "$VERSION_OUTPUT",
  "source_archive_sha256": "$CLI_ARCHIVE_SHA256",
  "rust": "$RUST_VERSION",
  "cargo_lock_sha256": "$LOCK_SHA256",
  "c2pa_rs_commit": "$C2PA_COMMIT",
  "c2pa_rs_archive_sha256": "$C2PA_ARCHIVE_SHA256",
  "declared_profile_commit_unavailable": "$DECLARED_PROFILE_COMMIT",
  "profile_repair_repository": "adobe/profile-evaluator-rs",
  "profile_repair_commit": "$PROFILE_REPAIR_COMMIT",
  "profile_repair_archive_sha256": "$PROFILE_ARCHIVE_SHA256",
  "declared_json_formula_commit": "$DECLARED_JSON_COMMIT",
  "json_formula_repair_repository": "adobe/json-formula-rs",
  "json_formula_repair_commit": "$JSON_REPAIR_COMMIT",
  "json_formula_repair_commit_verified": true,
  "compatibility_repair": true,
  "shared_engine_lineage": "c2pa-rs",
  "implementation_diversity_established": false
}
JSON
printf '%s\n' "$VERSION_OUTPUT"
