# Stage 003 Report — C2PA-backed IPEL Semantic Round-trip

## Question
Can an IPEL record be layered over C2PA/CAWG semantics without duplicating generic provenance or silently converting provenance/trust signals into Saudi legal facts?

## Method
Five synthetic benchmark cases were encoded into the Stage-003 C2PA-aligned profile and reconstructed into the Stage-001 review model:
1. clean PASS case;
2. unverified-publication REVIEW case;
3. prohibited-distribution FAIL case;
4. `allowed + trusted` but explicitly unlawful-acquisition FAIL case;
5. `allowed + trusted` but no output permission FAIL case.

The experiment compares every original leaf value with the reconstructed record, verifies the Article 30(3) four-field tuple, compares Stage-001 gate outcomes, and checks generic-field duplication.

## Result
Across the 5 committed benchmark cases:
- semantic loss after round-trip: **0 cases / 0 changed leaf paths**;
- Article 30(3) tuple preservation: **5/5**;
- PASS / REVIEW / FAIL outcome preservation: **5/5**;
- duplicate generic fields in valid profiles: **0**;
- false-equivalence attacks resisted: **2/2**;
- malformed profile missing `work.source`: rejected fail-closed.

## Most important finding
The interoperability review narrowed the safe C2PA delegation substantially. Only one current IPEL leaf fact was treated as safely generic enough to move out of the jurisdictional payload: work title (`dc:title`). The raw work digest remains in IPEL until a real C2PA hard-binding / hashed-reference implementation is tested.

**0/4 of the Saudi Article 30(3) minimum tuple were delegated to C2PA.** Work type, source, purpose of use, and date of use all remain jurisdiction-specific in this prototype because the closest C2PA fields are not semantically equivalent enough to substitute without additional capture rules.

This is a useful negative result: the legal-evidence layer is not merely a re-labelling of generic provenance metadata.

## False equivalence finding
A profile may simultaneously state:
- C2PA Manifest state = `valid`;
- trust state = `trusted`;
- CAWG `cawg.ai_training` = `allowed`;
- IPEL acquisition status = `false`.

Reconstruction preserves the acquisition status and the Stage-001 result remains `FAIL_EVIDENCE_GATE`. The C2PA/CAWG signals never override the legal evidence state.

## Limitations
- The representation is not a C2PA Manifest and is not cryptographically signed.
- A conformant content-digest delegation has not yet been implemented; the raw digest remains in IPEL.
- The benchmark is synthetic and small.
- The Stage-001 legal model itself remains a research abstraction, not an authoritative interpretation or legal opinion.
- Real C2PA SDK round-trip testing remains future work.

## Decision
**PASS Stage 003 foundation.** The narrow novelty claim survives this experiment: IPEL is best pursued as a jurisdiction-specific legal-evidence profile that references mature provenance infrastructure, while machine-visible barriers prevent provenance/trust signals from becoming legal conclusions.
