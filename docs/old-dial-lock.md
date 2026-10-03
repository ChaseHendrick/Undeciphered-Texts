# Simulated old dial lock

`engine/solvers/old_dial_lock.py` is a headless in-process model of an old three-number dial. Each number is an integer from 0 through 99. One combination is planted when the simulator is built. The function it returns answers only whether a try is that planted combination. A wrong try is false. The matching try is true. The answer carries no other information: not which wheel missed, not how close the try was, and not the combination itself.

`recover_combination` asks that function about triples in dial order, first wheel, then second, then third, each from 0 through 99. It stops at the first accepted try. The full space is 100 times 100 times 100, which is 1,000,000 tries. The search does not read the planted combination except by calling the simulator.

`tests/test_old_dial_lock.py` plants `3-11-7`, checks that a wrong try fails, and checks that the recovered combination is `3-11-7`.

This file is separate from `engine/solvers/sim_safe_lock.py`. That module is unchanged. Both are in-process boolean models. Neither one is a physical lock.

## Verification certificate

`engine/data/old_dial_lock_certificate.json` stores the method name, the combination string `3-11-7`, the three numbers, and the SHA-256 of the combination string `3-11-7`. The unit test recomputes that hash and runs the search again against the numbers in the certificate.

## What this does not do

This opens only the simulated lock inside the test, not a real safe. It does not open a physical dial, a mounted safe, a padlock, or any other container. It does not describe how to operate a lock. It is not a claim about army message Nr. 86 or any other undeciphered text.
