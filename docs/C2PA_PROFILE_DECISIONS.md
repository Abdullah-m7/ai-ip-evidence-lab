# Stage 003 — C2PA Profile Decisions

## Scope
This stage asks a narrow interoperability question: **which IPEL facts can be delegated to C2PA/CAWG without changing their meaning?** It does not claim to produce a conformant C2PA Manifest.

Normative/informative baselines reviewed:
- C2PA Technical Specification 2.4 (April 2026): https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- C2PA AI/ML guidance 2.4: https://spec.c2pa.org/specifications/specifications/2.4/ai-ml/ai_ml.html
- CAWG Training and Data Mining Assertion 1.1: https://cawg.io/training-and-data-mining/1.1/

## D1 — Do not fabricate a C2PA Manifest
C2PA 2.4 introduced crJSON as a derived representation for profile evaluation/interoperability and validation reporting. The specification states that crJSON is not independently verifiable and is not an input format. Stage 003 therefore uses an explicitly labelled `aligned-intermediate-not-a-manifest` object.

## D2 — Use Ingredient `inputTo` only as generic workflow meaning
C2PA Ingredient v3 defines `inputTo` for an ingredient used as input to a computational process, explicitly including AI/ML examples. IPEL can therefore reference that generic relationship without asserting anything about copyright status.

## D3 — Safe generic migrations are deliberately few
Current Stage-001 records safely delegate only:
- `work.title` → C2PA ingredient `dc:title` semantics.

`work.sha256` remains jurisdictional in Stage 003. C2PA has strong hard-binding and hashed-reference machinery, but a naked IPEL digest is not itself a conformant C2PA hard binding or Ingredient v3 hashed reference. Delegating it safely requires a real manifest/SDK experiment.

## D4 — Saudi “source” remains jurisdiction-specific
C2PA Ingredient v3 provides `informationalURI`, hashed references, active manifests, and external/embedded data mechanisms. None is automatically equivalent to the legal/evidentiary meaning of **source of the work** retained under the Saudi record requirement. `work.source` therefore stays in IPEL.

## D5 — Saudi “date of use” remains jurisdiction-specific
C2PA Actions may include `when`, but the specification describes it as a simple **non-trusted timestamp**, and its value is a date-time. Stage-001 currently stores a legal-use date (`YYYY-MM-DD`) rather than a captured RFC/CBOR event timestamp. Converting the date to midnight would invent precision. `use.date` therefore stays in IPEL.

## D6 — Work type and purpose remain jurisdiction-specific
C2PA `dc:format` is an IANA media type, not a Saudi copyright-work classification. A free-text action description is also not equivalent to the legally relevant purpose of use. `work.type` and `use.purpose` remain in IPEL.

## D7 — TDM assertions are signals, not legal conclusions
CAWG TDM 1.1 defines `allowed`, `notAllowed`, and `constrained` for four standard uses, including `cawg.ai_training` and `cawg.ai_generative_training`. The assertion communicates an actor's signal about use. It does **not** by itself prove ownership, authority to license, lawful acquisition, lawful publication, or the validity/scope of permission under Saudi law.

The round-trip code is therefore prohibited from deriving any IPEL legal-status field from a TDM value.

## D8 — C2PA validation/trust is not copyright compliance
A valid/trusted Manifest can support provenance trust. It does not establish that the work was lawfully published or acquired, nor that statutory conditions are satisfied. These states remain independent inputs to IPEL.

## Resulting architecture
```text
C2PA / CAWG layer
  generic provenance, ingredient relationship, content binding,
  TDM signal, manifest validation/trust references
                │
                │ references / carries generic facts
                ▼
IPEL jurisdictional profile
  work type + source + legal-use purpose + legal-use date
  acquisition/publication status + market/rights assessments
  output restrictions + evidence references
                │
                ▼
Saudi evidence-readiness gate
```

The Stage-003 result is therefore **complementarity, not substitution**.
