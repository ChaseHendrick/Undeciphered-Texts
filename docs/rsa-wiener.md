# RSA short private exponent recovery

`engine.solvers.rsa_wiener` uses only the public modulus and exponent to test continued-fraction candidates for a short private exponent. It includes ordinary convergents and the even-index increment in [Wiener's original paper](https://www.jannaud.fr/static/download/Travail/wiener.pdf), Sections III-V. Candidate factors must multiply to the modulus, pass the existing primality screen, and satisfy the RSA exponent relation. Below 2^64 the screen is deterministic; larger factors receive a fixed-base probable-prime screen.

```python
from engine.solvers.rsa_wiener import recover_wiener_key, solve_rsa_wiener
key = recover_wiener_key(8927, 2621)
assert (key.p, key.q, key.private_exponent) == (79, 113, 5)
result = solve_rsa_wiener(1511, modulus=8927, exponent=2621, plaintext_length=2)
assert result.plaintext == "0041"
```

Section V independently prints the key parameters above. The message65 and ciphertext1511 are synthetic controls using that published key. The certificate labels that distinction and hashes the raw recovered bytes. The original example uses an inverse modulo lambda(n), so its generalized probe matters.

`max_steps` counts generated continued-fraction terms, each with at most two probes. It permits0 through10000; the modulus is limited to4096 bits. Zero makes no probes. An exhausted budget returns `incomplete`, no factors and no plaintext. An exhausted expansion returns `not-found`; this does not prove that the key is secure. `search_complete` is also true once a verified key completes the requested recovery.

Recovered RSA plaintext is raw big-endian bytes represented as hexadecimal. An optional known byte length preserves leading zeros. No padding is removed. The attack covers weak short-exponent instances, with the usual balanced-factor sufficient condition explained in [Boneh's survey](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf), Section3. It is not a general RSA break.

```sh
python3 -m unittest tests.test_rsa_wiener -v
```
