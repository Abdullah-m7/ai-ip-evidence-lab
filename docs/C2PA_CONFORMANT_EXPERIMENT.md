# Stage 004 — Real C2PA Manifest / Hard-Binding Experiment

## Scope
Stage 004 leaves the Stage-003 intermediate representation and uses the maintained `contentauth/c2pa-rs` command-line tool to create and validate a real C2PA manifest embedded in a JPEG test asset.

This stage does **not** claim that AI-IP Evidence Lab, c2patool, or the generated artifact has received C2PA Conformance Program certification. The narrower claim is reproducible: the artifact is generated and validated by the pinned maintained C2PA implementation used in this experiment.

## Pinned toolchain
- repository: `contentauth/c2pa-rs`
- release: `c2patool-v0.27.16`
- published: 2026-08-27
- macOS universal archive SHA-256: `2c2cd9f949c7231a71bce26b0d4f7e7b45db2128bf93cd0e3189ad0172e9039e`
- Linux x86_64 archive SHA-256: `62eed34f0c90a24b696b1969c8aad4340e11ec7264e1cf6fc375ad15c1db7663`

The installer in `scripts/install_c2patool.sh` verifies the release archive digest before installing the binary.

Official implementation/release source: https://github.com/contentauth/c2pa-rs

## Synthetic asset
`examples/stage004/source.jpg` is a synthetic 32×32 JPEG created for this experiment. It contains a JPEG COM segment with `STAGE004-MUTATION-ANCHOR`, allowing an exactly one-byte, format-preserving post-signing mutation.

Frozen source SHA-256:
`652c561108a2961573a7dd10f720033359f650453ef33694f7dbc5fee29aae5e`

No third-party copyrighted content is needed for the experiment.

## Manifest construction
The experiment calls `c2patool` with `--create trainedAlgorithmicMedia`. The tool generates a `c2pa.created` action and a C2PA data-hash binding. The manifest definition also carries a CAWG `cawg.training-mining` assertion.

The constrained fixture declares:
- `cawg.ai_training = constrained`
- `cawg.ai_generative_training = notAllowed`

A second valid artifact declares `allowed` to test false legal equivalence.

CAWG TDM 1.1: https://cawg.io/training-and-data-mining/1.1/
C2PA 2.4 specification: https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html

## Development signer
For reproducibility, Stage 004 uses c2patool's built-in development certificate/key. c2patool explicitly warns that this signer is development-only. Consequently, the clean artifact has:
- `claimSignature.validated` — signature cryptographically validates;
- `assertion.dataHash.match` — asset binding validates;
- `assertion.hashedURI.match` — assertion references validate;
- `signingCredential.untrusted` — signer trust is not established.

This separation is deliberate. C2PA 2.4 distinguishes a **Valid Manifest** from a **Trusted Manifest**; signer trust requires the success code `signingCredential.trusted`.

## Adversarial tests
### A1 — one-byte asset mutation
One byte in the JPEG comment payload is flipped after signing. File length and JPEG structure remain intact.

Expected/observed C2PA failure: `assertion.dataHash.mismatch`.

### A2 — signed assertion corruption
One byte inside the embedded `notAllowed` value is flipped.

Expected/observed C2PA failure: `assertion.hashedURI.mismatch`.

### A3 — signing-credential / signed-manifest corruption
One byte in the embedded signing-credential material is flipped.

Expected/observed C2PA failure: `claimSignature.mismatch`.

## Important CLI behavior
`c2patool` may still exit with status code 0 while reporting an invalid artifact. Stage 004 therefore never treats process exit status as proof of validity. `src/ipel/c2pa_adapter.py` parses `validation_state` and structured validation codes.

## Legal boundary
C2PA evidence is represented independently from IPEL legal evidence. In particular:
- `cawg.* = allowed` does not establish lawful acquisition;
- `cawg.* = allowed` does not grant copyright permission;
- a valid claim signature does not establish ownership;
- a valid asset hash does not establish lawful publication;
- signer trust does not establish Saudi copyright compliance.

The experiment explicitly evaluates a cryptographically valid artifact with `cawg.ai_training = allowed` against an IPEL record with `acquisition_status = false`. The legal evidence gate remains `FAIL_EVIDENCE_GATE`.

## Delegation result
No Article 30(3) field is newly delegated in Stage 004. Real hard binding strengthens integrity of the provenance artifact, but it does not create a normative equivalence for work type, source, legal-use purpose, or legal-use date.

## Reproduce
```bash
./scripts/install_c2patool.sh .tools/c2patool
PYTHONPATH=. python3 experiments/stage004_conformant_c2pa.py \
  --c2patool .tools/c2patool \
  --output reports/stage004_conformant_c2pa.json
python3 -m unittest discover -s tests -v
```
