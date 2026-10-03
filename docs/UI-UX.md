# UI / UX

This repository is a terminal and a set of Markdown files. There is no web app. “UI” means what a person sees when they run `python -m engine`, and what GitHub renders from the README.

Checked against the code on 2026-10-02 (ET). `docs/engine.md` still describes a different CLI (`python -m engine.cli`, `stats`, `crib`, `unsupervised`). That file is stale. The help text below is what the process prints.

## Hero

README line 3 is `![Hero](docs/assets/readme-hero.svg)`.

The SVG is 1,366 bytes of XML: a dark panel, twelve outlined rectangles, and the words “UNDECIPHERED TEXTS”. GitHub renders SVG in a README. It does not depend on a binary upload.

`docs/assets/readme-hero.jpg` is a real JPEG beside it (53,643 bytes, magic `FF D8 FF E0`, `JFIF`). The README does **not** link it, because an MCP upload of that file can store base64 text instead of the blob. A base64 `.jpg` does not render. See [logs/errors.md](logs/errors.md). Do not point the hero at a file whose first bytes are not `FF D8 FF` (JPEG) or `<svg` / the PNG magic `89 50 4E 47`.

The picture is ornament. It is not a decipherment and not a scroll.

## One entry point

```text
usage: python -m engine [-h] {analyze,solve,demo} ...

Recover classical ciphers with IC, Kasiski, n-grams, and search.
```

Subcommands, from `python3 -m engine --help` on this machine (`python` itself was not on `PATH`; see the error log):

| Command | Help line | Defaults |
|---|---|---|
| `analyze` | IC, Friedman, Kasiski, and n-gram counts | `--max-period` 16. Text argument optional; omitted means stdin |
| `solve` | recover plaintext | method is `caesar`, `substitution`, or `vigenere`. `--max-period` 12, `--restarts` 10, `--steps` 4000, `--seed` 20261002 |
| `demo` | encrypt known text, solve it, write DEMO.md | `--out` `DEMO.md` (resolved from the repo root, not the cwd) |

There is no color. Correctness does not depend on a wide terminal. Lines are `key: value` and then `plaintext:`.

### What a successful Caesar solve looks like

`python3 -m engine solve caesar "Wkh kdueru ehoo udqj"` (the README sample). Captured output:

```text
method: caesar
key: 3
score: -49.6062
shift: 3
chi_square: 27.277
letters: 17
trials: 26
plaintext:
The harbor bell rang
```

Stdout is the product. There is no “done” with an empty screen.

### Errors a person will actually see

| Input | Exit | What is printed |
|---|---|---|
| `python -m engine` with no subcommand | 2 | argparse: `the following arguments are required: command` |
| `solve rot13 ...` | 2 | `invalid choice: 'rot13' (choose from caesar, substitution, vigenere)` |
| `analyze` of `123 !!!` or empty stdin | 2 | stderr: `no letters in input` |
| `solve caesar` of `123 !!!` | 1 | A traceback ending in `ValueError: ciphertext has no letters`. Analyze guards this; solve does not. That inconsistency is a gap, not a feature |
| `demo` when a fixture is not recovered | 1 | `DEMO.md` is still rewritten, with `failures:` naming the cipher, and `engine/errors.py` appends [logs/errors.md](logs/errors.md). A success does not append |
| `python -m engine.ocr` with no arguments | 2 | `give an image path or --render TEXT` |
| OCR stdout empty | 3 | stderr: `ocr returned no text` |

Do not print “deciphering Linear A” or a progress bar for an ancient script. The solvers only claim Caesar, Vigenère, and simple substitution of English.

## Demo witness

`python -m engine demo` overwrites `DEMO.md` with ciphertext, recovered plaintext, shift or key, and timings. The checked-in file is a previous run (overall about 3.6 seconds, failures none, substitution exact match). Re-running changes the timings. Do not hand-edit it and leave it looking like a run.

`python demos/run_demo.py` calls the same function.

## OCR surface

Separate from the solvers. `python3 -m engine.ocr --render "THE HARBOR BELL RANG"` writes a PNG and prints the line Tesseract read. Documented in [image-reading.md](image-reading.md). It must not be described as reading a photograph of a scroll.

## Docs presentation

- README leads with the limit (no new decipherment) and a start-here path (DECODE, Crypto Cellar), then the engine.
- Rankings live in [closest.md](closest.md) with criteria. Logs are not rankings.
- Tables for layout. Long arguments stay in the topical file.
- Research logs and the error log are visually separate from landscape claims.

## Gaps that still show up in the checklist

- `docs/engine.md` documents commands and files that are not in the tree (`engine.cli`, `engine/ic.py`, `en_quadgrams.json.gz`, `demos/fixtures/`, `tests/test_solvers`, German and Spanish Caesar). Trust this file and [TESTING.md](TESTING.md) until that page is rewritten.
- `docs/external.md` still says `python -m engine.cli demo`.
- README’s layout table does not yet list every doc (`next.md`, `image-reading.md`, `UI-UX.md`, `TESTING.md`, `ERROR-LOG.md`).
- No `.github` workflow runs the tests.
- No `LICENSE` file. The README says personal research notes.
- Solve’s no-letter path is a traceback; analyze’s is a one-line error. They should match, and they do not.
- `python` versus `python3` is undocumented in the README.
