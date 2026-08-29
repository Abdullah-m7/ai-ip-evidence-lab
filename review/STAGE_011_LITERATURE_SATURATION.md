# Stage 011 — Literature Saturation Review

## Controller status

**LITERATURE SATURATION: SUBSTANTIALLY COMPLETE FOR NOVELTY REVIEW — NOVELTY NARROWED, NOT INVALIDATED**

This review asks a stricter question than “are there papers on AI and copyright?” It asks whether the specific Paper A contribution has already been anticipated: a jurisdiction-specific legal-to-evidence decomposition for AI-development use events, with an executable evidence contract, provenance interoperability, and adversarial tests that prevent provenance/trust/rights signals from silently becoming legal conclusions.

Search emphasis: peer-reviewed and official sources first; 2025–2026 near-overlap work was deliberately prioritized. Grey literature is included only where it poses a practical prior-art or terminology risk.

## 1. Main conclusion

The broad idea that AI systems need **audit trails, provenance, reviewable records, or evidentiary infrastructure is no longer novel**. Multiple 2025–2026 works now use closely related language and problem framings.

Paper A therefore must **not** claim novelty in any of the following broad propositions:

- AI governance needs reviewable records;
- copyright enforcement needs training-data transparency;
- provenance can support rights management;
- C2PA can support copyright / AI-training metadata;
- auditability is distinct from correctness;
- legal rules can be translated into evidence duties.

The still-defensible contribution is narrower:

> **IPEL operationalizes a specific statutory AI-development copyright pathway into a use-event-level evidence contract, then empirically tests the semantic boundary between jurisdiction-specific legal evidence and C2PA/CAWG provenance/trust/rights signals.**

The strongest novelty is therefore the **combination of legal decomposition + executable contract + false-equivalence testing + real C2PA adversarial validation**, not the phrase “evidence layer” or “auditability”.

## 2. Literature clusters reviewed

### A. Substantive AI-training copyright doctrine and transparency

1. **Buick, Adam (2025), “Copyright and AI training data—transparency to the rescue?”, Journal of Intellectual Property Law & Practice 20(3):182–192. DOI 10.1093/jiplp/jpae102.**
   - Contribution: transparency is necessary but insufficient; the value of disclosure depends on the underlying copyright regime.
   - Relevance: directly supports Paper A’s distinction between transparency and legal sufficiency.
   - Novelty threat: **MEDIUM**. It anticipates the “transparency ≠ legal answer” argument, but does not build an executable evidence architecture.

2. **de la Durantaye, Katharina (2025), “Control and Compensation: A Comparative Analysis of Copyright Exceptions for Training Generative AI”, IIC 56:737–770. DOI 10.1007/s40319-025-01569-6.**
   - Contribution: comparative mapping of AI-training exceptions.
   - Relevance: shows jurisdictional divergence and therefore why a jurisdiction-specific evidence profile is plausible.
   - Novelty threat: **LOW** to implementation; **HIGH** if Paper A drifts into general comparative doctrine.

3. **Samuelson, Pamela (2026), “Assessing the feasibility of collective licensing of in-copyright works as training data for generative AI systems”, PNAS 123(30), e2509769122. DOI 10.1073/pnas.2509769122.**
   - Contribution: institutional feasibility of licensing at scale.
   - Relevance: licensing infrastructure is an alternative/adjacent solution to evidence preservation.
   - Novelty threat: **LOW**.

4. **“Training on the tightrope: AI copyright and data privacy as colliding regulatory regimes”, Computer Law & Security Review 61 (2026), 106343. DOI 10.1016/j.clsr.2026.106343.**
   - Contribution: maps conflicts between copyright and privacy during AI training, including retention and consent/licence tensions.
   - Relevance: important because evidence-retention duties can conflict with data-minimization/privacy duties.
   - Novelty threat: **MEDIUM** to Paper A’s generalization claims; adds a missing limitations discussion.

5. **Guadamuz, Andrés (2024), “A Scanner Darkly: Copyright Liability and Exceptions in Artificial Intelligence Inputs and Outputs”, GRUR International 73(2):111–127. DOI 10.1093/grurint/ikad140.**
   - Contribution: doctrinal treatment of AI input/output copyright.
   - Novelty threat: **LOW**.

6. **Sag, Matthew & Peter K. Yu (2025), “The Globalization of Copyright Exceptions for AI Training”, Emory Law Journal 74.**
   - Contribution: comparative/global diffusion of training exceptions.
   - Novelty threat: **LOW** to IPEL architecture; **HIGH** if manuscript overclaims comparative novelty.

