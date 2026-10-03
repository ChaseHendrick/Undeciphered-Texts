# Pacifist exact affine investigator

`investigate_pacifist(text, *, cribs=(), max_checks=5000, max_candidates=20)` exhaustively tests an established affine cipher family. It is a conservative strategy for the persona system, not a new neural class or cipher algorithm. The separate `solve_pacifist`, `choose_pacifist` and peaceful-word scoring APIs remain preferences described in [pacifist.md](pacifist.md).

The investigator uses aligned caller cribs as exact constraints and does not load a language model or score peaceful, violent or English-looking sentences. An affine model has 12 invertible multipliers and 26 offsets modulo 26, giving 312 keys including the identity. The arithmetic is `C = a*P + b mod 26`, where `gcd(a,26)=1`. The [WCSU textbook's affine section](https://sites.wcsu.edu/mbxml/html/affine_section.html) gives the encryption/decryption definitions and literal worked examples.

```python
from engine.reverse_engineer import Crib
from engine.solvers.pacifist import investigate_pacifist

report = investigate_pacifist(
    ciphertext,
    cribs=(Crib(0, "T"), Crib(3, "S")),
    max_checks=312,
    max_candidates=20,
)
```

Offsets count zero-based normalized A-Z plaintext letters. Input normalization removes separators, rejects digits and Unicode letters, and requires 4..512 normalized letters within 4,096 raw characters. The shared validator accepts at most 128 typed cribs, rejects contradictory overlaps and out-of-range coordinates, and counts duplicate evidence once. `max_checks` accepts 0..100,000 and `max_candidates` accepts 1..100. This API has 312 possible key checks, regardless of a higher supplied budget.

One check decrypts a full affine hypothesis and tests its cribs. Every compatible witness passes a forward transformation before it can be retained. Witness storage never stops enumeration; candidates are stored in multiplier-then-offset order with `score: 0.0` and no semantic confidence. A witness alone is not a forced plaintext.

After **complete** enumeration, `compatible_key_count` is exact, `unique_key_within_model` records whether exactly one key remains, and `consensus_plaintext` compares every compatible plaintext. Consensus includes keys whose witnesses were omitted by the retention cap. A forced letter is conditional on this affine family and the supplied cribs. With no cribs all 312 keys remain compatible, consensus is all `?`, and the investigator explicitly abstains. If no key fits, consensus is also unknown; absence of a model cannot vacuously prove text.

With an incomplete budget, `compatible_key_count`, `unique_key_within_model` and `plaintext_unique_within_model` are null, `compatible_keys_found` counts only the checked prefix, and consensus is all `?`. The report retains literal examples, discloses `untested_keys` and recommends finishing enumeration. `provided_crib_mask` displays only supplied evidence and is distinct from forced consensus.

The [certificate](../engine/data/persona_pacifist_solver_certificate.json) checks two primary published vectors. In WCSU Subsection 6.2.2, two independently selected crib letters T and S constrain a 259-letter printed ciphertext. No key enters inference; all 312 hypotheses are tested, leaving `a=9,b=14` and predicting 257 noncrib letters, including the 255-letter suffix after the second crib. The separate [university worksheet](https://uomus.edu.iq/img/lectures21/MUCLecture_2024_11830114.pdf) prints `AFFINE CIPHER` / `IHHWVC SWFRCP`; the investigator receives only AF and predicts the remaining ten letters. Tests hash actual complete consensus, use separate modular formulas, and exercise ambiguity, impossible evidence and incomplete-budget abstention.

These checks establish useful unknown-key recovery of the published controls inside the tested classical family. They do not establish a new historical decipherment or a reading of an unknown script. Reports always keep `claimed_plaintext` null, `correctness_known` false, `semantic_confidence` null and `happiness` null. Even a unique model key requires independent heldout plaintext or cited reference evidence before treating a real unknown text as solved. Nr. 86 is excluded. See [QUALITY.md](QUALITY.md) and [AI-AGENTS.md](AI-AGENTS.md).
