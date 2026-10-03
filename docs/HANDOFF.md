# Handoff for the next repository session

This continuation began from verified `origin/main` commit `1ce3727dd419c80fd7983f2a81cc0621943633f0`, subject "Add a handoff note for the next Codex session." That is the starting commit, not a claim about the current tip. Inspect `git log origin/main` before quoting a later SHA.

Use plain sentences. Do not put U+2014 or U+2013 in new text.

## Current user direction

The user asked for useful solvers across modern supplied-key cryptography, documented modern weaknesses, and classical searches. They also asked for stronger reverse engineering, local image OCR, a structured workflow when an unsolved cipher arrives, research into tractable targets, and a puzzle solver. Subagents are permitted.

Continue extending the one `engine/` package. Keep source-backed known answers, old-code-failing regressions, independent controls, explicit limits, and bounded claims. A technique can be useful without establishing a new historical decipherment.

## Added capabilities

- Quagmire I, II, and III supplied-key helpers complete the existing IV family. Modules, tests, certificates, and topical notes use the ACA's printed examples. They reuse the IV transformation. Do not rebuild them. These helpers remain outside `SOLVERS` because the ordinary text-only solve dispatch cannot supply their required keys.
- AES-128/192/256 single-block encryption/decryption matches NIST vectors. ChaCha20 matches RFC 8439 vectors. Both require supplied keys. They are educational primitives, with no authentication or general unknown-key recovery.
- RSA common-modulus recovery uses public parameters for the same-message, shared-modulus, coprime-exponent weakness. Bounded Fermat RSA recovery applies to sufficiently close factors and includes HAC Example 8.4. Existing RSA broadcast remains separate. None is a general RSA break.
- Word-pattern substitution search uses a supplied lexicon, MRV, forward checking, and explicit node/candidate limits. It reports incomplete and ambiguous searches separately. Uniqueness is conditional on the lexicon and completed search.
- Baseline reverse engineering fits affine, substitution, Vigenere, and Beaufort models to multiple aligned cribs. Missing parameters and predicted letters stay explicit; duplicate cribs do not create extra evidence.
- Optional Z3 synthesis adds exact constraints, unknown Quagmire I/II/III alphabets, identity/reverse layouts and row-fill/column-takeoff layouts. Layout occurs before letter encryption. Cribs and predictions use original plaintext coordinates. Example parameters are arbitrary satisfying witnesses. A letter is forced only if an alternate value is unsatisfiable. Any unresolved model or consensus check blocks aggregate prediction beyond supplied cribs. Time and check exhaustion remain unknown/incomplete. See `docs/cipher-synthesis.md` and `requirements-synthesis.txt`.
- `engine.case_workflow` creates local case manifests with preserved source bytes and a separate intake hash anchor. It validates provenance and metadata, observes Unicode without silently converting it to Latin, records bounded Latin statistics only for a declared A-Z alphabet, fits confirmed training cribs only, and compares candidate snapshots with independent heldout evidence. No command marks a case solved or publishes it. Each run records timestamps, settings, Python/Z3 versions, Git identity/dirty flag, input and code hashes, certificate fingerprints, and completion status. See `docs/WORKFLOW.md`, `schemas/cipher-case.schema.json`, `templates/unsolved-case.json`, and `cases/README.md`.
- `engine.puzzles` handles bounded Sudoku, eight-direction word search, and supplied-lexicon anagrams. Sudoku uniqueness requires exhaustive one-answer search; two answers prove nonuniqueness; budget exhaustion cannot return a claimed unique solution. Published Norvig fixtures have solution hashes. These puzzle fields stay outside the neural language router.

Main commands: `python3 -m engine reverse-engineer`, `python3 -m engine word-pattern`, `python3 -m engine.case_workflow`, and `python3 -m engine.puzzles`. Their topical notes give the complete arguments. CLI invalid input now returns a concise status 2 instead of a solve traceback.

## OCR on this checkout

`engine.ocr` detects system Tesseract first, then optional project-local `work/ocr-runtime/bin/tesseract`, then optional macOS Apple Vision. Explicit backend selection does not switch after an error. Native calls are bounded.

A portable official Homebrew Tesseract 5.5.3 bottle and its required libraries were hash-verified and extracted only under ignored `work/ocr-runtime`. Library paths were relocated and modified binaries signed locally. No Homebrew or system installation was performed. That runtime is specific to this Mac and is not committed. The real generated PNG phrase roundtrip and CLI passed with Tesseract. See `docs/ocr-backends.md`.

The Swift Vision helper compiled, but actual native inference failed in the sandbox and timed out outside it. Vision recognition is unvalidated on this desktop. Do not claim that its mocked unit checks prove real recognition. Printed-page OCR does not establish accuracy on archival glyphs, unknown scripts, hidden ink, or scrolls.

