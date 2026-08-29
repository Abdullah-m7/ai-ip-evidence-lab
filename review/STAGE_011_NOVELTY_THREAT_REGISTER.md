# Stage 011 — Novelty Threat Register

## Scoring
- **HIGH:** a reasonable reviewer could say the claim is substantially anticipated.
- **MEDIUM:** adjacent work narrows wording or requires explicit differentiation.
- **LOW:** background overlap only.

| ID | Candidate Paper A claim | Threat | Evidence from prior work | Controller action |
|---|---|---|---|---|
| N1 | “There is a missing evidence layer for AI governance/copyright.” | **HIGH** | Li 2026 minimum reviewable trace; Lucchi 2026 auditability gap; applied “evidence layer/evidentiary infrastructure” systems | **Remove as standalone novelty claim.** Reframe as an integration problem in a specific copyright pathway. |
| N2 | “Auditability/reviewability should be designed into AI systems.” | **HIGH** | Cobbe 2021; Raji 2020; Li 2026; broader auditability literature | Treat as intellectual foundation, not contribution. |
| N3 | “Training-data transparency alone is insufficient.” | **HIGH** | Buick 2025 states this directly | Cite and build on it; do not present as new finding. |
| N4 | “C2PA can be used for AI-training copyright/provenance management.” | **HIGH** | Park 2025; C2PA 2.4; CAWG 1.1 | Explicitly disclaim priority. Contribution is semantic boundary testing, not C2PA adoption. |
| N5 | “Training-data provenance can be verified/audited.” | **HIGH** | TrainProVe 2025; Qi et al. 2026; other model-side audit work | Distinguish evidence **of ingestion** from evidence **about the legal/operational basis of ingestion**. |
| N6 | “Copyright litigation may require cryptographic provenance records.” | **HIGH** | Krishna et al. 2026 PRPP | Cite; distinguish development-time record capture from litigation disclosure procedure. |
| N7 | “Translate legal/accountability rules into reviewable evidence duties.” | **HIGH** | Li 2026 directly does this in Australian public law | Narrow novelty to statutory copyright use-event decomposition + executable cross-standard tests. |
| N8 | “Jurisdiction-specific legal-to-evidence decomposition of Saudi Art. 26(4) + Reg. 30.” | **MEDIUM-LOW** | Saudi doctrinal works exist, but no close executable evidence architecture found | Retain; verify exhaustive legal concordance and avoid ‘first ever’ unless defensible. |
| N9 | “Article 30(3) four-field statutory record core can be operationalized as an evidence contract.” | **LOW** | No close implementation located | Retain as a central concrete contribution. |
| N10 | “C2PA/CAWG semantics must not overwrite separate jurisdiction-specific legal facts.” | **LOW-MEDIUM** | Standards distinguish scope; prior papers discuss limits, but no close executable false-equivalence experiment located | **Elevate to core empirical novelty.** |
| N11 | “Real C2PA hard binding can be combined with a copyright evidence gate and adversarial corruption tests.” | **MEDIUM** | C2PA integrity tests exist; Park uses C2PA conceptually | Retain as integration/validation contribution, not cryptographic novelty. |
| N12 | “0/4 Article 30(3) fields were safely delegated.” | **LOW** as project result | No one can anticipate this exact tested mapping | Retain only as bounded result, explicitly not impossibility theorem. |
| N13 | “IPEL improves legal review.” | **BLOCKED** | No human data | Do not claim before Paper B. |
| N14 | “IPEL is broadly generalizable across jurisdictions.” | **MEDIUM-HIGH** | Different copyright rules and privacy/retention tensions undermine field portability | Generalize the **method**, not field semantics. Add privacy/retention conflict discussion. |
| N15 | “Evidentiary observability” as a new concept/term. | **MEDIUM-HIGH** | Auditability, reviewable trace, evidentiary infrastructure are active adjacent terms | Use as project vocabulary only; do not claim conceptual priority without a terminology review. |

## Core novelty after threat reduction

The contribution that survives the threat register is:

> **A jurisdiction-specific, use-event-level evidence profile derived from an enacted AI-development copyright exception and record-retention regulation, coupled to executable tests that distinguish and stress-test legal evidence against cryptographic provenance, trust classification, and machine-readable rights signals.**

### Four irreducible contribution elements

Paper A should be organized around these, not around generic provenance/auditability language:

1. **Statutory decomposition:** enacted Saudi Article 26(4) + Regulation Article 30 → observable/evidentiary/judgment-sensitive requirements.
2. **Executable evidence contract:** use-event schema + fail-closed evidence gate that explicitly returns `legal_conclusion=false`.
3. **Semantic barrier experiment:** C2PA/CAWG valid/trusted/allowed signals cannot overwrite acquisition, permission, publication, or other jurisdiction-specific legal-evidence facts.
4. **Integrity validation:** real C2PA hard-binding corruption experiments + cross-version validation, with implementation-diversity limitation preserved.

If any one of these four disappears from the manuscript, novelty becomes materially weaker.

## Title implication

Current title is defensible but still broad:

> From Copyright Exception to Verifiable Evidence: An Evidence Architecture for AI Development under Saudi Arabia’s 2026 Copyright Law

A more novelty-specific candidate for later consideration is:

> **From Statutory Conditions to Verifiable Evidence: Executable Copyright-Provenance Boundaries for AI Development under Saudi Arabia’s 2026 Copyright Law**

Do not change the title yet; test it during the manuscript quality review.