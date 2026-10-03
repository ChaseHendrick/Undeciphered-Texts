# Handoff for a later Codex session

This note was written after `git pull` of `origin/main`. The tip confirmed with `git log` is `895bfb77eac829778944f29a6de81296768b0452`, subject "Record a bounded K4 ciphertext-error search." The parent is `5875597ffb87d546e35f28b55980ca36a5bc9d0e`, subject "Add a Solitaire known-deck keystream check for Schneier's published samples." Do not invent later SHAs. Cite a SHA only after `git log` on `origin/main` shows it.

Plain sentences. Do not put U+2014 or U+2013 in new text. Use a hyphen or a period instead.

## What the user wants

Keep adding published known-key solvers with verification certificates until a new one would only repeat a solver already on main. Then find the next missing published cipher that has a cited plaintext.

A test must decrypt and match the SHA-256 of the known plaintext. Cite the source URL in the certificate and the solver note. The pattern is in `docs/verification-certificates.md` and `docs/TESTING.md`.

Do not claim a solve of Kryptos K4, Zodiac Z13, Zodiac Z32, Beale 1, Beale 3, the Ricky McCormick notes, D'Agapeyeff's real 395-digit challenge, the Voynich manuscript, Linear A, the Indus script, or rongorongo unless you have a cited plaintext. A bounded negative search is not a solve.

Skip Funkspruch Nr. 86. The user said someone already solved it and the paper is not released. Do not start new Nr. 86 searches. Existing failed notes stay as logs only: `docs/logs/nr86-2026-10-02.md`, `docs/logs/nr86-german-climb-2026-10-02.md`, `docs/logs/nr86-three-score-2026-10-02.md`, and `docs/logs/nr86-crib-slide-2026-10-03.md`. `docs/CATALOG.md` says `engine/solvers/two_square.py` does not claim an Nr. 86 plaintext.

Neural router training stays inside the repo. The command is `python -m engine.neural_router_loop`. One pass is `python -m engine.neural_router_loop --once`. Do not create a Grok Bot routine or a cron job for it. The user explicitly rejected a weekday retrain routine. `engine/neural_router_loop.py` says the module does not register cron, a timer, or any wake outside the process. Each pass reads the certificate files on disk and adds a new known-answer `cipher_name` as a class. `engine/neural_grade.py` writes weights only when `heldout_accuracy_not_worse` is true, which means the held-out score does not drop. The net only routes among certified solvers. `docs/solver-net.md` says it declines Kryptos K4, army message Nr. 86, Linear A, the Indus script, the Voynich manuscript, and rongorongo.

The user asked to test whether K4 is unsolved because of a ciphertext error. The errors are one wrong letter, one adjacent swap, and one insert or delete. Do not claim a solve. That test is not the older bounded search in `docs/k4-attempt.md`
- `docs/k4-error-model.md`
- `engine/solvers/k4_error_model.py`. It is now on main. See the next section.

No JustLetMeRead or GENChase credits. Those were removed. Do not add them back. On this pull, `git log origin/main` shows `9d5b5716f39f93aa121097830664a0ae35236eff` ("Remove the JustLetMeRead and GENChase layout credit from the README.") and `d830cf3aba4e49dd23d763fdcc960220518ff282` ("Remove remaining JustLetMeRead and GENChase credits."). A text search of this tree found no remaining `JustLetMeRead` or `GENChase` string.

Do not touch `docs/assets/readme-hero.jpg`. It must stay a nameless JPEG. On this pull the first three bytes are `ff d8 ff`. Do not replace it, rename it, or rewrite it through the GitHub contents API. That API corrupts JPEGs.

Commit as `Chase` with email `326338179+ChaseHendrick@users.noreply.github.com`. Push with git, not the GitHub contents API. If the push is rejected, rebase onto `origin/main` and push again.

## What is next

1. The K4 error-model note is already on main. Do not write it again. `docs/k4-error-model.md`, `engine/solvers/k4_error_model.py`, and `tests/test_k4_error_model.py` landed in `895bfb77eac829778944f29a6de81296768b0452`. The catalog row says the same thing. The search tries one substituted crib letter, one neighbor swap that touches a crib letter, or one deletion or insertion that keeps every crib word contiguous. It pairs those edits only with Vigenere and Beaufort, periods 1 through 8. The note's counts are all `key-consistent` 0. The result line is "not solved. No plaintext claimed." `claimed_plaintext` stays null. Do not extend this into a claimed solve.

