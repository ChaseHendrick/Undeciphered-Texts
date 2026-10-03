# Boneh / Hastad low-exponent RSA broadcast (known-answer)

`engine/solvers/rsa_broadcast.py` recovers a known plaintext from a **synthetic textbook-weak** RSA broadcast instance with public exponent e=3 and three pairwise-coprime moduli. `tests/test_rsa_broadcast.py` checks that CRT plus an integer cube root recovers that plaintext exactly.

This is a **known-answer** helper. It is **not** an attack on a real key, a live server, TLS, or a padding oracle. It is **not** an unknown-script reading. It does **not** claim Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the Voynich manuscript, or army message Nr. 86.

## Attack source

Dan Boneh, *Twenty Years of Attacks on the RSA Cryptosystem*, Notices of the AMS 46(2), 1999 (low public exponent / Hastad broadcast). Survey PDF:

[https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)

## Synthetic worked instance (printed in the certificate)

The moduli, exponent, ciphertexts, and plaintext are stored in `engine/data/rsa_broadcast_certificate.json` so the test is reproducible. They were generated for this repository; they are not taken from a live system.

| Field | Value |
| --- | --- |
| Attack | Boneh / Hastad low-exponent broadcast, e=3 |
| Plaintext | `ATTACK AT DAWN` |
| Encoding | ASCII bytes as a big-endian integer m |
| Recovery | CRT on the three ciphertexts, then integer cube root of the combined residue |

If the same m is encrypted as c_i = m^3 mod n_i for i=1,2,3 with pairwise-coprime n_i, and m^3 is smaller than N = n1*n2*n3, the CRT residue C mod N equals m^3 exactly, so m is the integer cube root of C.

## What the engine does

- `recover_broadcast_plaintext` runs CRT and the cube root.
- `solve_rsa_broadcast` returns a `SolveResult` whose plaintext is the recovered ASCII string.
- Defaults use the synthetic certificate numbers. Callers may pass matching ciphertext and modulus lists.
- No search against a live service. No padding-oracle loop. Not registered in `SOLVERS`.

## Verification certificate

`engine/data/rsa_broadcast_certificate.json` records the attack name, e, the three n values, the three ciphertexts, the plaintext, the plaintext integer, the instance label `synthetic`, the Boneh survey URL, and the SHA-256 of the plaintext. `RsaBroadcastCertificateTest` recomputes that hash and recovers the plaintext from the printed numbers. See [verification-certificates.md](verification-certificates.md).

## What it does not do

- Attack a real RSA key, a production certificate, a live server, TLS, or a padding oracle.
- Claim a break of modern cryptography in general.
- Read an unknown script or claim Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
