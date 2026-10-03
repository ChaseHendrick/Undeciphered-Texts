# EM sign-to-letter aligner

`engine/solvers/em_sign_aligner.py` is a small expectation-maximization aligner
in the sense of Knight and Yamada (1999): a known language model is the source,
and a noisy channel from letters to unknown signs is what gets learned.

## What it does

1. Fit an English letter bigram on plaintext you already know.
2. Build a synthetic sign text by replacing each letter of a *different*
   English passage with one sign from a random bijection. Signs are labels
   such as `U+E00A`, not A-Z.
3. Run Baum-Welch. The bigram stays fixed. Only P(sign | letter) moves.
4. Read the map off the posterior: each observed sign goes to its most likely
   letter.

The unit test `tests/test_em_sign_aligner.py` generates that synthetic corpus
from `engine/data/english.txt`, holds the true map back from the aligner, and
requires the learned map to agree on most signs. Numpy performs the updates.
Without numpy the recovery test skips; the rest of this repository stays on
the standard library.

```bash
python3 -m unittest tests.test_em_sign_aligner -v
```

## What it does not do

This aligner does not read Linear A, the Indus script, or the Voynich
manuscript. It does not take those corpora as input, and a high score on the
synthetic map is not a decipherment of any historical writing. It is also not
registered in `engine.solvers.SOLVERS`, so the classical demo and CLI will
not present its output as a solution of an unknown script.

Rare English letters can still trade places. The test asks for most of the
sign map, not a perfect key and not a translation.