7. **United States Copyright Office (2025), Copyright and Artificial Intelligence, Part 3: Generative AI Training.**
   - Official policy source on training and licensing.
   - Novelty threat: **LOW**, but mandatory background.

8. **EUIPO Copyright Knowledge Centre / European Commission (2025–2026) materials on machine-readable TDM reservations and GPAI copyright compliance.**
   - Contribution: operational rights-reservation infrastructure is rapidly maturing.
   - Novelty threat: **MEDIUM** to any claim that machine-readable rights signaling is underdeveloped.

### B. Dataset documentation, provenance and training-data transparency

9. **Longpre et al. (2024), “A large-scale audit of dataset licensing and attribution in AI”, Nature Machine Intelligence 6:975–987. DOI 10.1038/s42256-024-00878-8.**
   - Contribution: large-scale dataset lineage/licensing audit.
   - Novelty threat: **MEDIUM**. It occupies the provenance/documentation layer but not the legal-evidence mapping layer.

10. **Bender & Friedman (2018), Data Statements for NLP, TACL 6:587–604. DOI 10.1162/tacl_a_00041.**
11. **Gebru et al. (2021), Datasheets for Datasets, CACM 64(12):86–92. DOI 10.1145/3458723.**
12. **Pushkarna et al. (2022), Data Cards, FAccT. DOI 10.1145/3531146.3533231.**
   - Contribution: documentation as a governance mechanism.
   - Novelty threat: **LOW individually; MEDIUM collectively**. Paper A must explain why a legal-evidence contract is more than another card/template.

13. **Buick (2025), especially discussion of item-level identification, data sources, and the limits of dataset summaries.**
   - Novelty threat: **MEDIUM-HIGH** to any claim that source/work-level traceability itself is novel.

14. **CASRAI (2026), AI Training Data Provenance, Copyright, and TDM Exceptions for Research.**
   - Grey/operational guidance: explicitly separates “is mining lawful?” from “can anyone tell what was used?”
   - Novelty threat: **MEDIUM** as terminology/practical prior art, but not a peer-reviewed executable architecture.

### C. Technical detection of unauthorized training use

15. **Xie et al. (CVPR 2025), “Training Data Provenance Verification: Did Your Model Use Synthetic Data from My Generative Model for Training?” DOI 10.1109/CVPR52734.2025.02218.**
   - Contribution: >99% reported verification accuracy for detecting provenance of suspicious model training data in tested settings.
   - Relationship: post-hoc model-side detection, not contemporaneous legal evidence capture.
   - Novelty threat: **LOW-MEDIUM**. Paper A must distinguish “prove data was used” from “preserve the legal facts governing that use.”

16. **Qi et al. (2026), “Auditing unauthorized training data from AI generated content using information isotopes”, Nature Communications 17:3007.**
   - Contribution: black-box detection/auditing of training-data use.
   - Novelty threat: **MEDIUM** to any broad “post-hoc evidence of use” claim; **LOW** to the statutory evidence-contract contribution.

17. **Li et al. (2026), distribution-level auditability of upstream training data in distilled diffusion models (arXiv / related preprint).**
   - Contribution: model-side detection after distillation.
   - Novelty threat: **LOW-MEDIUM**.

### D. C2PA, rights metadata and AI-training copyright management

18. **C2PA Technical Specification 2.4 (2026) and AI/ML guidance.**
   - Contribution: mature content provenance, bindings, Ingredients, collections, validation/trust semantics.
   - Novelty threat: **HIGH** to any claim that IPEL invents provenance or integrity infrastructure.
   - Paper A’s strongest response remains: reuse C2PA where semantics match; do not equate it with jurisdiction-specific legal facts.

19. **CAWG Training and Data Mining Assertion 1.1 (2025).**
   - Contribution: machine-readable `allowed / notAllowed / constrained` signals across mining/training/inference uses.
   - Novelty threat: **HIGH** to any rights-signaling novelty claim; **LOW** to evidence reconstruction.

20. **Park, Yusun (2025), “Study on Copyright Management of AI Training Data Using NFTs and C2PA”, Journal of Industrial Property, no. 80, 331–368. DOI 10.36669/ip.2025.80.8.**
   - Contribution: proposes NFT/blockchain + C2PA metadata for provenance, usage history, licensing and copyright management of AI training data.
   - Novelty threat: **HIGH**. This is the closest published copyright/C2PA work found.
   - Difference that must be explicit: Paper A does not propose C2PA as a general copyright-management ledger; it tests which statutory facts **cannot** safely be substituted by C2PA semantics and empirically attacks false equivalence.

