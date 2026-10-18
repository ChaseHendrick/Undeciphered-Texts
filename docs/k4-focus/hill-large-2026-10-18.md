# K4 in place under Hill 5 by 5 to 10 by 10, 18 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null in every report.

This follows [Hill to 4 by 4](unknown-alphabets-hill-2026-10-18.md), which closed sizes 2 to 4 by trying every row. From size 5 up the two published clues, EASTNORTHEAST at 21 and BERLINCLOCK at 63 (zero-based), give at most four known blocks, so a row is not pinned and listing 26^n rows per row is too slow. Code: `engine/k4_hill_large.py`. Tests: `tests/test_k4_hill_large.py`.

Model: p = M c mod 26 on blocks of n letters starting at the alignment, every alignment 0 to n-1, letters numbered A-Z or by the KRYPTOS, PALIMPSEST or ABSCISSA keyed alphabets. Letters before the first block and after the last full block are left out. Nothing here moves letters.

## Method

Row j of M must satisfy r . c_b = p_b[j] mod 26 for every block b wholly inside a clue. That system is solved exactly over GF(2) and over GF(13) by Gaussian elimination and joined by the Chinese remainder theorem, so a row's solution count mod 26 is 2^(n - rank mod 2) times 13^(n - rank mod 13), or 0 when it is inconsistent mod either prime.

A setting is excluded only if some row is inconsistent, or no choice of fitted rows is invertible mod 26. The second test is exact: over a field an invertible M with M c_b = p_b on every known block exists exactly when the rows are consistent and the known cipher blocks and the known plain blocks have the same rank. The rank of the plain blocks is fixed by the clues alone, whatever the key. The row counts were checked against brute force over all 26^5 rows for every 5 by 5 setting, and the rank exclusions were checked by listing every row choice mod 2 (1,024 or 32 choices); both agree.

The held-back fold fits one clue and predicts the other. A letter is forced only when every fitted row gives the same value, which happens when its cipher block is orthogonal to the null space mod 2 and mod 13.

## Results, 5 by 5

C rank and P rank are the ranks of the known cipher blocks and known plain blocks, mod 2 and mod 13. Row counts are mod 26.

| Numbering | Alignment | Known blocks | C rank mod 2, 13 | P rank mod 2, 13 | Rows consistent | Solutions per row | Result |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| A-Z | 0 | 2 | 2, 2 | 2, 2 | yes | 17,576 each | open, out of reach |
| A-Z | 1 | 3 | 3, 3 | 3, 3 | yes | 676 each | open, out of reach |
| A-Z | 2 | 3 | 2, 3 | 3, 3 | no | 0, 0, 1352, 0, 1352 | excluded |
| A-Z | 3 | 4 | 3, 4 | 4, 4 | no | 52, 52, 52, 0, 52 | excluded |
| A-Z | 4 | 4 | 4, 4 | 4, 4 | yes | 26 each | open, enumerated |
| KRYPTOS | 0 | 2 | 2, 2 | 2, 2 | yes | 17,576 each | open, out of reach |
| KRYPTOS | 1 | 3 | 3, 3 | 2, 3 | yes | 676 each | excluded, no invertible key |
| KRYPTOS | 2 | 3 | 3, 3 | 2, 3 | yes | 676 each | excluded, no invertible key |
| KRYPTOS | 3 | 4 | 3, 4 | 4, 4 | no | 0, 52, 0, 0, 0 | excluded |
| KRYPTOS | 4 | 4 | 4, 4 | 4, 4 | yes | 26 each | open, enumerated |
| PALIMPSEST | 0 | 2 | 2, 2 | 2, 2 | yes | 17,576 each | open, out of reach |
| PALIMPSEST | 1 | 3 | 3, 3 | 3, 3 | yes | 676 each | open, out of reach |
| PALIMPSEST | 2 | 3 | 3, 3 | 2, 3 | yes | 676 each | excluded, no invertible key |
| PALIMPSEST | 3 | 4 | 4, 4 | 3, 4 | yes | 26 each | excluded, no invertible key |
| PALIMPSEST | 4 | 4 | 3, 4 | 2, 4 | no | 0, 0, 0, 52, 0 | excluded |
| ABSCISSA | 0 | 2 | 2, 2 | 2, 2 | yes | 17,576 each | open, out of reach |
| ABSCISSA | 1 | 3 | 3, 3 | 2, 3 | yes | 676 each | excluded, no invertible key |
| ABSCISSA | 2 | 3 | 3, 3 | 2, 3 | yes | 676 each | excluded, no invertible key |
| ABSCISSA | 3 | 4 | 4, 4 | 4, 4 | yes | 26 each | open, enumerated |
| ABSCISSA | 4 | 4 | 4, 4 | 3, 4 | yes | 26 each | excluded, no invertible key |

