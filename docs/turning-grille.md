# Turning grille (known-stencil solver)

`engine/solvers/turning_grille.py` decrypts a **known** Fleissner turning grille. `tests/test_turning_grille.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Grille cipher sheet (fetched 2026-10-03):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf)

| Field | Value |
| --- | --- |
| Stencil (sols) | `1 8 10 12` |
| Square | 4 by 4, cells numbered by rows from 1 |
| Plaintext on the sheet | the turning grille |
| Plaintext recovered | `THETURNINGGRILLE` |
| Ciphertext groups | `TILUN RGHGE LTENI R` |

The sheet's openings in position 1 are cells 1, 8, 10, and 12. The first quarter, written across, is t h e t. A clockwise quarter-turn writes u r n i, the half-turn writes n g g r, and the three-quarter turn writes i l l e. Read by rows, the square is TILU / NRGH / GELT / ENIR. Groups of five give TILUN RGHGE LTENI R. The printed ciphertext line ends with a period. That period is not a cell. Spaces in "the turning grille" are not enciphered.

## What the engine does

- Parse the stencil as 1-based cell numbers. Four clockwise turns of those openings must be disjoint and must cover an even square of at most 12 by 12.
- `turning_grille_encrypt` writes plaintext letters through the openings, across, one quarter-turn at a time, then reads the square by rows in groups of five.
- `turning_grille_decrypt` fills the square by rows and reads the openings in the same order. Group spaces and a trailing period are ignored.
- `solve_turning_grille(ciphertext, key=...)` takes the stencil and returns a `SolveResult`.
- No search for an unknown stencil is registered. Supply the stencil.

## Verification certificate

`engine/data/turning_grille_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `TurningGrilleCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypting the stored plaintext matches the published ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown turning-grille stencil.
- Treat the period after the printed ciphertext as a letter.
