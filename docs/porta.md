# Porta cipher (known-key solver)

`engine/solvers/porta.py` decrypts a **known** Porta keyword. `tests/test_porta.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Boxentriq, Porta cipher](https://www.boxentriq.com/ciphers/porta-cipher) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `FORTIFICATION` |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `SYNNJSCVRNRLAHUTUKUCVRYRLANY` |

The page lines the repeated keyword `FORTIFICATIONFORTIFICATIONFO` under the plaintext and prints that ciphertext. The first three lookups on the page are D with F → S, E with O → Y, and F with R → N. Applying the same keyword again returns the plaintext, because the tableau is reciprocal.

The same letters are the Practical Cryptography Porta example (`FORTIFICATION` / `DEFENDTHEEASTWALLOFTHECASTLE` / `synnjscvrnrlahutukucvryrlany`). The certificate cites the Boxentriq page that was fetched.

## What the engine does

- Drop non-letters. A and B select row 0, C and D row 1, through Y and Z on row 12.
- A-M maps to N-Z rotated by the row; N-Z is the inverse, so encrypt and decrypt are the same function.
- `solve_porta(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind keyword search is registered. Supply the key.

## Verification certificate

`engine/data/porta_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `PortaCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Porta keyword.
