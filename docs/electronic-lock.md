# Simulated electronic lock

`engine/solvers/electronic_lock.py` is a headless in-process model of a modern short electronic code. The code is four digits, each from 0 through 9. One code is planted when the simulator is built. The function it returns answers only whether a try is that planted code. A wrong try is false. The matching try is true. The answer carries no other information: not which digit missed, not how close the try was, and not the code itself.

`recover_code` asks that function about codes in numeric order, from 0000 through 9999. It stops at the first accepted try. The full space is 10,000 tries. The search does not read the planted code except by calling the simulator.

`tests/test_electronic_lock.py` plants `4816`, checks that a wrong try fails, and checks that the recovered code is `4816`.

## Verification certificate

`engine/data/electronic_lock_certificate.json` stores the method name, the code string `4816`, the four digits, and the SHA-256 of the code string `4816`. The unit test recomputes that hash and runs the search again against the digits in the certificate.

## What this does not do

This opens only the simulated lock inside the test, not a real safe. It does not open a physical keypad, a mounted safe, a padlock, or any other container. It does not describe how to operate a lock. It is not a claim about army message Nr. 86 or any other undeciphered text.
