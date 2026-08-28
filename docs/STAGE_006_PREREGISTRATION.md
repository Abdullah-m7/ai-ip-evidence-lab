# Stage 006 Preregistration Draft — Reviewer Utility

**Status:** benchmark/protocol locked for software validation; **no human data collected**. Sample-size and recruitment parameters must be locked before any human data collection. This document is a preregistration-ready protocol, not evidence that a study has already occurred.

## 1. Research question

Does presenting the same underlying AI-development provenance facts in an IPEL structured record improve human review of **evidence readiness** relative to a strong narrative provenance note?

This operationalizes Stage-001 RQ1 and H1–H4 without asking reviewers to decide the law.

## 2. Hypotheses

### H1 — Evidence completeness
For NOT_READY cases, IPEL presentation will increase recall of ground-truth missing-information dimensions relative to the baseline presentation.

**Primary outcome:** missing-information recall on NOT_READY cases.

### H2 — Review reproducibility
Independent reviewers will show greater agreement on `READY / NOT_READY / UNSURE` under IPEL presentation than under baseline presentation.

**Primary agreement outcome:** agreement statistic by presentation condition; report raw percent agreement and a chance-corrected statistic appropriate to the final reviewer count.

### H3 — Minimality
After primary benchmark execution, an explicitly secondary ablation analysis may test whether a smaller subset of IPEL fields preserves review utility. No field will be removed before the primary H1/H2 analysis based on observed outcomes.

### H4 — Boundary effect
Judgment-sensitive cases will produce a higher `UNSURE` rate and/or lower agreement than objective cases, independent of presentation.

## 3. Construct definition

`READY_FOR_LEGAL_EVALUATION` means that scoped facts are sufficiently observable/evidenced for a qualified reviewer to evaluate them. It does **not** mean the underlying conduct is legally permissible.

Ground truth is defined from evidence sufficiency, independently of Stage-001 `PASS / REVIEW / FAIL`. The benchmark deliberately contains READY cases with explicit adverse facts and machine-gate `FAIL_EVIDENCE_GATE` outcomes.

## 4. Design

- 24 latent synthetic cases.
- 12 READY / 12 NOT_READY.
- 12 objective / 12 judgment-sensitive.
- Within each stratum × readiness cell: 6 cases.
- Two presentations: strong baseline and IPEL.
- Form A: 12 baseline + 12 IPEL.
- Form B: exact presentation swap for every latent case.
- Within each cell each form contains 3 baseline + 3 IPEL cases.
- A reviewer receives only one form and therefore never sees both renderings of the same latent case.
- Packet order is deterministically shuffled from seed `20260828`.

This is a counterbalanced mixed design: presentation varies within a reviewer across different cases, while each latent case is presented in both formats only across forms/reviewers.

## 5. Baseline strength / factual parity

The baseline is not a bare URL. It is a structured narrative provenance note with sections for work information, acquisition/publication, AI-development use, rights/market assessment, output context, and evidence references.

Both presentations are rendered from one latent fact map. IPEL may show empty schema slots, but it cannot introduce new underlying facts. The build audit requires identical latent records and identical available-fact digests across Form A/B representations.

Every reviewer receives the same missing-information codebook. Thus any IPEL effect must survive a baseline that already tells reviewers which dimensions can matter.

## 6. Reviewer task

For each packet reviewers provide:

1. `READY`, `NOT_READY`, or `UNSURE`;
2. missing-information checklist selections;
3. confidence (0–100);
4. assessment time if the collection interface supports reliable timing.

Reviewers are instructed not to decide legal compliance.

## 7. Planned outcomes

### Primary H1 metrics
- missing-information recall on NOT_READY cases;
- false-ready rate (`READY` response on NOT_READY ground truth).

### Primary H2 metrics
- inter-reviewer agreement by presentation;
- decision-distribution matrices by packet and presentation.

### Secondary metrics
- readiness classification accuracy;
- missing-information precision;
- `UNSURE` rate;
- confidence calibration relative to readiness correctness;
- assessment time;
- outcome stratification by objective vs judgment-sensitive cases.

## 8. Planned analysis

At minimum, report descriptive estimates and uncertainty intervals by presentation and stratum. If sample size supports it, model binary outcomes with case and reviewer clustering/random effects rather than treating 24 × N responses as independent observations.

For H1, the preferred unit is the reviewer × missing-information opportunity on NOT_READY cases. For H2, agreement is computed separately by presentation from reviewers who evaluated the same packet representation across assigned forms/cohorts. For H4, compare uncertainty and agreement across the two prespecified strata.

No human effect size is produced by Stage 006 benchmark generation itself.

## 9. Recruitment / sample size — must be locked before collection

Not yet specified in this repository. Before collection, record:

- target reviewer population (e.g. copyright/legal researchers, lawyers, AI-governance researchers, or prespecified mixed strata);
- inclusion/exclusion criteria;
- target N and power/simulation rationale;
- compensation, if any;
- applicable ethics/consent review requirements;
- assignment procedure to Form A/B.

These items must be committed/preregistered before looking at human outcomes.

## 10. Exclusion policy — before collection

Do not invent post-hoc speed thresholds. Before human collection, predefine only technically necessary exclusions (e.g. duplicate submission, missing consent where applicable, or responses with no completed packets) and preserve an exclusion audit trail.

## 11. Benchmark integrity gates

Before human use, automated tests require:

- factual parity for every latent case;
- no readiness/case/stratum answer labels in visible packets;
- exact counterbalancing;
- 12/12 readiness and stratum balance;
- 12/12 baseline/IPEL balance per form;
- 3 cases per stratum × readiness × presentation cell;
- unique packet IDs;
- at least one READY case with machine-gate FAIL;
- benign NOT_READY cases missing only one fact;
- deterministic regeneration.

## 12. Synthetic scoring fixtures

`benchmarks/stage006/generated/synthetic_responses/` contains explicitly labeled NON-HUMAN fixtures. They exist only to test scoring code. Their metrics must never be reported as reviewer-study findings.

## 13. Falsification posture

The substantive IPEL utility claim should be weakened if a properly powered reviewer study with the locked strong baseline shows no meaningful improvement in missing-information detection or review reproducibility. A null/negative result is scientifically informative and must not be hidden by changing the baseline or outcome definitions after collection.
