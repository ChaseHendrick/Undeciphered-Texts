# Fractionated Morse cipher (known-key solver)

`engine/solvers/fractionated_morse.py` decrypts a **known** fractionated Morse key. `tests/test_fractionated_morse.py` checks that this recovers a published worked example letter for letter, including the word spaces.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: [Practical Cryptography - Fractionated Morse cipher](http://practicalcryptography.com/ciphers/fractionated-morse-cipher/) (fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `ROUNDTABLECFGHIJKMPQSVWXYZ` |
| Plaintext | `DEFEND THE EAST` |
| Ciphertext | `ESOAVVLJRSSTRX` |

The page prints the plaintext in lowercase as "defend the east". Morse has no case. This solver returns A-Z letters and keeps the word spaces the page says are recovered, so the plaintext above is that text in uppercase.

The page converts the message to Morse with `x` between letters and `xx` between words, then pads with one `x` so the length is a multiple of 3:

```
-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-x
```

Groups of three are read against the keyed columns (dot, dash, x; the group `xxx` is omitted). The page states that `-..` is E and `x.x` is S. The full ciphertext is ESOAVVLJRSSTRX.

## What the engine does

- The key is a 26-letter mixed alphabet, or a keyword. A keyword is written first, without duplicate letters, and the unused letters of A-Z follow. `ROUNDTABLE` expands to the alphabet above.
- Encryption writes Morse (`.` dot, `-` dash), inserts `x` between symbols and `xx` between words, pads with `x` only when the length is not a multiple of 3, and maps each triple to a key letter.
- Decryption reverses the map, drops a trailing padding `x`, splits on `xx` for words and `x` for symbols, and returns uppercase text with single spaces between words.
- Grouping spaces in the ciphertext are ignored. Word spaces come from the Morse stream, not from the ciphertext skeleton.
- `solve_fractionated_morse(ciphertext, key=...)` returns a `SolveResult` whose plaintext is that recovered text.
- No blind key search is registered. Supply the key. This is the fractionated Morse cipher only.

## Verification certificate

`engine/data/fractionated_morse_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `FractionatedMorseCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks this published example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown fractionated Morse key.
