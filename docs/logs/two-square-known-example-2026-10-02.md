# Two-square known example — 2026-10-02 (EDT)

Run after syncing to `origin/main` (`7b575c7` plus this change). This note records one passing recovery and one honest failure. It does not replace `docs/logs/two-square-2026-10-02.md`. That earlier Nr. 86 experiment stays a **failure**.

## Method

Single-stage two-square (Truppenschlüssel rules) in `engine/ciphers.py`: two 5×5 squares, J omitted, plaintext J written as I. First plaintext letter in the left square, second in the right. Different rows use the rectangle; the same row uses the right-hand neighbour. The ciphertext digraph is read from the right square first. Rectangle pairs from Ostwald & Weierud Fig. 6 (`KR→IN`, `NI→RK`, `QT→EU`, `UE→TQ`) stay checked in `tests/test_two_square.py`. Source for the rule: Ostwald and Weierud, “Modern Cryptanalysis of the Truppenschlüssel,” author PDF https://cryptocellar.org/pubs/mcts.pdf.

`solve_two_square` / `solve_two_square_keywords` builds every square from a word list and keeps the decrypt with the best English quadgram log-likelihood (`engine.language.get_model`). The caller does not pass the two squares. Raw English trigram counts are not the ranker: on a long synthetic text they can score a wrong pair above the real plaintext. `climb_two_square` is unchanged (English trigram shotgun hill-climb) and is not the passing path.

## Passing example (constructed here, not a wartime message)

Plaintext, J already absent, odd length padded with X (92 letters):

`THENIGHTWATCHWALKEDTHEEASTWALLTWICEANDCOUNTEDEVERYLAMPALONGTHERIVERROADBEFORETHEGATEWASSHUTX`

Keyword squares `FROST` / `MAPLE` via `square_from_keyword`. Ciphertext:

`MLFLOCNNWRAEIWFFOSFQORCTLQWRNTAZICCTSBGITLMFGSZFLWITSFFFLINMORAHZFANPSCEGAAPFUORIFMFWRPQONPZ`

The solver was given `("FROST", "MAPLE")` plus `DEFAULT_KEYWORDS` and was not given the squares. It returned keywords `FROST`/`MAPLE` and that plaintext.

The older `HARBOR`/`CANAL` stream (`VIGENERE_PLAIN` with J folded to I) still recovers the same way.

Command:

```text
python3 -m unittest tests.test_two_square -v
```

Result: `Ran 8 tests` / `OK` (exit 0), including `test_recovers_constructed_frost_maple_ciphertext` and `test_keyword_solver_recovers_synthetic_plaintext`.

Novelty label: **already published method** (keyword two-square plus an English n-gram score) on a fixture made for the test.

## Nr. 86 — still failed

Source fetched 2026-10-02: https://cryptocellar.org/bgac/g-army-ts-messages.html (“Messages That We Have Failed to Break”, page updated 27 July 2026). Funkspruch Nr. 86 (FBOIQ), received 03.07.1941 1435, has **no** “Broken on” note. Ciphertext, 46 letters:

`FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ`

Same solver as the passing example:

- Keyword search over `DEFAULT_KEYWORDS` (English word list, wrong keying model for random wartime squares). Best pair `WATER`/`NORTH`. Letters: `HAAGOPNNEIUMTOLTVWNAROONSNOLTTAENKGHBWVLLGIUPS`. German mean quadgram (Grimm model in `engine.german`) about −3.673. Held-out probe `DERWOLFUNDDIESIEBENJUNGENGEISZLEINWARENALLEHUNGRIG` is about −2.393. This string is not German and is not a reading.
- Shotgun hill-climb (`climb_two_square`, restarts=4, kicks=8, seed=86), same settings as the earlier failure log. Letters: `UTGSANDTHEREODCLISATTVDENTHAORETIDNVPXGANDTHEW`. Mean quadgram about −3.487. English-looking fragments come from an English trigram objective. Not a reading.

The paper’s booklet example is 54 letters, `FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENABGEWEHRT`. Neither output equals it, and neither has that length. No sourced German plaintext of Nr. 86 was found on the CryptoCellar page. None is claimed.

Novelty label: **failed**. The message remains unbroken here.
