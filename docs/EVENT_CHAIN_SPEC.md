# IPEL Stage 002 — Event Chain Specification

## Status
Research prototype. The chain is an integrity experiment, not a replacement for C2PA, a trusted timestamp service, signatures, or legal review.

## Claim under test
A reviewer should be able to detect post-hoc mutation, insertion, deletion, or reordering of recorded AI-development events **relative to a previously known chain checkpoint**.

The prototype deliberately separates two propositions:

- `integrity_verified`: the observed bytes form the same chain committed to by the checkpoint.
- `claim_truth_verified`: always `false` in Stage 002. Hashes do not prove that an asserted licence, acquisition, actor, date, or legal assessment was truthful.

## Event contract
Each event contains:

- `version`: `ipel-event-v1`
- `chain_id`: stable chain identifier
- `sequence`: zero-based sequence number
- `event_id`, `event_type`, `occurred_at`
- `actor`: asserted actor identifier/type
- `payload`: event-specific evidence facts
- `evidence_refs`: references to evidence artifacts, optionally content-bound by SHA-256
- `previous_hash`: SHA-256 hash of the immediately preceding event, or null for genesis
- `event_hash`: SHA-256 over deterministic JSON of all event fields except `event_hash`

## Canonicalization profile
Stage 002 uses UTF-8 JSON with sorted object keys, compact separators, and Unicode preserved. Floating-point values are rejected.

This is intentionally **not claimed to implement RFC 8785/JCS**. A production interoperability stage must either adopt an established canonicalization standard or place the IPEL semantics inside a mature signed container such as C2PA.

## Checkpoint
A checkpoint contains:

```json
{
  "version": "ipel-checkpoint-v1",
  "chain_id": "chain-001",
  "event_count": 3,
  "head_hash": "<sha256>"
}
```

A checkpoint is only useful if preserved outside the mutable event store. Stage 002 does not specify how it is trusted.

## What is detectable
With an unchanged checkpoint:

1. payload/evidence mutation → event hash or checkpoint mismatch;
2. middle deletion → sequence/previous-hash/count mismatch;
3. insertion → sequence/binding/count mismatch;
4. reordering → sequence/previous-hash mismatch;
5. attacker rewrites an event and recomputes all downstream hashes → checkpoint head mismatch;
6. tail truncation → checkpoint count/head mismatch.

## What is not proven

- truth of an event;
- lawful publication or lawful acquisition;
- ownership or authority of the asserted signer/actor;
- trusted time;
- absence of omitted events before the checkpoint was created;
- integrity if an attacker can also replace the only trusted checkpoint;
- legal compliance.

## Falsification condition
The Stage-002 integrity claim fails if an adversarial fixture can alter a checkpoint-bound event history while `verify_chain(..., checkpoint)` still returns `integrity_verified=true`.
