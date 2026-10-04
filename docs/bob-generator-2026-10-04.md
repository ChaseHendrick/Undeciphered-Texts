# Bob generator probe, 2026-10-04

The incumbent was not replaced. This is family recognition on synthetic machine settings, not a decipherment. A family probability does not recover plaintext.

The shipped file `engine/data/neural_router_v2_weights.json` was only read. Training still uses the old generator in `engine.neural_grade.encrypt_family`. The broadened sampler lives in `engine/neural_generator_broad.py` and does not write weights.

## Run

| Item | Value |
| --- | --- |
| Seed | 20261004 |
| per_family | 16 |
| Samples | 16 Enigma + 16 M-209 on each generator (64 ciphertexts) |
| Format | 5 |
| Weight SHA-256 | `d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825` |
| Weights changed | no (same SHA-256 before and after) |
| Score time | 2.580 seconds |
| Scorer | `engine.neural_router_v2.route_probabilities` |

## Plaintext

Training-side Austen only. `engine.neural.load_training_prose` reads `engine/data/neural_train_austen.txt` and skips leading `#` lines. The probe keeps the first 180 A-Z letters of that stream (the router window). SHA-256 of those 180 letters:

`2f68d58d7b4b88c8ee5168569d0273f88fdded0ab11f98caf79b28febde92084`

Every sample encrypts that same excerpt. It is not Doyle, not the Wells audit, not a certificate plaintext, and not a held-out document.

## Settings

One `random.Random(20261004)` draws, in order: restricted Enigma, restricted M-209, broad Enigma, broad M-209.

Restricted matches `encrypt_family`:

- Enigma rotors are only `(I II III)`, `(II I III)`, `(III II I)`, or `(I III II)`. Reflector B. Random three-letter rings and positions. Empty plugboard.
- M-209 external key is one letter from each wheel alphabet. Pins and lugs stay `BOUCHAUDY_PINS` and `BOUCHAUDY_LUGS`.

Broad:

- Enigma rotors are any ordered triple from I, II, III, IV, V with no repeat. Reflector B or C. Rings and positions are three A-Z letters. The plugboard has 0 to 6 disjoint pairs.
- M-209 pins are a 0/1 string per wheel, with lengths taken from `WHEEL_SIZES`, then stored in the letter-or-underscore form `m209_encrypt` accepts. An all-zero wheel is rejected by turning one pin on. Lugs are 27 legal `left-right` specs, at least one of them active, and not a copy of `BOUCHAUDY_LUGS`.

Each ciphertext was decrypted with `enigma_decrypt` or `m209_decrypt` and matched the excerpt before scoring.

## Counts

Restricted generator (old settings):

| Family | Top 1 | Top 3 | Total |
| --- | --- | --- | --- |
| enigma | 6 | 16 | 16 |
| m209 | 8 | 16 | 16 |
| both | 14 | 32 | 32 |

Broad generator:

| Family | Top 1 | Top 3 | Total |
| --- | --- | --- | --- |
| enigma | 9 | 16 | 16 |
| m209 | 6 | 15 | 16 |
| both | 15 | 31 | 32 |

Broad Enigma checks, out of 16:

- nonempty plugboard: 14
- a rotor outside {I, II, III}: 14
- both of those: 12

Broad M-209 samples whose pins differ from `BOUCHAUDY_PINS`: 16 of 16.

## What this does not show

The incumbent was not replaced. These counts are family recognition on synthetic machine settings, not a decipherment. They are not the frozen 480-case or 204-case comparisons, and they are not the Wells audit (7/24 Enigma and 12/24 M-209 under the old generator, on other prose). Sixteen keys on one 180-letter training excerpt cannot decide whether the restricted settings are a shortcut. On this probe the combined top-1 count was 14/32 restricted and 15/32 broad. Top 3 was 32/32 restricted and 31/32 broad. Moves of a few hits on 16 samples are too small to promote or reject a model. No historical message was solved.
