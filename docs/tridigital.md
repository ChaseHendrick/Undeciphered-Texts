# Tridigital cipher (known-key solver)

`engine/solvers/tridigital.py` decrypts a **known** Tridigital key. `tests/test_tridigital.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Tridigital cipher sheet (fetched 2026-10-02):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Tridigital.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Tridigital.pdf)

| Field | Value |
| --- | --- |
| Digit keyword | `NOVELCRAFT` (numbered `6703528149`, with 0 standing for 10) |
| Alphabet keyword | `DRAGONFLY` |
| Plaintext sentence | the ides of march |
| Plaintext recovered | `THE IDES OF MARCH` |
| Ciphertext | `03095 60795 89107 73.` |

The sheet places the numbered keyword above a block 10 columns wide. The mixed alphabet fills nine columns in rows, and the last column stays blank. Its digit, here `9`, separates words. Any other digit replaces every letter in that column, so one digit stands for two or three letters.

The joined ciphertext digits are `03095607958910773`.

## How a single reading is chosen

The key fixes the columns. It does not fix one letter per digit. The solver splits the ciphertext on the separator and, for each word, keeps the lexicon word with the best frequency rank whose letters sit in those columns.

The lexicon is `engine/data/tridigital_lexicon.txt`: the 40,000 most frequent English words, most frequent first. Word membership is the public-domain `words_alpha` list (dwyl/english-words). Order is Peter Norvig's `count_1w.txt`. Both were fetched 2026-10-02.

For the ACA sentence that rule returns `THE IDES OF MARCH`.

## Second published walk-through

CryptoCrack's Tridigital page (fetched 2026-10-02) prints digit keyword `TRAMPOLINE` (digits `0915874362`), alphabet keyword `OSCARWILDE`, and the sentence "Some cause happiness wherever they go others whenever they go." Encryption with those keys reproduces the ciphertext printed there. That page is an encryption check, not the certificate example. The word "go" shares its columns with the more frequent word "up", so the ranked reading is not that sentence.

[https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/tridigital](https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/tridigital)

## What the engine does

- Number the 10-letter digit keyword alphabetically: 1 through 9, then 0. Ten distinct letters are required.
- Build the mixed alphabet from the second keyword, then the unused letters.
- Write that alphabet in rows of nine. The tenth column is the word separator.
- `tridigital_encrypt` replaces each letter by its column digit and each word space by the separator.
- `solve_tridigital(ciphertext, key=...)` takes a key of the form `DIGITKEYWORD|ALPHABETKEYWORD` and returns a `SolveResult`.
- No blind keyword search is registered. Supply both keywords.

## Verification certificate

`engine/data/tridigital_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `TridigitalCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the ACA example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Tridigital keyword.
- Treat the ranked lexicon reading as the only string of letters the columns allow.
