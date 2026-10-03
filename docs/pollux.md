# Supplied-map Pollux

`engine/solvers/pollux.py` follows the [ACA Pollux sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Pollux.pdf), fetched and visually inspected on 2026-10-03. Its PDF SHA-256 is `ad777b6e3ed4fe75ddf1f1af148ef12c67ff2287a17743506bc20cc05a4c1405`.

Every decimal digit represents a dot, dash, or divider. Several digits can represent the same symbol. Characters are separated by one divider and words by two. The printed map, reordered into digit order 0 through 9, is `.x-..x.--x`. The literal ciphertext `08639 34257 02417 68596 30414 56234 90874 5360.` decodes to `LUCK HELPS`.

The sentence period shown in the prose example is absent from its printed Morse stream. Its ciphertext period is display framing. `terminal_period=True` permits that final display mark explicitly; ordinary decryption rejects it. Encoded plaintext punctuation is recovered only when the digit stream actually contains its Morse code.

```python
from engine.solvers.pollux import pollux_decrypt, pollux_encrypt, solve_pollux

key = ".x-..x.--x"  # digit order 0 through 9
result = solve_pollux("08639 34257 02417 68596 30414 56234 90874 5360.", key=key, terminal_period=True)
assert result.plaintext == "LUCK HELPS"
assert pollux_decrypt(pollux_encrypt("SOS! 2026?", key), key) == "SOS! 2026?"
```

Keys are either a ten-symbol string or a complete mapping from ASCII digit strings to individual `.`, `-`, and `x` symbols. All three types must occur. The source's usual 4/3/3 allocation is supported but not required. Encryption cycles deterministically through each symbol's digits. To reproduce a particular homophonic choice sequence, pass `choices=` with one correctly mapped digit per Morse symbol; there is no random callback or implicit probability model.

The strict decoder rejects missing or ambiguous map entries, invalid Morse tokens, boundary gaps, and three consecutive dividers. It permits no trailing padding. Plaintext case and word whitespace normalize as in Morbit. Limits are 10,000 plaintext characters and 100,000 raw ciphertext or choice characters. Only finite linear transformations run; the standard library is sufficient.

Tests first failed before the module existed, then checked the independently printed ciphertext and raw recovered-text hash, its explicit encryption choices, alternate homophones, punctuation, invalid maps, framing, and bounds. Run `.venv/bin/python -m unittest tests.test_pollux -v`. The digit map is supplied. No unknown-map recovery or new historical decipherment is claimed.
