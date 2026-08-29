# Paper A — Bibliography Seed and Source Audit

This is a working source list, grouped by evidentiary authority. It is not yet formatted to the final journal style.

## A. Primary Saudi legal sources

1. **Saudi Arabia, Copyright Law (2026)**, Umm Al-Qura Official Gazette, including Article 26(4). 13 February 2026. https://www.uqn.gov.sa/details?p=28845
2. **Royal Decree No. M/169**, 14/08/1447H, approving the Copyright Law. https://www.uqn.gov.sa/decisions-and-regulations/4000304
3. **Implementing Regulations of the Copyright Law (2026)**, especially Article 30, dated 31 July 2026. https://www.uqn.gov.sa/decisions-and-regulations/4001498

### Legal-source handling rule

The Arabic official text governs. Any English rendering in Paper A is an author translation/paraphrase for analytical purposes and must be labeled as such where wording matters.

## B. Normative / official technical specifications

4. **C2PA Specifications 2.4**, Coalition for Content Provenance and Authenticity. https://spec.c2pa.org/specifications/
5. **C2PA Technical Specification 2.4 — Ingredient v3 and hashed references**. https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
6. **C2PA Guidance for Artificial Intelligence and Machine Learning**. https://spec.c2pa.org/specifications/
7. **Creator Assertions Working Group (CAWG), Training and Data Mining Assertion 1.1**, ratified 16 May 2025. https://cawg.io/training-and-data-mining/1.1/
8. **TDM·AI Protocol**, machine-readable AI/TDM usage preferences. https://docs.tdmai.org/
9. **TDM·AI, Opt-out, Opt-in and Content Licensing**, distinguishing public preference declarations from negotiated licences. https://docs.tdmai.org/opt-out-opt-in-and-content-licensing
10. **WIPO, AI Infrastructure Interchange (AIII)**. https://www.wipo.int/en/web/ai-infrastructure-interchange
11. **WIPO, AIII FAQs**. https://www.wipo.int/en/web/ai-infrastructure-interchange/faqs

## C. Peer-reviewed / scholarly related work

12. Longpre, S., Mahari, R., Chen, A., et al. (2024). **A large-scale audit of dataset licensing and attribution in AI.** *Nature Machine Intelligence*, 6, 975–987. https://www.nature.com/articles/s42256-024-00878-8
13. Guitton, C., Tamò-Larrieux, A., & Mayer, S. (2023). **Mapping the Issues of Automated Legal Systems: Why Worry About Automatically Processable Regulation?** *Artificial Intelligence and Law*, 31, 571–599. https://link.springer.com/article/10.1007/s10506-022-09323-w
14. Guitton, C., Gubelmann, R., Karray, G., Mayer, S., et al. (2025). **Identifying open-texture in regulations using LLMs.** *Artificial Intelligence and Law*. https://link.springer.com/article/10.1007/s10506-025-09450-0
15. Bench-Capon, T. (2022). **Thirty years of Artificial Intelligence and Law: Editor’s Introduction.** *Artificial Intelligence and Law*, 30, 475–479. https://link.springer.com/article/10.1007/s10506-022-09325-8
16. Di Porto, F. (2023). **Algorithmic disclosure rules.** *Artificial Intelligence and Law*, 31, 13–51. https://link.springer.com/article/10.1007/s10506-021-09302-7
17. Bex, F. J. (2025). **AI, Law and beyond. A transdisciplinary ecosystem for the future of AI & Law.** *Artificial Intelligence and Law*, 33, 253–270. https://link.springer.com/article/10.1007/s10506-024-09404-y

## D. Project-generated experimental evidence

These are not external authorities. They support only claims about what this project implemented or observed.

18. `docs/LEGAL_REQUIREMENTS_MATRIX.md` — Saudi legal-to-evidence abstraction.
19. `reports/STAGE_003_REPORT.md` and `reports/stage003_semantic_roundtrip.json` — semantic interoperability experiment.
20. `reports/STAGE_004_REPORT.md` and `reports/stage004_conformant_c2pa.json` — real C2PA hard-binding experiment.
21. `reports/STAGE_005_REPORT.md` and `reports/stage005_cross_validator.json` — cross-validator/cross-version and trust-boundary experiment.
22. `reports/STAGE_006_REPORT.md` — blinded benchmark construction; **no human results**.
23. `reports/STAGE_007_REPORT.md` and freeze manifest — independent-adjudication preparation; **no human adjudication collected**.
24. `reports/STAGE_008_REPORT.md` — contamination-resistant distribution/intake infrastructure; **no human responses collected**.

## E. Citation-source hierarchy for manuscript drafting

Use sources in this order where possible:

1. official Saudi legal text for Saudi legal claims;
2. normative standard/specification for C2PA/CAWG/TDM technical claims;
3. peer-reviewed paper for literature claims;
4. project reports/code/tests only for claims about IPEL experiments.

Do not use the project README as authority for a legal or external-standard proposition when a primary source exists.

## F. Literature gaps still to fill before submission

- comparative AI-training copyright scholarship from the EU, US, UK, Japan, and other jurisdictions, used to show that the *substantive legality* question is heavily studied;
- scholarship on legal evidence/provenance and auditability that is not AI-specific;
- work on data lineage, datasheets/model cards, and responsible dataset documentation beyond DPI;
- any Saudi-specific peer-reviewed analysis of the 2026 Copyright Law published after entry into force;
- literature on compliance-by-design / regulatory technology that distinguishes rule execution from evidence preservation.

These gaps should be filled before the manuscript is marked submission-ready.
