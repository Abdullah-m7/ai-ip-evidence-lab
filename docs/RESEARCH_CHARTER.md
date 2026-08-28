# Stage 001 Research Charter

## Working title

**From Copyright Exception to Verifiable Compliance: An Evidence Architecture for AI Development under Saudi Arabia's 2026 Copyright Law**

## Research problem

Legal rules can condition an AI developer's use of a copyrighted work on facts that may be difficult to reconstruct after model development. The scientific problem is therefore not only rule interpretation; it is **observability**.

Can a development pipeline capture enough contemporaneous, integrity-preserving evidence for an independent reviewer to reconstruct whether facts relevant to the Saudi AI-development exception were present?

## Primary research question

**RQ1.** Can a structured provenance record improve the accuracy and reproducibility of post-hoc assessment of AI-development uses against Article 26(4) of the 2026 Saudi Copyright Law and Article 30 of its Implementing Regulations?

## Secondary questions

**RQ2.** Which legal conditions can be evaluated from machine-recorded facts, and which remain irreducibly judgment-dependent?

**RQ3.** What is the minimum evidence set that preserves materially the same review outcome as the full evidence record?

**RQ4.** How robust is the evidence architecture to missing, stale, conflicting, or strategically manipulated provenance?

## Testable hypotheses

- **H1 — Evidence completeness:** reviewers supplied with IPEL records will identify missing legally relevant facts more accurately than reviewers supplied with ordinary dataset cards or source URLs alone.
- **H2 — Review reproducibility:** structured evidence will reduce disagreement between independent reviewers on whether a case is ready for legal evaluation.
- **H3 — Minimality:** a smaller core record can retain most of the review utility of a full record; fields that do not alter review outcomes can be removed.
- **H4 — Boundary effect:** fact-sensitive conditions such as effect on normal exploitation will produce higher reviewer uncertainty than objective record-retention conditions.
- **H5 — Integrity effect:** hash-linked evidence and timestamped acquisition/use events will make provenance tampering easier to detect than editable narrative documentation.

## Unit of analysis

An **AI-development use event**: one identifiable work (or work unit) copied or analyzed for a declared AI-development purpose at a given time.

The design deliberately avoids treating an entire training dataset as one legal event when work-level provenance exists.

## Stage 001 contribution

Stage 001 does **not** claim to automate legal compliance. It contributes:

1. a legal-to-evidence requirements matrix;
2. a machine-readable evidence contract;
3. a deterministic gate that separates hard contradictions from judgment-sensitive cases;
4. synthetic adversarial cases for falsification;
5. a path to an empirical reviewer study or benchmark without requiring access to proprietary model-training corpora.

## Evaluation plan

### Phase A — Contract validation

Construct synthetic cases spanning:

- complete evidence;
- missing mandatory record fields;
- unlawful/unknown publication or acquisition evidence;
- excessive copying without necessity rationale;
- republication or distribution;
- purely commercial use with unresolved materiality/normal-exploitation effects;
- unnecessary final-product inclusion;
- independently protected embedded elements;
- contradictory evidence artifacts.

Measure deterministic coverage and false PASS behavior.

### Phase B — Blind legal-readiness annotation

Create a case set in two forms:

- **baseline:** narrative/source metadata only;
- **IPEL:** structured evidence record plus the same underlying facts.

Reviewers answer only whether the record is *ready for legal evaluation* and which facts are missing. This avoids asking non-judicial software to decide the law.

Primary outcomes:

- missing-fact recall;
- false-ready rate;
- inter-reviewer agreement;
- time-to-assessment;
- uncertainty rate by legal condition.

### Phase C — Integrity adversary

Mutate source, date, acquisition status, work hash, and decision fields after record creation. Evaluate which mutations are detectable under progressively stronger evidence-chain designs.

## Falsification criteria

The core IPEL claim should be weakened or rejected if:

- structured records do not improve missing-fact detection over a strong baseline;
- reviewers show no reproducibility gain;
- the same evidence can be captured more simply with an existing mature standard without material loss;
- integrity mechanisms cannot detect meaningful record manipulation;
- the mapping embeds legal conclusions inside supposedly factual fields.

## Non-goals

- predicting court outcomes;
- declaring a work "safe to train on";
- replacing SAIP, courts, counsel, or rights holders;
- creating a broad copyright ontology before Stage 001 is validated;
- assuming that a hash proves lawful acquisition or truth of provenance.
