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

## Planned research tracks

1. **Training provenance** — evidence for acquisition and use of works during AI development.
2. **Human creative control** — evidence of human contribution in AI-assisted works.
3. **Agentic IP** — when an AI agent should ACT / CLARIFY / DEFER / REFUSE during rights-sensitive actions.

