# Seriated Playfair cipher (known-key solver)

`engine/solvers/seriated_playfair.py` encrypts and decrypts a **known** seriated Playfair keyword and period. `tests/test_seriated_playfair.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Seriated Playfair cipher sheet (fetched 2026-10-03, America/New_York):

[https://www.cryptogram.org/downloads/aca.info/ciphers/SeriatedPlayfair.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/SeriatedPlayfair.pdf)

PDF SHA-256: `8cce8115f416d4a6b8d133190cd26e0ca4aea3332ae432f0a366b66db08da94d`

| Field | Value |
| --- | --- |
| Keyword | `LOGARITHM` (5x5 square, J omitted) |
| Period | 6 (width of each 2-line group; not the keyword length) |
| Sentence on the sheet | Come quickly we need help immediately. tom. |
| Plaintext letter stream | `COMEQUICKLYWENEEDHXELPIMMEDIATELYTOM` |
| Ciphertext | `NLBCS PCDFG XZQQC DCMGC GQTBH CFTRH FGWHG B` |

The sheet writes the sentence in period-6 groups:

```
comequ eneedh mediat
icklyw xelpim elytom
```

Vertical pairs use Playfair rules 1-3 (same column down, same row right, otherwise the rectangle). The X under the second group is a null: without it the E of "help" would sit under another E. Ciphertext is taken off horizontally, top row then bottom row of each group, then split into fives. The last group is the single letter B.

## What the engine does

- Build the Playfair square from the keyword. I and J share a cell. J in the text becomes I.
- Drop spaces and punctuation. Write letters across the top row of a period group, then the bottom row.
- If the next letter would repeat the letter above it, write the null X in that cell (Q if the letter above is already X) and keep the plaintext letter for the next column.
- Encipher each vertical pair. Read the ciphertext as top row then bottom row, group by group.
- `solve_seriated_playfair(ciphertext, keyword=..., period=...)` returns a `SolveResult`.
- No blind keyword search is registered. Supply the keyword and the period.

## Verification certificate

`engine/data/seriated_playfair_certificate.json` records the cipher name, plaintext, ciphertext, key, period, source URL, the SHA-256 of the fetched PDF, and the SHA-256 of the plaintext letter stream. `SeriatedPlayfairCertificateTest` recomputes that plaintext hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlussel / army message Nr. 86, Kryptos K4, Zodiac, Beale, McCormick, or Voynich.
- Search for an unknown keyword or an unknown period.
- Remove a null X on decrypt. The null is a letter, and only the caller knows whether it was added.
