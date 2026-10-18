# K4 column orders at widths 11 to 16, 18 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

This extends [transposition plus substitution](transposition-substitution-2026-10-18.md), which checked every column order to width 10, to widths 11 to 16. The model, the conventions and the four strong variants are the same: columnar transposition with an incomplete last row, either reading direction, either order of composition with a periodic Vigenere or Beaufort on A-Z or the KRYPTOS alphabet, on the 97 carved letters or 98 with the question mark that ends K3. Only the two clues are used (EASTNORTHEAST at 21, BERLINCLOCK at 63), so a setting with no fitting order is excluded whatever language K4 is in.

## Two new solvers, checked against the old one

- `engine/k4_columnar_bnb.py` with `engine/k4_columnar_bnb.c` builds the order one read column at a time and drops a prefix as soon as its clue letters contradict the key. In the columns-then-rows direction it walks slot types instead and picks real columns only for slots that hold clue letters, counting the rest exactly by factorials. Its counts match the full enumeration of `engine.k4_transposition_sub` in 1,600 comparisons, and the slot walk matches the prefix search in 560 more. Width 10 at periods 1 to 20 takes under a second instead of about 25; the slowest width 14 case went from 108 seconds to under a millisecond.
- `engine/k4_columnar_sat.py` asks a SAT solver (CaDiCaL) whether any order fits, without listing orders. It agrees with the branch and bound in 776 settings, every satisfying model is decoded and passed through the reference check, and a planted width 18 key is found. An encoding error that made it miss the large width 13 survivor blocks was found by this comparison and fixed before any run below.

Tests: `tests/test_k4_columnar_bnb.py`, `tests/test_k4_columnar_sat.py`.

## Results

Smallest period at which some order fits, either direction, either composition, any of the four variants:

| Width | 97 letters | 98 letters | Solver |
| --- | --- | --- | --- |
| 11 | 19 | none to 20 | branch and bound |
| 12 | 17 | 20 | branch and bound |
| 13 | 17 | 19 | branch and bound |
| 14 | 17 | 18 | SAT |
| 15 | 16 | 16 | SAT |
| 16 | 15 | 15 | SAT |

So no column order at widths 11 to 14 fits at any period from 1 to 16 under these four variants, none at width 15 to period 15 and none at width 16 to period 14.

Where orders do fit, they are what chance leaves when a long key meets few clue letters per key column. At widths 11 to 13 every surviving order with a complete key was decrypted (183 decrypted, the rest are near copies): the best English quadgram score is -5.5 a letter and the highest index of coincidence 0.044, the same as random letters with the clues planted (about -6.5 and 0.038; English is about -2 and 0.066). At width 13 the 10,800 survivors in the columns-then-rows direction come from layouts that give almost every clue letter its own key column, so they test almost nothing. Widths 14 to 16 were run with the SAT model, which gives one witness per setting, not every order; the fitting settings there are not decrypted in full.

Run: `python3 -m engine.k4_columnar_bnb` per width for 11 to 13, and `python3 -m engine.k4_columnar_sat 14 16 3 20` (1,920 settings, 47 seconds on 3 cores).

## Not finished

Widths 17 to 24 were started with the SAT model and stopped after about 30 minutes, at an estimated 2 hours to go; no result from them is claimed. Samples at widths 18 and 22 already show fitting orders at period 16, as the number of orders (18! is about 6 times 10^15) makes likely. Running them needs a few CPU hours, which `engine.k4_columnar_sat.scan` can split across machines.
