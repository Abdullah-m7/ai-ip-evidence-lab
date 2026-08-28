# Stage 004 Report — Real C2PA Hard Binding

## Result
**PASS — bounded claim only.** A real C2PA manifest was generated and validated with pinned `c2patool 0.27.16`. The experiment supports cryptographic/provenance integrity claims while preserving the boundary against legal inference.

## Empirical outcomes
| Test | Result | Machine evidence |
|---|---|---|
| Clean generated artifact | PASS | `validation_state=valid`, `assertion.dataHash.match`, `claimSignature.validated` |
| Signer trust | intentionally not established | `signingCredential.untrusted` |
| Exactly one-byte asset mutation | DETECTED | `assertion.dataHash.mismatch` |
| Assertion payload corruption | DETECTED | `assertion.hashedURI.mismatch` |
| Signing-credential byte corruption | DETECTED | `claimSignature.mismatch` |
| CAWG `allowed` + unlawful acquisition | legal gate remains FAIL | no C2PA→legal overwrite |
| CAWG `allowed` + no output permission | legal gate remains FAIL | no C2PA→legal overwrite |

All Stage-004 acceptance gates in `reports/stage004_conformant_c2pa.json` are true.

## New finding: exit status is not validation status
During the mutation experiment, `c2patool` returned a structured Invalid report containing `assertion.dataHash.mismatch` while the process itself exited successfully. Any integration that equates CLI exit code 0 with a valid C2PA artifact can therefore create false assurance. IPEL's adapter parses the report semantics instead.

## Trust finding
The clean artifact is cryptographically valid but signed by c2patool's built-in development credential. The signature validates while the signer remains untrusted. This demonstrates why `claim_signature` and `signer_trust` must remain separate evidence dimensions.

## Interoperability conclusion
Stage 004 changes the integrity story but not the legal-semantic boundary. Actual C2PA hard binding provides much stronger evidence that bytes/assertions have not changed than the Stage-003 intermediate model, yet it still does not prove lawful acquisition, publication, ownership, permission, market effect, or compliance with Saudi law.

## Article 30(3) result
Newly delegated fields: **0/4**.

The four retained legal-evidence fields remain:
1. work type;
2. source;
3. purpose of use;
4. date of use.

## Research limitation
The generated artifact is verified using the maintained C2PA implementation that created it. Stage 004 does not claim independent cross-implementation interoperability or C2PA Conformance Program certification. A later stage can add a second implementation/conformance validator and broaden the benchmark corpus.
