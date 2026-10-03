# Redefence

The [ACA Redefence sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Redefence.pdf)
describes a zigzag fence whose rows are read in keyed order, starting at a
chosen point in the zigzag cycle. The printed diagram gives top-to-bottom row
ranks `213`, offset `0`, plaintext `CIVILWARFIELDCIPHER`, and ciphertext
`IIWRILCPECLFDHVAEIR`. It also gives the equivalent key `312`, offset `2`.
The diagram and both equivalents are checked by the tests.

```python
from engine.solvers.redefence import redefence_decrypt, search_redefence

plain = redefence_decrypt("IIWRI LCPEC LFDHV AEIR", "213", offset=0)
report = search_redefence(ciphertext, min_rails=3, max_rails=5,
                         max_keys=5000, max_candidates=10)
```

Key digits are readout ranks attached to the physical rows, from top to bottom.
They are a permutation of `1..r` for 3 through 7 rails. Integer sequences are
also accepted. The offset advances the downward-starting fence by that many
positions before the first letter; its range is `0..2*(r-1)-1`.
Known-key encryption/decryption accepts at most 4,096 A-Z letters. ASCII
punctuation and spacing are removed, and non-ASCII alphabetic characters are
rejected. Word boundaries are not reconstructed from ciphertext grouping.

Blind search accepts 4 through 1,024 letters and enumerates every row
permutation and offset in the requested rail range. The default 3 through 5
rails covers 1,128 keys. It scores plaintext with the existing English model,
retains at most `max_candidates` results, and stops at `max_keys`. Caps are
100,000 examined keys and 100 retained candidates. Expanding the bounds adds
work; there is no wall-clock deadline in this API.

`RedefenceSearchResult` reports examined/total keys, `search_complete`,
`stop_reason`, and score ties. Equivalent keys and identical plaintexts remain
separate key hypotheses. `uniqueness` always says `not_established`: exhausting
this key range does not prove the family or make the best English score a
verified historical reading. `solve_redefence` returns `SolveResult`, using a
supplied key if given and a clearly labeled score-ranked candidate otherwise.

The [certificate](../engine/data/redefence_certificate.json) hashes the recovered
published example. The blind regression uses literal ciphertext of the existing
original harbor fixture; no key or plaintext is passed to search. A separate
direction-walking oracle checks every key/offset for 3 and 4 rails, including
short uneven fences. These establish the published transform and the stated
bounded behavior, with no new historical solve claimed.

```sh
.venv/bin/python -m unittest tests.test_redefence -v
```