So 11 of the 20 settings are excluded by the clues alone, with no language model. Every exclusion is a parity effect: it comes from the rank mod 2, never mod 13. Of the 9 open settings, 3 have four known blocks and were enumerated in full, and 6 have two or three blocks and are out of reach (below).

Held-back folds: no letter is forced in any 5 by 5 setting in either fold. Fitting one clue leaves at most two known blocks, so each row keeps at least three free parameters and every reserved letter stays free.

## Results, 6 by 6 to 10 by 10

For every size 6 to 10, every alignment and all four numberings, every row is consistent and an invertible fit exists, so nothing is excluded. The ranks mod 2 and mod 13 of the cipher and plain blocks all equal the block count. The block count depends only on size and alignment, not on the numbering. No held-back letter is forced in any fold (0 right, 0 wrong across all 180 settings of sizes 5 to 10).

| Size | Alignments | Known blocks | Free parameters per row | Solutions per row | Row choices in all |
| ---: | --- | ---: | ---: | ---: | ---: |
| 6 | 3, 4 | 3 | 3 | 17,576 | 26^18, about 2.9e25 |
| 6 | 0, 1, 2, 5 | 2 | 4 | 456,976 | 26^24, about 9.1e33 |
| 7 | 0 to 4 | 2 | 5 | 11,881,376 | 26^35, about 3.3e49 |
| 7 | 5, 6 | 1 | 6 | 308,915,776 | 26^42, about 2.7e59 |
| 8 | 0, 1, 2, 7 | 2 | 6 | 308,915,776 | 26^48, about 8.3e67 |
| 8 | 5, 6 | 1 | 7 | 8,031,810,176 | 26^56, about 1.7e79 |
| 8 | 3, 4 | 0 | 8 | 26^8 | 26^64, about 3.6e90 |
| 9 | 0 to 7 | 1 | 8 | 26^8 | 26^72, about 7.6e101 |
| 9 | 8 | 0 | 9 | 26^9 | 26^81, about 4.1e114 |
| 10 | 3, 4 | 2 | 8 | 26^8 | 26^80, about 1.6e113 |
| 10 | 1, 2 | 1 | 9 | 26^9 | 26^90, about 2.2e127 |
| 10 | 0, 5, 6, 7, 8, 9 | 0 | 10 | 26^10 | 26^100, about 3.1e141 |

Exhaustive enumeration is not feasible for any of these. The smallest, 26^18, is about 2.5e18 times the 5 by 5 space that takes under a second here. These settings are untested by the clues, not supported.

## 5 by 5 enumeration

With four known blocks of rank 4 each row has 26 solutions, so there are 26^5 = 11,881,376 clue-consistent row choices. All of them were scored. The quadgram total over the block span splits into five tables, one per starting row, each over the four rows a quadgram window touches, so the whole space is scored by adding tables. Index of coincidence over the decrypt outside the clues splits the same way into per-row and pairwise terms. The top 2,000 by each score were deciphered, non-invertible keys were dropped, and the top 20 invertible keys were kept. Scores use `engine.language.get_model()` (discounted quadgrams, fit on `neural_train_public.txt`) over the 90 letters of the block span (87 quadgrams); per-quadgram is that total divided by 87.

English baseline: 239 non-overlapping 97-letter windows of held-out English (`neural_heldout_doyle.txt` and `neural_audit_wells.txt`, neither in the training file; comment lines dropped), both clues planted, scored the same way.

| Setting | Keys | Time | Best K4 per-quadgram | 20th best | Best K4 IoC (its per-quadgram) |
| --- | ---: | ---: | ---: | ---: | --- |
| A-Z, alignment 4 | 11,881,376 | 0.74 s | -4.767 | -4.952 | 0.0751 (-6.407) |
| KRYPTOS, alignment 4 | 11,881,376 | 0.71 s | -5.093 | -5.231 | 0.0685 (-6.967) |
| ABSCISSA, alignment 3 | 11,881,376 | 0.82 s | -5.085 | -5.264 | 0.0718 (-6.530) |

| Comparison, alignment 4 (alignment 3 in brackets) | Per-quadgram |
| --- | --- |
| Held-out English with clues planted, minimum of 239 | -2.672 (-2.648) |
| Same, 5th percentile | -2.533 (-2.538) |
| Same, median | -2.236 (-2.232) |
| True key in the 90 English planted controls, range | -2.672 to -1.895, median -2.232 |
| Null control: clues planted in uniform random letters, best of 26^5 keys, 20 seeds | -5.116 to -4.258, median -4.696 (-5.135 to -4.306, median -4.824) |

