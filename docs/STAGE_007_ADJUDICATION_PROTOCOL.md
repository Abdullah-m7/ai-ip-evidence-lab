# Stage 007 — Independent Ground-Truth Adjudication Protocol

## Purpose
Stage 006 created a balanced reviewer-utility benchmark, but its READY / NOT_READY labels were authored inside this project. Stage 007 treats those labels as **author hypotheses**, not unquestioned gold truth.

No real adjudication has been collected in this stage-preparation commit.

## Construct
Adjudicators answer one question only:

> Is the available record sufficiently complete and evidenced for a qualified legal reviewer to evaluate the scoped copyright questions?

`READY` does not mean lawful. An explicit adverse fact can still be fully observable. `NOT_READY` means at least one scoped relevant fact remains missing, unresolved, or unsupported. `UNSURE` is allowed.

## Blinding
Each Stage-006 latent case is rendered once as a neutral factual inventory. The visible packet excludes:
- Stage-006 case IDs;
- author readiness labels;
- author missing-information codes;
- objective/judgment-sensitive stratum;
- baseline/IPEL presentation condition;
- machine-gate outcomes.

A deterministic hidden map links each `ADJ-*` ID back to its original latent case for provenance only.

## Adjudicators
Primary consensus requires at least **3 independent eligible adjudicators per case**. The planned population and recruitment route are not yet fixed and must be locked before collection.

Each adjudicator supplies:
1. a pseudonymous adjudicator ID;
2. READY / NOT_READY / UNSURE;
3. missing-information codes;
4. confidence 0–100;
5. optional rationale;
6. prior-exposure flag;
7. conflict-of-interest flag.

Responses flagged for prior exposure or conflict are preserved in the audit trail but excluded from primary consensus.

## Consensus rule
For a case with at least three eligible adjudicators:
- READY or NOT_READY must reach at least **2/3** of eligible decisions;
- an UNSURE plurality/majority never becomes a substantive gold label;
- NOT_READY additionally requires at least one missing-information code to reach the same 2/3 threshold;
- READY with a 2/3-consensus missing-information code is internally contradictory and remains UNRESOLVED.

Anything else is `UNRESOLVED`. The software never breaks ties in favor of Stage-006 author labels.

## Case revision
If real adjudication exposes ambiguity, the original Stage-006 case and author label remain immutable provenance. Any revised latent case must receive:
- a new benchmark version;
- new packet IDs;
- a new adjudication cycle;
- a new lock manifest.

No case may be silently rewritten after primary reviewer outcomes are observed.

## Synthetic fixtures
Files under `benchmarks/stage007/generated/synthetic_adjudication/` are explicitly `SYNTHETIC_NON_HUMAN`. They test validation and consensus code only and must never be reported as content-validity evidence.
