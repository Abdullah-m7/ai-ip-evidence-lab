# Stage 013 Report — Preregistered Semantic-Equivalence Rubric

## Status

**PRE_OUTCOME_RUBRIC_LOCK CREATED — NO CORRECTED DELEGATION OUTCOMES RUN**

Stage 011 found that the historical Stage-003 phrase “sufficiently equivalent” left too much researcher discretion. Stage 013 fixes the method before rerunning any v0.2 Article-37-inclusive benchmark.

## Frozen source

Rubric source commit:

`037070dae5a93a1ef58c806a537784f378226998`

The lock records canonical JSON hashes for:

- `benchmarks/stage013/rubric_definition.json`;
- `benchmarks/stage013/candidate_registry.json`.

The candidate registry has `benchmark_executed=false` and every candidate has `assessment_status=NOT_RUN`.

## Decision rule

Four classes are preregistered:

- `SAFE_DELEGATION`;
- `PARTIAL_SUPPORT`;
- `NOT_SAFE_TO_DELEGATE`;
- `NO_CANDIDATE`.

Safe delegation requires all applicable dimensions to pass, a successful controlled round-trip, a maintained normative semantic, and no dependence on validation state, signer trust, rights preference, or a legal conclusion.

Nine of eleven dimensions are critical vetoes. A high aggregate closeness score cannot override one of those failures.

## Standards observations used only to define candidates

The registry is grounded in maintained specifications, not candidate outcomes:

- C2PA 2.4 Ingredient v3 defines `dc:title` as a human-readable ingredient name, `dc:format` as media type, `relationship=inputTo`, hashed data references and `informationalURI`.
- C2PA action/time constructs distinguish action timestamps and trusted RFC3161-backed timestamp evidence; field-name similarity is not assumed to establish the legally relevant `use.date` proposition.
- CAWG Training and Data Mining Assertion 1.1 communicates `allowed`, `notAllowed`, or `constrained` information for mining/training uses; it is not preregistered as the developer's actual purpose.

Normative anchors:
- https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- https://cawg.io/training-and-data-mining/1.1/

## Candidate set

Eleven initial candidates/hypotheses are frozen, covering:

- title;
- work type;
- source;
- use purpose;
- use date;
- the two Article 37 evaluative propositions.

The two Article 37 rows are explicit `NO_CANDIDATE` hypotheses at lock time, not findings. If later standards research identifies a maintained normative candidate before outcome execution, the registry must version-bump and the old lock remains preserved.

## Anti-gaming properties

The implementation fails closed when:

- a dimension is missing;
- a non-preregistered `NOT_APPLICABLE` exemption is introduced;
- a critical dimension fails;
- safe equivalence relies on signer trust, validation state, rights preference, or legal inference;
- a custom/private assertion is presented as proof of generic-standard equivalence;
- controlled round-trip has not passed.

`PARTIAL_SUPPORT` always retains the IPEL field.

## Scientific consequence

Stage 013 intentionally produces **no replacement for the historical `0/4` result**. That number remains a legacy v0.1 result until a corrected v0.2 benchmark is run under this frozen rubric.

This stage therefore removes a methodological weakness without manufacturing a stronger empirical result.

## Next step after lock verification

Build the Article 26(4) + Article 37(1) + Regulation Article 30 condition × state benchmark, then apply this rubric to candidate mappings and compare IPEL against a naïve provenance-mapping baseline.
