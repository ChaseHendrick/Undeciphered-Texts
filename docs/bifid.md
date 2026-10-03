# Bifid cipher (known-key solver)

`engine/solvers/bifid.py` decrypts a **known** Bifid keysquare and period. `tests/test_bifid.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** helper. It does **not** claim a reading of an ancient script, an unknown language, or any unsolved historical ciphertext.

## Published worked example (fetched)

Source: [Practical Cryptography, Bifid cipher](http://practicalcryptography.com/ciphers/bifid-cipher/)

| Field | Value |
| --- | --- |
| Keysquare (row-major) | `PHQGMEAYLNOFDXKRCVSZWBUTI` |
| Period | `5` |
| Plaintext | `DEFENDTHEEASTWALLOFTHECASTLE` |
| Ciphertext | `FFYHMKHYCPLIASHADTRLHCCHLBLR` |

The page also shows the same result via `pycipher.Bifid(...).encipher(...)` / `.decipher(...)`.

## What the engine does

- Fold `J`→`I`, drop non-letters, apply Delastelle fractionation per period block.
- `solve_bifid(ciphertext, square=..., period=...)` returns a `SolveResult` with the recovered plaintext.
- No blind keysquare search is registered in `SOLVERS`; supply the square and period.

## What it does not do

- Decipher Linear A, Indus, Rongorongo, Phaistos, Voynich, or any undeciphered script.
- Claim a wartime or archival Bifid break without a sourced keysquare.
- Touch two-square / Truppenschlüssel Nr. 86 tooling.
