# Stage 014 Report — Corrected-Profile Condition Benchmark and Delegation Assessment

## Status

**CORRECTED-PROFILE BENCHMARK EXECUTED — CONTROLLER REVIEW PENDING**

Stage 012 corrected the legal profile. Stage 013 froze the semantic-equivalence rubric before any
candidate outcome was observed. Stage 014 executes the frozen method: it runs the Copyright Law
Article 26(4) + Copyright Law Article 37(1) + Implementing Regulations Article 30(1)–(6)
condition × state benchmark on record profile `0.2.0`, applies rubric v1.0.0 to the preregistered
candidate mappings, and measures a declared naïve provenance-mapping baseline against the
rubric-governed mapping.

Nothing here is a legal conclusion, and Stage 014 makes no KEEP/NARROW/WITHDRAW decision. That
decision is reserved for Controller review after independent verification.

## Frozen inputs verified before execution

The runner refuses to execute unless the Stage 013 pre-outcome lock still matches its sources:

```text
rubric_definition_canonical_sha256 = 81c70506e6702bc4ad5ffad337e817c6ab71b55c946c185743da1887f8344fc5
candidate_registry_canonical_sha256 = be02f758a85c7f99a62e4de1c42079a61661ccb39cfce78710a405dd421ced76
lock_status = PRE_OUTCOME_RUBRIC_LOCK
lock_source_commit_sha = 037070dae5a93a1ef58c806a537784f378226998
```

The frozen registry is preserved unmodified: `benchmark_executed` is still `false` and every row is
still `assessment_status=NOT_RUN`. Stage 014 outcomes were written to new artifacts under
`benchmarks/stage014/`, not back into the Stage 013 lock. No candidate was added, removed, or
reselected after the lock.

## Reproduction

```bash
python experiments/stage014_corrected_profile_benchmark.py
python -m unittest tests.test_stage014_benchmark -v
```

Artifacts (all deterministic, sorted-key JSON):

- `benchmarks/stage014/candidate_assessments.json` — authored rubric assessments (input);
- `benchmarks/stage014/generated/condition_state_benchmark.json`;
- `benchmarks/stage014/generated/delegation_roundtrip.json`;
- `benchmarks/stage014/generated/delegation_assessment_results.json`;
- `benchmarks/stage014/generated/naive_baseline_comparison.json`;
- `benchmarks/stage014/generated/corrected_profile_roundtrip.json`;
- `benchmarks/stage014/generated/stage014_result.json` — machine-readable Stage 014 result.

## 1. Condition × state benchmark on profile 0.2.0

59 preregistered cases across 13 conditions. Every case declares its expected outcome, the gate rule
that must carry the finding, and a message marker, so a case cannot be satisfied by an unrelated
rule firing.

| Measure | Value |
|---|---|
| Cases | 59 |
| Conditions | 13 |
| Outcomes matching declared expectation | 59/59 |
| Cases where the expected rule/severity/marker finding was present | 59/59 |
| Favorable (evidence-ready) states | 16 |
| Unresolved (review) states | 19 |
| Adverse (fail) states | 24 |

All 0.2.0 cases report `legal_profile_id=sa-copyright-2026-art26-4-art37-1-ir30-v0.2` and
`declared_scope_complete=true`; the unsupported-version case reports
`unsupported-record-profile` and fails closed. `legal_conclusion=false` holds in all 59 cases.

### Article 37(1) is not collapsed into Regulation Article 30

Four separation cases are included in the benchmark rather than only in unit tests:

```text
art37_normal_exploitation_adverse_with_favorable_ir30   -> FAIL via LAW-37(1); no IR-30(2)/IR-30(4) finding
art37_rightsholder_adverse_with_favorable_ir30_4        -> FAIL via LAW-37(1); no IR-30(2)/IR-30(4) finding
ir30_2_adverse_with_favorable_art37                     -> FAIL via IR-30(2);  no LAW-37(1) finding
ir30_4_adverse_with_favorable_art37                     -> FAIL via IR-30(4);  no LAW-37(1) finding
```

The separation holds in both directions: a favorable Regulation field cannot mask an adverse
Article 37 fact, and an Article 37 assessment cannot silently satisfy a Regulation condition.

## 2. Rubric v1.0.0 applied to the preregistered candidates