21. **C2PA specifications issue/discussion on extending provenance to AI training-data attribution (2026).**
   - Grey prior art showing the training-boundary problem is recognized by implementers.
   - Novelty threat: **MEDIUM**.

### E. Reviewability, evidence architecture, and auditability

22. **Cobbe, Lee & Singh (2021), “Reviewable automated decision-making”, FAccT. DOI 10.1145/3442188.3445921.**
   - Contribution: reviewability as socio-technical recordkeeping/accountability.
   - Novelty threat: **MEDIUM** to broad reviewability framing.

23. **Raji et al. (2020), “Closing the AI Accountability Gap”, FAccT. DOI 10.1145/3351095.3372873.**
   - Contribution: lifecycle audit artifacts and accountability.
   - Novelty threat: **LOW-MEDIUM**.

24. **Grace Li (2026), “Auditable accountability without an AI act: Australia’s public-sector AI assurance stack and the minimum reviewable trace”, Law, Ethics & Technology, DOI 10.55092/let20260010.**
   - Contribution: translates abstract public-law obligations into evidence disciplines and a bounded **minimum reviewable trace** for AI-influenced public decisions.
   - Novelty threat: **HIGH — conceptual**.
   - This paper materially anticipates the idea that legal/accountability duties should be translated into reviewable evidence artifacts.
   - Distinction: administrative/public-sector decisions, not copyright training-use events; doctrinal/functional method rather than an executable cross-standard semantic/adversarial experiment.

25. **Nicola Lucchi (2026), “The Invisible Author: Generative AI and the Auditability Gap”, SSRN. DOI 10.2139/ssrn.7024098.**
   - Contribution: reframes AI-assisted copyright authorship as an auditability problem and distinguishes output-, interaction-, and model-side evidence.
   - Novelty threat: **HIGH — copyright/auditability terminology**.
   - Distinction: authorship/human creative contribution, not input-side training legality; no Saudi statutory record-retention testbed or executable provenance/legal-fact barrier.

26. **Krishna, Shaini Shree & Raguram (2026), “Training Data Disclosure in AI Copyright Litigation: The Post-Report Provenance Procedure”, SSRN. DOI 10.2139/ssrn.6570339.**
   - Contribution: UK civil-procedure framework compelling provenance evidence such as cryptographic hash manifests where ingestion is plausibly alleged.
   - Novelty threat: **HIGH — copyright/provenance/evidence**.
   - Distinction: litigation disclosure procedure and proof of ingestion; does not specify a development-time evidence contract for a statutory exception or experimentally distinguish C2PA/rights/trust semantics from legal facts.

27. **Alhalangy (2026), “Operationalizing Accountable AI Through Traceable Governance Architecture for Institutional Decision Support”, Information 17(7):694. DOI 10.3390/info17070694.**
   - Contribution: traceable governance architecture for institutional AI decisions.
   - Novelty threat: **MEDIUM** to generic architecture claims.

28. **Lucchi/Li/other 2026 auditability literature collectively.**
   - Finding: “auditability”, “evidence layer”, “reviewable trace”, and “evidentiary infrastructure” are now active terms of art/near-art.
   - Consequence: Paper A should not brand the contribution primarily through a new noun phrase. The novelty must be demonstrated by mechanism and experiment.

### F. Computational law and rule-to-evidence boundaries

29. **Guitton, Tamò-Larrieux & Mayer (2023), AI & Law 31:571–599. DOI 10.1007/s10506-022-09323-w.**
30. **Francesconi & Governatori (2023), AI & Law 31:445–464. DOI 10.1007/s10506-022-09317-8.**
31. **Witt et al. (2024), AI & Law 32:293–324. DOI 10.1007/s10506-023-09350-1.**
   - Contribution: formalization, compliance checking, encoding legislation, open-texture/legal alignment.
   - Novelty threat: **MEDIUM**. Paper A must frame IPEL as an evidence architecture around a rule, not as a novel theory of computational legal formalization.

### G. Saudi-specific literature

