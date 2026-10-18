# K4 running keys from texts other than K3, 18 October 2026

Not solved. No plaintext claimed.

Module: `engine/k4_running_key_texts.py`. Test: `tests/test_k4_running_key_texts.py`. `search_k4_running_key_texts()` returns `solved: false` and `claimed_plaintext: null`. A full 24-letter clue match would be stored as unverified with its decryption. None was found.

The earlier check in [`running-key-hill-2026-10-04.md`](running-key-hill-2026-10-04.md) used only the K3 plaintext under plain Vigenere. This note widens the key texts and the tableaux.

## What is tested

Ciphertext: the 97-letter `K4_CIPHERTEXT` in `engine/solvers/k4_attempt.py` (SHA-256 of the letters `eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab`). Clues, zero-based plaintext positions, from `CRIB_SPANS` in `engine/k4_gromark_obstruction.py`: EASTNORTHEAST at 21 and BERLINCLOCK at 63. Source of the ciphertext and clues: <https://en.wikipedia.org/wiki/Kryptos>.

Twelve tableaux: Vigenere (c = p + k), Beaufort (c = k - p) and variant Beaufort (c = p - k), each on A-Z and on the keyed alphabets KRYPTOS (`KRYPTOSABCDEFGHIJLMNQUVWXZ`), PALIMPSEST (`PALIMSETBCDFGHJKNOQRUVWXYZ`) and ABSCISSA (`ABSCIDEFGHJKLMNOPQRTUVWXYZ`). Keyed means the K1/K2 sense, c = A[(A^-1 p + A^-1 k) mod 26], with the analogous keyed Beaufort and variant. The keyed Vigenere convention is checked against the published K1 and K2 certificates in the test file.

For each tableau the clues fix 24 key letters, at positions 21..33 and 63..73:

| Tableau | Key at 21..33 | Key at 63..73 |
| --- | --- | --- |
| vigenere/AZ | `BLZCDCYYGCKAZ` | `MUYKLGKORNA` |
| vigenere/KRYPTOS | `RDUMRIYWOYNKY` | `ELYOIECBAQK` |
| vigenere/PALIMPSEST | `SAJJLATGIEJPY` | `BQTRMOVXUOP` |
| vigenere/ABSCISSA | `BLPSCSYZDSKAH` | `MRYHODJMRMA` |
| beaufort/AZ | `JLJODEGKUKKKL` | `OCGGBGOKTRU` |
| beaufort/KRYPTOS | `WXAKGZTOAXAFD` | `RGTGNWRJLFK` |
| beaufort/PALIMPSEST | `OIYLBCRPIQNDG` | `YMRXDXHALCM` |
| beaufort/ABSCISSA | `MLUNDEGKXNKIV` | `OIGFXFPKWTW` |
| variant_beaufort/AZ | `ZPBYXYCCUYQAB` | `OGCQPUQMJNA` |
| variant_beaufort/KRYPTOS | `ZJOBZEXPUXAKX` | `ICXUEILMNSK` |
| variant_beaufort/PALIMPSEST | `VZGGYZRJXUGPL` | `QBRTWCSIECP` |
| variant_beaufort/ABSCISSA | `ZNJYXYSBVYOAQ` | `MGSQKVPMGMA` |

Both tests below use only these clue letters, so they hold whatever language K4's plaintext is in.

## Frozen key texts

Letters only, uppercased. German letters are written AE, OE, UE, SS and other accents are dropped (`normalize_letters`). Project Gutenberg files keep only the lines between the `*** START OF` and `*** END OF` markers. Archive.org OCR files are used whole, so page headers, page numbers spelled as letters and OCR errors stay in. Fetched files sit in the git-ignored `work/k4_running_key_texts/raw/` and are not vendored. Accessed 18 October 2026.

