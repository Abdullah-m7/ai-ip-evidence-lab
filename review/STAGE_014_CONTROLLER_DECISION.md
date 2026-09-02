# Stage 014 Controller Decision — Paper A

**Decision:** `NARROW`
**Paper disposition:** continue Paper A under major revision; do not withdraw.
**Verified Stage014 source:** `a54393c329fae6efd0066d9eda8247697aaa25b3` + uncommitted Stage014 implementation on `stage/014-corrected-profile-benchmark`.

## Why not KEEP
Stage011 already established that generic claims such as a missing AI-copyright evidence layer, auditability by design, provenance insufficiency, or evidentiary observability as a new concept are substantially anticipated by prior work. Stage014 does not restore those broad novelty claims.

## Why not WITHDRAW
The narrower contribution survives the corrected legal profile and now has substantially stronger non-human evidence:
- 59 cases across 13 encoded legal conditions on profile `0.2.0`;
- 59/59 expected outcomes and rule/severity/marker findings reproduced;
- 55/55 constructible corrected-profile round-trips preserve gate outcome, Article 30(3) tuple, Article 37(1) tuple, and zero semantic loss;
- the frozen semantic-equivalence rubric yields 0/4 safe delegation for Article 30(3) core fields and 0/2 for Article 37(1) propositions;
- the only safe delegation is `work.title -> C2PA dc:title`, a non-gate-operative descriptive field;
- the declared naive provenance baseline produces demonstrable false equivalence and signal-driven instability, whereas the rubric-governed mapping preserves all 59 outcomes under both signal configurations.

## Narrowed contribution that survives
Paper A should claim only the combination below as its contribution:

> A jurisdiction-specific, use-event-level evidence profile derived from Saudi Arabia's Article 26(4), Article 37(1), and Implementing Regulation Article 30 pathway, coupled to executable tests showing when mature provenance and rights-signaling semantics are not safely substitutable for the legally relevant evidence propositions, while preserving a hard boundary between technical evidence state and legal conclusion.

The contribution is the **specific statutory decomposition + executable semantic-boundary experiment + corrected-profile benchmark**, not generic provenance, auditability, reviewability, or rights expression.

## Claims to retire or narrow
- Retire standalone novelty for a generic "missing evidence layer".
- Treat auditability/reviewability as prior intellectual foundations.
- Do not claim priority for C2PA use in AI copyright management.
- Do not claim provenance transparency insufficiency as new.
- Do not claim broad cross-jurisdictional field portability; generalize the method only.
- Do not claim conceptual priority for "evidentiary observability".
- Preserve historical Stage003 `0/4` and five-case results as legacy profile `0.1.0` evidence only; do not describe them as corrected-profile results.

## Remaining submission gates
`NARROW` is not a submission-readiness decision. Paper A remains `MAJOR_REVISION` until at least:
1. the manuscript is rewritten around the narrowed novelty position and corrected Stage014 results;
2. 2026 closest-prior-work and rights-expression literature are integrated explicitly;
3. the Stage002 integrity negative result is restored to the empirical narrative;
4. an ecological, lawfully usable trace demonstration is added or the absence is explicitly accepted as a venue-limiting weakness;
5. evidentiary sufficiency versus minimization/confidentiality/retention risk is addressed;
6. all legacy 0.1.0 wording is audited so no corrected-profile implication remains.

## Controller verification performed
- reran `experiments/stage014_corrected_profile_benchmark.py` twice;
- generated Stage014 artifacts were byte-identical before/after both reruns;
- `python3 -m unittest tests.test_stage014_benchmark -v`: 31 tests passed;
- `python3 -m unittest discover -s tests`: 187 tests passed;
- independent invariant checks matched Stage014 machine results;
- no manuscript, Stage012, Stage013, or legacy Stage003 artifact was modified;
- `legal_conclusion=false` remains invariant.

**Final Stage014 scientific decision:** `NARROW_AND_CONTINUE`.
