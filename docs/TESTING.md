# Testing

A passing run means the tested cipher routines matched their known answers and the workflow respected its input and result contracts. Some tests recover an unknown key; others decrypt a published worked example with its supplied key. With a local OCR backend, the image test reads a PNG drawn by the test itself. Symbolic checks require the optional Z3 dependency. It does not mean an ancient script, a scroll, or secure modern cryptography was broken.

## What “ALL PASS” means

The standard-library runner does **not** print the words `ALL PASS`.

A clean run ends like this (captured 2026-10-02, before the OCR tests existed the count was 7):

```text
----------------------------------------------------------------------
Ran N tests in …s

OK
```

**ALL PASS** in a checklist means all three of these, and nothing less:

1. The process exit status is **0**.
2. The last line is `OK`, not `FAILED (failures=…)` or `FAILED (errors=…)`.
3. The `Ran N tests` line matches the tests you think you ran. Report optional dependency skips separately.

`discover -s tests` collects every `test*.py`. A run that only executes `tests/test_recover.py` and says `Ran 7 tests` / `OK` is a pass of the classical set only. Say which command you ran.

## Commands

From the repository root, use Python 3.10 or newer. Local validation on 2026-10-03 uses `.venv/bin/python` (Python 3.12); the system Python may be older than the package requirement. Create a virtual environment with a supported interpreter if one is not present.

```bash
.venv/bin/python -m pip install Pillow numpy
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m engine demo
.venv/bin/python demos/run_demo.py
.venv/bin/python -m unittest tests.test_ocr tests.test_errors tests.test_recover -v
```

Pillow and NumPy are required by full discovery of the existing image and neural tests. Core cipher routines and the recovery demo remain usable without them. Install `requirements-synthesis.txt` for exact symbolic checks and a local OCR backend for the real image roundtrip; absent optional engines are reported as skips.

## Frozen searches

Many D'Agapeyeff and Bob reports are decorated with `@frozen` and stored in `engine/data/swarm_cache`. Their unit tests read the stored file and do not rerun the search, so a green unit run does not show that the code still produces those numbers. Rerun them with:

```bash
python3 tools/verify_cache.py --jobs 3            # every frozen file, about 40 minutes on 3 cores
python3 tools/verify_cache.py router-swarm widths # only these names
python3 tools/verify_cache.py --list              # names and the function behind each
```

It reports `match`, `mismatch` with the differing keys, `timeout`, or `error`, and never rewrites a file. A new frozen report also needs an entry in `engine/dagapeyeff_provenance.py`; `tests/test_dagapeyeff_cache.py` names any that are missing. Tests that download a cited page skip when the host cannot be reached.

`demo` rewrites `DEMO.md` and returns 1 if any fixture misses. It appends [logs/errors.md](logs/errors.md) only in that failure case. Do not run a deliberately broken demo against the real log.

## The seven recovery tests

`tests/test_recover.py`:

| Test | What it checks |
|---|---|
| `test_caesar_roundtrip` | encrypt then decrypt with the known shift |
| `test_vigenere_roundtrip_keeps_punctuation` | forward map preserves spaces and punctuation |
| `test_substitution_roundtrip` | key is 26 letters and round-trips |
| `test_caesar_recovers_shift_and_text` | solver is not told the shift |
| `test_vigenere_kasiski_and_recovery` | key length is among Kasiski votes; recovered key matches |
| `test_substitution_recovers_plaintext_and_key` | annealing from `DEMO_SEED` recovers the key |
| `test_ngrams_and_model_prefer_english` | the English model scores real prose above a shuffle |

Fixtures are in `engine/fixtures.py`. Ciphertext is built inside the test. The solver function is not passed the key.

## OCR and the error writer

- `tests/test_ocr.py` tests backend selection and error controls without native dependencies. Its image integration test detects system or local Tesseract, then optional macOS Vision. When it runs, it draws `THE HARBOR BELL RANG` and requires those letters back, spaces ignored. A detected backend that fails OCR makes the test fail. A missing-backend skip is not a pass of OCR.
- `tests/test_errors.py` points the writer at a temporary file. It must not create an entry in `docs/logs/errors.md`.

## Image bytes

`tests/test_assets.py` checks the hero JPEG magic and SVG fallback. Also compare the JPEG's bytes with the starting commit before landing unrelated changes:

```bash
python3 -c "p=open('docs/assets/readme-hero.jpg','rb').read(3); print(p.hex()); assert p==bytes.fromhex('ffd8ff')"
```

`FF D8 FF` is the JPEG start. If the file begins with `iVBOR` or `/9j/` or another base64 alphabet, the upload stored text. Do not commit that. PNG magic, if you add one, is `89 50 4E 47`. The README displays the preserved JPEG; its SVG fallback is text and starts with `<svg`.

## Adding a solver

1. Put it in `engine/solvers/`. `SOLVERS` contains the existing text-only unknown-key searches. Supplied-key helpers such as the Quagmires stay outside that registry. An explicit `engine/tool_registry.py` adapter may expose a helper or bounded search with its required parameters, input encoding and mode.
2. Add a known-plaintext test that fails before the solver works.
3. If it joins the demo, regenerate `DEMO.md` by running the demo, and commit that file.
4. Do not assert a stub, and do not decrypt with a key the test already used to build the ciphertext and then call that a recovery.

