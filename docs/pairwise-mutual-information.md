# Pairwise mutual information of adjacent signs

Unsupervised description of a transcription. New files only: `engine/pairwise_mutual_information.py` and `tests/test_pairwise_mutual_information.py`. This note does not change solvers, image assets, or other unsupervised experiments.

## What it does not do

This tool does **not** decipher ancient scripts. It does not read Linear A, the Voynich manuscript, Rongorongo, the Indus script, Cypro-Minoan, the Phaistos Disc, or any other undeciphered text. It does not name a language. It does not assign phonetic values.

A pair that ranks first is more tightly associated, in the token stream you supplied, than the other observed neighbor pairs. That is a count. It is not a word, a sound, or a translation. The same statistic lights up on a synthetic corpus built to contain one planted pair. Structure in a real inscription still needs an edition, a sign list, and an external check before anyone talks about a reading. See [methods.md](methods.md).

## What it computes

For a flat sequence of signs, each sign is paired with the next one. Let `N` be the number of those adjacent pairs.

- `P(left, right) = count(left, right) / N`
- `P(left)` and `P(right)` are the marginals of that same pair stream
- Pointwise mutual information, in bits:

```text
PMI(left, right) = log2( P(left, right) / (P(left) P(right)) )
```

- The pair's contribution to mutual information is `P(left, right) * PMI(left, right)`
- `I(left; right)` is the sum of those contributions over observed pairs

Pairs that never occur are omitted. There is no smoothing, so PMI is only defined for pairs that were seen. Ranking is PMI descending, then count descending, then the sign strings. A positive PMI means the ordered pair occurred more often than the product of its marginals (more often than chance under independence).

`pairwise_mutual_information_grouped` pools several spans and does not count a pair that would exist only because two lines were pasted together.

## Synthetic test

`tests/test_pairwise_mutual_information.py` builds a corpus of invented labels. Background signs are drawn independently from a separate alphabet. The ordered pair `QX ZY` is then inserted so that its count is more than five times `N * P(QX) * P(ZY)`. The test requires that pair to rank first, with a strictly higher PMI than the second-ranked pair. The check is repeated on twenty seeds.

Passing that test means the ranker notices a pair that was planted. It does not mean an ancient script was deciphered.
