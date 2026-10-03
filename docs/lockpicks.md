# Lock picks

This note names common pick types from a page fetched on 2026-10-02 and points at the in-process simulators in `engine/solvers/lockpicks.py`. It does not give steps for opening a real lock.

Source: Wikipedia, "Lock picking". The names below are taken from the illustration caption and the tool headings on that page.

https://en.wikipedia.org/wiki/Lock_picking

The caption of the traditional pick set names these items from left to right: tension wrench, twist-flex tension wrench, offset diamond pick, ball pick, half-diamond pick, short hook, medium hook, city rake, snake (or C) rake.

Headings on the same page, recorded here as names only:

- Comb pick. A named tool on the page. This note does not describe how it is used.
- Tension wrench. The page also calls it a torsion wrench, and it names two placements: bottom of the keyway and top of the keyway.
- Half-diamond pick. The page describes a triangular tip. It says a normal set has about three half-diamond picks and a full-diamond pick.
- Hook pick. The page describes a hook-shaped tip and says the tool is sometimes called a feeler or a finger. The caption also names a short hook and a medium hook.
- Ball pick. The page describes a half-circle or full-circle tip and associates this name with wafer locks.
- Rake pick. The page names the snake rake, plus double-peak and triple-peak rakes, which it also calls Bogota rakes. The caption names a city rake and a snake (or C) rake.
- Decoder pick. Named on the page as an adjustable key.
- Bump key. Named on the page as its own key type. This note does not describe how one is used.

Under the wafer tumbler heading, the same page names jigglers or try-out keys, the pick gun (also called a snap gun), and the tubular lock pick. Those are names only here.

## Simulated locks

`engine/solvers/lockpicks.py` builds three headless models. Each plants one secret. The picker reads only yes or no answers.

Pin-tumbler. Four pins. Depths are integers from 0 through 5. One binding order and one cut per pin are planted: order 2, 0, 3, 1 and cuts `3-1-5-0`. `pin_is_next` is true for exactly one unset pin, the next pin in that order. `depth_sets` is true only when the depth equals that pin's cut. A true answer records the pin. A false answer changes nothing. `recover_pin_tumbler_key` asks only those two methods.

Wafer. Three wafers. Depths are integers from 0 through 3. A separate planted order, 0, 2, 1, and separate lifts, `1-3-2`. `wafer_is_next` and `lift_sets` are the only questions. `recover_wafer_key` asks only those two methods.

Keypad. A simple four-digit electronic keypad, each digit from 0 through 9. The planted code is `7395`. `code_matches` is true only when the entire code matches. It does not say which digit is wrong. `recover_keypad_code` tries codes from 0000 through 9999, which is 10,000 codes, and stops at the first true answer.

`tests/test_lockpicks.py` checks that a wrong answer is false and that each recovered secret equals the planted secret.

## Verification certificate

`engine/data/lockpicks_certificate.json` stores the pin-tumbler key string `3-1-5-0`, the wafer key string `1-3-2`, the keypad key string `7395`, and the SHA-256 of each string. The unit test recomputes those hashes and runs each search again.

## What this does not do

This opens only the simulated lock inside the test, not a real lock. It does not open a physical pin-tumbler, a wafer lock, an electronic keypad, a padlock, a safe, or any other container. It does not describe how to operate a lock. It is not a claim about army message Nr. 86 or any other undeciphered text.
