# Affine cipher (known-key solver)

`engine/solvers/affine.py` decrypts a **known** affine key `E(x) = (a*x + b) mod 26`. `tests/test_affine.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Wikipedia, Affine cipher](https://en.wikipedia.org/wiki/Affine_cipher) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `a=5`, `b=8` (`E(x) = (5x + 8) mod 26`) |
| Plaintext | `AFFINECIPHER` (the page encrypts "AFFINE CIPHER" and drops the space) |
| Ciphertext | `IHHWVCSWFRCP` |

The page's encryption table maps A, F, F, I to I, H, H, W and finishes at `IHHWVCSWFRCP`. Decryption uses `a^{-1} = 21` because `5 * 21 ≡ 1 (mod 26)`, so `D(y) = 21(y − 8) mod 26`, and the page states the recovered plaintext is `AFFINECIPHER`.

## What the engine does

- Drop non-letters. A=0 … Z=25.
- `a` must be coprime to 26 (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, or 25). `b` is taken mod 26.
- `solve_affine(ciphertext, a=..., b=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind key search is registered. Supply `a` and `b`.

## Verification certificate

`engine/data/affine_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `AffineCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown affine key.
