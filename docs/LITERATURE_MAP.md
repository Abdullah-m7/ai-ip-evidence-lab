# Literature and Infrastructure Map — Stage 001

This map is intentionally narrow: it asks what already exists for AI data provenance, training-data auditing, and IP infrastructure, and what remains specific to IPEL.

## 1. Data Provenance Initiative / Nature Machine Intelligence (2024)

**Work:** Longpre et al., *A large-scale audit of dataset licensing and attribution in AI*, Nature Machine Intelligence 6, 975–987 (2024).

**Contribution:** Traces source, creators, licences, and lineage across more than 1,800 text datasets; documents substantial licence omission and miscategorization.

**Relevance to IPEL:** Strong prior art for dataset-lineage transparency. It means IPEL should **not** claim novelty merely for storing source or licence metadata.

**IPEL distinction:** Stage 001 maps a newly effective Saudi legal exception and its express record-retention duty to a work/use-event evidence contract, with a boundary between deterministic evidence checks and legal judgment.

Source: https://www.nature.com/articles/s42256-024-00878-8

## 2. WIPO AI Infrastructure Interchange (AIII, launched 2026)

**Contribution:** Global technical dialogue around identifiers, metadata, authentication, watermarking, rights management, content recognition, and AI/IP infrastructure.

**Relevance to IPEL:** Confirms that the research problem is infrastructural, not only doctrinal. It also raises the bar: any proposed architecture should be interoperable with existing identifiers and rights metadata rather than creating an isolated Saudi-only format.

**IPEL distinction:** AIII is not a legal standard and is deliberately cross-sector/global. IPEL can act as a jurisdiction-specific test case for how a concrete statutory record duty can be represented in interoperable evidence infrastructure.

Sources:
- https://www.wipo.int/en/web/ai-infrastructure-interchange
- https://www.wipo.int/en/web/ai-infrastructure-interchange/faqs

## 3. C2PA AI/ML provenance guidance

**Contribution:** C2PA guidance now includes model, training-data-set, and AI/ML output Content Credentials, along with provenance and training/data-mining assertions.

**Relevance to IPEL:** Provides mature building blocks for content binding, manifests, signatures, rights metadata, and provenance chains.

**Key limitation for this project:** Provenance/authenticity does not itself prove lawful acquisition, licence validity, ownership, or satisfaction of a jurisdiction-specific exception. IPEL should therefore integrate or map to C2PA where useful, not compete with it as a generic provenance format.

Source: https://spec.c2pa.org/specifications/specifications/2.3/ai-ml/ai_ml.html

## 4. Information Isotopes / Nature Communications (2026)

**Work:** *Auditing unauthorized training data from AI generated content using information isotopes*, Nature Communications (2026).

**Contribution:** Technical detection of unauthorized training-data use in black-box AI systems.

**Relevance to IPEL:** Important complementary direction: IPEL is primarily **ex ante / contemporaneous evidence**, whereas information-isotope approaches can help with **ex post detection** when a developer's internal provenance is unavailable or untrusted.

Source: https://www.nature.com/articles/s41467-026-68862-x

## 5. Saudi copyright scholarship and practice commentary

Earlier Saudi scholarship studied whether unauthorized use of copyrighted works for AI training could be legitimized and recommended reform. The 2026 law and implementing regulations materially change the legal baseline by expressly addressing AI-development copying and record retention.

A 27 August 2026 practitioner analysis highlights the same practical recordkeeping consequence of Article 30, reinforcing that provenance documentation is a real compliance problem rather than a hypothetical one.

Sources:
- Saudi Digital Library thesis (2023): https://drepo.sdl.edu.sa/items/22fda501-3d6b-474f-9a97-d16b69e5f4f2
- Gowling WLG (27 Aug 2026): https://gowlingwlg.com/en/insights-resources/articles/2026/saudi-arabia-copyright-law-implementing-regulations

## Provisional novelty claim — deliberately narrow

Stage 001 will **not** claim to invent training-data provenance, content credentials, rights metadata, or copyright compliance automation.

The provisional contribution to test is:

> A work/use-event evidence architecture that operationalizes the evidentiary facts made salient by Saudi Copyright Law Article 26(4) and Implementing Regulations Article 30, while explicitly separating machine-verifiable provenance from facts requiring human legal/economic judgment.

This claim remains provisional until a systematic literature search and prior-art review are completed.

## Immediate prior-art risks

1. Existing regtech may already map copyright exceptions into compliance records.
2. C2PA or creator-assertion extensions may cover enough of the evidence model that a new schema is unnecessary.
3. Data-governance lineage products may already preserve acquisition/use events with stronger integrity guarantees.
4. A Saudi practitioner or academic paper may appear rapidly because the implementing regulations are only weeks old.

These risks should be treated as falsification opportunities, not hidden.
