# Cadenus cipher (known-key solver)

`engine/solvers/cadenus.py` encrypts and decrypts a **known** Cadenus keyword. `tests/test_cadenus.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** helper. It does **not** claim a reading of an ancient script, an unknown language, or any unsolved historical ciphertext.

## Published worked example (fetched)

Source: [American Cryptogram Association, Cadenus cipher sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Cadenus.pdf) (sheet page 38).

| Field | Value |
| --- | --- |
| Keyword | `EASY` |
| Numeric key | `2-1-3-4` (A is 1, E is 2, S is 3, Y is 4) |
| Plaintext letters | `ASEVERELIMITATIONONTHEUSEFULNESSOFTHECADENUSISTHATEVERYMESSAGEMUSTBEAMULTIPLEOFTWENTYFIVELETTERSLONG` |
| Ciphertext | `SYSTRETOMTATTLUSOATLEEESFIYHEASDFNMSCHBHNEUVSNPMTOFARENUSEIEEIELTARLMENTIEETOGEVESITFAISLTNGEEUVOWUL` |

The sheet prints the plaintext as "A severe limitation on the usefulness of the Cadenus is that every message must be a multiple of twenty-five letters long." Spaces and the hyphen in twenty-five are not enciphered. The SHA-256 in `engine/data/cadenus_certificate.json` is of those 100 uppercase letters with no spaces. The sheet groups the ciphertext in blocks of five (`SYSTR ETOMT ... VOWUL`). Those spaces are grouping only and are not in the ciphertext field.

Plaintext is written in rows of four under `E A S Y`. Each column is cycled so the row labeled with that key letter is the new top. Labels are a 25-letter alphabet with V and W in one cell: A on top, then Z down through B. E is the 22nd label, and the 22nd letter of the first column is Y, which is why that cipher column starts with Y. Columns are then placed in alphabetical order (`A E S Y`, numbers 1 2 3 4) and the ciphertext is read by rows.

## What the engine does

- Keep A to Z, drop other characters, and require a length that is a multiple of 25 times the keyword length.
- V and W share one row shift (index 21). They stay distinct when the keyword is alphabetized, so V comes before W.
- A repeated keyword letter keeps left-to-right order: the left copy gets the smaller number.
- `solve_cadenus(ciphertext, keyword=...)` returns a `SolveResult` with the recovered plaintext.
- No blind keyword search is registered in `SOLVERS`. Supply the keyword.

## What it does not do

- Decipher Linear A, Indus, Rongorongo, Phaistos, Voynich, or any undeciphered script.
- Claim a solution of Kryptos K4, army message Nr. 86, or any ciphertext whose plaintext is not cited.
- Pad a message that is not a multiple of 25 times the keyword length. The caller supplies a block of that size, as the published sheet does.
