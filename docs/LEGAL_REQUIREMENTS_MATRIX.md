# Saudi 2026 AI-Development Evidence Matrix

**Current scope (profile 0.2.0):** Copyright Law Article 26(4) + Copyright Law Article 37(1) + Implementing Regulations Article 30(1)–(6).

This document maps legal conditions to evidence that a technical system can preserve. It is a research abstraction, not an authoritative interpretation by the Saudi Authority for Intellectual Property or a court.

## Legal-profile versioning

| Record version | Declared legal scope | Status |
|---|---|---|
| `0.1.0` | Copyright Law Art. 26(4) + Implementing Regulations Art. 30 | **LEGACY / INCOMPLETE FOR THE FULL PATHWAY** — retained only to reproduce Stages 001–005 |
| `0.2.0` | Copyright Law Art. 26(4) + Art. 37(1) + Implementing Regulations Art. 30(1)–(6) | **CURRENT** for new legal-completeness experiments |

Historical outputs are not silently relabelled as 0.2.0. Any empirical result that depends on the corrected legal scope must be rerun under the current profile.

## Requirements matrix

| Rule source | Condition / risk | Observable evidence candidate | Gate treatment | Why |
|---|---|---|---|---|
| Law 26(4) | Work was lawfully published | publication status, publication evidence reference | REVIEW if unverified; FAIL if explicitly false | Legal status may require external verification |
| Law 26(4) | Original copy was lawfully acquired | acquisition method, acquisition status, receipt/license/source evidence | REVIEW if unverified; FAIL if explicitly false | A URI or hash alone does not prove lawful acquisition |
| Law 26(4) | Copying is limited to the AI-development purpose | declared purpose, copied portion/extent, necessity rationale | REVIEW when necessity is uncertain; FAIL when explicitly unsupported | Proportionality is contextual |
| **Law 37(1)** | Use under Arts. 26–36 must not conflict with normal exploitation of the work | `article37_context.normal_exploitation_conflict` + `normal_exploitation_basis` | REVIEW if unresolved/not assessed or favorable without basis; FAIL if conflict is explicit | Cross-cutting statutory safeguard; applies beyond commercial context |
| **Law 37(1)** | Use under Arts. 26–36 must not cause unjustified prejudice to legitimate interests of rightsholders | `article37_context.rightsholder_legitimate_interests_prejudice` + `rightsholder_interests_basis` | REVIEW if unresolved/not assessed or favorable without basis; FAIL if unjustified prejudice is explicit | Actor and legal test differ from the author-specific IR 30(4) assessment |
| Reg. 30(1) | Copying/analysis limited to what AI development requires | extent + necessity rationale | REVIEW when uncertain; FAIL when explicitly unsupported | Context-sensitive |
| Reg. 30(1) | No republication, distribution, or direct commercial exploitation under the exception | event flags + output/delivery evidence | FAIL on explicit prohibited use | Encoded direct contradiction |
| Reg. 30(2) | Purely commercial use has a narrow qualifying condition | commercial context, materiality, normal-exploitation **impact** | REVIEW unless qualifying facts are established; FAIL where explicitly adverse | This commercial-context test is not treated as identical to Art. 37(1)'s general no-conflict test |
| Reg. 30(3) | Developer retains records of type, source, purpose, date | four core fields + record id | FAIL when absent | Express record-retention requirement |
| Reg. 30(4) | No unjustified prejudice to legitimate **author** interests / exploitation opportunity | author-interest prejudice, exploitation-opportunity effect, assessment basis | REVIEW if uncertain or favorable without basis; FAIL if explicitly adverse | Actor/interest formulation is not silently collapsed into Art. 37(1)'s rightsholder safeguard |
| Reg. 30(5) | No prohibited transformation/republication/public availability or unnecessary final-product inclusion absent permission/public domain | output inclusion, transformation/publication flags, permission/public-domain status | FAIL on explicit prohibited configuration | Can detect some direct contradictions |
| Reg. 30(6) | Independently protected elements must be respected | independent-rights assessment and linked evidence | REVIEW when elements exist but assessment incomplete | May involve multiple rights/owners |

## Why Article 37(1) is represented separately

The corrected profile deliberately does **not** reuse two superficially similar fields as automatic substitutes:

1. `use.normal_exploitation_impact` belongs to the Implementing Regulation Article 30(2) commercial-context pathway. Article 37(1) instead supplies a general statutory condition that the use not **conflict with** normal exploitation. The 0.2 profile therefore records `article37_context.normal_exploitation_conflict` separately.
2. `rights_context.legitimate_interests_prejudice` was designed around Implementing Regulation Article 30(4), which refers to the author's legitimate interests and exploitation opportunity. Article 37(1) refers to the legitimate interests of **rightsholders**. The corrected profile therefore records a distinct rightsholder assessment.

This separation is methodological, not a claim that the concepts can never overlap in a concrete legal analysis. It prevents the software from assuming equivalence before that equivalence is legally established.

## Core Article 30(3) record tuple

The regulation expressly requires retention of information corresponding to:

```text
(work type, source, purpose of use, date of use)
```

IPEL treats this tuple as the **minimum record-retention core**, not as the complete legal-compliance record. Article 37(1) makes the incompleteness of a four-field-only compliance view especially clear.

## Evidence layers

### L0 — Assertion
A human or process writes a value.

### L1 — Referenced assertion
The value points to an external document, license, receipt, archive event, policy, or assessment.

### L2 — Content-bound evidence
The referenced artifact is bound to a cryptographic digest.

### L3 — Event-bound evidence
The artifact, actor, work digest, and timestamp are linked to a specific acquisition/use event.

### L4 — Tamper-evident chain / external trust boundary
Events or assertions are bound so later modification can be detected relative to a preserved checkpoint, signature, or mature provenance system.

## Critical distinctions

`source_uri + sha256` can establish which bytes a record refers to. It **cannot by itself establish** publication lawfulness, acquisition lawfulness, ownership, license scope, absence of conflict with normal exploitation, or absence of unjustified prejudice.

Likewise:

```text
IR-30(2) normal-exploitation impact != automatically identical to LAW-37(1) normal-exploitation conflict
IR-30(4) author-interest assessment != automatically identical to LAW-37(1) rightsholder-interest assessment
integrity evidence != truth of the recorded legal proposition
```

These distinctions are enforced in profile 0.2.0 so later semantic-delegation experiments can test equivalence rather than assume it.
