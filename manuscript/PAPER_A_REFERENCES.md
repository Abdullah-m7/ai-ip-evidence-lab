# Paper A — Verified Bibliography and Source Hierarchy

## Status

**BIBLIOGRAPHY CURATED FOR CONTROLLER REVIEW.**

This file records the sources admitted to the current manuscript, the proposition for which each source may be used, and the authority boundary that must be preserved. The manuscript carries its own formatted reference list; this file is the audit companion.

## A. Primary Saudi legal sources

### Saudi Arabia (2026a) — Copyright Law

- **Source:** *Nizam Huquq al-Mu’allif* [Copyright Law], official Arabic text, *Umm Al-Qura*, 13 February 2026.
- **Relevant provision:** Article 26(4).
- **Permitted proposition:** the provision addresses copying an original work for AI-product and algorithm development subject to lawful publication, lawful acquisition of ownership of the original copy, and purpose-limited copying.
- **Boundary:** do not paraphrase this as a general authorization of every AI-training use.
- **Official location:** https://www.uqn.gov.sa/details?p=28845

### Saudi Arabia (2026b) — Implementing Regulations

- **Source:** Implementing Regulations of the Copyright Law, official Arabic text, *Umm Al-Qura*, 31 July 2026.
- **Relevant provision:** Article 30(1)–(6).
- **Permitted proposition:** Article 30 establishes necessity, commercial-use, retained-record, author-interest, downstream-use, and independently protected-element controls for the Article 26(4) pathway.
- **Core record proposition:** Article 30(3) requires retained records of work type, source, purpose of use, and date of use.
- **Boundary:** the four fields are a minimum retained-record core, not a complete legal-compliance test.
- **Official location:** https://www.uqn.gov.sa/decisions-and-regulations/4001498

### Saudi Arabia (2026c) — Royal Decree No. M/169

- **Source:** Royal Decree No. M/169 dated 14/08/1447H, *Umm Al-Qura*, 13 February 2026.
- **Permitted proposition:** the Decree approved the new Copyright Law.
- **Official location:** https://www.uqn.gov.sa/decisions-and-regulations/4000304

### Legal-source rule

The Arabic official text governs. English wording in Paper A is an analytical paraphrase unless expressly identified otherwise. The IPEL mapping is not an authoritative SAIP or judicial interpretation.

## B. Official comparative and policy sources

1. **European Union (2019).** Directive (EU) 2019/790 on copyright and related rights in the Digital Single Market, especially Articles 3 and 4. *Official Journal of the European Union* L 130:92–125. https://eur-lex.europa.eu/eli/dir/2019/790/oj
2. **Agency for Cultural Affairs (Japan) (2024).** *General Understanding on AI and Copyright in Japan—Overview*. The agency states that the document summarizes a non-binding interpretive view of current Japanese copyright law. https://www.bunka.go.jp/english/policy/copyright/
3. **United States Copyright Office (2025).** *Copyright and Artificial Intelligence, Part 3: Generative AI Training*. https://www.copyright.gov/ai/
4. **United Kingdom Government (2026).** *Report on Copyright and Artificial Intelligence*. Department for Science, Innovation and Technology; Department for Culture, Media and Sport; Intellectual Property Office, 18 March 2026. https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence

**Use boundary:** these sources establish the existence and structure of different legal/policy approaches. They do not establish that the Saudi pathway has the same elements.

## C. Normative and official technical specifications

1. **C2PA (2026).** *C2PA Technical Specification*, version 2.4. https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
   - Supports claims about manifest structure, hard bindings, validation, trust, Ingredient v3, collection data hashes, and AI/ML input relationships.
   - The specification’s own scope cautions against turning provenance validation into a “good/bad” value judgment.
2. **CAWG (2025).** *Training and Data Mining Assertion*, version 1.1, ratified 16 May 2025. https://cawg.io/training-and-data-mining/1.1/
   - Supports claims about `allowed`, `notAllowed`, and `constrained` usage signals for data mining, inference, generative training, and non-generative training.
   - Does not support a claim that such a signal is the complete legal basis for a specific use.
3. **TDM·AI (n.d.).** *TDM·AI Protocol and Documentation*. https://docs.tdmai.org/
   - Supports claims about machine-readable AI/TDM preferences.
   - Public declarations and negotiated licences must not be collapsed into one category.
4. **WIPO (2026).** *AI Infrastructure Interchange (AIII)*. https://www.wipo.int/en/web/ai-infrastructure-interchange
   - Supports infrastructure-level framing only.
   - Do not imply WIPO endorsement of IPEL or of the project’s Saudi-law interpretation.

## D. Dataset documentation and provenance literature

