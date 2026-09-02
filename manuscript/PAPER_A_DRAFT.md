# From Statutory Conditions to Reviewable Evidence: Executable Copyright–Provenance Boundaries for AI Development under Saudi Arabia’s 2026 Copyright Law

## Abstract

Copyright scholarship on artificial-intelligence development has largely focused on substantive permission: whether protected works may be copied for model development, which exceptions apply, and when licences or rightsholder reservations control. A separate problem arises after a legally relevant use has occurred: can a developer, regulator, court, or rights holder reconstruct the facts on which the asserted legal pathway depended? That the answer requires records, audit trails, and provenance is not a new observation, and this paper does not claim it as one. Saudi Arabia’s 2026 Copyright Law instead provides a concrete testbed for a narrower and testable question. Article 26(4) permits copying an original work for the development of AI products and algorithms subject to fact-sensitive conditions; Article 37(1) imposes a cross-cutting condition that such uses neither conflict with normal exploitation nor unjustifiably prejudice rightsholders’ legitimate interests; and Article 30 of the Implementing Regulations adds operational restrictions and expressly requires developers to retain records of the work type, source, purpose of use, and date of use. We decompose that three-source pathway into an executable, use-event-level evidence profile (record profile `0.2.0`) and then test, under a rubric frozen before any outcome was observed, which of its legally operative propositions can safely be delegated to C2PA and CAWG semantics. On a 59-case benchmark spanning 13 encoded legal conditions, all 59 declared outcomes and their expected rule, severity, and message findings were reproduced; 55 of 59 cases were constructible as corrected profiles and all 55 preserved the gate outcome, the Article 30(3) tuple, the Article 37(1) tuple, and zero semantic loss, while the four deliberately incomplete records failed closed. Under the frozen rubric, 0/4 Article 30(3) core fields and 0/2 Article 37(1) propositions were safely delegable; the single safe delegation was `work.title`, a descriptive field the evidence gate never reads. A declared naïve provenance-mapping baseline preserved only 31/59 and 29/59 outcomes under two provenance-signal configurations, produced 28 and 14 false equivalences that masked adverse or unresolved legal facts, and changed its legal-facing outcome in 44 of 59 cases purely because the provenance signals changed; the rubric-governed mapping preserved 59/59 in both. Real C2PA hard-binding and cross-validator experiments, and a bounded hash-chain integrity experiment whose negative result motivated reuse of mature provenance infrastructure, are reported as integration evidence rather than cryptographic novelty. The contribution is not automated copyright compliance, and not the idea of an evidence or audit layer: it is a specific statutory decomposition coupled to executable tests of when provenance and rights-signaling semantics are not safely substitutable for legally relevant evidence propositions.

**Keywords:** AI training; copyright; provenance; legal evidence; C2PA; computational law; Saudi Arabia; intellectual property; auditability; reviewability

---

## 1. Introduction

The use of copyrighted works in artificial-intelligence development has generated an increasingly international debate about reproduction, fair use, text-and-data-mining exceptions, licences, rights reservations, transparency, and compensation (Samuelson 2023; Guadamuz 2024; de la Durantaye 2025; Sag and Yu 2025). The legal answers vary substantially. The United States has developed the question largely through fair-use doctrine and litigation, the European Union has enacted text-and-data-mining exceptions subject to conditions and reservations, Japan applies a comparatively broad non-enjoyment-oriented limitation, and the United Kingdom has continued to evaluate competing reform options (European Union 2019; Agency for Cultural Affairs 2024; United States Copyright Office 2025; United Kingdom Government 2026). This paper does not attempt to resolve that substantive debate across jurisdictions.

A different systems problem appears when any legal pathway depends on facts that must be reconstructed later. A rule may ask whether a work was lawfully published or acquired, why it was copied, when it was used, how much was needed, whether downstream distribution occurred, whether a permission applied, or whether a use conflicted with normal exploitation or unjustifiably prejudiced the rightsholder’s legitimate interests. Even when the governing rule is known, a later reviewer cannot apply it reliably if the development pipeline did not preserve the relevant facts and their supporting evidence.

### 1.1 What this paper concedes at the outset

The general shape of that problem is well established, and this paper claims no priority over it. Accountability scholarship already argues that meaningful review depends on contextually appropriate records of technical *and* organizational process rather than on model-centric explanation (Cobbe, Lee, and Singh 2021), and internal algorithmic auditing already prescribes lifecycle documentation artifacts (Raji et al. 2020). Dataset-documentation frameworks already ask developers to disclose composition, provenance, collection practice, intended use, and limitations (Bender and Friedman 2018; Mitchell et al. 2019; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). Large-scale provenance audits already show that licence and attribution documentation fails at scale (Longpre et al. 2024). Machine-readable protocols already communicate training and data-mining preferences (CAWG 2025; TDM·AI n.d.), and C2PA already binds assertions to assets and supplies validation and trust machinery, including AI/ML ingredient and dataset constructs (C2PA 2026). Disclosure-design scholarship already warns that information which is nominally disclosed may not be usable or enforceable (Di Porto 2023). Recent work narrows the claim further: Li (2026) develops a minimum reviewable trace for public-sector AI accountability; Lucchi (2026) frames AI-assisted authorship as a copyright auditability gap; Park (2025) proposes NFT/C2PA-based copyright-management infrastructure for AI training data; and Krishna, Shree, and Raguram (2026) propose a provenance-disclosure procedure for AI copyright litigation. Model-side work such as TrainProVe (Xie et al. 2025) and information-isotope tracing (Qi et al. 2026) addresses post-hoc evidence that data were used in training rather than contemporaneous evidence of the legal/operational basis of a particular use.

Accordingly, this paper does **not** claim novelty for any of the following: that AI governance needs an evidence layer; that auditability or reviewability should be designed in; that transparency alone is insufficient; that C2PA can be applied to AI-training copyright and rights management; or that training-data provenance can be documented and verified. Each is treated here as prior intellectual foundation. The project’s working term **evidentiary observability** — the ability to reconstruct, test, and contest legally relevant facts about an AI-development use event after the event has occurred — is used as internal vocabulary for that foundation, not as a claim of conceptual priority over auditability, reviewability, minimum reviewable trace, or evidentiary-infrastructure terminology already in circulation.

### 1.2 The narrower question this paper actually tests

Saudi Arabia’s new Copyright Law makes one instance of the problem unusually concrete. Royal Decree No. M/169 approved the Copyright Law in February 2026 (Saudi Arabia 2026c). Article 26(4) permits copying an original work for the development of AI products and algorithms when the work was lawfully published, ownership of the original copy was lawfully obtained, and copying remains within what serves the purpose (Saudi Arabia 2026a, art. 26(4)). Article 37(1) applies a cross-cutting condition to uses permitted under Articles 26–36: they must not conflict with normal exploitation of the work and must not cause unjustified prejudice to the legitimate interests of rightsholders (Saudi Arabia 2026a, art. 37(1)). Article 30 of the Implementing Regulations adds six groups of controls, including an express duty to retain records showing the type of work, its source, the purpose of use, and the date of use (Saudi Arabia 2026b, art. 30).

The combination is computationally significant. Some requirements are record-like: a source or date can be required structurally. Others are evidence-dependent: a statement that acquisition was lawful may need a receipt, licence, archive record, or other basis. Still others are open-textured: whether a use conflicts with normal exploitation or causes unjustified prejudice cannot safely be reduced to a Boolean supplied by the developer. Research on automatically processable regulation and encoded legislation similarly warns that technical validation does not eliminate legal interpretation, ambiguity, or factual indeterminacy (Guitton, Tamò-Larrieux, and Mayer 2023; Francesconi and Governatori 2023; Witt et al. 2024).

