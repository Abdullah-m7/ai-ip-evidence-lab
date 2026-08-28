# Stage 005 — Cross-Validator C2PA Trust-Boundary Benchmark

## Question
Does the Stage-004 result survive a second standards-maintained validation surface and an explicit trust-list change?

Stage 005 compares:
1. `c2patool 0.27.16` Reader output;
2. `c2pa-conformance-tool-cli` / `c2pa-validate 0.2.0` crJSON output;
3. default versus custom signer trust;
4. the independent IPEL legal-evidence gate.

## Important limitation: not an independent cryptographic implementation
The conformance CLI directly depends on `vendor/c2pa-rs/sdk`. The Stage-004 generator/reader and Stage-005 cross-validator therefore share the **c2pa-rs implementation lineage**.

The experiment does establish a useful **cross-version** check:
- Stage-004 artifact reports `org.contentauth.c2pa_rs = 0.90.16`;
- the pinned conformance CLI emits `jsonGenerator.version = 0.78.0`.

The report consequently states `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED` rather than describing the two surfaces as independent implementations.

## Pinned conformance source
- repository: `contentauth/c2pa-conformance-tool-cli`
- commit: `c09f0340524b088a81475f7b7eaab5ba7042772f`
- CLI version: `0.2.0`
- historical Cargo.lock SHA-256: `80dcab12a2773a6cffd3c6c8794640d0be9cff3a9227d7abd44143e963fa6fd0`
- Rust: `1.98.0`
- declared c2pa-rs submodule: `61f2e676043c1d22fa60f4fe5d09d3874c7c8a10`

## Upstream reproducibility defect and bounded repair
The pinned conformance commit declares three git submodules. Its historical `vendor/profile-evaluator-rs` entry points to `lrosenthol/profile-evaluator-rs` at commit `c43d11162c27c5e992c7010fc75b72bb3e5520e1`. On 28 August 2026 that repository/commit is no longer retrievable from the declared location.

A literal checkout of the pinned commit is therefore not a complete reproducible source graph today.

Stage 005 does **not** hide this. The installer records a compatibility repair:
- keep c2pa-rs at the exact declared commit `61f2e676...`;
- replace the unavailable profile source with moved/current `adobe/profile-evaluator-rs` commit `40c4201933e3b4760932b65913e2a9c57413f8ac`;
- replace the historical json-formula source with compatible moved/current `adobe/json-formula-rs` commit `90ee7f44ded98c657a410a0bf1248a9e3f6f1627`;
- restore the historical package version labels (`0.1.0`) required by the pinned Cargo.lock;
- remove only profile-evaluator WASM/dev-only dependency sections for this native CLI build;
- build with `cargo --locked`, leaving the historical lockfile unchanged.

This is a **reproducibility repair build**, not an exact historical source reconstruction.

## Benchmark cases
- clean valid artifact;
- one-byte bound-asset mutation;
- one-byte signed-assertion corruption;
- one-byte signing-credential corruption;
- valid signed assertion with malformed CAWG TDM value `maybe`;
- no-manifest negative control;
- valid CAWG `allowed` plus explicit unlawful acquisition;
- valid CAWG `allowed` plus transformed output without recorded permission;
- clean artifact under default trust and under a custom test trust list built from its development certificate chain.

## Normalization
Raw Reader JSON and crJSON are intentionally not compared byte-for-byte. Manifest UUIDs, instance IDs, certificate material and report-generation timestamps are not the research endpoint.

`src/ipel/c2pa_crosscheck.py` maps both surfaces into common observations:
- cryptographic validity;
- asset binding;
- claim signature;
- assertion-reference integrity;
- signer trust;
- valid CAWG TDM entries;
- semantic warnings;
- success/failure codes.

No normalized object contains lawful-publication, lawful-acquisition, ownership, permission-validity or legal-compliance fields.

## Trust experiment
Under the default trust mode, the built-in c2patool development signer is `untrusted` while its signature and data hash are valid.

The certificate chain is then explicitly supplied to the conformance CLI as a **custom test trust list**. The same clean artifact changes to `signingCredential.trusted` while cryptographic validity remains unchanged.

That trust change is intentionally prevented from affecting the IPEL legal gate.

## Semantic-validity experiment
A separate artifact is correctly signed and hash-bound but contains:

`cawg.ai_training.use = "maybe"`

Both cryptographic surfaces accept its cryptographic integrity. The IPEL normalizers reject the value as an invalid TDM semantic and emit a warning. This demonstrates:

**signed metadata ≠ semantically valid metadata**.

## Reproduce
```bash
./scripts/install_c2patool.sh .tools/c2patool
./scripts/install_c2pa_conformance_tool.sh .tools/c2pa-validate
PYTHONPATH=. python3 experiments/stage005_cross_validator.py \
  --c2patool .tools/c2patool \
  --cross-validator .tools/c2pa-validate \
  --output reports/stage005_cross_validator.json
python3 -m unittest discover -s tests -v
```
