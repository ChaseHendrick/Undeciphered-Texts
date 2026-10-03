# Enigma starting-position search

`engine.solvers.enigma_crib_search` searches unknown three-letter starts using
the existing [three-rotor Enigma machine](enigma.md). Rotor order, rings,
reflector and plugboard are supplied settings, with explicit documented defaults.
Their values are not recovered. This repository composition makes no claim of
a general Enigma break, a new historical decipherment, or work on army message
Nr. 86.

[Crypto Museum's machine explanation](https://www.cryptomuseum.com/crypto/enigma/working.htm)
describes stepping before each keypress, the middle-rotor double-step, and the
reciprocal reflector. Its [wiring reference](https://www.cryptomuseum.com/crypto/enigma/wiring.htm)
publishes the rotor and reflector tables used by the existing engine and the
independent test oracle.

```python
from engine.reverse_engineer import Crib
from engine.solvers.enigma_crib_search import search_enigma_starts

report = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),),
    rotors=("I", "II", "III"), reflector="B", rings="AAA", plugboard=(),
    max_checks=17576, max_candidates=20)
payload = report.to_dict()
```

This replays the repo's existing published `AAAAA` / `BDZGO` control while
receiving no starting position. The search tests starts from `AAA` through
`ZZZ`, checks aligned cribs first, then decrypts and re-encrypts a complete
candidate before accepting it. Candidates use lexicographic start order and
a zero score. English plausibility and neural probability are not used to
declare a correct key.

Literal `?` and `-` each record exactly one missing ciphertext letter. Whitespace
separates groups and does not consume a step. Every missing letter advances the
machine, including notch carries and double-steps, and produces `?` in the
conditional plaintext. The tool does not guess its value or an unknown gap
length. Other punctuation is rejected so it cannot silently change alignment.

```python
report = search_enigma_starts("BD?GO",
    cribs=(Crib(0, "AA"), Crib(3, "AA")))
# The AAA witness predicts AA?AA, preserving the missing slot.
```

Crib offsets count normalized plaintext slots **including missing letters**.
A crib touching a missing ciphertext slot is rejected unless the caller
explicitly sets `skip_missing=True`. That setting ignores the affected crib
positions and reports how many were skipped; it still leaves `?` in the output.
At least one crib position must constrain a known ciphertext letter. Conflicting
overlapping known positions fail validation. Equal plaintext and ciphertext
letters analytically exclude the supplied reflector model, recorded as
`self_encryption` with no start trials.

One `check` is an initiated start trial. `checked_starts` excludes an unfinished
trial if the work budget expires. `letter_steps` counts every machine-slot
advance in crib checking, candidate decoding and forward replay, including gaps.
Cribs can reject a start early, so the search does not decrypt a long message
for every rejected start. It reserves both complete replays before creating
a candidate. Both budgets are strict: 0 through 17,576 starts and 0 through
1,000,000 slot steps. The latter default can stop a search with a late crib
before all starts are tested. `stop_reason`, `incomplete_start`, bounds and
elapsed time make that exhaustion visible. There is no wall-clock deadline.

The retained candidate limit is 1 through 100 and does not stop enumeration.
`accepted_start_count` counts all validated starts, even after storage fills.
Two accepted starts establish start ambiguity immediately. A single stored
candidate does not establish uniqueness when other starts remain or storage
was truncated. `unique_start_within_settings` requires a completed search and
exactly one accepted start. `unique_plaintext_within_settings` is scoped to
the supplied settings and cribs, including preserved unknown slots. Different
starts can have the same plaintext. These are conditional model properties;
`claimed_plaintext` always remains null. Re-encryption is transform consistency,
with independent correctness and historical attribution left to a separate
reference check.

Input is 1 through 512 normalized slots, at most 2,048 raw characters, with at
least one known ciphertext letter. Settings require three distinct rotors
from I through V, wide reflector B or C, three ASCII ring letters, and at most
13 disjoint plugboard pairs. The adapter validates strict types before reusing
the existing machine's configuration parser. Cribs are a finite list or tuple
of 1 through 128 shared `Crib` objects. Word separators in crib text are removed;
punctuation, digits and unsupported alphabets are rejected.

Tests first failed on the absent module. They replay the published control
without a supplied start, verify an independent arithmetic oracle using
nondefault settings, preserve gaps across a double-step, reject unsafe crib
alignment, account for both budgets, distinguish storage from uniqueness,
and reject an injected failed forward replay. The
[certificate](../engine/data/enigma_crib_search_certificate.json) uses a literal
constructed gapped fixture from that independent oracle. It hashes the actual
recovered output including `?` and lists only the settings supplied to search.
It uses `tool_name`, since the search is not a new cipher family for training.

```sh
.venv/bin/python -m unittest tests.test_enigma_crib_search tests.test_enigma -v
```
