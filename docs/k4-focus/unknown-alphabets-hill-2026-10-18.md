# K4 in place on unknown alphabets, and Hill to 4 by 4, 18 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

Two exact checks that use only the two published clues, EASTNORTHEAST at 21 and BERLINCLOCK at 63. Neither scores the rest of the text against English or any other language, so a blocked model is blocked whatever language the other 73 letters are in. Both apply to ciphers that keep every letter in its place. Nothing here speaks to models that move letters.

## Lane 1: unknown keyed alphabets, Z3

`engine.k4_alphabet_csp`, with the optional `z3-solver` (5.3.1 here; CI pins 5.1.0.0). Every alphabet is a free permutation, so a blocked period holds for every keyword, not only KRYPTOS, PALIMPSEST and ABSCISSA. Both clues are used together. `unsat` means no alphabet, keyword, key or primer of the family places both clues.

Periods and lags 1 to 96 were checked for each of ten families. Z3 returned no `unknown`. A control plants both clues under a random key of each family; it is never blocked.

| Family | Blocked for every alphabet | Not blocked |
| --- | --- | --- |
| Quagmire III, Vigenere sense (straight Vigenere; K1 and K2's keyed Vigenere with any keyword) | 1 to 26, 31 to 40, 42 to 52 | 27 to 30, 41, 53 to 96 |
| Quagmire III, Beaufort sense | 1 to 22, 24, 25, 34 to 45, 48, 50 | 23, 26 to 33, 46, 47, 49, 51 to 96 |
| Quagmire I (keyed plain, straight cipher) | 1 to 12, 14, 15, 17, 18, 20 to 22, 25, 34, 36, 37, 40, 42 to 45, 50 | 13, 16, 19, 23, 24, 26 to 33, 35, 38, 39, 41, 46 to 49, 51 to 96 |
| Quagmire II (straight plain, keyed cipher) | 1 to 15, 17, 18, 21, 22, 25, 34 to 36, 41 to 45, 50 | 16, 19, 20, 23, 24, 26 to 33, 37 to 40, 46 to 49, 51 to 96 |
| Quagmire IV (two keyed alphabets) | 1 to 7, 9 to 12, 14, 15, 17, 18, 21, 22, 25, 34, 36, 42 to 45, 50 | 8, 13, 16, 19, 20, 23, 24, 26 to 33, 35, 37 to 41, 46 to 49, 51 to 96 |
| Progressive Quagmire III, step 1 to 25 per cycle | 1 to 7, 9, 14, 15, 19, 21, 38, 41, 42, 45 | the rest |
| Ciphertext autokey, one keyed alphabet, any tableau row map, lag L | 1 to 7, 9 to 23, 25 to 36, 40, 42, 45, 47, 49 to 55, 58, 59, 63, 65, 66, 68 | 8, 24, 37 to 39, 41, 43, 44, 46, 48, 56, 57, 60 to 62, 64, 67, 69 to 96 |
| Ciphertext autokey, two keyed alphabets | 1, 2, 5 to 7, 9, 13, 14, 16 to 21, 23, 25, 27 to 31, 33, 35, 42, 49, 50, 53, 55, 58, 65 | the rest |
| Plaintext autokey, one keyed alphabet, lag L | 1 to 5, 9, 40 to 43, 45 | 6 to 8, 10 to 39, 44, 46 to 96 |
| Plaintext autokey, two keyed alphabets | 1 to 4, 42 | the rest |

The rows agree with each other where they must. Quagmire IV contains I, II and III, and every period it blocks is blocked for all three. The earlier [bijection bound](periodic-bijection-2026-10-07.md) allows any alphabet in every column, and every period it blocks is blocked in every periodic row here.

The keyed Vigenere row is the one that matters most, because K1 and K2 used it. It is blocked at every period from 1 to 26 for any keyword and any alphabet. Part of the reason is plain: S enciphers to S at 32 and K to K at 73, so under one alphabet those columns have shift 0, and no other clue letter in those columns may change.

## Held-back check on what is not blocked

For every family and period up to 32 that the clues do not block, one clue was fitted and the other held back. A held-back letter is forced when no other plaintext letter can be completed from the fit.

That leaves 137 settings across the ten families, each run in both folds: 3,288 held-back letters in all. 8 were forced right, none was forced wrong, and 3,280 were free. The forced letters come from four settings (Quagmire I, II and IV at period 19, and two-alphabet ciphertext autokey at lag 12), one letter in each fold. So the clues can block these families at many periods, but where they do not block, they cannot test them: a key fitted on one clue says almost nothing about the other. These settings are untested, not supported.

## Lane 2: Hill, 2 by 2 to 4 by 4

`engine.k4_hill_rows`. Deciphering is p = M c mod 26, one block of n letters at a time. Row j of M has to send every ciphertext block whose plaintext is known to that block's j-th letter. All 26^n candidate rows are tried, so nothing is sampled. Blocks may start at any of the n alignments. Letters are numbered A to Z or by the KRYPTOS, PALIMPSEST or ABSCISSA keyed alphabets.

All 36 settings (3 sizes, every alignment, 4 numberings) are blocked. At 2 by 2 and 3 by 3 no row fits at all. At 4 by 4 a few rows fit, but no choice of them is invertible mod 26.

The control plants both clues under a random invertible key at every setting. None is blocked. The check also has power: at 3 by 3, alignment 1, EASTNORTHEAST alone pins all 11 letters of BERLINCLOCK under a planted key (`tests/test_k4_alphabet_csp.py`).

## What this does not cover

- Any model that moves letters before or after the substitution. The open layered family stays open.
- Periods and lags in the "not blocked" column, which the clues cannot test.
- Hill at 5 by 5 and above, where two clues give too few known blocks to pin a row, and Hill on letter numberings other than the four listed.
- Running keys from texts other than K3. A running key is not periodic, so the bounds here do not apply.

Run: `python3 -m engine.k4_alphabet_csp 96 4` (about 2 minutes on 4 cores) and `python3 -m engine.k4_hill_rows` (under a second).