We introduce **IPEL (Intellectual-Property Evidence Ledger)** as a research architecture for this boundary. “Ledger” denotes a reviewable record abstraction and does not imply a blockchain. IPEL is not a copyright oracle and does not predict court outcomes. It models an identifiable AI-development **use event** and preserves jurisdiction-specific facts and evidence references that a later reviewer may need. Its deterministic evidence gate distinguishes structural absence and explicit contradiction from evidentiary uncertainty, while preserving a review-required state for conditions that cannot responsibly be automated.

The paper is organized around four research questions:

- **RQ1.** Which facts and evidence must remain observable to review a use under the Saudi Article 26(4) + Article 37(1) + Regulation Article 30 pathway?
- **RQ2.** Which of those legally operative propositions can be delegated to generic content-provenance or rights-signaling semantics without semantic loss, under criteria fixed before the outcome is observed?
- **RQ3.** What failure modes arise when a system does treat provenance validity, signer trust, or rights signals as legal facts?
- **RQ4.** What integrity properties does an evidence record gain, and fail to gain, from progressively stronger provenance designs?

### 1.3 Contributions

The contributions are correspondingly narrow.

First, a **statutory decomposition** of an enacted AI-development copying pathway at use-event granularity, spanning Copyright Law Article 26(4), Copyright Law Article 37(1), and Implementing Regulation Article 30(1)–(6), and encoded as a versioned, executable evidence profile (`0.2.0`) whose gate returns `legal_conclusion=false` by construction. The decomposition separates factual observability, evidentiary support, and normative judgment, and treats the Article 30(3) four-field tuple as a minimum retention core rather than a complete compliance record. It also refuses to collapse Article 37(1) into the superficially similar Regulation Article 30(2) and 30(4) conditions.

Second, an **executable semantic-boundary experiment**: a delegation rubric frozen before any candidate outcome was observed, applied to a preregistered candidate set covering work type/source, use purpose/date, a descriptive title field, and the two Article 37(1) propositions, with controlled substitution round-trips that measure — rather than assert — whether the original legal-evidence value can be recovered without inference and whether the evidence gate notices when it cannot.

Third, a **corrected-profile condition benchmark and declared baseline comparison**: 59 cases across 13 encoded conditions, plus a naïve provenance-mapping comparator that demonstrates the concrete failure mode (masking of adverse legal facts, and outcome instability driven by provenance signal state) that the semantic barrier is designed to prevent.

Fourth, an explicit **negative-result and limitation record**, including a bounded hash-chain integrity experiment whose failure modes motivated reusing mature provenance infrastructure instead of inventing one, the absence of any candidate for either Article 37(1) proposition, condition states the profile cannot express, and a preregistered human-validation pipeline from which **no human-effect result is claimed** in this paper.

The central claim is deliberately bounded: for this pathway, mature provenance and rights-signaling semantics were not safely substitutable for the legally operative evidence propositions under declared criteria, and a system that substitutes them anyway can be shown to mask adverse legal facts.

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

### 2.3 Article 37(1): the cross-cutting condition

Article 37(1) conditions the uses permitted under Articles 26–36 on two further propositions: that the use does not conflict with normal exploitation of the work, and that it does not cause unjustified prejudice to the legitimate interests of rightsholders (Saudi Arabia 2026a, art. 37(1)).

An earlier version of this project modelled the pathway as Article 26(4) plus Regulation Article 30 alone. That scope was materially incomplete, and the omission was corrected in a dedicated remediation stage rather than silently. The corrected profile now carries an explicit `article37_context` with two propositions and two assessment bases, and the evidence gate fails on an explicit conflict or explicit unjustified prejudice, requires review when either proposition is unresolved, and also requires review when a favorable assertion has no recorded assessment basis.

The corrected model deliberately does **not** treat the Regulation conditions as automatic substitutes:

```text
IR-30(2) commercial-context normal-exploitation impact
    != automatically LAW-37(1) cross-cutting normal-exploitation conflict

IR-30(4) author-interest / exploitation-opportunity assessment
    != automatically LAW-37(1) rightsholder legitimate-interests assessment
```

This is a conservative evidence-modelling choice, not a claim that the underlying legal concepts can never overlap in a concrete case. Section 6.2 reports the benchmark cases that test the separation in both directions.

### 2.4 Implementing Regulation Article 30

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

This decomposition differs from compiling the law into a binary legality rule. It follows the reviewability tradition (Cobbe, Lee, and Singh 2021; Raji et al. 2020) rather than extending it: preserve what a later evaluator will need, identify explicit inconsistencies, and expose what remains unresolved.

### 2.5 The Article 30(3) record core

Article 30(3) expressly identifies four retained-record fields:

```text
(work type, source, purpose of use, date of use)
```

We call this the **Article 30(3) core tuple**. It is useful scientifically because the legal text itself specifies information that must survive the development process, which makes the delegation question in RQ2 concrete rather than rhetorical. The tuple is nevertheless not sufficient to determine legality. A complete record may document an adverse fact—for example, an acquisition known to be unlawful. Accordingly, **evidence readiness is not a favorable legal outcome**.

---

## 3. Related work and adjacent evidence layers: what is conceded and what remains

### 3.1 Substantive copyright doctrine for AI training

A growing body of scholarship examines whether training-related copying falls within existing exclusive rights, fair-use or fair-dealing doctrines, TDM exceptions, or new licensing arrangements (Samuelson 2023; Guadamuz 2024). Comparative studies show that jurisdictions have adopted materially different combinations of control, compensation, transparency, opt-out, and legal-certainty mechanisms (de la Durantaye 2025; Sag and Yu 2025).

Official policy developments reinforce that diversity. Articles 3 and 4 of the EU Digital Single Market Directive provide TDM exceptions with different beneficiaries and conditions, including a rights-reservation mechanism for the broader exception (European Union 2019). The U.S. Copyright Office’s report on generative-AI training analyzes the application of copyright doctrine and licensing questions in the United States (United States Copyright Office 2025). Japan’s Agency for Cultural Affairs describes its 2024 “General Understanding” as a non-binding interpretation of existing copyright law rather than a definitive legal assessment of particular systems (Agency for Cultural Affairs 2024). The United Kingdom’s 2026 report evaluates copyright, input transparency, technical standards, licensing, and enforcement without treating any single technical mechanism as a complete answer (United Kingdom Government 2026).

IPEL does not offer another universal rule for whether AI training is lawful. It starts one step later: once a jurisdiction makes a use depend on particular facts, which of those facts can an existing standard carry, and which cannot it carry?

### 3.2 Dataset documentation and provenance audits

Data statements, datasheets, model cards, and data cards created a strong documentation tradition in responsible AI (Bender and Friedman 2018; Mitchell et al. 2019; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). These approaches ask developers to document provenance, composition, collection, intended use, performance, limitations, and stakeholder-relevant context. They are antecedents to IPEL, not gaps that IPEL fills.

Longpre et al. (2024) demonstrate why lineage and licensing documentation remain operationally difficult. Their audit traces more than 1,800 text datasets and reports frequent licence omissions and inconsistencies across major hosting and aggregation platforms. The Data Provenance Initiative contributes methods and tools for tracing dataset sources, creators, licences, and downstream use.

