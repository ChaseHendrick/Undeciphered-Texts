# RSA common-modulus attack

The [Handbook of Applied Cryptography, section 8.2.2(vi), page 289](https://cacr.uwaterloo.ca/hac/about/chap8.pdf) describes public recovery when a message is encrypted for different public exponents under one shared RSA modulus. [Marina Blanton's University at Buffalo lecture, slide 12](https://www.acsu.buffalo.edu/~mblanton/cse664/lecture14.pdf#page=12) gives the algebra used here.

For ciphertexts `c1 = m^e1 mod n` and `c2 = m^e2 mod n`, coprime exponents give integers `a` and `b` such that `a*e1 + b*e2 = 1`. The attacker computes `c1^a * c2^b mod n`. A negative exponent requires a modular inverse. The candidate must reencrypt to both supplied ciphertexts before it is accepted.

`engine/solvers/rsa_common_modulus.py` needs only public `c1`, `c2`, `e1`, `e2`, and `n`. It rejects invalid integer inputs, an even or small modulus, out-of-range ciphertexts, noncoprime exponents, noninvertible ciphertexts, and incompatible message pairs. The zero pair returns zero. The helper checks public algebraic consistency; it does not factor the modulus or prove that supplied parameters form a valid RSA key.

`solve_rsa_common_modulus` returns hex plaintext and encoding metadata. Its optional `byte_length` preserves externally known leading zero bytes; otherwise the result uses the shortest nonempty big-endian encoding. Leading zero bytes cannot be inferred from integer ciphertexts.

The certificate is a clearly labeled synthetic fixture with independent literal ciphertexts and a SHA-256 of recovered raw bytes. It uses a 128-bit modulus and public exponents 17 and 65537. No private key is passed to the attacker. Tests cover both negative-exponent positions, swapped inputs, leading zeros, and mismatched plaintexts. This work makes no historical decryption claim and does not implement randomized-padding removal or an attack on a configured service.
