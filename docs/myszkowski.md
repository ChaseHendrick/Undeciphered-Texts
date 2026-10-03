# Myszkowski transposition (known-key solver)

`engine/solvers/myszkowski.py` decrypts a **known** Myszkowski keyword. `tests/test_myszkowski.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It does **not** claim Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86. It does not read Linear A, the Indus script, or rongorongo.

## Published worked example (fetched)

Source: American Cryptogram Association, Myszkowski cipher sheet (fetched 2026-10-03):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf)

| Field | Value |
| --- | --- |
| Keyword | `BANANA` |
| Numeric key | `2-1-3-1-3-1` (A is 1, B is 2, N is 3; repeated letters share a number) |
| Plaintext on the sheet | Incomplete columnar with pattern word key and letters under same number taken off by row from top to bottom. |
| Plaintext recovered | `INCOMPLETECOLUMNARWITHPATTERNWORDKEYANDLETTERSUNDERSAMENUMBERTAKENOFFBYROWFROMTOPTOBOTTOM` |
| Ciphertext groups | `NOPEE OUNRI HATRW RKYNL TESNE SMNME TKNFB RWRMO TBTOI LLWTO ATDER OOTOC MTCMA TPEND EDERU RAUBA EFYFO POTM` |

The sheet writes the plaintext in rows of six under BANANA. The last row is short: `ottom` fills five cells and leaves the last cell empty. Columns numbered 1 (the three A columns) are read by rows, then the single B column, then the two N columns by rows. Groups of five give the ciphertext above. The printed ciphertext line ends with a period. That period is not a letter. Spaces in the plaintext sentence are not enciphered.

## What the engine does

- Number keyword letters in alphabetical order. Every copy of a letter gets that same number.
- `myszkowski_encrypt` writes plaintext letters in rows, reads same-numbered columns by rows, and groups the result in fives.
- `myszkowski_decrypt` fills those columns from the ciphertext in the same order, then reads the grid by rows. Group spaces and a trailing period are ignored.
- `solve_myszkowski(ciphertext, keyword=...)` takes the keyword and returns a `SolveResult`.
- No search for an unknown keyword is registered. Supply the keyword.

## Verification certificate

`engine/data/myszkowski_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `MyszkowskiCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypting the stored plaintext matches the published ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86.
- Search for an unknown Myszkowski keyword.
- Treat the period after the printed ciphertext as a letter.
