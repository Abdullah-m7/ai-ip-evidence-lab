# From Copyright Exception to Verifiable Evidence: An Evidence Architecture for AI Development under Saudi Arabia’s 2026 Copyright Law

## Abstract

Copyright rules governing artificial-intelligence development are often discussed as questions of permission: whether model developers may copy protected works, which exceptions apply, and when licences or rightsholder reservations control. A separate problem arises after a legally relevant use has occurred: can a developer or reviewer reconstruct the facts on which the legal pathway depended? Saudi Arabia’s 2026 Copyright Law creates a useful testbed because Article 26(4) permits copying an original work for AI product and algorithm development subject to fact-sensitive conditions, while Article 30 of the Implementing Regulations adds operational restrictions and expressly requires developers to retain records of the work type, source, purpose of use and date of use. This paper introduces IPEL, a jurisdiction-specific intellectual-property evidence layer designed to preserve such facts without turning technical provenance into an automated legal conclusion. We map the Saudi provisions into an evidence contract, distinguish observable facts from open-textured legal assessments, and test interoperability with machine-readable usage preferences and C2PA content provenance. In a five-case semantic round-trip experiment, the tested profile preserved all leaf values and evidence-gate outcomes, while none of the four Article 30(3) core fields was delegated to C2PA as a semantically equivalent substitute. A real C2PA hard-binding experiment detected tested asset, assertion and claim-signature corruptions and showed that cryptographic validity and signer trust are distinct. A cross-validator experiment reproduced the three tested corruption categories across two validation surfaces using different observed c2pa-rs versions, while explicitly not establishing implementation diversity. Across the experiments, CAWG training-use signals and C2PA trust states were prevented from overwriting jurisdiction-specific evidence such as acquisition status or output permission. The contribution is therefore not automated copyright compliance, but an evidentiary architecture and a falsifiable method for separating content provenance, usage signaling, legal-evidence observability and human legal judgment.

**Keywords:** AI training; copyright; provenance; legal evidence; C2PA; computational law; Saudi Arabia; intellectual property; auditability

---

## 1. Introduction

The copyright debate around artificial-intelligence development has concentrated on a difficult substantive question: when may protected works be copied for model development or training? Different legal systems answer that question through combinations of exclusive rights, exceptions, text-and-data-mining rules, fair-use or fair-dealing doctrines, licences, and rightsholder reservations. Technical initiatives have developed alongside that debate. Dataset-provenance work traces the sources and licences of AI data; machine-readable protocols communicate rightsholder preferences about automated processing or training; and content-provenance standards cryptographically bind claims to digital assets.

These efforts address important but non-identical problems. A further problem appears when a legal pathway depends on facts that must be reconstructed later. A rule may ask whether a work was lawfully acquired, why it was copied, when it was used, how much was needed, whether downstream distribution occurred, or whether a use prejudiced the normal exploitation of a work. Even if the applicable law is known, a later reviewer cannot apply it reliably if the development pipeline did not preserve the relevant facts and their supporting evidence.

This paper calls that problem **evidentiary observability**: the ability to reconstruct legally relevant facts about an AI-development use event after the event has occurred. The problem is narrower than legal compliance and broader than generic data lineage. It asks what evidence an engineering process must preserve so that legal review remains possible without pretending that cryptographic integrity, metadata, or machine-readable preferences resolve open-textured legal questions.

Saudi Arabia’s new Copyright Law provides an unusually explicit testbed. Article 26(4) of the 2026 Copyright Law permits copying an original work for the development of AI products and algorithms subject to conditions concerning lawful publication, lawful acquisition of the original copy, and copying limited to what serves the purpose. The Implementing Regulations then specify additional constraints. Article 30(3), in particular, requires the developing entity to retain records showing the type of work, its source, the purpose of use and the date of use, and to provide those records to a competent authority considering a related dispute upon request. Article 30 also contains conditions that are more evaluative, including necessity, normal exploitation, legitimate author interests, prohibited downstream uses and independently protected elements.

