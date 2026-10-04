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

`engine.headless_enigma` reports the stop window and re-enciphers. Full Nr. 101 stops at `WLN`. Nr. 99 starts at `SIM` and stops at `SOM`. KLJBO, LXACA, and JBIYH still do not beat the control on the six published keys, and every row re-enciphers. See `docs/logs/headless-enigma-2026-10-04.md`. Do not describe a stop window as a reading.

`engine.headless_truppenschluessel` re-seals every intact pair. A hole spoils only its own pair. The six residue messages still have no printed squares and were not opened. The lock oracles were left as yes-or-no machines. See `docs/logs/headless-truppenschluessel-2026-10-04.md`. Do not invent a square and call the output a reading.

The next swarm stayed inside the Truppenschlüssel residue and did not search a square. IASRZ Nr. 129 and 130 share the prefix `IASRZEDSTB`, and the bodies are odd once the designator is removed. DSZPZ and DEZPS, both headed 1735, align at 33 letters against a 20-draw null maximum of 15. SSKFV and HOHOX share the suffix `LMOTIYIZ`. See `docs/logs/ts-close-pairs-2026-10-04.md`. Do not describe that agreement as a reading.

A follow-up climb on the even windows, including one-letter endpoint drops, beat a shuffled control on all 7 windows. Both endpoint drops beat it, so the Grimm trigram scorer is not choosing a text. No plaintext was stored. See `docs/logs/ts-pair-climb-2026-10-04.md`. Do not promote those scores to a key.

The pair grid is a separate check. Pairs that start on the first printed letter repeat about as often as the Grimm sample in the longer messages, and random letters of that length do not. Removing the five-letter designator shifts the pairs by one and, for SSKFV, the excess disappears. The 1735 alignment's clumps are not tighter than a random set of 33 hits. See `docs/logs/ts-bigram-phase-2026-10-04.md`. Do not call that a square or a reading.

Read the residue as clerk work, not as a cleverer cipher. Station 4fc reused IASRZ and the next group `EDSTB`. Station f8y reused the closing `LMOTIYIZ` and not the opening. The two 1735 messages agree in 33 letters, differ in 20, and have 4 gaps, so they are not one transmission copied twice. Their first 10 body letters agree in 8. Dropping any one of HOHOX's 11 groups leaves only 1 or 2 repeated pairs, which random letters also reach. See `docs/logs/ts-clerk-2026-10-04.md`. Do not promote a habit into plaintext.

`engine.ts_isolog` slides twelve formulae along the pair grid. A window survives only when repeated pairs match in both directions. Formulae that never repeat a pair survive almost everywhere and are not evidence. `UNTERKUNFT` repeats its first and fourth pairs and fits only offsets 40, 60, and 64 on IASRZ Nr. 129. The same shape would fit any other formula, and the sister message has no window. Joint agreements between the two IASRZ messages are 0. A planted control is found. See `docs/logs/ts-isolog-2026-10-04.md`. Do not read those offsets as the word.

Bob's format 5 file is still the incumbent. A 128-row manifest, seed 20261005, 32 draws per family, scores 39/64 top one on the old Enigma and M-209 settings and 34/64 on the broad settings. Misses are almost all the other machine cipher. The weight SHA is unchanged. See `docs/bob-probe-manifest-2026-10-04.md`. Do not promote this probe to a weight update.

`engine.pooled_substitution` is the separate one-to-one substitution constraint from the Bob research note. It is not a Transformer and it does not touch Bob. On IASRZ Nr. 129 and on K4, a key that is allowed to collapse letters outscores the legal permutation under both English and Grimm quadgrams. K4 under Grimm does not beat a shuffle. See `docs/logs/pooled-substitution-2026-10-04.md`. Do not describe those scores as plaintext.

`engine.pen_pressure` reads only a supplied heavy/light channel or supplied pinprick positions. Bacon's a-form is light and the b-form is heavy. Ink with no pressure record returns no text. See `docs/logs/pen-pressure-2026-10-04.md`. Do not infer a hidden meaning from a transcription.

`engine.dagapeyeff_swarm` is the non-German, non-K4 swarm. The 1939 challenge is 196 Polybius cells in a 14 by 14 grid. The book's own example is only 89 cells, so its chi-square is a direction. Against 2,000 English strings of 196 letters, none is as flat and none uses as few distinct letters. One best cell change leaves it outside that range. It takes 4 changes to enter the range and 14 to reach the median. See `docs/logs/dagapeyeff-swarm-2026-10-04.md`. Do not keep those changed cells or treat the grid as a reading.

