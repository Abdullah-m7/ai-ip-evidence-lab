# Stage 011 — Simulated External Referee Report

## Recommendation

# **MAJOR REVISION**

The manuscript is **not ready for submission in its current form**, but I would not recommend abandoning it. The strongest parts are unusually disciplined boundary-setting, a reproducible implementation, and concrete experiments separating provenance integrity, signer trust, rights signaling, and jurisdiction-specific legal facts. The weakest parts are the now-incomplete 2026 literature positioning, an important omission from the Saudi legal mapping, and an empirical validation set that is too small to carry the paper's broader architecture rhetoric without further systematic testing.

The paper can become strong if it is revised around the narrow contribution that survives the saturation review rather than around generic “evidence layer / auditability” novelty.

---

## 1. Scorecard

| Dimension | Current score /10 | Referee assessment |
|---|---:|---|
| Novelty | **6.0** | Broad framing is anticipated; narrow integration/experimental contribution remains credible |
| Literature completeness | **5.5** | Good through 2025, but misses several close 2026 works and rights-expression standards |
| Saudi legal accuracy / completeness | **6.5** | Core Art. 26(4) / Reg. 30 treatment is careful, but Law Art. 37(1) is a material omission |
| Methodological rigor | **7.0** | Clear staged design and negative-result discipline; semantic mapping criteria remain too subjective |
| Empirical sufficiency | **5.5** | Five semantic cases + three corruption classes are proof-of-concept scale |
| Construct validity | **7.5** | Excellent separation of readiness vs legality; project-authored mapping/labels remain a limitation |
| External validity | **4.5** | All completed use cases are synthetic; no production-like corpus/workflow demonstration |
| Reproducibility | **9.5** | Exceptional for a law/technology paper; pinned tools, CI, frozen reports, fail-closed audits |
| Clarity / claim discipline | **8.5** | Strong limitations and explicit non-claims |
| Overclaim control | **9.0** | One of the manuscript's strongest features |
| Current strong-journal fit | **6.5–7.5** | Depends on revision; journal choice should remain open |

---

## 2. Major strength: the paper knows what cryptography cannot prove

The manuscript's most publishable intellectual move is not “provenance for copyright.” That ground is occupied. It is the experimentally enforced separation:

```text
content integrity != signer trust
signer trust != metadata semantic validity
rights/preference signal != complete legal basis
legal-evidence readiness != legal conclusion
```

This is not merely rhetorical. Stages 003–005 instantiate the boundary in code and test cases. A CAWG `allowed` signal does not cure an explicit adverse acquisition fact; changing trust policy does not alter legal evidence; a signed unsupported TDM value can remain cryptographically valid while failing semantic validation.

That combination is stronger than a typical doctrinal proposal and should become the center of the paper.

---

## 3. Major concern 1 — the novelty framing is now outdated

The current manuscript says that IPEL contributes a jurisdiction-specific evidence layer after introducing reviewability, dataset documentation, C2PA, and rights signaling. That is no longer enough.

Close 2026 work includes:

- Grace Li's **minimum reviewable trace**, which directly translates abstract legal/accountability duties into evidence disciplines and reviewable artifacts;
- Nicola Lucchi's copyright **auditability gap**, which frames copyright adjudication as an evidentiary-record problem;
- Park's 2025 **NFT/C2PA copyright management for AI training data**;
- Krishna et al.'s 2026 **Post-Report Provenance Procedure**, which treats cryptographic provenance as copyright-litigation evidence;
- TrainProVe and information-isotope work, which provide technical methods for post-hoc training-data provenance detection.

These works do not duplicate IPEL, but they invalidate any implication that “auditability/evidence/provenance for AI copyright” is itself the novelty.

### Mandatory revision
Rewrite the abstract, introduction, related work, contribution paragraph, and conclusion around this narrower statement:

> IPEL's contribution is the **executable decomposition of a specific statutory AI-development copyright pathway into use-event evidence requirements, plus empirical tests of when mature provenance/rights signals are not semantically substitutable for those legal-evidence facts.**

The paper should explicitly concede that reviewable traces, auditability, and C2PA-based copyright management are prior art.

---

## 4. Major concern 2 — Saudi Copyright Law Article 37(1) is missing from the legal scope

The current legal matrix declares its scope as **Article 26(4) + Implementing Regulation Article 30**. But the official Copyright Law also provides in Article 37(1) that uses under Articles 26–36 must not conflict with normal exploitation of the work and must not cause unjustified harm to the legitimate interests of rightsholders.

