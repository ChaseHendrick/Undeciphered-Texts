# Testing

## What "passing" means

A green test means the solver recovered **known classical plaintext** from ciphertext it was **not** given the key for. It does **not** mean any ancient script or modern cipher is broken.

## Commands

From the repository root (Python 3.10+):

```bash
python -m unittest discover -s tests -v
python -m engine demo          # also rewrites DEMO.md
python demos/run_demo.py       # same demo path
```

Expect **7** tests in `tests/test_recover.py`:

| Test area | Checks |
| --- | --- |
| Caesar round-trip | encode → decode with known shift |
| Vigenère round-trip | punctuation preserved in forward map |
| Substitution round-trip | key round-trips |
| Caesar recovery | shift + plaintext without being told the shift |
| Vigenère recovery | Kasiski/IC path recovers key + plaintext |
| Substitution recovery | annealing path recovers plaintext + key |
| N-gram model | English model prefers English-like text |

## Fixtures

- Built in `engine/fixtures.py` / generated inside tests via `engine/ciphers.py`.
- Demo plaintexts are fixed English prose; keys are known only to the test harness when building ciphertext, then discarded before solve.

## Adding a solver

1. Implement under `engine/solvers/`.
2. Register it like the existing solvers.
3. Add a **known-plaintext recovery** test that fails before the implementation works.
4. Run the demo path if the cipher is part of the public demo set; commit the regenerated `DEMO.md`.
5. Do not add a test that "passes" by asserting a stub or by decoding with a leaked key.

## What not to test here

- Claims about Linear A, Indus, Rongorongo, Voynich, etc.
- Modern crypto (AES, RSA, …).
- Flaky timing-only benchmarks as correctness gates.

## CI suggestion

Minimal job: `python -m unittest discover -s tests -v` on Python 3.10+. Optional second step: `python -m engine demo` and `git diff --exit-code DEMO.md` if you want the witness file kept in sync.
