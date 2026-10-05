# Columnar transposition under a letter key, 5 October 2026

The plainest classical hypothesis for the challenge is a Polybius substitution followed by a complete columnar transposition: plaintext written in rows of a width that divides 196, columns copied out in key order. Earlier passes scored random column keys by successive-symbol information, and ran the substitution solver with the legacy model, which recovered 1 of 8 known 200-letter substitutions. This pass anneals the column order and the letter key together under the default model: 4 restarts of 60,000 steps.

Width 1 is plain substitution. Each width has two planted controls, training prose with J folded into I, a random column order and a random letter key. A control counts only when every letter comes back.

| Width | Planted recovered | Cells | Regrouped cells | Shuffles as high as the cells |
| --- | --- | --- | --- | --- |
| 1 | 2 of 2 | -3.968 | -3.9946 | 3 of 4 |
| 2 | 2 of 2 | -3.8921 | -3.9727 | 1 of 4 |
| 4 | 2 of 2 | -3.9666 | -3.9553 | 4 of 4 |
| 7 | 2 of 2 | -3.8212 | -3.8994 | 4 of 4 |
| 14 | 0 of 2 | -3.4168 | -3.8538 | 0 of 4 |

The planted texts score -2.0111 and -1.9207 a letter. At widths 1 to 7 the search has shown it can find a planted text, and the cells land where shuffled cells land, nearly two units a letter under English. Plain substitution, and complete columnar transposition at widths 2, 4 and 7 with a substitution, do not read the cells in English.

Width 14 recovered neither planted text, so it closes nothing. A larger budget, 6 restarts of 250,000 steps, also recovered 0 of 3 planted width-14 texts. Tiago Rodrigues reported the same limit on Cipher Mysteries in 2014: his permutation and substitution solver needed about 240 letters for a 14-column key.

The cells beat 4 of 4 shuffles at width 14, so `engine.dagapeyeff_columnar14` searched the cells again under a new seed against 20 plain shuffles and 20 shuffles that keep the rare-symbol column in place. The cells scored -3.6146 this time, and 13 of 20 plain shuffles and 10 of 20 kept-column shuffles did as well. The earlier 0 of 4 was a small draw. The same cells scored 0.2 apart under two seeds, which is the size of this search's noise.

Not a reading. No letter string is stored.
