# Prism latch

New files only: `engine/solvers/prism_latch.py`, `engine/data/prism_latch_certificate.json`, `tests/test_prism_latch.py`, and this note. This change does not edit the lumen-braid cipher, other solvers, image assets, or army-message experiments. `docs/assets/readme-hero.jpg` is not part of this change.

## Original method, not a decipherment

The prism latch is an original method written for this repository. It is verified by the known-plaintext certificate in `engine/data/prism_latch_certificate.json`, which records the cipher name, the plaintext, the ciphertext, and the SHA-256 of that plaintext. The unit test decrypts the certificate ciphertext back to that plaintext and checks the hash.

This is not a reading of an ancient script. It is not a reading of army message Nr. 86. It is not a row of five, Playfair, bifid, Vigenère, two-square, or the lumen braid. It does not claim a decipherment of Voynich, Linear A, the Indus script, or any other undeciphered text.

## Rule

ASCII letters are numbered A=0 through Z=25. Letters whose positions in that stream are triangular numbers (0, 1, 3, 6, ...) move to the front in the order those positions occur, and the other letters follow in their original order. Each block of four values `(a, b, c, d)` is then replaced by `(a+b, b+c, c+d, d+2a+1)` modulo 26. A leftover triple `(a, b, c)` becomes `(a+2b, b+2c, c+2a)`, a leftover pair `(a, b)` becomes `(a+b, 2a+b)`, and a leftover single `p` becomes `(5p+3)`, all modulo 26. Each of those maps is invertible and the triangular move is a permutation, so decrypt undoes the sums and then puts the triangular positions back. Characters that are not ASCII letters stay in place, and letter case follows the original skeleton.

## How to run

```bash
python3 -m unittest tests.test_prism_latch -v
```

A passing run means the certificate ciphertext decrypts to the certificate plaintext and the SHA-256 matches. It does not mean an ancient script or army message Nr. 86 was read.
