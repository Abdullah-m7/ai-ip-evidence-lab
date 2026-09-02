# Paper A — Source, Claim, and Submission Audit

## Audit status

**MANUSCRIPT NARROWED TO STAGE 014 CORRECTED-PROFILE EVIDENCE — MAJOR REVISION CONTINUES — NOT JOURNAL-SUBMISSION READY**

The manuscript is a standalone scholarly draft with in-text citations, a formatted working bibliography, explicit source hierarchy, result tables, threats to validity, declarations, and a fail-closed structural claim/citation audit.

Following the Stage 014 controller decision (`NARROW_AND_CONTINUE`, `review/STAGE_014_CONTROLLER_DECISION.md`), the manuscript now reports corrected record profile `0.2.0` evidence for its central claims and marks all record profile `0.1.0` results as legacy. No new external source was admitted during that revision.

The previous bibliographic-thinness HOLD is closed. Remaining HOLDs concern the outstanding Stage 014 submission gates (ecological trace or explicit acceptance of its absence, 2026 closest-prior-work integration, independent scholarly review) and submission packaging.

## 1. Source hierarchy

Paper A uses the following authority order:

1. official Arabic Saudi legal text for Saudi-law propositions;
2. official legislation and government reports for comparative-jurisdiction descriptions;
3. normative specifications for C2PA, CAWG, and TDM·AI propositions;
4. peer-reviewed or authoritative scholarly literature for related-work positioning;
5. committed project reports and machine outputs only for claims about IPEL experiments.

Project documentation is never treated as external authority for a legal proposition or standard specification.

## 2. Saudi legal-claim audit

| Manuscript proposition | Primary source | Audit |
|---|---|---|
| Royal Decree M/169 approved the 2026 Copyright Law | official Royal Decree | PASS |
| Article 26(4) addresses copying an original work for AI products/algorithms subject to stated conditions | official Copyright Law | PASS |
| Article 37(1) imposes a cross-cutting condition on Article 26–36 uses (normal exploitation; unjustified prejudice to legitimate interests) | official Copyright Law | PASS — added to the declared scope in Stage 012 |
| Article 30 applies to the Article 26(4) pathway and contains six groups of controls | official Implementing Regulations | PASS |
| Article 30(3) requires retained records of work type, source, purpose, and date | official Implementing Regulations | PASS |
| The four fields are a minimum record core rather than a complete compliance test | clearly identified project interpretation | PASS — bounded |

Mandatory boundary retained: the Arabic official text governs, and the IPEL mapping is neither a SAIP interpretation nor a judicial conclusion.

## 3. Comparative-law audit

The revised manuscript now cites official or scholarly sources for:

- the EU Digital Single Market Directive TDM framework;
- the United States Copyright Office generative-AI training report;
- Japan’s official non-binding AI-and-copyright overview;
- the United Kingdom’s 2026 copyright-and-AI report;
- comparative scholarship covering materially different jurisdictional approaches.

Audit: **PASS for contextual positioning**.

Boundary: Paper A does not infer that any comparative jurisdiction uses the Saudi elements or that one system supplies a universally correct model.

## 4. Technical-standard audit

| Proposition | Normative source | Audit |
|---|---|---|
| C2PA binds assertions and supplies validation/trust infrastructure | C2PA 2.4 | PASS |
| C2PA supports collection hashes and AI/ML Ingredient relationships | C2PA 2.4 | PASS |
| C2PA validation is not a normative “good/bad” legal judgment | C2PA scope text | PASS |
| CAWG 1.1 communicates machine-readable training/data-mining usage signals | CAWG 1.1 | PASS |
| TDM·AI communicates AI/TDM preferences | official TDM·AI documentation | PASS |
| Preference signals are not silently substituted for every fact in the Saudi pathway | project design/experiment claim, not attributed to the standards | PASS — correctly separated |

## 5. Scholarly-literature audit

The manuscript now contains literature in four adjacent fields:

1. substantive AI-training copyright doctrine and comparison;
2. dataset statements, datasheets, model cards, data cards, and provenance audits;
3. reviewability and internal algorithmic auditing;
4. computational law, formal compliance checking, open texture, and legislation encoding.

