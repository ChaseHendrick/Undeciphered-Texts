# Playfair: known-key digraph decrypt

`engine/solvers/playfair.py` decrypts a **Playfair** ciphertext when the
keyword that builds the 5×5 square is supplied. `tests/test_playfair.py`
checks that this recovers the published Wikipedia worked example letter for
letter.

This is a **known-cipher** solver for a classical digraph substitution. It
does **not** read an unknown script. It does not search for an unknown key,
and it does not claim a break of an unsolved historical Playfair message.

## Published example (fetched)

Primary source (fetched 2026-10-02, America/New_York):

- https://en.wikipedia.org/wiki/Playfair_cipher

The article's **Example** section uses keyword `playfair example` (I and J
interchangeable). The 5×5 square, filled keyword-first then the remaining
letters of A-Z omitting J, is:

```
P L A Y F
I R E X M
B C D G H
K N O Q S
T U V W Z
```

Message:

```
hide the gold in the tree stump
```

Prepared digraphs (null `X` separates the repeated `E`s in `TREE`):

```
HI DE TH EG OL DI NT HE TR EX ES TU MP
```

Ciphertext groups printed in the article:

```
BM OD ZB XD NA BE KU DM UI XM MO UV IF
```

which is the continuous stream:

```
BMODZBXDNABEKUDMUIXMMOUVIF
```

Decrypt of that stream under the same keyword recovers the prepared
plaintext exactly:

```
HIDETHEGOLDINTHETREXESTUMP
```

## Check

```bash
python3 -m unittest tests.test_playfair -v
```

`playfair` is not one of the blind solvers in `SOLVERS`. Those still recover
a key from ciphertext alone. This one is given `playfair example`.

## Scope

- Classical Playfair only (one square, digraph substitution).
- Known keyword required.
- Not a decipherment of Linear A, Indus, Voynich, Rongorongo, or any other
  unknown script.