IPEL is complementary rather than substitutive. Its unit of analysis is an identifiable legal use event where work-level provenance exists, not a dataset as a collection. A dataset card may state a licence category; the tested profile additionally records which copy was acquired, how it was acquired, which purpose was declared, when the use occurred, what downstream acts were recorded, and which assertions remain unsupported — and, critically for RQ2, records which of those the tested standards could not carry.

### 3.3 Machine-readable usage preferences

The Creator Assertions Working Group’s Training and Data Mining Assertion 1.1 enables a human actor to express whether an asset may be used for data mining, AI inference, generative training, or non-generative training through `allowed`, `notAllowed`, or `constrained` values (CAWG 2025). TDM·AI likewise develops machine-readable AI/TDM preference infrastructure and distinguishes public declarations from negotiated licensing arrangements (TDM·AI n.d.).

The rights-expression lineage is older and broader than these AI-specific signals. ODRL 2.2 is a W3C Recommendation for expressing permissions, prohibitions, duties, actions, assets, parties, and constraints (W3C 2018); RightsML is an IPTC media-industry profile of ODRL (IPTC 2018); and ccREL expresses Creative Commons licensing terms in machine-readable form (Abelson et al. 2008). A 2026 ODRL AI Vocabulary draft extends that policy-expression tradition with AI-specific actions, but it remains a Community Group draft rather than a W3C Recommendation (W3C ODRL Community Group 2026). Paper A therefore claims no novelty for machine-readable rights expression.

These protocols answer a question such as: **what use preference or constraint has been expressed for this asset?** IPEL asks a different question: **what evidence exists that this developer’s particular use satisfied the facts required by the asserted legal pathway?** A usage signal may be highly relevant evidence, but it does not automatically establish lawful acquisition, contractual scope, necessity, downstream permission, absence of conflict with normal exploitation, or absence of unjustified prejudice. Section 6.5 measures what happens to a benchmark of encoded legal conditions when a system nevertheless infers those propositions from such a signal.

### 3.4 Cryptographic content provenance

C2PA provides a technical architecture for storing and validating cryptographically verifiable provenance information. It binds assertions, claims, and signatures into a C2PA Manifest and separates validation from trust-policy assessment (C2PA 2026). The specification expressly cautions against using provenance infrastructure to make value judgments about whether provenance is “good” or “bad”; the technical question is whether assertions are associated with the asset, correctly formed, and free from detected tampering (C2PA 2026, sec. 1.2).

C2PA 2.4 also supports AI/ML-related assets and workflows. Collection data hashes can bind folders of an AI/ML training dataset, and Ingredient assertions can describe data used as input to an AI/ML process (C2PA 2026, secs. 9.2.5 and 18.16). Applying content provenance to AI-training copyright and rights management is therefore an established direction, and this paper claims no priority for it. Paper A proposes no rival content-provenance standard; it tests which legal-evidence functions can be delegated to C2PA under declared criteria and which cannot.

### 3.5 Reviewability, auditability, and computational law

Reviewable automated decision-making argues that accountability requires contextually appropriate records of both technical and organizational processes, not only model-centric explanations (Cobbe, Lee, and Singh 2021). Internal algorithmic auditing similarly emphasizes documentation across the development lifecycle (Raji et al. 2020). Algorithmic-disclosure scholarship examines how disclosure design affects whether information is usable and enforceable (Di Porto 2023). These are the intellectual foundations of the present work, and the “design in auditability” argument belongs to them.

Computational-law research provides a second relevant boundary. Formal compliance-checking approaches can represent deontic norms and reason over structured facts (Francesconi and Governatori 2023), but automatically processable regulation encounters open texture and interpretive uncertainty (Guitton, Tamò-Larrieux, and Mayer 2023). Empirical work on encoding legislation distinguishes technical validation from legal alignment and shows that factual indeterminacy and interpretation remain even after rules are encoded (Witt et al. 2024).

IPEL adopts both insights. It treats record preservation as part of accountability, while refusing to confuse formal validation with authoritative legal interpretation.

### 3.6 Novelty position after narrowing

The adjacent layers can be summarized as follows:

| Layer | Primary question | What it does not necessarily establish |
|---|---|---|
| Copyright doctrine | Is the use permitted under the governing law? | whether the necessary historical facts were preserved |
| Dataset documentation/provenance | Where did data come from and how was it documented? | jurisdiction-specific sufficiency for a particular legal pathway |
| Rights signaling | What preference or constraint was expressed? | the complete legal basis for a developer’s use |
| Cryptographic provenance | Are assertions bound, valid, and trusted under a policy? | truth, ownership, acquisition lawfulness, or a legal conclusion |
| IPEL legal-evidence profile | Are the pathway’s legally operative facts observable, supported, and reviewable? | the final application of open-textured law |

The closest identified prior work makes the narrowing concrete. Li (2026) directly translates accountability duties into a minimum reviewable trace; Lucchi (2026) frames a copyright auditability gap around evidence of human creative contribution; Park (2025) combines C2PA metadata with copyright-management infrastructure for AI training data; and Krishna, Shree, and Raguram (2026) propose cryptographic provenance disclosure for copyright litigation. TrainProVe (Xie et al. 2025) and information-isotope tracing (Qi et al. 2026) show that training-data provenance can also be attacked from the model side after training. These works substantially anticipate any broad claim to “auditability”, “evidence infrastructure”, C2PA-for-copyright, or provenance verification. They do not, however, report the same Saudi use-event statutory decomposition plus a pre-locked cross-standard semantic-substitution experiment and corrected-profile false-equivalence baseline. The surviving claim is therefore a conjunction, not a concept:

> a jurisdiction-specific, use-event-level evidence profile derived from the Saudi Article 26(4) + Article 37(1) + Regulation Article 30 pathway, coupled to executable tests showing when mature provenance and rights-signaling semantics are **not** safely substitutable for the legally relevant evidence propositions, while preserving a hard boundary between technical evidence state and legal conclusion.

What is being contributed is the specific statutory decomposition, the executable semantic-boundary experiment, and the corrected-profile benchmark that measures both. What is *not* being contributed is generic provenance, generic auditability, generic reviewability, rights expression, or the terminology of evidentiary observability.

---

## 4. IPEL architecture

### 4.1 Design goals

IPEL is designed around five goals:

1. **Observability:** preserve facts a later reviewer may need.
2. **Contestability:** retain evidence references and adverse facts rather than only favorable summaries.
3. **Semantic separation:** distinguish content identity, integrity, signer trust, rights preferences, factual assertions, and legal judgments.
4. **Fail-closed validation:** treat malformed records, missing mandatory fields, and explicit contradictions as visible failures rather than silent passes.
5. **Falsifiability:** expose the architecture to semantic, cryptographic, and later human-review tests that could weaken its claims.

A sixth constraint is discussed in Section 8.7: the record should be **evidentiarily sufficient but minimal**, because retention is itself a risk.

### 4.2 Unit of analysis

The unit is an **AI-development use event** rather than an entire model or dataset. A use event identifies a work or work unit, its source and content identity, the declared purpose and time of use, and evidence about publication, acquisition, copying extent, downstream handling, and the Article 37(1) propositions.

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

The prototype contract contains five broad groups:

- **work identity and source:** identifier, type, title, source, content digest;
- **publication and acquisition evidence:** statuses, method, evidence references, and dates;
- **use-event evidence:** purpose, date, copied extent, necessity rationale, and event reference;
- **downstream and judgment-sensitive evidence:** distribution, transformation, public availability, output inclusion, permission/public-domain status, commercial context, market-effect basis, author-interest basis, and independently protected elements;
- **Article 37(1) context:** the normal-exploitation and legitimate-interests propositions plus their separate assessment bases.

