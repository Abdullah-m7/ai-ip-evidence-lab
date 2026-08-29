# From Copyright Exception to Verifiable Evidence: An Evidence Architecture for AI Development under Saudi Arabia’s 2026 Copyright Law

## Abstract

Copyright scholarship on artificial-intelligence development has largely focused on substantive permission: whether protected works may be copied for model development, which exceptions apply, and when licences or rightsholder reservations control. A separate problem arises after a legally relevant use has occurred: can a developer, regulator, court, or rights holder reconstruct the facts on which the asserted legal pathway depended? Saudi Arabia’s 2026 Copyright Law provides a concrete testbed. Article 26(4) permits copying an original work for the development of AI products and algorithms subject to fact-sensitive conditions, while Article 30 of the Implementing Regulations adds operational restrictions and expressly requires developers to retain records of the work type, source, purpose of use, and date of use. This paper introduces IPEL, a jurisdiction-specific intellectual-property evidence layer designed to preserve such facts without turning technical provenance into an automated legal conclusion. We map the Saudi provisions into an evidence contract, distinguish observable facts from open-textured legal assessments, and test interoperability with machine-readable usage preferences and C2PA content provenance. In a five-case semantic round-trip experiment, the tested profile preserved all leaf values and evidence-gate outcomes, while none of the four Article 30(3) core fields was delegated to C2PA as a semantically equivalent substitute. A real C2PA hard-binding experiment detected tested asset, assertion, and claim-signature corruptions and showed that cryptographic validity and signer trust are distinct. A cross-validator experiment reproduced the three tested corruption categories across two validation surfaces using different observed c2pa-rs versions, while explicitly not establishing implementation diversity. Across the experiments, CAWG training-use signals and C2PA trust states were prevented from overwriting jurisdiction-specific evidence such as acquisition status or output permission. The contribution is not automated copyright compliance, but an evidentiary architecture and a falsifiable method for separating content provenance, usage signaling, legal-evidence observability, and human legal judgment.

**Keywords:** AI training; copyright; provenance; legal evidence; C2PA; computational law; Saudi Arabia; intellectual property; auditability; reviewability

---

## 1. Introduction

The use of copyrighted works in artificial-intelligence development has generated an increasingly international debate about reproduction, fair use, text-and-data-mining exceptions, licences, rights reservations, transparency, and compensation (Samuelson 2023; Guadamuz 2024; de la Durantaye 2025; Sag and Yu 2025). The legal answers vary substantially. The United States has developed the question largely through fair-use doctrine and litigation, the European Union has enacted text-and-data-mining exceptions subject to conditions and reservations, Japan applies a comparatively broad non-enjoyment-oriented limitation, and the United Kingdom has continued to evaluate competing reform options (European Union 2019; Agency for Cultural Affairs 2024; United States Copyright Office 2025; United Kingdom Government 2026). This paper does not attempt to resolve that substantive debate across jurisdictions.

A different systems problem appears when any legal pathway depends on facts that must be reconstructed later. A rule may ask whether a work was lawfully published or acquired, why it was copied, when it was used, how much was needed, whether downstream distribution occurred, whether a permission applied, or whether a use prejudiced normal exploitation. Even when the governing rule is known, a later reviewer cannot apply it reliably if the development pipeline did not preserve the relevant facts and their supporting evidence.

Existing technical work addresses important parts of this problem. Dataset-documentation frameworks encourage disclosure of data composition, provenance, intended uses, limitations, and collection practices (Bender and Friedman 2018; Mitchell et al. 2019; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). Large-scale provenance audits reveal serious omissions and inconsistencies in dataset licensing and attribution (Longpre et al. 2024). Machine-readable rights protocols communicate preferences about training or data mining (CAWG 2025; TDM·AI n.d.). C2PA binds assertions to digital assets and supplies a trust and validation architecture for content provenance (C2PA 2026). These mechanisms are valuable, but they answer different questions.

This paper calls the remaining problem **evidentiary observability**: the ability to reconstruct, test, and contest legally relevant facts about an AI-development use event after the event has occurred. The concept is related to reviewability, which treats accountability as a socio-technical record-keeping problem extending beyond model explanation (Cobbe, Lee, and Singh 2021), and to internal algorithmic-audit frameworks that preserve organizational decisions across a system lifecycle (Raji et al. 2020). Evidentiary observability is narrower in object but more explicit in legal mapping: it asks which facts and evidence a particular legal pathway requires, what a technical system can preserve, and where the system must defer to human legal judgment.

Saudi Arabia’s new Copyright Law makes this distinction unusually concrete. Royal Decree No. M/169 approved the Copyright Law in February 2026 (Saudi Arabia 2026c). Article 26(4) permits copying an original work for the development of AI products and algorithms when the work was lawfully published, ownership of the original copy was lawfully obtained, and copying remains within what serves the purpose (Saudi Arabia 2026a, art. 26(4)). Article 30 of the Implementing Regulations adds six groups of controls, including an express duty to retain records showing the type of work, its source, the purpose of use, and the date of use (Saudi Arabia 2026b, art. 30).

