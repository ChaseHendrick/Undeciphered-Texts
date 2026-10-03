# Kryptos K1: keyed Vigenère

`engine/solvers/keyed_vigenere.py` decrypts a **known** repeating key on a keyword-mixed alphabet. `tests/test_keyed_vigenere.py` checks that this recovers the published Kryptos passage 1 (K1) letter for letter.

This is not a search for an unknown key. It does **not** claim a reading of K4. The same source that publishes K1 says the last 97 characters were unread.

## Published system (fetched)

Primary source: the NSA technical paper released under FOIA Case #61191 on 21 May 2013, DOCID 4051151 (the Kryptos memorandum package also numbered 4050988). Fetched as the Archive.org text of "Kryptos Sculpture FOIA CIA Documentation":

- https://archive.org/stream/KryptosSculptureFOIACIADocumentation/Kryptos%20Sculpture%20FOIA%20CIA%20Documentation%20_djvu.txt
- PDF: https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cia-kryptos-sculpture/doc_1.pdf

The recap of the first section (63 characters, the first two full lines of the copper panel) says:

> The cryptography is a periodic polyalphabetic substitution system employing 10 alphabets. The plain and cipher components are both a keyword mixed sequence based on KRYPTOS, using a repeating key of PALIMPSEST below the index letter K.

The paper prints that plain component as:

```
KRYPTOSABCDEFGHIJLMNQUVWXZ
```

That is the keyword `KRYPTOS` followed by the unused letters of A–Z in order. `C` stays. `K`, `R`, `Y`, `P`, `T`, `O`, and `S` are not written a second time.

Each cipher alphabet is that sequence rotated so the current key letter sits in the column of the index letter `K`. The ten rows for `PALIMPSEST` in the paper are:

| Key letter | Cipher alphabet |
| --- | --- |
| P | `PTOSABCDEFGHIJLMNQUVWXZKRY` |
| A | `ABCDEFGHIJLMNQUVWXZKRYPTOS` |
| L | `LMNQUVWXZKRYPTOSABCDEFGHIJ` |
| I | `IJLMNQUVWXZKRYPTOSABCDEFGH` |
| M | `MNQUVWXZKRYPTOSABCDEFGHIJL` |
| P | `PTOSABCDEFGHIJLMNQUVWXZKRY` |
| S | `SABCDEFGHIJLMNQUVWXZKRYPTO` |
| E | `EFGHIJLMNQUVWXZKRYPTOSABCD` |
| S | `SABCDEFGHIJLMNQUVWXZKRYPTO` |
| T | `TOSABCDEFGHIJLMNQUVWXZKRYP` |

`K` is the first letter of the mixed alphabet, so its column is 0. Decryption is then ordinary Vigenère arithmetic in that alphabet: the plaintext index is the ciphertext index minus the key-letter index, modulo 26. The key repeats. Non-letters are copied and do not advance the key. There are none in K1.

Ciphertext of those two lines, as on the sculpture and in the paper:

```
EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD
```

Letter-by-letter decrypt printed in the paper:

```
BETWEENSUB TLESHADING ANDTHABSCE NCEOFLIGHT
LIESTHENUA NCEOFIQLUS ION
```

which is:

```
BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION
```

A following sentence in the same memo respaces the text and prints `ILLUSION`. The groups immediately above that sentence are `IQLUSION`. The unit test requires `IQLUSION`. It fails if the last word is changed to `ILLUSION`.

Wikipedia, "Solution of passage 1", fetched 2026-10-02, states the same system and the same letters with spaces (https://en.wikipedia.org/wiki/Kryptos):

- Method: Vigenère
- Alphabet: `KRYPTOSABCDEFGHIJLMNQUVWXZ` (the pattern on the right-hand panel)
- Key: `PALIMPSEST`
- Plaintext: `BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION`

## Check

```bash
python -m unittest tests.test_keyed_vigenere -v
python -m engine solve keyed-vigenere \
  EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD \
  --key PALIMPSEST --alphabet KRYPTOS --index K
```

`keyed-vigenere` is not one of the blind solvers in `SOLVERS`. Those still recover a key from ciphertext alone. This one is given `PALIMPSEST` and `KRYPTOS`.

## Not K4

DOCID 4051151 says part 4 (97 characters) had not been read, and that a further breakthrough had not occurred. This repository does not claim a K4 decipherment and does not store a K4 plaintext.
