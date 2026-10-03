# Hill matrix inference from aligned letters

`infer_hill` recovers compatible 2x2 Hill matrices from ciphertext and caller
supplied plaintext cribs. The encryption matrix is not an input. It uses
column vectors with A=0 through Z=25. Slinko's published example gives
`K = [[3, 3], [2, 5]]`, inverse `[[15, 17], [20, 9]]`, and `HELP -> HIAT`.
The matrix rule and vector appear on physical PDF pages 22 through 25 of
[Algebra for Cryptology, University of Auckland](https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf).

```python
from engine.reverse_engineer import Crib
from engine.solvers.hill_inference import infer_hill

report = infer_hill("HIAT", cribs=(Crib(0, "HELP"),))
```

For inverse matrix `D`, an aligned plaintext letter imposes one congruence:
`P[2i+r] = D[r,0]*C[2i] + D[r,1]*C[2i+1] (mod 26)`.
The method tests all 676 coefficient pairs separately for each inverse row.
It then tests every pair of compatible rows, retaining only determinants
coprime to 26. Inverting the surviving matrix recovers the encryption key.
Every accepted key decrypts all complete ciphertext blocks, satisfies all
supplied letters, and passes forward replay. Cribs may start or end halfway
through a block; the method constrains only the letters actually supplied.

One `max_checks` budget covers every inverse-row trial and every compatible-row
pair trial, including applicable forward checks. The default and maximum is
100,000. Row enumeration takes 1,352 checks; subsequent pair count depends on
the evidence. Uninformative cribs can leave 456,976 pairs, so even the maximum
budget need not complete the declared search. The implementation counts
trials exactly, stops at the requested budget, and retains at most
`max_candidates` ranked key examples. English quadgrams determine ordering,
with matrix order breaking score ties. Scores are not correctness evidence.

`compatible_keys_seen` counts accepted tested keys. `compatible_key_count`,
`consensus_plaintext`, `key_unique_within_model` and
`plaintext_unique_within_model` are populated only after both row enumerations
and every compatible row pair finish without transformation inconsistencies.
Incomplete searches return null for those global conclusions. Consensus
includes all accepted keys, including examples removed from the ranked output.
Unknown consensus positions remain `?`. The distinct
`supplied_plaintext_positions` field records premises without treating them as
inferred facts. An empty completed search returns zero compatible keys and no
plaintext consensus, scoped to this model and the supplied cribs.

Inputs contain an even 4 through 512 normalized ASCII letters, with at most
4,096 raw characters. Formatting is removed; digits and non-ASCII alphanumeric
symbols are rejected. At least one and at most 128 typed `Crib` objects are
required. Offsets use zero-based normalized plaintext positions. Cribs must fit
the input and overlapping letters must agree. `max_candidates` is an integer
in 1 through 100, default 20; `max_checks` accepts 0 through 100,000. Missing
ciphertext pair letters are rejected. No padding is added or removed, so a
recovered terminal X remains visible. The method uses the standard library.

The [certificate](../engine/data/hill_inference_certificate.json) records the
downloaded source hash, the published vector recovered from its plaintext crib,
and an original 28-letter synthetic vector whose seven-letter crib begins at
offset 1. The latter predicts its remaining suffix without a supplied matrix
and keeps its terminal X. Hashes cover actual recovered ASCII bytes. Tests
also enumerate all 456,976 encryption matrices independently for a sparse
two-letter crib: 157 compatible keys yield consensus `?EL?`, even with only
two examples retained. Budget controls prevent incomplete prefixes from
asserting those conclusions. These are conditional classical cipher controls;
no historical decipherment, Nr. 86 solve or unknown-script reading is claimed.
Runtime `claimed_plaintext` remains null.