## Quagmire published examples

The Quagmire I, II, III, and IV tests use ciphertext printed on the ACA sheets and the published keywords. The certificate checks hash the recovered plaintext. Run this set with:

```bash
python3 -m unittest discover -s tests -p 'test_quagmire_*.py' -v
```

These checks cover supplied-key encryption and decryption, not a search for an unknown Quagmire key.

## What these tests do not cover

- Linear A, Indus, Rongorongo, Voynich, Iberian, Meroitic, Etruscan meaning.
- Herculaneum CT, ink models, or Greek transcription.
- Breaks of secure production AES, production RSA or live TLS. Modern primitive vectors and explicitly weak RSA instances have separate tests; a synthetic textbook-weak e=3 RSA broadcast check lives in `tests/test_rsa_broadcast.py`.
- General Enigma rotor, ring and plugboard key recovery. Known-key Enigma vectors and conditional start recovery under supplied machine settings are covered. Published Playfair and two-square controls are covered; wartime Truppenschlüssel Nr. 86 is logged as failed, not as a recovered plaintext.
- Wall-time performance guarantees. The demo's printed seconds are local measurements, not such a guarantee.
- The stale commands in `docs/engine.md`.

## CI

`.github/workflows/check.yml` installs Pillow and NumPy for the existing image and neural tests, then runs test discovery and the recovery demo on Python 3.10 without Z3. Exact symbolic tests report optional skips in that job. An extended Python 3.12 job installs Z3, Pillow, NumPy, Tesseract, and a demo font, then runs the full suite and demo. Demo output goes to the runner's temporary directory. These jobs run on pull requests, main pushes, or manual dispatch. Adding a workflow does not establish a remote CI pass; inspect the completed run.

## Modern helpers, constraints, and case records

```bash
python3 -m pip install -r requirements-synthesis.txt
python3 -m unittest tests.test_aes tests.test_chacha20 tests.test_rsa_common_modulus tests.test_rsa_fermat -v
python3 -m unittest tests.test_word_pattern tests.test_reverse_engineer tests.test_cipher_synthesis tests.test_case_workflow -v
```

AES and ChaCha20 match official published vectors using supplied keys. RSA checks exercise the stated weak-instance preconditions and rejection paths. Word-pattern search is also compared with an exhaustive small-instance oracle. Reverse-engineering checks predict letters beyond supplied cribs; symbolic checks distinguish satisfying examples from forced letters and keep timeout or check exhaustion incomplete. Case tests use temporary directories for source preservation, tamper detection, path restrictions, snapshots, and candidate classifications. No private intake source is a test fixture.

Without Z3, dependency validation still runs and the exact symbolic integration tests skip. No skip is reported as symbolic recovery. The core cipher package, baseline inference, and case intake remain usable without Z3.

## Sourced expansion and connected tools

```bash
.venv/bin/python -m unittest tests.test_baconian tests.test_condi tests.test_progressive_key tests.test_periodic_gromark -v
.venv/bin/python -m unittest tests.test_monome_dinome tests.test_morbit tests.test_pollux tests.test_numbered_key tests.test_redefence tests.test_sequence_transposition tests.test_rsa_wiener -v
.venv/bin/python -m unittest tests.test_checkerboard tests.test_homophonic tests.test_interrupted_key -v
.venv/bin/python -m unittest tests.test_morse_constraints tests.test_transposition_ensemble tests.test_tool_registry tests.test_solver_reasoning tests.test_cli_controls -v
.venv/bin/python -m unittest tests.test_connected_helpers tests.test_case_investigation -v
.venv/bin/python -m unittest tests.test_autokey_inference -v
.venv/bin/python -m unittest tests.test_enigma_crib_search tests.test_enigma -v
.venv/bin/python -m unittest tests.test_hill_inference -v
.venv/bin/python -m unittest tests.test_persona_emperor_solver tests.test_persona_inheritance_solver tests.test_persona_hallucinogens_solver tests.test_persona_pacifist_solver -v
.venv/bin/python -m unittest tests.test_persona_detective_solver tests.test_persona_cartographer_solver tests.test_persona_mechanic_solver tests.test_persona_normal_man_solver tests.test_persona_adversary_solver tests.test_persona_skeptic_solver -v
.venv/bin/python -m unittest tests.test_persona_solver_common tests.test_persona_council tests.test_persona_council_audit tests.test_case_investigation -v
.venv/bin/python -m unittest tests.test_solver_scheduler tests.test_persona_adaptive_schedule -v
.venv/bin/python -m unittest tests.test_neural_training tests.test_neural_router_v2 tests.test_neural_lookahead -v
.venv/bin/python -m unittest tests.test_neural_m209_features tests.test_neural_audit tests.test_neural_exclusions tests.test_neural_artifact -v
```