The best K4 decrypt at every enumerated setting scores far below the worst English window and inside the range of the best key found on random letters. Nothing at these settings looks like English. The best A-Z decrypt, shown only to make the point, is `obkrIEQWTHBNZLEDTWEDLWHITNORTHEASTCHICHWELXKEFXDOQUAHGIARNMENJYVERLINCLOCKGONCAHWKVPAYDEFYKISQcar` (lower case: ciphertext letters outside full blocks); it reads as noise apart from the planted clue letters.

The language-agnostic scores do not rescue any key. The highest IoC among K4 keys (0.0751, A-Z) comes from piles of X and similar repeats and has per-quadgram -6.41; the held-out English IoC median outside the clues is 0.063 (range 0.047 to 0.104) and unigram entropy median 3.92 bits (range 3.48 to 4.20). But IoC has little power here: in the planted English controls the median IoC rank of the true key was 963 to 6,062 of 11.9M per group at 26^5 keys, and 9,124 and 238,086 in the two 52^5 groups; it ranked first in only 2 of 90 controls. On 97 letters, IoC and entropy alone cannot pick the key out of 26^5 choices; the quadgram score can.

## Planted-control power

Each control plants both clues in a random held-out English window, enciphers every full block with a random invertible 5 by 5 key at the same alignment and numbering, and runs the same enumeration. The true key is never excluded.

| Numbering | Alignment | Controls | Keys each | True key first of all keys | True key first among invertible keys | Time each |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A-Z | 3 | 20 | 26^5 | 20 | 20 | 0.67 to 0.92 s |
| A-Z | 4 | 20 | 26^5 | 20 | 20 | 0.70 to 0.94 s |
| KRYPTOS | 3 | 10 | 26^5 | 9 | 10 | 0.76 to 0.86 s |
| KRYPTOS | 4 | 10 | 26^5 | 10 | 10 | 0.69 to 0.91 s |
| PALIMPSEST | 3 | 10 | 52^5 | 10 | 10 | 33 to 42 s |
| PALIMPSEST | 4 | 10 | 104^5 | not run | not run | out of reach |
| ABSCISSA | 3 | 10 | 26^5 | 9 | 9 | 0.85 to 1.01 s |
| ABSCISSA | 4 | 10 | 52^5 | 10 | 10 | 33 to 39 s |

Recovery: 88 of 90 enumerated controls rank the true key first of all row choices, and 89 of 90 rank it first among invertible keys. The one miss (ABSCISSA, alignment 3, seed 3001) put the true key at rank 15 (10th invertible); the winning key differs in one row and its decrypt still reads as the same English with a few letters wrong (`NOWEMIAN` for `BOHEMIAN`). Where the true key won, its margin over the best other key was at least 15.4 log units (median 57.0). The keys per control depend on the numbering because the rank of the planted plain blocks is fixed by the clues: PALIMPSEST at alignment 3 and ABSCISSA at alignment 4 have plain rank 3 mod 2, so every planted key leaves 52 solutions per row, and PALIMPSEST at alignment 4 has plain rank 2 mod 2, so 104 per row.

## Out of reach at 5 by 5

Six open settings have fewer than four known blocks. A-Z, KRYPTOS, PALIMPSEST and ABSCISSA at alignment 0 have two blocks, 17,576 solutions per row and 26^15, about 1.7e21, row choices. A-Z and PALIMPSEST at alignment 1 have three blocks, 676 per row and 676^5, about 1.4e14, row choices. At the measured 1.6e7 keys per second on one core, 1.4e14 keys is about 100 days per setting, and the score tables would need 676^4, about 2.1e11, entries each. No bounded search was run on these; they are untested, not supported.

## What this does not cover

- Any model that moves letters before or after the Hill layer, or that enciphers letters outside full blocks.
- Affine Hill (p = M c + v mod 26), and Hill with different numberings on the cipher and plain sides.
- The six 5 by 5 settings with two or three known blocks, and every size from 6 to 10. The clues neither exclude nor test them.
- Numberings other than A-Z, KRYPTOS, PALIMPSEST and ABSCISSA.
- Plaintext languages other than English for the quadgram ranking. The exclusions are language-free; the "nothing looks like English" finding is English only, and IoC and entropy, which are language-free, were shown to lack power at this length.

Run: `python3 -m engine.k4_hill_large` (the table, under a second) and `python3 -m engine.k4_hill_large enumerate` (all 5 by 5 enumerations, 239-window baseline, 100 planted controls and 40 null controls: 844 s on one core, most of it the twenty 52^5 controls). Test: `python3 -m unittest tests.test_k4_hill_large` (6 tests, about 11 s).