The combination is computationally significant. Some requirements are record-like: a source or date can be required structurally. Others are evidence-dependent: a statement that acquisition was lawful may need a receipt, licence, archive record, or other basis. Still others are open-textured: whether a commercial use affects normal exploitation or causes unjustified prejudice cannot safely be reduced to a Boolean supplied by the developer. Research on automatically processable regulation and encoded legislation similarly warns that technical validation does not eliminate legal interpretation, ambiguity, or factual indeterminacy (Guitton, Tamò-Larrieux, and Mayer 2023; Francesconi and Governatori 2023; Witt et al. 2024).

We introduce **IPEL (Intellectual-Property Evidence Ledger)** as a research architecture for this boundary. IPEL is not a copyright oracle and does not predict court outcomes. It models an identifiable AI-development **use event** and preserves jurisdiction-specific facts and evidence references that a later reviewer may need. Its deterministic evidence gate distinguishes structural absence and explicit contradiction from evidentiary uncertainty, while preserving a review-required state for conditions that cannot responsibly be automated.

The paper makes four contributions.

First, it presents a legal-to-evidence decomposition method using Saudi Arabia’s 2026 AI-development copying rule as a testbed. The method separates factual observability, evidentiary support, and normative judgment, and treats the Article 30(3) four-field tuple as a minimum retention core rather than a complete compliance record.

Second, it tests whether mature provenance infrastructure can substitute for the jurisdiction-specific evidence layer. A semantic round-trip experiment shows that generic provenance and the Saudi evidentiary tuple overlap less than a superficial comparison of field names might suggest.

Third, it reports real C2PA hard-binding and adversarial validation experiments. These show the value of cryptographic provenance while exposing boundaries among asset integrity, claim validity, signer trust, metadata semantics, usage preferences, and legal evidence.

Fourth, it defines a falsifiable future human-validation path. A balanced reviewer benchmark, independent-adjudication protocol, preregistration lock, and contamination-resistant distribution/intake pipeline have been implemented, but **no human-effect result is claimed in this paper**.

The central claim is deliberately bounded: a legal-evidence layer can complement provenance and rights-signaling standards by preserving jurisdiction-specific review facts and preventing technical trust signals from silently becoming legal conclusions.

---

## 2. Legal testbed: Saudi Arabia’s 2026 Copyright Law

### 2.1 Source hierarchy and interpretive status

The legal analysis begins with the official Arabic text published by *Umm Al-Qura*. The Copyright Law was approved under Royal Decree No. M/169 and published on 13 February 2026 (Saudi Arabia 2026a; Saudi Arabia 2026c). The Implementing Regulations were published separately and contain a dedicated chapter on computer programs and AI uses (Saudi Arabia 2026b). English descriptions in this paper are analytical paraphrases; the Arabic text governs.

The legal-to-evidence mapping is a research abstraction. It is not an interpretation issued by the Saudi Authority for Intellectual Property, a judicial ruling, or legal advice. The objective is to identify evidentiary propositions that a technical process can preserve, not to pre-empt the legal authority responsible for applying the provisions.

### 2.2 Article 26(4): a fact-conditioned use pathway

Article 26 permits specified uses without the author’s permission and without compensation. Paragraph 4 addresses copying an original work for the purpose of developing AI products and algorithms. It conditions that pathway on lawful publication of the work, lawful acquisition of ownership of the original copy, and copying limited to what serves the purpose (Saudi Arabia 2026a, art. 26(4)).

For an evidence architecture, the provision creates at least three classes of question:

1. **Publication status.** Was the work published in the legally relevant manner, and what evidence supports that proposition?
2. **Acquisition status.** How did the developer obtain the original copy, and what evidence establishes the asserted acquisition pathway?
3. **Purpose and scope.** Why was the work copied, what portion or extent was used, and what basis supports necessity or proportionality?

A content digest may identify bytes, but it cannot by itself establish lawful publication, lawful acquisition, or purpose limitation. Those are propositions about the legal and operational history of the copy, not only its content identity.

### 2.3 Implementing Regulation Article 30

Article 30 applies when an original work is copied for AI product or algorithm development under Article 26(4). It contains six groups of controls (Saudi Arabia 2026b, art. 30):

- copying and analysis must remain limited to what is necessary for AI development and must not extend to republication, distribution, or direct commercial exploitation under the exception;
- purely commercial use is restricted unless the use is non-material in relation to the work or does not affect normal exploitation;
- the developer must retain records of work type, source, purpose of use, and date of use and provide them to a competent authority considering a related dispute upon request;
- the use must not cause unjustified harm to the author’s legitimate interests or opportunity to exploit the work or obtain a material return;
- transformation, republication, public availability, or unnecessary inclusion in a final product is prohibited absent permission or public-domain status; and
- independently protected elements within the work must be respected.

The project maps these provisions into three machine-handling classes:

| Class | Machine role | Example | Boundary |
|---|---|---|---|
| Structural fact | require or validate a field | use date; work source | presence is not truth |
| Evidence-supported assertion | require a value plus an evidence basis | acquisition status; publication status | external evidence may still be contestable |
| Judgment-sensitive condition | preserve inputs and defer | necessity; normal exploitation; unjustified prejudice | no developer self-attestation may become a final legal conclusion |