IPEL is positioned as a bounded legal-evidence profile among established documentation, rights-signaling, provenance, auditability, and computational-law traditions. Per the Stage 011 novelty threat register and the Stage 014 controller decision, the manuscript concedes that reviewability, evidentiary record duties, transparency insufficiency, training-data provenance verification, and C2PA-based rights management all predate this work, and claims novelty only for the conjunction recorded as claim C30 in the claim–evidence matrix.

Controller source verification admitted the closest works individually: Li (2026), Lucchi (2026), Park (2025), Krishna, Shree, and Raguram (2026), Xie et al. (2025), and Qi et al. (2026). The rights-expression lineage is also explicit through ODRL 2.2, RightsML, ccREL, and the 2026 ODRL AI Vocabulary draft (identified as a draft, not a W3C Recommendation).

Audit: **PASS against Stage 014 submission gate 2**.

## 6. Project-result audit

Every numerical or categorical result admitted to the Results section maps to a committed repository artifact:

| Result | Repository evidence | Audit |
|---|---|---|
| Stage 002: 4/6 attacks detected internally, 6/6 against a preserved checkpoint; `integrity_verified != claim_truth_verified` | `reports/STAGE_002_REPORT.md`, `reports/stage002_attack_matrix.json` | PASS — bounded to six committed fixtures; used as a design-selection negative result |
| Stage 003: 0/5 cases with semantic loss; 5/5 gate outcome preservation; 2/2 false-equivalence attacks resisted | Stage-003 narrative and machine reports | PASS — **LEGACY profile `0.1.0` only**; must carry the legacy label |
| Stage 003: 0/4 Article 30(3) core fields delegated in the tested mapping | Stage-003 profile/report | PASS — **LEGACY profile `0.1.0`**, pre-rubric criterion; explicitly not an impossibility theorem; superseded for profile `0.2.0` by the Stage 014 result below |
| Stage 012: declared scope corrected to Art. 26(4) + Art. 37(1) + Reg. Art. 30; `0.1.0` reports `declared_scope_complete=false` | `reports/STAGE_012_ART37_REMEDIATION.md` | PASS |
| Stage 013: rubric `1.0.0` and candidate registry hash-locked before any outcome (`PRE_OUTCOME_RUBRIC_LOCK`) | `reports/STAGE_013_RUBRIC_REPORT.md` | PASS |
| Stage 014: 59 cases / 13 conditions; 59/59 outcomes and expected findings reproduced | `benchmarks/stage014/generated/condition_state_benchmark.json` | PASS |
| Stage 014: 0/4 Article 30(3) core fields and 0/2 Article 37(1) propositions safely delegable; 1 `SAFE_DELEGATION` (`work.title`), 8 `PARTIAL_SUPPORT`, 0 `NOT_SAFE_TO_DELEGATE`, 2 `NO_CANDIDATE` | `benchmarks/stage014/generated/delegation_assessment_results.json` | PASS — bounded by the frozen registry; assessments not independently adjudicated |
| Stage 014: 9 round-trips executed, 1 passing, 7 gate-silent semantic corruptions | `benchmarks/stage014/generated/delegation_roundtrip.json` | PASS |
| Stage 014: 55 constructible profiles, 55/55 preserving gate outcome, both statutory tuples, and zero semantic loss; 4 fail-closed | `benchmarks/stage014/generated/corrected_profile_roundtrip.json` | PASS |
| Stage 014: naïve baseline 31/59 and 29/59 preserved, 28/14 false equivalences, 0/16 spurious escalations, 557/1278 lost leaf paths, 44/59 signal-driven instability; rubric-governed 59/59 | `benchmarks/stage014/generated/naive_baseline_comparison.json` | PASS — declared project comparator, not an observed third-party system |
| Stage 004: clean validation and three distinct corruption codes | Stage-004 report/machine output | PASS |
| Stage 004: valid claim signature with untrusted development signer | Stage-004 report | PASS |
| Stage 004: process exit success did not substitute for report validation state | Stage-004 report | PASS |
| Stage 005: same normalized categories on two different observed c2pa-rs versions | Stage-005 report | PASS |
| Stage 005: shared implementation lineage | Stage-005 report | PASS |
| Stage 005: signed unsupported TDM value rejected semantically | Stage-005 report/tests | PASS |

Stages 006–008 are discussed only as future-study infrastructure. Their implementation is not counted as evidence that humans benefit from IPEL.

