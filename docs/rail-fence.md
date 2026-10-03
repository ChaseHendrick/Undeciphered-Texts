# Rail-fence cipher (known-key solver)

`engine/solvers/rail_fence.py` decrypts a **known** rail count. `tests/test_rail_fence.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Practical Cryptography — Rail Fence Cipher](http://practicalcryptography.com/ciphers/classical-era/rail-fence/) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key (rails) | `3` |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `DNETLHSEEDHESWLOTEATEFTAAFCL` |

The page writes "defend the east wall of the castle" on three rails and reads the rows:

```
d . . . n . . . e . . . t . . . l . . . h . . . s . . .
. e . e . d . h . e . s . w . l . o . t . e . a . t . e
. . f . . . t . . . a . . . a . . . f . . . c . . . l .
dnetlhseedheswloteateftaafcl
```

The same page with a key of 4 reads off `dttfsedhswotatfneaalhcleelee`.

## What the engine does

- Drop non-letters. The key is the number of rails (an integer of at least 2).
- Encryption writes letters down the fence and back up, then concatenates the rails from top to bottom.
- Decryption splits the ciphertext into those rail lengths and reads the zigzag back.
- `solve_rail_fence(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind rail search is registered. Supply the key.

## Verification certificate

`engine/data/rail_fence_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `RailFenceCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown rail count.