32. **Al-Anzi & Al-Maamari (2026), “Legal Analysis of Saudi Arabia’s New Copyright Law under Royal Decree No. M/169”, Trends in Intellectual Property Research 4(4), DOI 10.69971/tipr.4.4.2026.140.**
   - Contribution: broad doctrinal overview of the new law, including the AI exception.
   - Quality note: useful for prior-art awareness, but Paper A should continue to rely on the official Arabic text rather than this paper for propositions of law.
   - Novelty threat: **LOW** to architecture; **HIGH** to any claim of being the first analysis of the new Saudi law.

33. **Albakjaji & Almarzouqi (2024), “The Dilemma of the Copyrights of Artificial Intelligence: The Case of Saudi Arabia Regulations”, IJSKD 16(1), DOI 10.4018/IJSKD.336920.**
   - Contribution: earlier Saudi AI/copyright doctrinal analysis.
   - Novelty threat: **LOW** to Paper A architecture; confirms that generic “Saudi AI + copyright” novelty is unavailable.

34. **Saudi practitioner analyses (Baker McKenzie 2026; Gowling WLG 2026).**
   - Contribution: current implementation/practical commentary on the new law/regulations.
   - Use: secondary validation and issue spotting only; not authority over official text.
   - Novelty threat: **LOW**.

## 3. Saturation assessment by candidate claim

| Candidate claim | After review | Status |
|---|---|---|
| “AI copyright needs an evidence layer” | anticipated by multiple works | **DROP as novelty claim** |
| “AI governance needs reviewable traces” | directly anticipated by Li/Cobbe/Raji | **DROP as novelty claim** |
| “Training-data transparency is insufficient” | directly anticipated by Buick and others | **DROP as novelty claim** |
| “C2PA can support copyright/training provenance” | directly anticipated by Park + C2PA | **DROP as novelty claim** |
| Jurisdiction-specific legal-to-evidence decomposition of Saudi Art. 26(4)/Reg. 30 | no close executable match found | **RETAIN — MEDIUM/HIGH novelty** |
| Article 30(3) statutory record core used as an executable testbed | no close match found | **RETAIN — HIGH local novelty** |
| Use-event evidence contract separating structural facts / evidence-supported assertions / judgment-sensitive conditions | adjacent work exists, exact implementation not found | **RETAIN — MEDIUM novelty** |
| Empirical semantic test that C2PA/CAWG signals do not overwrite jurisdiction-specific legal facts | no close published match found | **RETAIN — HIGH novelty** |
| Real C2PA hard-binding corruption experiment embedded in a legal-evidence study | C2PA attack literature exists, copyright/legal integration appears uncommon | **RETAIN — MEDIUM/HIGH novelty** |
| 0/4 Article 30(3) fields delegated in tested mapping | project-specific empirical result | **RETAIN — result, not broad novelty theorem** |
| Human-review benefit | untested | **BLOCK until Paper B** |

## 4. Most important manuscript changes implied by the literature

1. **Replace “missing evidence layer” language with “a missing integration/operationalization problem” unless carefully qualified.** Evidence-layer terminology already exists in 2026 literature and applied systems.
2. **Add Li (2026) minimum reviewable trace** and explicitly state that Paper A applies a related reviewability logic to a different legal object and adds executable semantic/adversarial validation.
3. **Add Lucchi (2026) auditability gap** to show copyright auditability is already recognized, while distinguishing authorship-side from training-input-side evidence.
4. **Add Park (2025) C2PA/NFT copyright management** as the closest direct technical/legal prior work. Failure to cite it would be a significant literature omission.
5. **Add Krishna et al. (2026) PRPP** as close copyright/provenance procedural work, while distinguishing litigation disclosure from development-time evidence capture.
6. **Add TrainProVe / information-isotope work** to separate model-side detection of use from contemporaneous records of the legal basis and operational facts of use.
7. **Discuss copyright/privacy retention tension** using the 2026 CLSR work; a system that preserves evidence may create retention/minimization conflicts.
8. **Narrow the title/abstract contribution statement** away from “introduces the evidence layer” toward “implements and tests a jurisdiction-specific evidence profile and semantic barrier.”

## 5. Literature-review verdict

**Novelty survives, but only after narrowing.**

The literature does not support a broad first-of-kind claim for evidence, auditability, provenance, reviewable traces, or C2PA-based copyright management. It does support a more defensible contribution:

> A concrete statutory record-retention obligation is transformed into a machine-readable use-event evidence contract, and that contract is experimentally tested against mature provenance/rights infrastructure to show where semantic substitution is and is not safe.

This is a stronger, more falsifiable claim than “there is a missing evidence layer,” and it should become the organizing contribution of the revised manuscript.
