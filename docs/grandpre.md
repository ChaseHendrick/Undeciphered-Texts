# Grandpre cipher (known-key solver)

`engine/solvers/grandpre.py` decrypts a **known** Grandpre square. `tests/test_grandpre.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Grandpre cipher sheet (fetched 2026-10-02):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Grandpre.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Grandpre.pdf)

| Field | Value |
| --- | --- |
| Square | eight 8-letter words, rows and columns numbered 1 to 8 |
| First column (keyword) | `LACQUERS` |
| Words | `LADYBUGS`, `AZIMUTHS`, `CALFSKIN`, `QUACKISH`, `UNJOVIAL`, `EVULSION`, `ROWDYISM`, `SEXTUPLY` |
| Published sentence | The first column is the keyword. |
| Plaintext recovered | `THEFIRSTCOLUMNISTHEKEYWORD` |
| Ciphertext | `84 27 82 34 56 71 77 26 44 54 64 63 78 52 66 65 84 27 82 36 61 88 73 54 71 13` |

The joined digits are `8427823456717726445464637852666584278236618873547113`.

A letter that sits in more than one cell may use any of those pairs. The sheet's pairs are one valid encipherment. `grandpre_encrypt` uses the first cell in row-major order instead, then decryption returns the same letters.

## What the engine does

- The key is the words joined by `|`.
- `grandpre_encrypt` writes a row digit and a column digit for the first cell of each letter. On a 10-by-10 square the labels are 1 through 9 and then 0.
- `solve_grandpre(ciphertext, key=...)` reads digits in pairs and returns a `SolveResult`.
- No blind square search is registered. Supply the words.

## Verification certificate

`engine/data/grandpre_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `GrandpreCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of army message Nr. 86, Kryptos K4, Voynich, Linear A, Indus, or rongorongo.
- Search for an unknown Grandpre square.
- Treat the first-cell encipherment as the only digit string the sheet allows.
