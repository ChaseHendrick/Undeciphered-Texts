# Solitaire / Pontifex (known-deck keystream)

`engine/solvers/solitaire.py` turns a known 54-card deck, or a passphrase that keys that deck, into a keystream and adds it to plaintext modulo 26. `tests/test_solitaire.py` checks that this matches published worked examples letter for letter.

This is a **known classical-cipher** solver (a known-cipher solver). It is **not** an unknown-script reading. It does **not** claim Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86. It does not read Linear A, the Indus script, or rongorongo.

## Published worked examples (fetched)

Source: Bruce Schneier, "The Solitaire Encryption Algorithm", version 1.2 (26 May 1999), fetched 2026-10-03:

[https://www.schneier.com/academic/solitaire/](https://www.schneier.com/academic/solitaire/)

The page calls the cipher Solitaire. In Neal Stephenson's Cryptonomicon the same steps use the code name Pontifex.

| Field | Value |
| --- | --- |
| Sample 1 deck | Unkeyed bridge order: clubs, diamonds, hearts, spades, A joker, B joker |
| Sample 1 plaintext | `AAAAA AAAAA` |
| Sample 1 ciphertext | `EXKYI ZSGEH` |
| Sample 2 passphrase | `FOO` (method 3; the comma in the page's quotation is punctuation) |
| Sample 2 plaintext | fifteen As |
| Sample 2 ciphertext | `ITHZU JIWGR FARMW` |
| Sample 3 passphrase | `CRYPTONOMICON` |
| Sample 3 message | `SOLITAIRE` |
| Sample 3 letters enciphered | `SOLITAIREX` (final X fills the last group of five) |
| Sample 3 ciphertext | `KIRAK SFJAN` |

Cards are numbered in bridge order. Clubs are 1 through 13, diamonds 14 through 26, hearts 27 through 39, and spades 40 through 52. The A joker and the B joker both count as 53. Output letters use clubs and hearts as 1 through 13, and diamonds and spades as 14 through 26. A joker output is skipped.

Each keystream step moves the A joker down one card, moves the B joker down two, triple-cuts around the two jokers, then count-cuts on the bottom card. The top card selects the output card, which stays in the deck. A card that wraps from the bottom is inserted just below the top card.

Passphrase keying (method 3) starts from the unkeyed deck and, for each letter, runs those steps but replaces the output with a second count cut whose length is the letter (A=1 through Z=26). The optional step that places the jokers from the last two passphrase letters is **not** used. The page says that step is not used in the samples.

## What the engine does

- `solitaire_encrypt` keeps letters, pads the last group with X, adds the keystream modulo 26 (A=1), and groups by fives.
- `solitaire_decrypt` subtracts the same keystream. It keeps a filler X; it does not try to guess which X was padding.
- An empty passphrase is the unkeyed deck. A list of 54 cards (1..52 plus jokers 53 and 54) is an explicit known deck. Pass a passphrase or a deck, not both.
- `solve_solitaire(ciphertext, key=...)` or `solve_solitaire(ciphertext, deck=...)` returns a `SolveResult`.
- No search for an unknown deck is registered. Supply the deck or the passphrase.

## Verification certificate

`engine/data/solitaire_certificate.json` records the cipher name, the sample 3 letters `SOLITAIREX`, the ciphertext `KIRAK SFJAN`, the passphrase `CRYPTONOMICON`, the source URL, and the SHA-256 of `SOLITAIREX` (the filler X is included). `SolitaireCertificateTest` recomputes that hash and checks encrypt and decrypt. Sample 1 (`EXKYI ZSGEH`) and sample 2 (`ITHZU JIWGR FARMW`) are unit tests, not that hash. See [verification-certificates.md](verification-certificates.md). The certificate checks Schneier's published examples only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86.
- Search for an unknown deck or passphrase.
- Apply the optional joker-placement keying step.
- Treat Solitaire as a break of a real message. The page's samples are test vectors only, and Schneier says a real passphrase should be much longer.
