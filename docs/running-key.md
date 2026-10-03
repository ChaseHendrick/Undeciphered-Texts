# Running-key cipher (known-key solver)

`engine/solvers/running_key.py` decrypts a **known** running key. `tests/test_running_key.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Practical Cryptography, "Running Key Cipher" (fetched 2026-10-02):

[http://practicalcryptography.com/ciphers/classical-era/running-key/](http://practicalcryptography.com/ciphers/classical-era/running-key/)

| Field | Value |
| --- | --- |
| Key | `HOWDOESTHEDUCKKNOWTHATSAIDVI` (from "How does the duck know that? said Victor") |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `KSBHBHLALIDMVGKYZKYAHXUAAWGM` |

The page writes the key above the plaintext and uses the tabula recta. The first lookup is plaintext D with key letter H, which meets at ciphertext K. The full ciphertext printed on the page is `KSBHBHLALIDMVGKYZKYAHXUAAWGM`.

## What the engine does

- Drop non-letters. A=0 ... Z=25.
- Encryption is `C = (P + K) mod 26`. Decryption is `P = (C - K) mod 26`.
- The running key is not repeated. It must be at least as long as the letter stream. Extra key letters are ignored.
- `solve_running_key(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind key search is registered. Supply the key passage. This is not a one-time pad breaker.

## Verification certificate

`engine/data/running_key_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `RunningKeyCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown running key, or repeat a short keyword the way Vigenere does.
