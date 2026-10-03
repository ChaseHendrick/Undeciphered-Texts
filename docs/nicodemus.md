# Nicodemus cipher (known-key solver)

`engine/solvers/nicodemus.py` decrypts a **known** Nicodemus keyword. `tests/test_nicodemus.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Nicodemus cipher sheet (fetched 2026-10-02):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Nicodemus.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Nicodemus.pdf)

| Field | Value |
| --- | --- |
| Key | `CAT` (ranks C=2, A=1, T=3) |
| Plaintext sentence | the early bird gets the worm |
| Plaintext letters | `THEEARLYBIRDGETSTHEWORM` |
| Ciphertext | `HAYRE VGNKI XKUWM TWMUG TAH.` |

The sheet names three steps: column transposition, Vigenere encipherment with the same key, then a takeoff of 5 letters at a time from each column. A last block shorter than 5 is read the same way, column by column.

For key `CAT` the columns move to order A, C, T. The Vigenere key on those columns is `ACT`. The joined ciphertext letters are `HAYREVGNKIXKUWMTWMUGTAH`.

## Second published walk-through

CryptoCrack's Nicodemus page (fetched 2026-10-02) prints key `MONEY` (ranks 24315) and the sentence "Money can't buy happiness. But it sure makes misery easier to live with." The same steps reproduce the ciphertext printed there. That page is a check, not the certificate example.

[https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/nicodemus](https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/nicodemus)

## What the engine does

- Number the keyword alphabetically. An earlier copy of a repeated letter gets the smaller rank.
- Write the plaintext in rows of that width. A short last row fills columns from the left.
- Reorder the columns by rank.
- Shift each column by the keyword letter now at its head (Vigenere, A = 0).
- Read 5 letters from each column in order, repeating until the columns are empty.
- `solve_nicodemus(ciphertext, key=...)` returns a `SolveResult`. When the ciphertext is letters only, the plaintext is the recovered letters. Spaces in a ciphertext skeleton are kept.
- No blind keyword search is registered. Supply the keyword.

## Verification certificate

`engine/data/nicodemus_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `NicodemusCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Nicodemus keyword.