The combination is important computationally. Some requirements are record-like: a date or source can be required structurally. Others are evidentiary: a statement that acquisition was lawful may require a receipt, licence or other external support. Still others are open-textured: whether a commercial use affects normal exploitation cannot safely be reduced to a Boolean field supplied by the developer. A system that treats all three categories alike either becomes too weak to be useful or overclaims legal certainty.

We introduce **IPEL (Intellectual-Property Evidence Ledger)** as a research architecture for this boundary. IPEL is not a copyright oracle and does not predict court outcomes. It models an AI-development **use event** and stores jurisdiction-specific facts and evidence references that a later reviewer may need. Its validation gate distinguishes explicit contradictions from evidentiary uncertainty and deliberately returns review-required states where the legal condition is not machine-resolvable.

We make four contributions.

First, we present a legal-to-evidence decomposition method using Saudi Arabia’s 2026 AI-development copying rule as the testbed. The method separates factual observability from normative judgment and treats the Article 30(3) four-field record tuple as a minimum retention core rather than a complete compliance record.

Second, we test whether mature provenance infrastructure can substitute for the jurisdiction-specific evidence layer. A semantic round-trip experiment shows that generic provenance and the Saudi evidentiary tuple overlap less than a superficial metadata comparison suggests.

Third, we conduct real C2PA hard-binding and adversarial validation experiments. These demonstrate the value of cryptographic provenance while also exposing boundaries between artifact integrity, signer trust, metadata semantics and legal evidence.

Fourth, we define a falsifiable future human-validation path. A balanced reviewer benchmark, independent-adjudication protocol, preregistration lock and contamination-resistant distribution/intake pipeline have been implemented, but **no human-effect result is claimed in this paper**.

The central claim is therefore deliberately bounded: a legal-evidence layer can complement provenance and rights-signaling standards by preserving jurisdiction-specific facts and preventing technical trust signals from silently becoming legal conclusions.

---

## 2. Legal testbed: Saudi Arabia’s 2026 Copyright Law

### 2.1 Article 26(4)

Saudi Arabia adopted a new Copyright Law in 2026 through Royal Decree No. M/169. Article 26(4) permits, without the ordinary authorization mechanism, copying an original work for the purpose of developing AI products and algorithms when the work was lawfully published, ownership of the original copy was lawfully obtained, and the copying remains within what serves the purpose. The official Arabic text is the authoritative source; English descriptions in this paper are analytical paraphrases.

For an evidence architecture, Article 26(4) creates at least three different types of question:

1. **publication status** — a factual/legal state that may require evidence external to the copied bytes;
2. **acquisition status** — a fact about how the developer obtained the relevant copy, also requiring external support;
3. **purpose and scope** — a partly factual and partly evaluative question concerning why and how much was copied.

A content digest can identify bytes but cannot establish any of these propositions by itself.

### 2.2 Implementing Regulation Article 30

Article 30 of the Implementing Regulations applies when a work is copied for AI-product or algorithm development under Article 26(4). It contains six groups of controls.

Article 30(1) limits copying and analysis to what is necessary for AI-development purposes and excludes republication, distribution and direct commercial exploitation under the exception. Article 30(2) addresses purely commercial use and connects permissibility to materiality and normal exploitation. Article 30(3) creates a record-retention obligation. Article 30(4) addresses unjustified harm to legitimate author interests and the opportunity to exploit or obtain material return. Article 30(5) restricts transformation, republication, public availability and unnecessary inclusion in final products absent permission or public-domain status. Article 30(6) requires respect for separately protected elements contained in the work.

The project’s legal-to-evidence matrix maps these provisions into three machine-handling classes:

- **structural factual requirements**, where absence can be detected directly;
- **evidence-supported factual assertions**, where a value without a basis remains uncertain;
- **judgment-sensitive conditions**, which require legal/economic assessment and should not be converted into developer self-attestation.

This is a research abstraction, not an authoritative interpretation by the Saudi Authority for Intellectual Property or a court.

### 2.3 The Article 30(3) record core

Article 30(3) expressly requires records identifying:

```text
(work type, source, purpose of use, date of use)
```