This decomposition differs from compiling the law into a binary legality rule. It is closer to reviewability by design: preserve what a later evaluator will need, identify explicit inconsistencies, and expose what remains unresolved.

### 2.4 The Article 30(3) record core

Article 30(3) expressly identifies four retained-record fields:

```text
(work type, source, purpose of use, date of use)
```

We call this the **Article 30(3) core tuple**. It is useful scientifically because the legal text itself specifies information that must survive the development process. The tuple is nevertheless not sufficient to determine legality. A complete record may document an adverse fact—for example, an acquisition known to be unlawful. Accordingly, **evidence readiness is not a favorable legal outcome**.

---

## 3. Related work and the missing evidence layer

### 3.1 Substantive copyright doctrine for AI training

A growing body of scholarship examines whether training-related copying falls within existing exclusive rights, fair-use or fair-dealing doctrines, TDM exceptions, or new licensing arrangements (Samuelson 2023; Guadamuz 2024). Comparative studies show that jurisdictions have adopted materially different combinations of control, compensation, transparency, opt-out, and legal-certainty mechanisms (de la Durantaye 2025; Sag and Yu 2025).

Official policy developments reinforce that diversity. Articles 3 and 4 of the EU Digital Single Market Directive provide TDM exceptions with different beneficiaries and conditions, including a rights-reservation mechanism for the broader exception (European Union 2019). The U.S. Copyright Office’s report on generative-AI training analyzes the application of copyright doctrine and licensing questions in the United States (United States Copyright Office 2025). Japan’s Agency for Cultural Affairs describes its 2024 “General Understanding” as a non-binding interpretation of existing copyright law rather than a definitive legal assessment of particular systems (Agency for Cultural Affairs 2024). The United Kingdom’s 2026 report evaluates copyright, input transparency, technical standards, licensing, and enforcement without treating any single technical mechanism as a complete answer (United Kingdom Government 2026).

IPEL does not offer another universal rule for whether AI training is lawful. It starts one step later: once a jurisdiction makes a use depend on particular facts, what evidence must be preserved so those facts can be reviewed?

### 3.2 Dataset documentation and provenance audits

Data statements, datasheets, model cards, and data cards created a strong documentation tradition in responsible AI (Bender and Friedman 2018; Mitchell et al. 2019; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). These approaches ask developers to document provenance, composition, collection, intended use, performance, limitations, and stakeholder-relevant context. They are essential antecedents to IPEL.

Longpre et al. (2024) demonstrate why lineage and licensing documentation remain operationally difficult. Their audit traces more than 1,800 text datasets and reports frequent licence omissions and inconsistencies across major hosting and aggregation platforms. The Data Provenance Initiative contributes methods and tools for tracing dataset sources, creators, licences, and downstream use.

IPEL is complementary rather than substitutive. Its unit of analysis is an identifiable legal use event where work-level provenance exists, not merely a dataset as a collection. It asks whether the record contains the jurisdiction-specific facts and evidence needed for a later legal review. A dataset card may state a licence category; IPEL additionally preserves which copy was acquired, how it was acquired, which purpose was declared, when the use occurred, what downstream acts were recorded, and which assertions remain unsupported.

### 3.3 Machine-readable usage preferences

The Creator Assertions Working Group’s Training and Data Mining Assertion 1.1 enables a human actor to express whether an asset may be used for data mining, AI inference, generative training, or non-generative training through `allowed`, `notAllowed`, or `constrained` values (CAWG 2025). TDM·AI likewise develops machine-readable AI/TDM preference infrastructure and distinguishes public declarations from negotiated licensing arrangements (TDM·AI n.d.).

These protocols answer a question such as: **what use preference or constraint has been expressed for this asset?** IPEL asks a different question: **what evidence exists that this developer’s particular use satisfied the facts required by the asserted legal pathway?** A usage signal may be highly relevant evidence, but it does not automatically establish lawful acquisition, contractual scope, necessity, downstream permission, or absence of market harm.

### 3.4 Cryptographic content provenance

C2PA provides a technical architecture for storing and validating cryptographically verifiable provenance information. It binds assertions, claims, and signatures into a C2PA Manifest and separates validation from trust-policy assessment (C2PA 2026). The specification expressly cautions against using provenance infrastructure to make value judgments about whether provenance is “good” or “bad”; the technical question is whether assertions are associated with the asset, correctly formed, and free from detected tampering (C2PA 2026, sec. 1.2).

C2PA 2.4 also supports AI/ML-related assets and workflows. Collection data hashes can bind folders of an AI/ML training dataset, and Ingredient assertions can describe data used as input to an AI/ML process (C2PA 2026, secs. 9.2.5 and 18.16). These are important capabilities. Paper A therefore does not propose a rival content-provenance standard. It tests which legal-evidence functions can safely be delegated to C2PA and which remain jurisdiction-specific.

### 3.5 Reviewability, auditability, and computational law

Reviewable automated decision-making argues that accountability requires contextually appropriate records of both technical and organizational processes, not only model-centric explanations (Cobbe, Lee, and Singh 2021). Internal algorithmic auditing similarly emphasizes documentation across the development lifecycle (Raji et al. 2020). Algorithmic-disclosure scholarship examines how disclosure design affects whether information is usable and enforceable (Di Porto 2023).

