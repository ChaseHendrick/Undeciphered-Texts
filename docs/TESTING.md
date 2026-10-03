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

From the repository root. On this box the binary is `python3`. A venv named `python` is what the README assumes.

```bash
python3 -m unittest discover -s tests -v
python3 -m engine demo
python3 demos/run_demo.py
python3 -m unittest tests.test_ocr tests.test_errors tests.test_recover -v
```

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

There is no unit test for the hero JPEG. Check it by hand before trusting a render:

```bash
python3 -c "p=open('docs/assets/readme-hero.jpg','rb').read(3); print(p.hex()); assert p==bytes.fromhex('ffd8ff')"
```

`FF D8 FF` is the JPEG start. If the file begins with `iVBOR` or `/9j/` or another base64 alphabet, the upload stored text. Do not commit that. PNG magic, if you add one, is `89 50 4E 47`. The README hero that must render is the SVG, which is text and starts with `<svg`.

## Adding a solver

1. Put it in `engine/solvers/`. Register a text-only unknown-key search in `SOLVERS` when the CLI can invoke it. Supplied-key helpers such as the Quagmires stay outside that registry.
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
- Production AES, production RSA, live TLS, Enigma, single-square Playfair. A synthetic textbook-weak e=3 RSA broadcast known-answer check lives in `tests/test_rsa_broadcast.py`. Two-square keyword recovery is covered in `tests/test_two_square.py`; wartime Truppenschlüssel Nr. 86 is logged as failed, not as a recovered plaintext.
- Timing. The demo prints seconds. They are not a gate.
- The stale commands in `docs/engine.md`.

## CI

`.github/workflows/check.yml` runs standard-library tests and the recovery demo on Python 3.10. An extended Python 3.12 job installs Z3, Pillow, NumPy, Tesseract, and a demo font, then runs the full suite and demo. Demo output goes to the runner's temporary directory. These jobs run on pull requests, main pushes, or manual dispatch. Adding a workflow does not establish a remote CI pass; inspect the completed run.

## Modern helpers, constraints, and case records

```bash
python3 -m pip install -r requirements-synthesis.txt
python3 -m unittest tests.test_aes tests.test_chacha20 tests.test_rsa_common_modulus tests.test_rsa_fermat -v
python3 -m unittest tests.test_word_pattern tests.test_reverse_engineer tests.test_cipher_synthesis tests.test_case_workflow -v
```

AES and ChaCha20 match official published vectors using supplied keys. RSA checks exercise the stated weak-instance preconditions and rejection paths. Word-pattern search is also compared with an exhaustive small-instance oracle. Reverse-engineering checks predict letters beyond supplied cribs; symbolic checks distinguish satisfying examples from forced letters and keep timeout or check exhaustion incomplete. Case tests use temporary directories for source preservation, tamper detection, path restrictions, snapshots, and candidate classifications. No private intake source is a test fixture.

Without Z3, dependency validation still runs and the exact symbolic integration tests skip. No skip is reported as symbolic recovery. The core cipher package, baseline inference, and case intake remain usable without Z3.
