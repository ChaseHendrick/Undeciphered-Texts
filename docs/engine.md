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


## German letter and quadgram score

`engine/german.py` is a fitness function for **Latin letters that might be German**. It is not wired into Caesar, Vigenère, or substitution search, and it does not decrypt anything.

The sample is a short public-domain excerpt, not an unsolved ciphertext: the opening of Jacob and Wilhelm Grimm, "Der Froschkönig oder der eiserne Heinrich," from *Deutsche Märchen gesammelt durch die Brüder Grimm*, ed. M. Thilo-Luyken (Ebenhausen: Wilhelm Langewiesche-Brandt, 1921), Project Gutenberg eBook #77905, in `engine/data/german_excerpt.txt`. Attribution lines in that file are not counted. After umlaut folding the sample is 1938 letters. Smoothed unigram rates from that count (highest first) begin E, N, I, S, D, R, A, H, T, L. Quadgrams use the same backoff log-likelihood as `LanguageModel`, fit on the folded excerpt.

`tests/test_german.py` holds out a sentence from a different tale in the same edition ("Der Wolf und die sieben jungen Geißlein"). That sentence is not in the excerpt. On the run recorded here its quadgram sum was about −288.9 against about −629.3 for a same-length random string (seed 86), and its chi-square against the excerpt unigrams was about 22.7 against about 7829 for that random string. Higher quadgram and unigram log-likelihood, and lower chi-square, means "more like this fairy tale," not "this is the plaintext."

### Truppenschlüssel Nr. 86, logged failures only

The 3 July 1941 Funkspruch Nr. 86 (FBOIQ, 46 letters) is still unsolved here. The strings below are the Caesar, Vigenère, and substitution dumps already logged as **failed** in `docs/logs/attempt-2026-10-02.md`. They were not re-solved, and no German plaintext was written for them. Mean quadgram is the sum divided by (letters − 3), so the 46-letter dumps can be set next to the longer probe (probe mean about −2.05):

| Stream | Mean quadgram | Quadgram sum | Unigram log | Chi-square |
|---|---:|---:|---:|---:|
| Held-out Grimm sentence | −2.05 | −288.9 | −383.1 | 22.7 |
| Logged substitution dump | −3.33 | −143.3 | −159.3 | 241.8 |
| Logged Caesar dump (shift 4) | −3.50 | −150.5 | −170.5 | 1113.1 |
| Logged Vigenère dump (key `FTTA`) | −3.74 | −161.0 | −157.4 | 206.2 |
| Undecrypted ciphertext | −4.10 | −176.4 | −169.8 | 503.2 |
| Random 46 letters (seed 86) | −4.64 | −199.4 | −216.7 | 3140.4 |

All three failed dumps sit below the German sentence. The substitution dump is the least bad of them and beats the raw ciphertext, which is what an English letter search does: it pushes the string toward English-looking fragments. That is not German and not a reading of the message.

Limits:

- The excerpt is nineteenth-century literary German, a few thousand letters, not 1941 military prose. Letter habits the tale barely has (J, Q, X, Y) stay near the smoothing floor, so chi-square on a short string is unstable and is not a verdict.
- ä, ö, ü, and ß are expanded to AE, OE, UE, and SS. The model never sees those characters as their own letters.
- Forty-six letters is too short for a quadgram score to identify a plaintext. A better score is still only resemblance to this sample.
- Truppenschlüssel is a manual digraph cipher on two 5×5 squares (J omitted). This score does not implement that cipher. Running it on a Caesar, Vigenère, or monoalphabetic dump does not turn the dump into German.
- Nothing here is a historical decipherment. The Nr. 86 message remains unbroken.
