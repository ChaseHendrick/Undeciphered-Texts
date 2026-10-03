# Condi

The [ACA Condi sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf) uses a keyword alphabet, an initial offset, and feedback from each plaintext letter. Keyword duplicates are removed, unused A-Z letters are appended, and the alphabet may be rotated. The next offset is the preceding plaintext letter's **one-based** position in that alphabet. Word divisions and punctuation are retained.

```python
from engine.solvers.condi import condi_decrypt, solve_condi

plaintext = condi_decrypt(ciphertext, keyword="STRANGE", initial_offset=25, alphabet_shift=21)
result = solve_condi(ciphertext, keyword="STRANGE", initial_offset=25, alphabet_shift=21)
```

`condi_alphabet(keyword, shift=0)` rotates the deduplicated alphabet left. `condi_encrypt` and `condi_decrypt` uppercase A-Z letters while preserving all non-letter separators. Separators do not advance the feedback state. The keyword and text require at least one A-Z letter. Non-ASCII alphabetic characters fail validation. Text inputs are limited to 1,000,000 characters. Initial offsets are integers 0 through 26; 0 and 26 are equivalent. Alphabet shifts are 0 through 25. Boolean and noninteger settings are rejected.

The complete printed example has 83 letters, keyword STRANGE, initial offset 25, and alphabet `VWXYZSTRANGEBCDFHIJKLMOPQU`. This is the ordinary keyed alphabet rotated left 21. The published ciphertext decrypts exactly with these supplied settings, preserving the printed word divisions. [The certificate](../engine/data/condi_certificate.json) records the literal plaintext/ciphertext and SHA-256 over uppercase A-Z plaintext bytes. The PDF was downloaded and visually checked on 3 October 2026; its hash is also recorded. The `SolveResult` wrapper uses `mode: known_key` and an informational score equal to the recovered letter count.

## Bounded dictionary and parameter candidates

```python
from engine.reverse_engineer import Crib
from engine.solvers.condi import infer_condi

report = infer_condi(
    ciphertext,
    keywords=("PLANET", "SECRET", "CIPHER"),
    cribs=(Crib(0, "MEETINGATDAWNUS"),),
    max_checks=3000,
    max_candidates=1000,
)
```

Inference does not receive a selected keyword or its shift/offset. It tests the explicitly supplied finite dictionary, alphabet shifts, and initial offsets. Default shifts and offsets cover 0 through 25. Supplied offset 26 is canonicalized to 0; duplicate settings and keyword repeats do not create extra evidence. Cribs use the shared `engine.reverse_engineer.Crib` type and zero-based normalized A-Z positions. Overlapping cribs must agree. Word separators are omitted in the candidate prediction stream.

Limits are 512 ciphertext letters, 256 dictionary entries of at most 128 characters each, 100,000 settings checks, and 10,000 retained candidates. Every keyword/shift/offset combination consumes one check. A truncated search sets `search_complete: false`, `exhausted: true`, and an exhaustion reason. `claimed_plaintext` stays null. Results are compatible candidates inside the supplied dictionary; the search does not enumerate all 26-letter alphabets. The synthetic certificate fixture demonstrates recovery from a three-entry dictionary and a 15-letter crib. It is not an attack on a named historical target.

The report exposes `.candidates`, `.checks`, `.search_complete`, `.exhausted`, `.bounds`, and `.to_dict()`, matching the corresponding Progressive Key inference structure. This permits a caller to compare bounded families with the same crib coordinates while retaining each family's assumptions. A candidate's crib fit or reencryption does not establish a historical decipherment.

```sh
.venv/bin/python -m unittest tests.test_condi -v
```