All 11 frozen candidates were assessed under the locked rubric with no rubric change and no
reselection.

| Decision | Count |
|---|---|
| SAFE_DELEGATION | 1 |
| PARTIAL_SUPPORT | 8 |
| NOT_SAFE_TO_DELEGATE | 0 |
| NO_CANDIDATE | 2 |

The single `SAFE_DELEGATION` is `work.title → C2PA 2.4 Ingredient v3 dc:title`. `work.title` is a
human-readable entity attribute; it is not one of the four Implementing Regulations Article 30(3)
retained-record fields and is not read by the evidence gate. 10 of 11 IPEL fields are retained.

Delegability of the legally operative fields:

```text
Implementing Regulations Article 30(3) core fields safely delegable : 0/4
Copyright Law Article 37(1) propositions safely delegable           : 0/2
```

This is a corrected-profile result produced under an explicit rubric. It corroborates the direction
of the legacy `0/4` intuition, but it does not restate the legacy number: the legacy result was
generated under profile `0.1.0` with the pre-Stage-013 "sufficiently equivalent" wording and remains
a separate, legacy claim.

### Controlled delegation round-trips (measured, not declared)

Every non-`NO_CANDIDATE` candidate was substituted and read back. The harness separates three
observables and passes only when all three are satisfied.

| Measure | Value |
|---|---|
| Candidates round-tripped | 9 |
| Round-trips passing every criterion | 1 |
| Candidates whose value was recovered byte-identically | 2 |
| Candidates needing a declared bridging assumption | 8 |
| Substitutions the evidence gate could **not** detect (gate-silent semantic corruption) | 7 |

Two findings deserve emphasis.

