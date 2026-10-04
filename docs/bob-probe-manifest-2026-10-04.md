# Bob probe manifest, 4 October 2026

The incumbent was not replaced. This is family recognition on synthetic machine settings, not a decipherment.

`engine.neural_generator_broad.probe_manifest` draws the same four blocks as `evaluate_incumbent`: restricted Enigma, restricted M-209, broad Enigma, broad M-209. Each row stores the generator, the true family, the SHA-256 of the ciphertext, the router's top family, and whether the true family is in the top three. The plaintext and the keys are not in the file. The weight file was only read.

| Item | Value |
| --- | --- |
| Seed | 20261005 |
| per_family | 32 |
| Rows | 128 |
| Format | 5 |
| Weight SHA-256 | `d8c985dfdaf2d1dd0e17cfdb8412d0f947221b3f9e30318169d9183145c5c825` |
| Weights changed | no |
| Plaintext | training Austen, letters only, windowed at 180 |
| Score time | 5.29 seconds |
| File | `engine/data/bob_probe_manifest_2026-10-04.json` |

| Generator | Family | Top 1 | Top 3 | Usual wrong family |
| --- | --- | ---: | ---: | --- |
| Restricted | Enigma | 18/32 | 32/32 | M-209, 14 times |
| Restricted | M-209 | 21/32 | 32/32 | Enigma, 10 times |
| Broad | Enigma | 19/32 | 31/32 | M-209, 12 times |
| Broad | M-209 | 15/32 | 32/32 | Enigma, 15 times |

Restricted top 1 is 39/64. Broad top 1 is 34/64. The earlier 16-sample probe was 14/32 restricted and 15/32 broad, too small to see a direction. On this larger draw the broadened settings are a little harder, and almost every miss is the other machine cipher. That is a measurement of the frozen format 5 file. It is not a new weight file, and it is not the 480-case or 204-case gate.
