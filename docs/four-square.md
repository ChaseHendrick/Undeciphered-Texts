# Four-square: known-key digraph decrypt

`engine/solvers/four_square.py` decrypts a **four-square** ciphertext when
both keywords are supplied. `tests/test_four_square.py` checks that this
recovers the published Wikipedia worked example letter for letter.

This is a **known-cipher** solver for a classical digraph substitution. It
does **not** read an unknown script. It does not search for an unknown key,
and it is **not** a claim about army message Nr. 86.

## Published example (fetched)

Primary source (fetched 2026-10-02, America/New_York):

- https://en.wikipedia.org/wiki/Four-square_cipher

The article's worked example uses keywords `example` (upper-right) and
`keyword` (lower-left). The alphabet omits Q and keeps I and J distinct.
Plaintext squares are the standard alphabet, row-major:

```
A B C D E
F G H I J
K L M N O
P R S T U
V W X Y Z
```

Upper-right square (`example`):

```
E X A M P
L B C D F
G H I J K
N O R S T
U V W Y Z
```

Lower-left square (`keyword`):

```
K E Y W O
R D A B C
F G H I J
L M N P S
T U V X Z
```

Plaintext digraphs printed in the article:

```
he lp me ob iw an ke no bi
```

which is the continuous stream:

```
HELPMEOBIWANKENOBI
```

Ciphertext groups printed in the article:

```
FY GM KY HO BX MF KK KI MD
```

which is the continuous stream:

```
FYGMKYHOBXMFKKKIMD
```

Decrypt of that stream under the same keywords recovers the plaintext
exactly:

```
HELPMEOBIWANKENOBI
```

## Check

```bash
python3 -m unittest tests.test_four_square -v
```

`four_square` is not one of the blind solvers in `SOLVERS`. Those still
recover a key from ciphertext alone. This one is given `example` and
`keyword`.

The verification certificate is `engine/data/four_square_certificate.json`
(cipher name, plaintext, ciphertext, keys, source URL, and the SHA-256 of
the plaintext). The unit test recomputes that hash and decrypts the
ciphertext, matching `docs/verification-certificates.md`.

## Scope

- Classical four-square only (four squares, digraph substitution, Q omitted).
- Both keywords required.
- Not a decipherment of Linear A, Indus, Voynich, Rongorongo, or any other
  unknown script.
- Not a reading or claim about army message Nr. 86.
