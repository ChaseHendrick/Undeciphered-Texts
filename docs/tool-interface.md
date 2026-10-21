# Connected solver interface

Run `python3 -m engine tools` to list every allowlisted tool, its execution mode, input encoding and required parameters. The catalog is generated from the actual public function signatures. It includes supplied-key helpers, unknown-key searches, crib inference and composed investigation. There is no user-supplied module import or dynamic code evaluation. Required fields reflect Python signatures; semantic requirements still apply. For example, Hill inference needs a nonempty crib even though its signature defaults to an empty sequence, and Morse inference needs a lexicon or a crib. The topical documentation and runtime validation state these constraints.

```sh
python3 -m engine run progressive-key KCIWVCD --params '{"keyword":"GRAPEFRUIT","progression":1}'
python3 -m engine run transposition-ensemble AIVLHCEWPFIDRIRLE --params '{"max_checks":1000,"max_candidates":5}'
python3 -m engine run rsa-wiener 1511 --params '{"modulus":8927,"exponent":2621,"plaintext_length":2}'
python3 -m engine run rsa-common-modulus 2790 --params '{"c2":1317,"e1":17,"e2":7,"n":3233}'
python3 -m engine run morse-constraints 0 --params '{"families":["pollux"],"lexicon":["E"],"max_maps":1000}'
python3 -m engine run k4-models EHPFSFEBHMHPF --params '{"cribs":[{"offset":4,"plaintext":"O"}],"families":["plaintext-autokey"],"alphabets":["ABCDEFGHIJKLMNOPQRSTUVWXYZ"],"orders":["substitute-then-transpose"],"max_period":1}'
python3 -m engine investigate LXFOPVEFRNHR --crib 0:ATTACK --max-checks 5000
```

These invocations illustrate explicit parameter contracts. Consult the selected helper's certificate for a complete known-answer vector. Text input can be piped through stdin. AES and ChaCha20 use hexadecimal ciphertext and hexadecimal key/nonce fields. RSA Wiener, Fermat and common-modulus tools accept an integer ciphertext and explicit public parameters. Their plaintext byte results are hexadecimal.

`--params` must contain a JSON object. Unknown names, missing required fields and unexpected parameters fail before invocation. Reports preserve the selected mode and expose derived report fields, including Morse uniqueness only when the actual search establishes it. Cribs use records such as `{"offset":0,"plaintext":"KNOWN"}`. Most Latin tools use A-Z letter positions; Morse constraints and numeric investigation count decoded spaces and punctuation. See [Morse constraints](morse-constraints.md).

The adapter caps raw input at 8,192 characters, RSA values at 4,096 bits, parameter JSON at 64 KiB, nesting at eight levels, strings at 8,192 characters, sequences at 1,000 entries and mappings at 100 fields. Individual tools impose narrower bounds. It also caps restarts, iteration counts and requested byte lengths. These constraints bound local invocation rather than establishing a hard wall-time limit for every function.

Some repository experiments accept callbacks, lists of ciphertexts or physical-device signals; those require their documented Python APIs. They are not silently forced into a text invocation. `run` reports successful execution under the selected tool's assumptions. A recovered candidate, score, crib fit or reencryption check still requires independent evidence before a historical solve claim.

`substitution-tempering` searches unknown bijective keys using several logical
temperature chains, sparse quadgram swap deltas, and replica exchanges. It
returns a score-ranked `SolveResult`, actual work counters and the reason it
stopped. Its finite proposal allowance includes greedy polishing. The optional
dense `logp` table belongs to the Python API: 456,976 entries exceed this JSON
adapter's sequence limit. The default uses the existing English model.
See [replica exchange](substitution-parallel-tempering.md).

`unspaced-substitution` jointly infers word boundaries and a global bijective
mapping using a supplied lexicon. Node, frontier, candidate and time limits
remain explicit; exhausting a limit does not establish uniqueness. Complete
search excludes only the supplied vocabulary and word-length model. This adapter
accepts at most 1,000 lexicon entries within 64 KiB of parameters; the direct
Python API has separate larger finite bounds. See [unspaced constraints](unspaced-substitution.md).

```sh
python3 -m engine run substitution-tempering CEIOPFIFCIKIGCEIKDDOPFGCEIFCEIDCEIKOIFQPOICDOIICEAOCEIKIAFCEIODKFAFMCEIWTIKIPNNKIPGWPFG --params '{"seed":1729,"restarts":4,"sweeps":5000,"max_proposals":180000,"timeout_seconds":20}'
python3 -m engine run unspaced-substitution DTTZQZZITUQZT --params '{"lexicon":["MEET","AT","THE","GATE"],"max_nodes":10000}'
```

Both examples recover constructed controls without receiving their keys.
The [Dorabella campaign](logs/dorabella-force-2026-10-03.md) records actual
target searches, independent replay audits, and failed short controls.

`k4-models` is a conditional composition tester usable on any 4 through 512
ASCII-letter input, despite its K4 research origin. It requires at least one
aligned crib and tests repeating, Beaufort, plaintext-autokey and
ciphertext-autokey recurrences with ragged layouts in both composition orders.
Periods and widths stop at 32; at most 10,000 model checks are allowed. Unknown
key slots remain `null` and unknown plaintext positions remain `?`. Candidate
storage limits do not imply search completion. It never claims a historical
plaintext. Reserve verification clues outside inference and evaluate them after
the search; see the [executed experiment and complete reproduction record](k4-focus/model-experiments-2026-10-03.md).