This matters because Article 26(4) does not operate in isolation. The manuscript currently discusses normal exploitation and unjustified harm mainly through Regulation Article 30(2)/(4), but the law-level cross-cutting condition in Article 37 should be included explicitly in the legal architecture.

### Why this is not cosmetic

If the paper claims to derive an evidence contract from the governing legal pathway, omitting an expressly applicable statutory condition undermines the completeness of that decomposition. A skeptical legal reviewer could question the validity of the entire requirements matrix.

### Mandatory revision
- Expand legal scope to `Law Art. 26(4) + Law Art. 37(1) + Implementing Regulation Art. 30`.
- Update the legal requirements matrix, schema rationale, manuscript legal section, and claim-evidence audit.
- Explain the relationship between the general Art. 37 three-step-type safeguard and the more specific Reg. 30 controls.
- Do not assume redundancy merely because similar concepts appear in Reg. 30.

---

## 5. Major concern 3 — “safe semantic delegation” lacks a sufficiently explicit method

The central Stage-003 result is that **0/4 Article 30(3) fields were delegated to C2PA in the tested mapping**. Yet the method currently says a field is delegated only where semantics are “sufficiently equivalent.” That decision rule is under-specified.

A reviewer can reasonably ask:

- What makes two fields sufficiently equivalent?
- Must they share subject, temporal reference, actor, event, legal meaning, provenance level, and evidentiary function?
- Are custom C2PA assertions in scope?
- Is a generic provenance field rejected because of the standard, or because of the selected profile design?
- Could another competent mapper reach 1/4, 2/4, or 4/4?

### Mandatory revision
Create a **predefined semantic-equivalence rubric** before expanding the experiment. At minimum score/require:

1. same referent / object;
2. same event or lifecycle moment;
3. same actor/issuer semantics;
4. same temporal semantics;
5. same normative vs descriptive status;
6. same evidence/provenance function;
7. no loss of legally material qualifiers;
8. round-trip recoverability without inference.

Then rerun the delegation analysis under that rubric. The `0/4` result should emerge from declared criteria rather than expert intuition alone.

---

## 6. Major concern 4 — the empirical validation is proof-of-concept scale

Five semantic profiles are too few to support a broad architecture claim. Three corruption classes are useful but narrow.

The manuscript is commendably honest about this, but honesty alone does not eliminate the evidentiary weakness.

### Mandatory revision
Expand the **non-human** benchmark before submission. This does not require a human study.

A reasonable minimum design would include:

- every legal condition in Art. 26(4), Art. 37(1), and Reg. 30 represented in positive, unresolved, and adverse forms where logically possible;
- paired cases for structural absence vs explicit adverse fact;
- paired false-equivalence cases for `valid`, `trusted`, `allowed`, and rights-expression signals;
- malformed/contradictory metadata cases;
- temporal change cases (licence/rights state changes before vs after use);
- at least one mixed-rights or independently protected-element case.

The goal is not an arbitrary N. The goal is **condition coverage** and a documented false-pass search space.

---

## 7. Major concern 5 — there is no strong baseline / ablation for the semantic barrier

Paper A shows that IPEL refuses false equivalence. It does not yet show what goes wrong in a plausible alternative design.

### Mandatory revision
Add at least one explicit baseline, for example:

- **naïve provenance mapping:** superficially similar C2PA/rights fields are accepted as substitutes;
- **flat evidence record:** same fields but no semantic barrier between integrity/trust and legal status;
- optionally, **C2PA-only profile** for the overlapping facts.

Then measure false-pass / semantic-loss behavior on the expanded case set.

This would convert the paper from “our design has a safety property” to “the safety property prevents a demonstrable failure mode relative to a plausible alternative.”

---

## 8. Major concern 6 — Stage 002 should not be omitted from the scientific story

Stage 002 produced a valuable negative result:

- internal hash-chain consistency detected **4/6** committed attacks;
- verification against a previously preserved checkpoint detected **6/6**;
- fully rehashed forgery and tail deletion escaped internal-only verification.

This is exactly the kind of bounded negative result that supports the later decision to reuse C2PA rather than invent an IPEL signing stack.

### Mandatory revision
Include Stage 002 as an **integrity ablation / design-selection experiment**, not as a production security guarantee. It strengthens the methodological narrative:

`raw hash chain → demonstrated boundary → external commitment requirement → mature C2PA infrastructure`.

This is more scientifically informative than beginning the empirical story at Stage 003.

---

## 9. Major concern 7 — all completed scenarios are synthetic

