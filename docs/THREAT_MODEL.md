# IPEL Threat Model — Stage 001

## Asset being protected

The asset is not the copyrighted work itself. It is the **credibility of the historical evidence trail** about how a work entered and was used in an AI-development pipeline.

## Adversaries / failure modes

1. **Missing provenance** — source or acquisition evidence was never recorded.
2. **Retrospective reconstruction** — a team fills records after a dispute and mistakes memory for contemporaneous evidence.
3. **Metadata substitution** — a record points to a different edition/file than the bytes actually used.
4. **License drift** — a webpage's terms change after acquisition.
5. **Purpose drift** — a work acquired for one experiment is silently reused for another.
6. **Output leakage** — copied material appears unnecessarily in a final product.
7. **Nested rights blindness** — a nominally licensed container contains independently protected elements.
8. **Strategic self-attestation** — the developer marks acquisition/publication as lawful without supporting evidence.
9. **Record tampering** — dates, sources, hashes, or assessments are edited after use.
10. **Automation overclaim** — a rules engine converts incomplete facts into a false legal-compliance conclusion.

## Stage-001 defenses

- mandatory work/source/purpose/date fields;
- SHA-256 binding for the work artifact where bytes are available;
- explicit evidence references for publication/acquisition assertions;
- tri-state factual status (`verified`, `unverified`, `false`) rather than forced booleans;
- `REVIEW_REQUIRED` for judgment-sensitive conditions;
- hard failure for explicit prohibited configurations encoded in the record;
- prohibition on interpreting PASS as legal compliance.

## What Stage 001 does not solve

- authenticity of an external receipt or license;
- trusted timestamping;
- key management or digital signatures;
- whether the rights holder actually owned every claimed right;
- whether a market effect is legally sufficient to defeat an exception;
- conflicts of laws across jurisdictions;
- collective licensing and orphan-work edge cases;
- proof that a dataset ingestion system emitted a record for *every* work used.

These limitations are research targets, not implementation bugs to hide.

## Stage 002 integrity threat model

Stage 002 adds a hash-linked event history and an optional external checkpoint. This narrows one threat only: **detectable post-hoc modification of a previously committed event history**.

A hash chain without an external checkpoint is insufficient against an attacker who can rewrite an event and recompute every downstream hash. Tail deletion can also leave an internally consistent shorter chain. Therefore, verification reports `boundary_verified=false` when no checkpoint is supplied, even if internal hashes are consistent.

The checkpoint itself is not authenticated in Stage 002. If the same attacker can replace both the event store and its sole checkpoint, the prototype provides no protection. C2PA signatures, trusted timestamps, append-only transparency services, independent witnesses, or other anchoring mechanisms are candidate later layers—not assumptions smuggled into this stage.
