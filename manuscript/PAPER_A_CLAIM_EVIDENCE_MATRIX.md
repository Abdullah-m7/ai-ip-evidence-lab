# Paper A — Claim–Evidence Matrix

This matrix is the controller gate for the first manuscript. A claim may enter the Results section only if it is supported by a committed artifact or an external authoritative source. Human-effect claims are prohibited until real data exist.

| ID | Proposed claim | Evidence source | Allowed wording | Forbidden overclaim |
|---|---|---|---|---|
| C1 | Saudi Copyright Law Article 26(4) permits copying an original work for AI product/algorithm development subject to lawful publication, lawful acquisition of the original copy, and copying limited to purpose | Official Umm Al-Qura Copyright Law; `docs/LEGAL_REQUIREMENTS_MATRIX.md` | “Article 26(4) creates a fact-conditioned AI-development copying exception.” | “Saudi law generally authorizes AI training.” |
| C2 | Implementing Regulation Article 30(3) requires retained records of work type, source, purpose, and date of use | Official Umm Al-Qura regulation; `docs/LEGAL_REQUIREMENTS_MATRIX.md` | “Article 30(3) expressly requires a four-field retained-record core.” | “These four fields are sufficient for legal compliance.” |
| C3 | Other Article 30 conditions include necessity, restrictions on republication/distribution/direct commercial exploitation, author-interest/normal-exploitation considerations, final-product inclusion limits, and independent protected elements | Official regulation Art. 30(1)–(6); matrix | “The retained-record core sits inside a broader set of fact-sensitive conditions.” | “Every condition is machine-decidable.” |
| C4 | IPEL intentionally distinguishes explicit contradiction, evidentiary uncertainty, and evidentiary sufficiency without issuing a legal conclusion | `src/ipel/validator.py`, Stage-001 report/tests | “The gate is an evidence-readiness instrument, not a legal adjudicator.” | “IPEL determines legality.” |
| C5 | Stage 003 preserved all tested leaf values and gate outcomes across five synthetic round-trip cases | `reports/STAGE_003_REPORT.md`, `reports/stage003_semantic_roundtrip.json` | “In the five-case tested profile, semantic loss was zero and gate outcomes were preserved 5/5.” | “IPEL is lossless under all C2PA mappings.” |
| C6 | In the tested Stage-003 mapping, none of the four Article 30(3) core fields was safely delegated to C2PA | Stage-003 report/profile code | “0/4 core fields were delegated in the tested mapping.” | “C2PA can never represent these facts.” |
| C7 | Real C2PA hard binding detected three distinct corruption classes in Stage 004 | `reports/STAGE_004_REPORT.md`, machine report | “The tested one-byte asset mutation, assertion corruption, and claim-signature corruption were detected.” | “C2PA detects all provenance attacks.” |
| C8 | The clean Stage-004 artifact had a valid signature while signer trust remained unestablished | Stage-004 report | “Cryptographic validity and signer trust were empirically separable in the test.” | “An untrusted signer implies invalid content.” |
| C9 | `c2patool` process success did not guarantee artifact validation success in the mutation experiment | Stage-004 report/logged result | “The integration must parse validation semantics rather than rely on process exit code.” | “c2patool is unreliable.” |
| C10 | CAWG `allowed` did not overwrite explicit unlawful acquisition or missing output permission in IPEL | Stage-003/004/005 tests | “A machine-readable usage signal was not treated as a substitute for the project’s jurisdiction-specific legal-evidence facts.” | “CAWG `allowed` is legally meaningless.” |
| C11 | Stage 005 obtained the same normalized corruption categories on two validation surfaces using different observed c2pa-rs versions | `reports/STAGE_005_REPORT.md` | “Cross-version agreement was observed for the three tested corruption classes.” | “Independent implementation diversity was established.” |
| C12 | Stage 005 did not establish independent cryptographic implementation diversity | Stage-005 report | Explicitly state `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`. | Any “independent implementations confirmed…” wording. |
| C13 | A signed TDM assertion with unsupported `use=maybe` could remain cryptographically valid while semantic validation rejected the value | Stage-005 report/tests | “Cryptographic validity did not imply metadata-semantic validity in the tested malformed assertion.” | “Signed metadata are generally untrustworthy.” |
| C14 | The Stage-006 benchmark contains 24 balanced synthetic cases with exact factual parity between baseline and IPEL renderings | `reports/STAGE_006_REPORT.md`, generated audit | “The future human-study benchmark is structurally balanced and deterministic.” | “IPEL improves reviewer performance.” |
| C15 | Eight Stage-006 cases are evidence-ready despite a machine-gate FAIL, demonstrating readiness ≠ favorable legal outcome in the benchmark design | Stage-006 report | “The benchmark explicitly separates observability from legal favorability.” | “Eight real legal cases were correctly adjudicated.” |
| C16 | Stage 007 freezes a procedural adjudication design but has no real adjudication data | `reports/STAGE_007_REPORT.md`, lock manifest | “Independent content validation is preregistered but not yet performed.” | “Independent experts validated the benchmark.” |
| C17 | Stage 008 creates contamination-resistant distribution/intake infrastructure but no human results | `reports/STAGE_008_REPORT.md` | “Operational safeguards for future adjudication are implemented.” | “Human provenance/authorship is cryptographically verified.” |
| C18 | WIPO AIII treats metadata, identifiers, authentication, watermarking, rights-management and provenance infrastructure as a distinct technical/operational IP layer | WIPO AIII official sources | Use to motivate infrastructure-level problem. | Imply WIPO endorses IPEL or any legal interpretation. |
| C19 | Data Provenance Initiative documents widespread license/attribution problems and develops dataset lineage/audit infrastructure | Longpre et al., Nature Machine Intelligence 2024 | “Dataset lineage and licensing documentation are an adjacent but different problem layer.” | “DPI provides legal compliance proof.” |
| C20 | CAWG and TDM·AI communicate machine-readable usage preferences/constraints rather than a complete legal basis for copying | CAWG 1.1; TDM·AI official docs | “Preference protocols address rights signaling; IPEL addresses later evidentiary reconstruction.” | “Preference protocols are irrelevant to copyright compliance.” |

## Claims reserved for Paper B

The following claims are **blocked** until real, properly governed human data exist:

- IPEL improves missing-information recall.
- IPEL reduces false-ready classifications.
- IPEL reduces inter-reviewer disagreement.
- IPEL reduces assessment time.
- Objective cases have lower human uncertainty than judgment-sensitive cases.
- Independent adjudicators validate or revise the Stage-006 author labels.

## Mandatory red-team wording check

Before submission, search the manuscript for the following phrases and inspect each occurrence manually:

- `proves compliance`
- `ensures compliance`
- `legal validity`
- `independent implementation`
- `human validation`
- `expert validated`
- `reviewer improvement`
- `cryptographically blind`
- `lawful because`
- `C2PA proves`
- `CAWG permission`

Any occurrence requires direct evidence or narrower wording.