## Target research and priorities

`docs/target-triage.md` and `docs/target-shortlist.json` record dated primary-source research checked on 3 October 2026. No checked named unsolved target is established as easy. Prioritize trustworthy transcriptions, known languages, constrained families, related messages, keys, and independent controls. Distinguish applying a surviving key or finding an old decipherment from recovering a new key.

Several Enigma entries in the old unbroken overview are now marked Broken on current message pages. Do not rely on that overview alone. WEUWY Nr. 138 has a potentially useful comparison with Nr. 140, but the message and key pages conflict, so first resolve the sources. RXPSB has 105 known body letters and two gaps in the current transcription, not the stale table's 99; header and transcription lengths conflict. Hyphens represent missing positions, and the existing Enigma helper removes them. It cannot be fed a damaged intercept unchanged without losing rotor steps.

Archival records labeled non-decrypted can have keys, deciphered siblings, contemporary plaintexts, or newer public readings elsewhere. Check those before spending compute. Unknown scripts and short famous puzzles are not quick-win cipher targets merely because their input is small.

## Continuing to add methods

The next published ACA gap identified in this continuation is Condi: `https://www.cryptogram.org/downloads/aca.info/ciphers/Condi.pdf`. Confirm the current module list before implementing it. Read the actual sheet, transcribe its literal plaintext/ciphertext, and add a recovered-output SHA-256 certificate. Do not substitute generated roundtrips for the published known answer.

For real unsolved work, follow `docs/WORKFLOW.md`. Intake files and runtime downloads are ignored by default. Publish only deliberately reviewed case material. Failed or bounded negative results stay research logs, with declared models and bounds. The new K4 baseline crib fit is logged in `docs/logs/reverse-engineer-2026-10-03.md`; no plaintext is claimed.

## Preserve prior user constraints

- Skip Funkspruch Nr. 86. The user said it was solved and the paper was not released. Do not run new Nr. 86 searches. Existing failed logs remain evidence of their own bounded attempts.
- Do not claim a solve of Kryptos K4, Zodiac Z13/Z32, Beale 1/3, McCormick, the real D'Agapeyeff challenge, Voynich, Linear A, Indus, or rongorongo without a cited plaintext and independent evidence. A satisfying model or a bounded negative search is not a decipherment.
- Neural training stays inside the repo. Use `python3 -m engine.neural_router_loop --once` for one pass if needed. Do not create a cron job, recurring routine, or wakeup. New language certificates are discovered automatically. The grader writes weights only if heldout accuracy does not drop. Binary, analysis, and puzzle certificates do not create language training examples. This continuation did not retrain or replace shipped weights.
- Existing K4 search and ciphertext-error modules are already present. Do not recreate them or promote their negative results into a solve.
- Do not reintroduce unrelated project credits.
- Preserve `docs/assets/readme-hero.jpg` exactly. It must remain a real nameless JPEG with magic `ff d8 ff`. Never rewrite it through a contents API.
- Commit as Chase, email `326338179+ChaseHendrick@users.noreply.github.com`. Push using git. If rejected because main advanced, fetch and rebase before retrying.

## Validation and landing

Python 3.10+ is supported. Core routines use the standard library. Optional synthesis uses pinned Z3; OCR requires a local backend and its image-render test needs Pillow. Local executed checks used Python 3.12.14. Python 3.10 syntax was checked statically; actual 3.10 execution belongs to CI.

This checkout also has an ignored `.venv` created with the bundled Python 3.12 runtime and access to its existing Pillow/NumPy packages. Z3 5.1.0.0 is installed inside that venv. Activate it with `source .venv/bin/activate`, or invoke `.venv/bin/python` directly. See `docs/logs/continuation-2026-10-03.md` for the executed 747-test run and validation boundaries.

`.github/workflows/check.yml` runs a core Python 3.10 job with Pillow and NumPy, and an extended Python 3.12 job with Z3, Pillow, NumPy, Tesseract, and fonts. Each runs the suite and a demo in a temporary location. Exact symbolic tests are optional skips without Z3. The first remote run passed extended checks but exposed missing Pillow and NumPy in the original core setup; those dependencies were added. Do not claim success for the corrected run until it completes and is inspected.

Run `python3 -m unittest discover -s tests -v`, and use `python3 -m engine demo --out /path/to/temporary-demo.md` for a fresh witness without committing timing churn. Report the actual test count, exit status, and any optional skips. Known-key decryption, synthetic recovery, OCR phrase recognition, exact conditional constraints, and historical decipherment are different validation scopes.
