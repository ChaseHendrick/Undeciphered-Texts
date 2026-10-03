# Lumen braid

New files only: `engine/solvers/lumen_braid.py`, `engine/data/lumen_braid_certificate.json`, and `tests/test_lumen_braid.py`. This note does not change other solvers, image assets, or army-message experiments. `docs/assets/readme-hero.jpg` is not part of this change.

## Original method, not a decipherment

The lumen braid is an original method written for this repository. It is verified by the known-plaintext certificate in `engine/data/lumen_braid_certificate.json`, which records the cipher name, the plaintext, the ciphertext, and the SHA-256 of that plaintext. The unit test decrypts the certificate ciphertext back to that plaintext and checks the hash.

This is not a reading of an ancient script. It is not a reading of army message Nr. 86. It is not Playfair, bifid, Vigenère, or two-square. It does not claim a decipherment of Voynich, Linear A, the Indus script, or any other undeciphered text.

## Rule

Letters are taken as A–Z and put in rows of five. Even rows are read in column order 0, 2, 4, 1, 3. Odd rows are read in column order 3, 1, 4, 2, 0. Each complete trio `(a, b, c)` of that stream is replaced by `((a+c), (a+b+c), (a+b))` modulo 26. A leftover pair `(a, b)` becomes `(a+b, a+2b)` modulo 26, and a leftover single `p` becomes `(3p+1)` modulo 26. Those three maps are invertible, and the row read is a permutation, so decrypt undoes the sums and then undoes the braid. Characters that are not ASCII letters stay in place, and letter case follows the original skeleton.

## How to run

```bash
python3 -m unittest tests.test_lumen_braid -v
```

A passing run means the certificate ciphertext decrypts to the certificate plaintext and the SHA-256 matches. It does not mean an ancient script or army message Nr. 86 was read.