Computational-law research provides a second relevant boundary. Formal compliance-checking approaches can represent deontic norms and reason over structured facts (Francesconi and Governatori 2023), but automatically processable regulation encounters open texture and interpretive uncertainty (Guitton, Tamò-Larrieux, and Mayer 2023). Empirical work on encoding legislation distinguishes technical validation from legal alignment and shows that factual indeterminacy and interpretation remain even after rules are encoded (Witt et al. 2024).

IPEL adopts both insights. It treats record preservation as part of accountability, while refusing to confuse formal validation with authoritative legal interpretation.

### 3.6 Novelty position

The adjacent layers can be summarized as follows:

| Layer | Primary question | What it does not necessarily establish |
|---|---|---|
| Copyright doctrine | Is the use permitted under the governing law? | whether the necessary historical facts were preserved |
| Dataset documentation/provenance | Where did data come from and how was it documented? | jurisdiction-specific sufficiency for a particular legal pathway |
| Rights signaling | What preference or constraint was expressed? | the complete legal basis for a developer’s use |
| Cryptographic provenance | Are assertions bound, valid, and trusted under a policy? | truth, ownership, acquisition lawfulness, or a legal conclusion |
| IPEL legal-evidence layer | Are legally relevant facts observable, supported, and reviewable? | the final application of open-textured law |

The defensible novelty claim is narrow: IPEL contributes a tested **jurisdiction-specific legal-evidence layer** that maps fact-conditioned copyright rules into observable evidence requirements and enforces semantic barriers so provenance, trust, and preference signals cannot silently become legal conclusions.

---

## 4. IPEL architecture

### 4.1 Design goals

IPEL is designed around five goals:

1. **Observability:** preserve facts a later reviewer may need.
2. **Contestability:** retain evidence references and adverse facts rather than only favorable summaries.
3. **Semantic separation:** distinguish content identity, integrity, signer trust, rights preferences, factual assertions, and legal judgments.
4. **Fail-closed validation:** treat malformed records, missing mandatory fields, and explicit contradictions as visible failures rather than silent passes.
5. **Falsifiability:** expose the architecture to semantic, cryptographic, and later human-review tests that could weaken its claims.

### 4.2 Unit of analysis

The unit is an **AI-development use event** rather than an entire model or dataset. A use event identifies a work or work unit, its source and content identity, the declared purpose and time of use, and evidence about publication, acquisition, copying extent, and downstream handling.

This granularity matters because a dataset-level label can conceal heterogeneous sources and acquisition histories. Where work-level provenance does not exist, IPEL cannot create it retrospectively; the absence itself becomes an evidentiary limitation.

### 4.3 Evidence layers

The legal-to-evidence matrix distinguishes progressively stronger layers:

- **L0 — assertion:** a person or process records a value;
- **L1 — referenced assertion:** the value points to a licence, receipt, archive event, policy, or assessment;
- **L2 — content-bound evidence:** the referenced artifact is identified by a cryptographic digest;
- **L3 — event-bound evidence:** artifact, actor, work digest, purpose, and time are connected to a use event;
- **L4 — tamper-evident evidence:** later modification is detectable through chained, signed, or externally anchored integrity mechanisms.

Moving upward strengthens evidence about identity and change. It does not automatically make the preserved proposition true. A tamper-evident false assertion remains false.

### 4.4 Evidence contract

The prototype contract contains four broad groups:

- **work identity and source:** identifier, type, title, source, content digest;
- **publication and acquisition evidence:** statuses, method, evidence references, and dates;
- **use-event evidence:** purpose, date, copied extent, necessity rationale, and event reference;
- **downstream and judgment-sensitive evidence:** distribution, transformation, public availability, output inclusion, permission/public-domain status, commercial context, market-effect basis, author-interest basis, and independently protected elements.

The contract deliberately separates a status from its basis. For example, a developer cannot obtain a clean outcome merely by setting `market_effect=none` without an evidence or assessment reference.

### 4.5 Gate semantics

The deterministic evidence gate uses three outcomes:

- `PASS_EVIDENCE_GATE` — the tested record contains no hard contradiction or unresolved evidence condition under the project abstraction;
- `REVIEW_REQUIRED` — one or more evidence-dependent or judgment-sensitive matters remain unresolved;
- `FAIL_EVIDENCE_GATE` — the record has a structural deficiency or an explicit adverse contradiction under the tested abstraction.

`PASS_EVIDENCE_GATE` is deliberately not named “lawful” or “compliant”. The output also records `legal_conclusion=false`. An automated system can detect that `work.source` is absent. It cannot determine that a market effect is legally acceptable because the developer asserted that it is.

### 4.6 Interoperability rule

IPEL delegates a field to a generic provenance layer only when the semantics are sufficiently equivalent for the tested purpose. Superficial similarity is insufficient. A generic `dc:title` may safely carry a human-readable work title. A generic ingredient source or relationship does not necessarily substitute for the legally specified source, acquisition history, purpose, or use date without additional capture rules.

---

## 5. Methods

### 5.1 Study scope