1. **String-level recovery is not semantic equivalence.** `use.date → c2pa.actions[0].when`
   recovered the same date string and preserved the gate outcome, yet still fails: recovery is only
   possible under the declared bridging assumption that the timestamped C2PA action *is* the legally
   relevant use event. The frozen rubric anticipated exactly this ("a timestamp must be assessed for
   the proposition it timestamps rather than equated with `use.date` from field-name similarity").
2. **The evidence gate is not a detector of bad delegation.** In 7 of 9 substitutions the IPEL value
   was replaced by a semantically different value and the gate outcome did not change. Delegation
   safety must therefore be established by the rubric, not by observing that the gate still passes.

Declared round-trip states in `candidate_assessments.json` are cross-checked against the measured
harness output; a mismatch aborts the run rather than being reconciled.

## 3. Naïve provenance-mapping baseline

The comparator is declared explicitly. The naïve baseline delegates 5 IPEL paths to the most
name-similar C2PA/CAWG semantic (first registered candidate per path) and infers 13 further paths —
including both Article 37(1) propositions — from provenance signals (manifest validity, signer trust,
and the CAWG training/mining declaration). Fields with no provenance analogue are retained. The
rubric-governed mapping delegates only what rubric v1.0.0 classified `SAFE_DELEGATION` (1 path) and
infers nothing.

| Provenance signals | Naïve outcomes preserved | Naïve false equivalences | Naïve spurious escalations | Rubric-governed outcomes preserved |
|---|---:|---:|---:|---:|
| valid / trusted / `allowed` | 31/59 | 28 | 0 | 59/59 |
| unknown / unknown / `constrained` | 29/59 | 14 | 16 | 59/59 |

A *false equivalence* is a case whose true outcome is `FAIL_EVIDENCE_GATE` or `REVIEW_REQUIRED` but
whose naïve reconstruction is strictly less severe — the baseline masks an adverse or unresolved
legal fact.

Under favorable provenance the naïve baseline masks, among others, explicit Article 37(1) conflict,
explicit Article 37(1) unjustified rightsholder prejudice, explicitly false lawful publication,
explicitly false lawful acquisition, unsupported necessity, and the omission of
`article37_context` altogether.

Two further comparator results:

- **Semantic loss.** Across the 59 cases the naïve reconstruction differs from the record on 557
  leaf paths under favorable provenance and 1278 under unknown provenance; the rubric-governed
  mapping loses 0 paths in both configurations.
- **Signal-driven instability.** The naïve outcome changes between the two provenance-signal
  configurations in 44 of 59 cases, so its legal-facing outcome tracks provenance signal state rather
  than the recorded legal facts. The rubric-governed outcome is identical in both configurations.

The direction of error also flips with the signals: favorable provenance produces masking (28 false
equivalences, 0 spurious escalations), while unknown provenance produces both masking of adverse
facts and 16 spurious escalations of otherwise evidence-ready cases.

## 4. Corrected-profile mapping / round-trip coverage

This replaces **only** the part of the Stage 003 evidence that was generated under profile `0.1.0`.

| Measure | Value |
|---|---|
| Cases | 59 |
| Profiles constructed | 55 |
| Profiles failing closed on a missing Article 30(3) core field | 4 |
| Constructed cases preserving the gate outcome | 55/55 |
| Constructed cases preserving the Article 30(3) tuple | 55/55 |
| Constructed cases preserving the Article 37(1) context tuple | 55/55 |
| Constructed round-trips with zero semantic loss | 55/55 |

The four fail-closed cases are the deliberately incomplete Article 30(3) records
(`work.type`, `work.source`, `use.purpose`, `use.date`); the profile contract refuses to build
rather than emitting a partial mapping.

Stage 001–005 artifacts were not rewritten. `reports/stage003_semantic_roundtrip.json` and
`examples/profiles/stage003_*.json` remain the historical `0.1.0` evidence, and a regression test
asserts they still declare `record_version=0.1.0`.

## Negative and unresolved results

Reported exactly as observed:

- **0/4** Article 30(3) core fields and **0/2** Article 37(1) propositions are safely delegable. The
  only safe delegation is a field with no legal operation in the gate.
- **No candidate at all** exists for either Article 37(1) proposition. That is a reported absence at
  the frozen registry, not a demonstration that no such normative semantic could ever be defined.
- **`IR-30(6)-independent-elements` has no adverse state in profile 0.2.0.** The gate can escalate
  independent-elements problems to review but can never fail on them. This is an observed coverage
  limit of the profile, not evidence of compliance.
- **`EVIDENCE-references` likewise has no adverse state**: missing evidence references escalate to
  review only.
- **`IR-30(1)-prohibited-uses`, `IR-30(3)-retained-record` and `PROFILE-0.2.0-integrity` have no
  unresolved state**, because they are encoded as booleans or as presence/absence. The benchmark
  reports these absences rather than fabricating a case.
- **The evidence gate did not detect 7 of 9 bad delegations.** The gate is a legal-condition
  evaluator, not a semantic-substitution detector.
- One naïve-baseline case (`ir30_3_adverse_missing_use_date`) is *not* masked only because the
  harness derives the synthetic C2PA action time from the record's own `use.date`. A production
  pipeline would take that timestamp from the tool run, so the real naïve baseline would likely mask
  this case too. The modelling choice is conservative in the baseline's favour and is disclosed here
  rather than tuned away.
- The synthetic provenance values (`text/plain`, `c2pa.types.dataset`, the informational URI, and the
  JUMBF-style data reference) are fixtures for a controlled substitution experiment. No assessment
  turns on the particular token chosen; each assessment turns on the proposition class.

## Limitations

- The rubric assessments are analyst judgements applied through a frozen classifier. The classifier
  is mechanical and fails closed, but the per-dimension `PASS`/`FAIL` calls are not independently
  adjudicated. Independent adjudication is not part of Stage 014.
- The benchmark evaluates the *encoded abstraction* of the legal conditions in profile 0.2.0. It
  measures the fidelity of the model, not the correctness of the underlying legal interpretation.
  The controlling source remains the official Arabic Copyright Law published by *Umm Al-Qura*;
  English labels here are analytical modelling terms and **not a legal conclusion**, an official
  translation, a SAIP interpretation, or legal advice.
- The naïve baseline is a declared comparator constructed by this project, not an observation of any
  third party's system.
- One record fixture (`examples/records/valid_v020_art37.json`) is the base for all 59 cases, so the
  benchmark measures condition coverage, not population-level variation.

## What Stage 014 does not decide

Stage 014 produces evidence. It does not decide whether Paper A's delegation claims are kept,
narrowed, or withdrawn. `stage014_result.json` records
`controller_decision = NOT_MADE_BY_THIS_STAGE`. The KEEP/NARROW/WITHDRAW decision is reserved for
Controller review after independent verification of these artifacts.
