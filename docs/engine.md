# Classical decipherment engine

Runnable solvers for **known classical ciphers of a known language** (English by default). This is not a decoder for undeciphered scripts.

Run from the repository root:

```bash
python -m engine.cli --help
python -m engine.cli demo
python -m demos.run_known_solves
python -m unittest tests.test_solvers
```

No third-party packages. `requirements.txt` documents that the standard library is enough.

## What it does

| Cipher | Attack | Module |
|---|---|---|
| Caesar (shift) | All 26 shifts, keep the lowest chi-squared fit to English, German, or Spanish letter frequencies | `engine/solvers/caesar.py` |
| Vigenère | Friedman column index of coincidence, Friedman length estimate, Kasiski votes on repeated trigrams (and factors of high-IC periods). Each column is a Caesar cipher scored by chi-squared. Candidate plaintexts are ranked by English **quadgram log-likelihood**, with a shorter key preferred on a near-tie, then a short coordinate-descent polish on the keyword | `engine/solvers/vigenere.py`, `engine/ic.py` |
| Simple substitution | Random-restart **hill-climbing** and **simulated annealing** over pairwise letter swaps. Fitness is the sum of ln P(quadgram). Temperature starts from the size of typical swap deltas and cools geometrically. A worse key is kept with probability exp(Δ / T). The default is anneal, then a strict hill-climb that stops after 1000 non-improving swaps. `--method hillclimb` skips the annealing phase | `engine/solvers/substitution.py` |

Quadgram probabilities are ln(count / N) on letters-only public-domain prose (Project Gutenberg #1342 Pride and Prejudice, #11 Alice, #84 Frankenstein, #1228 Origin of Species), with unseen quadgrams scored ln(0.01 / N). The shipped table is `engine/data/en_quadgrams.json.gz`. The demo and test plaintexts are not in that corpus.

Also included, as measurements rather than decipherments:

- Index of coincidence, letter frequencies, n-gram counts (`engine.cli stats`)
- Crib dragging for an additive cipher (`engine.cli crib`)
- `engine.cli unsupervised` — the same English substitution search, explicitly assuming English monoalphabetic plaintext

The CLI is `python -m engine.cli` with explicit subcommands (`caesar`, `vigenere`, `substitution`, `stats`, `crib`, `unsupervised`, `demo`). Known fixtures live in `demos/fixtures/`. The demo prints the recovered plaintext and exits non-zero if a known case is not recovered.

These are the usual published techniques (Friedman, Kasiski, chi-squared column shifts, quadgram hill-climbing, Metropolis annealing). The code is local; it is not a copy of another solver project.


## Learned fitness function

`engine/neural.py` trains a small character-level network and uses it as a **second opinion** beside the quadgram score. Substitution search itself is unchanged: `solve_substitution` still maximises quadgram log-likelihood from `engine/language.py`. After a candidate key is chosen, the network's log-likelihood is stored on the result as `details["neural_score"]` (`details["second_opinion"]` is `neural_trigram`).

The model is a trigram net. The two previous letters are one-hot vectors, a tanh hidden layer of 32 units mixes them, and a 26-way softmax predicts the next letter. Weights start random and are fit by gradient descent on next-letter cross-entropy, so the parameters are learned rather than copied from a published frequency table. Numpy does the matrix updates when it is installed; otherwise the same updates run in the standard library. No GPU and no downloaded checkpoint.

Training text is a short public-domain excerpt: Lewis Carroll, *Alice's Adventures in Wonderland*, chapter I (Project Gutenberg eBook 11), in `engine/data/alice_excerpt.txt`. Attribution lines in that file are not trained on. The excerpt is not the demo plaintext and not the plaintext in `engine/fixtures.py`. `tests/test_neural.py` checks that the fitted model prefers a held-out English sentence over a random letter string of the same length, and that training loss fell.

Limits of this fitness function:

- A higher neural score means "these Latin letters look more like the Alice excerpt." It does not mean the candidate is the correct plaintext, and it does not identify an unknown language.
- It does not decipher Linear A, the Voynich manuscript, the Vesuvius scrolls, or any other undeciphered script. Putting those signs through the model only measures a forced resemblance to one English sample.
- It is not the search objective. Quadgrams can prefer a key that the network likes less, and the reverse. The two numbers check each other; together they are still only English-letter fitness.
- The sample is short and literary. Letter habits that the excerpt barely contains stay weak. German, Spanish, and non-Latin scripts are outside this model.
- Nothing here is a historical decipherment.


## What it cannot do

**Linear A, Voynich, Rongorongo, the Indus script, the Phaistos disc, and other undeciphered writing systems are out of scope.** The engine will not produce a reading of them.

Reasons, not missing polish:

- Those problems are not “English under a 26-letter substitution.” The language is unknown, the script is not the Latin alphabet, word breaks are uncertain, and there is often no bilingual. A quadgram model of Austen and Darwin cannot identify an unknown language.
- Running the substitution solver on Voynich-like input will emit *some* Latin-letter string that scores well as English. That string is a forced fit to the fitness function, not a decipherment. Treat it as garbage.
- IC and frequency tables can describe a corpus. They do not decide whether a sign sequence is a script, a hoax, or which language it records.
- Homophonic ciphers, nomenclators, Playfair/Hill, Enigma and other machine ciphers, and codes (word lists, codebooks) are not implemented. A Vigenère solver will mis-read them as a repeating keyword and still print “plaintext.”

Short ciphertext is also a hard limit. Caesar needs enough letters for a frequency peak. Vigenère on this engine wants on the order of a few dozen letters per key column. Simple substitution wants roughly 80 letters and is aimed at a few hundred; below that the search is not reliable. German and Spanish are supported for Caesar and Vigenère unigram scoring only. Substitution fitness is English.

Nothing here claims a new historical decipherment.
