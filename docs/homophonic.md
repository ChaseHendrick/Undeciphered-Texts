# ACA four-row Homophonic

`engine/solvers/homophonic.py` implements the [ACA Homophonic sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Homophonic.pdf), printed page 51, fetched and visually inspected on 2026-10-03. This particular construction has four cyclic numeric rows under the straight 25-letter alphabet with I/J merged. It differs from arbitrary homophonic substitution and the repository's separate [fixed-temperature attack](homophonic-fixed-temperature.md).

The four keyword letters identify the columns where codes 01, 26, 51 and 76 start. Each row continues cyclically across the alphabet; row four ends at 00, which denotes the hundredth entry. Any of a letter's four row codes may encode it. The worksheet supplies GOLF, all numeric rows and a literal 22-code example recovering `WORDDIVISIONSMAYBEKEPT`.

```python
from engine.solvers.homophonic import homophonic_decrypt, infer_homophonic
from engine.reverse_engineer import Crib

cipher = "16 26 11 99 69 46 33 03 88 79 54 83 12 06 38 94 67 24 04 00 27 89."
plain = homophonic_decrypt(cipher, key="GOLF", terminal_period=True)
report = infer_homophonic(cipher, cribs=(Crib(0, "WORDD"),),
                         max_checks=100, terminal_period=True)
assert report.key_pattern == "GOLF"
assert report.predicted_plaintext == plain
```

`homophonic_table`, `homophonic_encrypt`, `homophonic_decrypt` and `solve_homophonic` require a four-letter ASCII keyword, with optional key whitespace and J merged into I. The table contains all codes 00 through 99 exactly once. Encryption defaults to each letter's row-zero code; optional `rows` gives one zero-based row 0 through 3 per normalized plaintext letter. Replaying the literal source requires its supplied row choices. No randomness or homophone probability is inferred.

Plaintext normalizes ASCII case, removes spacing and punctuation, rejects digits and non-ASCII characters, and merges J into I. Ciphertext is a whitespace-separated sequence of two-digit ASCII codes; a final display period requires `terminal_period=True`. The source permits retaining word divisions, but this interface treats code grouping as display layout and returns normalized letters. `SolveResult` explicitly reports lost word spaces and merged letters. A punctuation mark is not encrypted by the 25-letter table.

Aligned-crib inference is a separate bounded API requiring at least one `engine.reverse_engineer.Crib`. Offsets count zero-based normalized plaintext letters, one per code token. Each numeric code identifies its row. That row has only 25 possible keyword shifts, so the tool tests 25 shifts per row against all aligned evidence, up to 100 checks total. Independent row option counts multiply to an exact compatible-key count without enumerating up to `25**4` full keywords.

If no crib observes a row, every shift for that row remains possible. The report retains `?` key slots and `?` plaintext positions instead of filling them with a plausible letter. The completed first-three-letter control gives `GO??` with 625 compatible keywords. An incompatible completed model returns count zero. A check budget below completion returns `check_limit`, no key prediction, no plaintext prediction and no exact count. Duplicate consistent crib positions count once; contradictory overlaps, out-of-range coordinates and empty evidence fail. `claimed_plaintext` always remains null: these implications require the four-row family and crib assumptions.

Known-key limits are 4,096 letters/codes and 16,384 raw input characters. Inference accepts at most 512 codes and 128 cribs, with an integer `max_checks` in 0 through 100. All transformations and search use the standard library. Completion is not a historical verification or general homophonic attack.

The [certificate](../engine/data/homophonic_certificate.json) separates the supplied-key published example from the conditional first-five-letter crib control. The latter receives no keyword and predicts the remaining seventeen letters. Tests first failed on the missing module, then checked literal numeric rows and codes, an independent rotation oracle, code 00, I/J loss, unknown rows, budgets, incompatible cribs, malformed tokens and actual recovered hashes.

```sh
.venv/bin/python -m unittest tests.test_homophonic -v
```
