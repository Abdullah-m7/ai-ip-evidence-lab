# Paper A — Related Work and Novelty Positioning

## 1. Doctrinal AI-training copyright scholarship

A large and rapidly growing literature asks whether copying copyrighted works for model development is permitted, under which exceptions, and how licensing, fair use/fair dealing, text-and-data-mining exceptions, and rightsholder reservations should apply. That literature is necessary to identify substantive legal conditions, but Paper A asks a different systems question:

> Once a legal regime makes an AI-development use depend on facts such as lawful acquisition, source, purpose, timing, proportionality, or downstream use, what evidence must a development pipeline preserve so those facts remain reconstructable later?

This is an **observability/evidence** problem rather than a new universal theory of AI-training legality.

Saudi Arabia's 2026 Copyright Law makes the distinction unusually concrete. Article 26(4) conditions AI-development copying on lawful publication, lawful acquisition of the original copy, and purpose-limited copying. Implementing Regulation Article 30 adds further constraints and expressly requires the developer to retain records of work type, source, purpose and date of use.

Paper A treats that legal testbed as a source of machine-observable requirements while preserving open-textured issues for human/legal judgment.

Official sources:
- Saudi Copyright Law: https://www.uqn.gov.sa/details?p=28845
- Royal Decree M/169: https://www.uqn.gov.sa/decisions-and-regulations/4000304
- Implementing Regulations: https://www.uqn.gov.sa/decisions-and-regulations/4001498

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

A preference signal can be relevant evidence, but it is not automatically equivalent to lawful acquisition, publication status, license scope, necessity, market effect, or downstream permission. The Stage-003 to Stage-005 tests therefore deliberately prevent `allowed` or `trusted` metadata from overwriting jurisdiction-specific legal-evidence fields.

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

## 6. Computational law and automatically processable regulation

Artificial Intelligence and Law has a long tradition of studying computational models of legal rules, legal reasoning, and the consequences of making regulation machine-processable. More recent research emphasizes open-texture: legal terms can be vague, evaluative, or under-specified and therefore resist naïve automation.

IPEL adopts that caution as an architectural principle. Instead of trying to compile Article 26(4) and Regulation Article 30 into a binary legality oracle, it divides requirements into:

- facts that can be structurally required or contradicted by a record;
- facts requiring referenced evidence;
- open-textured assessments that remain `REVIEW` rather than being fabricated by code.

Relevant literature:
- Guitton, Tamò-Larrieux & Mayer, *Mapping the Issues of Automated Legal Systems: Why Worry About Automatically Processable Regulation?* https://link.springer.com/article/10.1007/s10506-022-09323-w
- Guitton et al., *Identifying open-texture in regulations using LLMs*. https://link.springer.com/article/10.1007/s10506-025-09450-0
- Bench-Capon, *Thirty years of Artificial Intelligence and Law: Editor's Introduction*. https://link.springer.com/article/10.1007/s10506-022-09325-8

## 7. Novelty claim after related-work review

The defensible novelty claim is deliberately narrow:

> Existing work separately addresses substantive AI-training copyright doctrine, dataset lineage and license documentation, machine-readable rightsholder preferences, and cryptographic content provenance. Paper A contributes a tested **jurisdiction-specific legal-evidence layer** that maps fact-conditioned copyright rules into observable evidence requirements and enforces semantic barriers so provenance, trust, and preference signals cannot silently become legal conclusions.

The paper does **not** claim:

- the first provenance system for AI;
- the first machine-readable copyright protocol;
- the first C2PA use in AI;
- automated copyright compliance;
- universal cross-jurisdiction copyright semantics.

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
