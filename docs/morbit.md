# Supplied-key Morbit

`engine/solvers/morbit.py` implements the [ACA Morbit sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Morbit.pdf). The sheet was fetched and visually inspected on 2026-10-03; its PDF SHA-256 is `0c3877ad5188e5972f44110a45677030e1f0ea25020ff3927494a07d381ff998`.

A nine-letter keyword is ranked alphabetically, breaking duplicate-letter ties left to right. WISECRACK produces `958427136`. Those digits label the ordered Morse pairs `.. .- .x -. -- -x x. x- xx`. A single `x` separates characters, and `xx` separates words. One final `x` pads an odd-length stream.

The literal printed ciphertext is `27435 88151 28274 65679 378.`. It recovers `ONCE UPON A TIME`. The prose example has a sentence period, but its printed Morse stream omits it. The ciphertext period is display framing. The certificate hashes the recovered uppercase words and spaces, without inventing punctuation.

```python
from engine.solvers.morbit import morbit_encrypt, morbit_decrypt, solve_morbit

cipher = morbit_encrypt("ONCE UPON A TIME", "WISECRACK")
assert cipher == "27435881512827465679378"
assert morbit_decrypt(cipher, "WISECRACK") == "ONCE UPON A TIME"
result = solve_morbit("27435 88151 28274 65679 378.", key="WISECRACK", terminal_period=True)
```

`morbit_key` accepts nine ASCII keyword letters or a permutation of digits 1 through 9. Plaintext supports the existing fractionated-Morse letter, number, and punctuation table. Case becomes uppercase and whitespace becomes single word spaces. Ciphertext permits ASCII digits and whitespace grouping; a final period requires the explicit `terminal_period=True` option. A plaintext period is a Morse character and must actually be encoded.

Leading dividers, excessive dividers, empty tokens, invalid Morse codes, digit zero, and malformed keys raise errors. Plaintext is capped at 10,000 characters and ciphertext at 100,000 raw characters. Runtime is linear in these finite inputs, with no search or optional dependency. Only the shared Morse tables are reused; the older lenient decoder is not used.

The tests first failed with a missing-module import, then checked the independent printed vector, recovered-output hash, general punctuation, stable duplicate ranks, framing, strict gaps, and bounds. Run `.venv/bin/python -m unittest tests.test_morbit -v`. The helper requires its key and makes no unknown-key or historical decipherment claim.
