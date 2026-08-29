# Semantic Equivalence Rubric — v1.0.0

## Purpose

This rubric is frozen **before** the corrected v0.2 legal-profile delegation benchmark is run. Its purpose is to prevent post-hoc use of the phrase “sufficiently equivalent.” A C2PA/CAWG semantic may replace an IPEL jurisdiction-specific fact only when the legally relevant proposition survives substitution without hidden inference.

Stage 013 freezes method only. It reports no new delegation count.

## Decision classes

- `SAFE_DELEGATION` — generic semantic may replace the IPEL leaf for the declared experiment; controlled round-trip is mandatory.
- `PARTIAL_SUPPORT` — generic semantic is evidentially useful, but the IPEL leaf remains.
- `NOT_SAFE_TO_DELEGATE` — semantic substitution is prohibited.
- `NO_CANDIDATE` — no maintained normative generic semantic is registered.

## Eleven dimensions

| Dimension | Critical veto? | Question |
|---|---:|---|
| referent identity | yes | Do both fields denote the same legally relevant object/work/event? |
| predicate semantics | yes | Do they assert the same proposition rather than adjacent metadata? |
| subject/actor identity | yes | Is the same actor/subject preserved? |
| event/process anchor | yes | Is the fact attached to the same use/acquisition/publication event? |
| temporal semantics | yes | Is the same time proposition and trust level preserved? |
| qualifier/scope preservation | yes | Are purpose, context, conditions, and legal qualifiers retained? |
| value-domain compatibility | no | Can the target encode the source value without coercive loss? |
| evidentiary/normative role | yes | Are fact, preference, permission, trust and legal assessment kept distinct? |
| round-trip recoverability | yes | Can the IPEL proposition be reconstructed without hidden state/inference? |
| inference independence | yes | Does equivalence avoid relying on validation state, signer trust, rights preference or a legal conclusion? |
| normative maintained-spec status | yes | Is the semantic actually defined by a maintained normative standard rather than a private/custom extension? |

A critical failure can never be offset by an aggregate score.

## `NOT_APPLICABLE`

`NOT_APPLICABLE` is allowed only where preregistered by proposition class. For an entity attribute such as a human-readable title, subject/actor, event anchor and temporal semantics may be genuinely inapplicable. Event attributes and legal-evaluative assertions have no preregistered N/A dimensions in v1.0.0. An evaluator cannot introduce a new N/A exemption without a rubric version bump.

## Safe-delegation rule

`SAFE_DELEGATION` requires:

1. every applicable dimension = `PASS`;
2. every applicable critical dimension = `PASS`;
3. candidate kind is `NORMATIVE_FIELD` or `NORMATIVE_ASSERTION`;
4. controlled round-trip was executed and passed;
5. no semantic equivalence inference depends on `VALIDATION_STATE`, `SIGNER_TRUST`, `RIGHTS_PREFERENCE`, or `LEGAL_CONCLUSION`;
6. the candidate semantic is normative and maintained.

A custom assertion can preserve IPEL data and can be useful interoperability engineering, but it is **not evidence that the generic standard already supplies an equivalent semantic**.

## Partial support

`PARTIAL_SUPPORT` always retains the IPEL fact. Examples may include a provenance URI that helps identify supporting material, a C2PA relationship that establishes that an ingredient was an input, or a CAWG signal that supplies a rights-holder usage declaration. These can be evidence without being substitutes for the legally specified proposition.

## Normative anchors frozen for candidate assessment

- **C2PA 2.4 Ingredient v3.** `dc:title` is a human-readable ingredient name; `dc:format` is an IANA media type; `relationship=inputTo` describes an ingredient as input to a computational process; `data` is a hashed reference; `informationalURI` points to an informational page. Source: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- **C2PA 2.4 actions/time.** Action `when` is an action date/time; C2PA distinguishes ordinary/claimed time information from RFC3161-backed trusted timestamps. A timestamp therefore must be assessed for the proposition it timestamps rather than equated with `use.date` from field-name similarity alone. Same normative source.
- **CAWG Training and Data Mining Assertion 1.1.** It supplies `allowed`, `notAllowed`, or `constrained` information about specified mining/training uses. It is assessed as a rights/usage signal, not assumed to be the developer’s actual use purpose. Source: https://cawg.io/training-and-data-mining/1.1/

## Candidate registry

The candidate registry is frozen with assessment state `NOT_RUN`. It contains candidate semantics for title, work type, source, purpose and date, plus explicit no-candidate hypotheses for the two Article 37 evaluative propositions. These are hypotheses/candidates, not outcomes.

## Change control

After a candidate outcome is observed:

- changing any dimension, criticality, N/A rule, threshold, prohibited inference, or candidate meaning requires a new rubric version;
- the original v1.0.0 result must remain reported alongside any new version if direct comparison is made;
- a new custom C2PA assertion cannot be retroactively counted as proof that C2PA 2.4 had a generic equivalent field.

The benchmark may falsify the historical `0/4` intuition. That is an acceptable result.