## 7. Human-data firewall

The manuscript contains no claimed human result.

Blocked until a separately governed study exists:

- improved reviewer accuracy or missing-information recall;
- lower false-ready rates;
- reduced assessment time;
- increased inter-reviewer agreement;
- expert-validated ground truth;
- successful real recruitment, consent, or adjudication.

The manuscript states that Stage-006 labels are project-authored and that Stages 007–008 contain no real adjudication or human responses.

Audit: **PASS**.

## 8. Mandatory limitations

The following limitations are present in the manuscript and machine-audited:

- the contribution is not automated copyright compliance;
- `legal_conclusion=false` remains visible;
- integrity does not prove truth, lawful acquisition, ownership, permission, or legal compliance;
- `0/4` is scoped to the tested mapping, the frozen candidate registry, and rubric `1.0.0`;
- the Stage 014 rubric assessments are analyst judgements and are not independently adjudicated;
- the evidence gate did not detect 7 of 9 bad delegations;
- two encoded conditions have no adverse state and three have no unresolved state in profile `0.2.0`;
- one record fixture underlies all 59 corrected-profile cases;
- the naïve baseline is a project-declared comparator, not an observed third-party system;
- `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED` is stated verbatim;
- completed cases are synthetic and technically bounded, and no ecological trace has been executed;
- evidentiary sufficiency conflicts with minimization, confidentiality, and retention risk, and that tradeoff is discussed but not measured;
- public-repository blinding is procedural rather than cryptographic;
- Stage 008 does not authenticate a human response before intake;
- the legal mapping is non-authoritative and version-sensitive.

Audit: **PASS**.

## 9. Machine audit

`scripts/audit_paper_a.py` now checks, fail-closed:

- required manuscript sections;
- minimum manuscript length;
- admitted in-text citation keys and corresponding bibliography entries;
- separate source-audit coverage;
- mandatory evidence boundaries;
- committed numerical result values;
- prohibited affirmative overclaims;
- citation placeholders;
- claim-matrix boundaries; and
- a minimum floor of persistent scholarly identifiers.

`tests/test_paper_a_audit.py` verifies both the current passing manuscript and failure after injecting an affirmative legal overclaim or removing the implementation-diversity limitation.

This is a structural audit only. It does not replace legal review, source-truth verification, peer review, plagiarism screening, or copy-editing.

## 10. Remaining submission gates

Before submission to *Artificial Intelligence and Law*, complete:

1. journal-style conversion and final word-count/category check;
2. publisher-metadata verification for every reference and full author list;
3. line-level legal translation review against the official Arabic text;
4. independent scholarly red-team review of novelty and methods;
5. English-language copy-editing;
6. anonymized review package if required;
7. persistent archival snapshot/identifier for code and artifacts;
8. cover letter, declarations, author affiliation, and corresponding-author details;
9. final journal-policy checks for code, data, generative-AI disclosure, and supplementary materials.

None of these gates requires adding speculative engineering features.

## 11. Controller decision

The governing decision is the Stage 014 controller decision: **`NARROW_AND_CONTINUE`** — continue Paper A under major revision; do not withdraw. That decision is a scientific-scope decision, not a submission-readiness decision, and is not modified by this audit.

Stage 014 submission gates and their current state:

| Gate | State |
|---|---|
| 1. Manuscript rewritten around the narrowed novelty position and corrected Stage 014 results | addressed in this revision |
| 2. 2026 closest-prior-work and rights-expression literature integrated explicitly | **addressed** — individually source-verified and cited |
| 3. Stage 002 integrity negative result restored to the empirical narrative | addressed (manuscript §5.2, §6.1) |
| 4. Ecological, lawfully usable trace added, or its absence explicitly accepted as a venue-limiting weakness | **open** — the absence is now stated explicitly (manuscript §8.5, §9); adding a trace remains a separate bounded decision |
| 5. Evidentiary sufficiency versus minimization/confidentiality/retention risk addressed | addressed (manuscript §8.7) |
| 6. All legacy `0.1.0` wording audited so no corrected-profile implication remains | addressed (manuscript §5.8, §6.7; matrix C5/C6) |

Paper A remains **MAJOR_REVISION**. Paper B remains blocked until real adjudication and human-study governance exist.
