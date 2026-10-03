# Neural grade

Held-out numbers for the trigram letter model and a cipher-family router. These numbers are fitness and routing scores on text whose plaintext is known because we encrypted it, or on prose we did not train on. They are not a decipherment.

This does **not** decipher Kryptos K4, army message Nr. 86, or an unknown script (Linear A, the Indus script, rongorongo, the Voynich manuscript, the Phaistos disc, or the Vesuvius scrolls).

`engine/solver_net.py` is scored below and is not edited. The extra router, which covers certified families that module does not route, is `engine/neural_grade.py`.

## Split

Training and evaluation prose are different public-domain books. Attribution lines in the files (the lines that start with `#`) are not fit and not scored. No evaluation sentence is in the training file. `tests/test_neural_grade.py` rejects a fit whose training letters contain the held-out English letters, including a fit trained on the held-out file itself.

| Role | Text | File | URL |
| --- | --- | --- | --- |
| Train | Jane Austen, *Pride and Prejudice*, chapters I-III. Illustration blocks and the 1894 George Allen copyright lines inside those blocks are removed. | `engine/data/neural_train_austen.txt` | [eBook 1342](https://www.gutenberg.org/ebooks/1342), [UTF-8 text](https://www.gutenberg.org/cache/epub/1342/pg1342.txt) |
| Held-out English | Arthur Conan Doyle, "A Scandal in Bohemia," opening, in *The Adventures of Sherlock Holmes*, through the paragraph that ends "to resolve all our doubts." Gutenberg italic markers were removed. | `engine/data/neural_heldout_doyle.txt` | [eBook 1661](https://www.gutenberg.org/ebooks/1661), [UTF-8 text](https://www.gutenberg.org/cache/epub/1661/pg1661.txt) |
| Held-out German | Jacob and Wilhelm Grimm, "Der Wolf und die sieben jungen Geißlein," in *Deutsche Märchen* (eBook 77905). This is not the Froschkönig excerpt in `engine/data/german_excerpt.txt`. Umlauts are folded (ä→ae, ö→oe, ü→ue, ß→ss) before scoring. | `engine/data/neural_heldout_grimm_wolf.txt` | [eBook 77905](https://www.gutenberg.org/ebooks/77905), [UTF-8 text](https://www.gutenberg.org/cache/epub/77905/pg77905.txt) |

The older Alice excerpt is still at `engine/data/alice_excerpt.txt`. `engine/neural.py` does not train on it.

Certificate plaintexts under `engine/data/*_certificate.json` are not the Austen or Doyle letter strings used to build router ciphertexts. The router keys are drawn fresh. They are not the keys stored on those certificates.

## Letter model

`engine.neural.NeuralLetterModel`: the two previous letters are one-hot, a tanh hidden layer of 32 units mixes them, and a 26-way softmax predicts the next letter. With numpy installed, gradient descent runs for 200 epochs (`NUMPY_EPOCHS`). The counts below are that numpy fit, seed 20261002. The standard-library fit is a shorter run and is not the source of these counts.

Evaluation uses non-overlapping 120-letter windows. The Grimm tale yields fewer windows than the Doyle passage, so both sides are cut to the shorter count: **38 windows**. Each English window is scored against a shuffle of its own letters (seed 20261002) and against the German window of the same length. The reported log-loss is the mean, over windows, of the negative mean log probability of each letter after the first two. Lower log-loss is better.

Chance baselines, computed rather than copied from the run:

- Three-way preference: if the English, shuffled, and German scores are i.i.d. continuous, the probability that English is strictly best is 1/3 = **0.333333**.
- Pairwise: the probability that English scores strictly above one other string is 1/2 = **0.5**.

| Comparison | Result | Chance |
| --- | --- | --- |
| English strictly best of English, shuffled English, and German | **36/38 = 0.947368** | 0.333333 |
| English log-score above the shuffle | **38/38 = 1.0** | 0.5 |
| English log-score above German | **36/38 = 0.947368** | 0.5 |
| Mean log-loss, English | **2.581298** |  |
| Mean log-loss, German | **2.794671** |  |
| Mean log-loss, shuffled English | **3.230853** |  |

Training events (next-letter predictions in the Austen chapters): 12471.

## Cipher-family router

Two routers are scored. Neither is edited inside `engine/solver_net.py`.

### Grade router

`engine/neural_grade.py` fits a tanh hidden layer of 40 units on fixed ciphertext features (index of coincidence, letter entropy, agreement with the Austen unigram under the best Caesar shift, digraph and period statistics, alphabet shape). Training ciphertexts are generated from the Austen letters (20 plaintexts per family, 180 letters, fresh keys, seed 20261002). Evaluation ciphertexts are generated from the Doyle letters (12 per family, seed 20261003). The plaintext is not a certificate plaintext.

Families are the certified systems with an A-Z forward map: caesar, vigenère, keyed Vigenère, substitution, Playfair, bifid, two-square, four-square, ADFGVX, columnar transposition, Beaufort, Porta, Enigma, M-209, keel-sieve, lumen-braid, and prism-latch. Beam-search and the Vigenère crib are search procedures for families already in that list, not extra classes. The Polybius-Gronsfeld module searches one digit cryptogram; it is not an A-Z family in this router.

Chance for a uniform guess among 17 families is 1/17 = **0.058824**.

Held-out accuracy: **126/204 = 0.617647**.

| Family | Correct / 12 |
| --- | --- |
| caesar | 12 |
| vigenere | 9 |
| keyed-vigenere | 2 |
| substitution | 11 |
| playfair | 11 |
| bifid | 11 |
| two-square | 9 |
| four-square | 12 |
| adfgvx | 11 |
| columnar-transposition | 12 |
| beaufort | 2 |
| porta | 5 |
| enigma | 2 |
| m209 | 2 |
| keel-sieve | 5 |
| lumen-braid | 6 |
| prism-latch | 4 |

Keyed Vigenère, Beaufort, Enigma, and M-209 are the weak rows (2/12). They are easy to confuse with each other because several of them are polyalphabetic. 2/12 is still above 1/17 on this draw, and the 17-way accuracy is 0.617647. A correct family label is not plaintext and is not a key recovery.

M-209 samples use the published pin and lug list from the known-key certificate and a fresh 6-letter external key drawn from each wheel's alphabet. Enigma samples use rotor orders I-III, reflector B, an empty plugboard, and fresh ring and window letters. They do not reuse a certificate plaintext.

### Shipped solver net

`engine.solver_net.train_solver_net` is called as published. Its training prose is `engine/data/english.txt`, plus the ciphertext exemplars on the certificates. That file does not contain the Doyle held-out letters. This grade does not change `engine/solver_net.py`.

The net is then asked to route ciphertexts built from the Doyle letters with that module's own encrypt helpers (40 windows of 180 letters, seed 20261003). Beam-search is not a separate synthetic label there. The net can still emit any of its 12 routed names, so chance is 1/12 = **0.083333**.

Held-out accuracy: **261/440 = 0.593182**.

| Family | Correct / 40 |
| --- | --- |
| caesar | 34 |
| vigenere | 29 |
| keyed-vigenere | 32 |
| substitution | 5 |
| playfair | 26 |
| bifid | 4 |
| adfgvx | 40 |
| columnar | 40 |
| two-square | 26 |
| lumen-braid | 2 |
| prism-latch | 23 |

Substitution, bifid, and lumen-braid are weak on this draw. The total is still above 1/12. This is not a reading of an unsolved ciphertext.

## Files

- `engine/data/neural_grade_metrics.json` stores the counts, the log-loss figures, and the source URLs.
- `engine/data/neural_grade_certificate.json` stores the SHA-256 of that metrics file: `a40cefa442cd691848ac86a36c14e71eda58ca442de9c2b2e006bfd8c2d7e84c`.
- `tests/test_neural_grade.py` recomputes the grade, checks it against those counts when the backend matches, checks the SHA-256, and checks the chance baselines.

Numpy is used for the grade router's matrix updates when it is installed. The letter model still trains with the standard library if numpy is absent. `engine.solver_net` does not need numpy. No other numeric dependency is required.
