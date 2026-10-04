# Handoff for the next repository session

This continuation began from verified `origin/main` commit `1ce3727dd419c80fd7983f2a81cc0621943633f0`, subject "Add a handoff note for the next Codex session." That is the starting commit, not a claim about the current tip. Inspect `git log origin/main` before quoting a later SHA.

Use plain sentences. Do not put U+2014 or U+2013 in new text.

## Session 4 October 2026

Started from verified `origin/main` commit `6a6df75c1a9a323a7aaa0b10f16ccb761faa2ab1`. Added a metadata-only Truppenschlüssel residue ledger for the CryptoCellar page updated 27 July 2026. The count is 41 listed, 11 marked broken, 30 unmarked. See `docs/truppenschluessel-residue-2026-10-04.md` and `engine/truppenschluessel_residue.py`. No ciphertext was added and no residue message was attacked. Funkspruch Nr. 86 remains skipped. The next unchecked queue item in `docs/next.md` is the DECODE metadata audit.

## Session 4 October 2026, Bob and K4

Started from the residue commit on `main`. Bob's shipped format 5 file was scored, not replaced. SHA-256 `d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825` was unchanged. Seed 20261004, 16 samples per family, first 180 training Austen letters: restricted Enigma/M-209 top one 14/32, broad settings 15/32. That sample is too small to promote or reject a model. See `docs/bob-generator-2026-10-04.md`.

K4 swarm, all with `solved` false and `claimed_plaintext` null:

- `engine.k4_model_finish` completed both 32,512-hypothesis folds (65,024 checks). Reserved exact predictions: 0. All 888 complete keys contradicted the withheld crib.
- Running key: 240 offsets of the in-repo K3 plaintext, 0 crib hits. K1 is 63 letters and was skipped. No K2 text was typed in.
- Hill: the 97-letter string is rejected without padding. Dropping either endpoint letter finishes 2x2 Hill with 0 compatible keys.
- Keyword panel: PALIMPSEST, ABSCISSA, KRYPTOS. Porta returned three 97-letter texts and no crib hit. Playfair and two-square reject the odd length. Gromark rejects a missing primer.
- Innovative swarm, 4 October 2026: in-place ACA Gromark is impossible for any keyword because ciphertext letters F, K, and P cannot share one alphabet index with both public cribs. Myszkowski under the three published keywords, on either side of that Gromark, is the same blocked pairing. Periodic Gromark on those keywords has 0 crib hits. Quagmire I-IV over 11310 declared settings has 0 crib hits. See `docs/k4-focus/innovative-swarm-2026-10-04.md`.

Do not describe any of those negative results as a K4 solution. Do not replace the format 5 weights from the 16-sample probe.

## Session 4 October 2026, what is close

The September 2026 master list has already credited the MVUEH, FMNGI, AWTZK, ZNLZT, and WEUWY breaks. The open Enigma row that the publisher marks as one day away is LXACA, 5 July 1941, Nr. 100, 20 body letters. The key page says it does not break on 5 July and is probably 4 July traffic. No 4 July key is printed.

`engine.lxaca_neighborhood` checks the published keys for 1 July and 5 through 9 July, then 152 indicator edits on the 5 July key. Controls match first: DEROP's indicator gives WER, and the corrected WEUWY indicator gives SPE. No LXACA output is claimed. One noisy 20-letter edit scores above the DEROP prefix and does not read as German. See `docs/logs/lxaca-neighborhood-2026-10-04.md`. Do not describe that score as a break. Do not search an invented 4 July key and call the result unique.

The next swarm stayed inside the Truppenschlüssel residue and did not search a square. IASRZ Nr. 129 and 130 share the prefix `IASRZEDSTB`, and the bodies are odd once the designator is removed. DSZPZ and DEZPS, both headed 1735, align at 33 letters against a 20-draw null maximum of 15. SSKFV and HOHOX share the suffix `LMOTIYIZ`. See `docs/logs/ts-close-pairs-2026-10-04.md`. Do not describe that agreement as a reading.

