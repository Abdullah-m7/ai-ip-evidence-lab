# Paper A — Source Audit and Red-Team Claim Review

## Audit status

**FIRST-DRAFT AUDIT — PASS WITH CITATION INSERTION / SECONDARY LITERATURE COMPLETION REQUIRED**

The current draft is suitable for internal scientific review. The original comparative-copyright gap has been materially reduced; remaining work is mainly inline citation insertion, broader dataset-documentation/evidence literature, and final bibliographic verification.

## 1. Saudi legal claims

| Draft proposition | Primary source | Audit |
|---|---|---|
| New Saudi Copyright Law adopted in 2026 under Royal Decree M/169 | Umm Al-Qura Royal Decree and Copyright Law | PASS |
| Art. 26(4) addresses copying original works for AI product/algorithm development | Official Copyright Law | PASS |
| Art. 26(4) conditions include lawful publication, lawful acquisition and purpose-limited copying | Official Copyright Law | PASS |
| Implementing Regulation Art. 30 applies to the Art. 26(4) use pathway | Official Implementing Regulations | PASS |
| Art. 30(3) requires records of type, source, purpose, date | Official Implementing Regulations | PASS |
| Art. 30 contains necessity/downstream use/commercial/author-interest/independent-elements conditions | Official Implementing Regulations | PASS |

**Boundary:** The manuscript states that the Arabic official text governs and labels the project mapping as a research abstraction rather than an authoritative SAIP/court interpretation.

## 2. External technical-standard claims

| Proposition | Normative / official source | Audit |
|---|---|---|
| C2PA is content-provenance/authenticity infrastructure | C2PA 2.4 | PASS |
| C2PA Ingredient v3 can represent assets/data used as AI/ML inputs | C2PA 2.4 Ingredient section | PASS |
| CAWG 1.1 communicates training/data-mining usage information | CAWG 1.1 | PASS |
| TDM·AI communicates machine-readable AI/TDM preferences | TDM·AI official docs | PASS |
| TDM·AI distinguishes public declarations from negotiated licensing | TDM·AI opt-out/licensing documentation | PASS |
| WIPO AIII focuses on technical/operational IP infrastructure rather than setting law/policy | WIPO AIII official pages | PASS |

## 3. Peer-reviewed related-work claims

| Proposition | Source set | Audit |
|---|---|---|
| Dataset provenance/licensing documentation is widely incomplete/inconsistent | Longpre et al., Nature Machine Intelligence 2024 | PASS |
| Automatically processable regulation faces open-texture/interpretive limitations | Guitton et al., Artificial Intelligence and Law | PASS |
| AI & Law journal scope includes computational models of law/legal reasoning and AI legal applications | Bench-Capon 2022 | PASS |
| AI-training copyright rules differ materially across major jurisdictions | de la Durantaye 2025 + US/EU/UK/Japan sources | PASS |
| US AI-input fair use remains doctrinally contested and is developing through recent decisions/reports | Ginsburg 2025; Bruni 2026 | PASS |
| EU AI-training analysis centers on DSM TDM exceptions, reservations, transparency and AI Act interaction | Tyagi 2024; Guadamuz 2025; CLSR 2025 | PASS |
| UK policy remains contested between opt-in/opt-out, transparency and remuneration models | Kretschmer et al. 2025 | PASS |
| Law-by-design scholarship distinguishes technical/organisational implementation, documentation and enforcement dimensions | Djeffal 2025; Regulation by Design 2024 | PASS |
| Technical evidence/auditability can be framed as an enforceability condition rather than merely a transparency value | IJLIT 2026 source | PASS — final metadata check pending |

### Remaining literature work

Before submission:

- add 2–4 foundational dataset-documentation sources beyond DPI where directly relevant;
- deepen evidence-preservation/auditability literature that focuses on later enforcement/contestability, not only ex-ante compliance-by-design;
- search for credible Saudi-specific peer-reviewed commentary on the 2026 Copyright Law published after entry into force;
- verify full metadata for every reference and convert to final journal citation style.

## 4. Project-generated Results claims

All Results claims are tied to committed project artifacts rather than memory or narrative summaries.

| Result | Repository evidence | Audit |
|---|---|---|
| Stage 003: 0 semantic-loss cases / 5 outcome-preserving cases | `reports/STAGE_003_REPORT.md`; machine report | PASS |
| Stage 003: 0/4 core fields delegated in tested mapping | Stage-003 report/profile | PASS — wording explicitly scoped to tested mapping |
| Stage 004: three corruption classes detected | Stage-004 report/machine output | PASS |
| Stage 004: cryptographic validity vs untrusted signer | Stage-004 report | PASS |
| Stage 004: exit-code ≠ validation-state finding | Stage-004 report | PASS |
| Stage 005: same normalized corruption categories on two surfaces | Stage-005 report | PASS |
| Stage 005: different observed c2pa-rs versions but shared lineage | Stage-005 report | PASS |
| Stage 005: malformed signed TDM semantic rejection | Stage-005 report/tests | PASS |

## 5. Human-data firewall

Current draft contains **no claimed human result**.

Allowed statements:

- benchmark constructed;
- preregistration/adjudication infrastructure implemented;
- human study remains future validation;
- no human effect result exists.

Blocked statements until Paper B data exist:

- improved reviewer accuracy;
- reduced disagreement;
- reduced assessment time;
- validated by independent legal experts;
- human-ground-truth confirmed.

Audit: **PASS**.

## 6. Overclaim search

### Explicitly preserved limitations

- `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED` — present.
- 0/4 C2PA delegation finding limited to the tested mapping — present.
- hash/integrity does not prove lawful acquisition or truth — present.
- trusted signer does not imply legal compliance — present.
- machine-readable preference is not substituted for complete legal basis — present.
- Saudi legal mapping is non-authoritative research abstraction — present.
- no human results — repeated explicitly.
- public repository prevents cryptographic blinding — present.

### Wording to keep out of final title/abstract/results

- “automated compliance” except in a denial/non-goal sentence;
- “proves legality”;
- “ensures lawful training”;
- “independent implementation validation”;
- “expert-validated ground truth”;
- “human performance improvement”.

## 7. Current draft weakness

The novelty position is now supported by comparative copyright and law-by-design literature, but **the manuscript body still lacks full inline citations**. The next Stage-009 action is citation insertion and paragraph-level source mapping, not new feature engineering.

A secondary weakness remains the evidence/auditability literature: Paper A should connect its “evidentiary observability” concept to enforcement/contestability scholarship strongly enough that it does not look like an isolated new label.

## 8. Controller decision

**GO — continue manuscript refinement. HOLD submission.**

Do not resume feature-building merely to make the repository larger. New engineering should be admitted only if manuscript review identifies a specific evidentiary gap that materially threatens Paper A’s claims.
