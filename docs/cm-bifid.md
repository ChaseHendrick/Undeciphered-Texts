# CM Bifid cipher (known-key solver)

`engine/solvers/cm_bifid.py` decrypts a **known** pair of CM Bifid squares and a period. `tests/test_cm_bifid.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script, rongorongo, or army message Nr. 86.

## Published worked example (fetched)

Source: American Cryptogram Association, CM Bifid cipher sheet (fetched 2026-10-03), sheet page 42:

[https://www.cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf)

The fetched file is one page, PDF 1.6, not encrypted, 63251 bytes. SHA-256:

`90d3e1133e00d1100fbee3e3b188cdb621cf4282b415a38cab3b4acf5b2dfd89`

The sheet says to proceed as for Bifid, then, after the coordinates are read horizontally, take the letter from the second 5 by 5 square. It prints both squares. The ciphertext square keyword is NOVELTY, written in alternating verticals (down the first column, up the second, and so on). The plaintext square is printed on the sheet. The sheet says See: BIFID. That Bifid sheet names the same square as keyword EXTRAORDINARY written in a clockwise spiral, and it states period 7 for this plaintext:

[https://www.cryptogram.org/downloads/aca.info/ciphers/Bifid.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Bifid.pdf)

The CM sheet writes ciphertext in period-length groups. The first two groups have 7 letters. The last group is shorter because 20 is not a multiple of 7.

| Field | Value |
| --- | --- |
| Plaintext square (row by row) | `EXTRAKLMPOHWZQDGVUSIFCBYN` |
| Plaintext keyword and route | EXTRAORDINARY, clockwise spiral |
| Ciphertext square (row by row) | `NCDRSOBFQUVAGPWEYHMXLTIKZ` |
| Ciphertext keyword and route | NOVELTY, alternating verticals |
| Period | `7` |
| Plaintext on the sheet | Odd periods are popular. |
| Plaintext stored | `ODDPERIODSAREPOPULAR` |
| Ciphertext on the sheet | `FANXZEX FENUKKR BYNKAK` |
| Ciphertext stored | `FANXZEXFENUKKRBYNKAK` |

Spaces are not enciphered. They are dropped, not copied. The SHA-256 in `engine/data/cm_bifid_certificate.json` is of `ODDPERIODSAREPOPULAR` with no spaces. The ciphertext spaces on the sheet are period groups and are not in the ciphertext field.

`O` is row 2, column 5 of the plaintext square, so the first coordinate pair on the sheet is `25` in the sheet's 1-based numbering. The first period block `oddperi` reads back, through the second square, as `FANXZEX`.

The same plaintext and plaintext square, read as ordinary Bifid, are the Bifid sheet ciphertext `MWEIN GIMGE OYYRL VEYWY`. CM Bifid is that fractionation with the second square substituted for the readout.

## What the engine does

- Fold `J` to `I`. Drop spaces and every other non-letter.
- In each period block, write row digits then column digits from the plaintext square, read those digits in pairs, and map each pair through the ciphertext square.
- `cm_bifid_encrypt` and `cm_bifid_decrypt` take both squares and the period.
- `square_clockwise_spiral` and `square_alternating_verticals` rebuild the sheet squares from the keywords.
- `solve_cm_bifid(ciphertext, plain_square=..., cipher_square=..., period=...)` returns a `SolveResult`.
- No blind square search is registered in `SOLVERS`. Supply both squares and the period.

## Verification certificate

`engine/data/cm_bifid_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, the SHA-256 of the fetched PDF, and the SHA-256 of the stored plaintext. Spaces are not included in that plaintext. `CmBifidCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypt matches the stored ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Claim a reading of Linear A, Indus, Voynich, rongorongo, or Kryptos K4.
- Claim a reading of Zodiac, Beale, or McCormick.
- Search for an unknown CM Bifid key.