The contract deliberately separates a status from its basis. A developer cannot obtain a clean outcome merely by asserting that normal exploitation is unaffected without an assessment reference.

### 4.5 Gate semantics

The deterministic evidence gate uses three outcomes:

- `PASS_EVIDENCE_GATE` — the tested record contains no hard contradiction or unresolved evidence condition under the project abstraction;
- `REVIEW_REQUIRED` — one or more evidence-dependent or judgment-sensitive matters remain unresolved;
- `FAIL_EVIDENCE_GATE` — the record has a structural deficiency or an explicit adverse contradiction under the tested abstraction.

`PASS_EVIDENCE_GATE` is deliberately not named “lawful” or “compliant”. The output also records `legal_conclusion=false`, together with the `legal_profile_id` and whether the declared legal scope is complete. An automated system can detect that `work.source` is absent. It cannot determine that a use is consistent with normal exploitation because the developer asserted that it is.

### 4.6 Delegation rule: from discretion to a frozen rubric

An earlier formulation of the interoperability rule delegated a field to a generic provenance layer when the semantics were “sufficiently equivalent for the tested purpose”. That phrasing was too discretionary to be falsifiable, because the person applying it could observe the result they preferred.

It was replaced by an explicit rubric (version `1.0.0`) fixed and hash-locked before any candidate was assessed. A generic field may substitute for a jurisdiction-specific evidence field only if every applicable dimension passes: referent/subject equivalence, event or process anchoring, actor or issuer equivalence, temporal semantics, predicate semantics (no rights preference substituted for a historical or legal fact), evidentiary-function equivalence, value-domain compatibility, qualifier and scope preservation, and round-trip recoverability without inference. Dimensions that do not apply to a proposition class are declared not-applicable in advance rather than silently passed, and the classifier fails closed.

The rubric produces four decisions: `SAFE_DELEGATION`, `PARTIAL_SUPPORT` (the generic field is informative but the IPEL field is retained), `NOT_SAFE_TO_DELEGATE`, and `NO_CANDIDATE`. Section 5.4 describes the lock procedure that separates rubric authorship from outcome observation.

---

## 5. Methods

### 5.1 Study scope

Paper A reports non-human technical experiments. The earlier experiments — the integrity ablation, the original semantic round-trip, and the two C2PA validation experiments — were completed on the legacy record profile `0.1.0`; the legal-evidence experiments that carry the paper’s central claims were re-executed on the corrected profile `0.2.0` after Article 37(1) was added to the declared scope. The reviewer-benchmark and adjudication stages are described only as future-validation infrastructure. No participant data, expert adjudication, or human-effect estimate is included.

The experiments use synthetic works and records. This avoids unauthorized use of protected corpora and permits controlled manipulation of legally relevant facts. It also limits external validity, a limitation addressed in Section 8.

### 5.2 Integrity ablation: is a self-contained history sufficient?

Before adopting any external provenance standard, the project tested the simplest candidate mechanism: a minimal hash-linked event history maintained by the developer. A three-event synthetic history (acquisition, AI-development use, rights assessment) was subjected to six committed adversarial variants — middle-event deletion, event insertion, payload mutation, payload rewrite with full downstream rehashing, reordering, and tail deletion — and each variant was verified twice: against internal chain consistency only, and against the clean chain’s previously preserved `(event_count, head_hash)` checkpoint.

This experiment is reported here as a **design-selection ablation**, because its outcome determined the architecture that the rest of the paper tests.

### 5.3 Legal-to-evidence mapping and profile correction

Article 26(4), Article 37(1), and Regulation Article 30 were manually decomposed into conditions and candidate evidence. Each condition was classified as structural, evidence-supported, or judgment-sensitive, and implemented in a machine-readable record contract and deterministic validator.

The correction from profile `0.1.0` (`sa-copyright-2026-art26-4-ir30-legacy-v0.1`) to profile `0.2.0` (`sa-copyright-2026-art26-4-art37-1-ir30-v0.2`) was versioned rather than retroactive. Legacy records continue to validate under the legacy profile but now report `declared_scope_complete=false`, and legacy artifacts were not rewritten. Regression tests assert both that the Article 37(1) conditions cannot be satisfied by favorable Regulation Article 30 fields and that the historical artifacts still declare `record_version=0.1.0`.

### 5.4 Pre-outcome rubric lock

The delegation rubric of Section 4.6 and the registry of candidate mappings were authored, canonicalized, and hash-locked in a separate stage before any candidate was assessed. The lock records the canonical SHA-256 of the rubric definition and of the candidate registry, the lock status `PRE_OUTCOME_RUBRIC_LOCK`, and the source commit. Every registry row was frozen with `assessment_status=NOT_RUN`.

The benchmark runner refuses to execute unless both hashes still match the lock. Outcomes are written to separate artifacts rather than back into the frozen registry, so no candidate can be added, removed, or reselected after outcomes become visible.

### 5.5 Corrected-profile condition benchmark

Cases were constructed by condition coverage rather than to a target count: every encoded condition of the declared legal scope appears in its logically available states (favorable/supported, unresolved/unsupported, explicit adverse). The result is 59 cases across 13 conditions. Each case declares in advance its expected outcome, the gate rule that must carry the finding, and a message marker, so a case cannot be satisfied by an unrelated rule firing.

Four cases specifically test the Article 37(1) / Regulation Article 30 separation in both directions: an adverse Article 37 fact combined with favorable Regulation fields, and an adverse Regulation fact combined with a favorable Article 37 assessment.

Every case was additionally used for a corrected-profile mapping round-trip: the record was encoded into a C2PA-aligned intermediate profile and reconstructed, comparing every original leaf value, the Article 30(3) tuple, the Article 37(1) context tuple, and the evidence-gate outcome. The intermediate representation is expressly not described as a conformant C2PA Manifest.

### 5.6 Rubric application and controlled delegation round-trips

All 11 frozen candidates were assessed under rubric `1.0.0` with per-dimension reasons recorded. For every candidate that had a counterpart at all, the substitution was then actually performed and read back: the IPEL value was replaced by the generic semantic, and the harness measured whether the original value was recovered, whether recovery required a declared bridging assumption, and whether the evidence-gate outcome changed. Declared round-trip states are cross-checked against measured harness output, and a mismatch aborts the run rather than being reconciled.

### 5.7 Declared naïve baseline

A comparator was declared before outcomes were read. The naïve provenance-mapping baseline is what an engineer would build from field-name similarity alone: five IPEL paths are delegated to the most name-similar C2PA/CAWG semantic, and thirteen further paths — including both Article 37(1) propositions — are inferred from provenance signals (manifest validity, signer trust, and the CAWG training/mining declaration). Fields with no provenance analogue are retained unchanged. The rubric-governed mapping delegates only what the rubric classified `SAFE_DELEGATION` and infers nothing.

Both mappings were run over all 59 cases under two provenance-signal configurations: valid/trusted/`allowed`, and unknown/unknown/`constrained`. Metrics were outcome preservation, *false equivalence* (true outcome adverse or unresolved but reconstructed outcome strictly less severe), spurious escalation, leaf-path semantic loss, and outcome stability across the two signal configurations. The baseline is a comparator constructed by this project; it is not an observation of any third party’s system.

### 5.8 Legacy semantic round-trip (profile 0.1.0)

