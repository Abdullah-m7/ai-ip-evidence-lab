# Stage 011 — Evidence-Driven Revision Plan

## Controller decision

**MAJOR REVISION — GO, but do not submit or retarget yet.**

The literature review does not invalidate Paper A. It narrows what can honestly be claimed as novel and identifies one material legal-scope omission plus several empirical weaknesses. Revision should therefore proceed in scientific-risk order, not in formatting order.

---

## Priority model

- **P0 — validity-threatening:** must be corrected before any journal decision.
- **P1 — acceptance-threatening:** likely major-reviewer objections; should be completed before submission.
- **P2 — strength/clarity:** materially improves the paper but does not currently invalidate the core result.
- **P3 — packaging:** only after scientific revision passes.

---

# Phase 1 — Legal completeness and novelty correction

## P0.1 Add Copyright Law Article 37(1) to the governing legal pathway

### Problem
The current scope uses Article 26(4) + Implementing Regulation Article 30. Article 37(1) imposes a cross-cutting statutory condition on uses under Articles 26–36 concerning normal exploitation and unjustified prejudice to legitimate interests.

### Required work
- Verify the controlling Arabic wording line-by-line against the official source.
- Expand the legal scope to:
  `Copyright Law Art. 26(4) + Art. 37(1) + Implementing Regulation Art. 30(1)–(6)`.
- Update `docs/LEGAL_REQUIREMENTS_MATRIX.md`.
- Review schema fields / gate logic for whether Art. 37 introduces a missing requirement or merely adds source authority to existing market-effect/author-interest fields.
- Add tests showing the legal-source mapping is complete at the declared scope.
- Update Paper A legal section and source audit.

### Acceptance gate
No manuscript claim may describe the mapped AI-development pathway as complete while Art. 37(1) is absent.

---

## P0.2 Rewrite novelty against the 2026 saturation review

### Drop as novelty
- “AI needs an evidence layer.”
- “Auditability/reviewability should be designed in.”
- “Transparency alone is insufficient.”
- “C2PA can support copyright/training provenance.”
- “Training-data provenance can be verified.”

### Retain as core contribution
1. statutory Saudi legal-to-evidence decomposition;
2. use-event-level executable evidence contract;
3. semantic barrier between legal evidence and provenance/trust/rights signals;
4. empirical false-equivalence tests;
5. real C2PA hard-binding validation as an integration test, not cryptographic novelty.

### Required citations
At minimum integrate and distinguish:
- Li 2026 — minimum reviewable trace;
- Lucchi 2026 — copyright auditability gap;
- Park 2025 — NFT + C2PA copyright management for AI training data;
- Krishna et al. 2026 — post-report provenance procedure;
- Buick 2025 — transparency insufficiency;
- Xie et al. 2025 / Qi et al. 2026 — model-side provenance detection.

### Acceptance gate
A skeptical reader should be able to understand in one paragraph exactly what these close works already do and exactly what IPEL tests that they do not.

---

# Phase 2 — Formalize the central semantic claim

## P0.3 Define semantic-equivalence/delegation rubric

The current phrase “sufficiently equivalent” is too discretionary.

### Required rubric
A generic provenance field can substitute for a jurisdiction-specific evidence field only when all required dimensions pass:

1. **referent equivalence** — same work/object/fact;
2. **event equivalence** — same lifecycle/use event;
3. **actor/issuer equivalence** — same entity whose act/assertion matters;
4. **temporal equivalence** — same time semantics;
5. **descriptive/normative equivalence** — no rights preference substituted for historical/legal fact;
6. **evidentiary-function equivalence** — field supports the same review proposition;
7. **qualifier preservation** — no legally material condition is lost;
8. **round-trip recoverability** — original legal-evidence value can be reconstructed without inference.

### Required experiment
- Apply rubric independently to each Article 30(3) field and all proposed generic mappings.
- Record per-dimension reasons for PASS/FAIL.
- Recompute the `0/4` result.
- If result changes, report the new result; do not preserve `0/4` for narrative convenience.

