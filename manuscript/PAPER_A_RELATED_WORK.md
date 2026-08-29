# Paper A — Related Work and Novelty Positioning

## 1. Doctrinal AI-training copyright scholarship

A large and rapidly growing literature asks whether copying copyrighted works for model development is permitted, under which exceptions, and how licensing, fair use/fair dealing, text-and-data-mining exceptions, rightsholder reservations, remuneration and transparency should apply. That literature is necessary to identify substantive legal conditions, but Paper A asks a different systems question:

> Once a legal regime makes an AI-development use depend on facts such as lawful acquisition, source, purpose, timing, proportionality, rights reservation, or downstream use, what evidence must a development pipeline preserve so those facts remain reconstructable later?

This is an **observability/evidence** problem rather than a new universal theory of AI-training legality.

Recent comparative scholarship makes the jurisdictional variation explicit. De la Durantaye (2025) compares AI-training exceptions and policy debates across the United States, Canada, the United Kingdom, European Union, Israel, China, Singapore and Japan, showing that control, compensation, transparency and legal certainty are calibrated differently. Ginsburg (2025) discusses the still-contested US fair-use treatment of AI inputs; Tyagi (2024) examines EU text-and-data-mining and generative AI; Kretschmer et al. (2025) analyse UK opt-in/opt-out policy; and Bruni (2026) examines the first US federal AI-training fair-use decisions.

These studies reinforce rather than displace Paper A's premise: the substantive rule changes across jurisdictions, so a technical system should not hard-code one jurisdiction's legality conclusion as if it were universal. What may generalize is a **method for turning the applicable rule into an evidence-preservation problem**.

Saudi Arabia's 2026 Copyright Law makes the distinction unusually concrete. Article 26(4) conditions AI-development copying on lawful publication, lawful acquisition of the original copy, and purpose-limited copying. Implementing Regulation Article 30 adds further constraints and expressly requires the developer to retain records of work type, source, purpose and date of use.

Paper A treats that legal testbed as a source of machine-observable requirements while preserving open-textured issues for human/legal judgment.

Official sources:
- Saudi Copyright Law: https://www.uqn.gov.sa/details?p=28845
- Royal Decree M/169: https://www.uqn.gov.sa/decisions-and-regulations/4000304
- Implementing Regulations: https://www.uqn.gov.sa/decisions-and-regulations/4001498

Comparative anchors:
- de la Durantaye (2025), *Control and Compensation*: https://link.springer.com/article/10.1007/s40319-025-01569-6
- Ginsburg (2025), *AI inputs, fair use and the US Copyright Office Report*: https://academic.oup.com/jiplp/article/20/8/521/8221808
- Tyagi (2024), *Copyright, text & data mining and the innovation dimension of generative AI*: https://academic.oup.com/jiplp/article/19/7/557/7624901
- Kretschmer et al. (2025), *Copyright and AI in the UK: Opting-In or Opting-Out?*: https://academic.oup.com/grurint/article/74/11/1055/8209765
- Bruni (2026), *Training on Trial*: https://copyrightsociety.org/journal-entries/training-on-trial-insights-from-bartz-and-kadrey/

## 2. Dataset provenance and licensing audits

Longpre et al.'s Data Provenance Initiative demonstrates that the AI data ecosystem suffers from serious lineage, attribution, and licensing-documentation problems. The published Nature Machine Intelligence study audits more than 1,800 datasets and reports high rates of missing and inconsistent license information. It contributes dataset-level lineage tracing, source/license audit methods, and provenance cards.

IPEL is complementary rather than substitutive:

| Data provenance audit | IPEL |
|---|---|
| asks where datasets/data came from | asks what evidence exists for a legally relevant use event |
| traces source, creator, license and lineage | captures source plus jurisdiction-specific review facts |
| primarily dataset/collection-oriented | work/use-event oriented when work-level provenance exists |
| improves documentation and attribution | separates evidence sufficiency from legal judgment |
| does not purport to prove legal compliance | explicitly refuses to do so as well |

