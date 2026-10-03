# Sequence Transposition

This supplied-key helper implements the [ACA Sequence Transposition sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/SequenceTransposition.pdf).
Its inspected diagram uses keyword `GUMMYBEARS`, primer `69315`, and plaintext
`THEEARLYBIRDGETSTHEWORM`. Its letter ciphertext is
`YHOMARTBDETHIGWLRESEERT`; the complete printed frame is
`69315 YHOMA RTBDE THIGW LRESE ERT 9` followed by a period.

```python
from engine.solvers.sequence_transposition import sequence_transposition_decrypt

plain = sequence_transposition_decrypt(
    "69315 YHOMA RTBDE THIGW LRESE ERT 9.", "GUMMYBEARS")
```

The five primer digits grow by units-only chain addition: successive neighboring
pairs produce the sixth, seventh and later digits. Keyword letters receive
alphabetical ranks, breaking duplicate-letter ties from left to right; rank
ten is written zero. Plaintext positions are assigned chain digits and gathered
by digit in the keyword's original column order. Empty digit columns contribute
no letters. Decryption restores the original positions from their known lengths.

`sequence_digits`, `sequence_key_ranks`, `sequence_transposition_encrypt`,
`sequence_transposition_decrypt`, and `solve_sequence_transposition` are the
public helpers. The keyword/phrase must contain exactly ten ASCII letters after
spacing and punctuation are removed. The primer is exactly five ASCII digits
in a string, preserving leading zeros. Text has 1 through 4,096 A-Z letters;
digits in letter-only input and non-ASCII alphabetic characters are rejected.
Output has no restored word boundaries.

Encryption returns letter ciphertext unless `framed=True`, which adds the
primer, five-letter groups, and the final chain digit. Decryption with no primer
argument requires that complete frame and verifies its final digit. Decryption
with an explicit primer accepts letter ciphertext and an optional
`check_digit` string. In the published example the final chain digit is `9`,
matching the printed check. This catches some transmission/length errors and
is not authentication; many corruptions retain the same digit.

The [certificate](../engine/data/sequence_transposition_certificate.json) hashes
actual recovered letters from the printed vector. Tests also check the literal
chain and rank diagram, malformed/incorrect checks, short texts, leading-zero
primers, duplicate keywords, and a separate position-sort oracle. The keyword
and primer are supplied; there is no unknown-key recovery claim.

```sh
.venv/bin/python -m unittest tests.test_sequence_transposition -v
```
