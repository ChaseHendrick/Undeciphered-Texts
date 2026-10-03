# Numbered Key

The [ACA Numbered Key sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/NumberedKey.pdf)
preserves repeated letters of a keyword or phrase, appends missing A-Z letters,
and numbers a rotation of that extended key. Each plaintext letter can use any
of its numbered positions. The inspected example uses `I like ciphers.` and
starts numbering at the original extended key's index `18`, the letter M.

```python
from engine.solvers.numbered_key import numbered_key_decrypt

plain = numbered_key_decrypt(
    "04 19 20 21 02 23 25 04 02 22 05 16 16 15 22 22 11 22 23 12 07 23 "
    "09 22 05 01 25 20 21 16 02 01 22 04 21 05 16 04 17 02 01",
    "I like ciphers.", start=18)
```

The result is `THEROADTOSUCCESSISALWAYSUNDERCONSTRUCTION`. Repeated I values
at codes 11, 13 and 17 are homophones; deduplicating the phrase would change the
cipher. The published worksheet uses different homophones for repeated letters.

`numbered_key_alphabet`, `numbered_key_encrypt`, `numbered_key_decrypt`, and
`solve_numbered_key` require a supplied phrase and zero-based `start` index
within its unrotated extended key. Default encryption chooses the first
numbered occurrence of each letter. An optional `homophone_indices` sequence
selects a zero-based alternative for each plaintext letter; tests replay the
sheet's choices to reproduce its literal ciphertext. Other valid selections
produce different ciphertext with the same plaintext and key.

Keys/text normalize to uppercase ASCII letters, dropping punctuation and spaces.
Non-ASCII alphabetic characters are rejected. The extended key is limited to
100 positions to retain two-digit codes `00..99`. Ciphertext accepts at most
4,096 space-separated two-digit ASCII codes, with an optional final period,
or a finite sequence of code integers. Every code must index the actual table.
The helper rejects negative/out-of-range codes, booleans, invalid rotations,
wrong-length homophone selections and nonexistent alternatives. Plaintext is
limited to 4,096 letters; word boundaries are not reconstructed.

The [certificate](../engine/data/numbered_key_certificate.json) stores the literal
printed codes and hashes actual recovered letters. Tests check every letter
under every rotation of three keys using a separate index-mapping oracle.
This is supplied-key homophonic substitution, with no blind keyword search or
historical decipherment claim.

```sh
.venv/bin/python -m unittest tests.test_numbered_key -v
```
