# Open-target source gate and K4 composition attempt, 3 October 2026

**No new reading was recovered.** Five short Enigma targets remain highlighted as open in the publisher's current master list, but none had an applicable daily key in the checked sources. The new Hallucinogens composition search then tested 5,000 hypotheses in each of two K4 clue folds. Both returned zero candidates and stopped at the check limit.

The [machine-readable record](tractable-open-attempt-2026-10-03.json) contains literal inputs, source byte hashes and retrieval dates, known-key control outputs, complete bounded-search reports, separate heldout checks, code/data hashes and the execution script. `claimed_plaintext` remains null and `new_verified_plaintext` is false. This attempt adds no historical solve.

## Enigma eligibility

The first-party [1941 master list](https://cryptocellar.org/bgac/1941-msg-list.html), dated 30 September 2026, highlights EHSTQ, RXPSB, KLJBO, LXACA and JBIYH without a Broken label. That dated source supports their open status within this collection. It does not establish that no independent researcher has unpublished results.

| Target | Body size | Required evidence still missing |
| --- | ---: | --- |
| LXACA, Nr. 100 | 20 letters | Applicable July 4 key and a solved sibling on that key. |
| KLJBO, Nr. 87 | 50 slots, four missing letters | July 3 key and a solved sibling on that key. |
| JBIYH, Nr. 242 | 55 letters | July 20 key and a solved sibling on that key. |
| EHSTQ, Nr. 3 | 52 letters in the master list | June 22 key and a solved sibling on that key. |
| RXPSB, Nr. 53 | 109 slots listed, 107 transcribed | Applicable date/network key and reconciliation of the length discrepancy. |

The [July key table](https://cryptocellar.org/bgac/e-keys-july-1941.html), updated 28 September 2026, has no July 3, July 4 or July 20 entry. It explicitly says LXACA probably belongs to July 4, despite reception on July 5, and fails the July 5 key. The [June through October table](https://cryptocellar.org/bgac/e-keys-jun-oct-1941.html) lacks June 22 and June 28 settings. The checked [author supplement](https://cryptocellar.org/enigma/enigma-modern-breaking.html) supplied no applicable replacement. These are absences in the consulted sources, not assertions about every archive.

The [July message page](https://cryptocellar.org/bgac/g-army-july-1941.html) gives LXACA's 23:40 preparation time and 04:45 reception time, JBIYH's July 20 header, and KLJBO's July 3 header. The master list labels nearby solved July 3 and July 4 records TS hand cipher, so those records do not validate Enigma settings.

The [LXACA](https://cryptocellar.org/bgac/spruch/05071941-100-in.pdf), [JBIYH](https://cryptocellar.org/bgac/spruch/20071941-242-in.pdf) and [KLJBO](https://cryptocellar.org/bgac/spruch/03071941-087-in.pdf) facsimiles were visually inspected. An unclear handwritten annotation under LXACA was left uninterpreted. It was not promoted into a start position or plaintext clue. KLJBO's four lost body letters remain unknown at zero-based offsets 33, 40, 44 and 46. No replacement letters were inserted.

The [earlier RXPSB audit](enigma-open-target-2026-10-03.md) records two explicit gaps and the length conflict. Its nearby same-call-sign Nr. 51 is explicitly enciphered on June 27 despite reception on June 28. That cannot establish RXPSB's enciphering date or key. WEUWY is already solved in the current master list and was excluded, as was Nr. 86.

## Reproduced key controls

Before rejecting a July 5 transfer to LXACA, the implementation reproduced two published controls with reflector B, left-to-right rotors III/V/IV, rings WHJ and plugs `BI CW EQ FX HZ JN KY MT OV PR`:

| Control | Indicator decoded | Start | Body letters | Final windows |
| --- | --- | --- | ---: | --- |
| Nr. 99, XTMSY | QCB: NSR | SIM | 156 | SOM |
| Nr. 101, DEROP | AIK: SUD | WER | 178 | WLN |

Both starts and stops match the key table. A separate arithmetic oracle agrees with both complete raw body outputs, and full forward replay reproduces each original ciphertext. The raw outputs contain garbles and were not edited into smoother German. No independently published complete plaintext reference was found in the checked pages, so these are indicator/stop and transformation controls, not full plaintext verification.

Under July 5 settings, LXACA's OGD: PKN indicator yields LXI in both implementations. Any supplied key can decode an indicator to three letters; that observation does not validate the key's applicability. The publisher's date warning still rejects this transfer. There were seven engine process calls, seven arithmetic-oracle comparisons, and **zero unknown-start searches on open Enigma targets**. No arbitrary default settings or guessed German crib were used.

## Actual K4 hypothesis search

The live [CIA transcription](https://www.cia.gov/legacy/headquarters/kryptos-sculpture/) and [participant transcription](https://www.elonka.com/kryptos/transcript.html) match the literal 97-letter K4 input in the JSON. Its ASCII SHA-256 is `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`.

The [participant clue page](https://www.elonka.com/kryptos/) records Sanborn's NORTHEAST and BERLINCLOCK disclosures and aligned locations. The API uses zero-based offsets 25 and 63. Its broad status statement is dated August 2025. The first-party [RR Auction record](https://content.rrauction.com/jim-sanborns-complete-kryptos-archive-sells-for-962500-at-auction/), dated 21 November 2025, reports transfer of a private archive containing K4 plaintext and its coding system. Neither full text nor mechanism was obtained from these pages. This is a public cryptanalytic recovery attempt, acknowledging private archival knowledge, not a verified claim that nobody knows the plaintext.

The frozen model was `plaintext = affine_inverse(permutation(ciphertext))`. The permutation is identity, reversal, or a left rotation by 1 through 32. Each permutation has 312 invertible affine keys, giving 34 permutations and 10,608 requested pairs per fold. These are explicit repository hypotheses, not artist-endorsed mechanisms.

The [Hallucinogens solver](../persona-hallucinogens-solver.md) interleaves permutations under one 5,000-check budget and retains at most 20 candidates. It preserves original plaintext crib coordinates and must forward-replay every accepted candidate to the original ciphertext. English scoring can rank candidates but cannot establish correctness.

| Fitted clue | Reserved clue | Checks | Fitted candidates | Reserved candidates examined | Completed requested model? |
| --- | --- | ---: | ---: | ---: | --- |
| NORTHEAST, offset 25 | BERLINCLOCK, offset 63 | 5,000 | 0 | 0 | No |
| BERLINCLOCK, offset 63 | NORTHEAST, offset 25 | 5,000 | 0 | 0 | No |

Only the fitted clue entered each search. The reserved clue was compared after candidate generation; with no candidate returned, there was nothing to validate. EAST was neither fitted nor used as a filter. Each fold rejected all 5,000 tested pairs on its fitted clue and left 5,608 requested pairs untested. Transform check counts differed by at most one, so the cap did not consume only the identity model. Zero recorded forward mismatches reflects zero accepted candidates, not a new plaintext proof.

The recorded folds took approximately 0.288 and 0.099 seconds locally; the complete recorded execution took 0.403 seconds. A preliminary identical two-fold smoke also ran 10,000 checks and returned zero candidates. Thus 20,000 checks were executed in this task, but repeated smoke checks add no model coverage beyond the recorded 10,000. Local timing is not a performance guarantee.

## Checks and next evidence

The focused command `.venv/bin/python -m unittest tests.test_persona_hallucinogens_solver tests.test_persona_preferences tests.test_enigma_crib_search tests.test_enigma` passed 30 tests in 0.872 seconds. All 13 primary source snapshots were hashed. The inspected code/data hashes were unchanged during the recorded run. JSON, source-hash, input-length, gap-coordinate, budget and heldout-separation checks passed.

Reproduce each K4 fold with `investigate_hallucinogens(ciphertext, cribs=(Crib(offset, phrase),), max_checks=5000, max_candidates=20, max_rotations=32)` using the literal JSON input, then evaluate the other phrase separately. The JSON includes the exact execution script and settings for the Enigma controls.

An Enigma start search next requires an applicable daily key plus independently solved same-network evidence, and damaged inputs still require transcription reconciliation. K4 next requires a separately justified mechanism or explicit completion of the remaining bounded pairs. This attempt produced no candidate, no new clue and no independently verified reading.