We call this the **Article 30(3) core tuple**. It is particularly useful scientifically because the rule itself identifies concrete information that must survive the development process. But the tuple is not sufficient to determine whether the use was lawful. A complete record can document an adverse fact—for example, an acquisition known to be unlawful. This distinction later becomes important in the benchmark design: **evidence readiness is not a favorable legal outcome**.

---

## 3. Related work and the missing evidence layer

### 3.1 Dataset lineage and licence documentation

The Data Provenance Initiative demonstrates why provenance is a first-order AI-governance problem. Longpre et al. audit more than 1,800 text datasets, tracing source, creator, licences and downstream use, and report widespread missing and inconsistent licensing information. Their work provides dataset-lineage methods and provenance cards that materially improve the transparency of AI-data supply chains.

IPEL addresses a different unit of analysis. Where work-level provenance exists, it models an identifiable use event: one work or work unit used for a declared AI-development purpose at a given time. The aim is not only to know where a dataset came from, but to preserve the facts required to review a specific legally relevant use pathway.

### 3.2 Machine-readable usage preferences

CAWG’s Training and Data Mining Assertion 1.1 enables a human actor to communicate, within the C2PA ecosystem, information about whether an asset may be used in a data-mining or AI/ML-training workflow. TDM·AI similarly provides machine-readable usage preferences and expressly distinguishes public opt-out or permission declarations from negotiated licensing arrangements.

Such signals can be valuable evidence. They do not, however, answer every question a legal exception may ask. A declaration that training is `allowed` does not itself establish how a particular developer acquired a copy, whether a separate contract applied, whether an output use exceeded permission, or whether another jurisdiction-specific condition was met. Paper A therefore treats rights signaling as an input to an evidence system rather than a complete legal basis.

### 3.3 Content provenance and C2PA

C2PA provides technical standards for certifying the source and history of digital content. Version 2.4 supports Ingredient assertions and hashed references, including cases in which assets or data are inputs to AI/ML processes. Its AI/ML guidance discusses training datasets and model-development workflows.

Rather than create a rival provenance standard, IPEL attempts to delegate generic provenance functions to C2PA where semantics actually match. The key research question is what remains jurisdiction-specific after that delegation.

### 3.4 Computational law and open texture

Research in *Artificial Intelligence and Law* has long examined computational models of law and the risks of automatically processable regulation. Guitton and colleagues emphasize that open-textured terms—vague, evaluative or under-specified concepts—create obstacles to automatic processing. IPEL applies that insight architecturally: it does not force every legal condition into a binary variable. The system can require a record, identify an explicit contradiction, or flag a matter for review without fabricating the final legal judgment.

### 3.5 Novelty position

Existing work separately addresses substantive AI-training copyright doctrine, dataset provenance, machine-readable preferences and cryptographic content provenance. IPEL contributes a **jurisdiction-specific legal-evidence layer** between those technical systems and the later legal reviewer. Its novelty lies in the decomposition method and enforced semantic boundaries, not in claiming the first provenance system or the first machine-readable copyright protocol.

---

## 4. IPEL design

### 4.1 Unit of analysis

The unit is an **AI-development use event** rather than an entire model or dataset. A use event identifies the work or work unit, its source and content identity, the declared purpose and time of use, and supporting evidence about acquisition, publication and downstream handling.

This granularity is intentional. A dataset-level licence label may not reveal whether different constituent works were obtained from different sources or under different conditions.

### 4.2 Evidence layers

The legal-to-evidence matrix distinguishes progressively stronger evidence:

- **L0 — assertion:** a person or process records a value;
- **L1 — referenced assertion:** the value points to a licence, receipt, archive event or policy;
- **L2 — content-bound evidence:** the referenced artifact is cryptographically identified;
- **L3 — event-bound evidence:** artifact, actor, work digest and time are connected to a use event;
- **L4 — tamper-evident evidence:** later modification is detectable through chained or signed integrity mechanisms.

The crucial point is epistemic: moving upward strengthens the evidence that a record or artifact has not changed. It does not automatically make the proposition legally true.

### 4.3 Gate semantics

The deterministic evidence gate uses three broad outcomes:

