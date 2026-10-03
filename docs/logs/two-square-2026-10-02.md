# Two-square solver — 2026-10-02 (EDT)

Run at 2026-10-02 22:45 EDT from a checkout of `1f55e89` plus the new two-square files. Nothing below is a decipherment of an unsolved message.

## 1. Known two-square, synthetic English

- Cipher: `two_square_encrypt` of `VIGENERE_PLAIN` (J folded to I) under keyword squares `HARBOR` / `CANAL` from `engine.ciphers.square_from_keyword`. The solver was not given the squares.
- Tool: `engine/solvers/two_square.py`, `solve_two_square` / `solve_two_square_keywords`, default English word list.
- Encipherment checks against Ostwald & Weierud Fig. 6: `KR→IN`, `NI→RK`, `QT→EU`, `UE→TQ` on the published squares.
- Command: `python3 -m unittest tests.test_two_square -v`
- Result: `Ran 7 tests` / `OK` (exit 0). `test_keyword_solver_recovers_synthetic_plaintext` returned keywords `HARBOR`/`CANAL` and the synthetic letter stream.
- Novelty label: **already published method** (keyword two-square + trigram scoring on a fixture made for the test).

## 2. Experiment — German Army Truppenschlüssel, 3 July 1941, Nr. 86 (FBOIQ)

- Source URL: https://cryptocellar.org/bgac/g-army-ts-messages.html (page “Messages That We Have Failed to Break”, updated 27 July 2026). Nr. 86 has no “Broken on” note.
- Cipher description: two 5×5 squares, J omitted, single-stage digraph substitution. Ostwald & Weierud, “Modern Cryptanalysis of the Truppenschlüssel,” https://cryptocellar.org/pubs/mcts.pdf
- Ciphertext, 46 letters: `FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ`
- This run used the new two-square tools only:
  1. Keyword search over the default English word list (wrong keying model for random wartime squares).
  2. Shotgun hill-climb (`climb_two_square`, restarts=4, kicks=8, seed=86) scored by English trigram counts.
- German scores use `engine.german` (Grimm excerpt). Higher (closer to zero) mean quadgram is more like that fairy tale. It is not a decipherment test.
- Held-out probe (different Grimm tale, umlaut-folded): mean quadgram ≈ −2.325.
- Climb best mean ≈ −3.487 (preview begins `UTGSANDTHEREODCLISATTVDENTHAORETIDNVPXGANDTHEW` — English-looking fragments from an English trigram objective).
- Keyword best (`NORTH`/`SOUTH`) mean ≈ −3.900.
- Raw ciphertext mean ≈ −4.102.
- The paper’s booklet example plaintext is 54 letters (`FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENABGEWEHRT`) and cannot be this 46-letter message. No climb or keyword string equals that sentence.
- No string was checked against a sourced German reading of Nr. 86, because none is published on the source page.
- Novelty label: **failed**

## Result

The two-square keyword solver recovers the synthetic English fixture. The Nr. 86 experiment **failed**. The message remains unbroken here. No plaintext is claimed.
