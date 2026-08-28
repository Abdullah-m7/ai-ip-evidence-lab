# Stage 008 — Adjudication Distribution and Intake Protocol

## Purpose
Stage 007 froze the neutral adjudication construct. Stage 008 prepares the operational path for distributing those cases to real independent adjudicators without exposing the public internal case identifiers in the delivered bundle.

This stage does **not** collect or invent human responses.

## Threat model
The project repository is public, so complete cryptographic blindness is impossible: a motivated adjudicator can search public materials. Stage 008 therefore targets **casual/accidental deblinding**, mapping integrity, and post-intake tamper evidence.

It does not claim to prove:
- that a respondent is biologically human;
- that the respondent has the claimed qualification;
- that a response was not altered before it reached the intake process;
- that ethics/consent requirements have been satisfied.

Those are real-world study controls.

## Distribution key
For a real export, generate a high-entropy secret key of at least 32 bytes and provide it only through `IPEL_STAGE008_KEY_HEX`. Never commit the key.

The same key is used to derive:
- per-distribution external case IDs via HMAC-SHA-256;
- bundle HMACs;
- private-mapping authentication.

A different `distribution_id` produces a different set of external case IDs and a different packet order even for the same frozen cases.

## Public distribution bundle
Run:

```bash
export IPEL_STAGE008_KEY_HEX='<private hex key>'
PYTHONPATH=. python scripts/export_adjudication_bundle.py \
  --distribution-id REVIEWER-001 \
  --output-dir /path/outside/repository/reviewer-001 \
  --private-dir /secure/private/location/reviewer-001
```

The external directory contains:
- `adjudication_bundle.json`;
- `bundle_manifest.json`;
- `response_template.json`.

The bundle must contain no `ADJ-*` internal ID, Stage-006 case ID, author answer label, machine-gate result, hidden-map name, repository URL, or repository owner identifier.

## Private mapping
`private_case_mapping.json` maps each external `CASE-*` ID back to its internal Stage-007 ID. It also contains a keyed integrity code and a non-secret key fingerprint.

Inside this repository, the official tools only allow mappings under `.private-stage008/`, which is gitignored. A mapping may also be stored outside the repository. Do not send it to adjudicators.

## Response intake
A completed external response is validated against the bundle/manifest/private mapping and then normalized through the Stage-007 adjudication validator.

Example:

```bash
export IPEL_STAGE008_KEY_HEX='<same private hex key>'
PYTHONPATH=. python scripts/ingest_adjudication_responses.py \
  --bundle /secure/distribution/adjudication_bundle.json \
  --manifest /secure/distribution/bundle_manifest.json \
  --private-mapping /secure/private/private_case_mapping.json \
  --response /secure/returned/response.json \
  --ledger /secure/private/intake_ledger.json
```

The ingestion tool produces/extends a private hash-chained intake ledger. It preserves `prior_exposure` and `conflict_of_interest` rather than deleting those rows.

## Integrity boundary
Bundle and private-mapping tampering are detectable at ingestion because they are covered by a project-held HMAC.

For responses, the system creates an exact `submission_sha256` at intake and then hashes the normalized response slice into an append-only receipt chain. Therefore **post-intake** modification of a recorded response is detectable.

This does not authenticate the respondent's decision before intake. Without an adjudicator-controlled signature or an authenticated collection service, the project cannot infer whether a pre-intake response file was changed in transit. The paper must not claim otherwise.

## Synthetic software tests
Synthetic responses may be accepted only with the explicit `--allow-synthetic` lane and `SYNTHETIC_NON_HUMAN` origin. They cannot be mixed into a `REAL_HUMAN` intake ledger and cannot promote a Stage-007 study lock.

## Lock boundary
Stage 008 ingestion outputs raw responses only. It contains no function that creates `POST_ADJUDICATION_LOCK` or `PRE_PRIMARY_STUDY_LOCK`.

A future POST lock remains governed by the already-frozen Stage-007 requirements: real-data validation, all 24 cases resolved under the prespecified rule, raw-response provenance, and an exactly recomputed aggregate.
