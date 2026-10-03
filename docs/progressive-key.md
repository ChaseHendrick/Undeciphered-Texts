# Progressive Key Vigenere

The [ACA Progressive Key sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/ProgressiveKey.pdf) first applies periodic Vigenere with the keyword, then adds a progressing Caesar shift to each keyword-length group. For progression 1 the group shifts are A, B, C; for progression 2 they are A, C, E. This module implements that Vigenere variant with zero initial progression:

`cipher[i] = (plain[i] + key[i % period] + progression * (i // period)) % 26`

```python
from engine.solvers.progressive_key import progressive_key_decrypt, solve_progressive_key

plaintext = progressive_key_decrypt(ciphertext, keyword="GRAPEFRUIT", progression=1)
result = solve_progressive_key(ciphertext, keyword="GRAPEFRUIT", progression=1)
```

Keyword repeats are retained; the normalized keyword length sets the period. Inputs use A-Z letters with separators omitted and uppercase output. Non-ASCII alphabetic characters fail validation. Keywords contain 1 through 128 normalized letters. Text input is limited to 1,000,000 characters. Progression is an integer 0 through 25; 0 reduces to periodic Vigenere. No final-group padding is added. The `SolveResult` wrapper records `mode: known_key`; it does not infer a keyword.

The ACA sheet prints a 40-letter final ciphertext but only 30 aligned plaintext letters in the worked table. [The published certificate](../engine/data/progressive_key_certificate.json) therefore certifies only that independently printed prefix, using GRAPEFRUIT and progression 1. Its hash covers 30 uppercase A-Z ASCII plaintext bytes. The remaining ten ciphertext letters have no independently printed answer on this sheet and are not certified. The source PDF and table were visually checked on 3 October 2026, and its downloaded hash is recorded.

## Bounded inference without a supplied key

```python
from engine.reverse_engineer import Crib
from engine.solvers.progressive_key import infer_progressive_key

report = infer_progressive_key(
    ciphertext,
    cribs=(Crib(0, "THEQUICKBROWNFOX"),),
    max_period=8,
    progressions=tuple(range(26)),
    max_checks=4096,
    max_candidates=1000,
)
```

Each tested period/progression pair consumes one check. Known plaintext determines keyword slots by subtracting the candidate group progression from ciphertext/plaintext differences. Every supplied position must fit the same slot. Cribs use the shared `engine.reverse_engineer.Crib` and zero-based normalized A-Z offsets. Duplicate crib positions add no evidence. Unknown keyword slots remain `?`, and predictions using those slots also remain `?`.

The synthetic certificate fixture supplies only the first 16 letters of a 67-letter message. With period at most 8 and progression 0 through 25, the search finds one compatible LEMON/period 5/progression 7 candidate and predicts the remaining 51 letters exactly. The keyword and progression are expected outputs in the test, not inputs to inference. Ciphertext was generated independently using modular arithmetic before implementation. This verifies recovery within stated synthetic bounds, not a named historical decipherment.

Limits are 512 normalized ciphertext letters, periods 1 through 128, up to 26 requested progression values, 100,000 checks, and 10,000 retained candidates. The tested period bound is also limited by ciphertext length. A zero check budget is allowed and immediately reports incomplete. Check or candidate exhaustion sets `search_complete: false`, `exhausted: true`, and an explicit reason. No candidate can mean the completed tested family was inconsistent, or an incomplete search found none; inspect completion status. A single candidate establishes compatibility only inside these bounds. `claimed_plaintext` always stays null.

Reports expose `.candidates`, `.checks`, `.search_complete`, `.exhausted`, `.bounds`, and `.to_dict()`, compatible with the [Condi candidate tool](condi.md). Combining these reports is a repository-specific analysis workflow, not a claim of a new cryptanalytic method. Supplied-key helpers remain separate from candidate inference and outside text-only solve dispatch.

```sh
.venv/bin/python -m unittest tests.test_progressive_key -v
```