- `PASS_EVIDENCE_GATE` — the tested contract contains no hard contradiction or unresolved evidence condition in the project’s abstraction;
- `REVIEW_REQUIRED` — the record contains unresolved or judgment-sensitive matters;
- `FAIL_EVIDENCE_GATE` — the record has a structural deficiency or an explicit adverse contradiction under the tested rule abstraction.

`PASS_EVIDENCE_GATE` is deliberately not named “LEGAL” or “COMPLIANT”. The validator output also marks `legal_conclusion=false`.

This naming is substantive, not cosmetic. An automated system can check that `work.source` is absent. It cannot infer that a particular market effect is legally acceptable simply because the developer wrote `none`.

---

## 5. Methods

### 5.1 Legal-to-evidence mapping

We manually decomposed Article 26(4) and Implementing Regulation Article 30 into conditions and candidate evidence. Requirements were classified according to whether absence/contradiction could be detected structurally, whether external evidence was needed, and whether the condition remained judgment-sensitive.

The resulting contract was implemented as a machine-readable schema and deterministic validation gate. Synthetic cases were used to test missing fields, adverse acquisition/publication states, prohibited distribution, uncertain proportionality, market-effect assertions without a basis, downstream inclusion, independent protected elements and contradictory evidence.

### 5.2 Stage 003: semantic interoperability

We constructed five synthetic cases:

1. a clean case;
2. an unverified-publication case;
3. a prohibited-distribution case;
4. a case with a trusted/allowed provenance signal but explicit unlawful acquisition;
5. a trusted/allowed signal combined with missing output permission.

Each case was encoded into a C2PA-aligned intermediate profile and reconstructed into the IPEL review model. We compared every original leaf value, the Article 30(3) core tuple, the evidence-gate outcome and duplicated generic fields.

The intermediate representation was expressly not described as a conformant C2PA Manifest.

### 5.3 Stage 004: real C2PA hard binding

We then generated a real C2PA Manifest in a synthetic JPEG using pinned `c2patool 0.27.16`. Three corruptions were introduced:

- a one-byte mutation to the bound asset;
- corruption of an assertion payload;
- corruption affecting claim-signature material.

The adapter parsed structured validation results rather than relying on the command-line exit code. We also tested the effect of CAWG `allowed` signals on explicitly adverse IPEL legal-evidence facts.

### 5.4 Stage 005: cross-validator and trust boundary

A second validation surface was built from the C2PA conformance CLI. The historical dependency graph could not be reproduced literally because a historical submodule source was no longer available; the project records a bounded compatibility repair and does not label it exact upstream reproduction.

The two validation surfaces used different observed c2pa-rs versions (0.90.16 and 0.78.0). We compared normalized cryptographic outcomes for the three corruption classes, changed the trust configuration for the same valid artifact, tested legal-evidence invariance under that trust change, and submitted a signed TDM assertion containing the unsupported value `maybe`.

Because both validation surfaces share c2pa-rs lineage, the study explicitly records `IMPLEMENTATION_DIVERSITY_NOT_ESTABLISHED`.

### 5.5 Future human validation

Stages 006–008 implement but do not execute a human-study path. Stage 006 creates 24 latent synthetic cases with exact factual parity between a strong narrative baseline and IPEL presentation. Stage 007 freezes an independent-adjudication protocol and prevents synthetic data from being promoted into a real study lock. Stage 008 produces per-distribution external IDs and keyed post-intake integrity infrastructure.

These artifacts make later claims falsifiable but supply **no human-effect result** to Paper A.

---

## 6. Results

### 6.1 Semantic round-trip

Across the five committed Stage-003 benchmark cases, reconstruction produced:

| Outcome | Result |
|---|---:|
| Cases with semantic loss | 0/5 |
| Changed leaf paths | 0 |
| Article 30(3) tuple preserved | 5/5 |
| PASS / REVIEW / FAIL outcome preserved | 5/5 |
| False-equivalence attacks resisted | 2/2 |

The main negative finding was more important than metadata reuse: **0/4 Article 30(3) core fields were delegated to C2PA in the tested mapping**. Work type, source, purpose of use and date of use remained in the jurisdiction-specific layer because the closest generic fields were not treated as safe semantic substitutes under the tested profile.

