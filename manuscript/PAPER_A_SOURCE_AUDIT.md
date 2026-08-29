# Paper A — Source, Claim, and Submission Audit

## Audit status

**CITATION INSERTION COMPLETE — CONTROLLER REVIEW READY — NOT YET JOURNAL-SUBMISSION READY**

The manuscript is now a standalone scholarly draft with in-text citations, a formatted working bibliography, explicit source hierarchy, result tables, threats to validity, declarations, and a fail-closed structural claim/citation audit.

The previous bibliographic-thinness HOLD is closed. The remaining HOLD concerns submission packaging and independent scholarly review, not missing core manuscript architecture.

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

This substantially strengthens the novelty argument. IPEL is no longer positioned against a single provenance paper; it is positioned as a bounded legal-evidence layer among established documentation, rights-signaling, provenance, auditability, and computational-law traditions.

Audit: **PASS for internal controller review**.

## 6. Project-result audit

Every numerical or categorical result admitted to the Results section maps to a committed repository artifact:

| Result | Repository evidence | Audit |
|---|---|---|
| Stage 003: 0/5 cases with semantic loss; 5/5 gate outcome preservation; 2/2 false-equivalence attacks resisted | Stage-003 narrative and machine reports | PASS |
| Stage 003: 0/4 Article 30(3) core fields delegated in the tested mapping | Stage-003 profile/report | PASS — explicitly not an impossibility theorem |
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
- `0/4` is scoped to the tested mapping;
- `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED` is stated verbatim;
- completed cases are synthetic and technically bounded;
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

**GO for CI-backed controller review and merge of Stage 009 once all checks pass.**

After merge, the next work package should be a submission package and independent manuscript review—not Stage 010 feature expansion. Paper B remains blocked until real adjudication and human-study governance exist.
