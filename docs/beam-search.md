# Beam-search decipherment

`engine/solvers/beam_search.py` searches a **monoalphabetic substitution** of Latin letters. It is a classical cipher exercise on synthetic ciphertext, not a method for undeciphered writing.

## What this does not do

This beam search **does not decipher ancient scripts**. It does not read Linear A, the Indus script, Rongorongo, the Voynich manuscript, or any other unknown writing system. A string that scores well is only an English-letter hypothesis under a unigram and bigram model. It is not a translation, a sign reading, or evidence that an ancient script has been solved.

## Model

`engine/data/beam_english.txt` is original English prose included with this solver (UTF-8). The fitter counts A–Z unigrams and word-internal bigrams and stores add-k smoothed log probabilities. Accented letters are treated as separators so they never enter the 26-letter tables.

## Search

1. Split the ciphertext into A–Z words. Spaces and punctuation stay in the skeleton and are written back into the plaintext.
2. Extend a partial cipher-to-plain key one ciphertext symbol at a time, most frequent symbol first. Each symbol receives a still-unused plaintext letter.
3. Score a partial key by the English unigram of every mapped letter plus the conditional bigram of every word-internal pair whose two symbols are both mapped. At a given depth every beam has mapped the same ciphertext symbols, so the scores are comparable.
4. Keep the `beam_width` best partial keys and repeat until every symbol that occurs in the text is mapped.

The default width is 80. On the held-out paragraph in `tests/test_beam_search.py`, a width of 40 already recovers the plaintext exactly, which is far above a random key (about one letter in twenty-six by chance).

## Test

`tests/test_beam_search.py` builds a synthetic substitution with `substitution_encrypt`, runs the beam search, and checks that letter accuracy beats the best of several seeded random keys. The plaintext is not copied from the model sample.
