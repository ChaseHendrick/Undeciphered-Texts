# Ragbaby cipher (known-key solver)

`engine/solvers/ragbaby.py` decrypts a **known** Ragbaby keyword. `tests/test_ragbaby.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Ragbaby cipher sheet (fetched 2026-10-02):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Ragbaby.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Ragbaby.pdf)

| Field | Value |
| --- | --- |
| Keyword | `GROSBEAK` |
| Keyed alphabet | `GROSBEAKCDFHILMNPQTUVWYZ` (24 letters, I/J and W/X paired) |
| Plaintext sentence | Word divisions are kept. |
| Plaintext recovered | `WORD DIVISIONS ARE KEPT.` |
| Ciphertext | `YBBL HNGQDUFGL DEF HFYR.` |

The sheet prints that keyed alphabet as `G R O S B E A K C D F H I L M N P Q T U V W Y Z`. The keyword is the leading block `GROSBEAK`; the rest are the unused letters of the 24-letter alphabet. The plaintext sentence on the sheet is "Word divisions are kept." Word lengths are kept, so the ciphertext words are 4, 9, 3, and 4 letters. The first letter W moves 1 place (Y), O moves 2 (B), R moves 3 (B), and D moves 4 (L).

## What the engine does

- Build a 24-letter alphabet: keyword letters first (duplicates dropped), then the unused letters. J is read as I and X is read as W.
- Number each word from its place in the message: word 1 starts at 1, word 2 starts at 2, and so on. The count runs to 24 and then repeats (25 is 1).
- A hyphen, an apostrophe, or a leading asterisk stays inside the word. Spaces and other punctuation separate words and are copied through.
- `ragbaby_encrypt` moves each letter right by that count. `ragbaby_decrypt` moves left by the same count.
- `solve_ragbaby(ciphertext, key=...)` takes the keyword and returns a `SolveResult`.
- No blind keyword search is registered. Supply the keyword.

## Verification certificate

`engine/data/ragbaby_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `RagbabyCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Ragbaby keyword.
- Implement the 26-letter or 36-letter alphabets the sheet mentions only as options. The published example uses 24 letters.
