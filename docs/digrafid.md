# Digrafid cipher (known-key solver)

`engine/solvers/digrafid.py` decrypts a **known** pair of Digrafid alphabets and a period. `tests/test_digrafid.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** helper. It does **not** claim a reading of an ancient script, an unknown language, or any unsolved historical ciphertext.

## Published worked example (fetched)

Source: [American Cryptogram Association, Digrafid cipher sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf) (sheet page 43).

The sheet prints one tableau and two fractionations of the same plaintext. The certificate uses fractionation 3. Fractionation 4 is the same alphabets with period 4 and is checked in the test file.

| Field | Value |
| --- | --- |
| Horizontal alphabet (3 by 9, row by row) | `KEYWORDABCFGHIJLMNPQSTUVXZ#` |
| Vertical alphabet (9 by 3, down the columns) | `VERTICALBDFGHJKMNOPQSUWXYZ#` |
| Period | `3` digraphs (the sheet's fractionation 3, which is 6 letters) |
| Plaintext letters | `THISISTHEFORESTPRI` |
| Ciphertext | `HJMXWSWJADWGFCSPYI` |

The sheet prints the plaintext as "This is the forest pri". Spaces are not enciphered. The SHA-256 in `engine/data/digrafid_certificate.json` is of the 18 uppercase letters `THISISTHEFORESTPRI` with no spaces. The sheet groups the ciphertext as `HJMXWS WJADWG FCSPYI`. Those spaces are grouping only and are not in the ciphertext field.

The same sheet's fractionation 4 ciphertext is printed as `HJTKVHYU FFWDSQYP RI`. Without grouping spaces that is `HJTKVHYUFFWDSQYPRI`.

The horizontal alphabet is keyword `KEYWORD`, then the unused letters, then `#`. The vertical alphabet is keyword `VERTICAL`, then the unused letters, then `#`, written down the columns.

## Second published example

[CryptoCrack, Digrafid](https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/digrafid) uses keywords `GOLF` and `CLUB`. The page labels the setting "Period: 6" and groups the ciphertext in blocks of 6 letters. That block is 3 digraphs, the same period unit as the ACA fractionation. The quote "Golf: A good walk ruined." has an odd letter count, so the page adds a null `X`.

| Field | Value |
| --- | --- |
| Horizontal | `GOLFABCDEHIJKMNPQRSTUVWXYZ#` |
| Vertical | `CLUBADEFGHIJKMNOPQRSTVWXYZ#` |
| Period | `3` digraphs (6 letters on that page) |
| Plaintext letters, including the null | `GOLFAGOODWALKRUINEDX` |
| Ciphertext | `GWOCYQTMORPIFXXKGODX` |

Spaces in "Golf: A good walk ruined." are not part of that letter stream.

## What the engine does

- Keep `A` to `Z` and `#`, drop other characters, and fractionate by the period (digraphs per group).
- `solve_digrafid(ciphertext, horizontal=..., vertical=..., period=...)` returns a `SolveResult` with the recovered plaintext.
- No blind keyword search is registered in `SOLVERS`. Supply both alphabets and the period.

## What it does not do

- Decipher Linear A, Indus, Rongorongo, Phaistos, Voynich, or any undeciphered script.
- Claim a solution of Kryptos K4, army message Nr. 86, or any ciphertext whose plaintext is not cited.
- Invent a null when the letter count is odd. The caller supplies one, as the published pages do.
