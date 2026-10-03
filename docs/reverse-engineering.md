# Reverse engineering letter-cipher rules

`engine/reverse_engineer.py` tests which rules fit aligned plaintext cribs. It can infer parameters from multiple disjoint spans, retain incomplete keys, and make conditional predictions outside those spans. It does not need the key or the cipher family as input.

The supported families are Caesar, invertible affine substitution, arbitrary one-to-one substitution, and repeating Vigenere or Beaufort. It tries all 312 affine parameter pairs and every period up to the specified bound, capped at 128 and the ciphertext length. The algebra follows the [ACA Vigenere formula](https://www.cryptogram.org/downloads/aca.info/ciphers/Vigenere.pdf) and [Beaufort formula](https://www.cryptogram.org/downloads/aca.info/ciphers/Beaufort.pdf). This is an extension of the repository's single-span Vigenere crib search: it compares several families and several spans together, and exposes partially determined keys.

## Command

```bash
python3 -m engine reverse-engineer LXFOPVEFRNHR --crib 0:ATTACK --max-period 5
```

The command prints JSON. `--crib OFFSET:TEXT` may be repeated. Offsets are zero-based positions after spaces and punctuation are removed. In this constructed example, the period-5 Vigenere hypothesis infers LEMON and predicts ATTACKATDAWN. The six supplied letters determine five slots with one repeated-slot confirmation. The remaining letters were not supplied to the inference.

```python
from engine.reverse_engineer import Crib, infer_cipher_models

report = infer_cipher_models(
    ciphertext,
    cribs=[Crib(21, "EASTNORTHEAST"), Crib(63, "BERLINCLOCK")],
    max_period=16,
)
```

Each hypothesis reports its family, parameters, period where relevant, unresolved parameter count, repeated-constraint confirmations, conditional predicted plaintext, and number of predicted positions. Unknown letters and key slots remain `?`. Duplicate cribs do not count as additional evidence. Contradictory overlapping cribs are input errors. Contradictions within a candidate model reject that model.

`claimed_plaintext` is always null. A fully determined key still depends on the chosen family being correct. Several models or periods can fit the same evidence. There is no English score that silently chooses one. `predict_plaintext(text, hypothesis, offset=...)` can test a separate span at its global letter offset.

## Verification

`engine/data/reverse_engineer_certificate.json` uses the [ACA Vigenere worked example](https://www.cryptogram.org/downloads/aca.info/ciphers/Vigenere.pdf). The inference receives only its first 28 plaintext letters and the printed ciphertext. The period-14 Vigenere hypothesis must predict the complete 47-letter plaintext, including the 19 letters outside the crib, and match its SHA-256. The key is not an inference input. Other tests cover a published Beaufort vector, affine inference, partial substitution, sparse keys, contradictory evidence, and the CLI.

## Use on unsolved material

Cribs can rule out specific transformations. An empty report means these tested families and bounds are incompatible with the supplied positions. It says nothing about untested keyed alphabets, transpositions, multi-stage systems, enciphering errors, or whether the crib alignment is correct. With no aligned known plaintext, this tool has no evidence to infer a rule.

It does not claim a solution for Kryptos K4, Zodiac, Beale, McCormick, Voynich, an unknown language, or army message Nr. 86. See the unchanged [K4 bounded-search note](k4-attempt.md) and [ciphertext-error note](k4-error-model.md) for their own declared bounds.

## Symbolic constraints and case records

The optional [symbolic engine](cipher-synthesis.md) extends this workflow with Z3 constraints, unknown alphabet permutations for Quagmire I/II/III, and layout stages before letter encryption. It reports satisfiable, unsatisfiable, and unknown model classes separately. It tests alternate letter values to distinguish forced plaintext from an arbitrary satisfying example. Period, layout, time, and check limits remain part of every report.

Use the [case workflow](WORKFLOW.md) for real intake. It hashes the original source, validates the alphabet and provenance, excludes tentative cribs from inference, and saves complete run records. Candidate reports require independent validation before publication.
