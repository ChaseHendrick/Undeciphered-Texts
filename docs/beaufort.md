# Beaufort cipher (known-key solver)

`engine/solvers/beaufort.py` decrypts a **known** Beaufort keyword. `tests/test_beaufort.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Practical Cryptography — Beaufort cipher](http://practicalcryptography.com/ciphers/beaufort-cipher/) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `FORTIFICATION` |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `CKMPVCPVWPIWUJOGIUAPVWRIWUUK` |

The page lines the repeated keyword `FORTIFICATIONFORTIFICATIONFO` under the plaintext and prints that ciphertext. The first lookup on the page is plaintext D with key F → C. Applying the same keyword again returns the plaintext, because Beaufort is reciprocal: `C = (K − P) mod 26` and `P = (K − C) mod 26` (A=0).

The same page also shows key `HELLO` encrypting "defend the east wall of the castle" to `EAGHBELEHKHMSPOWTXGVAAJLWOTH`.

## What the engine does

- Drop non-letters. Repeat the keyword across the remaining letters.
- Each ciphertext letter is `(key letter − plaintext letter) mod 26`. Encrypt and decrypt are the same function.
- `solve_beaufort(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind keyword search is registered. Supply the key.

## Verification certificate

`engine/data/beaufort_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `BeaufortCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Beaufort keyword.