2. The shortlist that was in progress is done. Each of these is on main:

- Seriated Playfair: `engine/solvers/seriated_playfair.py`, `tests/test_seriated_playfair.py`, `engine/data/seriated_playfair_certificate.json`, `docs/seriated-playfair.md`. Commit `b73444d7eb5d3537ed6ac1efdc6cc631b514c749`.
- CM Bifid: `engine/solvers/cm_bifid.py`, `tests/test_cm_bifid.py`, `engine/data/cm_bifid_certificate.json`, `docs/cm-bifid.md`. Commit `89f9da9f034c5af3b96824d448708090ffb28121`.
- Quagmire IV: `engine/solvers/quagmire_iv.py`, `tests/test_quagmire_iv.py`, `engine/data/quagmire_iv_certificate.json`. There is no `docs/quagmire-iv.md`. The catalog row and `docs/verification-certificates.md` already name it. Commit `9a79f471b291b9b15c0ff154846cf74aa8f40471`. Do not rebuild this solver.
- Tri-square: `engine/solvers/tri_square.py`, `tests/test_tri_square.py`, `engine/data/tri_square_certificate.json`, `docs/tri-square.md`. Commit `d577784b68b9402d2b9debbb8529267ea5d9c46b`.
- Chaocipher: `engine/solvers/chaocipher.py`, `tests/test_chaocipher.py`, `engine/data/chaocipher_certificate.json`, `docs/chaocipher.md`. Commit `917fd0316cfef72f4f0b9c6654f6a5f05a1ff10d`.
- Nihilist transposition: `engine/solvers/nihilist_transposition.py`, `tests/test_nihilist_transposition.py`, `engine/data/nihilist_transposition_certificate.json`, `docs/nihilist-transposition.md`. Commit `68c28746ca084208abb7d65bf77a209f0b389e49`. This is not the Nihilist substitution solver in `engine/solvers/nihilist.py`.
- Solitaire: `engine/solvers/solitaire.py`, `tests/test_solitaire.py`, `engine/data/solitaire_certificate.json`, `docs/solitaire.md`. Commit `5875597ffb87d546e35f28b55980ca36a5bc9d0e`.

3. Add the next published classical cipher that is not already a solver, with a worked example and a SHA-256 certificate. The error-model note is not that job.

Checked before naming the gap:

- Homophonic beyond the fixed-temperature search is not a free module name. `engine/solvers/homophonic_fixed_temperature.py` is already on main. It follows Kopal 2019 on a constructed fixture (`docs/homophonic-fixed-temperature.md`). The ACA also has a Homophonic sheet at `https://www.cryptogram.org/downloads/aca.info/ciphers/Homophonic.pdf`. That sheet is not its own solver here. Do not repeat the fixed-temperature module.
- Grille variants: the ACA cipher list has one Grille type. This repo already has the Fleissner turning grille in `engine/solvers/turning_grille.py`, checked on `https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf`. No second grille solver is missing from that list.
- Digrafid is done: `engine/solvers/digrafid.py`.
- Fractionated Morse is done: `engine/solvers/fractionated_morse.py`.
- Quagmire IV is done. Quagmire I, Quagmire II, and Quagmire III are absent. There is no `quagmire_i.py`, `quagmire_ii.py`, `quagmire_iii.py`, matching test, or matching certificate.

Three ciphers that are actually absent, confirmed against the ACA list at `https://www.cryptogram.org/resource-area/cipher-types/` and against `engine/solvers/` plus `docs/CATALOG.md`:

- Quagmire I. Sheet URL checked: `https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf`.
- Quagmire II. Sheet URL checked: `https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireII.pdf`.
- Quagmire III. Sheet URL checked: `https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf`.

Add Quagmire I next. Use the sheet's printed plaintext and ciphertext. Do not treat it as a Kryptos K4 solve. The Roman numeral IV in the existing solver is the ACA keyword plan, not the Kryptos section.

Do not keep retrying Nr. 86.

## What has been done

`docs/CATALOG.md` is a deep inventory, but the README layout table still names only Caesar, Vigenere, keyed Vigenere, and substitution. Trust `engine/solvers/` for the module list. These solver modules are the `.py` files in that directory on this pull, aside from `__init__.py`:

