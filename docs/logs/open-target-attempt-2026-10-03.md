# K4 attempt with separate crib validation, 3 October 2026

**No new reading was recovered.** This run completed 30,968 target checks across two reciprocal crib folds. The small Condi dictionary and pure transposition portfolio produced no fitted candidates. Every fully determined Progressive Key candidate failed the withheld phrase. Some partial keys remain underdetermined; they are not evidence of a recovered plaintext.

The complete machine-readable record is [open-target-attempt-2026-10-03.json](open-target-attempt-2026-10-03.json). It stores exact inputs, bounds, checks, all compatible candidates with unknown positions retained, withheld comparisons, source observations, code/data hashes, runtime and Git state. `claimed_plaintext` is null, `new_verified_plaintext` is false, and status is `not_solved`.

## Source check and status boundary

The live [CIA headquarters page](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/) prints a K4 tail that exactly matches the repository's 97-letter fixture. Its broad unbroken-status wording has no recent timestamp and is not treated as proof about current worldwide knowledge. The independently checked [participant transcription](https://www.elonka.com/kryptos/transcript.html) matches the same tail; the [participant clue page](https://www.elonka.com/kryptos/) records Sanborn's clue disclosures and aligned mask. Its global-status line explicitly says August 2025.

The first-party [RR Auction sale record](https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/), dated 21 November 2025, says the transferred archive included K4's plaintext and original coding system. It does not print that full text or method. The artist's main page was unavailable to the web tool during this check. This report therefore describes a **public cryptanalytic recovery attempt**, acknowledging private archival knowledge, rather than claiming that nobody knows the plaintext or that worldwide unsolved status has been verified.

The literal input, without the question mark ending K3, is:

```text
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

Its ASCII SHA-256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`. The published coordinates checked against this string are NORTHEAST at one-based positions 26 through 34, corresponding to `QQPRNGKSS`, and BERLINCLOCK at positions 64 through 74, corresponding to `NYPVTTMZFPK`. APIs use zero-based plaintext offsets 25 and 63.

## Frozen hypotheses and validation rule

The first fold fits only BERLINCLOCK and reserves NORTHEAST. The second fits only NORTHEAST and reserves BERLINCLOCK. Both folds use identical bounds and dictionary guesses. EAST is neither fitted nor used to filter results. No full K4 plaintext, private key, purported solution text or clock-derived keystream enters the run.

- [Progressive Key inference](../progressive-key.md): periods 1 through 32, all 26 progression values, zero initial progression, 832 setting checks and up to 1,000 retained candidates. Keyword slots forced by the training crib remain unknown elsewhere. This is the straight-alphabet Vigenere variant.
- [Condi inference](../condi.md): 20 explicitly guessed keywords, all 26 alphabet shifts and all 26 initial offsets, 13,520 setting checks and up to 1,000 retained candidates. The guesses are `KRYPTOS`, `PALIMPSEST`, `ABSCISSA`, `SANBORN`, `SCHEIDT`, `LANGLEY`, `INTELLIGENCE`, `GATHERING`, `SHADOW`, `MAGNETISM`, `COPPER`, `GRANITE`, `QUARTZ`, `LODESTONE`, `COMPASS`, `VIGENERE`, `MATRIX`, `SECRET`, `LUCID` and `INVISIBLE`. These are unendorsed hypotheses inspired by public sculpture context/materials and K1-K3 keywords. Neither reserved phrase nor its component clue words are in this list. This is not a search over all keyword alphabets.
- [Transposition portfolio](../transposition-ensemble.md): a 5,000-check cap, widths through 32, rails through 5 and up to 100 retained candidates, with forward transformation checks. Because 97 is prime, no complete rectangle width 2 through 32 divides the input. Route and columnar families therefore have zero eligible settings. Four rail-fence keys and 1,128 Redefence keys give 1,132 actual checks per fold.

A determined letter disagreeing with the withheld phrase rejects that setting, even when other withheld letters are unknown. A full withheld prediction requires every letter to be determined and correct. A compatible `?` is never counted as a match, and withheld evidence never completes a key. Candidate storage did not hit its cap. All setting searches finished within their declared bounds; no run is mislabeled as a timeout or check exhaustion.

## Actual results

| Fitted phrase | Tool | Checks | Compatible settings | Withheld exact predictions | Withheld contradictions | Withheld undetermined |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| BERLINCLOCK | Progressive Key | 832 | 573 | 0 | 442 | 131 |
| BERLINCLOCK | Condi | 13,520 | 0 | 0 | 0 | 0 |
| BERLINCLOCK | Transposition portfolio | 1,132 | 0 | 0 | 0 | 0 |
| NORTHEAST | Progressive Key | 832 | 626 | 0 | 495 | 131 |
| NORTHEAST | Condi | 13,520 | 0 | 0 | 0 | 0 |
| NORTHEAST | Transposition portfolio | 1,132 | 0 | 0 | 0 | 0 |

The first Progressive Key fold has 27 fully determined keys; the second has 28. All fail their withheld phrase. Among each fold's 131 undetermined settings, 130 predict **zero** withheld letters. They have periods 25 through 29, with free key slots covering the reserved interval. The remaining setting, period 30 and progression 13, predicts only one matching withheld letter: `????????T` in the first fold and `B??????????` in the second. Those single-letter coincidences do not provide a full withheld prediction or a useful new reading.

The 131 settings are therefore underconstrained alternatives, not verified leads. The completed Progressive Key setting enumeration does not enumerate or identify every completion of a partially known keyword. Condi and transposition results reject only the explicitly tested dictionary and families. They do not reject other alphabets, nonrectangular arrangements, arbitrary column permutations, unknown padding/nulls, combined cipher layers or clock-related mechanisms.

## Controls and reproducibility

Before testing K4, the same APIs passed three frozen constructed certificate controls, with no selected key or expected plaintext passed into inference:

- Progressive Key: 208 setting checks, one candidate, 16 fitted letters and 51 additional predicted letters, actual recovered hash matching the recorded fixture.
- Condi: 2,028 checks, one candidate from the explicit three-word dictionary, 15 fitted letters and 44 additional predicted letters, actual recovered hash matching the recorded fixture.
- Transposition portfolio: 1,136 checks, no crib or key, top recovered harbor-prose hash matching the recorded fixture.

The run performed 3,372 control checks plus 30,968 target checks and took 1.353 seconds locally, including controls. Check units differ by tool, and local elapsed time is not a performance guarantee. Python was 3.12.14. The JSON records Git state and SHA-256 for the actual helper modules, their transformation dependencies, the English scoring corpus and the execution script. All code/data hashes remained identical before and after the run.

The relevant calls can be reproduced from the JSON inputs using `infer_progressive_key(ciphertext, cribs=training_cribs, max_period=32, progressions=tuple(range(26)), max_checks=832, max_candidates=1000)`, `infer_condi(ciphertext, keywords=the_recorded_guesses, cribs=training_cribs, max_checks=13520, max_candidates=1000)` and `search_transposition_ensemble(ciphertext, cribs=training_cribs, max_checks=5000, max_candidates=100, max_width=32, max_rails=5)`. Evaluate the reserved span only after each report returns, preserving `?` rather than inventing letters.

This is a negative or underdetermined bounded experiment, not an incomplete execution and not a historical solve. Nr. 86 was excluded. The next useful step would require a separately justified model or additional independent evidence; raising these same caps would not resolve the free keyword slots or supply the missing mechanism.
