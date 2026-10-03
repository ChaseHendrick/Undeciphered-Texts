# Bounded cipher investigation

`engine.solver_reasoning` turns existing cipher tools into a bounded investigation
with a factual ledger. Its objective is to **seek independently verifiable
solutions to unresolved ciphers**. Candidate generation, falsifiable constraints,
and a separate `verify_case` stage make that objective operational. It makes no
claim of historical algorithm novelty, a solved unknown script, or a solution to
army message Nr. 86.

```python
from engine.reverse_engineer import Crib
from engine.solver_reasoning import investigate_cipher

report = investigate_cipher("LXFOPVEFRNHR", cribs=(Crib(0, "ATTACK"),),
                            max_checks=5000, max_candidates=20)
payload = report.to_dict()
```

This control infers a Vigenere `LEMON` candidate and predicts `ATTACKATDAWN`.
The supplied crib constrains the model. The suffix remains a conditional
prediction until a separate reference checks it. `claimed_plaintext` stays null,
`solved_status` stays `unverified`, `correctness_known` stays false, and
`happiness` stays null in every investigation report.

For Latin input, the planner tries all 312 invertible affine keys, including
the 26 Caesar shifts. When aligned cribs and enough budget exist, it instead
calls the existing [model inference](reverse-engineering.md) for affine,
substitution, and repeating Vigenere or Beaufort periods through the smaller
of 16 and the text length. It reserves exactly `313 + 2 * tested_periods`
checks for those models before calling them. It passes only the remaining
global budget to the [transposition portfolio](transposition-ensemble.md).
With too little budget for model inference, the report records that omission
and remains incomplete. Partial mappings and key slots remain unknown in the
separate, bounded `hypotheses` list; they are not filled with guessed letters.
Vigenere and Beaufort without aligned cribs are outside this tool's search
scope. Arbitrary substitution, keyed columnar permutations, null removal, and
other route patterns are also outside it.

The existing neural router supplies real, model-derived family probabilities
when NumPy and its weights are usable and the input has at least 16 Latin
letters. Its status and artifact hash appear in `neural_advice`. Missing NumPy,
weights, or valid router data produces an explicit fallback with an empty
probability list. No synthetic probabilities are substituted. Neural advice
does not remove other models or change constraints. Complete candidates share
the existing English quadgram score; family probability breaks score ties.
Neither quantity is a probability that a plaintext is correct. Each family
retains at most `max_candidates` candidates before the global top list is
bounded to that same limit.

Numeric input invokes [Morse constraints](morse-constraints.md) only when the
caller provides a lexicon or aligned decoded-text cribs. Maps are tested without
a supplied key. A zero digit excludes Morbit according to its digit alphabet.
Numeric cribs use zero-based uppercase decoded characters **including recovered
word spaces and punctuation**. Latin cribs use zero-based A-Z plaintext letters
after removing spaces and punctuation. These coordinate systems appear in the
report and are never silently interchanged. For example:

```python
report = investigate_cipher("0", lexicon=("E",), max_checks=6)
```

The small control produces an `E` Pollux witness and records an incomplete map
search. It does not identify a unique map or verify a real message. Numeric
text accepts whitespace and one optional final framing period. Mixed letters
and digits require a cipher-specific framing model and are rejected here.
Latin lexicons are validated but are not used as evidence by the current letter
families; this omission is recorded explicitly.

A global check is one tested key or model setting, with the applicable forward
transform comparison. Caesar and affine candidates, complete crib-inference
predictions, and transposition candidates must re-encrypt to the normalized
ciphertext. Morbit re-encryption must match its digits; Pollux checks the
original digit choices against its inferred map. A mismatch rejects the
candidate and adds a contradiction. Forward consistency proves only that a
transform reproduces the ciphertext. It is separate from independent correctness.
Neural feature evaluation is advisory overhead, measured by `elapsed_seconds`,
and is not a cryptanalytic key check.

`premises`, `actions`, `results`, `contradictions`, and `next_actions` are generated
from actual inputs and program outcomes. Overlapping incompatible cribs produce
a `constraint_conflict` report with no search. A completed empty candidate set
means the stated models fail the supplied constraints, with untested models
still possible. It does not make the unresolved cipher a wrong answer. Plans
call for reviewing constraints, extending exhausted bounds, considering other
models, and seeking independent keys, archival plaintext, or held-out evidence.

The `thought` field is a program-generated plan summary. `simulated_affect`
exposes display-only curiosity, caution, and frustration states, explicitly
without literal feelings or sentience. `balanced`, `curious`, and `cautious`
temperaments change this telemetry only. Search order, budgets, candidate
evidence, consistency checks, and correctness criteria remain identical.

Two pure helpers support independent evaluation by a caller:

```python
from engine.solver_reasoning import score_reward, evaluation_policy

score_reward(correct=20, total=20, checks=2000, budget=5000)  # 0.96
evaluation_policy(correct=14, total=20)  # recommends retire_or_demote
```

`score_reward` returns null for no independent cases, zero for any checked
error, and a reward from 0.9 to 1 only when all supplied independent cases pass.
Efficiency is a secondary tie-breaker, so a fast incorrect result never outranks
a slower correct one. The caller must supply actual independent evaluation
counts, not candidate scores or crib matches. The investigation itself has no
such reference and earns no verified reward.

The explicit default evaluation policy needs at least 20 independently checked
cases, requires accuracy of at least 0.8, and recommends retirement or demotion
at five checked failures or below the accuracy threshold. Its thresholds are
configurable repository policy, not a calibrated statistical guarantee.
Eligibility remains null below the minimum count. No model is removed by this
helper; it emits a reviewable recommendation. Rejected cipher models and
incomplete searches never supply its error counts.

Input is bounded to 4 through 512 Latin letters or 1 through 512 digits, at most
4,096 raw characters. Non-ASCII alphanumeric input is rejected. The API accepts
0 through 100,000 checks, 1 through 100 retained candidates, at most 128 cribs,
and 1 through 10,000 lexicon entries when provided. Transposition defaults stop
at width 8 and five rails. Numeric map enumeration also stops after five seconds
and records time exhaustion. Latin work is bounded by input sizes and check
counts, with no wall-clock deadline. Search completion refers to the explicitly
stated finite models and supplied evidence, never every possible cipher.

Tests first failed on the absent module, then recovered independent literal
Caesar, affine, and Redefence controls without supplied keys or plaintext.
They also cover crib-based prediction beyond a crib, one global budget, numeric
evidence and space coordinates, contradictory premises, failed models, missing
NumPy fallback, actual router advice when available, temperament invariance,
rejected forward mismatches, and independent reward and retirement semantics.
The [certificate](../engine/data/solver_reasoning_certificate.json) hashes the
actual top recovered Caesar control. It uses `tool_name`, since this composition
is not a new cipher family for neural training.

```sh
.venv/bin/python -m unittest tests.test_solver_reasoning -v
```
