# Bounded Fermat RSA recovery

`engine/solvers/rsa_fermat.py` factors a textbook RSA modulus with close prime factors and recovers a plaintext integer from public `n`, public `e`, and ciphertext `c`. The caller supplies no factor or private key. The search has an explicit square-check budget and reports exhaustion without a plaintext claim.

The method follows Hanno Bock's [Fermat Factorization in the Wild](https://eprint.iacr.org/2023/026.pdf), section 1.2. Write `n = a*a - b*b = (a-b)*(a+b)`. Starting at `ceil(sqrt(n))`, check successive integer values of `a` until `a*a-n` is a square. Close factors make their midpoint close to the starting value. Our implementation uses exact integer square roots and does at most `max_steps` square checks.

RSA integer recovery follows [Handbook of Applied Cryptography, section 8.2](https://cacr.uwaterloo.ca/hac/about/chap8.pdf). After factoring `n = p*q`, compute `phi = (p-1)*(q-1)`, `d = pow(e, -1, phi)`, and `m = pow(c, d, n)`. The implementation also verifies `pow(m, e, n) == c`.

## Published example

[HAC Example 8.4, printed page 287](https://cacr.uwaterloo.ca/hac/about/chap8.pdf) publishes an artificially small textbook RSA instance:

| Value | Integer |
| --- | --- |
| Public modulus n | 6012707 |
| Public exponent e | 3674911 |
| Ciphertext c | 3650502 |
| Expected plaintext m | 5234673 |
| Published prime factors p, q | 2357, 2551 |
| Published private exponent d | 422191 |

The source page was fetched and visually checked on 2026-10-03. The PDF SHA-256 was `1e685acec91de0de94f28503ef55a2c2d3f4d34de621e10424f92c53d50257f0`.

The certificate test supplies only the public modulus, exponent, ciphertext, search budget, and byte length. It checks `a=2453` and then `a=2454`, where `a*a-n = 97*97`. The second check recovers `p=2357` and `q=2551`; the derived private exponent decrypts to the independently printed `m=5234673`.

The integer becomes exactly three big-endian bytes, `4f df f1`. Their SHA-256 is `f48e45df90513516cd0aa5fbaed887b79e10ac6d10fddbd3d3092e7d8e162cf8`. This hashes recovered binary bytes, not decimal text or hexadecimal characters. The certificate uses integer and hexadecimal fields and omits language plaintext/ciphertext fields, so the text-only neural router does not consume this vector.

## API and bounds

```python
from engine.solvers.rsa_fermat import factor_fermat, solve_rsa_fermat

factors = factor_fermat(6012707, max_steps=2)
assert factors.found
assert (factors.p, factors.q) == (2357, 2551)
assert factors.checks == 2

result = solve_rsa_fermat(
    3650502,
    modulus=6012707,
    exponent=3674911,
    max_steps=2,
    plaintext_length=3,
)
assert result.details["plaintext_integer"] == 5234673
assert result.plaintext == "4fdff1"
```

`max_steps` counts tested values of `a`, including the first one. Its default is 10,000. A zero budget performs no square checks. If the budget ends first, `factor_fermat` returns `exhausted=True` and the exact check count. `solve_rsa_fermat` returns empty plaintext with `status: "exhausted"` and `claimed_plaintext: null`. Exhaustion says only that this bounded method did not recover factors.

Recovered plaintext is hexadecimal of big-endian bytes. The default byte length is minimal; the integer zero becomes one zero byte. Supply a known positive `plaintext_length` to preserve leading zero bytes. A requested length too short for the recovered integer raises `ValueError`.

The modulus must have two distinct odd prime factors. The implementation rejects even and square moduli, prime moduli below `2**64`, composite recovered factors, noninvertible exponents, invalid ciphertext ranges, negative budgets, and inappropriate types including booleans. It uses a Miller-Rabin screen following [HAC Algorithm 4.24](https://cacr.uwaterloo.ca/hac/about/chap4.pdf). Below `2**64`, it uses the [seven-base deterministic record credited to Jim Sinclair](https://miller-rabin.appspot.com/). Larger recovered factors receive a fixed sixteen-base probable-prime screen and are labeled `fixed_base_probable_prime_screen`; that is not a primality proof or a stated random-error probability.

## Validation and limits

`tests/test_rsa_fermat.py` failed with a missing-module import before implementation. The focused tests cover the published factor and plaintext outputs, raw-byte hash certificate, exact successful and exhausted check counts, zero budget, larger constructed close-prime instances, another public exponent, residues sharing a factor with the modulus, requested leading zeros, wide-gap exhaustion, and invalid inputs. Run with Python 3.10 or newer:

```bash
python3 -m unittest tests.test_rsa_fermat -v
```

The helper uses the Python standard library only and stays outside the text-only `SOLVERS` dispatch. It does not parse RSA keys, strip OAEP or PKCS padding, decode language, or target a live service. The checked certificate is a published small textbook example. This is an attack on the specific close-prime condition, not a general RSA break or a solve of an unresolved historical cipher or unknown script.
