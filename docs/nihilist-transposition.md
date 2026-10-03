# Nihilist transposition (known-key solver)

`engine/solvers/nihilist_transposition.py` decrypts a **known** numeric key used on both rows and columns. `tests/test_nihilist_transposition.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It does **not** claim Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86. It does not read Linear A, the Indus script, or rongorongo. It is **not** the Nihilist substitution (Polybius addition) cipher in [nihilist.md](nihilist.md).

## Published worked example (fetched)

Source: American Cryptogram Association, Nihilist Transposition cipher sheet (fetched 2026-10-03):

[https://www.cryptogram.org/downloads/aca.info/ciphers/NihilistTransposition.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/NihilistTransposition.pdf)

| Field | Value |
| --- | --- |
| Numeric key | `2134` (same key on rows and columns; 4 by 4 square) |
| Plaintext on the sheet | square needed here |
| Plaintext recovered | `SQUARENEEDEDHERE` |
| Ciphertext by columns (C1) | `EQDER SEHNU EREAD E` |
| Ciphertext by rows (C2) | `ERNEQ SUADE EDEHR E` |

The sheet writes the plaintext in rows into square 1. Columns are moved into numerical key order (taking-out), then rows are moved the same way. For key 2134 the writing-in key (Elcy) and the taking-out key (LEDGE) are identical, so both sheet paths print the same final square. Groups of five give the ciphertexts above. Each printed ciphertext line ends with a period. That period is not a letter. Spaces in the plaintext phrase are not enciphered.

## What the engine does

- Require a numeric key that is a permutation of `1..n` with `n` from 2 to 10 (sheet maximum 10 by 10).
- Require the letter count to be exactly `n` by `n`.
- `nihilist_transposition_encrypt` writes letters by rows, reorders columns then rows into key order, and reads by columns (default) or by rows, grouped in fives.
- `nihilist_transposition_decrypt` refills that square from the ciphertext, restores rows and columns, and reads by rows. Group spaces and a trailing period are ignored.
- `solve_nihilist_transposition(ciphertext, key=..., takeoff=...)` returns a `SolveResult`.
- No search for an unknown key is registered. Supply the key.

## Verification certificate

`engine/data/nihilist_transposition_certificate.json` records the cipher name, plaintext, column-takeoff ciphertext, key, source URL, and the SHA-256 of the plaintext. `NihilistTranspositionCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypting the stored plaintext matches the published column ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86.
- Search for an unknown Nihilist transposition key.
- Implement Nihilist substitution (coordinate addition on a Polybius square).
- Treat the period after the printed ciphertext as a letter.
