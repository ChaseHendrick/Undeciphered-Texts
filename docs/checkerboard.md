# Supplied-square Checkerboard

`engine/solvers/checkerboard.py` follows the [ACA Checkerboard sheet](https://www.cryptogram.org/downloads/aca.info/ciphers/Checkerboard.pdf), printed page 39, fetched and visually inspected on 2026-10-03. A letter is the row coordinate followed by the column coordinate of a supplied 5 by 5 square. This differs from [straddling checkerboard](straddling-checkerboard.md), which uses variable-length digit codes.

The printed square, in row-major order, is `KNIGHPQRSTOYZUAMXWVBLFEDC`. The simple labels are BLACK down the rows and WHITE across the columns. The complex example also supplies HORSE down the rows and GRAYS across the columns; either label set on each axis provides valid coordinate homophones. Both literal ciphertexts recover `NUMBERSCANALSOBEUSEDASCOORDINATES`.

```python
from engine.solvers.checkerboard import checkerboard_decrypt

plain = checkerboard_decrypt(
    "BH AT CW CE KI LI LT KE AE BH AE KW LT AW CE KI AT LT KI KT AE LT "
    "KE AW AW LI KT BI BH AE LE KI LT.",
    square="KNIGHPQRSTOYZUAMXWVBLFEDC",
    row_labels=("BLACK",), column_labels=("WHITE",), terminal_period=True)
```

`checkerboard_encrypt`, `checkerboard_decrypt` and `solve_checkerboard` require the complete square and labels. The square must contain every 25-letter I/J-merged cell exactly once; the helper does not infer a keyword or construction route from the source diagram. Each axis accepts a finite sequence of one or two five-character label strings, using ASCII letters or digits. Labels on the same axis must be distinct across both strings so code parsing remains unambiguous. Characters on different axes may overlap because row and column positions are explicit.

Encryption uses the first row and column label sets by default. Its optional `choices` supplies one pair of zero-based label-set indices per normalized plaintext letter. Replaying the complex worksheet's different homophones requires those choices. Different choices decrypt to the same plaintext; they do not add a different square or a new cipher family.

Plaintext normalizes to uppercase ASCII letters, removes ASCII spacing and punctuation, rejects digits and non-ASCII input, and merges J into I. Grouped ciphertext uses pairs of ASCII coordinate characters. Whitespace grouping does not retain word divisions. A final printed period requires explicit `terminal_period=True`; other punctuation and incomplete or wrongly ordered coordinates fail. `SolveResult` reports supplied-key mode, merged letters and lost word spaces.

Limits are 4,096 plaintext letters, 16,384 raw plaintext/square characters, and 32,768 raw ciphertext characters with at most 4,096 complete pairs. Transformations are finite linear passes with the standard library. There is no unknown-square search or carrier detection.

The [certificate](../engine/data/checkerboard_certificate.json) stores both independently printed examples and hashes actual recovered normalized letters. Tests first failed on the absent module, then checked both vectors, every square cell under all four complex label choices, numeric coordinates, I/J loss, framing, malformed labels, strict bounds and recovered-output hashes.

```sh
.venv/bin/python -m unittest tests.test_checkerboard -v
```
