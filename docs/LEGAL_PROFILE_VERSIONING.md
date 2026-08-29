# IPEL Legal-Profile Versioning

## Purpose

IPEL versions the **legal mapping**, not only the JSON syntax. A record version therefore identifies which legal pathway the evidence gate actually models.

This prevents a later manuscript or experiment from silently treating an older result as if it had evaluated legal conditions that were not represented at the time.

## Profiles

### `0.1.0` — historical legacy profile

Legal profile ID:

`sa-copyright-2026-art26-4-ir30-legacy-v0.1`

Declared scope at the time of Stages 001–005:

- Copyright Law Article 26(4);
- Implementing Regulations Article 30(1)–(6).

This profile omitted the cross-cutting condition in Copyright Law Article 37(1). It is therefore **incomplete for a claim that the full statutory/regulatory AI-development pathway has been mapped**.

The profile is retained unchanged enough to reproduce historical experiments. The gate reports:

```text
declared_scope_complete = false
```

Historical PASS/REVIEW/FAIL outcomes are not rewritten retroactively.

### `0.2.0` — current corrected profile

Legal profile ID:

`sa-copyright-2026-art26-4-art37-1-ir30-v0.2`

Declared scope:

- Copyright Law Article 26(4);
- Copyright Law Article 37(1);
- Implementing Regulations Article 30(1)–(6).

The gate reports:

```text
declared_scope_complete = true
```

This means only that the **declared project scope** includes the identified provisions. It is not a claim that the profile is an authoritative interpretation, that no other law can matter to a concrete dispute, or that a PASS outcome proves legal compliance.

## Why Article 37 has separate fields

Article 37(1) is not encoded by merely changing the citation attached to existing Regulation Article 30 fields.

Two distinctions are preserved:

1. **Normal exploitation.** Regulation Article 30(2) contains a commercial-context condition framed around an effect on normal exploitation. Article 37(1) imposes a cross-cutting condition on uses under Articles 26–36 that the use not conflict with normal exploitation. IPEL 0.2.0 keeps a separate `article37_context.normal_exploitation_conflict` proposition until legal analysis establishes when one fact can safely satisfy both tests.
2. **Protected interests.** Regulation Article 30(4) is framed around the author's legitimate interests and exploitation opportunity. Article 37(1) refers to the legitimate interests of rightsholders. IPEL 0.2.0 therefore keeps `article37_context.rightsholder_legitimate_interests_prejudice` separate from the Regulation Article 30(4) author-interest field.

This separation is intentionally conservative. It is a semantic anti-collapse rule, not a holding that the concepts never overlap.

## Migration rule

Do not transform a 0.1.0 record into 0.2.0 merely by changing `record_version`.

A valid migration must add independent evidence/assessment for:

- Article 37(1) normal-exploitation conflict; and
- Article 37(1) rightsholder legitimate-interests prejudice.

If those assessments do not exist, the 0.2.0 record must use `uncertain` or `not_assessed`, producing `REVIEW_REQUIRED` rather than manufacturing favorable facts.

## Experiment provenance rule

Stages 001–005 remain historical 0.1.0 evidence. Their numerical and categorical results remain reproducible, but they cannot be described as having tested the corrected Article 37-inclusive legal profile.

Any Paper A result that claims coverage of the corrected Saudi pathway must be generated anew under 0.2.0.

In particular:

- Stage 003's five-case semantic round-trip remains a legacy proof of concept;
- the historical `0/4` Article 30(3) delegation result remains evidence about the tested 0.1 mapping only;
- Stages 004–005 remain valid C2PA/trust-boundary experiments but do not themselves establish Article 37 condition coverage.

## Manuscript state after Stage 012

Paper A remains on **SCIENTIFIC HOLD / MAJOR REVISION** until the corrected profile is used in:

1. a declared semantic-equivalence/delegation rubric;
2. a condition × state coverage benchmark covering Article 26(4), Article 37(1), and Regulation Article 30(1)–(6);
3. the planned naïve-baseline/false-equivalence comparison.

No submission-readiness claim follows from fixing the legal profile alone.

## Source authority

The controlling legal source is the official Arabic Copyright Law published by *Umm Al-Qura*. The project uses English analytical labels for computational modeling. Those labels are not official translations, SAIP interpretations, judicial holdings, or legal advice.