`engine.dagapeyeff_more` continues that swarm. 200 workers share 2,457 alphabet shapes. The friendliest is Italian with M and U merged, score 14.05, and 0 of 200 English texts given the same menu are that bad. Reversing the last three digits of each group is the only other order that stays on the square, and it fails the book's solved example. Do not adopt it as plaintext.

The man is not the 1969 or 2003 namesake. London Gazette: oath 17 March 1947, died 22 March 1955 at Maugersbury Manor, Wing Commander, service number 87808, dismissed by court martial 18 January 1949. The "he forgot" line is not a quote from him. See `docs/logs/dagapeyeff-life-2026-10-04.md`.

`engine.dagapeyeff_life.search_life` reads `engine/data/dagapeyeff_life.json`. Ask it for `87808`, `Rachel`, or `1969`. Names from 1939 and numbers from his life were tried as keys and lost to random keys of the same size. Do not store a string from that test.

`engine.dagapeyeff_nulls` tries the book's dummy-letter rule at every period from 2 to 31. 495 workers agree the best is still flat (11.33 against an English cherry-pick median of 3.61). Deleting digits never stays on the square. Not a reading.

`engine.dagapeyeff_rule` changes the order of work. A worker writes the prediction first: a dummy every third, fourth, or fifth cell would be one symbol. None of the 12 residues is. 214 of 400 shuffles are as narrow. The solved example is not a filler either. He did not use that rule. The 196 cells are the cipher. Do not delete them and call the remainder a reading.

`engine.dagapeyeff_column` checks the column other people marked. All 3 symbols that appear once, and all 5 cells of symbols that appear at most twice, sit in column 14. Seven legal pairs are absent, not three: 61, 73, 95, 01, 02, 03, 05. Deleting column 14 is the worst of the 14 columns (45.57). Do not adopt a published letter string. See `docs/logs/dagapeyeff-others-2026-10-04.md`.

`engine.dagapeyeff_methods` ranks measurements on 37,000 trials. The rare-column search still fires after it is allowed to shop widths (0 of 10,000). Full-length letter counts still reject English (0 of 10,000, while the solved example scores 4.14). Printed-order digrams, either half alone, and symbol spacing do not. A 10,000-draw English maximum is 32.65 against the challenge's 34.23, so the gap is small. Do not store a letter string. See `docs/logs/dagapeyeff-methods-2026-10-04.md`.

`engine.dagapeyeff_reads` tries 10,000 column keys and digit reads at widths 2 through 28. No key stands out of its own draw. Even widths destroy the square. Width 3 is the only read that stays legal, and its better score (11.73) loses to random ungluing (7,473 of 10,000). The flatness is in the original pairs. Do not store a letter string. See `docs/logs/dagapeyeff-reads-2026-10-04.md`.

`engine.dagapeyeff_add` tries every period-2 and period-3 shift on the square, 666,450 evaluations. The friendliest period-3 key makes the counts look English (2.80) and a shuffled cipher does too. Its word score stays at -3.5039, with prose at -2.5185. Not a solution. Do not store a letter string. See `docs/logs/dagapeyeff-add-2026-10-04.md`.

`engine.dagapeyeff_languages` does not assume English. French, German, Spanish, Italian, Portuguese, Dutch, and folded Esperanto are each scored against text drawn from that language. French is closest at 21.36 and still only 2 of 2,000 French draws are that flat. The solved English exercise is accepted as English and rejected as Italian. Not a reading. See `docs/logs/dagapeyeff-languages-2026-10-04.md`.

`engine.dagapeyeff_frames` uses no letter table. Even places are exactly the digits 06789. Odd places are exactly 12345 except index 393, a 0. 0 of 20,000 shuffles are that clean. Dropping the last three zeros as filler is stronger than the digits require: only the middle one is on the wrong side. Adjacent pairs are not more predictable than a shuffle (16,611 of 20,000). Do not store a letter string. See `docs/logs/dagapeyeff-frames-2026-10-04.md`.

`engine.dagapeyeff_order` reorders the 196 cells. Relabeling cannot raise successive-symbol dependence: an English passage scores 1.0658 before and after a letter shift. The best of 20,000 column keys scores 0.7657, about the same as the best of 5,000 random orders (0.7556), and below same-length English (1.0658) and German (1.2000). A substitution of these orders is not a reading. Do not store a letter string. See `docs/logs/dagapeyeff-order-2026-10-04.md`.

`engine.dagapeyeff_routes` tries rails, diagonals, and regular deletions. Deleting every other cell scores 1.0556, close to English of length 196, but English of the remaining 98 cells scores 1.2922. 963 of 10,000 shuffled deletions match it. The rise is the shorter text. Do not store a letter string. See `docs/logs/dagapeyeff-routes-2026-10-04.md`.