The optional council scheduler has 17 policy and integration controls. They check
correctness before check cost, baseline-relative evidence gates, exact budgets,
minimum exploration, current-input exclusion and isolation of prior outcomes
from plaintext fitting. Without a profile the original council allocation stays
unchanged. Full local discovery on 2026-10-03 passed 1078 tests in 37.108 seconds
with NumPy, Pillow, Z3 and a detected local OCR backend, without skips. This is a
local tested result; inspect CI separately. See [cross-repository learning](cross-repo-learning.md).

The thirteen new classical helpers replay literal ACA examples with their published parameters. RSA Wiener instead uses an independently published weak key and a clearly labeled synthetic message. Recovered output is hashed, including only the bytes or letters declared by each certificate. Progressive Key certifies the printed 30-letter prefix; Baconian's second carrier certifies eleven printed letters. No missing continuation is invented.

Unknown-key checks are separate. Condi receives a bounded keyword list and cribs; Progressive Key infers period, progression and key slots from cribs; Redefence enumerates a declared key range. Homophonic infers independent numeric-row shifts while retaining unobserved rows. Interrupted Key receives a reset pattern and fits unknown keyword slots without pretending to search all interruptions. Plaintext-autokey inference tests bounded primer lengths, separates exact crib-forced values from scored examples, and validates NumPy and standard-library feature calculations against an independent modular oracle using caller training tables. Morse map inference receives a lexicon or cribs, checks complete combinatorial counts and keeps unresolved ambiguity on exhaustion. Morse crib offsets include decoded spaces, unlike letter-only Latin coordinates. The transposition portfolio shares a budget across families and checks each inverse against its forward transform. English rank, a compatible key, and reencryption are not independent historical verification.

Hill inference receives aligned letters instead of an encryption matrix. Its
printed four-letter control checks matrix recovery; a separate literal
28-letter constructed vector predicts 21 letters beyond a seven-letter crib.
Tests independently enumerate all 456,976 possible 2 by 2 encryption matrices
for a sparse case, compare conditional consensus across all accepted keys,
and prevent incomplete budget prefixes from asserting uniqueness or forced
plaintext. Retained candidate caps do not truncate the consensus calculation.

Registry and investigation tests check JSON parameter contracts, required keys, binary encodings, typed crib coordinates, global check accounting, rejected contradictory premises, forward mismatch detection, neural-unavailable behavior, and unverified candidate status. Case integration preserves original input snapshots, records operation bounds and runtime versions, excludes tentative or heldout cribs from fitting, and verifies candidate files in a separate run.

Neural objective tests use central finite differences for label-smoothed weighted cross-entropy and paired-view consistency, including shared pairs and zero supervised weights. They check normalized curricula, a valid 11,776-row two-view batch, rejected limits, and the control that a faster wrong answer earns no positive reward. Residual-router tests check exact derivatives, repeatable fitting, numerical stability, class-order and artifact validation, and promotion gates. The shipped model uses disclosed synthetic family labels and separate training/selection/calibration slices. The fixed Doyle source was initially heldout; repeated model comparisons now make its reported scores development-benchmark results. An untouched source is required for an independent final generalization audit. Benchmark comparisons must replay the same ciphertexts and state the output class counts; adding classes changes the problem and does not justify comparing unmatched aggregate accuracies.

Training augmentation and dropout views are not repairs of an unknown transcription. Family ranking is advisory. Simulated reward and investigation control states describe numerical behavior, not feelings or consciousness. Timing is local evidence only; independent correctness gates determine promotion. Final run counts, optional skips and current benchmark results are recorded in [logs/solver-expansion-2026-10-03.md](logs/solver-expansion-2026-10-03.md).

The final separate Wells audit uses a frozen model and source-hashed previously unused prose, checks corpus separation, and records fresh synthetic-key results without fitting or calibration. Current counts and source files are in [neural-upgrades.md](neural-upgrades.md). It remains a family-classification audit, not a test of historical decipherment. The Enigma start search preserves each lost-letter slot across rotor steps and independently checks both work budgets and start ambiguity under supplied machine settings.

Persona solver tests are `tests/test_persona_*_solver.py`, with shared input and council tests alongside them. Legacy sentence-preference tests remain separate. New APIs recover literal unknown-key controls, preserve exact budgets, and keep incomplete consensus unknown. The council's heterogeneous-score regression failed before a single shared score replaced sum/mean comparisons. Case integration tests confirm the council receives no reserved evidence; standalone Skeptic review uses that evidence only after candidate generation.

The ten-policy council tests selected lazy loading, evidence overlap rejection,
reserved-reference review after generation, and rejection without silently
backfilling an unreviewed lower-ranked answer. Normal Human Man tests only 26
Caesar shifts and fence heights 2 through 7. Its narration and the other
persona names do not alter correctness requirements or Bob's family labels.

The `tools` command reports signature-required fields, which do not describe
every runtime evidence constraint. A Hill call still needs a nonempty crib;
Morse inference needs a lexicon or decoded-text crib. CLI checks should include
`--help`, JSON discovery, a literal published supplied-key example, and clean
rejection of omitted required keys. A successful invocation or printed
candidate does not establish a historical solution. Record the actual command,
bounded checks and output contract; remote CI and final full-suite counts must
come from completed runs.
