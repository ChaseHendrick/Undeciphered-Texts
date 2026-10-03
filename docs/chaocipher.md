# Chaocipher (known alphabets)

`engine/solvers/chaocipher.py` encrypts and decrypts Chaocipher when both starting alphabets are known. `tests/test_chaocipher.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It checks the revealed algorithm's published test vector. It is **not** a claim that Byrne's challenge exhibits are solved. It does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4, and it is not a claim about army message Nr. 86.

## Published worked example (fetched)

Source: Programming Praxis, Chaocipher, 6 July 2010 (fetched 2026-10-03, America/New_York):

[https://programmingpraxis.com/2010/07/06/chaocipher/](https://programmingpraxis.com/2010/07/06/chaocipher/)

The page states the algorithm Moshe Rubin had just published from John F. Byrne's papers, and it prints this vector.

| Field | Value |
| --- | --- |
| Left disk (ciphertext alphabet) | `HXUCZVAMDSLKPEFJRIGTWOBNYQ` |
| Right disk (plaintext alphabet) | `PTLNBQDEOYSFAVZKGJRIHWXUMC` |
| Plaintext | `WELLDONEISBETTERTHANWELLSAID` |
| Ciphertext | `OAHQHCNYNXTSZJRRHJBYHQKSOUJY` |

Zenith is position 1 and nadir is position 14. Encryption reads the plaintext letter on the right disk and writes the left-disk letter in that same position. Decryption does the reverse. After each letter the left disk rotates that ciphertext letter to position 1, then cycles positions 2 through 14 one place left. The right disk rotates that plaintext letter to position 1, moves position 1 to the end, then cycles positions 3 through 14 one place left.

The page also prints two standalone steps. Left `HXUCZVAMDSLKPEFJRIGTWOBNYQ` with P becomes `PFJRIGTWOBNYQEHXUCZVAMDSLK`. Right `PTLNBQDEOYSFAVZKGJRIHWXUMC` with A becomes `VZGJRIHWXUMCPKTLNBQDEOYSFA`.

## What the engine does

- `chaocipher_encrypt` and `chaocipher_decrypt` take the two starting alphabets.
- Non-letters are dropped. Output is uppercase A-Z.
- Decrypt must start from the original alphabets. A previous call does not leave the disks in place for the next call.
- `solve_chaocipher(ciphertext, left=..., right=...)` returns a `SolveResult`.
- No search over unknown alphabets is registered. Supply both disks.

## Verification certificate

`engine/data/chaocipher_certificate.json` records the cipher name, plaintext, ciphertext, both alphabets, the source URL, and the SHA-256 of the plaintext. `ChaocipherCertificateTest` recomputes that plaintext hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the Programming Praxis vector only.

## What it does not do

- Claim that Byrne's old challenge exhibits are solved.
- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlussel / army message Nr. 86, Kryptos K4, Zodiac, Beale, McCormick, or Voynich.
- Search for unknown disk alphabets.
