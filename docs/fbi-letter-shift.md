# FBI one-letter shift (known-answer check)

`engine/solvers/fbi_letter_shift.py` decrypts the **known** one-letter right shift printed by the FBI. `tests/test_fbi_letter_shift.py` checks that this recovers that published example letter for letter.

This is a **known classical-cipher** check (a known-answer check of a published method). It is **not** an unknown-script reading. It is **not** a new break of Kryptos K4 or of any unsolved text. It does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or army message Nr. 86.

## Published worked example (fetched)

Source: FBI, "Help Solve an Open Murder Case, Part 2", captured 2011-04-05 and fetched 2026-10-03 from the Internet Archive:

[https://web.archive.org/web/20110405112022/http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911](https://web.archive.org/web/20110405112022/http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911)

Original page: [http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911](http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911)

The page states four steps: determine the language, determine the system, reconstruct the key, and reconstruct the plaintext. For this example the system is letter substitution and the key is a shift of one letter to the right.

| Field | Value |
| --- | --- |
| Ciphertext | `Nffu nf bu uif qbsl bu oppo` |
| Key | every character shifted one letter to the right (`shift_right` = 1) |
| Plaintext | `Meet me at the park at noon` |

The period after the cipher on the page closes the FBI sentence. It is not part of the ciphertext. The printed solution has no period.

The same page discusses other notes that the FBI says are unsolved. This check does not read those notes.

## What the engine does

- `fbi_letter_shift_encrypt` shifts each letter right by the given count. Spaces and other non-letters stay put. Case follows the input letter.
- `solve_fbi_letter_shift(ciphertext, shift_right=1)` undoes that shift and returns a `SolveResult`.
- The default shift is the published key, not a search over 26 shifts.
- No blind search is registered. Supply the shift.

## Verification certificate

`engine/data/fbi_letter_shift_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `FbiLetterShiftCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this FBI example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of army message Nr. 86, Kryptos K4, Voynich, Linear A, Indus, or rongorongo.
- Claim a reading of the unsolved notes in the same FBI article.
- Search for an unknown shift.
