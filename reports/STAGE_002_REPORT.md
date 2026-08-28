# Stage 002 Report — Tamper-Evident Event History

## Question
Can a minimal hash-linked IPEL event history reveal post-hoc manipulation, and what changes when verification is anchored to a previously preserved checkpoint?

## Experimental setup
A three-event synthetic history was created for acquisition, AI-development use, and rights assessment. Six adversarial variants were committed as fixtures:

1. middle-event deletion;
2. event insertion;
3. payload mutation (purpose drift);
4. payload rewrite followed by full downstream rehashing;
5. event reordering;
6. tail deletion.

Each fixture is verified twice: (a) internal chain consistency only and (b) against the clean chain's original `(event_count, head_hash)` checkpoint.

## Results

| Attack | Internal-only detects? | Checkpoint detects? | Primary signal |
|---|---:|---:|---|
| deletion_middle | yes | yes | sequence / previous-hash / count |
| insertion_event | yes | yes | sequence / previous-hash / count |
| mutation_payload | yes | yes | event-hash mismatch |
| rehashed_forgery | **no** | yes | checkpoint head mismatch |
| reordered | yes | yes | sequence / previous-hash |
| tail_deletion | **no** | yes | checkpoint count + head mismatch |

Synthetic-fixture detection coverage:

- internal consistency only: **4/6 (66.7%)**;
- original checkpoint available: **6/6 (100%)**.

These percentages describe only the six committed attack fixtures. They are not a security guarantee or an estimate of real-world adversarial coverage.

## Main finding
A hash chain is not sufficient as a historical trust mechanism when an attacker can rewrite the stored history and recompute hashes. An independently preserved boundary commitment changes the observable security property: rehashed rewrites and tail truncation become detectable relative to that commitment.

## Negative result / limit
Stage 002 does **not** establish who created the checkpoint, whether it existed at the asserted time, whether the recorded events were truthful when first written, or whether an attacker can replace both the chain and its checkpoint. Consequently:

```text
integrity_verified != claim_truth_verified
```

The implementation hard-codes `claim_truth_verified=false` to make this boundary machine-visible.

## C2PA implication
The experiment weakens the case for inventing an IPEL-specific production signing/provenance stack. C2PA already supplies signed claims, asset bindings, ingredients, dataset/model provenance, and a trust ecosystem. IPEL's defensible contribution is therefore more likely to be a **jurisdictional evidence profile and legal-review boundary** that references or is carried by mature provenance infrastructure.

## Reproducibility

```bash
python3 -m unittest discover -s tests -v
python3 experiments/stage002_attack_matrix.py
```

Machine-readable results are committed at `reports/stage002_attack_matrix.json`.

## Stage decision
**PASS as a bounded integrity experiment.** Do not promote the raw hash-chain mechanism as production architecture. The next stage should evaluate a concrete C2PA-backed representation of one IPEL event/record and quantify information duplication/loss across the crosswalk.