Paper A reports non-human technical experiments completed in Stages 003–005 of the reproducibility package. Stages 006–008 are described only as future-validation infrastructure. No participant data, expert adjudication, or human-effect estimate is included.

The experiments use synthetic works and records. This avoids unauthorized use of protected corpora and permits controlled manipulation of legally relevant facts. It also limits external validity, a limitation addressed in Section 9.

### 5.2 Legal-to-evidence mapping and validator

Article 26(4) and Regulation Article 30 were manually decomposed into conditions and candidate evidence. Each condition was classified as structural, evidence-supported, or judgment-sensitive. The mapping was implemented in a machine-readable record contract and deterministic validator.

Synthetic cases tested:

- missing mandatory record fields;
- adverse or unverified publication/acquisition states;
- prohibited distribution or public availability;
- uncertain necessity/proportionality;
- favorable market-effect or author-interest assertions without a basis;
- unnecessary final-product inclusion;
- independently protected embedded elements; and
- malformed or contradictory evidence.

The validator was tested for false-pass paths, including direct calls that bypass schema validation and self-attested favorable conclusions without supporting evidence.

### 5.3 Stage 003: semantic round-trip

Five synthetic cases were constructed:

1. a clean case;
2. an unverified-publication case;
3. a prohibited-distribution case;
4. a case combining a trusted/allowed provenance signal with explicit unlawful acquisition; and
5. a trusted/allowed signal combined with absent output permission.

Each case was encoded into a C2PA-aligned intermediate profile and reconstructed into the IPEL review model. The experiment compared:

- every original leaf value;
- the Article 30(3) four-field tuple;
- the evidence-gate outcome;
- duplication of generic fields; and
- resistance to false equivalence between provenance/trust signals and jurisdiction-specific evidence.

The intermediate representation was expressly not described as a conformant C2PA Manifest.

### 5.4 Stage 004: real C2PA hard binding

A real C2PA Manifest was generated in a synthetic JPEG using pinned `c2patool 0.27.16`. Three corruption classes were introduced:

- a one-byte mutation to the bound asset;
- corruption of a signed assertion payload; and
- corruption affecting claim-signature material.

The adapter parsed structured validation semantics rather than relying only on the command-line exit status. Separate scenarios combined a cryptographically valid CAWG `allowed` signal with explicitly adverse IPEL acquisition or output-permission facts.

### 5.5 Stage 005: second validation surface and trust boundary

A second validation surface was built from the C2PA conformance CLI. The historical dependency graph could not be reconstructed literally because one historical submodule source was unavailable. The reproducibility package records a bounded compatibility repair and does not label it exact upstream reproduction.

The validation surfaces used different observed c2pa-rs versions, 0.90.16 and 0.78.0, but shared the same implementation lineage. We compared normalized outcomes for the three corruption classes, changed the trust configuration for the same valid artifact, tested legal-evidence invariance under that trust change, and submitted a signed TDM assertion containing the unsupported value `maybe`.

Because both surfaces share c2pa-rs lineage, the study records **`IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`**.

### 5.6 Future human validation infrastructure

Stage 006 creates 24 latent synthetic cases with exact factual parity between a strong narrative baseline and an IPEL presentation. The benchmark is balanced by readiness and objective/judgment-sensitive strata and swaps presentation across Forms A and B.

Stage 007 creates a neutral independent-adjudication packet, fail-closed consensus rules, a simulation-based design grid, and a pre-adjudication freeze manifest. Synthetic responses cannot promote the study lock.

Stage 008 creates per-distribution HMAC-derived external case IDs, authenticated private mappings, and a keyed post-intake receipt chain. It reduces accidental deblinding but does not authenticate a human response before intake.

These artifacts make later claims falsifiable. They supply **no human result** to the present paper.

---

## 6. Results

### 6.1 Semantic round-trip

Across the five committed Stage-003 cases, reconstruction produced:

| Outcome | Result |
|---|---:|
| Cases with semantic loss | 0/5 |
| Changed leaf paths | 0 |
| Article 30(3) tuple preserved | 5/5 |
| PASS / REVIEW / FAIL outcome preserved | 5/5 |
| False-equivalence attacks resisted | 2/2 |

The principal negative finding was **0/4 Article 30(3) core fields delegated to C2PA in the tested mapping**. Work type, source, purpose of use, and date of use remained in the jurisdiction-specific layer because the closest generic fields were not treated as safe semantic substitutes under the tested profile.

This is not an impossibility theorem. C2PA supports custom assertions and evolving AI/ML constructs. The finding concerns the tested mapping and the refusal to replace legally specified evidence fields with merely similar provenance fields.

### 6.2 Real C2PA hard binding

The clean Stage-004 artifact produced a valid cryptographic result while its development signer remained untrusted. The tested corruptions were distinguished as follows:

| Test | Structured evidence |
|---|---|
| Clean asset | `validation_state=valid`; data-hash match; claim signature validated |
| One-byte asset mutation | `assertion.dataHash.mismatch` |
| Assertion-payload corruption | `assertion.hashedURI.mismatch` |
| Claim/signature corruption | `claimSignature.mismatch` |

The experiment demonstrates that hard binding materially strengthens evidence about artifact integrity while remaining conceptually distinct from legal meaning.

