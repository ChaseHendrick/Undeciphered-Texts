# AMSCO cipher (known-key solver)

`engine/solvers/amsco.py` decrypts a **known** AMSCO numeric key. `tests/test_amsco.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, Kryptos K4, Zodiac Z13, Zodiac Z32, the Beale ciphers, or the McCormick cipher.

## Published worked example (fetched)

Source: American Cryptogram Association, AMSCO cipher sheet (fetched 2026-10-03):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf)

The sheet says the first entry may be either a digraph or a single letter. In both even and odd periods the first column and the first row always alternate. A null is not required when the last cell is short.

| Field | Value |
| --- | --- |
| Numeric key | `41325` |
| First cell | digraph (`in`) |
| Plaintext on the sheet | Incomplete columnar with alternating single letters and digraphs. |
| Plaintext stored | `INCOMPLETECOLUMNARWITHALTERNATINGSINGLELETTERSANDDIGRAPHS` |
| Ciphertext on the sheet | `CECRT EGLEN PHPLU TNANT EIOMO WIRSI TDDSI NTNAL INESA ALEMH ATGLR GR` |
| Ciphertext stored | `CECRTEGLENPHPLUTNANTEIOMOWIRSITDDSINTNALINESAALEMHATGLRGR` |

Spaces are not enciphered. They are dropped, not copied. The SHA-256 in `engine/data/amsco_certificate.json` is of the 57 uppercase letters with no spaces. The ciphertext spaces on the sheet are groups of five, and the final period is punctuation. Neither is in the ciphertext field.

Under key `41325` the first row is `in c om p le`. Columns are taken in digit order 1, 2, 3, 4, 5, which is the second, fourth, third, first, and fifth columns. That reads `CECRTEGLENPH` first.

## What the engine does

- Keep `A` to `Z`. Drop spaces and every other character.
- Fill rows of cells whose sizes alternate. The first cell is a digraph or a single, as supplied. Cell `(row, column)` is the other size when `row + column` is odd.
- Read each column top to bottom, in numeric-key order.
- `amsco_encrypt` and `amsco_decrypt` take the numeric key and `start` (`digraph` or `single`).
- `solve_amsco(ciphertext, key=..., start=...)` returns a `SolveResult`.
- No blind key search is registered in `SOLVERS`. Supply the key and the first-cell size.

## Verification certificate

`engine/data/amsco_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the stored plaintext. Spaces are not included in that plaintext. `AmscoCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypt matches the stored ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of army message Nr. 86.
- Claim a reading of Linear A, Indus, Voynich, rongorongo, Kryptos K4, Zodiac Z13, Zodiac Z32, the Beale ciphers, or the McCormick cipher.
- Search for an unknown AMSCO key.
