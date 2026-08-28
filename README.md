# AI–IP Evidence Lab

A research lab for **verifiable intellectual-property evidence in AI systems**.

The project starts from a concrete legal-engineering problem created by Saudi Arabia's 2026 Copyright Law: an AI developer may need not only to satisfy legal conditions for copying works during AI development, but also to **show what work was used, where it came from, why it was used, when it was used, and whether the surrounding conditions were respected**.

This repository studies the gap between a legal rule and the evidence needed to demonstrate that an AI pipeline behaved consistently with that rule.

> **Core question:** What evidence must an AI developer preserve so that a later reviewer can reconstruct and evaluate the use of copyrighted works in AI development?

## Stage 001 — Saudi AI-training evidence prototype

Stage 001 operationalizes two current Saudi provisions:

- Copyright Law (Royal Decree M/169, 2026), Article 26(4): the AI-development copying exception is conditioned on lawful publication, lawful acquisition of the original copy, and copying limited to the development purpose.
- Implementing Regulations (31 July 2026), Article 30: adds constraints concerning necessity, republication/distribution/direct commercial exploitation, certain purely commercial uses, record retention, prejudice to legitimate author interests, final-product inclusion, and independently protected elements.

The first prototype is **IPEL — IP Evidence Ledger**. It is not a legal-opinion engine. It checks whether a structured evidence record contains and contradicts facts relevant to those provisions, and then returns:

- `PASS_EVIDENCE_GATE` — no encoded contradiction and the required evidence fields are present;
- `REVIEW_REQUIRED` — a fact-sensitive or uncertain legal condition needs human review;
- `FAIL_EVIDENCE_GATE` — the record contains an encoded contradiction to a hard rule or lacks a core required record field.

A PASS is **not** a conclusion of legal compliance.

## Repository map

- `docs/RESEARCH_CHARTER.md` — falsifiable research program and hypotheses.
- `docs/LEGAL_REQUIREMENTS_MATRIX.md` — legal rule → observable evidence mapping.
- `docs/THREAT_MODEL.md` — what provenance can and cannot prove.
- `schemas/ipel-record.schema.json` — evidence-record contract.
- `src/ipel/validator.py` — deterministic Stage-001 evidence gate.
- `examples/records/` — synthetic positive/negative records.
- `tests/` — executable behavioral tests.

## Quick start

```bash
python3 -m unittest discover -s tests -v
python3 -m src.ipel.validator examples/records/valid.json
python3 -m src.ipel.validator examples/records/invalid_missing_source.json
```

## Official legal sources

- Saudi Copyright Law, Royal Decree M/169 (Umm Al-Qura): https://www.uqn.gov.sa/details?p=28845
- Implementing Regulations of the Copyright Law (Umm Al-Qura, 31 July 2026): https://www.uqn.gov.sa/decisions-and-regulations/4001498
- National Center for Archives and Records, Copyright Law document: https://ncar.gov.sa/

## Research posture

This is a research prototype, not legal advice. It deliberately separates:

1. **fact capture** — what the system can record;
2. **evidence integrity** — whether those records are tamper-evident and internally consistent;
3. **rule evaluation** — what deterministic conditions can be checked;
4. **legal judgment** — what remains context-dependent and must be decided by a qualified human or competent authority.

## Stage 002 — integrity boundary experiment

Stage 002 adds a tamper-evident work/use event chain and an explicit external checkpoint. The experiment detects committed-history mutation, deletion, insertion, reordering, recomputed-history forgery, and tail truncation **when the original checkpoint is available**.

The negative result is equally important: an internally consistent hash chain alone cannot detect a fully rehashed rewrite or tail truncation. The prototype therefore never treats local hash consistency as proof of historical truth.

Run the attack matrix:

```bash
python3 experiments/stage002_attack_matrix.py
```

See `docs/EVENT_CHAIN_SPEC.md`, `docs/C2PA_CROSSWALK.md`, and `reports/stage002_attack_matrix.json`. The current interoperability baseline is C2PA 2.4 AI/ML guidance + CAWG Training and Data Mining Assertion 1.1.

## Stage 003 — C2PA-backed legal-evidence profile

Stage 003 tests whether IPEL can layer jurisdiction-specific legal evidence over C2PA 2.4 and CAWG Training and Data Mining 1.1 semantics without false equivalence. The committed experiment preserves the Article 30(3) tuple and Stage-001 gate outcome across PASS/REVIEW/FAIL cases while keeping C2PA trust/TDM signals from becoming legal conclusions.

A key negative result is intentional: none of the four Article 30(3) minimum fields (work type, source, purpose, date) are delegated to C2PA in the current profile because the closest generic fields are not semantically equivalent enough. See `docs/C2PA_PROFILE_DECISIONS.md` and `reports/STAGE_003_REPORT.md`.

```bash
PYTHONPATH=. python3 experiments/stage003_semantic_roundtrip.py
python3 -m unittest discover -s tests -v
```

## Stage 004 — real C2PA hard-binding experiment

Stage 004 uses pinned `c2patool 0.27.16` to generate and validate an actual embedded C2PA manifest on a synthetic JPEG. A one-byte asset mutation triggers `assertion.dataHash.mismatch`; signed assertion corruption triggers `assertion.hashedURI.mismatch`; signing-credential corruption triggers `claimSignature.mismatch`.

The clean artifact deliberately uses c2patool's development signer: its claim signature and data hash validate while signer trust remains unestablished. This keeps cryptographic validity, provenance trust, and Saudi legal-evidence readiness as separate dimensions. A valid CAWG `allowed` signal never upgrades unlawful acquisition or missing output permission.

See `docs/C2PA_CONFORMANT_EXPERIMENT.md` and `reports/STAGE_004_REPORT.md`.

```bash
./scripts/install_c2patool.sh .tools/c2patool
PYTHONPATH=. python3 experiments/stage004_conformant_c2pa.py --c2patool .tools/c2patool
```

## Stage 005 — cross-validator and trust-boundary benchmark

Stage 005 validates the Stage-004 real C2PA artifact through a second conformance-oriented CLI. The two surfaces share c2pa-rs lineage but use different observed engine versions (`0.90.16` vs `0.78.0`). They agree on clean validity and all three corruption categories.

The same clean artifact changes from `untrusted` under default trust to `trusted` under an explicitly configured test trust list, while the IPEL legal gate remains unchanged. A correctly signed TDM assertion with an invalid `use=maybe` value is cryptographically valid but semantically rejected.

The stage explicitly reports `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`; cross-validator does not mean independent cryptographic implementation. See `docs/C2PA_CROSS_VALIDATOR_BENCHMARK.md` and `reports/STAGE_005_REPORT.md`.

```bash
./scripts/install_c2patool.sh .tools/c2patool
./scripts/install_c2pa_conformance_tool.sh .tools/c2pa-validate
PYTHONPATH=. python3 experiments/stage005_cross_validator.py --c2patool .tools/c2patool --cross-validator .tools/c2pa-validate
```

## Planned research tracks

1. **Training provenance** — evidence for acquisition and use of works during AI development.
2. **Human creative control** — evidence of human contribution in AI-assisted works.
3. **Agentic IP** — when an AI agent should ACT / CLARIFY / DEFER / REFUSE during rights-sensitive actions.

