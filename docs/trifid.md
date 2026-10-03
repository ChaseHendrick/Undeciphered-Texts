# Trifid cipher (known-key solver)

`engine/solvers/trifid.py` decrypts a **known** Trifid cube and period. `tests/test_trifid.py` checks that this recovers a published worked example symbol for symbol.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Practical Cryptography, Trifid cipher (fetched 2026-10-03):

[http://practicalcryptography.com/ciphers/trifid-cipher/](http://practicalcryptography.com/ciphers/trifid-cipher/)

The page prints the key as three 3 by 3 squares filled from `EPSDUCVWYM.ZLKXNBTFGORIJHAQ`:

| Square | Rows |
| --- | --- |
| 1 | `EPS` / `DUC` / `VWY` |
| 2 | `M.Z` / `LKX` / `NBT` |
| 3 | `FGO` / `RIJ` / `HAQ` |

| Field | Value |
| --- | --- |
| Key (27 symbols, period included) | `EPSDUCVWYM.ZLKXNBTFGORIJHAQ` |
| Period | `5` |
| Plaintext on the page | DEFEND THE EAST WALL OF THE CASTLE. |
| Plaintext stored | `DEFENDTHEEASTWALLOFTHECASTLE.` |
| Ciphertext on the page | `SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP` |
| Ciphertext stored | `SUEFECPHSEGYYJIXIMFOFOCEJLBSP` |

Spaces are not enciphered. They are dropped, not copied. The SHA-256 in `engine/data/trifid_certificate.json` is of `DEFENDTHEEASTWALLOFTHECASTLE.` with no spaces. The final period is a cube symbol and is included in that hash. The ciphertext spaces on the page are groups of 5 and are not in the ciphertext field.

A letter's three digits are square, row, column, counting from 1 on the page. `D` is square 1, row 2, column 1, so `121`. With period 5 the first block `DEFEN` reads back as `SUEFE`.

## What the engine does

- Keep `A` to `Z` and `.`. Drop spaces and every other character.
- In each period block, write layer, row, and column digits, read them across, and map each new triplet back through the same cube.
- `trifid_encrypt` and `trifid_decrypt` take the 27-symbol key and the period.
- `solve_trifid(ciphertext, key=..., period=...)` returns a `SolveResult`.
- No blind cube search is registered in `SOLVERS`. Supply the key and the period.

## Verification certificate

`engine/data/trifid_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the stored plaintext. Spaces are not included in that plaintext. `TrifidCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypt matches the stored ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Claim a reading of Linear A, Indus, Voynich, rongorongo, or Kryptos K4.
- Search for an unknown Trifid key.
