# Bounded transposition portfolio

`engine.transposition_ensemble` connects the existing rail-fence, route,
columnar and Redefence transforms under one budget and one candidate format.
This is a repository-specific composition, with no claim of historical
algorithm novelty or a new historical decipherment.

```python
from engine.transposition_ensemble import search_transposition_ensemble
from engine.reverse_engineer import Crib

report = search_transposition_ensemble(ciphertext, max_candidates=20,
    max_checks=5000, max_width=8, max_rails=5, cribs=(Crib(0, "KNOWN"),))
payload = report.to_dict()
```

No key is supplied. The portfolio tries:

- Rail-fence rail counts 2 through `max_rails`.
- The existing clockwise inward route from the top right, with row or column
  fill, at every allowed width that divides the letter count.
- The existing right-to-left columnar transform, singly and as ordered pairs
  of dividing widths. This is not an arbitrary keyed-columnar search.
- Every [Redefence](redefence.md) row-rank permutation and cyclic offset for
  3 through `max_rails` rails.

Families receive checks round-robin, so one family cannot consume the entire
initial budget. A check consists of decryption and a separate call to its
existing forward transform. A mismatch is rejected and counted. Supplied cribs
then filter candidates in zero-based normalized plaintext coordinates. Duplicate
or overlapping consistent cribs do not create additional confirmed positions;
contradictory or out-of-range cribs fail validation.

The remaining plaintexts share the existing English score and are deduplicated
by plaintext SHA-256. Full plaintext strings are retained only for the bounded
top candidate set. Each candidate contains `family`, a structured `key`,
`plaintext`, `score`, and `re_encryption_matches`. It also records up to eight
equivalent family/key examples and the number observed. The first encountered
representation is a representative, not an identified cipher family. Alternate
keys can yield the same text.

Reports include `checks`, `total_checks`, per-family counts, rejected cribs,
forward mismatches, duplicates, all bounds, and `search_complete`. Completion
means all requested models were tested; `stop_reason: check_limit` means some
remain. An empty completed candidate set means these models did not match the
supplied constraints. Retaining fewer candidates is separate from completing
the search. `claimed_plaintext` stays null and `uniqueness` remains
`not_established`, even when there is one retained text. English rank and
reencryption establish neither linguistic correctness nor independent
historical evidence.

Input is 4 through 1,024 normalized A-Z letters, at most 4,096 raw characters;
non-ASCII alphabetic input is rejected. Bounds are 1 through 100 retained
candidates, 0 through 100,000 checks, width 2 through 32, and maximum rails
3 through 7. Default widths stop at 8 and rails at 5. No padding, null removal,
word segmentation, or other route is invented. Work is bounded by these sizes
and check counts; the API has no wall-clock deadline.

Tests recover a literal harbor-prose Redefence fixture without a supplied key
or plaintext, check existing rail and route examples with cribs but no keys,
and include the existing published K3 control when `max_width=28` and a
`SLOWLY` crib are explicitly requested. They also cover exact budgets, zero
checks, deduplication, capped key examples, malformed constraints, and an
injected broken inverse rejected by the forward check. The
[certificate](../engine/data/transposition_ensemble_certificate.json) hashes the
actual blind harbor candidate. It uses `tool_name`, since a portfolio is not a
new cipher class for the neural router.

```sh
.venv/bin/python -m unittest tests.test_transposition_ensemble -v
```
