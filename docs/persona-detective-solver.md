# Detective unknown-offset crib investigator

`investigate_detective` searches for a supplied plaintext crib whose location
is unknown. It tests ordinary straight-alphabet Vigenere periods, using the
[existing crib solver's equations](../engine/solvers/crib.py). It has no default
crib or keyword. The role changes search policy, not evidence or neural identity.

```python
from engine.solvers.persona_detective import investigate_detective
report = investigate_detective(ciphertext, crib="LETTER BESIDE")
```

For alignment `s`, each crib letter implies shift
`K[(s+i) mod L] = C[s+i] - P[i] (mod 26)` for period `L`.
All repeated assignments must agree, every key slot must be filled, and at
least `min_checks` later crib letters must confirm an earlier assignment.
These confirmations establish internal consistency; they are not independent
evidence. A filled key decrypts the whole stream and is checked by forward
replay. Positions outside the crib are conditional model predictions.

`min_checks`, default 2, counts repeated key-slot confirmations.
Report `checks` has a different unit: one alignment/period trial, including
any applicable forward comparison. One global budget stops work exactly.
`max_checks` accepts 0 through 100,000, default 5,000, and `max_candidates`
accepts 1 through 100, default 20. Ranked retention does not stop searching.
Eligible periods are bounded by `max_period` and crib length minus the required
confirmations. `max_period` accepts 1 through 128, default 16;
`min_checks` accepts 1 through 512. No eligible period gives a complete empty
search within that policy. Exhausted prefixes remain incomplete.

Ciphertext must contain 4 through 512 normalized ASCII letters, with at most
4,096 raw characters. The crib must contain at least two normalized letters
and fit the message. Spaces and punctuation are removed. Digits and non-ASCII
alphanumeric symbols are rejected. Keys are indexed from normalized message
position zero, even when the crib starts in the middle of a key cycle.

Candidate evidence records the inferred offset, period, keyword and confirmation
count. Summed repository English quadgrams rank examples; a solitary or leading
match does not prove uniqueness or historical correctness. The method uses
the standard library and explicitly records neural advice as `not_used`.
Runtime `claimed_plaintext` remains null and correctness remains unknown.

The [certificate](../engine/data/persona_detective_solver_certificate.json)
contains an original synthetic literal encrypted with separate modular
arithmetic before the module existed. Providing only twelve crib letters
recovers an unknown offset of 27 and a six-letter key, predicting the remaining
105-letter message after 940 trials. Tests also enumerate every actual
one-letter and two-letter key for a small control and compare all matching
offsets against the bounded search. Hashes cover actual recovered ASCII bytes.
This is a composition of established crib reasoning, not a new cryptographic
algorithm or a historical decipherment claim.
