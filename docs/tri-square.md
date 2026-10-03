# Tri-square cipher (known-key solver)

`engine/solvers/tri_square.py` decrypts a **known** set of three Tri-square squares. `tests/test_tri_square.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script, rongorongo, or army message Nr. 86.

## Published worked example (fetched)

Source: American Cryptogram Association, Tri-square cipher sheet (fetched 2026-10-03), sheet page 86:

[https://www.cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf)

The fetched file is one page, PDF 1.6, not encrypted, 63533 bytes. SHA-256:

`74b8200474df8a50e6782fcc33b4a34517f09d644b3954dc918c373f3f1b4151`

The sheet uses three 5 by 5 Polybius squares. Plaintext is taken in pairs. The first letter is found in square 1 and the second in square 2. Each pair becomes three cipher letters. The first may be any letter in the same column of square 1 as the first plaintext letter. The second is the square 3 cell where that row meets the column of the second plaintext letter in square 2. The third may be any letter in that same row of square 2.

The sheet prints the squares. It does not print keyword names. The squares are the keyword fills below. J is omitted.

| Field | Value |
| --- | --- |
| Square 1 (row by row) | `NSFMUOAGPWVBHQXECIRYLDKTZ` |
| Square 1 keyword and route | NOVELS, vertical (down the columns) |
| Square 2 (row by row) | `READINGBCFHKLMOPQSTUVWXYZ` |
| Square 2 keyword and route | READING, horizontal (across the rows) |
| Square 3 (row by row) | `PASTINOQRMLYZUEKXWVBHGFDC` |
| Square 3 keyword and route | PASTIME, clockwise spiral |
| Plaintext on the sheet | t h r e e k e y s q u a r e s u s e d x |
| Plaintext stored | `THREEKEYSQUARESUSEDX` |
| Ciphertext on the sheet | `RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ.` |
| Ciphertext stored | `RHLQXRLXOEVZBATXSERXDDIUAAABFZ` |

Spaces are not enciphered. They are dropped, not copied. The SHA-256 in `engine/data/tri_square_certificate.json` is of `THREEKEYSQUARESUSEDX` with no spaces. The final X is the even-length null printed on the sheet. The ciphertext spaces on the sheet are trigraph groups, and the final period is punctuation. Neither is in the ciphertext field.

The first plaintext pair is T H. T is row 5, column 4 of square 1 in the sheet's 1-based numbering (column letters M P Q R T). H is row 3, column 1 of square 2 (row letters H K L M O). Square 3 at that row and column is H. The sheet's first trigraph RHL uses R from that column and L from that row.

## What the engine does

- Fold `J` to `I`. Drop spaces and every other non-letter.
- `tri_square_encrypt` takes the three squares. An odd length is padded with X. `first_rows` and `third_cols` select the free letters. They default to the top of the column and the left of the row.
- `tri_square_decrypt` takes the three squares. It does not need the free-letter choice.
- `square_vertical`, `square_horizontal`, and `square_clockwise_spiral` rebuild the sheet squares from the keywords.
- `solve_tri_square(ciphertext, square1=..., square2=..., square3=...)` returns a `SolveResult`.
- No blind square search is registered in `SOLVERS`. Supply all three squares.

## Verification certificate

`engine/data/tri_square_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, the SHA-256 of the fetched PDF, and the SHA-256 of the stored plaintext. Spaces are not included in that plaintext. `TriSquareCertificateTest` recomputes that hash, decrypts the ciphertext, and checks that encrypt with the printed free-letter choices matches the stored ciphertext. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of army message Nr. 86.
- Claim a reading of Linear A, Indus, Voynich, rongorongo, or Kryptos K4.
- Claim a reading of Zodiac, Beale, or McCormick.
- Search for an unknown Tri-square key.
