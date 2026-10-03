# Tool catalog

Inventory of every **solver** and **analysis tool** that exists in this repository on `main`. Each entry is taken from the matching module and its unit tests. Nothing here invents a tool that is not in the tree, and nothing here is a decipherment of an ancient script or of Kryptos K4.

Companion notes for some tools: [beam-search.md](beam-search.md), [mural-analyzer.md](mural-analyzer.md), [compression-language-score.md](compression-language-score.md), [em-sign-aligner.md](em-sign-aligner.md), [hmm-baum-welch.md](hmm-baum-welch.md), [pairwise-mutual-information.md](pairwise-mutual-information.md), [sign-clustering.md](sign-clustering.md), [kryptos-k1.md](kryptos-k1.md), [TESTING.md](TESTING.md), [engine.md](engine.md).

## How to read this catalog

| Field | Meaning |
| --- | --- |
| **Path** | Source file under the repo root |
| **What it does** | Behavior of the code as written |
| **What the test proved** | Assertion(s) in the named test file(s)—not a historical claim |
| **What it does not do** | Explicit non-claims from the module, docs, or tests |

CLI registration: only `caesar`, `vigenere`, and `substitution` sit in `engine.solvers.SOLVERS`. Keyed Vigenère is a separate CLI path (`solve keyed-vigenere`) that requires `--key` and `--alphabet`. Beam search, columnar, crib, EM aligner, German, neural, script tools, clustering, HMM, PMI, compression, mural analyzer, and OCR are importable modules (and some have docs); they are not blind “solve unknown ciphertext” entries in `SOLVERS`.

---

## Classical cipher solvers

### Caesar

| | |
| --- | --- |
| **Path** | [`engine/solvers/caesar.py`](../engine/solvers/caesar.py) |
| **What it does** | Tries all 26 shifts; keeps the candidate with the best English unigram score (`unigram_score`), recording χ² as a detail. Reinjects non-letters. Registered as `SOLVERS["caesar"]`. |
| **What the test proved** | `tests/test_recover.py`: round-trip encrypt/decrypt with the fixture shift; blind recovery of shift and plaintext from ciphertext built inside the test (solver is not given the shift). |
| **What it does not do** | Does not attack polyalphabetic, transposition, digraph, or modern ciphers; does not read undeciphered scripts. |

### Vigenère (standard A–Z)

| | |
| --- | --- |
| **Path** | [`engine/solvers/vigenere.py`](../engine/solvers/vigenere.py) |
| **What it does** | Proposes periods via Kasiski factors and column IC; solves each column as Caesar by unigram score; ranks full plaintext with the English quadgram model; prefers the shortest period near the best score. Registered as `SOLVERS["vigenere"]`. |
| **What the test proved** | `tests/test_recover.py`: round-trip keeps punctuation; Kasiski votes include the true key length; recovered key and plaintext match the fixture without the key being passed to the solver. |
| **What it does not do** | Does not search a keyword-mixed alphabet (use keyed Vigenère); does not handle digraph/Playfair/Enigma; not a script decipherment. |

### Monoalphabetic substitution (annealing)

| | |
| --- | --- |
| **Path** | [`engine/solvers/substitution.py`](../engine/solvers/substitution.py) |
| **What it does** | Seeds a key from ciphertext letter frequencies onto English unigram order, then simulated annealing + hill-climb + exhaustive swap polish to raise English quadgram log-likelihood. Records the neural trigram score as a second opinion only. Registered as `SOLVERS["substitution"]`. |
| **What the test proved** | `tests/test_recover.py`: round-trip with a 26-letter key; annealing from `DEMO_SEED` recovers plaintext and key. `tests/test_neural.py`: substitution result includes a neural second-opinion score. |
| **What it does not do** | Search objective is not the neural net; does not claim a script or language is solved; does not break transposition or polyalphabetic systems by itself. |

### Beam-search monoalphabetic substitution

