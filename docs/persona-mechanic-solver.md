# Mechanic algebra and recurrence investigator

`investigate_mechanic` tests algebraic cipher assumptions against aligned caller
cribs. Its role connects [Progressive Key inference](progressive-key.md),
[plaintext-autokey propagation](autokey-inference.md), and
[Hill matrix inference](hill-inference.md). No selected keyword, primer,
progression or matrix is supplied. There are no default clues.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_mechanic import investigate_mechanic
report = investigate_mechanic(ciphertext, cribs=(Crib(0, "THECLO"),))
```

One budget is allocated across the applicable branches. Each branch receives
a share of remaining work; unused checks are passed to subsequent branches.
Progressive Key tests periods through 16 and all 26 progression values.
Autokey tests primer lengths through 32, capped at message length.
Hill tests the unknown invertible 2x2 matrix on complete two-letter blocks.
Odd ciphertext length makes Hill explicitly inapplicable; no padding letter is
invented. Reports disclose each allocation, executed count, check unit and
completion state. These heterogeneous units bound stated operations, not time.

For Progressive Key, a known letter implies a key slot after subtracting its
block progression. Unseen slots and their plaintext positions remain `?`.
For plaintext autokey, each residue column obeys
`P[i] + P[i-L] = C[i] (mod 26)` after the primer. A crib fixes the column seed
exactly; contradictory seeds reject that period. Unconstrained columns remain
unknown. Only fully determined models become complete plaintext candidates.
English ranking never supplies missing letters.

The Hill branch reuses its inverse-row and compatible-row-pair enumeration and
forward replay. It can retain consistent examples from an incomplete search;
such examples are labeled accordingly. Its global compatible-key count and
consensus stay null until the declared matrix search completes. Mechanic does
not promote branch-specific predictions into agreement across all model classes.

The shared candidate schema contains plaintext, family, key, summed repository
quadgram score, forward consistency, crib fit and evidence. Scores and supplied
constraints are not independent correctness evidence. `hypotheses` preserves
partial predictions, with explicit truncation counts. Complete `branch_reports`
retain bounded diagnostic outputs for further inspection. `claimed_plaintext`
is always null. With no aligned cribs the method performs zero checks and
returns `requires_aligned_cribs`; it does not fabricate a reading.

Input bounds are 4 through 512 normalized ASCII letters, 4,096 raw characters,
128 typed cribs, 0 through 100,000 checks and 1 through 100 retained candidates.
Defaults are 5,000 checks and 20 candidates. Crib positions refer to normalized
plaintext letters and overlaps must agree. The standard library is sufficient;
neural advice is explicitly `not_used`. Optional NumPy or symbolic packages
are unnecessary for these branches.

The [certificate](../engine/data/persona_mechanic_solver_certificate.json)
contains original literal controls encrypted independently before the module
existed. Progressive Key, plaintext autokey and Hill controls predict unprovided
suffixes without their selected keys. Tests verify strict shared budgets,
incomplete scopes, unknown columns, odd-block handling and every two-letter
autokey primer for a small forced-letter control. Hashes cover actual recovered
ASCII plaintext. This portfolio is a repository composition of established
methods, not a new cipher algorithm or an unsolved historical decipherment.
