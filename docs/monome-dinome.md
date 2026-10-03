# Supplied-key Monome-Dinome

`engine/solvers/monome_dinome.py` implements the [ACA Monome-Dinome sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/MonomeDinome.pdf), printed page 55, fetched and visually inspected on 2026-10-03. The PDF SHA-256 is `77445627e00e37c1dbfd8b6c569a1dad5a0ea39d071501f10bd27b262bad726c`.

The keyword produces a 3 by 8 box. I/J share one entry, and a second letter pair shares another, default Y/Z. The first two entries of `digit_order` label the lower rows; the last eight label columns. Top-row letters receive one column digit. Lower-row letters receive their row digit followed by their column digit. Row and column digits are disjoint, so a complete supplied box gives unambiguous code boundaries.

The printed example uses keyword NOTARIES and digit order `6318927054`:

| Row | 1 | 8 | 9 | 2 | 7 | 0 | 5 | 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Single digit | N | O | T | A | R | I | E | S |
| Prefix 6 | B | C | D | F | G | H | K | L |
| Prefix 3 | M | P | Q | U | V | W | X | Y |

The literal printed ciphertext `60067 60627 53932 51683 46553 44460 87951 68038 60579 5359.` recovers `HIGHFREQUENCYKEYSSHORTENCIPHERTEXT`. The certificate hashes exactly these normalized uppercase letters. The final ciphertext period is explicitly permitted display framing.

```python
from engine.solvers.monome_dinome import monome_dinome_encrypt, monome_dinome_decrypt

cipher = monome_dinome_encrypt("HIGH FREQUENCY KEYS SHORTEN CIPHERTEXT", "NOTARIES", digit_order="6318927054")
plain = monome_dinome_decrypt(cipher, "NOTARIES", digit_order="6318927054")
assert plain == "HIGHFREQUENCYKEYSSHORTENCIPHERTEXT"
```

The default digit order is `0123456789`. `merge=("Q", "Z")`, for example, selects Q as the additional merged representative while retaining mandatory I/J. Merge letters must be distinct uppercase A-Z letters excluding I and J. Keywords contain 1 through 1,000 ASCII letters. Plaintext permits letters and whitespace, capped at 10,000 raw characters; ciphertext permits grouped ASCII digits, capped at 100,000 raw characters. Other punctuation is rejected, except an explicitly permitted final ciphertext framing period.

Encryption omits word spaces and folds merged letters. Decryption cannot recover original word boundaries or distinguish J from I and Z from Y. `solve_monome_dinome` exposes the merges, `lossy: true`, and supplied-key mode. A dangling row prefix or a prefix digit used as a column raises an error. Parsing is linear and bounded, with no unknown-key search or optional dependency.

The tests first failed on the absent module, then checked the independent printed box and vector, recovered-output hash, single and double codes, custom merges, lossy metadata, malformed codes, framing, and input bounds. Run `.venv/bin/python -m unittest tests.test_monome_dinome -v`. This is a known-key classical helper, with no new historical decipherment claim.
