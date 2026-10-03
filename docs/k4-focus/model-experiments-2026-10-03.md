# K4 conditional composition experiment, 3 October 2026

**No new reading was recovered.** This experiment used exactly 10,000 model checks including controls. None of the 9,832 K4 hypotheses tested fully predicted its reserved clue. All 163 hypotheses with complete inferred keys failed that independent clue-position check. Another 356 partial hypotheses remain underdetermined across the reciprocal folds. The requested portfolio was not exhausted.

The [machine-readable record](model-experiments-2026-10-03.json) contains literal inputs, controls and recovered-output SHA-256 certificates, exact coverage counters, retained witnesses, reserved comparisons, code hashes, runtime and the complete reproduction script. `claimed_plaintext` is null and `new_verified_plaintext` is false. A source-matched clue prediction would still require a complete mechanism and independent verification before claiming historical recovery.

## Evidence and new coverage

The frozen ciphertext is the same 97-letter input in the [earlier bounded run](../logs/open-target-attempt-2026-10-03.md), checked against the [CIA transcription](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/) and [participant transcription](https://www.elonka.com/kryptos/transcript.html). Its ASCII SHA-256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. The [participant clue page](https://www.elonka.com/kryptos/) supplies the aligned artist-disclosure mask. In zero-based original plaintext coordinates:

| Clue group | Offset | Length | Original ciphertext span |
| --- | ---: | ---: | --- |
| EASTNORTHEAST | 21 | 13 | FLRVQQPRNGKSS |
| BERLINCLOCK | 63 | 11 | NYPVTTMZFPK |

The first fold fits EASTNORTHEAST and reserves BERLINCLOCK. The second reverses their roles. EAST was not used in the earlier run. Neither reserved group enters inference, key completion, ranking or witness selection in its fold. These are heldout disclosed positions, not an independently acquired full historical plaintext.

The [2025 first-party auction account](https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/) describes a private archive containing the plaintext and coding system. This experiment neither inspected nor independently verified those underlying contents. It seeks a public cryptanalytic recovery and makes no assertion that nobody knows K4's plaintext.

The previous portfolio tested direct Progressive Key and a finite Condi dictionary. Its pure transposition search required complete rectangles, so prime-length 97 excluded columnar widths 2 through 32. The [later affine composition attempt](../logs/tractable-open-attempt-2026-10-03.md) sampled reversal/rotation followed by affine substitution. The new helper adds ragged columnar layouts composed with periodic or autokey substitution, in either order. Some direct identity hypotheses overlap earlier coverage; they are controls within this portfolio, not wholly new mechanisms.

The existing [symbolic synthesis engine](../cipher-synthesis.md) already models ragged left-to-right columnar transposition before Vigenere/Beaufort and includes broader unknown Quagmire alphabets. Those models overlap this implementation. The additional helper scope is plaintext/ciphertext-autokey propagation, substitution before transposition, right-to-left column orders, explicit fixed-alphabet assumptions, and dependency-free exact algebra. The new K4 experiment extends the dated runs; it does not claim that composition, ragged layouts or these classical algorithms are novel.

## Exact model definitions and bounds

The new `engine.k4_models.search_k4_models` function is a repository-specific constraint tester, not a discovered Sanborn construction. It assumes one of two explicitly fixed alphabets: A-Z or `KRYPTOSABCDEFGHIJLMNQUVWXZ`. Indices are 0 through 25 with alphabet origin zero. Reported keys are modular shift indices, not claimed artist keywords or indicator letters. K1/K2 usage does not establish K4 usage.

With all arithmetic modulo 26, the substitution families are listed below. `P` and `C` refer to the substitution-stage streams. When a transposition acts first, its permuted plaintext positions also determine the key period positions.

- Repeating: `C[i] = P[i] + K[i mod L]`, following the [ACA Vigenere definition](https://www.cryptogram.org/downloads/aca.info/ciphers/Vigenere.pdf).
- Beaufort: `C[i] = K[i mod L] - P[i]`, following the [ACA Beaufort definition](https://www.cryptogram.org/downloads/aca.info/ciphers/Beaufort.pdf).
- Plaintext-autokey: primer shifts for the first `L` positions, then `C[i] = P[i] + P[i-L]`, following the [ACA Autokey definition](https://www.cryptogram.org/downloads/aca.info/ciphers/Autokey.pdf).
- Ciphertext-autokey: primer shifts first, then `C[i] = P[i] + C[i-L]`. This explicitly declared recurrence has a constructed control here; the ACA plaintext-autokey source is not represented as publishing this variant.

For every family, `L` ranges from 1 through 32. Layouts are identity, reversal, or writing rows of width 2 through 32 and reading columns top to bottom, from left to right or right to left. Short final rows keep their actual column lengths. No padding or letters are inserted. All 64 distinct layouts preserve the complete input.

Substitution can precede transposition or follow it. Cribs always retain original plaintext coordinates. Identity's two equivalent orderings are tested once. This defines 32,512 layout/family/alphabet/order/period hypotheses per fold. A check fits one such hypothesis algebraically, not one guessed key completion. Seed domains are propagated exactly; unconstrained key slots stay `null`, and plaintext positions stay `?`.

Round robin across the 16 family/alphabet/order streams prevents one family consuming the budget. A diagonal layout/period schedule exposes every requested width and period early. Each fold tested 4,916 hypotheses; stream counts differ by at most one. Every width, period, alphabet, family and order received sampled coverage. This does not complete every combination: 27,596 requested hypotheses remain untested per fold.

No language scoring, neural advice, randomness, learned parameters, full proposed plaintext, dictionary, clock-derived keystream, transcription errors, null removal or unknown alphabet search enters this experiment. The finite alphabet/layout assumptions are not artist-endorsed evidence.

## Actual results

| Fitted group | Checks | Rejected on fitting clue | Compatible models | Complete keys | Reserved contradictions | Reserved underdetermined | Reserved exact predictions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EASTNORTHEAST | 4,916 | 3,582 | 1,334 | 77 | 1,159 | 175 | 0 |
| BERLINCLOCK | 4,916 | 3,296 | 1,620 | 86 | 1,439 | 181 | 0 |

Any determined mismatch rejects that hypothesis. Unknown positions are never matches. Every complete-key hypothesis failed the reserved group. The partial survivors neither contradict nor fully predict it; free key slots leave alternatives rather than recovered text. Completing those slots from the reserved letters would change the experiment and invalidate that group's heldout role.

The temporary retention limit was 10,000, greater than each fold's possible accepted count, so every compatible tested hypothesis received reserved evaluation. The JSON saves at most ten witnesses per fold: the first five complete-key and first five partial-key hypotheses in the fitting-only stable ranking. This rule was fixed before reserved evaluation. Rankings use forced-position count and model labels, never English plausibility or withheld matches. Partial witnesses report verified forced equations and `re_encryption_matches: null`; only complete keys receive a whole-ciphertext forward replay. Replay establishes transform consistency, not historical truth.

Both folds stopped at `check_limit`; `search_complete` is false. Completed model enumeration would still not enumerate every free key completion or establish a unique historical interpretation.

## Controls, regression and reproduction

Four frozen constructed controls use a 97-letter prefix of the repository's harbor prose. They cover ragged repeating substitution, keyed-alphabet plaintext-autokey, transposition before Beaufort, and ragged ciphertext-autokey. Each searches periods 1 through 3 and widths through 7, fits only the first 21 plaintext letters, and receives neither the selected key nor the complete expected plaintext. Each recovered the complete literal fixture and its recorded output SHA-256. A separately implemented arithmetic/layout oracle reproduces the frozen ciphertext. They are constructed controls, not published historical solves.

Each control completed 42 model checks, for 168 total. The remaining 9,832 checks were divided equally between the K4 folds. Total recorded model checks were exactly 10,000. The complete local run took 1.799 seconds; this is a measured run, not a speed guarantee. Each stream contains at most 512 letters. Fitting makes several linear passes and complete keys additionally receive a full forward replay; a hypothesis is not a unit of equal computational cost across all tools.

The new test file first failed with `ModuleNotFoundError: engine.k4_models`. After implementation, `.venv/bin/python -m unittest tests.test_k4_models` passed 11 tests. The focused compatibility command `.venv/bin/python -m unittest tests.test_k4_models tests.test_autokey_inference tests.test_reverse_engineer` passed 33 tests in 0.920 seconds. Tests include literal hidden-key recovery, both composition orders, both column directions, an independent oracle across randomized constructed controls, exact budget fairness, partial-key ambiguity, contradiction handling and invalid input rejection. The random-control seed is 730; the target experiment uses no RNG.

The JSON embeds the execution script. Its K4 calls use `search_k4_models(ciphertext, cribs=(fitted_group,), max_checks=4916, max_period=32, max_width=32, max_candidates=10000)`, followed by a separate reserved-span comparison over all returned hypotheses. Source hashes were unchanged during execution. The helper does not read a historical plaintext reference, weights or corpus. Nr. 86 is outside this work.

The useful result is a reproducible bounded rejection and an explicit set of unresolved constraints. Further work should predeclare a materially justified construction or finish a chosen finite model space with fresh verification evidence. This run does not reject untested combinations, other alphabets, arbitrary column permutations, additional layers, altered clue coordinates, running keys or other mechanisms.
