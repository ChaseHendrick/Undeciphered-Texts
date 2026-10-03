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

`engine.neural.NeuralLetterModel`: the two previous letters are one-hot, a tanh hidden layer of 32 units mixes them, and a 26-way softmax predicts the next letter. With numpy installed, momentum gradient descent runs for 60 epochs (`NUMPY_EPOCHS`, momentum 0.8). Scoring is a vectorized matrix product. The counts below are that numpy fit, seed 20261002. The standard-library fit is a shorter run and is not the source of these counts.

Evaluation uses non-overlapping 120-letter windows. The Grimm tale yields fewer windows than the Doyle passage, so both sides are cut to the shorter count: **38 windows**. Each English window is scored against a shuffle of its own letters (seed 20261002) and against the German window of the same length. The reported log-loss is the mean, over windows, of the negative mean log probability of each letter after the first two. Lower log-loss is better.

Chance baselines, computed rather than copied from the run:

- Three-way preference: if the English, shuffled, and German scores are i.i.d. continuous, the probability that English is strictly best is 1/3 = **0.333333**.
- Pairwise: the probability that English scores strictly above one other string is 1/2 = **0.5**.

| Comparison | Result | Chance |
| --- | --- | --- |
| English strictly best of English, shuffled English, and German | **38/38 = 1.0** | 0.333333 |
| English log-score above the shuffle | **38/38 = 1.0** | 0.5 |
| English log-score above German | **38/38 = 1.0** | 0.5 |
| Mean log-loss, English | **2.563862** |  |
| Mean log-loss, German | **2.808083** |  |
| Mean log-loss, shuffled English | **3.299463** |  |

Training events (next-letter predictions in the Austen chapters): 12471.

## Cipher-family router

Two routers are scored. Neither is edited inside `engine/solver_net.py`.

### Grade router

`engine/neural_grade.py` fits a tanh hidden layer of 32 units for 60 epochs. The feature row is smaller than a raw letter histogram: index of coincidence, entropy, Caesar and sorted-unigram agreement, digraph and period statistics, plus a look-ahead. Look-ahead tries the certified Vigenere, Beaufort, and Porta maps, and the keyless inverses of keel-sieve, lumen-braid, and prism-latch, then keeps only the English digraph fitness. The trial string is not returned. Training ciphertexts are generated from the Austen letters (20 plaintexts per family, 180 letters, fresh keys, seed 20261002). Evaluation ciphertexts are generated from the Doyle letters (12 per family, seed 20261003). The plaintext is not a certificate plaintext.

Families are the certified systems with an A-Z forward map: caesar, vigenère, keyed Vigenère, substitution, Playfair, bifid, two-square, four-square, ADFGVX, columnar transposition, Beaufort, Porta, Enigma, M-209, keel-sieve, lumen-braid, and prism-latch. Beam-search and the Vigenère crib are search procedures for families already in that list, not extra classes. The Polybius-Gronsfeld module searches one digit cryptogram; it is not an A-Z family in this router.

Chance for a uniform guess among 17 families is 1/17 = **0.058824**.

Held-out accuracy: **161/204 = 0.789216**.

| Family | Correct / 12 |
| --- | --- |
| caesar | 12 |
| vigenere | 7 |
| keyed-vigenere | 3 |
| substitution | 11 |
| playfair | 10 |
| bifid | 11 |
| two-square | 8 |
| four-square | 10 |
| adfgvx | 12 |
| columnar-transposition | 12 |
| beaufort | 9 |
| porta | 10 |
| enigma | 4 |
| m209 | 6 |
| keel-sieve | 12 |
| lumen-braid | 12 |
| prism-latch | 12 |

Keyed Vigenère is still the weak row (3/12). Beaufort is 9/12, Enigma is 4/12, and M-209 is 6/12. Those three were 2/12 before the look-ahead features. 3/12 is still above 1/17 on this draw, and the 17-way accuracy is 0.789216. A correct family label is not plaintext and is not a key recovery.

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
- `engine/data/neural_grade_certificate.json` stores the SHA-256 of that metrics file: `e1f6d681ee7b883a82412a13e79e28f171de2c5958f5da12391b6c1b910863df`.
- `tests/test_neural_grade.py` recomputes the grade, checks it against those counts when the backend matches, checks the SHA-256, and checks the chance baselines.

Numpy is used for the grade router's matrix updates when it is installed. The letter model still trains with the standard library if numpy is absent. `engine.solver_net` does not need numpy. No other numeric dependency is required.

## Retrain loop

`python -m engine.neural_router_loop` fits the router in the foreground until you stop it. `python -m engine.neural_router_loop --once` does one pass. There is no cron entry and no external wake. Create `engine/data/neural_router_loop.stop` or end the process to leave the loop. The default gap between passes is 20 seconds, inside that process only.

Each pass calls `discover_solver_labels()`, which reads `engine/data/*_certificate.json`. A file becomes a class when it has `cipher_name`, `plaintext`, and `ciphertext`. The plaintext is not stored and is not emitted. Two files with the same cipher name are one class. Names for K4, Zodiac, Beale, McCormick, Voynich, and Nr. 86 are refused.

If the label has a generator (the 17 families above, or a later certificate whose normalized name matches one of those generators), the pass builds fresh Austen and Doyle samples. Any other known-answer label is still a class: its certificate ciphertext is a training exemplar. Weights in `engine/data/neural_router_weights.json` are replaced only when the Doyle held-out accuracy does not drop. `route_ciphertext` returns that family label and nothing else.

