# Vigenère autokey cipher (known-key solver)

`engine/solvers/autokey.py` decrypts a **known** Vigenère-autokey primer. `tests/test_autokey.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Practical Cryptography, Autokey cipher](http://practicalcryptography.com/ciphers/autokey-cipher/) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key (primer) | `FORTIFICATION` |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `ISWXVIBJEXIGGZEQPBIMOIGAKMHE` |

The page places the primer and then the plaintext itself above the message:

```
FORTIFICATIONDEFENDTHEEASTWA
DEFENDTHEEASTWALLOFTHECASTLE
ISWXVIBJEXIGGZEQPBIMOIGAKMHE
```

The first lookup on the page is plaintext D with key F → I. With A=0, `C = (P + K) mod 26`. To decrypt, the primer recovers the first letters, and each recovered plaintext letter extends the keystream: `P = (C − K) mod 26`.

The same page also shows primer `HELLO` encrypting "defend the east wall of the castle" to `KIQPBGXMIRDLAAELDHBTSPQFLAPG` (pycipher `Autokey`).

## What the engine does

- Drop non-letters. The keystream is the primer followed by the plaintext, cut to the message length.
- Encryption adds plaintext and keystream letters mod 26. Decryption subtracts, feeding each recovered letter back into the keystream.
- `solve_autokey(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind primer search is registered. Supply the key. This is the plaintext-autokey (Vigenère autokey), not a ciphertext-autokey variant.

## Verification certificate

`engine/data/autokey_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `AutokeyCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown autokey primer.
