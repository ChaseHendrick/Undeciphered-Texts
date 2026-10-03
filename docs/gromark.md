# Gromark cipher (known-key solver)

`engine/solvers/gromark.py` decrypts a **known** Gromark keyword and 5-digit primer. `tests/test_gromark.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: American Cryptogram Association, Gromark cipher sheet (fetched 2026-10-02):

[https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf](https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf)

| Field | Value |
| --- | --- |
| Keyword | `ENIGMA` (column order 264351) |
| Primer | `23452` |
| Plaintext | `THEREAREUPTOTENSUBSTITUTESPERLETTER` |
| Ciphertext | `NFYCKBTIJCNWZYCACJNAYNLQPWWSTWPJQFL` |

The sheet prints the plaintext in lowercase as `thereareuptotensubstitutesperletter`. This solver returns those letters in A-Z.

The sheet builds a K2M block from ENIGMA and reads columns in alphabetical order. The cipher alphabet it prints is `AJRXEBKSYGFPVIDOUMHQWNCLTZ`. The numeric key it prints is `23452579772664982037023072537978066`. Plaintext T with the first digit 2 is counted two places to the right (V), and the cipher alphabet under V is N, the first ciphertext letter. The grouped line on the sheet is `23452 NFYCK BTIJC NWZYC ACJNA YNLQP WWSTW PJQFL 6`. The leading `23452` is the primer and the trailing `6` is the last digit of that numeric key, written as a check. The letter ciphertext is the groups joined.

## What the engine does

- The key string is a keyword and a 5-digit primer, for example `ENIGMA 23452`. Duplicate keyword letters are dropped.
- The cipher alphabet is the K2M column transcription: keyword, then unused A-Z letters, filled in rows, columns read in alphabetical order of the keyword.
- The primer grows by the units digit of each successive pair (1st+2nd makes the 6th) until it is as long as the letter stream.
- Encryption counts right in A-Z by that digit and reads the cipher alphabet. Decryption reverses that step.
- `solve_gromark(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind key search is registered. Supply the keyword and the primer.

## Verification certificate

`engine/data/gromark_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `GromarkCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown Gromark keyword or primer.
