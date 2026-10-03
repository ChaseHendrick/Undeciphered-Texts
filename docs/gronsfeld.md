# Gronsfeld cipher (known-key solver)

`engine/solvers/gronsfeld.py` decrypts a **known** Gronsfeld numeric key. `tests/test_gronsfeld.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

Polybius-plus-Gronsfeld (`engine/solvers/polybius_gronsfeld.py`) is a different construction. This page is the digit-key Gronsfeld cipher only.

## Published worked example (fetched)

Source: [CaesarCipher.org, Gronsfeld cipher](https://caesarcipher.org/learn/gronsfeld-cipher-numeric-key-vigenere-variant-guide) (fetched 2026-10-02).

The page encrypts the message "ATTACK AT DAWN" with numeric key `3 1 4 1 5`. Step 1 removes spaces, then each letter is shifted by the repeating digits (A=0). The table prints:

| Field | Value |
| --- | --- |
| Key | `31415` |
| Plaintext letter stream | `ATTACKATDAWN` |
| Ciphertext letter stream | `DUXBHNBXEFZO` |

The page also groups the ciphertext as `DUXBH NBXEF ZO`. The first row of the table is plaintext A with key digit 3 → D. Decrypting subtracts the same digits: `P = (C − digit) mod 26`.

## What the engine does

- Drop non-letters. Repeat the digits 0-9 across the remaining letters.
- Each ciphertext letter is `(plaintext letter + key digit) mod 26`. Decrypt subtracts the digit.
- `solve_gronsfeld(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind key search is registered. Supply the key.

## Verification certificate

`engine/data/gronsfeld_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `GronsfeldCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Gronsfeld key.