The original proof-of-concept used five synthetic cases: a clean case; an unverified-publication case; a prohibited-distribution case; a trusted/`allowed` provenance signal combined with explicit unlawful acquisition; and a trusted/`allowed` signal combined with absent output permission. It is retained in this paper only as legacy `0.1.0` evidence of feasibility, and its numbers are never used as corrected-profile results.

### 5.9 Real C2PA hard binding

A real C2PA Manifest was generated in a synthetic JPEG using pinned `c2patool 0.27.16`. Three corruption classes were introduced: a one-byte mutation to the bound asset; corruption of a signed assertion payload; and corruption affecting claim-signature material. The adapter parsed structured validation semantics rather than relying only on the command-line exit status. Separate scenarios combined a cryptographically valid CAWG `allowed` signal with explicitly adverse IPEL acquisition or output-permission facts.

### 5.10 Second validation surface and trust boundary

A second validation surface was built from the C2PA conformance CLI. The historical dependency graph could not be reconstructed literally because one historical submodule source was unavailable. The reproducibility package records a bounded compatibility repair and does not label it exact upstream reproduction.

The validation surfaces used different observed c2pa-rs versions, 0.90.16 and 0.78.0, but shared the same implementation lineage. We compared normalized outcomes for the three corruption classes, changed the trust configuration for the same valid artifact, tested legal-evidence invariance under that trust change, and submitted a signed TDM assertion containing the unsupported value `maybe`.

Because both surfaces share c2pa-rs lineage, the study records **`IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`**.

### 5.11 Future human validation infrastructure

A reviewer benchmark of 24 latent synthetic cases with exact factual parity between a strong narrative baseline and an IPEL presentation has been implemented, balanced by readiness and objective/judgment-sensitive strata and swapped across Forms A and B. A neutral independent-adjudication packet, fail-closed consensus rules, a simulation-based design grid, and a pre-adjudication freeze manifest exist; synthetic responses cannot promote the study lock. A distribution layer supplies per-distribution HMAC-derived external case IDs, authenticated private mappings, and a keyed post-intake receipt chain; it reduces accidental deblinding but does **not authenticate a human response before intake**.

These artifacts make later claims falsifiable. They supply **no human result** to the present paper.

---

## 6. Results

### 6.1 Integrity ablation: why a self-contained chain was rejected

| Attack | Internal-only detects? | Checkpoint detects? |
|---|---:|---:|
| Middle-event deletion | yes | yes |
| Event insertion | yes | yes |
| Payload mutation | yes | yes |
| Rehashed forgery | **no** | yes |
| Reordering | yes | yes |
| Tail deletion | **no** | yes |

Internal consistency alone detected 4/6 of the committed fixtures; verification against an independently preserved checkpoint detected 6/6. These percentages describe only the six committed attack fixtures and are not a security guarantee or an estimate of real-world adversarial coverage.

The negative result is the useful part. A hash chain maintained by the party whose conduct is under review is not sufficient as a historical trust mechanism: an actor able to rewrite the stored history and recompute hashes defeats internal verification, and tail truncation is invisible without an external boundary commitment. The experiment also does not establish who created a checkpoint, whether it existed at the asserted time, or whether the recorded events were truthful when written. The implementation therefore hard-codes:

```text
integrity_verified != claim_truth_verified
```

This is why the architecture does not propose an IPEL-specific production signing stack. Mature provenance infrastructure already supplies signed claims, asset bindings, ingredients, and a trust ecosystem; the design choice that follows is to reuse it and to spend the project’s effort on the jurisdiction-specific evidence profile and its boundaries.

### 6.2 Corrected-profile condition benchmark

| Measure | Value |
|---|---|
| Cases | 59 |
| Conditions | 13 |
| Outcomes matching declared expectation | 59/59 |
| Cases where the expected rule/severity/marker finding was present | 59/59 |
| Favorable (evidence-ready) states | 16 |
| Unresolved (review) states | 19 |
| Adverse (fail) states | 24 |

All corrected-profile cases report `legal_profile_id=sa-copyright-2026-art26-4-art37-1-ir30-v0.2` and a complete declared scope; an unsupported-version case fails closed. `legal_conclusion=false` holds in all 59 cases.

The Article 37(1) separation held in both directions. A favorable Regulation Article 30(2) or 30(4) field did not mask an adverse Article 37(1) fact, and an Article 37(1) assessment did not silently satisfy a Regulation condition; in each of the four separation cases the failure was carried by the expected rule and the other rule produced no finding.

### 6.3 What can be delegated to C2PA and CAWG

All 11 preregistered candidates were assessed under the locked rubric with no rubric change and no reselection.

| Decision | Count |
|---|---:|
| `SAFE_DELEGATION` | 1 |
| `PARTIAL_SUPPORT` | 8 |
| `NOT_SAFE_TO_DELEGATE` | 0 |
| `NO_CANDIDATE` | 2 |

The single safe delegation is `work.title → C2PA 2.4 Ingredient v3 dc:title`. `work.title` is a human-readable entity attribute: it is not one of the four Implementing Regulations Article 30(3) retained-record fields and is not read by the evidence gate. Delegating it removes no legally operative proposition. Ten of eleven IPEL fields are retained.

For the legally operative propositions:

```text
Implementing Regulations Article 30(3) core fields safely delegable : 0/4
Copyright Law Article 37(1) propositions safely delegable           : 0/2
```

Neither Article 37(1) proposition had any candidate at all in the frozen registry. That is a reported absence at the registry, not a demonstration that no such normative semantic could ever be defined.

**0/4 Article 30(3) core fields** is therefore a corrected-profile result produced under an explicit, pre-locked rubric. It corroborates the direction of a legacy intuition recorded earlier in the project, but it does not restate that legacy number, which was generated under a different profile and a more discretionary criterion (Section 6.7). This is not an impossibility theorem: C2PA supports custom assertions and evolving AI/ML constructs, the assessment is bounded by the candidates in the frozen registry, and the result must be re-run against later specification versions.

### 6.4 Controlled delegation round-trips

Every candidate that had a counterpart was substituted and read back.

| Measure | Value |
|---|---|
| Candidates round-tripped | 9 |
| Round-trips passing every criterion | 1 |
| Candidates whose value was recovered byte-identically | 2 |
| Candidates needing a declared bridging assumption | 8 |
| Substitutions the evidence gate could **not** detect | 7 |

Two findings deserve emphasis.

First, **string-level recovery is not semantic equivalence**. Delegating `use.date` to the `when` field of a C2PA action recovered the same date string and preserved the gate outcome, yet still failed the rubric: recovery is only possible under the declared bridging assumption that the timestamped provenance action *is* the legally relevant use event. The frozen rubric anticipated this case before any outcome was observed, requiring that a timestamp be assessed for the proposition it timestamps rather than equated with `use.date` by field-name similarity.

Second, **the evidence gate is not a detector of bad delegation**. In 7 of 9 substitutions the IPEL value was replaced by a semantically different value and the gate outcome did not change. Delegation safety must therefore be established by a declared rubric; observing that a gate still passes proves nothing about it. This is a limitation of the architecture reported as such, not a property to be advertised.

### 6.5 The naïve baseline fails in a specific, measurable way

| Provenance signals | Naïve outcomes preserved | Naïve false equivalences | Naïve spurious escalations | Rubric-governed outcomes preserved |
|---|---:|---:|---:|---:|
| valid / trusted / `allowed` | 31/59 | 28 | 0 | 59/59 |
| unknown / unknown / `constrained` | 29/59 | 14 | 16 | 59/59 |

