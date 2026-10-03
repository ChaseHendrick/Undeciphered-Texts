# Route cipher (known-key solver)

`engine/solvers/route.py` decrypts a **known** grid width, fill order, and route. `tests/test_route.py` checks that this recovers a published worked example letter for letter.

This is a **known classical-cipher** solver. It is **not** an unknown-script reading. It is **not** a claim about army message Nr. 86, and it does not read Linear A, the Indus script, the Voynich manuscript, rongorongo, or Kryptos K4.

## Published worked example (fetched)

Source: Crypto-IT, [Route Cipher](http://www.crypto-it.net/eng/simple/route-cipher.html) (page dated 2020-03-09, fetched 2026-10-02).

| Field | Value |
| --- | --- |
| Key | `width=3;fill=rows;route=spiral-cw-top-right` |
| Plaintext | `BRIGHTONANDHOVE` |
| Ciphertext | `ITAHEVONOGBRHND` |

The page encrypts "Brighton and Hove". Non-letters are dropped and letters are capitalized. The secret width is 3. Letters are written row by row, left to right:

```
B R I
G H T
O N A
N D H
O V E
```

They are read in a clockwise inward spiral starting at the top right, first step down: `ITAHEVONOGBRHND`.

A second published grid is on [Wikipedia, Transposition cipher, Route cipher](https://en.wikipedia.org/wiki/Transposition_cipher#Route_cipher) (fetched 2026-10-02). The sentence "WE ARE DISCOVERED FLEE AT ONCE" is written down the columns of a 3 by 9 grid, and the page draws nulls J and X in the last column. The same spiral reads `EJXCTEDECDAEWRIORFEONALEVSE`. The test recovers `WEAREDISCOVEREDFLEEATONCEJX`, the letters in that grid, with key `width=9;fill=cols;route=spiral-cw-top-right`. That check is the published grid, not a reading of an unknown script.

## What the engine does

- Drop non-letters. The key is `width` or `height`, `fill` (`rows` or `cols`), and `route`.
- The only route name is `spiral-cw-top-right`: clockwise, inward, start at the top-right cell, first step down.
- The letter count must fill the rectangle. The solver does not add nulls.
- Encryption writes the fill, then reads the spiral. Decryption writes the spiral, then reads the fill.
- `solve_route(ciphertext, key=...)` returns a `SolveResult` whose plaintext is those recovered letters (spaces in the ciphertext skeleton are kept).
- No blind route search is registered. Supply the key.

## Verification certificate

`engine/data/route_certificate.json` records the cipher name, plaintext, ciphertext, key, source URL, and the SHA-256 of the plaintext. `RouteCertificateTest` recomputes that hash and decrypts the ciphertext so the recovered text matches. See [verification-certificates.md](verification-certificates.md). The certificate checks the Crypto-IT example only.

## What it does not do

- Read an unknown script or an undeciphered manuscript.
- Claim a solution of Truppenschlüssel / army message Nr. 86.
- Search for an unknown route, width, or fill order.