This is not a theorem that C2PA can never carry such information. It is a finding about the semantics of the tested mapping and the decision not to replace legally specified evidence fields with superficially similar provenance fields.

### 6.2 Real C2PA hard binding

The Stage-004 artifact produced a valid cryptographic result while its development signer remained untrusted. The three corruption classes were detected distinctly:

| Test | Structured evidence |
|---|---|
| Clean asset | `validation_state=valid`; data-hash match; claim signature validated |
| One-byte asset mutation | `assertion.dataHash.mismatch` |
| Assertion corruption | `assertion.hashedURI.mismatch` |
| Claim/signature corruption | `claimSignature.mismatch` |

This experiment demonstrates that cryptographic integrity materially strengthens the evidence architecture while remaining conceptually distinct from legal meaning.

A practical integration finding also emerged: during a mutation test, `c2patool` returned a structured invalid result while the process itself exited successfully. The adapter therefore parses validation semantics instead of equating command success with artifact validity.

### 6.3 Trust is not cryptographic validity

The clean Stage-004 artifact had a validated claim signature but an untrusted development signer. In Stage 005, adding the relevant certificate chain to a custom test trust list changed the trust classification of the same cryptographically valid artifact from untrusted to trusted.

That change did not alter the IPEL acquisition status, output-permission state or evidence-gate outcome. Trust policy was therefore empirically separable from both cryptographic integrity and jurisdiction-specific legal evidence.

### 6.4 Usage preference is not a complete legal basis

In the tested profiles, a CAWG training-use signal of `allowed` did not cure either:

- an explicit `acquisition_status=false`; or
- a transformed-output scenario lacking required permission.

Both cases remained `FAIL_EVIDENCE_GATE` in the relevant project abstraction.

The result should be interpreted narrowly. It does not say that usage preferences are legally irrelevant. It shows that a machine-readable preference signal should not be silently substituted for other legally relevant facts that the governing pathway separately requires.

### 6.5 Cross-validator and semantic validity

Both Stage-005 validation surfaces identified the same normalized corruption categories for the three Stage-004 attacks. This is cross-version validation within a shared implementation lineage, not independent implementation diversity.

The malformed TDM experiment further separated cryptographic validity from metadata semantics. A signed assertion containing `use=maybe` remained cryptographically valid at the artifact level, while the IPEL semantic normalizers rejected the unsupported value. A valid signature can therefore establish integrity of the signed statement without establishing that the statement belongs to the expected semantic vocabulary.

---

## 7. What provenance can and cannot prove

The experiments support a layered interpretation of technical evidence.

### 7.1 Provenance can support identity and integrity propositions

A cryptographic binding can help answer questions such as:

- are these the bytes to which the claim referred?
- did a bound assertion change?
- did the claim-signature material change?
- is a signer trusted under the selected trust policy?

These are valuable evidentiary propositions.

### 7.2 Provenance does not automatically prove legal facts

A digest does not itself show that a copy was lawfully acquired. A trusted signer does not determine whether an exception applies. A rights preference does not necessarily establish a negotiated licence or resolve every downstream-use question. A signed self-assessment that market harm is absent remains a self-assessment unless supported by an appropriate basis.

This distinction is the reason IPEL retains jurisdiction-specific fields and evidence references even when content provenance is cryptographically strong.

### 7.3 Legal evidence does not eliminate legal judgment

Conversely, better evidence does not make every legal condition computable. Article 30 contains concepts such as necessity, normal exploitation and unjustified prejudice. A system may preserve the facts relevant to those assessments and identify missing inputs, but Paper A does not claim to replace the legal decision-maker.

The architecture therefore treats **deference to review** as a valid system output rather than a failure of automation.

---

## 8. Generalizability beyond Saudi Arabia

Paper A does not claim that other jurisdictions use the same copyright elements. The generalizable contribution is a method.

For another legal regime, the method is:

1. identify the legal pathway under which an AI-development use may occur;
2. decompose the pathway into factual, evidentiary and evaluative conditions;
3. identify which factual conditions must be observable after the event;
4. define an evidence contract without encoding unsupported legal conclusions;
5. delegate generic provenance functions to mature standards when semantics match;
6. retain jurisdiction-specific evidence where they do not;
7. test adversarially whether provenance/trust/preference signals can overwrite legal facts;
8. defer open-textured conditions to human/legal review;
9. preregister empirical validation before claiming human-review benefits.

