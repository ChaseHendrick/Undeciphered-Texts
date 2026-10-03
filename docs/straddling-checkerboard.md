# Straddling checkerboard (known-key solver)

`engine/solvers/straddling_checkerboard.py` decrypts a **known** straddling checkerboard key. `tests/test_straddling_checkerboard.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Wikipedia, "Straddling checkerboard" (fetched 2026-10-02):

[https://en.wikipedia.org/wiki/Straddling_checkerboard](https://en.wikipedia.org/wiki/Straddling_checkerboard)

The article prints this board. Columns are 0 through 9. Columns 2 and 6 are blank in the header, and those digits label the extra rows.

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | E | T | | A | O | N | | R | I | S |
| 2 | B | C | D | F | G | H | J | K | L | M |
| 6 | P | Q | / | U | V | W | X | Y | Z | . |

Key: `2,6|ETAONRIS|BCDFGHJKLMPQ/UVWXYZ.`

| Field | Value |
| --- | --- |
| Printed sentence | ATTACK AT DAWN |
| Plaintext recovered | `ATTACKATDAWN` |
| Ciphertext | `3113212731223655` |

The article's number row is 3, 1, 1, 3, 21, 27, 3, 1, 22, 3, 65, 5. Joined, that is `3113212731223655`. Spaces in the printed sentence are not encoded, so the digit stream recovers the twelve letters and not the spaces.

## What the engine does

- Read the key as `row,row|HEADER|BODY`. The two digits are the blank columns and the extra row labels, in order.
- Place the eight header symbols in the other columns, left to right. Column labels stay 0 through 9.
- Place the twenty body symbols in the first extra row, then the second.
- `straddling_checkerboard_encrypt` writes one digit for a header symbol and two digits for any other board symbol. Whitespace is dropped.
- `solve_straddling_checkerboard(ciphertext, key=...)` returns a `SolveResult`.
- Decryption is unambiguous: a row digit starts a pair, and any other digit is one header symbol.
- No search for an unknown board is registered. Supply the key.

## Verification certificate

`engine/data/straddling_checkerboard_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `StraddlingCheckerboardCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the Wikipedia example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown straddling checkerboard key.
- Restore spaces that the published digit stream does not encode.
- Scramble the column digits. This solver keeps columns 0 through 9 in order, as in the published example.
