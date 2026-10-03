# Simulated safe lock

`engine/solvers/sim_safe_lock.py` is a headless in-process model of a three-number dial. Each number is an integer from 0 through 99. One combination is planted when the simulator is built. The function it returns answers only whether a try is that planted combination. A wrong try is false. The matching try is true. The answer carries no other information: not which wheel missed, not how close the try was, and not the combination itself.

`recover_combination` asks that function about triples in dial order, first wheel, then second, then third, each from 0 through 99. It stops at the first accepted try. The full space is 100 times 100 times 100, which is 1,000,000 tries. The search does not read the planted combination except by calling the simulator.

`tests/test_sim_safe_lock.py` plants `19-73-41`, checks that a wrong try fails, and checks that the recovered combination is `19-73-41`.

## Verification certificate

`engine/data/sim_safe_lock_certificate.json` stores the method name, the combination string `19-73-41`, the three numbers, and the SHA-256 of the combination string `19-73-41`. The unit test recomputes that hash and runs the search again against the numbers in the certificate.

## What this does not do

This cracks only the simulated lock inside the test, not a real safe. It does not open a physical dial, a mounted safe, a padlock, or any other container. It does not describe how to operate a lock. It is not a claim about army message Nr. 86 or any other undeciphered text.