The key novelty is not “more provenance metadata”; it is the legal-to-evidence mapping and the machine-enforced boundary preventing metadata from silently becoming a legal conclusion.

Reference:
- Longpre et al. (2024), *A large-scale audit of dataset licensing and attribution in AI*, Nature Machine Intelligence. https://www.nature.com/articles/s42256-024-00878-8

## 3. Machine-readable rightsholder preferences: CAWG and TDM·AI

CAWG's Training and Data Mining Assertion and the TDM·AI protocol address a different infrastructure need: communicating whether a rightsholder permits, restricts, or reserves certain automated-processing or training uses.

CAWG 1.1 enables a human actor to place a signed assertion in C2PA metadata indicating whether an asset may be used in a training or data-mining workflow. TDM·AI similarly focuses on machine-readable usage preferences and explicitly distinguishes public opt-out/permission declarations from negotiated licensing.

These protocols answer questions like:

> What preference or restriction has been expressed for this asset?

IPEL asks:

> What evidence exists that this developer's particular use satisfied the facts required by the governing legal pathway?

A preference signal can be relevant evidence, but it is not automatically equivalent to lawful acquisition, publication status, license scope, necessity, market effect, or downstream permission. This distinction is especially important in legal systems where a rights reservation is only one element of the applicable rule. The Stage-003 to Stage-005 tests therefore deliberately prevent `allowed` or `trusted` metadata from overwriting jurisdiction-specific legal-evidence fields.

Official sources:
- CAWG Training and Data Mining Assertion 1.1: https://cawg.io/training-and-data-mining/1.1/
- TDM·AI protocol: https://docs.tdmai.org/
- TDM·AI on opt-out vs licensing: https://docs.tdmai.org/opt-out-opt-in-and-content-licensing

## 4. Cryptographic content provenance: C2PA

C2PA provides a mature technical standard for content provenance and authenticity. Its current specification supports ingredients and hashed references, including AI/ML inputs and training-related provenance. The AI/ML guidance also discusses Content Credentials for training datasets and model-development workflows.

Paper A does not propose a rival cryptographic provenance standard. Stages 003–005 instead ask which IPEL facts can safely be delegated to C2PA and whether cryptographic integrity/trust can be kept separate from legal meaning.

The experiments produce three relevant findings:

1. the tested Article 30(3) core fields were not safely delegated in the Stage-003 mapping (0/4);
2. actual C2PA hard binding detected the tested asset/assertion/signature corruptions in Stage 004;
3. cryptographic validity, signer trust, and metadata-semantic validity remained distinct in Stage 005.

This yields a layered model:

```text
C2PA / content provenance
        ↓ supplies integrity evidence
IPEL / jurisdiction-specific evidence profile
        ↓ organizes legally relevant facts
human/legal reviewer
        ↓ applies open-textured legal judgment
legal conclusion
```

C2PA source:
- C2PA Specifications 2.4: https://spec.c2pa.org/specifications/
- C2PA Ingredient v3 / AI inputs: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html

## 5. WIPO and IP infrastructure

WIPO's 2026 AI Infrastructure Interchange (AIII) treats metadata, digital identifiers, authentication tools, watermarking, rights-management systems, content recognition and distribution frameworks as an infrastructure layer that must adapt to AI. WIPO explicitly frames AIII as technical/operational dialogue rather than lawmaking.

This framing supports Paper A's central distinction: substantive IP rules and technical infrastructure are related but different layers. IPEL is positioned as a research prototype for one missing infrastructure problem—**post-hoc legal-evidence observability**—not as a policy standard endorsed by WIPO.

Source:
- WIPO AIII: https://www.wipo.int/en/web/ai-infrastructure-interchange

## 6. Computational law, law by design, and open texture