Different jurisdictions may produce different field sets, different risk classifications and different evidence thresholds. That variability is expected. The reusable result is the architecture for preserving the boundary between technical evidence and legal judgment.

The approach may also extend beyond copyright. Other domains—data protection, product safety, regulated AI, consumer law or evidence-heavy administrative compliance—often contain rules that depend on reconstructable operational facts while retaining open-textured normative conditions.

---

## 9. Limitations

First, the legal mapping is a research abstraction. It is not an authoritative interpretation by SAIP or a Saudi court, and future interpretation, guidance or case law may change the evidentiary significance of particular fields.

Second, the completed empirical results are synthetic and technical. The paper does not yet show that human reviewers are more accurate, faster or more consistent when using IPEL.

Third, the Stage-003 semantic benchmark is small. The finding that 0/4 core fields were delegated is limited to the tested profile and should not be generalized into an impossibility claim about C2PA extension mechanisms.

Fourth, Stage 005 provides cross-version validation on two surfaces sharing c2pa-rs lineage. **Implementation diversity was not established.** A genuinely independent validator would strengthen the result.

Fifth, integrity does not prove truth. Even a tamper-evident record can faithfully preserve a false assertion. The architecture therefore distinguishes referenced evidence and review from bare self-attestation.

Sixth, the future adjudication and human-review study requires real recruitment, qualification checks, an applicable ethics/consent determination and independent participants. The repository currently records these as unresolved and contains no human effect size.

Finally, the public repository limits blinding. Stage 008 reduces accidental deblinding through per-distribution identifiers and private mappings but does not make public synthetic facts secret from a motivated participant.

---

## 10. Falsification path

The architecture is intentionally falsifiable in two ways.

At the technical layer, the novelty claim should be narrowed if an existing mature standard can encode the same jurisdiction-specific evidentiary semantics without material loss or false equivalence. Future C2PA or rights-infrastructure developments may therefore reduce the need for a separate profile.

At the human-review layer, the project’s strongest practical claim remains untested. Stage 006 defines a strong baseline containing the same underlying facts as IPEL. If a properly governed reviewer study shows no meaningful improvement in missing-information detection or review reproducibility, the utility claim should be weakened rather than rescued by changing the baseline or endpoints after data collection.

This negative-result posture is important. IPEL’s value cannot rest on the fact that it is structured; it must eventually demonstrate that the structure changes a relevant review outcome or lowers a real evidentiary risk.

---

## 11. Conclusion

AI copyright infrastructure needs more than one technical layer. Dataset lineage can reveal where data came from. Rights protocols can communicate usage preferences. C2PA can provide strong evidence about content provenance, bindings and signer trust. None of those functions is identical to preserving the jurisdiction-specific facts required for later legal review.

Saudi Arabia’s 2026 Copyright Law makes this distinction concrete by combining a fact-conditioned AI-development copying pathway with an express record-retention rule. IPEL operationalizes that problem as an evidence architecture rather than an automated compliance oracle.

The experiments show three boundaries that should remain visible in AI governance systems:

```text
cryptographic integrity ≠ signer trust
signer trust ≠ metadata semantic validity
metadata / preference signals ≠ legal conclusion
```

The proposed architecture sits between those layers. It preserves evidence, reuses mature provenance infrastructure where semantics match, refuses false equivalence where they do not, and defers open-textured judgment rather than fabricating it.

The next empirical question is no longer whether the architecture can be implemented. It is whether independent legal reviewers actually benefit from it. That question is preregistered for a separate human-validation study and is not answered by the present paper.

---

## References — working list

See `manuscript/PAPER_A_REFERENCES.md`. Primary sources include the Saudi Copyright Law and Implementing Regulations published by Umm Al-Qura; C2PA 2.4; CAWG Training and Data Mining Assertion 1.1; TDM·AI; WIPO AIII; Longpre et al. (2024); and computational-law work on automatically processable regulation and open texture.
