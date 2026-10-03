# Emperor systematic cipher investigation

`investigate_emperor` performs a real bounded search on ciphertext. Its persona
selects a systematic search policy; it does not provide plaintext evidence or
create a separate neural network. The older `choose` and `covers` functions
remain court-notice sentence preferences. Their word list never filters the
investigation's recovered candidates.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_court_notice import investigate_emperor

report = investigate_emperor("LXFOPVEFRNHR", cribs=(Crib(0, "ATTACK"),))
```

The wrapper calls [the existing investigation engine](solver-reasoning.md)
once. With enough budget and aligned cribs, that engine fits affine,
substitution, Vigenere and Beaufort models. Otherwise it enumerates invertible
affine keys, including Caesar shifts. The finite rail-fence, route, columnar
and Redefence portfolio receives the remaining check budget. Every retained
complete candidate has passed a forward transform and the supplied cribs.
English quadgrams rank candidates, with available neural family advice used
as a secondary signal. These checks establish consistency within a tested
model, not independent correctness or a historical decipherment.

The result is a JSON-serializable dictionary with normalized candidate fields,
the exact underlying `ledger`, tested `actions`, `checks`, `search_complete`,
`stop_reason`, `bounds`, `contradictions` and `next_actions`. Partial models are
retained in `hypotheses` and `conditional_predictions`, including unknown
positions. `neural_advice` preserves the actual router status. Missing NumPy
or model data produces explicit unavailable advice and no invented confidence;
the cipher searches continue. Neural feature computation is advisory overhead
outside the cryptanalytic check count, as disclosed in the ledger.

Ciphertext contains 4 through 512 ASCII letters after formatting is removed,
with at most 4,096 raw characters. Digits and non-ASCII alphanumeric symbols
are rejected. Crib offsets refer to normalized A-Z plaintext positions. At most
128 typed `Crib` objects are accepted; contradictory overlaps are invalid.
`max_checks` is an integer in 0 through 100,000, default 5,000;
`max_candidates` is in 1 through 100, default 20. The wrapper introduces no
extra search passes. Exhausted budgets remain incomplete. Even a complete
search covers only the finite model portfolio stated in its bounds.

The [certificate](../engine/data/persona_emperor_solver_certificate.json)
contains two original synthetic literal controls, frozen before the wrapper
existed. Blind Caesar and three-row rail-fence controls recover the same
105-letter paragraph without supplied keys or cribs. The rail-fence control
also admits an ordered Redefence representation, so it does not prove a unique
family. A separate aligned-crib control predicts the unprovided suffix
`ATDAWN` while preserving other incomplete hypotheses. Hashes are computed from
actual recovered ASCII plaintext. No Nr. 86, K4 or unknown-script solution is
claimed. Runtime reports keep `claimed_plaintext` null and correctness unknown.