A follow-up climb on the even windows, including one-letter endpoint drops, beat a shuffled control on all 7 windows. Both endpoint drops beat it, so the Grimm trigram scorer is not choosing a text. No plaintext was stored. See `docs/logs/ts-pair-climb-2026-10-04.md`. Do not promote those scores to a key.

The pair grid is a separate check. Pairs that start on the first printed letter repeat about as often as the Grimm sample in the longer messages, and random letters of that length do not. Removing the five-letter designator shifts the pairs by one and, for SSKFV, the excess disappears. The 1735 alignment's clumps are not tighter than a random set of 33 hits. See `docs/logs/ts-bigram-phase-2026-10-04.md`. Do not call that a square or a reading.

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

Several Enigma entries in the old unbroken overview are now marked Broken in newer sources. The [master list, status 30 September 2026](https://cryptocellar.org/bgac/1941-msg-list.html), credits WEUWY Nr. 138 to Cécile Sakellis with Claude on 26 September; it is already solved material. Its corrected indicator and Nr. 140 stop reproduce under the published July key, with residual garbles and no complete independent plaintext control. [Source hashes and controls](logs/enigma-open-target-2026-10-03.md) record the conflict. RXPSB remains unmarked Broken and has 105 known body letters plus two gaps, with header and transcription lengths conflicting. No applicable 28 June daily key was found; nearby solved Nr. 51 explicitly uses 27 June. The newer Enigma start-search helper preserves and advances gaps, but still needs supplied daily settings and aligned cribs.

Archival records labeled non-decrypted can have keys, deciphered siblings, contemporary plaintexts, or newer public readings elsewhere. Check those before spending compute. Unknown scripts and short famous puzzles are not quick-win cipher targets merely because their input is small.

## Continuing to add methods

Condi and twelve further ACA gaps are now implemented and source-checked. Consult `docs/CATALOG.md` before adding another method. Read the actual source, transcribe literal known answers, and add a recovered-output SHA-256 certificate. Supplied-key helpers and conditional unknown-key inference remain separate. Do not substitute generated roundtrips for published known answers.

For real unsolved work, follow `docs/WORKFLOW.md`. Intake files and runtime downloads are ignored by default. Publish only deliberately reviewed case material. Failed or bounded negative results stay research logs, with declared models and bounds. The new K4 baseline crib fit is logged in `docs/logs/reverse-engineer-2026-10-03.md`; no plaintext is claimed.

## Preserve prior user constraints

- Skip Funkspruch Nr. 86. The user said it was solved and the paper was not released. Do not run new Nr. 86 searches. Existing failed logs remain evidence of their own bounded attempts.
- Do not claim a solve of Kryptos K4, Zodiac Z13/Z32, Beale 1/3, McCormick, the real D'Agapeyeff challenge, Voynich, Linear A, Indus, or rongorongo without a cited plaintext and independent evidence. A satisfying model or a bounded negative search is not a decipherment.
- Neural training stays inside the repo. The local `python3 -m engine train-router` runs one bounded residual-ensemble pass with explicit settings and a promotion gate. `--warm-start` starts from a compatible incumbent; `--learning-rate` sets the maximum cosine-schedule rate. The legacy grader remains available. Do not create a cron job, recurring routine, or wakeup. Binary, analysis, and puzzle certificates do not create language training examples. New router artifacts and actual benchmark metrics are documented in `docs/neural-upgrades.md`; the original legacy weights are preserved.
- Existing K4 search and ciphertext-error modules are already present. Do not recreate them or promote their negative results into a solve.
- Do not reintroduce unrelated project credits.
- Preserve `docs/assets/readme-hero.jpg` exactly. It must remain a real nameless JPEG with magic `ff d8 ff`. Never rewrite it through a contents API.
- Commit as Chase, email `326338179+ChaseHendrick@users.noreply.github.com`. Push using git. If rejected because main advanced, fetch and rebase before retrying.

## Validation and landing

Python 3.10+ is supported. Core routines use the standard library. Optional synthesis uses pinned Z3; OCR requires a local backend and its image-render test needs Pillow. Local executed checks used Python 3.12.14. Python 3.10 syntax was checked statically; actual 3.10 execution belongs to CI.

This checkout also has an ignored `.venv` created with the bundled Python 3.12 runtime and access to its existing Pillow/NumPy packages. Z3 5.1.0.0 is installed inside that venv. Activate it with `source .venv/bin/activate`, or invoke `.venv/bin/python` directly. See `docs/logs/continuation-2026-10-03.md` for the executed 747-test run and validation boundaries.

`.github/workflows/check.yml` runs a core Python 3.10 job with Pillow and NumPy, and an extended Python 3.12 job with Z3, Pillow, NumPy, Tesseract, and fonts. Each runs the suite and a demo in a temporary location. Exact symbolic tests are optional skips without Z3. The corrected prior run for commit4e2924f passed both jobs, including747 tests per job with13 optional skips on3.10 and no skips on3.12. This is evidence about the previous commit. Inspect new CI before claiming success for the solver expansion.

Run `python3 -m unittest discover -s tests -v`, and use `python3 -m engine demo --out /path/to/temporary-demo.md` for a fresh witness without committing timing churn. Report the actual test count, exit status, and any optional skips. Known-key decryption, synthetic recovery, OCR phrase recognition, exact conditional constraints, and historical decipherment are different validation scopes.

## Solver and inference expansion

The user's objective is to seek independently verifiable solutions to unresolved ciphers. They asked for continued solver additions, multiple training methods, reasoning and inference, and simulated thought/emotion with correctness and speed signals. The current requested classifier target is 480/480; report progress accurately and never memorize test ciphertexts or use their answers as training input. Reusing Doyle scores for development makes those fixed comparisons development benchmarks, not an untouched final generalization test. The Wells audit was evaluated after the earlier selection stage: 429/480 top one and 476/480 top three for the hashed format 5 artifact. Subsequent authorized training stages exclude Wells; this is an artifact-specific audit, not a globally untouched final claim. The saved format 5 model gets 428/480 and 477/480 on the fixed development cases and 193/204 on the earlier benchmark. Format 6, the local blend and format 7 were rejected. Source format 8 supports 148 features and warm starts. Its rate 0.01 warm trial scored 433/480 top one, 477 top three, 191/204 legacy; a later rate 0.0003 trial scored 432/480 top one, 476 top three, 191/204 legacy. Both were rejected without using Wells or retuning, leaving format 5 SHA d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825 unchanged. Formats 2 through 8 remain loadable. See docs/neural-upgrades.md and the saved audit/provenance. Mathematical cipher families can overlap, and current training generators do not represent every possible historical instance.

New helpers cover Baconian, Condi, Progressive Key, Periodic Gromark, Monome-Dinome, Morbit, Pollux, Numbered Key, Redefence, Sequence Transposition, Checkerboard, Homophonic and Interrupted Key. Wiener adds a documented weak-exponent RSA attack. Unknown-key methods include constrained Morse maps, bounded transposition ensembles, Condi dictionary/crib inference, Progressive Key parameter inference, structured Homophonic row inference, supplied-reset Interrupted Key inference and plaintext-autokey primer inference. See the dated solver-expansion log for source and validation boundaries.

`engine.tool_registry` connects allowlisted helpers and searches through `python3 -m engine tools` and `python3 -m engine run TOOL --params JSON`. The investigation ledger shares a search budget, records premises/results/contradictions/next actions, and treats neural rankings as advice. Simulated affect is transparent display telemetry. No independent checked evidence means correctness and happiness remain unknown. Worse benchmark models are rejected; a separate independently checked-case policy can suggest retirement or demotion.

Workflow1.1 adds `python3 -m engine.case_workflow investigate CASE` with confirmed training cribs only, source/solver hashes and exact model snapshots when neural advice is used. Heldout evidence and expected plaintext hashes are excluded from fitting. Case status stays unsolved until independently reviewed evidence supports a public claim. The new command records candidates without making that claim itself.
