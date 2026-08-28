# Saudi 2026 AI-Development Evidence Matrix

**Scope:** Copyright Law Article 26(4) + Implementing Regulations Article 30.

This document maps legal conditions to evidence that a technical system can preserve. It is a research abstraction, not an authoritative interpretation.

| Rule source | Condition / risk | Observable evidence candidate | Gate treatment | Why |
|---|---|---|---|---|
| Law 26(4) | Work was lawfully published | publication status, publication evidence reference | REVIEW if unverified; FAIL if explicitly false | Legal status may require external verification |
| Law 26(4) | Original copy was lawfully acquired | acquisition method, acquisition status, receipt/license/source evidence | REVIEW if unverified; FAIL if explicitly false | A URI or hash alone does not prove lawful acquisition |
| Law 26(4) | Copying is limited to development purpose | declared purpose, copied portion/extent, necessity rationale | REVIEW when necessity is uncertain | Proportionality is contextual |
| Reg. 30(1) | Copying/analysis limited to what AI development requires | extent + necessity rationale | REVIEW when uncertain | Context-sensitive |
| Reg. 30(1) | No republication, distribution, or direct commercial exploitation under the exception | event flags + output/delivery evidence | FAIL on explicit prohibited use | Encoded direct contradiction |
| Reg. 30(2) | Purely commercial use has a narrow qualifying condition | commercial context, materiality, normal-exploitation effect | REVIEW unless exception facts are established; FAIL where explicitly adverse | Requires evaluative facts |
| Reg. 30(3) | Developer retains records of type, source, purpose, date | four core fields + record id | FAIL when absent | Express record-retention requirement |
| Reg. 30(4) | No unjustified prejudice to legitimate author interests / exploitation opportunity | impact assessment + evidence | REVIEW if uncertain; FAIL if explicitly adverse | Predominantly legal/economic judgment |
| Reg. 30(5) | No prohibited transformation/republication/public availability or unnecessary final-product inclusion absent permission/public domain | output inclusion, transformation/publication flags, permission/public-domain status | FAIL on explicit prohibited configuration | Can detect some direct contradictions |
| Reg. 30(6) | Independently protected elements must be respected | independent-rights assessment and linked evidence | REVIEW when elements exist but assessment incomplete | May involve multiple rights/owners |

## Core Article 30(3) record tuple

The regulation expressly requires retention of information corresponding to:

```text
(work type, source, purpose of use, date of use)
```

IPEL treats this tuple as the **minimum record-retention core**, not as the complete legal-compliance record.

## Evidence layers

### L0 — Assertion
A human or process writes a value.

### L1 — Referenced assertion
The value points to an external document, license, receipt, archive event, or policy.

### L2 — Content-bound evidence
The referenced artifact is bound to a cryptographic digest.

### L3 — Event-bound evidence
The artifact, actor, work digest, and timestamp are linked to a specific acquisition/use event.

### L4 — Tamper-evident chain
Events are chained or signed so later modifications become detectable.

The Stage-001 schema reaches primarily L2/L3. A later stage will test L4 designs.

## Critical distinction

`source_uri + sha256` can establish which bytes a record refers to. It **cannot by itself establish** publication lawfulness, acquisition lawfulness, ownership, license scope, or absence of market harm. Those remain separate claims requiring evidence or human review.
