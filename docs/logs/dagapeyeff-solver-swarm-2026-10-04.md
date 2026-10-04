# Solver swarm

4 October 2026. No letter string is stored.

The 196 cells were labeled A through Y and handed to the repo's own solvers. Caesar, Vigenere through period 8, and a 400-step substitution. The plaintext each solver printed was discarded. Only the score per letter was kept. Shuffled cells got the same solvers.

| Solver | Per letter | Prose, same solver | Shuffles as high |
| --- | ---: | ---: | ---: |
| Caesar | -3.4459 | -2.9415 | 33 of 40 |
| Vigenere, it chose period 3 | -3.7393 | -2.4363 | 7 of 20 |
| Substitution, reading flag false | -3.0858 | -2.6585 | 8 of 8 |

Period 3 was already a failed key. The substitution score on the printed order does not beat a single shuffle. None of the three reaches prose.

The solver refuses the swarm. No letters are kept.

The chain ends at `5be84ca8878bf1bb9392495f9ad1a6637ad024d7b985ae30f565608b34e35898`.

No letter string is stored.