1. **Bender, E. M., & Friedman, B. (2018).** Data statements for natural language processing: Toward mitigating system bias and enabling better science. *Transactions of the Association for Computational Linguistics*, 6, 587–604. https://doi.org/10.1162/tacl_a_00041
2. **Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019).** Model cards for model reporting. In *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 220–229. https://doi.org/10.1145/3287560.3287596
3. **Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé, H. III, & Crawford, K. (2021).** Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92. https://doi.org/10.1145/3458723
4. **Pushkarna, M., Zaldivar, A., & Kjartansson, O. (2022).** Data cards: Purposeful and transparent dataset documentation for responsible AI. In *Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3531146.3533231
5. **Longpre, S., Mahari, R., Chen, A., Obeng-Marnu, N., Sileo, D., Brannon, W., Muennighoff, N., Khazam, N., Kabbara, J., Perisetla, K., Wu, X. A., Shippole, E., Bollacker, K., Wu, T., Villa, L., Pentland, A., & Hooker, S. (2024).** A large-scale audit of dataset licensing and attribution in AI. *Nature Machine Intelligence*, 6, 975–987. https://doi.org/10.1038/s42256-024-00878-8

**Positioning boundary:** these works establish documentation, lineage, and transparency foundations. Paper A must not claim that they are inadequate generally; it argues that jurisdiction-specific legal-evidence mapping is an additional layer.

## E. Reviewability, auditability, and computational-law literature

1. **Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., & Barnes, P. (2020).** Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*, 33–44. https://doi.org/10.1145/3351095.3372873
2. **Cobbe, J., Lee, M. S. A., & Singh, J. (2021).** Reviewable automated decision-making: A framework for accountable algorithmic systems. In *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445921
3. **Di Porto, F. (2023).** Algorithmic disclosure rules. *Artificial Intelligence and Law*, 31, 13–51. https://doi.org/10.1007/s10506-021-09302-7
4. **Guitton, C., Tamò-Larrieux, A., & Mayer, S. (2023).** Mapping the issues of automated legal systems: Why worry about automatically processable regulation? *Artificial Intelligence and Law*, 31, 571–599. https://doi.org/10.1007/s10506-022-09323-w
5. **Francesconi, E., & Governatori, G. (2023).** Patterns for legal compliance checking in a decidable framework of linked open data. *Artificial Intelligence and Law*, 31, 445–464. https://doi.org/10.1007/s10506-022-09317-8
6. **Witt, A., Huggins, A., Governatori, G., et al. (2024).** Encoding legislation: A methodology for enhancing technical validation, legal alignment and interdisciplinarity. *Artificial Intelligence and Law*, 32, 293–324. https://doi.org/10.1007/s10506-023-09350-1

**Positioning boundary:** IPEL adopts reviewability and open-texture cautions. It does not claim that formal legal reasoning or compliance checking is impossible; it limits its own automation to evidence observability and explicit contradictions.

## F. AI-training copyright scholarship

1. **Samuelson, P. (2023).** Generative AI meets copyright. *Science*, 381(6654), 158–161. https://doi.org/10.1126/science.adi0656
2. **Guadamuz, A. (2024).** A scanner darkly: Copyright liability and exceptions in artificial intelligence inputs and outputs. *GRUR International*, 73(2), 111–127. https://doi.org/10.1093/grurint/ikad140
3. **de la Durantaye, K. (2025).** Control and compensation: A comparative analysis of copyright exceptions for training generative AI. *IIC—International Review of Intellectual Property and Competition Law*, 56, 737–770. https://doi.org/10.1007/s40319-025-01569-6
4. **Sag, M., & Yu, P. K. (2025).** The globalization of copyright exceptions for AI training. *Emory Law Journal*, 74, 1163–1227.

**Positioning boundary:** this literature supports the claim that substantive legality differs across jurisdictions and is heavily contested. Paper A’s novelty is not a new universal legality rule.

## G. Project-generated experimental evidence

These materials support only claims about what the project implemented or observed:

1. `docs/LEGAL_REQUIREMENTS_MATRIX.md` — legal-to-evidence research abstraction.
2. `reports/STAGE_003_REPORT.md` and `reports/stage003_semantic_roundtrip.json` — five-case semantic round-trip.
3. `reports/STAGE_004_REPORT.md` and `reports/stage004_conformant_c2pa.json` — real C2PA hard-binding experiment.
4. `reports/STAGE_005_REPORT.md` and `reports/stage005_cross_validator.json` — cross-version/trust-boundary experiment.
5. `reports/STAGE_006_REPORT.md` — future reviewer benchmark; no human results.
6. `reports/STAGE_007_REPORT.md` and freeze manifest — independent-adjudication preparation; no real adjudication.
7. `reports/STAGE_008_REPORT.md` — distribution/intake infrastructure; no human responses.

Project reports are not external legal or technical authorities. They may support only bounded empirical statements about this implementation.

## H. Citation hierarchy

Use sources in this order:

1. official Arabic legal text for Saudi-law propositions;
2. official legislation/policy for comparative jurisdiction descriptions;
3. normative specifications for C2PA/CAWG/TDM technical propositions;
4. peer-reviewed literature for scholarly positioning;
5. committed project reports and machine outputs for IPEL experimental results.

## I. Remaining pre-submission bibliographic work

- Verify every author list and page range against publisher metadata during journal-style conversion.
- Replace raw web locations with the target journal’s preferred reference formatting.
- Add access dates only if required by the journal.
- Create a persistent archival identifier for the reproducibility package.
- Recheck for credible Saudi-specific peer-reviewed analysis published after the law’s entry into force; use only if its quality and proposition are independently verified.