A practical integration result also emerged: during a mutation test, `c2patool` returned a structured invalid report while the process itself exited successfully. The adapter therefore parses validation semantics rather than equating process success with artifact validity.

### 6.3 Signer trust is not cryptographic validity

The clean Stage-004 artifact had a validated claim signature but an untrusted development signer. In Stage 005, adding the relevant certificate chain to a custom test trust list changed the same cryptographically valid artifact from `untrusted` to `trusted`.

That trust-policy change did not alter the IPEL acquisition status, output-permission state, or evidence-gate outcome. Trust was therefore empirically separable from both cryptographic integrity and jurisdiction-specific legal evidence in the tested system.

### 6.4 Usage preference is not a complete legal basis

In the tested profiles, a CAWG training-use signal of `allowed` did not cure either:

- an explicit `acquisition_status=false`; or
- a transformed-output scenario lacking required permission.

Both remained `FAIL_EVIDENCE_GATE` under the project abstraction. The result does not imply that usage preferences are legally irrelevant. It shows that a machine-readable preference should not silently substitute for other facts that the governing legal pathway separately requires.

### 6.5 Cross-validator agreement and semantic validity

Both Stage-005 validation surfaces identified the same normalized corruption categories for the three Stage-004 attacks. This is cross-version validation within a shared implementation lineage, not independent implementation diversity.

The malformed TDM experiment further separated cryptographic validity from metadata semantics. A signed assertion containing `use=maybe` remained cryptographically valid at the artifact level, while the IPEL semantic normalizers rejected the unsupported value. A valid signature can establish integrity of the signed statement without establishing that the statement belongs to the expected semantic vocabulary.

### 6.6 What Paper A does not report

| Claim | Status |
|---|---|
| IPEL improves reviewer accuracy | not tested with humans |
| IPEL reduces review time | not tested with humans |
| Independent experts confirmed the author labels | no real adjudication collected |
| Independent cryptographic implementations agreed | not established |
| The gate determines legal compliance | expressly disclaimed |

This negative table is part of the results discipline: implemented infrastructure is not counted as empirical support for an unrun study.

---

## 7. Discussion

### 7.1 A layered account of legal-technical evidence

The experiments support four separations:

```text
content identity / integrity
        ≠ signer trust
signer trust
        ≠ metadata semantic validity
usage preference
        ≠ complete legal basis
legal-evidence readiness
        ≠ legal conclusion
```

C2PA is strongest at the first two layers: binding assertions and evaluating them within a trust model. CAWG and TDM·AI communicate rights-related preferences or constraints. IPEL preserves the jurisdiction-specific facts and evidence needed for a later legal review. The final application of open-textured law remains with the competent human or institution.

### 7.2 Integrity is valuable even though it is not truth

The statement that “a hash does not prove legality” should not be misunderstood as minimizing cryptographic provenance. The corruption experiments show that binding and validation can expose changes that ordinary narrative documentation would not. The correct inference is narrower: integrity evidence answers whether identified content or assertions changed; it does not independently establish ownership, acquisition lawfulness, consent, licence scope, market effect, or legal compliance.

This distinction is consistent with C2PA’s own scope, which focuses on validation, association, formation, tamper evidence, and trust signals rather than normative value judgments (C2PA 2026).

### 7.3 Evidence architecture rather than rules-as-code maximalism

IPEL does not attempt to encode every legal condition as executable law. Formal compliance systems can be valuable where norms and facts are sufficiently determinate (Francesconi and Governatori 2023). Yet open texture, factual indeterminacy, and interpretive divergence impose limits on automatic processing (Guitton, Tamò-Larrieux, and Mayer 2023; Witt et al. 2024).

The architecture therefore automates the narrower tasks that are defensible:

- require specified records;
- preserve adverse as well as favorable facts;
- demand evidence bases for selected assertions;
- detect malformed or contradictory configurations;
- bind records to content and events;
- expose uncertainty; and
- route judgment-sensitive matters to review.

Deference is a valid output, not a software failure.

### 7.4 Relationship to reviewability and documentation

IPEL extends the reviewability insight into a specific intellectual-property setting. Cobbe, Lee, and Singh (2021) emphasize that meaningful review requires records of the broader socio-technical process. Dataset documentation frameworks specify useful disclosures about collection, use, limitations, and provenance (Bender and Friedman 2018; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). IPEL adds a jurisdiction-specific mapping that asks why a particular field or evidence reference matters to a particular legal pathway.

This mapping also makes absence visible. The architecture does not infer facts from silence or permit a generic “licensed” label to conceal uncertainty about source, copy, date, scope, or downstream conduct.

### 7.5 Generalizability beyond Saudi Arabia

Paper A does not claim that other jurisdictions use the same copyright elements. The reusable contribution is a method:

1. identify the legal pathway under which an AI-development use may occur;
2. decompose it into factual, evidentiary, and evaluative conditions;
3. identify which facts must remain observable after the event;
4. define an evidence contract without encoding unsupported legal conclusions;
5. delegate generic provenance functions to mature standards when semantics match;
6. retain jurisdiction-specific evidence where they do not;
7. test adversarially whether provenance, trust, or preference signals can overwrite legal facts;
8. defer open-textured conditions to legal review; and
9. preregister human validation before claiming reviewer benefit.