### Acceptance gate
`0/4` becomes a reproducible output of declared criteria rather than an expert judgment embedded in code.

---

# Phase 3 — Expand non-human empirical evidence

## P1.1 Replace the five-case proof-of-concept with condition-coverage benchmark

### Coverage target
Every condition in:
- Art. 26(4);
- Art. 37(1);
- Reg. 30(1)–(6)

must appear in controlled cases across logically possible states:
- favorable / supported;
- unresolved / unsupported;
- explicit adverse / contradictory.

### Additional case classes
- structural absence vs explicit adverse fact;
- conflicting evidence;
- malformed metadata;
- temporal changes in licence/right status;
- mixed rights / independently protected elements;
- downstream transformation/output permission;
- purely commercial / normal-exploitation cases;
- rights signal vs acquisition/publication/permission false equivalence.

### Selection rule
Do **not** target an arbitrary N. Build until condition × state coverage is complete and documented.

### Acceptance gate
A machine-readable coverage matrix shows no declared legal condition absent from the benchmark.

---

## P1.2 Add a naïve baseline / ablation

### Baseline candidates
A. **Naïve provenance substitution:** maps superficially similar C2PA/rights fields directly into legal-evidence fields.

B. **Flat record:** contains the same facts but no typed semantic barrier between provenance integrity, trust, rights signal, and legal status.

C. Optional **C2PA-only overlapping profile**.

### Metrics
- false-pass count/rate on controlled cases;
- legal-field semantic loss;
- round-trip loss;
- false-equivalence susceptibility;
- unresolved-condition masking.

### Acceptance gate
Paper A demonstrates a failure mode prevented by IPEL, rather than merely asserting that the design is safer.

---

## P1.3 Integrate Stage 002 as an integrity ablation

### Existing result
- internal hash-chain consistency detects 4/6 committed attacks;
- external checkpoint detects 6/6 in fixtures;
- full rehash and tail truncation pass internal-only verification.

### Manuscript role
Use Stage 002 as a design-selection negative result:

`naïve internal chain → boundary failure → need for external trust boundary → reuse mature C2PA infrastructure`.

### Acceptance gate
The manuscript does not portray the raw IPEL hash chain as production security and retains `integrity_verified != claim_truth_verified`.

---

# Phase 4 — Ecological and infrastructure validity

## P1.4 Add a small real/open ecological trace set

Use only lawfully accessible/open materials. Candidate categories:
- public-domain work;
- Creative Commons work with explicit licence;
- openly licensed dataset/document;
- controlled mock acquisition/use event referencing a real public licence.

### Purpose
Test whether the evidence contract can represent realistic:
- source URLs and redirects;
- licences/versions;
- acquisition evidence;
- nested/mixed metadata;
- timestamps;
- evidence references;
- provenance bindings.

### Non-claim
This is **not** a legal-compliance validation of the real work.

### Acceptance gate
At least one non-synthetic end-to-end trace executes through the evidence profile without relaxing legal/evidentiary boundaries.

---

## P1.5 Add rights-expression standards to related work

Distinguish IPEL from:
- W3C ODRL 2.2;
- IPTC RightsML;
- Creative Commons ccREL;
- ODRL AI Vocabulary/Profile work.

### Core distinction
`policy/rights expression` ≠ `historical evidence that a particular use event occurred under a particular factual basis`.

### Acceptance gate
A reviewer familiar with rights-expression standards cannot reasonably describe IPEL as an unacknowledged ODRL-like policy language.

---

## P1.6 Add evidence-retention vs privacy/confidentiality tension

### Required discussion
- evidence sufficiency vs data minimization;
- raw copy retention vs hashes/references;
- personal/confidential information in acquisition/use records;
- retention schedules / legal holds;
- access controls;
- litigation/discovery risks.

Use current copyright/privacy scholarship to show this is a design tradeoff rather than “more evidence is always better.”

