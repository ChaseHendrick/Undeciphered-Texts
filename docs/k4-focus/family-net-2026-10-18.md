Not solved. No plaintext claimed.

# K4 cipher-family prior from a small neural classifier, 18 October 2026

`solved` is false and `claimed_plaintext` is null in every report dict. Nothing below is a reading of K4, a key or a method. The output is a prior for ordering searches.

Code: `engine/k4_family_net.py`. Tests: `tests/test_k4_family_net.py`. Run: `python -m engine.k4_family_net --json OUT.json` (one thread; the module sets the BLAS thread variables to 1 unless they are already set).

The repo's general nets (`engine/solver_net.py`, `engine/neural_grade.py`) deliberately refuse K4 labels. This is a separate tool that only answers which of a fixed list of generated families K4's 97 letters resemble.

## Generator

Each sample is 97 letters. For every class except `random`, a 97-letter plaintext window gets both public clues planted at their zero-based positions, EASTNORTHEAST at 21 and BERLINCLOCK at 63 (`CRIB_SPANS` in `engine/k4_gromark_obstruction.py`), and is then encrypted with random keys.

- English windows: `engine/data/neural_train_public.txt` (1,916,398 letters).
- German windows (20 percent of samples): `work/k4_running_key_texts/raw/pg22367.txt` (Kafka, Die Verwandlung) and `pg2229.txt` (Goethe, Faust I), Gutenberg header and footer removed, umlauts expanded to AE, OE, UE and sharp s to SS, letters only (251,772 letters). If those files are absent the module falls back to `engine/data/german_excerpt.txt`.
- Train and validation windows come from the first 80 percent of each corpus. Test windows come from the last 20 percent, with a different generator seed. A running key is another window of the same language and region.