| Name | Lang | URL | Letters | SHA-256 of letters | Status |
| --- | --- | --- | ---: | --- | --- |
| `kryptos_k1_plaintext` | en | https://en.wikipedia.org/wiki/Kryptos | 63 | `a4a581f02185ae92d52bbf55113cb59e73a2914f24af2634ffdb33c1d4988c15` | repo |
| `kryptos_k2_plaintext` | en | https://en.wikipedia.org/wiki/Kryptos | 370 | `cb5420f5cd5e8def287353d8522a79bb066a76c083746d56f4fed85e23a5a165` | repo |
| `kryptos_k3_plaintext` | en | https://en.wikipedia.org/wiki/Kryptos | 336 | `ea07f4ff5bc4ffcf6cd2a3e33263d25543ea81d1089ed9a413021d75db46aafc` | repo |
| `kryptos_k1k2k3_plaintext` | en | https://en.wikipedia.org/wiki/Kryptos | 769 | `d6867c975d1150ebe529abf3027da24353fda20bff4a310e51f3e51f2044008c` | repo |
| `kryptos_k1k2k3_ciphertext` | none | https://en.wikipedia.org/wiki/Kryptos | 769 | `df59b0c4d29a0493e2ff39061e006128700e2fb0c83cfa331676431ab675e16b` | repo |
| `neural_heldout_doyle` | en | https://www.gutenberg.org/cache/epub/1661/pg1661.txt | 7314 | `cbee687d0c9465488180c158b20542777681e2b1900ca4015caa9d25aaba162a` | repo |
| `neural_train_public` | en | engine/data/neural_train_public.txt (public-domain training prose) | 1916398 | `8ec4db841fced52b112282e6fbe0f9aee89e38af3d371b9b43b1b620203326fb` | repo |
| `carter_tomb_vol1_1923_ocr` | en | https://archive.org/download/tomboftutankhame00cart_1/tomboftutankhame00cart_1_djvu.txt | 284914 | `2e398a0b57f6ce5f0d16710e968fd4da7fa5662981474212a345376b7d996865` | fetched |
| `carter_tomb_vol2_1927_ocr` | en | https://archive.org/download/tomboftutankhame02cart/tomboftutankhame02cart_djvu.txt | 351185 | `4bbcb5dacadb6e6575409e15bb26188f5307ed3d2676fb83b20fc26abb731a75` | fetched |
| `declaration_of_independence` | en | https://www.gutenberg.org/cache/epub/1/pg1.txt | 8448 | `6cb6c0a224a7f53c90be6b724bd7f120603a98b0ba44d7a0ca7ce64cb0a4a872` | fetched |
| `us_constitution` | en | https://www.gutenberg.org/cache/epub/5/pg5.txt | 22328 | `a392b34ff2b774d97baf04997fc7c360ca56d2ef952e22c0554dea83c0e8c37a` | fetched |
| `king_james_bible` | en | https://www.gutenberg.org/cache/epub/10/pg10.txt | 3225906 | `b6c30fd38555f0b6be949eef7ceacfdd8fe96309b60d3a4563071649f886f049` | fetched |
| `pride_and_prejudice` | en | https://www.gutenberg.org/cache/epub/1342/pg1342.txt | 563939 | `47619b437e5e71f4b126ff803f4be493903e2aca6fe1b1440d14b99d89f8c03c` | fetched |
| `moby_dick` | en | https://www.gutenberg.org/cache/epub/2701/pg2701.txt | 955178 | `e2140a13eb2a68c575e21428a0b6d3773c05e4c0f6f9f93d7de1af7ea320c1be` | fetched |
| `tale_of_two_cities` | en | https://www.gutenberg.org/cache/epub/98/pg98.txt | 584912 | `4a97885eb286ce2d1d5de60c975fb8f6a7130101187ae7e267f6cdb553b35f98` | fetched |
| `war_and_peace` | en | https://www.gutenberg.org/cache/epub/2600/pg2600.txt | 2517012 | `66fad2084a5b2646de1e1f3bdb17d545020c6116a2c169a70fdba45af60bab94` | fetched |
| `goethe_faust_1` | de | https://www.gutenberg.org/cache/epub/2229/pg2229.txt | 150796 | `d92c0b35e48b63f25f5183f686f02f362efce9597aa4b3d51ec8ab023047e727` | fetched |
| `kafka_verwandlung` | de | https://www.gutenberg.org/cache/epub/22367/pg22367.txt | 100976 | `76fff2217254107492dd8377235b863fac35f8256b9fa4328dc002e36f28ca7d` | fetched |
| `fontane_effi_briest` | de | https://www.gutenberg.org/cache/epub/5323/pg5323.txt | 477712 | `8bcdc1d122968881ba8a2e422086eb5be9ccdd515fa0c56b8acb50ef8f39a4fb` | fetched |
| `fontane_frau_jenny_treibel_berlin` | de | https://www.gutenberg.org/cache/epub/46184/pg46184.txt | 311569 | `d2087dcc8d9a658f7a90c5adda0d8b92c46e9217e6de822897a74ce93573c348` | fetched |