`adfgvx.py`, `affine.py`, `amsco.py`, `autokey.py`, `bazeries.py`, `beam_search.py`, `beaufort.py`, `bifid.py`, `cadenus.py`, `caesar.py`, `chaocipher.py`, `chaos_search.py`, `click_lock.py`, `cm_bifid.py`, `columnar.py`, `crib.py`, `digrafid.py`, `dudley_lock.py`, `electronic_lock.py`, `em_sign_aligner.py`, `enigma.py`, `fbi_letter_shift.py`, `four_square.py`, `fractionated_morse.py`, `grandpre.py`, `gromark.py`, `gronsfeld.py`, `hill.py`, `homophonic_fixed_temperature.py`, `k4_attempt.py`, `k4_error_model.py`, `keel_sieve.py`, `keyed_vigenere.py`, `lockpicks.py`, `lumen_braid.py`, `m209.py`, `master_lock.py`, `myszkowski.py`, `nicodemus.py`, `nihilist.py`, `nihilist_transposition.py`, `old_dial_lock.py`, `pacifist.py`, `persona_court_notice.py`, `persona_hallucinogens.py`, `persona_inheritance.py`, `phillips.py`, `playfair.py`, `polybius_gronsfeld.py`, `porta.py`, `portax.py`, `prism_latch.py`, `quagmire_iv.py`, `ragbaby.py`, `rail_fence.py`, `route.py`, `rsa_broadcast.py`, `running_key.py`, `seriated_playfair.py`, `sim_safe_lock.py`, `simplex_lock.py`, `slidefair.py`, `solitaire.py`, `straddling_checkerboard.py`, `substitution.py`, `swagman.py`, `tiny_exhaustive.py`, `tri_square.py`, `tridigital.py`, `trifid.py`, `turning_grille.py`, `two_square.py`, `vibration_lock.py`, `vigenere.py`.

The RSA broadcast attacker is `engine/solvers/rsa_broadcast.py` with `engine/data/rsa_broadcast_certificate.json` and `tests/test_rsa_broadcast.py`. Commit `827bea3a7360c9effd99be616ff19290e430e97d` says "Add a Boneh/Hastad e=3 RSA broadcast known-answer attacker." `docs/CATALOG.md` says it is a synthetic textbook-weak instance, not an attack on a real key, a live server, TLS, or a padding oracle.

The neural loop is `engine/neural_router_loop.py`. The grader is `engine/neural_grade.py`. The shipped router is `engine/solver_net.py`. Weights live in `engine/data/neural_router_weights.json`. Commit `adc6d2500ee80c8258d0c8debc9080c495d82bca` added the solver net. Commit `191080ba62d6ad784de85d7ed95d352e11561928` sped up the letter model and raised the held-out cipher router score. New certificates should become classes on the next pass. Keep weights only if the held-out score does not drop.

The negative K4 search is on main. `docs/k4-attempt.md` exists. `engine/solvers/k4_attempt.py` and `tests/test_k4_attempt.py` exist. Commit `5af1d092617773c99e1307d7c6cafa7263d65891` says "Add a bounded Kryptos K4 search that does not recover a plaintext." The note's result line is "not solved. No plaintext claimed."

The ciphertext-error test is also on main, and it is a separate file. `docs/k4-error-model.md` exists. `engine/solvers/k4_error_model.py` and `tests/test_k4_error_model.py` exist. Commit `895bfb77eac829778944f29a6de81296768b0452` says "Record a bounded K4 ciphertext-error search." That result is also not solved, and no plaintext is claimed.

Certificates are the JSON files `engine/data/*_certificate.json`. `docs/verification-certificates.md` lists the classical examples those tests hash.

## Where to read

- `README.md`
- `docs/verification-certificates.md`
- `docs/TESTING.md`
- `docs/CATALOG.md`
- `engine/solvers/`
- `engine/data/*_certificate.json`
- `docs/k4-attempt.md`
- `engine/neural_router_loop.py`
- `engine/neural_grade.py`
- `docs/solver-net.md`
- ACA cipher types: `https://www.cryptogram.org/resource-area/cipher-types/`

## How to land the next change

Pull `origin/main` first. Add one known-key solver, its test, its certificate, and a short doc. The test decrypts the published example and checks the SHA-256 of the known plaintext. Cite the source URL. Do not edit `docs/assets/readme-hero.jpg`. Do not add JustLetMeRead or GENChase. Do not use U+2014 or U+2013. Commit as Chase at `326338179+ChaseHendrick@users.noreply.github.com`. Push with git.