Different jurisdictions will produce different field sets, thresholds, and evidence priorities. That variation is expected. Comparative copyright scholarship confirms that legal pathways differ substantially (de la Durantaye 2025; Sag and Yu 2025). The architecture generalizes as a disciplined mapping and boundary method, not as a universal Saudi field list.

The approach may also extend beyond copyright. Data protection, product safety, regulated AI, consumer protection, and evidence-heavy administrative compliance often depend on reconstructable operational facts while retaining normative conditions that resist complete automation.

---

## 8. Threats to validity

### 8.1 Construct validity

The gate evaluates evidence readiness under a project-authored abstraction, not legal compliance. The names `PASS_EVIDENCE_GATE`, `REVIEW_REQUIRED`, and `FAIL_EVIDENCE_GATE` reduce—but cannot eliminate—the risk that users interpret the output normatively. Documentation, interface design, and governance controls remain necessary.

### 8.2 Internal validity

The semantic benchmark contains five cases and the cryptographic attack set contains three primary corruption classes. These experiments test known boundaries but cannot exhaust all malformed manifests, parser differences, trust-store configurations, or adversarial strategies.

### 8.3 Implementation validity

The two Stage-005 validation surfaces share c2pa-rs lineage. Different observed versions provide useful cross-version evidence, but **implementation diversity was not established**. Agreement may therefore reflect shared code paths or assumptions.

### 8.4 External validity

All completed cases are synthetic. They provide precise control over facts and avoid unauthorized corpus use, but they do not reproduce the scale, heterogeneity, changing licences, mixed ownership, incomplete records, or organizational incentives of a production training pipeline.

### 8.5 Legal validity

The mapping is not authoritative. Future SAIP guidance, judicial interpretation, amendments, or factual contexts may change the relevance or weight of particular fields. The architecture must therefore version legal mappings and preserve the source text and interpretive assumptions on which each profile depends.

### 8.6 Human-study validity

No real adjudicator or reviewer data exist. Stage 006 labels were authored within the project and cannot be treated as independently validated ground truth. Stages 007–008 prepare independent adjudication and controlled intake but do not resolve recruitment, qualification, ethics, consent, or contamination risks.

### 8.7 Blinding and response provenance

The repository is public. Per-distribution external identifiers reduce accidental deblinding but cannot prevent a motivated participant from searching for the synthetic cases. Stage 008 supplies keyed post-intake tamper evidence, not proof that a response was authored by the claimed person or remained unaltered before intake.

---

## 9. Falsification and future work

The architecture is intentionally falsifiable at technical and human-review layers.

At the technical layer, the novelty claim should be narrowed if a mature standard can encode the same jurisdiction-specific evidentiary semantics without material loss or false equivalence. Future C2PA, CAWG, WIPO, or rights-management developments may reduce the need for a separate profile. The `0/4` result must therefore be repeated against later specifications rather than treated as permanent.

A broader corpus should test additional work types, acquisition pathways, licences, mixed rights, transformations, and temporal changes. A genuinely independent C2PA implementation should be added when a maintained and reproducible validator is available.

At the human-review layer, the strongest practical hypothesis remains untested. Stage 006 defines a strong narrative baseline containing the same available facts as IPEL. If a properly governed study shows no meaningful improvement in missing-information detection, false-ready rate, assessment time, or inter-reviewer reproducibility, the utility claim should be weakened rather than rescued by changing the baseline or outcomes after data collection.

Independent adjudication must precede that study. Substantial disagreement with the project-authored readiness labels would be scientifically useful: it would identify ambiguous constructs or cases requiring a new benchmark version. The original labels must remain preserved as provenance rather than silently overwritten.

---

## 10. Conclusion

AI copyright infrastructure needs more than one technical layer. Dataset documentation can disclose data composition and lineage. Rights protocols can communicate usage preferences. C2PA can provide strong evidence about content bindings, assertion validity, and signer trust. None of those functions is identical to preserving the jurisdiction-specific facts required for later legal review.

Saudi Arabia’s 2026 Copyright Law makes this distinction concrete by combining a fact-conditioned AI-development copying pathway with an express record-retention obligation. IPEL operationalizes that problem as an evidence architecture rather than an automated compliance oracle.

The completed experiments show that cryptographic integrity, signer trust, metadata semantics, rights preferences, and legal-evidence status can and should remain separate. The architecture preserves evidence, reuses mature provenance infrastructure where semantics match, refuses false equivalence where they do not, and defers open-textured judgment rather than fabricating it.

The next empirical question is whether independent legal reviewers actually benefit from the structure. That question is reserved for a separately governed human-validation study and is not answered by the present paper.

---

## Declarations

### Data and code availability

All completed experiments use synthetic records and synthetic media. The source code, schemas, generated reports, frozen benchmark materials, and reproducibility scripts are maintained in the project repository. A review-anonymized archival snapshot and persistent identifier should be created before submission if required by the journal.

### Ethics statement

Paper A reports no human-participant data. The future adjudication and reviewer study will not begin until the applicable ethics/consent determination, recruitment population, qualification criteria, data-retention rules, and privacy controls are resolved and documented.