The K3 plaintext is a paraphrase of Howard Carter's 26 November 1922 entry (Wikipedia, same page). The 1923 volume 1 OCR contains that passage ("Slowly, desperately slowly ... the remains of passage debris that encumbered the lower part of the doorway"). Frau Jenny Treibel is subtitled "Roman aus der Berliner Gesellschaft" and was added because BERLIN is a clue. The raw-download SHA-256 of each fetched file is frozen in `FROZEN_SOURCES` as `raw_sha256`. `load_sources()` recomputes the letters hash and marks a file `hash_mismatch` if it changed.

Not used, recorded in `NOT_FETCHED`:

- Carter vol. 1 on Project Gutenberg: the Gutenberg search for "tut-ankh-amen" returned no record. The archive.org OCR of the 1923 printing was used instead. OCR noise means an exact Carter key would match only if the 24 key positions avoid OCR errors.
- CIA Kryptos texts (<https://www.cia.gov/legacy/museum/artifact/kryptos/>): no public full text; skipped as instructed.
- No Sanborn-written public-domain text was found to add.

K1 (63 letters) is shorter than the 74 letters a clue scan needs, so it is skipped alone and used inside `kryptos_k1k2k3_plaintext`.

## Exact clue scan

For each text and tableau, `scan_text` counts, at every offset o, how many of the 24 required key letters sit at o+21..o+33 and o+63..o+73. Offsets run over the text read forwards and read backwards, as long as 74 letters remain. A count of 24 is a full match. Chance is judged two ways. "Expected max" is the expected maximum over all scanned offsets if each offset's count were Poisson-binomial with the text's own letter rates. "Shuffle best" is the best count after one seeded shuffle of the same text (seed 20261018). "Smallest p" is the smallest, over the 12 tableaux, of P(max at least the observed best) under the Poisson-binomial model.

Columns V, B and VB are Vigenere, Beaufort and variant Beaufort; AZ, KRY, PAL and ABS are the alphabets. Cells are the best partial match out of 24.

| Text | Offsets | Full | V/AZ | V/KRY | V/PAL | V/ABS | B/AZ | B/KRY | B/PAL | B/ABS | VB/AZ | VB/KRY | VB/PAL | VB/ABS | Expected max | Shuffle best | Smallest p | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: |
| `kryptos_k1_plaintext` | 0 | skipped |  |  |  |  |  |  |  |  |  |  |  |  | | | | |
| `kryptos_k2_plaintext` | 594 | 0 | 5 | 5 | 5 | 7 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 3.69 to 5.07 | 3 to 6 | 0.00873 | 0.00 |
| `kryptos_k3_plaintext` | 526 | 0 | 4 | 6 | 5 | 5 | 4 | 4 | 4 | 4 | 3 | 5 | 5 | 4 | 3.84 to 5.14 | 3 to 5 | 0.238 | 0.00 |
| `kryptos_k1k2k3_plaintext` | 1392 | 0 | 5 | 6 | 5 | 7 | 5 | 5 | 6 | 5 | 4 | 5 | 5 | 4 | 4.18 to 5.51 | 4 to 6 | 0.0269 | 0.00 |
| `kryptos_k1k2k3_ciphertext` | 1392 | 0 | 6 | 5 | 7 | 6 | 6 | 5 | 5 | 6 | 4 | 4 | 5 | 6 | 4.71 to 5.30 | 4 to 6 | 0.0247 | 0.00 |
| `neural_heldout_doyle` | 14482 | 0 | 6 | 7 | 6 | 6 | 6 | 6 | 7 | 6 | 5 | 5 | 5 | 6 | 5.22 to 6.66 | 5 to 7 | 0.214 | 0.01 |
| `neural_train_public` | 3832650 | 0 | 8 | 9 | 8 | 8 | 7 | 8 | 8 | 8 | 7 | 7 | 8 | 8 | 7.06 to 8.76 | 7 to 9 | 0.228 | 3.85 |
| `carter_tomb_vol1_1923_ocr` | 569682 | 0 | 7 | 8 | 7 | 8 | 8 | 8 | 8 | 8 | 6 | 7 | 7 | 6 | 6.42 to 8.04 | 6 to 8 | 0.203 | 0.51 |
| `carter_tomb_vol2_1927_ocr` | 702224 | 0 | 7 | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 7 | 7 | 7 | 6 | 6.51 to 8.08 | 7 to 9 | 0.238 | 0.63 |
| `declaration_of_independence` | 16750 | 0 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 5 | 6 | 5 | 6 | 5.20 to 6.53 | 5 to 7 | 0.257 | 0.01 |
| `us_constitution` | 44510 | 0 | 6 | 7 | 7 | 8 | 6 | 6 | 6 | 6 | 6 | 6 | 7 | 6 | 5.50 to 6.91 | 5 to 7 | 0.0677 | 0.03 |
| `king_james_bible` | 6451666 | 0 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 7 | 8 | 7.02 to 8.78 | 7 to 9 | 0.247 | 6.78 |
| `pride_and_prejudice` | 1127732 | 0 | 7 | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 7 | 7 | 6 | 8 | 6.68 to 8.35 | 7 to 9 | 0.0805 | 0.99 |
| `moby_dick` | 1910210 | 0 | 7 | 9 | 8 | 7 | 8 | 8 | 8 | 8 | 7 | 8 | 7 | 8 | 6.83 to 8.40 | 6 to 8 | 0.117 | 1.84 |
| `tale_of_two_cities` | 1169678 | 0 | 7 | 9 | 8 | 8 | 7 | 8 | 8 | 7 | 7 | 7 | 7 | 6 | 6.58 to 8.32 | 7 to 9 | 0.305 | 1.10 |
| `war_and_peace` | 5033878 | 0 | 7 | 9 | 9 | 9 | 8 | 9 | 8 | 8 | 7 | 8 | 7 | 7 | 7.09 to 8.82 | 7 to 9 | 0.273 | 4.57 |
| `goethe_faust_1` | 301446 | 0 | 7 | 8 | 7 | 8 | 7 | 6 | 7 | 8 | 7 | 7 | 6 | 5 | 6.00 to 7.51 | 5 to 8 | 0.0965 | 0.27 |
| `kafka_verwandlung` | 201806 | 0 | 7 | 7 | 7 | 7 | 7 | 8 | 7 | 7 | 6 | 8 | 7 | 6 | 5.80 to 7.41 | 5 to 8 | 0.113 | 0.15 |
| `fontane_effi_briest` | 955278 | 0 | 7 | 8 | 9 | 7 | 8 | 8 | 7 | 8 | 6 | 8 | 8 | 6 | 6.30 to 8.03 | 6 to 8 | 0.0138 | 0.94 |
| `fontane_frau_jenny_treibel_berlin` | 622992 | 0 | 8 | 8 | 7 | 7 | 7 | 7 | 7 | 8 | 6 | 8 | 7 | 6 | 6.20 to 7.91 | 6 to 8 | 0.142 | 0.53 |

Full matches: 0 in all 228 text and tableau pairs. Unverified decryptions stored: 0 (cap 20).

Best partial matches are 3 to 9 of 24, in line with the expected maximum and the shuffled text. The highest is 9 of 24. The smallest p is 0.0087 (K2 plaintext, vigenere/ABSCISSA, 7 of 24 at forward offset 13, expected max 4.7). With 228 pairs about two p values under 0.01 are expected by chance, so it is not a lead. No text came near 24, so there is no near miss of the kind a few OCR or edition differences would produce (for example 20 or more of 24).

Scope: this rules out these exact letter streams as a non-wrapping, unskipped running key for K4 under these twelve tableaux, with no transposition layer. It says nothing about other editions, other spellings or normalizations, keys with skipped or inserted letters, other tableaux, or a K4 that is transposed before or after the substitution.

## Source-agnostic English-key check

If the running key is English prose from any source, the key letters at 21..33 (13 letters) and 63..73 (11 letters), 42 letters apart, are two pieces of English. The score of a pair is the sum of `DiscountedLanguageModel.full_score` (from `engine/language.py` `get_model()`) over the two fragments, in nats.

Null: every aligned pair at the same separation in `engine/data/neural_train_public.txt`, 1916325 pairs. Threshold: the 1st percentile of that null, fixed in `THRESHOLD_PERCENTILE = 1.0` in the module before K4 was scored. Value -62.41. The lowest of the 1916325 English pairs scores -86.21.

The null text also fits the quadgram model, so in-sample pairs score a little high. The power control measures that bias on text the model never saw.

### Power control

`english_fragment_control` plants an English running key from a held-out text, encrypts a 97-letter plaintext window (K2 plus K3 plaintext) under each tableau, takes the planted plaintext at 21..33 and 63..73 as the clues, recovers the 24 key letters exactly as for K4, and scores them. The round trip (recovered fragments equal the planted key, and decryption returns the plaintext) held in every trial. Because the recovered fragments are the planted key letters, the rates are the same for all 12 tableaux. None of these key texts is in `neural_train_public.txt`.

| Held-out key text | Stride | Trials per tableau | Below threshold | Rate | Lowest score | At or below -137.74 | Round trip |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `neural_heldout_doyle` | 4 | 1805 | 83 | 4.60% | -80.43 | 0 | ok, all 12 |
| `pride_and_prejudice` | 375 | 1504 | 45 | 2.99% | -73.68 | 0 | ok, all 12 |
| `war_and_peace` | 1678 | 1500 | 142 | 9.47% | -103.75 | 0 | ok, all 12 |
| `declaration_of_independence` | 5 | 1671 | 87 | 5.21% | -118.07 | 0 | ok, all 12 |
| `king_james_bible` | 2150 | 1501 | 119 | 7.93% | -100.11 | 0 | ok, all 12 |
| `carter_tomb_vol1_1923_ocr` | 189 | 1507 | 211 | 14.00% | -150.49 | 2 | ok, all 12 |

At the 1st-percentile threshold, a true English key from clean held-out prose falls below it 3.0% to 9.5% of the time, not 1%. That is the in-sample bias plus names, foreign words and archaic spelling. The noisy Carter OCR falls below 14.0% of the time. The last numeric column counts planted pairs that score at or below -137.74, the highest K4 score in the next table: 0 of 7981 clean-prose pairs, and 2 of 1507 OCR pairs.

### K4

Scores of the K4 key fragments per tableau. "Reversed" scores the reversed fragments, which is what an English key read backwards would give. Percentile is the share of the 1916325 null pairs at or below the score.

| Tableau | Key at 21..33 | Key at 63..73 | Score | Percentile | Reversed score | Reversed percentile | Below threshold (both) |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| vigenere/AZ | `BLZCDCYYGCKAZ` | `MUYKLGKORNA` | -171.43 | 0.0000 | -166.57 | 0.0000 | yes |
| vigenere/KRYPTOS | `RDUMRIYWOYNKY` | `ELYOIECBAQK` | -161.82 | 0.0000 | -137.74 | 0.0000 | yes |
| vigenere/PALIMPSEST | `SAJJLATGIEJPY` | `BQTRMOVXUOP` | -181.70 | 0.0000 | -168.64 | 0.0000 | yes |
| vigenere/ABSCISSA | `BLPSCSYZDSKAH` | `MRYHODJMRMA` | -144.38 | 0.0000 | -152.74 | 0.0000 | yes |
| beaufort/AZ | `JLJODEGKUKKKL` | `OCGGBGOKTRU` | -168.00 | 0.0000 | -166.03 | 0.0000 | yes |
| beaufort/KRYPTOS | `WXAKGZTOAXAFD` | `RGTGNWRJLFK` | -169.56 | 0.0000 | -159.49 | 0.0000 | yes |
| beaufort/PALIMPSEST | `OIYLBCRPIQNDG` | `YMRXDXHALCM` | -174.39 | 0.0000 | -167.47 | 0.0000 | yes |
| beaufort/ABSCISSA | `MLUNDEGKXNKIV` | `OIGFXFPKWTW` | -154.63 | 0.0000 | -158.94 | 0.0000 | yes |
| variant_beaufort/AZ | `ZPBYXYCCUYQAB` | `OGCQPUQMJNA` | -192.14 | 0.0000 | -186.80 | 0.0000 | yes |
| variant_beaufort/KRYPTOS | `ZJOBZEXPUXAKX` | `ICXUEILMNSK` | -178.62 | 0.0000 | -163.67 | 0.0000 | yes |
| variant_beaufort/PALIMPSEST | `VZGGYZRJXUGPL` | `QBRTWCSIECP` | -191.60 | 0.0000 | -182.93 | 0.0000 | yes |
| variant_beaufort/ABSCISSA | `ZNJYXYSBVYOAQ` | `MGSQKVPMGMA` | -179.50 | 0.0000 | -192.17 | 0.0000 | yes |

Every K4 fragment pair, in both readings, scores below the lowest of the 1916325 null pairs (-86.21) and below every one of the 7981 clean held-out control pairs.

Excluded at the stated threshold: all twelve tableaux, for an English-prose running key read forwards or backwards. This is a statistical exclusion, not an exact one. The control shows the threshold wrongly rejects 3% to 9.5% of true clean English keys, and K4's margin is far larger than that: its best score is 51 nats below the lowest null pair. The exclusion does not cover a key that is not English prose (another language, a list of names or numbers, a cipher alphabet, or OCR-like noise: 2 of 1507 noisy Carter OCR pairs scored as low as K4's best), a key with a transposition layer on K4, or tableaux not listed here. The German texts in the exact scan are not covered by this English check.

## Timing

One core, CPython, standard library only. Full run `python -m engine.k4_running_key_texts`: 60.6 seconds. The exact scan over 20 texts, 12 tableaux, both directions and one shuffle each took 22.2 seconds (per-text times in the scan table). The English null, the K4 fragment table and the six controls took 36.7 seconds. The unit tests take about 6 seconds and need no network.

## Reproduce

```
python -c "from engine.k4_running_key_texts import fetch_sources; print(fetch_sources())"
python -m engine.k4_running_key_texts
python -m unittest tests.test_k4_running_key_texts -v
```

`fetch_sources()` writes to `work/k4_running_key_texts/raw/`. The run verifies each file against the frozen letters hash before use.

## Result

Not solved. No plaintext claimed.

No frozen text places both clues under any of the twelve tableaux. Best partial matches are at chance. An English-prose running key from any source is statistically excluded for all twelve tableaux at the 1st-percentile threshold, with the control rates stated above.
