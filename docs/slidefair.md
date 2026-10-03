# Slidefair cipher (known-key solver)

`engine/solvers/slidefair.py` encrypts and decrypts a **known** Slidefair keyword. `tests/test_slidefair.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Slidefair cipher sheet (fetched 2026-10-03):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Slidefair.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Slidefair.pdf)

| Field | Value |
| --- | --- |
| Keyword | `DIGRAPH` (period 7, one key letter per digraph) |
| Table | Vigenere |
| Sentence on the sheet | The Slidefair can be used with Vigenere, Variant or Beaufort. |
| Plaintext letter stream | `THESLIDEFAIRCANBEUSEDWITHVIGENEREVARIANTORBEAUFORT` |
| Ciphertext | `EW KM CR NU AF CX TJ YQ MM YY FU TI GW ZP KH JM PK BS AI EC KV CF MI IL CI` |

The sheet also prints the Variant and Beaufort rows. With key letter B, plaintext `ca` becomes ZD, BB, or BZ, and plaintext `de` becomes EF, FC, or XY. A second Vigenere check is the CryptoCrack quote "If you do a job too well, you'll get stuck with it." under keyword SLIDEFAIR, with a final X because the letter count is odd:

[https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/slidefair](https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/slidefair)

## What the engine does

- Keep every keyword letter, including repeats. The period is that length.
- Drop spaces and punctuation. If the letter count is odd, append X before encrypting.
- For each pair, find the first letter in the top A-Z row and the second letter in the key-letter row. Take the other rectangle corners, top letter first. A vertical pair uses the next column to the right. Decrypt uses the previous column.
- `solve_slidefair(ciphertext, key=..., table=...)` returns a `SolveResult`. The default table is Vigenere.
- No blind keyword search is registered. Supply the keyword.

## Verification certificate

`engine/data/slidefair_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext letter stream. `SlidefairCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlussel / army message Nr. 86.
- Search for an unknown Slidefair keyword.
- Strip a final X on decrypt. The pad is a letter, and only the caller knows whether it was added.
