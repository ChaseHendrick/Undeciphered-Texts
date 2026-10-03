# Solver net

The solver net in `engine/solver_net.py` routes a **known Latin-letter cipher** to a solver this repository already certifies. It then records a causal link: the solver it chose, the ciphertext features that caused that choice, and the certificate id that choice checks.

It does **not** decipher Kryptos K4, army message Nr. 86, Linear A, the Indus script, the Voynich manuscript, or rongorongo. Unknown scripts stay unread.

## Solvers it knows

| Solver | Family the net can select | Certificate it checks |
|---|---|---|
| caesar | caesar | `caesar_certificate.json` |
| vigenere | vigenere | `vigenere_certificate.json` |
| keyed vigenere | keyed-vigenere | `kryptos_k1_certificate.json` (K2 is a second exemplar) |
| substitution | substitution | `substitution_certificate.json` |
| playfair | playfair | `playfair_certificate.json` |
| bifid | bifid | `bifid_certificate.json` |
| adfgvx | adfgvx | `adfgvx_certificate.json` |
| columnar | columnar | `kryptos_k3_certificate.json` |
| two-square | two-square | `two_square_certificate.json` |
| crib | vigenere (related; not a separate feature class) | `crib_certificate.json` |
| beam search | beam-search | `beam_search_certificate.json` |
| lumen-braid | lumen-braid | `lumen_braid_certificate.json` |
| prism-latch | prism-latch | `prism_latch_certificate.json` |

Crib rides on the Vigenère family. The crib certificate ciphertext is the same string as the Vigenère certificate, so features cannot tell them apart. A Vigenère route names crib as a related solver. The crib solver still needs the crib string from its own certificate; the feature net does not invent one.

Beam search has its own certificate ciphertext, so it is its own class. It is still only a monoalphabetic search over A-Z, not a reader of an unknown script.

## What the classifier uses

Training is standard-library only. Numpy is not required.

Each ciphertext becomes a short feature row:

- index of coincidence
- digraph repeat rate (and a non-overlapping pair repeat rate)
- ADFGVX alphabet ratio, plus a flag when every letter is in `ADFGVX`
- even length of the letter stream
- space and digit ratios, whether `J` appears, alphabet coverage
- chi-square of the letter counts against English, at shift 0 and at the best Caesar shift
- double-letter rate, vowel ratio, top-letter ratio, letter entropy
- column unigram fitness (how English the columns look after a Caesar trial)
- log length

The net trains a kernel classifier on those features. Synthetic exemplars are produced by each solver's own encrypt function on windows of `engine/data/english.txt`, with keys drawn inside the trainer. The verification-certificate ciphertexts are added as labeled exemplars of the same families. At route time the class score is a sum of Gaussians on the z-scored features. If the feature vector matches a certificate exemplar exactly, the link checks **that** certificate.

The causal link stores:

- the chosen solver and its family
- the feature values
- the features that sat closer to the chosen family than to the runner-up (name, value, contribution)
- the certificate id the solver then checks
- the nearest exemplar and the kernel scores

`recover` calls the existing solver. Caesar and Vigenère search without being handed the key. Playfair, Bifid, ADFGVX, keyed Vigenère, columnar, and two-square are known-key checks: the keys come from the linked certificate, not from a search over an unsolved text.

## What it refuses

`SolverNet.decline` returns an unreadable link and does not call a solver for:

- Kryptos K4
- army message Nr. 86
- Linear A
- the Indus script
- the Voynich manuscript
- rongorongo

Passing one of those names does not produce a plaintext. A high score on a Latin-letter cipher only means the features looked like one of the certified families above.

## Test

From the repository root:

```bash
python3 -m unittest tests.test_solver_net -v
```

The route test uses three certificate ciphertexts already in the repo: Caesar, Playfair, and ADFGVX. For each one the net must select that family, and the linked solver must recover the certified plaintext and its SHA-256.