Under favorable provenance the naïve baseline masked, among others, explicit Article 37(1) normal-exploitation conflict, explicit Article 37(1) unjustified rightsholder prejudice, explicitly false lawful publication, explicitly false lawful acquisition, unsupported necessity, and the omission of the entire Article 37(1) context.

Two further comparator results:

- **Semantic loss.** Across the 59 cases the naïve reconstruction differed from the record on 557 leaf paths under favorable provenance and 1278 under unknown provenance; the rubric-governed mapping lost 0 paths in both configurations.
- **Signal-driven instability.** The naïve outcome changed between the two provenance-signal configurations in 44 of 59 cases, so its legal-facing outcome tracked provenance signal state rather than the recorded legal facts. The rubric-governed outcome was identical in both configurations.

The direction of error also flips with the signals: favorable provenance produces masking (28 false equivalences, 0 spurious escalations), while unknown provenance produces both masking of adverse facts and 16 spurious escalations of otherwise evidence-ready cases. A system of this kind is therefore not merely optimistic; it is unstable in both directions with respect to facts that the governing rule makes decisive.

One baseline case escaped masking only because the harness derived the synthetic provenance action time from the record’s own use date. A production pipeline would take that timestamp from the tool run, so the real naïve baseline would likely mask that case too. The modelling choice is conservative in the baseline’s favour and is disclosed rather than tuned away.

### 6.6 Corrected-profile mapping and round-trip coverage

| Measure | Value |
|---|---|
| Cases | 59 |
| Profiles constructed | 55 |
| Profiles failing closed on a missing Article 30(3) core field | 4 |
| Constructed cases preserving the gate outcome | 55/55 |
| Constructed cases preserving the Article 30(3) tuple | 55/55 |
| Constructed cases preserving the Article 37(1) context tuple | 55/55 |
| Constructed round-trips with zero semantic loss | 55/55 |

The four fail-closed cases are the deliberately incomplete Article 30(3) records (missing work type, work source, use purpose, or use date); the profile contract refuses to build rather than emitting a partial mapping. Fail-closed refusal is counted here as a correct outcome, not as a missing result.

### 6.7 Legacy profile 0.1.0 evidence (superseded for the corrected profile)

The following table is retained for historical completeness only. It was produced under the legacy record profile `0.1.0`, whose declared legal scope omitted Article 37(1) and now reports `declared_scope_complete=false`, and under the pre-rubric “sufficiently equivalent” criterion. **It is not corrected-profile evidence, and its five-case and delegation figures must not be read as results for profile `0.2.0`,** which are given in Sections 6.2–6.6.

| Legacy outcome (profile 0.1.0, 5 cases) | Result |
|---|---:|
| Cases with semantic loss | 0/5 |
| Changed leaf paths | 0 |
| Article 30(3) tuple preserved | 5/5 |
| PASS / REVIEW / FAIL outcome preserved | 5/5 |
| False-equivalence attacks resisted | 2/2 |

The legacy artifacts were deliberately not rewritten when the profile was corrected, and a regression test asserts that they still declare `record_version=0.1.0`. Their role in this paper is to document that the approach was feasible before it was made falsifiable, not to support any claim about the corrected pathway.

### 6.8 Real C2PA hard binding

The clean artifact produced a valid cryptographic result while its development signer remained untrusted. The tested corruptions were distinguished as follows:

| Test | Structured evidence |
|---|---|
| Clean asset | `validation_state=valid`; data-hash match; claim signature validated |
| One-byte asset mutation | `assertion.dataHash.mismatch` |
| Assertion-payload corruption | `assertion.hashedURI.mismatch` |
| Claim/signature corruption | `claimSignature.mismatch` |

The experiment demonstrates that hard binding materially strengthens evidence about artifact integrity while remaining conceptually distinct from legal meaning. It is reported as an integration test of an existing standard, not as a cryptographic contribution.

A practical integration result also emerged: during a mutation test, `c2patool` returned a structured invalid report while the process itself exited successfully. The adapter therefore parses validation semantics rather than equating process success with artifact validity.

### 6.9 Signer trust is not cryptographic validity

The clean artifact had a validated claim signature but an untrusted development signer. Adding the relevant certificate chain to a custom test trust list changed the same cryptographically valid artifact from `untrusted` to `trusted`.

That trust-policy change did not alter the IPEL acquisition status, output-permission state, or evidence-gate outcome. Trust was therefore empirically separable from both cryptographic integrity and jurisdiction-specific legal evidence in the tested system.

### 6.10 Usage preference is not a complete legal basis

In the tested profiles, a CAWG training-use signal of `allowed` did not cure either an explicit adverse acquisition status or a transformed-output scenario lacking required permission. Both remained `FAIL_EVIDENCE_GATE` under the project abstraction. The corrected-profile benchmark generalizes the point: when the naïve baseline was permitted to infer legal propositions from that signal, it masked 28 adverse or unresolved cases (Section 6.5).

The result does not imply that usage preferences are legally irrelevant. It shows that a machine-readable preference should not silently substitute for other facts that the governing legal pathway separately requires.

### 6.11 Cross-validator agreement and semantic validity

Both validation surfaces identified the same normalized corruption categories for the three attacks. This is cross-version validation within a shared implementation lineage, not independent implementation diversity.

The malformed TDM experiment further separated cryptographic validity from metadata semantics. A signed assertion containing `use=maybe` remained cryptographically valid at the artifact level, while the IPEL semantic normalizers rejected the unsupported value. A valid signature can establish integrity of the signed statement without establishing that the statement belongs to the expected semantic vocabulary.

### 6.12 Negative and unresolved results

Reported exactly as observed:

- 0/4 Article 30(3) core fields and 0/2 Article 37(1) propositions were safely delegable; the only safe delegation is a field with no legal operation in the gate.
- No candidate at all exists for either Article 37(1) proposition in the frozen registry.
- Two encoded conditions — independent protected elements, and evidence references — have no adverse state in profile `0.2.0`: the gate can escalate them to review but can never fail on them. This is an observed coverage limit of the profile, not evidence of compliance.
- Three encoded conditions — prohibited uses, the retained-record core, and profile integrity — have no unresolved state, because they are encoded as booleans or as presence/absence. The benchmark reports these absences rather than fabricating a case.
- The evidence gate did not detect 7 of 9 bad delegations.
- The naïve baseline’s single unmasked case is an artifact of a conservative modelling choice, as described in Section 6.5.

### 6.13 What Paper A does not report

| Claim | Status |
|---|---|
| IPEL improves reviewer accuracy | not tested with humans |
| IPEL reduces review time | not tested with humans |
| Independent experts confirmed the author labels | no real adjudication collected |
| Independent adjudicators verified the delegation assessments | not performed |
| Independent cryptographic implementations agreed | not established |
| The gate determines legal compliance | expressly disclaimed |
| The evidence profile has been exercised on a real, non-synthetic trace | not performed |

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

C2PA is strongest at the first two layers: binding assertions and evaluating them within a trust model. CAWG and TDM·AI communicate rights-related preferences or constraints. The jurisdiction-specific profile preserves the facts and evidence a later legal review of this pathway needs. The final application of open-textured law remains with the competent human or institution.

The contribution of Sections 6.3–6.5 is to make the last separation measurable rather than assertable. Before the rubric, “these semantics are not equivalent” was an expert opinion embedded in code; after it, the claim is the output of criteria fixed in advance, and the cost of ignoring it is quantified by the baseline.

### 7.2 Integrity is valuable even though it is not truth