`engine.dagapeyeff_glue` separates the two digits. Neither stream has an order of its own (row predictability is beaten by 15,767 of 20,000 shuffles). The pairing does: score 77.36, 0 of 20,000 re-pairings. Cell 91 appears 12 times against about 3 from the totals. The unevenness is which digits share a cell, not the sequence. Do not store a letter string. See `docs/logs/dagapeyeff-glue-2026-10-04.md`.

`engine.solvers.substitution` now records an order gate. `reading` is false when a shuffle of the ciphertext is at least as dependent, because renaming symbols cannot fix that. A known English substitution still passes (0 of 200). The 1939 pairs fail (170 of 200). `engine.dagapeyeff_split` cuts cells 91, 75, and 81 in two. The best cut scores 0.7002 against same-length English at 1.0658, and 15 of 20 shuffled cuts match it. Do not store a letter string. See `docs/logs/dagapeyeff-split-2026-10-04.md`.

`engine.dagapeyeff_battery` runs 1,000 pre-specified attacks against 500 order shuffles and 500 re-pairings, 1,000,000 scores. The only order hits are the rare-cell pile at widths 7, 14, and 28. Re-pair hits are the glue, including windows that only look special because re-pairing invents new cells. Lags, deletions, and repeating shifts do not hit. Do not store a letter string. See `docs/logs/dagapeyeff-battery-2026-10-04.md`.

`engine.dagapeyeff_symbols` separates one repeating cell from that pile. Cell 82 sits in one column six times, and 738 of 20,000 grids match when the luckiest cell is allowed to win. The five rare cells in one column are matched by 0 of 20,000. Their row bunch, once the column is given, is 100 of 2,002. Do not store a letter string. See `docs/logs/dagapeyeff-symbols-2026-10-04.md`.

`engine.dagapeyeff_battery` scores are unchanged after removing a duplicated tail count that never ran and rebuilding the scorer without per-attack dictionaries. `engine.dagapeyeff_check` asks whether the rare column is a check digit of its row. Thirty-three predictors. A planted sum scores 14/14. The real column scores 6, and every one of 20,000 shuffled columns also reaches 6. Do not store a letter string. See `docs/logs/dagapeyeff-check-2026-10-04.md`.

`engine.dagapeyeff_private` finds five symbols that never leave column 13: 92 (three times), 93 (twice), and 04, 71, 94 once each. That is 8 cells. 0 of 20,000 grids match. Their positions are also 6 mod 7, so a reported period of 7 is this column at half resolution, not a 7-letter key. Do not adopt an outside mapping of these cells onto codewords. Do not store a letter string. See `docs/logs/dagapeyeff-private-2026-10-04.md`.

`engine.dagapeyeff_strip` deletes those five symbols. The score falls from 0.5706 to 0.4174, against English of the remaining length at 1.0946. All 10,000 other eight-cell cuts and all 5,000 other symbol bundles of mass 8 stay higher. The private symbols are not filler. Do not store a letter string. See `docs/logs/dagapeyeff-strip-2026-10-04.md`.

`engine.dagapeyeff_bearing` deletes one column at a time. Only column 13 drops the score, from 0.5706 to 0.4514. The next worst column stays at 0.5655. 0 of 10,000 shuffled grids have a column that load-bearing. English of the remaining 182 cells is 1.1264. Do not store a letter string. See `docs/logs/dagapeyeff-bearing-2026-10-04.md`.

`engine.dagapeyeff_joins` splits that score across columns. Column 13's joins hold 0.1847, column 12 holds 0.1256, and column 0 holds 0.1226. Shares overlap on the boundary between columns. 0 of 10,000 shuffled grids have a column holding 0.1847. Do not store a letter string. See `docs/logs/dagapeyeff-joins-2026-10-04.md`.

`engine.dagapeyeff_outgoing` counts each pair once. The numbers then add to 0.5706. Column 13 is 0.0953 and column 12 is 0.0894, and 7 of 10,000 shuffled grids reach 0.0953. Of those two scores, 0.0839 and 0.077 are pairs that touch the private symbols. The seam is not a second pattern. Do not store a letter string. See `docs/logs/dagapeyeff-outgoing-2026-10-04.md`.

`engine.dagapeyeff_yardstick` is the line a reading has to clear. English at this length scores 1.0658, German 1.2, the cells 0.5706. Sorting scores 2.3931 and is not a reading. The index of coincidence is already 0.069702, so a cutoff of 0.06 is not the line. The book's solved square, in 8 flips, never rises above 0.5706. Do not store a letter string. See `docs/logs/dagapeyeff-yardstick-2026-10-04.md`.

