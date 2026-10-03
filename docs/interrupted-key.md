# Interrupted Key

The [ACA worksheet](https://www.cryptogram.org/downloads/aca.info/ciphers/InterruptedKey.pdf)
restarts a keyword at each interruption and requires the entire keyword to be
used at least once. Its example uses Vigenere. This module implements that
tableau with explicit interruption lengths. Other periodic tableaux and unknown
interruption patterns are outside its scope.

```python
from engine.solvers.interrupted_key import interrupted_key_decrypt

runs = (4, 6, 2, 3, 4, 3, 1, 1, 5, 1, 2, 3, 5)
plain = interrupted_key_decrypt(
    "HYIFQ ZPUKV QRBSE IJEQK ZTVOB POSZ VSGSI ICUIP Y.",
    "ORANGE", segment_lengths=runs)
```

This matches the literal published plaintext `THISCIPHERCANBEUSEDWITHANYOFTHEPERIODICS`.
The runs come from the worksheet's printed key-stream diagram, not ciphertext
group sizes. A keyword cycles normally inside a longer run, and restarts at the
next boundary. Repeated keyword letters are retained. `solve_interrupted_key`
labels this mode `supplied_key_and_reset_pattern`.

Unknown-key inference uses aligned plaintext equations instead of dictionary
ranking or plaintext lookup:

```python
from engine.reverse_engineer import Crib
from engine.solvers.interrupted_key import infer_interrupted_key

report = infer_interrupted_key(
    "HYIFQZPUKVQRBSEIJEQKZTVOBPOSZVSGSIICUIPY",
    segment_lengths=runs, keyword_length=6,
    cribs=(Crib(4, "CIPHER"),), max_checks=4096)
payload = report.to_dict()
```

The six-letter crib determines the unknown keyword `ORANGE` and predicts the
other 34 letters. The published reference independently checks that control.
The inference API receives no keyword or expected plaintext. It does receive
the reset pattern and keyword length as model constraints. If `keyword_length`
is omitted, it explicitly assumes the longest supplied run uses the whole
keyword exactly once, and records that assumption. Supply the length explicitly
when a run contains multiple keyword cycles. It does not infer every possible
length or reset arrangement.

One check is one distinct known-position equation. Duplicate consistent cribs
do not inflate the count. Contradictory overlapping plaintext cribs fail input
validation. Different positions requiring incompatible values in the same key
slot reject the model and appear in `contradictions`. Unobserved slots remain
`?`, and conditional predicted plaintext retains `?` at affected positions.
`compatible` is null when the equation budget expires before all constraints
are checked, unless a checked contradiction already rejects the model.

`search_complete` means every supplied crib equation was checked within this
fixed model. It does not mean all interruption schemes were tested. A complete
keyword is re-encrypted and `unique_key_within_pattern` applies only to the
supplied pattern and length. Crib fit and re-encryption do not independently
verify a real historical cipher; `claimed_plaintext` always remains null.

Bounds are 1 through 4,096 normalized A-Z text letters, at most 16,384 raw
characters, keywords of 1 through 64 ASCII letters, 1 through 4,096 positive
run lengths that exactly partition the text, and 1 through 128 aligned cribs.
Runs must collectively use the whole keyword in at least one uninterrupted
segment. Offsets use zero-based normalized plaintext letters. Digits and
non-ASCII alphanumeric input are rejected. Inference accepts 0 through 4,096
checks. Its work is bounded by these sizes and equation counts; it has no
wall-clock deadline.

Tests first failed on the absent module. They cover the literal published key
diagram and vector, an independent arithmetic oracle with repeated letters
and longer runs, unknown-key recovery beyond a crib, partial slots, exact and
zero budgets, conflicting equations, malformed parameters, and the
[certificate](../engine/data/interrupted_key_certificate.json) hash of actual
recovered output. This is a published solved control, not a newly solved
historical message or a novelty claim.

```sh
.venv/bin/python -m unittest tests.test_interrupted_key -v
```