| | |
| --- | --- |
| **Path** | [`engine/solvers/beam_search.py`](../engine/solvers/beam_search.py) |
| **What it does** | Extends a partial cipher→plain key one ciphertext symbol at a time (most frequent first), keeping the best partial keys under an add-k smoothed English unigram/bigram model fit on `engine/data/beam_english.txt`. Spaces preserved; bigrams scored inside words only. |
| **What the test proved** | `tests/test_beam_search.py`: on a synthetic substitution of held-out English prose, recovers the plaintext exactly at `beam_width=40` and beats the best of many random keys (letter accuracy > 0.5); model sample is not the plaintext; documents non-decipherment of ancient scripts; rejects short ciphertext. |
| **What it does not do** | Does not decipher Linear A, Indus, Rongorongo, Voynich, or other unknown scripts; not registered in `SOLVERS`. See [`docs/beam-search.md`](beam-search.md). |

### Keyed Vigenère (known key)

| | |
| --- | --- |
| **Path** | [`engine/solvers/keyed_vigenere.py`](../engine/solvers/keyed_vigenere.py) |
| **What it does** | Keyword-mixed alphabet + repeating key + index letter (Kryptos / NSA FOIA tableau style). Encrypt/decrypt and `solve_keyed_vigenere` when key and alphabet keyword are supplied. CLI: `python -m engine solve keyed-vigenere … --key … --alphabet … --index …`. |
| **What the test proved** | `tests/test_keyed_vigenere.py`: KRYPTOS mixed alphabet and published tableau rows; exact recovery of published K1 and K2 plaintext with the published keys; encrypt reproduces published ciphertext; with a plain A–Z alphabet it matches standard Vigenère; punctuation does not advance the key; **not** registered in `SOLVERS` as a blind solver. |
| **What it does not do** | Does not search for an unknown key; does not read or claim Kryptos K4. See [`docs/kryptos-k1.md`](kryptos-k1.md). |

### Columnar transposition (incl. Kryptos K3)

| | |
| --- | --- |
| **Path** | [`engine/solvers/columnar.py`](../engine/solvers/columnar.py) |
| **What it does** | Numerical keyword ranks; single- and double-width right-to-left columnar encrypt/decrypt on full rectangles; Sanborn-form helpers; `solve_kryptos_k3` recovers the published K3 reading; `solve_columnar` exposes general widths. |
| **What the test proved** | `tests/test_columnar_k3.py`: single- and double-width round-trips; exact match to published K3 plaintext (including DESPARATLY); default ciphertext matches the Wikipedia transcript used in-module; Sanborn rotation form matches double columnar; `solve_columnar` returns general-width results. |
| **What it does not do** | Does not read or claim Kryptos K4; not a blind break of arbitrary incomplete matrices without the published K3 route. |

### Vigenère crib drag

| | |
| --- | --- |
| **Path** | [`engine/solvers/crib.py`](../engine/solvers/crib.py) |
| **What it does** | Slides a known plaintext crib through a standard A–Z Vigenère ciphertext; keeps periods whose implied keystream is consistent and fully determined; scores full decrypts with the English model. Returns `CribHit` list (offset, period, key, checks, score, plaintext). |
| **What the test proved** | `tests/test_crib.py`: correct crib recovers fixture key, period, and plaintext without being given the key; wrong crib does not return the fixture plaintext or key. |
| **What it does not do** | Not a digraph-cipher solver; letters outside the crib are only a Vigenère hypothesis; not registered in `SOLVERS`. |

---

## Language scorers and classical analysis helpers

### English language model and unigram tools

| | |
| --- | --- |
| **Path** | [`engine/language.py`](../engine/language.py) |
| **What it does** | Published English unigram rates; χ² vs English; quadgram `LanguageModel` with backoff (tri/bi/uni) fit on `engine/data/english.txt`. Objective for substitution search and Vigenère period choice. |
| **What the test proved** | `tests/test_recover.py` `test_ngrams_and_model_prefer_english`: model scores real prose above a shuffle. Used implicitly by Caesar/Vigenère/substitution/crib recovery tests. |
| **What it does not do** | Not a language identifier for arbitrary scripts; not a decipherment of unknown writing systems. |

