# Undeciphered Texts & Open Historical Ciphers

Research notes and a **classical cipher engine** for **Chase Hendrick (Sharpie)**.

**This repository does not claim any new decipherment of ancient scripts.**
The `engine/` package recovers *known* classical ciphers (Caesar, Vigenère, monoalphabetic substitution) with tests and fixtures. Famous undeciphered systems are documented for context and realistic contribution paths.

Inspiration: amateur / hobby recovery of old German coded messages (Crypto Cellar Enigma work and related discussion), plus historical breaks such as Copiale and Zodiac Z340.

## Recommendation (start here)

Work **digitized historical ciphertexts in known languages** first—not Linear A or Voynich.

1. [DECODE / DECRYPT](https://de-crypt.org/) — thousands of archival cipher images, keys, transcription/cryptanalysis tools.
2. [Crypto Cellar — Breaking German Army Ciphers](https://cryptocellar.org/bgac/) — remaining public Enigma / Wehrmacht challenges.
3. Early-modern diplomatic / nomenclator letters marked non-decrypted in DECODE (see also community catalogues built on DECODE).

## Quick start (engine)

```bash
# from repo root
PYTHONPATH=. python -m engine.cli --help
PYTHONPATH=. python -m engine.cli demo          # recovers built-in known cases
PYTHONPATH=. python -m demos.run_known_solves
PYTHONPATH=. python -m tests.test_solvers
```

Optional: `pip install -r requirements.txt` (stdlib-first; numpy listed for future numeric work).

## Repository layout

| Path | Role |
|------|------|
| [`engine/`](engine/) | Classical cryptanalysis package + CLI |
| [`demos/fixtures/`](demos/fixtures/) | Known plaintext/ciphertext pairs |
| [`demos/run_known_solves.py`](demos/run_known_solves.py) | Prints PT/CT/solver output; exit 0 on recovery |
| [`tests/`](tests/) | Unit tests for Caesar / Vigenère / substitution |
| [`docs/landscape.md`](docs/landscape.md) | Undeciphered & partly deciphered scripts/texts |
| [`docs/closest.md`](docs/closest.md) | Ranked “closest to breakthrough” (hype-checked) |
| [`docs/recent-cracks.md`](docs/recent-cracks.md) | Recent/famous cracks and methods |
| [`docs/starter-projects.md`](docs/starter-projects.md) | Concrete open targets with data URLs |
| [`docs/methods.md`](docs/methods.md) | How amateurs make progress |
| [`docs/engine.md`](docs/engine.md) | SOTA vs what this engine actually does |
| [`docs/sources.md`](docs/sources.md) | Consolidated URLs |
| [`docs/external.md`](docs/external.md) | External repos, tools, papers (pointers; not vendored) |

Architecture quality bar (structure/CLI/tests honesty) references [GENChase](https://github.com/ChaseHendrick/GENChase); domain logic here is original classical crypto—not genart/simulation code.

## Honest limits

- **Does:** frequency stats, IC, Kasiski-style period hints, Caesar, Vigenère, English substitution (annealing), crib drag, demo recovery of fixtures.
- **Does not:** decipher Linear A, Indus, Rongorongo, Phaistos, Voynich, or other undeciphered scripts/languages.

## External engines (not vendored)

Prefer [CrypTool 2](https://github.com/CrypToolProject/CrypTool-2), [CTTS](https://github.com/CrypToolProject/CTTS), and [DECODE](https://de-crypt.org/) for real manuscripts. See [`docs/external.md`](docs/external.md).

## License note

Personal research notes. Linked museum/archive resources keep their own terms.
