# Sign clustering (distributional only)

`engine/sign_cluster.py` groups transcribed symbols that keep similar
neighbors. Each symbol becomes a co-occurrence vector (counts of the symbols
to its left and to its right, inside a word). NumPy k-means, with
average-linkage hierarchical clustering as a second method, cuts those vectors
into groups.

**This does not decipher an ancient script.** A cluster is not a phonetic
value, a translation, or a reading. It does not decipher Linear A, the Indus
script, Rongorongo, the Phaistos disc, or the Voynich manuscript. It only
reports which symbols in *your* transcription share contexts.

## What the unit test actually checks

`tests/test_sign_cluster.py` builds a synthetic corpus. Two symbol classes are
generated on purpose: one class plays the role of vowels, the other of
consonants. Words strictly alternate consonant, vowel, consonant, vowel.
Symbols are invented labels (`C0`, `V0`, …), not signs from a historical
inscription.

The clusterer is not given those class labels. After k-means (and, separately,
hierarchical clustering) the test scores the partition by the better of the
two ways to match clusters onto the two classes. That accuracy has to beat a
chance baseline: the same partition scored against class labels that have been
randomly shuffled, class sizes held fixed. Beating chance on this toy
generator only shows that the method can see a context difference that was
built in. It is not evidence about any real undeciphered text.

## How to run

NumPy is required for this module. The rest of the classical engine stays on
the standard library.

```bash
python3 -m unittest tests.test_sign_cluster -v
```

Files in this change are UTF-8 text. The README hero JPEG is not part of it.
