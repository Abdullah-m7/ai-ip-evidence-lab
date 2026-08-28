# Stage 006 Reviewer Codebook

## Decision construct

Reviewers judge **evidence readiness**, not legal compliance.

- `READY`: the available record is sufficiently complete and evidenced for a qualified legal reviewer to evaluate the scoped copyright questions.
- `NOT_READY`: at least one relevant fact is missing, unresolved, or unsupported.
- `UNSURE`: the reviewer cannot confidently classify readiness from the packet.

A `READY` record may contain facts that are legally adverse. For example, an explicitly evidenced `acquisition_status=false` can be ready for evaluation because the relevant fact is known. `READY` must never be read as “lawful”, “safe”, or “compliant”.

## Missing-information checklist

Every reviewer receives the same checklist in both presentation conditions. This makes the narrative baseline deliberately strong rather than withholding the dimensions IPEL is designed to structure.

| Code | Reviewer-facing meaning |
|---|---|
| `WORK_TYPE` | Type/category of the work is not sufficiently recorded. |
| `WORK_SOURCE` | Source from which the work was obtained is not sufficiently recorded. |
| `USE_PURPOSE` | Purpose of the AI-development use is not sufficiently recorded. |
| `USE_DATE` | Date of the AI-development use is not sufficiently recorded. |
| `PUBLICATION` | Lawful-publication status is unresolved or unsupported. |
| `ACQUISITION` | Lawful-acquisition status is unresolved or unsupported. |
| `NECESSITY` | Necessity/proportionality is unresolved. |
| `PROHIBITED_USE_STATUS` | Republication/distribution/direct-exploitation status is unresolved. |
| `COMMERCIAL_EFFECT` | Commercial materiality or normal-exploitation effect is unresolved. |
| `AUTHOR_INTERESTS` | Legitimate-author-interest effect lacks a sufficient assessment or basis. |
| `OUTPUT_CONTEXT` | Output use/transformation/permission context is unresolved. |
| `INDEPENDENT_ELEMENTS` | Independently protected elements are unresolved or lack an assessment basis. |
| `USE_EVENT_EVIDENCE` | Contemporaneous evidence of the use event is not recorded. |

## Reviewer response fields

For every packet:

1. `decision`: `READY`, `NOT_READY`, or `UNSURE`.
2. `missing_information_codes`: zero or more checklist codes.
3. `confidence_0_to_100`: subjective confidence in the readiness assessment.
4. `assessment_seconds`: elapsed assessment time, recorded by the study interface if available.

The term `missing_fact_codes` appears only in the hidden answer key; it is intentionally different from the reviewer response field to reduce accidental answer-key leakage.

## Presentation conditions

### Baseline
A strong provenance-review note organized into common sections. It contains every available underlying fact for the latent case. Missing facts simply do not appear as entries.

### IPEL
A structured evidence record generated from the same underlying facts. The schema also exposes absent slots as `NOT_RECORDED`. Those empty slots are structural cues, not additional facts.

Both conditions use the same response checklist.

## What reviewers are not asked to do

- predict a court outcome;
- decide whether training/use is lawful;
- infer ownership from signatures or provenance;
- treat C2PA trust as legal permission;
- reproduce the Stage-001 machine gate.

The benchmark is intentionally about the **observability and completeness of evidence before legal judgment**.
