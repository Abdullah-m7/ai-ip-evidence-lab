# Stage 007 — Study Lock Protocol

## Goal
Prevent benchmark labels, analysis code, and study-design choices from drifting after human outcomes become visible.

## Lock states
### PRE_ADJUDICATION_LOCK
Can be completed now. It freezes the Stage-006 benchmark, neutral adjudication materials, adjudication schema/code, power-design grid, and protocols.

It must state:
- `real_adjudication_collected=false`;
- `final_sample_size_locked=false`.

### POST_ADJUDICATION_LOCK
May exist only after real human adjudication is ingested and all 24 cases meet the prespecified resolution rule. Synthetic fixtures cannot satisfy this transition.

The original Stage-006 author labels remain preserved even if adjudicated labels differ.

### PRE_PRIMARY_STUDY_LOCK
May exist only after POST_ADJUDICATION_LOCK plus an explicit selected study-design file specifying:
- reviewer population;
- inclusion criteria;
- target N;
- power rationale;
- recruitment constraints;
- assignment procedure;
- resolved ethics/consent status.

Only this state may set `final_sample_size_locked=true`.

## Power planning
`experiments/stage007_power_simulation.py` reports a sensitivity grid, not a selected N. It uses no human Stage-006 outcomes.

The grid varies recruited reviewer count and plausible IPEL improvements while including attrition, reviewer heterogeneity, and case heterogeneity. Its approximate z-based power is for design comparison only; the eventual primary model should use the preregistered clustered/mixed-effects analysis appropriate to the collected data.

## Freeze manifest
Each lock manifest records SHA-256 hashes for the benchmark, packets, schemas, analysis code, power grid, and protocols plus the source Git commit SHA.

A higher lock state cannot be claimed merely by editing the manifest: `src/ipel/study_lock.py` validates the real-world prerequisites.

## Mutation rule
After PRE_ADJUDICATION_LOCK, any change to a frozen input requires a new manifest. After human adjudication begins, changes to latent cases require a new benchmark version and adjudication cycle. After primary outcome collection begins, outcome definitions and the strong baseline must not be weakened in response to observed results.

## Human-origin provenance boundary
A lock file cannot cryptographically prove that a person, rather than software, produced a response. For POST adjudication the state machine therefore enforces the strongest claim available inside the repository: a raw response set declaring `REAL_HUMAN`, schema/eligibility validation of every row, recomputation of the 24-case aggregate from those raw rows, exact equality with the committed summary, and hashes for both raw and summary files.

This proves **structural provenance and internal consistency**, not biological human identity. Recruitment records, consent/ethics process, and adjudicator identity/qualification checks remain real-world study controls and must not be replaced by a JSON label.