Repo encryptors used: `vigenere_encrypt`, `substitution_encrypt` (engine/ciphers.py), `beaufort_encrypt`, `keyed_vigenere_encrypt`, `autokey_encrypt`, `running_key_encrypt`, `progressive_key_encrypt`, `gromark_encrypt`, `hill_encrypt`, `bifid_encrypt`, `trifid_encrypt` (engine/solvers/*), and `columnar_perm` from `engine/k4_transposition_sub.py` for keyed columnar with an incomplete last row. Written locally because the repo had none: ciphertext autokey, Hill 3x3, and the columnar encrypt and decrypt wrappers. Every encryptor is round-trip tested (`round_trip_checks`, all 14 pass). Playfair is skipped because 97 is odd.

## Classes (17)

| class | construction |
|---|---|
| random | uniform random letters, no cipher, no clues planted |
| monoalphabetic | random simple substitution |
| periodic_p2_12 | Vigenere or Beaufort on A-Z, random key, period 2 to 12 |
| periodic_p13_30 | Vigenere or Beaufort on A-Z, random key, period 13 to 30 |
| keyed_vigenere | Kryptos-style keyed Vigenere: random mixed or keyword-mixed alphabet, random index letter, period 2 to 15 |
| autokey_plain | Vigenere plaintext autokey, primer 1 to 15 letters |
| autokey_cipher | Vigenere ciphertext autokey, primer 1 to 15 letters |
| running_key | Vigenere running key from another window of the same language |
| progressive_key | keyword 1 to 12 letters, progression 1 to 25 |
| gromark | keyword 5 to 10 letters, random 5-digit primer |
| hill_2x2 | Hill 2x2 on letters 1 to 96, letter 97 random |
| hill_3x3 | Hill 3x3 on letters 1 to 96, letter 97 random |
| bifid | 5x5 square (J folded to I), period 2 to 15 or whole text |
| trifid | 3x3x3 cube, period 2 to 15 or whole text; outputs of the 27th symbol are shown as one duplicate letter, so this class is a statistical stand-in, not an invertible 26-letter cipher |
| columnar | keyed columnar transposition only, width 2 to 20, either direction |
| columnar_then_periodic | columnar transposition, then Vigenere or Beaufort period 2 to 12 |
| periodic_then_columnar | Vigenere or Beaufort period 2 to 12, then columnar transposition |

## Features (415)

Statistics (93): index of coincidence; mean periodic IC for periods 1 to 30; kappa at shifts 1 to 30; the sorted letter frequency profile (26); log chi-square to English unigrams; overlapping digraph IC and non-overlapping digraph IC at both alignments; repeated trigram count; number of distinct letters.

Crib key (322): for Vigenere (k = c - p) and Beaufort (k = c + p) on A-Z, the 24 key letters implied by the clues, their IC, their log chi-square to English, for periods 1 to 30 the share of same-residue clue pairs whose key letters agree, for periods 1 to 30 the best progressive-key agreement (key difference equal to a constant times the number of periods between the pair), and ciphertext and plaintext autokey agreement at lags 1 to 30. One alphabet-free block: for periods 1 to 30, the number of same-column clue pairs that break a one-to-one substitution (the bijection test of `engine/k4_periodic_bijection.py`, as a count).

All features are standardized with training means and deviations.

## Model and data sizes

- Train 136,000 (8,000 per class), validation 17,000 (1,000 per class), test 17,000 (1,000 per class, held-out windows and fresh seed).
- Full model: MLP 415 to 256 to 128 to 17, ReLU, softmax, Adam (learning rate 3e-4), L2 3e-3, batch 256, early stopping on validation loss with patience 6, at most 40 epochs, seeds 11, 23, 37, 41. Best epochs 18 to 23.
- Statistics-only model: the same network on the 93 statistics features alone, seeds 11, 23, 37 (it ran to the 40-epoch cap). It shows how much of the answer comes from the clues.
- Configuration choice: a first full run with learning rate 1e-3 and L2 1e-4 stopped at epoch 3 to 4 with validation loss 0.756. A one-seed comparison gave 0.733 for 128-64 units (lr 5e-4, L2 1e-3) and 0.719 for 256-128 units (lr 3e-4, L2 3e-3); the last was kept.
- A 1D CNN over one-hot letters was not tried, to stay inside the one-core time budget.
- Temperature scaling: one temperature per seed, grid search on validation negative log likelihood (full model temperatures 0.90 to 0.92).

## Test results (held-out windows)

Full model: ensemble accuracy 0.755; seeds 0.747, 0.750, 0.749, 0.749. Test NLL 0.684. Chance is 0.059.

Per-class recall: monoalphabetic 1.00, autokey_cipher 1.00, columnar 1.00, periodic_p2_12 1.00, progressive_key 0.99, hill_3x3 0.99, hill_2x2 0.94, running_key 0.88, periodic_p13_30 0.79, autokey_plain 0.78, keyed_vigenere 0.69, bifid 0.66, gromark 0.62, columnar_then_periodic 0.56, random 0.47, trifid 0.24, periodic_then_columnar 0.21.

Largest confusions (true to predicted, of 1,000): autokey_plain to running_key 200; trifid to bifid 191; random to gromark 189; periodic_then_columnar to random 178; periodic_then_columnar to bifid 174; gromark to random 145; trifid to random 144; periodic_then_columnar to columnar_then_periodic 130; periodic_then_columnar to trifid 127; trifid to gromark 124.

So the classes split into a well-separated group (monoalphabetic, periodic A-Z, progressive, autokeys, running key, Hill, columnar) and a flat group that 97 letters cannot separate well: random, gromark, trifid, bifid, keyed_vigenere at long periods, and the two transposition plus periodic orders.

Statistics-only model: ensemble accuracy 0.389 (seeds 0.390, 0.389, 0.387). Its worst confusion is keyed_vigenere to periodic_p2_12 (315), which is exactly what the crib features fix.

Calibration (15-bin expected calibration error on test): full model members 0.016 to 0.019 before temperature scaling, 0.010 to 0.011 after; calibrated ensemble 0.014. Statistics-only calibrated ensemble 0.009.

## K4 posterior

Calibrated posterior, mean over seeds, with standard deviation and range across seeds.

Full model (4 seeds):

| family | mean | sd | min | max |
|---|---|---|---|---|
| random | 0.364 | 0.051 | 0.296 | 0.436 |
| gromark | 0.322 | 0.058 | 0.237 | 0.395 |
| trifid | 0.123 | 0.019 | 0.103 | 0.154 |
| periodic_then_columnar | 0.090 | 0.015 | 0.078 | 0.114 |
| columnar_then_periodic | 0.061 | 0.020 | 0.038 | 0.092 |
| periodic_p13_30 | 0.024 | 0.013 | 0.012 | 0.044 |
| keyed_vigenere | 0.007 | 0.003 | 0.004 | 0.011 |
| hill_2x2 | 0.006 | 0.005 | 0.003 | 0.015 |
| bifid | 0.002 | 0.001 | 0.001 | 0.004 |
| all others | under 0.001 each | | | |

Seed argmax: random, gromark, gromark, random.

Statistics-only model (3 seeds): progressive_key 0.146 (sd 0.009), autokey_cipher 0.142 (0.011), random 0.140 (0.006), running_key 0.105 (0.005), autokey_plain 0.102 (0.001), gromark 0.086 (0.006), periodic_p13_30 0.071 (0.007), trifid 0.062 (0.013), hill_2x2 0.051 (0.012), then smaller. Without the clues the model can only say that K4 is flat; it spreads mass over every flat family.

Reading: once the clues are used, K4 sits in the flat group. The crib-key features push almost all mass off the families whose clue-implied key would show structure (periodic A-Z keys, progressive keys, both autokeys, English running keys, monoalphabetic, Hill, pure transposition). The remaining mass is on families the net cannot tell from uniform random letters at this length. K4's random-class posterior (0.36) is about the same as the mean for 50 true random strings (0.30, below), so the net does not distinguish K4 from random letters. The useful content is the exclusions, which agree with the repo's exact clue tests (for example `engine/k4_periodic_bijection.py` and `engine/k4_transposition_sub.py`), not the top class.

## Sanity checks

50 uniform random strings (scored with K4's clue positions and letters): full model argmax random 21, gromark 13, bifid 5, trifid 5, periodic_then_columnar 4, columnar_then_periodic 2; mean random posterior 0.303. Statistics-only: random 8 of 50, mean random posterior 0.120. This is the same flat-group confusion seen on the test set.

Kryptos K1 to K3 (known methods). Each 97-letter window is scored with its own published plaintext at positions 21 to 33 and 63 to 73 as the clue, so the crib features have the same meaning as for K4. Ciphertexts and plaintexts are the repo's: `engine/data/kryptos_k1_certificate.json`, `engine/data/kryptos_k2_certificate.json`, `KRYPTOS_K3_*` in `engine/solvers/columnar.py`. K1 has only 63 letters, so it appears only in a window of all of K1 followed by the first 34 letters of K2 (the key changes from PALIMPSEST to ABSCISSA at letter 63, which no training sample does).

| window | known | full model argmax (p of known family) | statistics-only argmax (p of known) |
|---|---|---|---|
| K1 + K2 letters 0-33 | keyed Vigenere | columnar_then_periodic (keyed_vigenere 0.13, third) | keyed_vigenere (0.33) |
| K2 letters 0-96 | keyed Vigenere | keyed_vigenere (0.64) | periodic_p2_12 (0.32) |
| K2 letters 97-193 | keyed Vigenere | keyed_vigenere (0.64) | periodic_p2_12 (0.17) |
| K2 letters 194-290 | keyed Vigenere | keyed_vigenere (0.41) | periodic_then_columnar (0.07) |
| K2 letters 273-369 | keyed Vigenere | keyed_vigenere (1.00) | columnar_then_periodic (0.21) |
| K3 letters 0-96 | transposition | columnar (0.99) | columnar (0.99) |
| K3 letters 97-193 | transposition | columnar (1.00) | columnar (0.97) |
| K3 letters 194-290 | transposition | columnar (1.00) | columnar (1.00) |
| K3 letters 239-335 | transposition | columnar (0.82) | columnar (0.96) |

The full model puts all four K2 windows and all four K3 windows on the right family. It misses the mixed-key K1 plus K2 window, which is outside the generator. The statistics-only model gets K3 but not K2, as expected without clue information.

## Timing

One core (taskset to CPU 0, BLAS threads 1). Final run: generation 7.9 s, features 33.8 s, full model 503 s (4 seeds), statistics-only model 257 s (3 seeds), 13 min 24 s wall in all. With the first run (5 min 48 s) and the one-seed comparison (about 3 min), total compute was about 22 minutes.

Tests: `python -m unittest tests.test_k4_family_net` runs 5 tests in under 1 s (round trips, generator shapes and planted clues, held-out split, a tiny run that separates random from monoalphabetic at 95 percent or better, and a tiny K4 report that claims nothing).

## Limits

- The answer can only be one of the 17 generated families. If K4 uses a method not in the list (another tableau, a different transposition, a key change mid-text, nulls, a misprint), the posterior still sums to one over these classes.
- 97 letters is short. Random, Gromark, Trifid, Bifid and the two transposition plus periodic orders are poorly separated at this length (test recall 0.21 to 0.66), and K4 falls in that group.
- A statistical resemblance is not a method. A high posterior on a family says nothing about its key and is not evidence that K4 was made that way.
- The key ranges are this generator's choices (for example columnar widths 2 to 20, periods up to 30). Families with keys outside them are not represented.
- The trifid class maps the 27th cube symbol to a duplicate letter; real 26-letter trifid variants differ.
- Plaintext windows are English novels and two German texts with the clues planted. Military or telegraphic plaintext, or plaintext with X separators, may look different.
- Seeds share one training set; the spread across seeds reflects initialization and shuffling, not data resampling.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