### Index of coincidence, Friedman, Kasiski

| | |
| --- | --- |
| **Path** | [`engine/stats.py`](../engine/stats.py) |
| **What it does** | Letter counts, IC, Friedman period estimate, n-gram counts, Kasiski repeated-distance factors, column-mean IC. Used by Vigenère solver and `python -m engine analyze`. |
| **What the test proved** | Exercised via Vigenère Kasiski recovery in `tests/test_recover.py` (true period among Kasiski votes). No separate ancient-script claim. |
| **What it does not do** | Does not recover plaintext alone; does not apply to non–Latin-letter streams unless you map them to A–Z first. |

### Forward classical maps

| | |
| --- | --- |
| **Path** | [`engine/ciphers.py`](../engine/ciphers.py) |
| **What it does** | Encrypt/decrypt Caesar, Vigenère, and substitution for fixtures, demo, and tests. |
| **What the test proved** | Round-trips in `tests/test_recover.py`; used to build ciphertext that solvers must recover without the key. |
| **What it does not do** | Solvers must not be fed the secret through these maps and then called a recovery (see [`docs/TESTING.md`](TESTING.md)). |

### Alphabet / letter stream utilities

| | |
| --- | --- |
| **Path** | [`engine/alphabet.py`](../engine/alphabet.py) |
| **What it does** | A–Z helpers: `letters_only`, int encode/decode, reinject casing and non-letters. |
| **What the test proved** | Used throughout recovery and analysis tests (not a standalone decipherment test). |
| **What it does not do** | Not a cipher solver. |

### German letter scorer

| | |
| --- | --- |
| **Path** | [`engine/german.py`](../engine/german.py) |
| **What it does** | 26-letter German unigram + quadgram model fit on a Grimm fairy-tale excerpt (`engine/data/german_excerpt.txt`); folds ä/ö/ü/ß → ae/oe/ue/ss. Helpers to score logged Truppenschlüssel Nr. 86 failure strings for resemblance only. |
| **What the test proved** | `tests/test_german.py`: held-out German prose scores above random letters; training excerpt is not the unsolved ciphertext; logged Nr. 86 failure approaches score below German prose. |
| **What it does not do** | Not a full German orthography model; does not decipher Truppenschlüssel / Enigma / Nr. 86; a higher score is resemblance to the Grimm sample, not a plaintext. |

### Neural English trigram scorer

| | |
| --- | --- |
| **Path** | [`engine/neural.py`](../engine/neural.py) |
| **What it does** | Small trigram neural LM (one-hot → tanh → softmax); trained on Alice excerpt (`engine/data/alice_excerpt.txt`). Second opinion beside quadgrams; numpy backend when available, else pure Python. |
| **What the test proved** | `tests/test_neural.py`: prefers held-out English over random letters; training loss drops; training prose is not the solver fixtures; substitution solver records a neural second-opinion field. |
| **What it does not do** | Not the substitution search objective; not a reading of Linear A, Voynich, or Vesuvius scrolls. |

### Compression / zlib language score

| | |
| --- | --- |
| **Path** | [`engine/compression_score.py`](../engine/compression_score.py) |
| **What it does** | `language_score` = raw UTF-8 bytes / zlib compressed bytes; `cross_entropy_bits_per_byte`; `compare_to_shuffle` vs a seeded character permutation. |
| **What the test proved** | `tests/test_compression_score.py`: English and German fixtures rank above a shuffle; score matches raw/compressed definition; rejects empty/non-str; documents that it does not decipher ancient scripts. |
| **What it does not do** | Does not decipher ancient scripts; not language ID; not a translation. See [`docs/compression-language-score.md`](compression-language-score.md). |

