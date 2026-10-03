# Testing

A passing run means the solvers recovered **known English plaintext** from ciphertext they were not given the key for, and, if Tesseract is installed, that OCR read a PNG the test itself drew. It does not mean an ancient script, a scroll, or a modern cipher was broken.

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
3. The `Ran N tests` line matches the tests you think you ran. Today that is the recovery file plus `tests/test_ocr.py` and `tests/test_errors.py` when those files are collected.

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

- `tests/test_ocr.py` skips if `tesseract` is not on `PATH`. When it runs, it draws `THE HARBOR BELL RANG` and requires those letters back, spaces ignored. A skip is not a pass of OCR. Report the skip.
- `tests/test_errors.py` points the writer at a temporary file. It must not create an entry in `docs/logs/errors.md`.

## Image bytes

There is no unit test for the hero JPEG. Check it by hand before trusting a render:

```bash
python3 -c "p=open('docs/assets/readme-hero.jpg','rb').read(3); print(p.hex()); assert p==bytes.fromhex('ffd8ff')"
```

`FF D8 FF` is the JPEG start. If the file begins with `iVBOR` or `/9j/` or another base64 alphabet, the upload stored text. Do not commit that. PNG magic, if you add one, is `89 50 4E 47`. The README hero that must render is the SVG, which is text and starts with `<svg`.

## Adding a solver

1. Put it in `engine/solvers/` and register it in `SOLVERS`.
2. Add a known-plaintext test that fails before the solver works.
3. If it joins the demo, regenerate `DEMO.md` by running the demo, and commit that file.
4. Do not assert a stub, and do not decrypt with a key the test already used to build the ciphertext and then call that a recovery.

## What these tests do not cover

- Linear A, Indus, Rongorongo, Voynich, Iberian, Meroitic, Etruscan meaning.
- Herculaneum CT, ink models, or Greek transcription.
- Production AES, production RSA, live TLS, Enigma, single-square Playfair. A synthetic textbook-weak e=3 RSA broadcast known-answer check lives in `tests/test_rsa_broadcast.py`. Two-square keyword recovery is covered in `tests/test_two_square.py`; wartime Truppenschlüssel Nr. 86 is logged as failed, not as a recovered plaintext.
- Timing. The demo prints seconds. They are not a gate.
- The stale commands in `docs/engine.md`.

## CI

There is no workflow in the tree. A minimal job is `python3 -m unittest discover -s tests -v` on Python 3.10 or newer. Optional second step: `python3 -m engine demo` and `git diff --exit-code DEMO.md` if the witness must stay frozen. OCR belongs in the same job only on an image that also installs `tesseract-ocr` and `python3-pil`.