The statement that “a hash does not prove legality” should not be misunderstood as minimizing cryptographic provenance. The corruption experiments show that binding and validation can expose changes that ordinary narrative documentation would not, and the integrity ablation of Section 6.1 shows what is lost when integrity is self-attested rather than externally anchored. The correct inference is narrower: integrity evidence answers whether identified content or assertions changed; it does not independently establish ownership, acquisition lawfulness, consent, licence scope, effect on normal exploitation, or legal compliance.

This distinction is consistent with C2PA’s own scope, which focuses on validation, association, formation, tamper evidence, and trust signals rather than normative value judgments (C2PA 2026).

### 7.3 Evidence architecture rather than rules-as-code maximalism

IPEL does not attempt to encode every legal condition as executable law. Formal compliance systems can be valuable where norms and facts are sufficiently determinate (Francesconi and Governatori 2023). Yet open texture, factual indeterminacy, and interpretive divergence impose limits on automatic processing (Guitton, Tamò-Larrieux, and Mayer 2023; Witt et al. 2024).

The architecture therefore automates the narrower tasks that are defensible: require specified records; preserve adverse as well as favorable facts; demand evidence bases for selected assertions; detect malformed or contradictory configurations; bind records to content and events; expose uncertainty; and route judgment-sensitive matters to review. Deference is a valid output, not a software failure.

### 7.4 Relationship to reviewability and documentation

IPEL applies the reviewability insight to a specific intellectual-property setting; it does not extend the insight itself. Cobbe, Lee, and Singh (2021) established that meaningful review requires records of the broader socio-technical process, and dataset documentation frameworks specify useful disclosures about collection, use, limitations, and provenance (Bender and Friedman 2018; Gebru et al. 2021; Pushkarna, Zaldivar, and Kjartansson 2022). What this paper adds is a test: for one enacted pathway, which of the required propositions can the available generic standards actually carry, and what happens when a system pretends they can.

This mapping also makes absence visible. The architecture does not infer facts from silence or permit a generic “licensed” label to conceal uncertainty about source, copy, date, scope, or downstream conduct.

### 7.5 Generalizability beyond Saudi Arabia

Paper A does not claim that other jurisdictions use the same copyright elements, and it does not claim that the field set is portable. The reusable contribution is a method:

1. identify the legal pathway under which an AI-development use may occur;
2. decompose it into factual, evidentiary, and evaluative conditions;
3. identify which facts must remain observable after the event;
4. define an evidence contract without encoding unsupported legal conclusions;
5. declare delegation criteria before assessing any candidate mapping;
6. delegate generic provenance functions only where those criteria pass, and retain jurisdiction-specific evidence where they do not;
7. test adversarially, against a declared baseline, whether provenance, trust, or preference signals can overwrite legal facts;
8. defer open-textured conditions to legal review; and
9. preregister human validation before claiming reviewer benefit.

Different jurisdictions will produce different field sets, thresholds, and evidence priorities, and comparative scholarship confirms that legal pathways differ substantially (de la Durantaye 2025; Sag and Yu 2025). Retention duties and privacy constraints also differ, which further limits field portability (Section 8.7). The architecture generalizes as a disciplined mapping and boundary method, not as a universal field list, and this paper offers no cross-jurisdictional evidence.

---

## 8. Threats to validity

### 8.1 Construct validity

The gate evaluates evidence readiness under a project-authored abstraction, not legal compliance. The names `PASS_EVIDENCE_GATE`, `REVIEW_REQUIRED`, and `FAIL_EVIDENCE_GATE` reduce—but cannot eliminate—the risk that users interpret the output normatively. Documentation, interface design, and governance controls remain necessary.

The benchmark also evaluates the *encoded abstraction* of the legal conditions. It measures the fidelity of the model, not the correctness of the underlying legal interpretation.

### 8.2 Assessment validity

This is the most important limitation of the central result. The rubric assessments are analyst judgements applied through a frozen classifier. The classifier is mechanical, fails closed, and was hash-locked before any outcome was observed, and every declared round-trip state is cross-checked against measured harness output. But the per-dimension `PASS`/`FAIL` calls were made by the project and have **not been independently adjudicated**. A reviewer who disagrees with a specific dimension call could in principle change a specific candidate’s decision; the delegation results should be read as reproducible under declared criteria, not as externally validated.

### 8.3 Internal validity

One record fixture is the base for all 59 corrected-profile cases, so the benchmark measures condition coverage rather than population-level variation. Two encoded conditions have no adverse state and three have no unresolved state in the profile, so the coverage matrix is complete only with respect to states the profile can express. The cryptographic attack set contains three primary corruption classes and cannot exhaust malformed manifests, parser differences, trust-store configurations, or adversarial strategies. The naïve baseline is a declared comparator built by this project and is not evidence about any deployed system.

### 8.4 Implementation validity

The two validation surfaces share c2pa-rs lineage. Different observed versions provide useful cross-version evidence, but **implementation diversity was not established**. Agreement may therefore reflect shared code paths or assumptions.

### 8.5 External validity

All completed cases are synthetic. They provide precise control over facts and avoid unauthorized corpus use, but they do not reproduce the scale, heterogeneity, changing licences, mixed ownership, incomplete records, or organizational incentives of a production training pipeline. No ecological, lawfully obtained trace has yet been executed end-to-end through the evidence profile; that absence is stated here as a substantive weakness of the empirical case rather than deferred silently to future work.

### 8.6 Legal validity

The mapping is not authoritative. Future SAIP guidance, judicial interpretation, amendments, or factual contexts may change the relevance or weight of particular fields. The architecture must therefore version legal mappings — as it did when Article 37(1) was added — and preserve the source text and interpretive assumptions on which each profile depends.

### 8.7 Evidentiary sufficiency versus minimization, confidentiality, and retention risk

A record designed to make later review possible is also a record that must be stored, secured, and eventually produced. The architecture’s bias toward preservation therefore carries costs that a purely evidentiary framing hides.

- **Sufficiency versus minimization.** Article 30(3) fixes a minimum, not a maximum. Everything the architecture retains beyond that minimum must be justified by a review proposition it actually supports; the layered model of Section 4.3 is used to prefer references and digests over retained copies wherever a reference suffices.
- **Confidentiality.** Acquisition and use records can carry commercially sensitive supplier terms, pricing, internal purposes, and personal data about the individuals who performed the acts. Evidence references can leak by pointing at material that is itself confidential.
- **Retention and legal hold.** A record retained indefinitely to satisfy one duty may conflict with retention limits arising elsewhere, and a record retained for review is discoverable in litigation — including for uses that the developer believed were permitted.
- **Access.** Because the record is designed to be produced to a competent authority on request, access control and disclosure scoping are part of the design surface, not deployment details.

Disclosure scholarship makes the general point that information which is nominally available may not be usable, and that disclosure design determines whether it is (Di Porto 2023); reviewability scholarship makes the parallel point that records must be *contextually appropriate* rather than maximal (Cobbe, Lee, and Singh 2021). The design principle this paper adopts is accordingly **minimal sufficient evidence**: retain what a declared review proposition requires, prefer a reference or digest to a copy, and treat indefinite maximal retention as a defect rather than a safety margin. This paper does not evaluate that principle empirically, and no privacy, confidentiality, or retention-risk measurement is claimed.

### 8.8 Human-study validity

No real adjudicator or reviewer data exist. Reviewer-benchmark labels were authored within the project and cannot be treated as independently validated ground truth. The adjudication and intake infrastructure prepares independent review and controlled intake but does not resolve recruitment, qualification, ethics, consent, or contamination risks.