---

## Unknown-script / sign-stream analysis (not decipherment)

### Script tools (inventory, repeats, bilingual crib check)

| | |
| --- | --- |
| **Path** | [`engine/script_tools.py`](../engine/script_tools.py) |
| **What it does** | Tokenize sign corpora; frequency inventory; find repeated n-grams; apply a supplied sign→gloss map and check a bilingual crib against a synthetic lexicon (`engine/data/synthetic_sign_corpus.txt`, `engine/data/synthetic_bilingual.json`). |
| **What the test proved** | `tests/test_script_tools.py`: fixture inventory/frequencies; tokenizer skips comments/commas; finds repeated bigrams; correct map matches synthetic lexicon and wrong map is rejected; unmapped signs skipped; fixture files are UTF-8. |
| **What it does not do** | Does not decipher Linear A, Voynich, Rongorongo, Indus, or any other undeciphered script. Measurements are only vs inputs you supply. |

### EM sign-to-letter aligner

| | |
| --- | --- |
| **Path** | [`engine/solvers/em_sign_aligner.py`](../engine/solvers/em_sign_aligner.py) |
| **What it does** | Knight-style EM: fixed English bigram source; learn P(sign|letter) by Baum–Welch; map signs (labels like `U+E00A`) to letters. Requires numpy. |
| **What the test proved** | `tests/test_em_sign_aligner.py`: scope string names scripts it does not read; recovers most of a random synthetic sign map held back from the aligner (may skip without numpy). |
| **What it does not do** | Does not read Linear A, Indus, or Voynich; not in `SOLVERS`; synthetic-map accuracy is not a historical decipherment. See [`docs/em-sign-aligner.md`](em-sign-aligner.md). |

### Sign clustering

| | |
| --- | --- |
| **Path** | [`engine/sign_cluster.py`](../engine/sign_cluster.py) |
| **What it does** | Co-occurrence vectors; k-means and average-linkage hierarchical clustering of symbols by neighbor context. Numpy required. |
| **What the test proved** | `tests/test_sign_cluster.py`: disclaimer present; k-means and hierarchical partitions beat chance on a synthetic vowel/consonant alternating corpus; same seed is repeatable; class labels unused by the clusterer. |
| **What it does not do** | A cluster is not a sound, word, or reading of Linear A / Indus / Rongorongo / Phaistos / Voynich. See [`docs/sign-clustering.md`](sign-clustering.md). |

### First-order HMM (Baum–Welch)

| | |
| --- | --- |
| **Path** | [`engine/hmm_baum_welch.py`](../engine/hmm_baum_welch.py) |
| **What it does** | Fit a small discrete first-order HMM by Baum–Welch; Viterbi path; synthetic two-state corpus generator; accuracy after best label flip. |
| **What the test proved** | `tests/test_hmm_baum_welch.py`: recovered states beat constant-majority chance on a synthetic two-state draw; module documents non-decipherment; rejects short/unknown symbol inputs. |
| **What it does not do** | Does not decipher ancient scripts; state path ≠ translation or phonetic values. See [`docs/hmm-baum-welch.md`](hmm-baum-welch.md). |

### Pairwise mutual information

| | |
| --- | --- |
| **Path** | [`engine/pairwise_mutual_information.py`](../engine/pairwise_mutual_information.py) |
| **What it does** | Ranks ordered adjacent sign pairs by PMI (and contribution to MI); grouped spans avoid cross-boundary pairs. |
| **What the test proved** | `tests/test_pairwise_mutual_information.py`: planted pair ranks first and stays stable across seeds; short stream empty; independent pair PMI ~ 0; grouped spans do not cross boundaries; module states it does not decipher. |
| **What it does not do** | Does not decipher ancient scripts; top pair is a count, not a word or sound. See [`docs/pairwise-mutual-information.md`](pairwise-mutual-information.md). |

---
