# Stage 008 Preparation Report

## Status
**DISTRIBUTION_AND_INGESTION_INFRASTRUCTURE_PREPARED — NO HUMAN DATA**

Stage 008 operationalizes the transition from the frozen Stage-007 neutral adjudication packet to external per-adjudicator bundles and later raw-response intake.

## Security / validity posture
- Real bundle IDs and external case IDs are derived with a project-held HMAC key that is never committed.
- Each distribution ID produces a distinct external case-ID namespace and packet order.
- The public bundle excludes internal `ADJ-*` identifiers, Stage-006 IDs/labels, machine-gate outcomes, hidden-map names, and repository URLs.
- Bundle and private-mapping integrity are checked with keyed HMACs.
- Synthetic responses require an explicit software-test lane and cannot be mixed into a real intake ledger.
- Intake produces raw normalized responses only; it has no study-lock promotion capability.

## Important limitation
This design reduces accidental deblinding but cannot make a public benchmark cryptographically secret from a motivated adjudicator who searches for the underlying synthetic facts.

The project also cannot authenticate a human decision before intake without an adjudicator-controlled signature or an authenticated collection service. Stage 008 therefore claims **post-intake tamper evidence**: the exact received response document is hashed, normalized rows are hashed, and intake receipts form a hash chain. Changes to recorded responses after intake are detectable.

## Real-world state
- Real adjudicators recruited: **false**
- Real responses collected: **false**
- Ethics / consent determination: **UNRESOLVED**
- Adjudicator population / qualification criteria: **UNRESOLVED**
- Final primary-study sample size: **not locked**
