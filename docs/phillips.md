# Phillips cipher (known-key solver)

`engine/solvers/phillips.py` decrypts a **known** Phillips keyword. `tests/test_phillips.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Central Washington University, Kryptos challenge Phillips cipher sheet (fetched 2026-10-02):

[https://www.cwu.edu/academics/math/_documents/kryptos-challenges/cwu-kryptos-challenge-phillips-cipher.pdf](https://www.cwu.edu/academics/math/_documents/kryptos-challenges/cwu-kryptos-challenge-phillips-cipher.pdf)

| Field | Value |
| --- | --- |
| Key | `COMPETE` (left-to-right 5x5 fill, I stands for J) |
| Plaintext | `SQUARESONEANDFIVEARETHESAMEANDSOARETWOANDEIGHT` |
| Ciphertext | `ZXVIYGZIWGIWLGPAVIPVHRTZIKGRWUFIXDGOBIMWLTSQRO` |

The sheet prints the plaintext and ciphertext in letter rows under square numbers. The first lookup is plaintext S on grid 1, replaced by Z. The joined letter-row ciphertext is the value above.

The one-line summary at the bottom of that page writes `TWQRO` where the letter rows show `TSQRO`. The certificate follows the letter rows, which agree with the rules on the same page.

## What the engine does

- Build a 5x5 square: keyword with duplicate letters dropped, J omitted, then the unused letters A to Z left to right.
- Make eight grids by shifting rows. Grids 2 to 5 walk row 1 downward. Grids 6 to 8, starting from grid 5, walk row 2 downward.
- Take the plaintext in blocks of five letters. Block n uses grid `((n) mod 8) + 1`. A short final block stays on its grid.
- Encryption replaces each letter with the letter one row down and one column to the right, wrapping at the edges. Decryption steps one row up and one column to the left.
- `solve_phillips(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind keyword search is registered. Supply the keyword.

## Verification certificate

`engine/data/phillips_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `PhillipsCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Phillips keyword.
