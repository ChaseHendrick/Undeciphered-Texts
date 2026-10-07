# Latin under double columnar transposition: power by size, 7 October 2026

Not a reading. No letter string is stored. The cells were not searched.

The [double transposition pass](dagapeyeff-double-2026-10-05.md) closed every pair of orders to width 6 with a key-invariant score whose power was shown on English and German. `engine.dagapeyeff_latindouble` anneals both column orders and the letter key together under the Latin quadgram model (`engine/dagapeyeff_latindouble.c`, 4 restarts of 8,000,000 steps, short last rows allowed). Three planted held-out Thomistic windows per size test it. A text counts as recovered when at least 90 percent of its cells get their true letter and the found score is within 0.1 a letter of the true text's. A right key under wrong orders is not a reading.

| Widths | Recovered | Found, per letter, when missed |
| --- | --- | --- |
| 4 by 5 | 3 of 3 | |
| 5 by 7 | 3 of 3 | |
| 6 by 8 | 1 of 3 | -3.34, -3.67 |
| 7 by 9 | 0 of 3 | -3.56 to -3.78 |
| 9 by 11 | 0 of 3 | -3.40 to -3.80 |

The true texts score -1.46 to -2.31 a letter, so a missed search is a search failure, not a model that prefers a wrong text. In one 6 by 8 miss the key was 98 percent right while the orders were wrong. A scratch two-phase variant, which set the orders first by a key-invariant count of repeated pairs and triples, did worse: that count has spurious maxima above the true orders even at 5 by 7.

The joint search has Latin power only at sizes the key-invariant search already closed. Latin under double transposition at larger widths stays open; divide-and-conquer methods for double transposition exist but assume known letters.

Not a reading. No letter string is stored.
