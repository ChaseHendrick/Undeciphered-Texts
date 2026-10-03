# Hill cipher, 2x2 (known-key solver)

`engine/solvers/hill.py` decrypts a **known** 2x2 Hill key. `tests/test_hill.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Arkadii Slinko, *Algebra for Cryptology* (Department of Mathematics, University of Auckland, 6 April 2013), “Hill’s cryptosystem. Example 2” and “Example 3”. PDF fetched 2026-10-02:

[https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf](https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf)

| Field | Value |
| --- | --- |
| Key | `3 3 2 5`, the matrix `[[3, 3], [2, 5]]` |
| Plaintext | `HELP` |
| Ciphertext | `HIAT` |

The notes split HELP into pairs HE = (7, 4) and LP = (11, 15), with A=0. Multiplying on the left by K gives (7, 8) and (0, 19), which are HI and AT. Example 3 states the inverse `[[15, 17], [20, 9]]` and decrypts HIAT back to HELP.

## What the engine does

- Drop non-letters. A=0 … Z=25. Pairs are column vectors.
- The key is four integers, row by row (`3 3 2 5` or `3, 3; 2, 5`). Entries are reduced mod 26. The determinant must be coprime to 26.
- Encryption is `C = K P (mod 26)`. An odd letter count is padded with a trailing X. The published HELP example is even and is not padded.
- Decryption multiplies by `K^{-1}` mod 26. It does not strip a padding X.
- `solve_hill(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind key search is registered. Supply the matrix. This is the 2x2 Hill cipher only.

## Verification certificate

`engine/data/hill_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `HillCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Hill key, or solve a 3x3 (or larger) Hill cipher.
