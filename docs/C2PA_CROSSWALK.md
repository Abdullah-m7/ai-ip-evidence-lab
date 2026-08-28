# IPEL ↔ C2PA Crosswalk — Stage 002

**Reference baseline:** C2PA Specifications 2.4 AI/ML guidance and CAWG Training and Data Mining Assertion 1.1, reviewed 28 August 2026.

## Design principle
IPEL must not claim novelty for generic provenance, signing, asset hashing, dataset ingredients, or rights-preference metadata. C2PA already provides mature mechanisms for cryptographically bound Content Credentials, while its AI/ML guidance explicitly covers models, training datasets, ingredients, hashes, and model outputs.

The research question is narrower: **which Saudi copyright evidence facts can reuse C2PA semantics, and which remain jurisdiction-specific facts or legal judgments?**

| Saudi / IPEL fact | Closest C2PA / CAWG mechanism | Equivalence | Stage-002 interpretation |
|---|---|---|---|
| Work/dataset identity | Asset type assertion; ingredient | Partial | Good asset identity/provenance primitive; not a legal work classification by itself. |
| Source URI | Asset Reference Assertion / ingredient URI | Strong technical overlap | Reuse rather than invent a second URI mechanism. |
| Content digest | Data hash / collection data hash / hard binding | Strong technical overlap | C2PA is preferable for interoperable content binding. |
| Dataset used to train model | Training-dataset ingredient; AI/ML Training Data Set Content Credential | Strong provenance overlap | Can show dataset/model relationship; not necessarily the Saudi statutory purpose statement. |
| Type of use / AI training permission preference | `cawg.training-mining` entries (`allowed`, `notAllowed`, `constrained`) | Partial | Valuable rights signal. It does not itself prove licence validity, actor authority, or applicability of a statutory exception. |
| Purpose of use (IR 30(3)) | Ingredient relationship / AI-ML workflow metadata | Partial | IPEL still needs an explicit jurisdictional purpose fact unless a stable C2PA semantic is proven equivalent. |
| Date of use (IR 30(3)) | C2PA provenance/timestamp metadata | Partial | A timestamp can carry evidence; trusted time and the legally relevant "date of use" remain separate questions. |
| Lawful publication (Law 26(4)) | No direct C2PA equivalent | None | Requires external evidence/legal assessment. |
| Lawful acquisition (Law 26(4)) | Source/ingredient/rights assertions can support evidence | None-to-partial | Provenance of bytes is not proof of lawful acquisition. |
| Necessity / proportionality (Law 26(4), IR 30(1)) | No generic C2PA equivalent | None | Judgment-sensitive Saudi evidence field. |
| No republication/distribution/direct exploitation | C2PA actions/provenance can record events | Partial | C2PA can support event evidence but does not make the Saudi legal classification. |
| Market / legitimate-interest prejudice (IR 30(4)) | No direct equivalent | None | Human legal/economic assessment with evidentiary basis. |
| Permission/public-domain status (IR 30(5)) | TDM assertion and other metadata may communicate rights signals | Partial | Signed assertion ≠ legally valid permission unless authority/scope are established. |
| Independently protected elements (IR 30(6)) | Ingredients can identify components | Partial | Component provenance helps discovery; rights analysis remains external. |
| Tamper evidence | Signed C2PA claim + content binding | C2PA stronger | Stage-002 hash chain is experimental; production should reuse mature signing/trust infrastructure. |
| Actor identity/authority | C2PA signer; CAWG identity ecosystem | Partial | Identity/trust signal can support evidence; legal authority still needs verification. |

## Current C2PA facts that constrain our architecture

C2PA 2.4 states that Content Credentials can be applied to AI/ML datasets, software, and models to detect tampering. For large or external datasets, manifests can be sidecars and can use Asset Reference Assertions and hashes. The AI/ML guidance also models training datasets as ingredients of a model and recommends provenance for dataset partitions and model checkpoints.

CAWG Training and Data Mining Assertion 1.1 distinguishes data mining, AI inference, generative training, and non-generative training. Each can be `allowed`, `notAllowed`, or `constrained`.

## Non-equivalence rule

A C2PA validation success must never be translated into `lawful_acquisition=true`, `lawful_publication=true`, or `Saudi_exception_satisfied=true` without separate evidence and rule evaluation.

This follows the same conceptual boundary as C2PA itself: provenance validation establishes association, structure, integrity, and trust signals—not a value judgment that the underlying assertion is legally true.

## Integration options

### A. IPEL sidecar bound as a C2PA asset/ingredient
Low implementation risk, but duplicates some envelope metadata.

### B. IPEL jurisdictional custom assertion inside a C2PA Manifest
Best cryptographic integration, but premature before the IPEL semantic core and privacy model stabilize.

### C. IPEL legal-evidence profile references C2PA manifests
C2PA carries generic asset provenance/integrity; IPEL carries Saudi-specific factual and judgment-sensitive fields plus references to C2PA claims/manifests.

**Stage-002 recommendation: Option C.** It minimizes reinvention and keeps the legal-evidence layer separable from a generic provenance standard.

## Sources

- C2PA Specifications 2.4, Guidance for Artificial Intelligence and Machine Learning: https://spec.c2pa.org/specifications/specifications/2.4/ai-ml/ai_ml.html
- CAWG Training and Data Mining Assertion 1.1: https://cawg.io/training-and-data-mining/1.1/
