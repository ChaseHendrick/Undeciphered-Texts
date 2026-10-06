# An Enigma trial for Bob, 5 October 2026

Bob gets Enigma right 12 times in 24 on the 480 development cases and M-209 12 times in 24. Those two families are 24 of his 51 misses. Two-square is 8 more.

The training generator draws Enigma with reflector B, rotors I, II and III in four orders, random rings, random start positions and no plugboard. Rings and positions matter only through their difference, the rotor offset, and through when the right rotor carries the middle one. `engine.neural_enigma_features` tries every left, middle and right offset and every phase of that carry, for each of the four orders: 4 x 17,576 x 26 settings, vectorized, about 0.27 seconds for a text. The left rotor's step and the middle rotor's double step are not modeled. A plugboard, another reflector or another rotor set defeats it.

Each setting is scored with Bob's own training-only digraph table. The trial returns three numbers: the best mean digraph log-likelihood, how many standard deviations that best stands above every tried setting, and the unigram score of the best setting's letters. No setting or plaintext leaves the module.

On a known key, rotors I, II, III, rings AAA and positions AAD, the trial finds offsets 0, 0 and 4 and a carry at letter 18, which is the true setting.

`engine.bob_enigma` draws eight ciphertexts per family from the training slice at the router's three lengths. The lowest Enigma score is 12.62 standard deviations. The highest score of any other family, over 152 texts, is 5.74. The trial separates the families completely on this draw.

The trial ranks families. It is not a break of any intercept.

## Training and the gate

`cipher_statistics_v10` is the format 5 prefix of 142 numbers plus these 3. Settings were chosen on the Austen validation split only. The official warm start, rate 0.005, 150 epochs, 256 samples per family, passed the gate against the format 5 incumbent on the same cases: 451 of 480 top one (was 429), 477 top three (unchanged), and 199 of 204 on the earlier benchmark (was 193). Enigma went from 12 to 24 of 24 and M-209 from 12 to 21. Rail fence fell from 21 to 19 and four-square from 22 to 21. The new SHA-256 is `149b88cae9de463b2447c74c5eb138a6a74818cfd01d70d4f6757f084c75c2da`.

The Wells audit was run after promotion; Wells was not used to train, select, calibrate or gate this file. 456 of 480 top one (the format 5 file scored 429), 479 top three (was 476), log loss 0.154 (was 0.278). Enigma 23 of 24 (was 7), M-209 22 of 24 (was 12).

The broad probe is the limit. With plugboards and other rotors, Enigma falls from 19 of 32 to 0, called M-209 29 times. Broad M-209 rises from 15 to 30. A trial that cannot see a plugboard reads as not Enigma.
