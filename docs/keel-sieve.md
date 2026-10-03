# Keel sieve

New files only: `engine/solvers/keel_sieve.py`, `engine/data/keel_sieve_certificate.json`, `tests/test_keel_sieve.py`, and this note. This change does not edit the lumen-braid cipher, the prism-latch cipher, other solvers, image assets, four-square files, or Porta files. `docs/assets/readme-hero.jpg` is not part of this change.

## Original method, not a decipherment

The keel sieve is an original method written for this repository. It is verified by the known-plaintext certificate in `engine/data/keel_sieve_certificate.json`, which records the cipher name, the plaintext, the ciphertext, and the SHA-256 of that plaintext. The unit test decrypts the certificate ciphertext back to that plaintext and checks the hash.

This is not a reading of an ancient script. It is not a reading of army message Nr. 86. It is not rows of five, a triangular-index latch, Playfair, bifid, Vigenère, Porta, two-square, the lumen braid, or the prism latch. It does not claim a decipherment of Voynich, Linear A, the Indus script, or any other undeciphered text.

## Rule

ASCII letters are numbered A=0 through Z=25. Letters at perfect-square positions (0, 1, 4, 9, ...) move to the end in the order those positions occur, and the other letters stay in front in their original order. The moved stream is then sieved by `c0 = (3*p0 + 1)` and `ci = (pi + 2*p(i-1) + 3*i + 1)`, both modulo 26. Three is coprime to 26, so the first step is invertible, each later step names `pi` once, and the square move is a permutation, so decrypt undoes the chain and then puts the square positions back. Characters that are not ASCII letters stay in place, and letter case follows the original skeleton.

## How to run

```bash
python3 -m unittest tests.test_keel_sieve -v
```

A passing run means the certificate ciphertext decrypts to the certificate plaintext and the SHA-256 matches. It does not mean an ancient script or army message Nr. 86 was read.
