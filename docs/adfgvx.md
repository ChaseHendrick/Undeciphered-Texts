# ADFGVX: known-key decrypt

`engine/solvers/adfgvx.py` decrypts an **ADFGVX** ciphertext when both keys
are supplied: the 6×6 substitution square and the columnar transposition
keyword. `tests/test_adfgvx.py` checks that this recovers the published
Wikipedia worked example letter for letter.

This is a **known-cipher** solver for a classical fractionating transposition.
It does **not** read an unknown script. It does not search for an unknown
key, and it does not claim a break of an unsolved historical ADFGVX message.

## Published example (fetched)

Primary source (fetched 2026-10-02, America/New_York):

- https://en.wikipedia.org/wiki/ADFGVX_cipher

The article's **ADFGVX** section (the June 1918 6×6 cipher, not the earlier
5×5 ADFGX example) codes the square with the Dutch keyword
`nachtbommenwerper`. Unique keyword letters, then the rest of A–Z, give
`NACHTBOMEWRPDFGIJKLQSUVXYZ`. Digits are inserted after the first A–J
(A→1, B→2, … I→9, J→0). The square, rows and columns labeled `ADFGVX`, is:

```
  | A D F G V X
--+------------
A | N A 1 C 3 H
D | 8 T B 2 O M
F | E 5 W R P D
G | 4 F 6 G 7 I
V | 9 J 0 K L Q
X | S U V X Y Z
```

Message:

```
attack at 1200am
```

Fractionated coordinates:

```
AD DD DD AD AG VG AD DD AF DG VF VF AD DX
```

Transposition keyword `PRIVACY`. Reading the columns in alphabetical key
order produces the groups printed in the article:

```
DGDD DAGD DGAF ADDF DADV DVFA ADVX
```

which is the continuous stream:

```
DGDDDAGDDGAFADDFDADVDVFAADVX
```

Decrypt of that stream under the same keys recovers the enciphered
plaintext exactly. Spaces are not in the ADFGVX alphabet, so the recovered
stream is the published message with spaces removed:

```
ATTACKAT1200AM
```

## Check

```bash
python3 -m unittest tests.test_adfgvx -v
```

`adfgvx` is not one of the blind solvers in `SOLVERS`. Those still recover
a key from ciphertext alone. This one is given `nachtbommenwerper` and
`PRIVACY`.

## Scope

- Classical ADFGVX only (6×6 Polybius square over A–Z and 0–9, then one
  columnar transposition).
- Both keys required.
- Not a decipherment of Linear A, Indus, Voynich, Rongorongo, or any other
  unknown script.