Artificial Intelligence and Law has a long tradition of studying computational models of legal rules, legal reasoning, and the consequences of making regulation machine-processable. More recent research emphasizes open-texture: legal terms can be vague, evaluative, or under-specified and therefore resist naïve automation.

A parallel “law by design” / “compliance by design” literature asks how legal goals should shape technical systems across their lifecycle. Djeffal (2025) identifies documentation, compliance roles, enforcement and technical/organisational measures as recurring features of law-by-design obligations. Regulation-by-design scholarship also warns that embedding law in technology creates contextual and methodological limits. Recent work on enforceable algorithmic transparency similarly frames technical evidence and auditability as prerequisites for later legal scrutiny.

IPEL sits adjacent to this literature but adopts a deliberately narrower posture. It does **not** try to hardwire the full legal outcome into the system. Instead, it treats evidence preservation itself as the design objective. The architecture therefore distinguishes:

- facts that can be structurally required or contradicted by a record;
- facts requiring referenced evidence;
- open-textured assessments that remain `REVIEW` rather than being fabricated by code.

This distinction is important because “compliance by design” can otherwise be read as if successful technical translation eliminates the need for legal interpretation. IPEL's contribution is closer to **reviewability by design** or **evidentiary observability by design**: preserve what a later reviewer needs, bind what can be bound, and leave normative questions visible rather than silently resolving them.

Relevant literature:
- Guitton, Tamò-Larrieux & Mayer, *Mapping the Issues of Automated Legal Systems: Why Worry About Automatically Processable Regulation?* https://link.springer.com/article/10.1007/s10506-022-09323-w
- Guitton et al., *Identifying open-texture in regulations using LLMs*. https://link.springer.com/article/10.1007/s10506-025-09450-0
- Bench-Capon, *Thirty years of Artificial Intelligence and Law: Editor's Introduction*. https://link.springer.com/article/10.1007/s10506-022-09325-8
- Djeffal, *Law by design obligations: The future of regulating digital technologies in Europe?* https://doi.org/10.1016/j.clsr.2025.106232
- *Regulation by Design: Features, Practices, Limitations, and Governance Implications*. https://link.springer.com/article/10.1007/s11023-024-09675-z
- *Making algorithmic transparency enforceable: sufficient intelligibility, technical evidence, and auditability across the EU and the US*. https://doi.org/10.1093/ijlit/eaag008

## 7. Novelty claim after expanded related-work review

The defensible novelty claim is deliberately narrow:

> Existing work separately addresses substantive AI-training copyright doctrine, dataset lineage and license documentation, machine-readable rightsholder preferences, cryptographic content provenance, and compliance/law-by-design. Paper A contributes a tested **jurisdiction-specific legal-evidence layer** that maps fact-conditioned copyright rules into observable evidence requirements and enforces semantic barriers so provenance, trust, and preference signals cannot silently become legal conclusions.

A second way to express the contribution is:

> The architecture shifts the technical objective from “automate the legal answer” to “make the legally relevant facts reconstructable and contestable.”

The paper does **not** claim:

- the first provenance system for AI;
- the first machine-readable copyright protocol;
- the first C2PA use in AI;
- automated copyright compliance;
- universal cross-jurisdiction copyright semantics;
- that evidence preservation eliminates legal interpretation.

## 8. Generalization hypothesis

The cross-jurisdiction hypothesis should be framed methodologically:

1. identify a legally available use pathway;
2. decompose it into factual and evaluative conditions;
3. map factual conditions to evidence candidates;
4. separate assertion, referenced evidence, content binding and event binding;
5. reuse generic provenance standards where semantics genuinely match;
6. retain jurisdiction-specific facts where they do not;
7. fail closed or defer where legal judgment remains open-textured.

Whether another jurisdiction needs the same fields is an empirical/legal question. The reusable contribution is the decomposition method and boundary discipline, not the Saudi field list itself.