Synthetic records are appropriate for falsification and avoid unauthorized corpus use, but the manuscript currently has no ecological demonstration that the contract can represent a realistic source/licence/use history.

### Recommended-to-mandatory revision for a strong journal
Add one or more **lawfully usable ecological traces**, such as:

- a public-domain work;
- a clearly licensed Creative Commons work;
- an openly licensed dataset with documented source/licence history;
- a controlled mock acquisition record based on a real public licence text.

The objective is not to assert Saudi-law compliance. It is to demonstrate that real-world metadata heterogeneity can be ingested without the schema collapsing into synthetic toy fields.

---

## 10. Major concern 8 — rights-expression literature is incomplete

The paper discusses CAWG and TDM·AI but not the longer rights-expression tradition:

- W3C **ODRL 2.2**;
- IPTC **RightsML**;
- Creative Commons **ccREL**;
- the emerging **ODRL AI Vocabulary/Profile** for AI-specific actions.

This omission matters because a reviewer could ask whether IPEL is rediscovering rights-policy expression.

### Mandatory revision
Add a short subsection distinguishing:

- **rights/policy expression** (permission, prohibition, duty, constraint), from
- **evidence about a historical use event** (what happened, when, on which copy, with which evidence basis).

This distinction will strengthen rather than weaken IPEL.

---

## 11. Major concern 9 — evidence retention creates privacy / minimization tensions

Recent copyright/privacy scholarship emphasizes that keeping detailed training records can itself create retention, personal-data, confidentiality, and discovery risks.

IPEL currently treats more durable evidence as primarily beneficial. That is incomplete.

### Mandatory revision
Add a design tension:

> **evidentiary sufficiency vs data minimization / confidentiality / retention risk**.

The architecture should not imply that retaining all source material or all raw data forever is the answer. It should distinguish minimal evidence references, digests, legal holds, privacy-sensitive metadata, and retention schedules.

---

## 12. Title and terminology concern

“Verifiable Evidence” may be read as verification of truth. The paper itself correctly states that integrity does not prove truth.

Likewise, “evidentiary observability” is useful vocabulary but should not be sold as a wholly new concept given the 2026 auditability/evidentiary-infrastructure literature.

### Revision direction
Consider a title closer to the actual contribution, e.g.:

> **From Statutory Conditions to Reviewable Evidence: Executable Copyright-Provenance Boundaries for AI Development under Saudi Arabia’s 2026 Copyright Law**

or

> **Operationalizing AI-Training Copyright Evidence: A Saudi Legal Testbed for Provenance, Rights Signals, and Reviewable Records**

No title change should be locked until the expanded benchmark is complete.

---

## 13. Minor / presentation comments

1. State explicit research questions in the manuscript, not only contributions.
2. Move future human-study infrastructure out of the central Methods flow or compress it; it currently risks making an unrun study look more central than the completed experiments.
3. Add a one-page architecture figure showing `legal source → evidence contract → provenance carrier → evidence gate → human/legal review`.
4. Add a table distinguishing **assertion / evidence reference / integrity proof / legal conclusion**.
5. Clarify why “Ledger” is retained in the IPEL name if production architecture is not a blockchain or append-only ledger by definition.
6. Add versioning requirements for legal mappings and standards; the paper already acknowledges standards can evolve.
7. Cite close 2026 prior work directly in the Discussion rather than burying it in Related Work.

---

## 14. Journal-fit assessment

### Artificial Intelligence and Law
Potentially suitable **after major revision** if the paper foregrounds:
- legal-to-evidence formalization;
- open-texture/deference boundary;
- executable semantic validation;
- reproducible computational-law methodology.

### Computer Law & Security Review
Potentially suitable **after major revision** if the paper foregrounds:
- copyright governance;
- technical provenance and rights infrastructure;
- evidentiary/retention/privacy implications;
- practical regulatory architecture.

**Do not choose between them yet.** The revised paper's center of gravity should determine the target, not the current availability of one journal.

---

## 15. Referee conclusion

The paper has a real contribution, but its strongest version is **narrower and more empirical** than the current framing.

I would encourage resubmission after major revision if the authors:

1. absorb the 2026 near-overlap literature;
2. correct the Saudi legal scope to include Art. 37(1);
3. formalize semantic-equivalence criteria;
4. expand condition coverage and add a baseline/ablation;
5. include the Stage-002 integrity negative result;
6. add a small ecological trace demonstration; and
7. retain the unusually strong claim-discipline already present.

**Recommendation: MAJOR REVISION.**