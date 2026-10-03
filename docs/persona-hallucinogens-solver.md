# Hallucinogens composition search

`investigate_hallucinogens` implements a bounded creative search policy inside
the existing engine. It tries alternate ciphertext orderings before exhaustive
affine inversion. The persona expands hypotheses; it does not intentionally
produce false answers or change the proof requirements. This is a
repository-specific composition, with no historical novelty claim.

```python
from engine.reverse_engineer import Crib
from engine.solvers.persona_hallucinogens import investigate_hallucinogens

report = investigate_hallucinogens(ciphertext, cribs=(Crib(0, "KNOWN"),),
    max_checks=5000, max_candidates=20, max_rotations=8)
```

The existing `choose` and `covers` APIs still implement their documented
[word preferences](persona-preferences.md). Their words and behavior are
unchanged. They are separate from the new cipher search and supply no evidence
to its candidates.

## Exact models and bounds

The search tries identity, complete reversal, and left cyclic rotations with
offsets 1 through `min(max_rotations, letter_count - 1)`. For every permutation it
tests all 312 invertible affine keys. The arithmetic comes from the existing
[checked affine helper](../engine/solvers/affine.py) and [affine documentation](affine.md).
The portfolio shares the bounded-composition approach documented in
[the transposition ensemble](transposition-ensemble.md).

Each key is interleaved across all permutations before moving to the next key,
so an early budget gives every permutation a turn. One affine/permutation pair
costs one global check, including rejected trials. Completion means the entire
requested finite set was tested. Candidate retention never ends the search.
Default settings request ten permutations and 3,120 checks. With rotations
disabled, identity and reversal request 624. Fewer than nine letters reduce the
default distinct rotation offsets.

Input uses the shared persona bounds: 4 through 512 normalized A-Z letters and
at most 4,096 raw characters, with non-letter alphanumeric input rejected.
Whitespace and punctuation are removed before coordinates are assigned. Limits
are 0 through 100,000 checks, 1 through 100 retained candidates, 0 through 64
rotation offsets and at most 128 shared typed cribs. Duplicate or consistent
overlapping cribs do not create additional known positions. Contradictory or
out-of-range cribs fail validation. The maximum requested model set is 20,592
checks. The API has no wall-clock deadline.

For a permutation T, a candidate must satisfy:

```text
plaintext = affine_inverse(T(original_ciphertext))
original_ciphertext = inverse_T(affine(plaintext))
```

The separate forward replay must reproduce the original normalized cipher
string exactly. A left rotation is undone by a right rotation with the same
offset; reversal undoes itself. No plaintext letters are inserted or deleted.
Cribs constrain original normalized plaintext coordinates, regardless of which
ciphertext permutation is tested.

## Candidate and report meaning

Each JSON candidate has `plaintext`, `family: composed_affine`, a structured
`key` containing `transform` and `affine`, `score`, `forward_consistent`,
`crib_match`, `status` and a factual `evidence` plan. Plaintexts are deduplicated;
each retained text records up to four equivalent composition keys and the
number observed. These witnesses are alternate descriptions of the same text,
not additional independent evidence. All seen plaintexts are tracked within the
finite input and model bounds; only the best candidate objects are retained.

The existing English score ranks eligible candidates, with plaintext as a
deterministic tie-break. It is not a probability or proof of correctness.
Reports include per-permutation checks, rejections, mismatches, effective
rotation offsets, retention truncation and explicit search completion. A
completed empty result rejects only the requested models under the supplied
constraints. A check-limit stop leaves untested models in that finite set.

`claimed_plaintext` and `happiness` remain null, `correctness_known` stays false,
and `solved_status` remains unverified. The program-generated thought field
summarizes performed work. Personality and thought labels do not imply
consciousness, and the finite candidate count does not establish historical
uniqueness. Supplied cribs remain separate from independent validation.

## Controls actually tested

The new regression first failed because `investigate_hallucinogens` did not
exist. Tests then recover two literal constructed controls, affine encryption
followed by reversal or right rotation by three, without supplying their keys.
Independent test arithmetic verifies every returned composition against the
original ciphertext. A plain affine-only control cannot recover the reversed
fixture, and disabling rotations fails the aligned-crib rotation control.
Tests also cover budgets, fair interleaving, fixed crib coordinates, equivalent
witness limits, malformed input, forward-replay failure and legacy preferences.

The [certificate](../engine/data/persona_hallucinogens_solver_certificate.json)
hashes the actual top recovered reversed-affine candidate, found in all 624
requested checks with no key or cribs supplied. The complete normalized fixture
string is absent from the existing English scoring corpus. This small
constructed control verifies composition recovery and report behavior; it does
not establish general language accuracy or a historical solve.

```sh
.venv/bin/python -m unittest tests.test_persona_hallucinogens_solver tests.test_persona_preferences
```

13 tests passed, including nine new solver controls and four legacy preference
checks.
