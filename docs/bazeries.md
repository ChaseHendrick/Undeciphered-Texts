# Bazeries cipher (known-key solver)

`engine/solvers/bazeries.py` decrypts a **known** Bazeries number. `tests/test_bazeries.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [ACA cipher types, Bazeries](https://www.cryptogram.org/downloads/aca.info/ciphers/Bazeries.pdf) (page 35, fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `3752` |
| Plaintext | `SIMPLESUBSTITUTIONPLUSTRANSPOSITION` |
| Ciphertext | `ACYYUXYMRQKXKCKGCRQIYITNKYXKCYGQGCI` |

The sheet spells the number and uses it as the keyword of a 5×5 ciphertext Polybius square filled left to right. The plaintext square is the alphabet in normal order, filled vertically, with I and J in one cell. The plaintext is cut into groups of 3, 7, 5, and 2; each group is reversed; then each letter is replaced by the ciphertext-square letter in the same cell. The sheet prints the ciphertext in five-letter groups: `ACYYU XYMRQ KXKCK GCRQI YITNK YXKCY GQGCI`.

The spelled keyword, with "and" omitted, is `THREETHOUSANDSEVENHUNDREDFIFTYTWO`. That fills the ciphertext square printed on the sheet:

```
T H R E O
U S A N D
V F I Y W
B C G K L
M P Q X Z
```

The first group on the sheet is `SIM` reversed to `MIS`, which enciphers as `ACY`.

## What the engine does

- Drop non-letters. Fold J into I before either square is used.
- Reverse groups whose lengths are the decimal digits of the key, repeated. A 0 digit is a group of length 10.
- Substitute between the column-filled plaintext square and the row-filled ciphertext square keyed by the English cardinal of the number (no "and").
- `solve_bazeries(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No search for an unknown number is registered. Supply the key.

## Verification certificate

`engine/data/bazeries_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `BazeriesCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Bazeries number.
