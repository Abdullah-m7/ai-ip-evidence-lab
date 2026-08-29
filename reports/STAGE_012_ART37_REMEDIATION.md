# Stage 012 Report — Article 37(1) Legal-Profile Remediation

## Status

**P0 LEGAL-SCOPE REMEDIATION IMPLEMENTED — PAPER A REMAINS ON SCIENTIFIC HOLD**

Stage 011 identified a material legal-completeness defect: the project described the Saudi AI-development pathway using Copyright Law Article 26(4) and Implementing Regulation Article 30, while Copyright Law Article 37(1) imposes a cross-cutting safeguard on uses under Articles 26–36.

Official source: Saudi Copyright Law, *Umm Al-Qura*, Article 37(1):
https://www.uqn.gov.sa/details?p=28845

The controlling Arabic provision requires the relevant uses not to conflict with normal exploitation of the work and not to cause unjustified prejudice to the legitimate interests of rightsholders. The English labels used below are analytical modeling terms, not an official translation.

## Remediation

The project now distinguishes two legal profiles:

| Record version | Profile | Scope status |
|---|---|---|
| `0.1.0` | `sa-copyright-2026-art26-4-ir30-legacy-v0.1` | legacy; declared full-pathway scope incomplete |
| `0.2.0` | `sa-copyright-2026-art26-4-art37-1-ir30-v0.2` | current corrected declared scope |

Profile 0.2.0 adds a required `article37_context` with four fields:

- `normal_exploitation_conflict`;
- `rightsholder_legitimate_interests_prejudice`;
- `normal_exploitation_basis`;
- `rightsholder_interests_basis`.

The evidence gate fails on an explicit conflict or unjustified prejudice, requires review when the condition is unresolved, and also requires review when a favorable assertion has no recorded assessment basis.

## Important semantic result

Stage 012 does **not** treat existing Regulation Article 30 fields as automatic substitutes for Article 37(1).

The corrected model distinguishes:

```text
IR-30(2) commercial-context normal-exploitation impact
    != automatically LAW-37(1) cross-cutting normal-exploitation conflict

IR-30(4) author-interest / exploitation-opportunity assessment
    != automatically LAW-37(1) rightsholder legitimate-interests assessment
```

Regression tests explicitly set the Regulation fields to favorable values while setting the Article 37 proposition to an adverse value; the Article 37 failure must survive.

This is a conservative evidence-modeling choice. It does not claim that the legal concepts can never overlap in a concrete case.

## Historical-result preservation

The correction is intentionally versioned rather than retroactive.

Existing Stages 001–005 used `record_version=0.1.0`. Their historical outputs remain reproducible and retain their original gate outcomes, but the gate now exposes:

```text
legal_profile_id = sa-copyright-2026-art26-4-ir30-legacy-v0.1
declared_scope_complete = false
```

New 0.2.0 records expose:

```text
legal_profile_id = sa-copyright-2026-art26-4-art37-1-ir30-v0.2
declared_scope_complete = true
```

`declared_scope_complete=true` refers only to the project's declared provision set. It is not a legal conclusion and does not assert that no other law may matter.

## Negative result for Paper A

Fixing the model does **not** rehabilitate the old Paper A experiments automatically.

The Stage-003 five-case semantic round-trip and the historical `0/4` delegation finding were generated against the 0.1.0 profile. They therefore remain historical proof-of-concept evidence and must not be described as testing the corrected Article 37-inclusive pathway.

This creates a new empirical obligation rather than a narrative patch: the semantic mapping and condition-coverage experiments must be rerun on profile 0.2.0.

## Acceptance gates

Stage 012 is acceptable only if all of the following hold:

1. Article 37(1) is present in the legal requirements matrix.
2. 0.2.0 records cannot omit `article37_context` without failing closed.
3. explicit normal-exploitation conflict produces `FAIL_EVIDENCE_GATE`.
4. explicit unjustified rightsholder prejudice produces `FAIL_EVIDENCE_GATE`.
5. unresolved Article 37 assessments produce `REVIEW_REQUIRED`.
6. favorable Article 37 assertions without a basis produce `REVIEW_REQUIRED`.
7. favorable IR-30 fields cannot mask an adverse Article 37 fact.
8. legacy 0.1.0 results preserve historical outcomes but are machine-labelled scope-incomplete.
9. unsupported record versions fail closed.
10. `legal_conclusion=false` remains invariant.

## Scientific decision

**GO to the next P0 revision only after CI confirms the remediation.**

The next scientific step is not journal formatting. It is to formalize the semantic-equivalence/delegation rubric and then build the full Article 26(4) + Article 37(1) + Regulation Article 30 condition-coverage benchmark.
