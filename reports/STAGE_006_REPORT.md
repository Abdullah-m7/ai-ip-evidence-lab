# Stage 006 Report — Blinded Reviewer-Utility Benchmark

## Status

**BENCHMARK READY / NO HUMAN RESULTS**

Stage 006 prepares the empirical test of H1–H4 from the Stage-001 research charter. It does not claim that IPEL improves human review yet; that claim remains to be tested with actual reviewers under a preregistered collection plan.

## Benchmark composition

- 24 latent synthetic cases.
- 12 `READY_FOR_LEGAL_EVALUATION` / 12 `NOT_READY_FOR_LEGAL_EVALUATION`.
- 12 objective / 12 judgment-sensitive.
- 6 cases in each stratum × readiness cell.
- Form A: 12 baseline + 12 IPEL.
- Form B: exact representation swap for every case.
- Within every stratum × readiness cell, each form has 3 baseline + 3 IPEL cases.

## Structural audit

All automated gates pass:

- 100% latent-record identity across forms;
- 100% available-fact digest parity across the two representations;
- every case presentation-swapped between Form A/B;
- no readiness, case-ID, stratum, or hidden missing-fact labels in reviewer-visible packets;
- unique packet IDs;
- balanced readiness, stratum, and presentation;
- deterministic regeneration byte-for-byte from seed `20260828`.

The machine-readable audit is `benchmarks/stage006/generated/audit.json`.

## Construct-separation result

Evidence readiness is not equated with legal compliance or with the Stage-001 machine gate.

The benchmark currently contains **8 READY cases with `FAIL_EVIDENCE_GATE` machine outcomes**. These cases contain explicit facts that are adverse but sufficiently observed for a legal evaluator to assess. This is a deliberate construct-validity check, not an anomaly.

Examples include explicit unlawful acquisition/publication facts and explicit prohibited-use facts. In contrast, cases with `unverified` acquisition/publication are NOT_READY because the relevant fact remains unresolved.

## Strong baseline

The baseline is a provenance-review note with the same available facts and the same domain sections used to generate the IPEL record. All reviewers receive the same missing-information checklist.

IPEL's treatment advantage, if any, must therefore come from its structured field representation and explicit empty slots—not from access to extra underlying facts or a weaker control condition.

## Scoring implementation

The scoring harness supports:

- readiness accuracy;
- false-ready rate;
- missing-information recall on NOT_READY cases;
- missing-information precision;
- uncertainty rate;
- assessment time;
- presentation and objective/judgment-sensitive stratification;
- per-packet decision matrices and pairwise agreement-ready summaries.

Synthetic perfect/noisy response fixtures are committed solely to test this code. The perfect fixture scores 100% by construction; this is **not a human-study result**.

## Human-study boundary

Before any human data collection, the preregistration still requires a locked:

- reviewer population;
- inclusion/exclusion criteria;
- target sample size and power/simulation rationale;
- Form A/B assignment procedure;
- applicable consent/ethics process;
- collection interface and timing policy.

No effect size or claim about reviewer benefit should be made until that phase is completed.

## Falsification posture

If a properly powered reviewer study using this strong baseline shows no meaningful gain in missing-information detection or review reproducibility, the core IPEL reviewer-utility claim should be weakened rather than rescued by changing outcomes or weakening the baseline after the fact.
