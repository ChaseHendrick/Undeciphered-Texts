# K4 with wrong clue letters allowed, and two stacked keys, 18 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

Code: `engine/k4_sat.py`, tests `tests/test_k4_sat.py`. The families, the clues (EASTNORTHEAST at 21, BERLINCLOCK at 63, zero-based) and the meaning of "fits" are those of [the unknown-alphabet log](unknown-alphabets-hill-2026-10-18.md). Every alphabet is left free and no language model is used, so the results hold whatever language the rest of K4 is in.

## A faster solver

The same questions are now encoded as pure SAT, with one boolean per letter and rank and per column and shift, and solved by CaDiCaL through PySAT. On 300-odd family and period settings it returns exactly what the Z3 module returned. A case that took Z3 345 seconds takes 2.7. The speed is what made the two scans below possible.

## Wrong clue letters

Sanborn left deliberate misspellings in K1 to K3 (IQLUSION, UNDERGRUUND, DESPARATLY). Every exclusion so far treats all 24 clue letters as exact. Here RC2, a MaxSAT solver, finds the fewest clue letters that must be dropped before a family fits. A dropped letter stands for a misspelled plaintext letter or a wrong ciphertext letter. For autokey a ciphertext error would also move a later key letter, so those counts are a lower bound.

Dropping letters makes every model easier to fit, so each K4 count is set beside the same count on 10 random 97-letter strings. Families: the eight of the earlier log, periods or lags 1 to 26. Run: `python3 -m engine.k4_sat 3 10`, 2,288 MaxSAT problems, about 85 minutes on 3 cores.

Keyed Vigenere, the K1 and K2 system, needs this many dropped clue letters at each period (K4, then the range over random strings):

| Period | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K4 | 12 | 7 | 9 | 5 | 5 | 4 | 4 | 2 | 7 | 3 | 3 | 3 | 2 |
| Random | 10 to 13 | 6 to 9 | 6 to 9 | 3 to 8 | 3 to 7 | 2 to 5 | 2 to 4 | 1 to 3 | 4 to 8 | 0 to 5 | 0 to 2 | 1 to 4 | 1 to 4 |

| Period | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K4 | 2 | 3 | 2 | 4 | 2 | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 1 |
| Random | 0 to 3 | 1 to 4 | 0 to 2 | 1 to 2 | 0 to 3 | 1 to 3 | 0 to 3 | 0 to 4 | 0 to 4 | 0 to 4 | 0 to 1 | 0 to 1 | 0 to 1 |

So one misspelled clue letter does not rescue keyed Vigenere at any period from 1 to 18, 20 to 22 or 25. With one wrong letter it fits only at periods 19, 23, 24 and 26, where random text usually fits too. At periods 11, 17 and 25 K4 needs more dropped letters than all ten random strings.

Where K4 needs fewer dropped letters than all ten random strings:

| Family | Setting | K4 | Random |
| --- | --- | --- | --- |
| Quagmire I | period 4 | 6 | 7 to 9 |
| Quagmire I, II and IV | period 19 | 0 | 1 to 3 |
| Two-alphabet ciphertext autokey | lag 15 | 0 | 1 to 2 |

These were then checked against a larger null of 300 random strings and 300 shuffles of K4's own letters (exact fit only):

| Setting | Random strings that fit | Shuffles of K4 that fit |
| --- | --- | --- |
| Quagmire I, period 19 | 7 of 300 | 3 of 300 |
| Quagmire II, period 19 | 10 of 300 | 8 of 300 |
| Quagmire IV, period 19 | 11 of 300 | 9 of 300 |
| Two-alphabet ciphertext autokey, lag 15 | 122 of 300 | 127 of 300 |

The autokey case was an artifact of ten controls. Period 19 fits by chance 1 to 4 percent of the time, and 208 family and period settings were scanned, so a few such hits are expected. Period 19 is not significant. It is still the most unusual setting found, and a language-scored search there, with planted controls, is the next check; it is recorded in its own log if run.

## Two stacked keys

Two repeating keys added together, of lengths m and n, on one keyed alphabet left free (Vigenere and Beaufort sense). This is a special case of one key of length lcm(m, n), with far fewer free shifts, so the clues can test it where the one-key check is blind (lcm above 26). Every pair 2 <= m < n <= 26 was checked; planted controls always fit. Run: `two_key_scan(top=26)`, 52 seconds.

No pair with lcm at most 26 fits K4 in the Vigenere sense; in the Beaufort sense only 2+13, 2+26 and 13+26 (lcm 26, where the one-key Beaufort check is also open). The pairs with lcm above 26 that do not fit, and so are excluded for any keyed alphabet:

- Vigenere sense, 37 pairs: 2+15, 2+17, 2+19, 2+21, 2+23, 2+25, 3+11, 3+13, 3+14, 3+16, 3+17, 4+7, 4+9, 4+11, 4+13, 4+14, 4+18, 4+21, 4+22, 4+26, 5+7, 5+8, 5+9, 5+19, 6+7, 6+14, 6+16, 6+21, 8+10, 8+20, 9+12, 9+15, 10+25, 12+16, 12+18, 14+21, 16+24.
- Beaufort sense, 31 pairs: 2+17, 2+19, 2+21, 2+25, 3+13, 3+14, 3+16, 4+7, 4+9, 4+11, 4+14, 4+18, 4+19, 4+21, 4+22, 5+7, 5+8, 5+9, 6+7, 6+14, 6+16, 6+21, 8+10, 8+20, 9+12, 9+15, 10+25, 12+16, 12+18, 14+21, 16+24.

The other 207 and 213 pairs fit; like the long single keys, they are not tested by the clues.

## What this does not cover

- More than one wrong letter in a family that moves letters, and wrong letters outside the clue positions under autokey.
- Two stacked keys on two different alphabets, or three keys.
- Any transposition; these are in-place models.
