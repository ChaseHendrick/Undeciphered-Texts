# K4 under fractionating ciphers: 5 by 5 squares and trifid, 18 October 2026

Not solved. No plaintext claimed. `solved` is false and `claimed_plaintext` is null.

The [neural family prior](family-net-2026-10-18.md) put K4 with random letters, Gromark and trifid. This note checks the fractionating side. Code: `engine/k4_fractionation.py`, tests `tests/test_k4_fractionation.py`. Only the two clues are used (EASTNORTHEAST at 21, BERLINCLOCK at 63, zero-based), so the results hold whatever language the rest of K4 is in.

## Every 25-cell square: excluded by a letter count

A cipher whose output letters come from one 5 by 5 square can write at most 25 different letters. That covers bifid, the conjugated-matrix bifid, Playfair and seriated Playfair, two-square, four-square, Phillips and Polybius substitutions, with any keys and any period. K4 uses all 26 letters (each at least once), so all of them are excluded outright. A bifid ciphertext of 400 letters under a random square is checked to stay within 25 letters as a control.

## Trifid with an unknown cube: excluded at every period

Trifid uses a 3 by 3 by 3 cube of 27 symbols. Inside each block of the period it writes each symbol as three coordinates, reads them by rows (all layers, then all rows, then all columns, the convention of `engine/solvers/trifid.py` and its published worked example) and turns each new triple back into a symbol. Here the cube is left completely unknown. A SAT model (CaDiCaL through PySAT) places the 27 symbols in the 27 cells, gives each plaintext position in a block that holds a clue letter one symbol, and requires each ciphertext symbol to sit in the cell its block reads out.

Two lengths:

- 97 letters, the carving. The 27th symbol ('.') may appear in the plaintext but not in the ciphertext.
- 98 letters, with the question mark that ends K3 on the sculpture as ciphertext position 0 and as the 27th symbol, the clue positions moved up by one. Trifid needs exactly one symbol beyond the 26 letters, and the sculpture shows exactly one.

| Length | Periods checked | Periods that fit both clues |
| --- | --- | --- |
| 97 | 1 to 97 (97 is one block) | none |
| 98 | 1 to 98 | none |

EASTNORTHEAST alone already blocks 96 of the 97 periods at 97 letters; BERLINCLOCK alone blocks 10.

Controls: 80 planted texts, random length (97 or 98), random period and random cube, enciphered with the repo's `trifid_encrypt` and with both clues in place, are never blocked. That also checks that the model's reading convention matches the repo's. The whole scan of 195 periods takes 14 seconds.

## What this does not cover

- Trifid with other reading conventions than the standard one, a cube larger than 27, or a transposition before or after it.
- Fractionation into more than three coordinates, and fractionated Morse, whose letters do not stay at fixed positions, so the clues as published cannot place them.
- Gromark variants, which are checked separately.