### Acceptance gate
The architecture articulates a minimal-evidence principle rather than indefinite maximal retention.

---

# Phase 5 — Manuscript restructuring

## P1.7 Add explicit research questions

Recommended form:

- **RQ1:** Which facts/evidence must remain observable to review the Saudi AI-development copyright pathway?
- **RQ2:** Which of those facts can be safely represented/delegated through generic provenance or rights-expression standards without semantic loss?
- **RQ3:** What false-equivalence failures arise when cryptographic validity, signer trust, or rights signals are treated as legal facts?
- **RQ4:** What integrity properties are gained by progressively stronger provenance designs?

---

## P2.1 Recenter Results around comparative experiments

Preferred empirical sequence:

1. Stage 002 integrity ablation;
2. legal-condition coverage benchmark;
3. semantic-equivalence rubric + mapping result;
4. IPEL vs naïve baseline false-equivalence experiment;
5. real C2PA hard-binding attacks;
6. cross-version/trust/semantic validation;
7. ecological trace demonstration.

Human-study infrastructure moves to Future Work / supplementary material.

---

## P2.2 Add architecture figure and epistemic-layer table

Figure:

`Official legal source → versioned legal profile → evidence capture/use event → provenance binding → evidence gate → human/legal review`

Table:

| Layer | Example | What it can establish | What it cannot establish |
|---|---|---|---|
| Assertion | `acquisition_status=true` | stated claim | truth |
| Evidence reference | receipt/licence | referenced basis | authenticity/legal effect by itself |
| Integrity proof | hash/C2PA | binding/tamper signal | lawful acquisition |
| Rights expression | CAWG/ODRL | declared preference/policy | complete historical legal basis |
| Legal evidence profile | IPEL | structured review facts | final legal conclusion |

---

## P2.3 Clarify IPEL name

Explain that “Ledger” means a reviewable record/history abstraction and **does not imply blockchain**. If that remains confusing after external review, rename the expansion while retaining the IPEL acronym only if justified.

---

## P2.4 Reconsider title only after experiments

Candidate A:
**From Statutory Conditions to Reviewable Evidence: Executable Copyright-Provenance Boundaries for AI Development under Saudi Arabia’s 2026 Copyright Law**

Candidate B:
**Operationalizing AI-Training Copyright Evidence: A Saudi Legal Testbed for Provenance, Rights Signals, and Reviewable Records**

Do not lock title until Phases 1–4 are complete.

---

# Phase 6 — Second referee pass and journal selection

After P0/P1 revisions:

1. rerun literature search for newly published near-overlap;
2. rerun claim-evidence audit;
3. issue a second simulated referee report;
4. score both journal fits:
   - *Artificial Intelligence and Law* — if computational-law formalization dominates;
   - *Computer Law & Security Review* — if copyright/governance/privacy/infrastructure dominates;
5. only then choose journal.

### Submission threshold
No submission if the second review remains below:
- novelty 7.5/10;
- legal accuracy 8.5/10;
- methodological rigor 8/10;
- empirical sufficiency 7.5/10;
- reproducibility 9/10;
- overclaim control 9/10.

---

# Phase 7 — Packaging only after scientific PASS

Resume Stage 010 only after the second referee review passes. Then complete:
- bilingual legal concordance;
- journal formatting/policy verification;
- reference metadata verification;
- anonymized package;
- persistent archive/DOI;
- cover letter/declarations.

---

## Immediate next execution order

1. **Art. 37(1) legal remediation.**
2. **Semantic-equivalence rubric.**
3. **Condition-coverage benchmark design.**
4. **Naïve baseline/ablation.**
5. **Stage 002 integration.**
6. **Ecological traces.**
7. **Related-work/privacy/right-expression revision.**
8. **Rewrite manuscript around surviving novelty.**
9. **Second referee review.**
10. **Journal decision / Stage 010 resume.**

This order is intentionally scientific: no formatting work proceeds while legal completeness and empirical sufficiency remain unresolved.