`engine.dagapeyeff_balls` encloses those scores as a center and a radius. Thirty terms of the logarithm leave every radius under 10^-30. The cell ball sits entirely under English and under German. Column 13's once-counted share sits entirely above column 12, which sits entirely above the rest. Sorting still sits above English and is not a reading. Do not store a letter string. See `docs/logs/dagapeyeff-balls-2026-10-04.md`.

`engine.dagapeyeff_record` places the cells against a published chi-square of 49.23 and against 2,000 same-length English draws. The cells score 34.23, which is past that candidate and still 10.06 above the worst English draw. A legal group reversal scores 8.86 and fails the solved example. The order gap from 0.5706 to 1.0658 is unclosed. Do not convert his -692 onto this scale. Do not store a letter string. See `docs/logs/dagapeyeff-record-2026-10-04.md`.

`engine.dagapeyeff_provenance` hashes the cells, then the yardstick, the balls, the record, and the conversion. Floats are written with 17 significant digits. The chain ends at `bc1777b69a21801037a41ee2b4129edf6503014b813c26e4cc781f204482fe59`. A matching hash means those objects were recomputed. Do not treat it as a reading. Do not store a letter string. See `docs/logs/dagapeyeff-provenance-2026-10-04.md`.

`engine.dagapeyeff_convert` turns the published chi-square 49.23 into the ball from 49.225 to 49.235, and the published index 0.0697 into the ball from 0.06965 to 0.06975. The cells sit between 34.174639 and 34.292468, entirely under the first ball and entirely over the worst English draw. Their index, 0.069702, sits inside the published index ball. The score -692.13 has no formula and is not compared. Replacing cell 04 with 75 makes the chi-square ball worse. None of the 24 possible replacements reach English, and 0 of them improve on the cells. Do not store a letter string. See `docs/logs/dagapeyeff-convert-2026-10-04.md`.

`engine.dagapeyeff_edits` exhausts one and two count-moves. The best two-move ball reaches 27.557769, still above 24.165. A greedy path clears that line at four edits, with a ball high of 22.471061, and those cells are not kept. `engine.solvers.dagapeyeff` refuses a frequency claim with fewer than three moves, and it still marks a claim unsolved when the frequency line is cleared. Do not store a letter string. See `docs/logs/dagapeyeff-edits-2026-10-04.md`.

`engine.corrections` searches `engine/data/corrections.json` (schema `corrections-1`). Append a record when a later measurement contradicts an earlier claim. Do not edit an existing record. A subagent note is not a correction until that measurement is in the repo. A search hit is a retracted claim, not a reading. Do not store a letter string. See `docs/logs/corrections-2026-10-04.md`.

`engine.dagapeyeff_regroup` scores the one other legal grouping, `01432`. The chi-square ball runs from 8.8291 to 8.889665, under the worst English draw. The order score is 0.7801 against English 1.0658, and 2,216 of 10,000 shuffles match the downward read of 0.8735. The book's solved example moves from 4.14 to 21.56. `engine.solvers.dagapeyeff` refuses the regrouping. Do not store a letter string. See `docs/logs/dagapeyeff-regroup-2026-10-04.md`.

`engine.dagapeyeff_keys` scores 20,000 column orders of that regrouping. The best is 1.0033, under English at 1.0658. One shuffle sample of the same size topped out at 0.9925. Thirteen of twenty further samples reached 1.0033. `engine.solvers.dagapeyeff` refuses the key. Do not store a letter string. See `docs/logs/dagapeyeff-keys-2026-10-04.md`.

`engine.dagapeyeff_model` labels cells by English letter frequency and scores that string. English of this length scores -1.553 per quadgram. The printed cells score -3.6316 and the regrouping scores -3.6352, so the lower chi-square made the model score worse. Of 200,000 shuffles, 177,295 beat the printed cells and 151,728 beat the regrouping. The best shuffle reached -3.107. `engine.solvers.dagapeyeff` refuses the labeling. Do not store a letter string. See `docs/logs/dagapeyeff-model-2026-10-04.md`.

`engine.dagapeyeff_bifid` undoes a bifid on the coordinate digits for every period from 1 to 196. Period 1 scores -3.6316. The best period is 174, at -3.4727, against English at -1.553. Of 2,000 shuffles, 1,109 have a best period at least that high. That is 392,000 period scores. `engine.solvers.dagapeyeff` refuses the period. Do not store a letter string. See `docs/logs/dagapeyeff-bifid-2026-10-04.md`. The provenance chain ends at `052661154c4364a74c5deb984a1fc02c3ab2670f6e49d08855b1af3d8d1341c4`.

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
