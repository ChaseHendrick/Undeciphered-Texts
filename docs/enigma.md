# Three-rotor Enigma (known-key historical machine)

`engine/solvers/enigma.py` decrypts a **known** three-rotor Enigma key. `tests/test_enigma.py` checks that this recovers a published worked example letter for letter.

This is a **known-key historical machine**. It is the three-rotor Enigma I (the military form of the commercial Enigma): three rotors chosen from I–V, a fixed reflector B or C, the military identity entry wheel, and an optional plugboard. The key is supplied. It is **not** a break of an unsolved intercept. It is **not** a claim about army message Nr. 86 or Kryptos K4, and it does not read Linear A, the Indus script, the Voynich manuscript, or rongorongo.

## Published worked example (fetched)

Source: [Wikipedia — Enigma rotor details](https://en.wikipedia.org/wiki/Enigma_rotor_details) (fetched 2026-10-02). The machine itself is described in [Enigma machine](https://en.wikipedia.org/wiki/Enigma_machine).

The rotor-details page states: with the rotors I, II and III (from left to right), wide B-reflector, all ring settings in A-position, and start position AAA, typing AAAAA produces BDZGO. No plugboard pairs are used.

| Field | Value |
| --- | --- |
| Rotors (left to right) | I, II, III |
| Reflector | B (wide B) |
| Ring settings | AAA |
| Start positions | AAA |
| Plugboard | none |
| Plaintext | `AAAAA` |
| Ciphertext | `BDZGO` |

The same page gives a second check: all ring settings in the B-position, same rotors, reflector, and start, typing AAAAA produces `EWTYX`. It also lists the step sequence for rotors I II III, including the middle-rotor double step (`AAU` then `AAV`, `ABW`, `ABX`; `ADU` then `ADV`, `AEW`, `BFX`, `BFY`).

The rotor steps before the lamp is lit. Notch letters follow that page: I leaves Q for R, II leaves E for F, III leaves V for W.

## What the engine does

- Drop non-letters. Step the rotors (right rotor every letter; middle rotor when the right rotor is on its notch; left and middle together when the middle rotor is on its notch), then pass the letter through the plugboard, the three rotors, the reflector, back through the rotors, and the plugboard again.
- Encrypt and decrypt are the same function. Reset the start positions before the second pass.
- `solve_enigma(ciphertext, rotors=..., reflector=..., rings=..., positions=..., plugboard=...)` returns a `SolveResult` whose plaintext is those recovered letters.
- No search over rotor order, rings, positions, or plugboard is registered. Supply the key.

## Verification certificate

`engine/data/enigma_certificate.json` records the cipher name, plaintext, ciphertext, key settings (rotors, reflector, rings, positions, plugboard), source URL, and the SHA-256 of the plaintext. `EnigmaCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Break an unsolved intercept, or search an unknown daily key.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Claim a solution of Kryptos K4.
- Implement the four-rotor naval M4, the commercial A/B wirings, or a QWERTZ entry wheel. Those are different machines. This file is the three-rotor Enigma I example Wikipedia prints.