### Competing interests

The author declares no competing interests at the current draft stage.

### Funding

No external funding is claimed for the work reported in this draft.

---

## References

Agency for Cultural Affairs (Japan) (2024) *General Understanding on AI and Copyright in Japan—Overview*. Copyright Division, Agency for Cultural Affairs.

Bender EM, Friedman B (2018) Data statements for natural language processing: toward mitigating system bias and enabling better science. *Transactions of the Association for Computational Linguistics* 6:587–604. https://doi.org/10.1162/tacl_a_00041

CAWG (Creator Assertions Working Group) (2025) *Training and Data Mining Assertion*, version 1.1, ratified 16 May 2025.

Cobbe J, Lee MSA, Singh J (2021) Reviewable automated decision-making: a framework for accountable algorithmic systems. In: *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445921

C2PA (Coalition for Content Provenance and Authenticity) (2026) *C2PA Technical Specification*, version 2.4.

de la Durantaye K (2025) Control and compensation: a comparative analysis of copyright exceptions for training generative AI. *International Review of Intellectual Property and Competition Law* 56:737–770. https://doi.org/10.1007/s40319-025-01569-6

Di Porto F (2023) Algorithmic disclosure rules. *Artificial Intelligence and Law* 31:13–51. https://doi.org/10.1007/s10506-021-09302-7

European Union (2019) Directive (EU) 2019/790 of the European Parliament and of the Council of 17 April 2019 on copyright and related rights in the Digital Single Market. *Official Journal of the European Union* L 130:92–125.

Francesconi E, Governatori G (2023) Patterns for legal compliance checking in a decidable framework of linked open data. *Artificial Intelligence and Law* 31:445–464. https://doi.org/10.1007/s10506-022-09317-8

Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé H III, Crawford K (2021) Datasheets for datasets. *Communications of the ACM* 64(12):86–92. https://doi.org/10.1145/3458723

Guadamuz A (2024) A scanner darkly: copyright liability and exceptions in artificial intelligence inputs and outputs. *GRUR International* 73(2):111–127. https://doi.org/10.1093/grurint/ikad140

Guitton C, Tamò-Larrieux A, Mayer S (2023) Mapping the issues of automated legal systems: why worry about automatically processable regulation? *Artificial Intelligence and Law* 31:571–599. https://doi.org/10.1007/s10506-022-09323-w

Longpre S, Mahari R, Chen A, Obeng-Marnu N, Sileo D, Brannon W, Muennighoff N, Khazam N, Kabbara J, Perisetla K, Wu XA, Shippole E, Bollacker K, Wu T, Villa L, Pentland A, Hooker S (2024) A large-scale audit of dataset licensing and attribution in AI. *Nature Machine Intelligence* 6:975–987. https://doi.org/10.1038/s42256-024-00878-8

Mitchell M, Wu S, Zaldivar A, Barnes P, Vasserman L, Hutchinson B, Spitzer E, Raji ID, Gebru T (2019) Model cards for model reporting. In: *Proceedings of the Conference on Fairness, Accountability, and Transparency*, pp 220–229. https://doi.org/10.1145/3287560.3287596

Pushkarna M, Zaldivar A, Kjartansson O (2022) Data cards: purposeful and transparent dataset documentation for responsible AI. In: *Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3531146.3533231

Raji ID, Smart A, White RN, Mitchell M, Gebru T, Hutchinson B, Smith-Loud J, Theron D, Barnes P (2020) Closing the AI accountability gap: defining an end-to-end framework for internal algorithmic auditing. In: *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*, pp 33–44. https://doi.org/10.1145/3351095.3372873

Sag M, Yu PK (2025) The globalization of copyright exceptions for AI training. *Emory Law Journal* 74:1163–1227.

Samuelson P (2023) Generative AI meets copyright. *Science* 381(6654):158–161. https://doi.org/10.1126/science.adi0656

Saudi Arabia (2026a) *Copyright Law [Nizam Huquq al-Mu’allif]*, including Article 26(4). *Umm Al-Qura*, 13 February 2026. Official Arabic text.

Saudi Arabia (2026b) *Implementing Regulations of the Copyright Law*, including Article 30. *Umm Al-Qura*, 31 July 2026. Official Arabic text.

Saudi Arabia (2026c) Royal Decree No. M/169 dated 14/08/1447H approving the Copyright Law. *Umm Al-Qura*, 13 February 2026.

TDM·AI (n.d.) *TDM·AI Protocol and Documentation*.

United Kingdom Government (2026) *Report on Copyright and Artificial Intelligence*. Department for Science, Innovation and Technology; Department for Culture, Media and Sport; Intellectual Property Office, 18 March 2026.

United States Copyright Office (2025) *Copyright and Artificial Intelligence, Part 3: Generative AI Training*. Washington, DC.

WIPO (World Intellectual Property Organization) (2026) *AI Infrastructure Interchange (AIII)*.

Witt A, Huggins A, Governatori G et al. (2024) Encoding legislation: a methodology for enhancing technical validation, legal alignment and interdisciplinarity. *Artificial Intelligence and Law* 32:293–324. https://doi.org/10.1007/s10506-023-09350-1
