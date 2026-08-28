# Stage 005 Report — Cross-Validator / Trust Boundary

## Result
**PASS**, with one deliberate limitation: `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`.

## Findings
1. The clean real C2PA artifact has the same normalized cryptographic meaning on both validation surfaces.
2. The three Stage-004 corruption classes are detected by both surfaces with the same standard failure category:
   - bound asset → `assertion.dataHash.mismatch`;
   - signed assertion → `assertion.hashedURI.mismatch`;
   - claim/signature → `claimSignature.mismatch`.
3. The two surfaces share c2pa-rs lineage but exercise different observed c2pa-rs versions: `0.90.16` versus `0.78.0`.
4. Default trust classifies the development signer as `untrusted`; explicitly adding its certificate chain to a custom test trust list changes the same cryptographically valid artifact to `trusted`.
5. That trust transition does not change any IPEL legal fact or legal-gate outcome.
6. `CAWG allowed + acquisition_status=false` remains `FAIL_EVIDENCE_GATE` in both trust contexts.
7. `CAWG allowed + transformed output without permission` remains `FAIL_EVIDENCE_GATE` in both trust contexts.
8. A cryptographically valid, signed TDM assertion containing `use=maybe` is rejected semantically by both IPEL normalizers. Cryptographic validity therefore cannot be used as metadata-semantic validity.
9. A source file with no manifest is rejected by both command-line surfaces.

## Reproducibility finding
The pinned `c2pa-conformance-tool-cli` commit cannot currently be reconstructed literally because one historical submodule source (`lrosenthol/profile-evaluator-rs` at `c43d111...`) is unavailable.

Stage 005 records and tests a bounded compatibility repair using moved/current Adobe profile/json-formula commits while retaining the historical c2pa-rs commit and Cargo.lock and building with `--locked`.

This repair is machine-visible in the installed-tool provenance sidecar and in the Stage-005 report. It is not described as exact upstream reproduction.

## Novelty implication
Stage 005 strengthens the separation central to IPEL:

`cryptographic integrity` → evidence about artifact integrity

`signer trust` → trust-policy classification

`CAWG usage signal` → machine-readable usage preference/constraint

`IPEL legal evidence` → jurisdiction-specific facts needed for legal review

None of the first three is allowed to collapse into the fourth.

## Article 30(3)
New minimum-record fields safely delegated to C2PA after cross-validation: **0/4**.

The cross-validator strengthens confidence in the integrity boundary but does not create a normative equivalent for work type, work source, purpose of use or date of use.