### 8.9 Blinding and response provenance

The repository is public. Per-distribution external identifiers reduce accidental deblinding but cannot prevent a motivated participant from searching for the synthetic cases. The intake layer supplies keyed post-intake tamper evidence, not proof that a response was authored by the claimed person or remained unaltered before intake.

---

## 9. Falsification and future work

The architecture is intentionally falsifiable at technical and human-review layers.

At the technical layer, the delegation claim should be narrowed further, or abandoned, if a mature standard can encode the same jurisdiction-specific evidentiary semantics without material loss or inference. The result is bounded by the candidates in the frozen registry, by rubric version `1.0.0`, and by the specification versions tested. Future C2PA, CAWG, WIPO, or rights-management developments may supply normative semantics for propositions that currently have no candidate at all — including the two Article 37(1) propositions. The delegation experiment must therefore be re-run against later specifications rather than treated as settled, and a later re-run that returns a different ratio should be reported as such.

Independent adjudication of the per-dimension rubric calls is the most direct way to attack the central result and has not been performed. Substantial disagreement would be scientifically useful: it would identify ambiguous dimensions or candidate classes requiring a rubric revision, and the original assessments must be preserved as provenance rather than silently overwritten.

An ecological demonstration is the most significant missing empirical component. A small set of lawfully usable materials — public-domain works, openly licensed works with explicit licence terms, or controlled mock acquisitions referencing real public licences — should be run end-to-end through the evidence profile to test whether real source URLs, licence versions, nested metadata, timestamps, and evidence references can be represented without relaxing any evidentiary boundary. Until that exists, the empirical case rests entirely on synthetic condition coverage.

A broader corpus should test additional work types, acquisition pathways, licences, mixed rights, transformations, and temporal changes, and should introduce population-level variation rather than varying one fixture. A genuinely independent C2PA implementation should be added when a maintained and reproducible validator is available.

At the human-review layer, the strongest practical hypothesis remains untested. The reviewer benchmark defines a strong narrative baseline containing the same available facts as the IPEL presentation. If a properly governed study shows no meaningful improvement in missing-information detection, false-ready rate, assessment time, or inter-reviewer reproducibility, the utility claim should be weakened rather than rescued by changing the baseline or outcomes after data collection.

---

## 10. Conclusion

AI copyright infrastructure needs more than one technical layer, and the observation that it needs an evidence layer at all is not this paper’s. Dataset documentation can disclose data composition and lineage. Rights protocols can communicate usage preferences. C2PA can provide strong evidence about content bindings, assertion validity, and signer trust. Accountability scholarship established well before this work that later review requires records.

What remained open was narrower and testable: for a specific enacted pathway, how much of the legally operative record can those mature layers actually carry? Saudi Arabia’s 2026 Copyright Law supplies a pathway precise enough to answer that question, because Article 26(4), Article 37(1), and Implementing Regulation Article 30 together fix a fact-conditioned exception, a cross-cutting safeguard, and an express four-field record-retention duty.

Decomposed into an executable use-event profile and tested under criteria frozen before any outcome was observed, none of the six legally operative propositions singled out in the preregistered delegation set passed safe delegation: zero of four Article 30(3) core fields and zero of two Article 37(1) propositions were safely delegable to the tested C2PA and CAWG semantics; the one safe delegation was a descriptive title the evidence gate never reads; the gate failed to notice seven of nine bad substitutions; and a naïve mapping that delegated and inferred anyway masked adverse or unresolved legal facts in 28 of 59 cases and let its legal-facing outcome swing with provenance signal state in 44 of 59. Those numbers are bounded by a frozen candidate registry, one record fixture, synthetic data, and analyst-authored dimension calls that no independent adjudicator has yet checked.

The claim that survives is a conjunction rather than a concept: a jurisdiction-specific statutory decomposition at use-event granularity, plus executable tests of when provenance and rights semantics are not safely substitutable for legally relevant evidence propositions, with a hard boundary between technical evidence state and legal conclusion. Whether independent legal reviewers actually benefit from that structure is reserved for a separately governed human-validation study and is not answered here.

---

## Declarations

### Data and code availability

All completed experiments use synthetic records and synthetic media. The source code, schemas, generated reports, frozen benchmark materials, rubric lock manifests, and reproducibility scripts are maintained in the project repository. Legacy profile `0.1.0` artifacts are preserved unmodified alongside the corrected profile `0.2.0` artifacts. A review-anonymized archival snapshot and persistent identifier should be created before submission if required by the journal.

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

Saudi Arabia (2026a) *Copyright Law [Nizam Huquq al-Mu’allif]*, including Articles 26(4) and 37(1). *Umm Al-Qura*, 13 February 2026. Official Arabic text.

Saudi Arabia (2026b) *Implementing Regulations of the Copyright Law*, including Article 30. *Umm Al-Qura*, 31 July 2026. Official Arabic text.

Saudi Arabia (2026c) Royal Decree No. M/169 dated 14/08/1447H approving the Copyright Law. *Umm Al-Qura*, 13 February 2026.

TDM·AI (n.d.) *TDM·AI Protocol and Documentation*.

United Kingdom Government (2026) *Report on Copyright and Artificial Intelligence*. Department for Science, Innovation and Technology; Department for Culture, Media and Sport; Intellectual Property Office, 18 March 2026.

United States Copyright Office (2025) *Copyright and Artificial Intelligence, Part 3: Generative AI Training*. Washington, DC.

Abelson H, Adida B, Linksvayer M, Yergler N (2008) *ccREL: The Creative Commons Rights Expression Language*, version 1.0. Creative Commons.

IPTC (International Press Telecommunications Council) (2018) *RightsML 2.0.2*.

Krishna RAA, Shree SM, Raguram SA (2026) *Training Data Disclosure in AI Copyright Litigation: The Post-Report Provenance Procedure*. SSRN preprint, posted 20 April 2026.

Li G (2026) Auditable accountability without an AI act: Australia’s public-sector AI assurance stack and the minimum reviewable trace. *Law, Ethics & Technology* 3(3):0010. https://doi.org/10.55092/let20260010

Lucchi N (2026) *The Invisible Author: Generative AI and the Auditability Gap*. SSRN preprint. https://doi.org/10.2139/ssrn.7024098

Park Y (2025) Study on Copyright Management of AI Training Data Using NFTs and C2PA. *Journal of Industrial Property* 80:331–368. https://doi.org/10.36669/ip.2025.80.8

Qi T, Yin J, Cai D et al. (2026) Auditing unauthorized training data from AI generated content using information isotopes. *Nature Communications* 17:3007. https://doi.org/10.1038/s41467-026-68862-x

W3C (2018) *ODRL Information Model 2.2* and *ODRL Vocabulary & Expression 2.2*. W3C Recommendations.

W3C ODRL Community Group (2026) *ODRL Profile: AI Vocabulary*. Draft Community Group Report, 17 August 2026.

Xie Y, Song J, Wang H, Song M (2025) Training Data Provenance Verification: Did Your Model Use Synthetic Data from My Generative Model for Training? In: *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp 23817–23827.

WIPO (World Intellectual Property Organization) (2026) *AI Infrastructure Interchange (AIII)*.

Witt A, Huggins A, Governatori G et al. (2024) Encoding legislation: a methodology for enhancing technical validation, legal alignment and interdisciplinarity. *Artificial Intelligence and Law* 32:293–324. https://doi.org/10.1007/s10506-023-09350-1
