"""Textbook RSA common-modulus recovery using public parameters only.

If c1 = m**e1 mod n and c2 = m**e2 mod n, with coprime e1 and e2,
extended Euclid gives a*e1 + b*e2 = 1. Thus c1**a * c2**b mod n
recovers m when the ciphertexts are invertible. Negative powers use
modular inverses. The recovered candidate must reencrypt to both inputs.

Sources inspected 2026-10-03:
https://cacr.uwaterloo.ca/hac/about/chap8.pdf, section 8.2.2(vi), page 289.
https://www.acsu.buffalo.edu/~mblanton/cse664/lecture14.pdf, slide 12.

The certificate is synthetic, with no historical decryption claim. This
helper does not recover private keys or attack a configured service. It
does not handle randomized RSA padding, unknown scripts, or unsolved
historical challenges.
"""

from __future__ import annotations

import hashlib
from math import gcd

from engine.result import SolveResult


HAC_URL = "https://cacr.uwaterloo.ca/hac/about/chap8.pdf"
ALGEBRA_URL = "https://www.acsu.buffalo.edu/~mblanton/cse664/lecture14.pdf#page=12"
ATTACK_NAME = "rsa_common_modulus_coprime_exponents"


def _integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")


def common_modulus_coefficients(e1: int, e2: int) -> tuple[int, int]:
    """Return signed coefficients a, b satisfying a*e1 + b*e2 = 1."""
    _integer(e1, "e1")
    _integer(e2, "e2")
    if e1 <= 1 or e2 <= 1:
        raise ValueError("public exponents must be greater than 1")
    old_r, r = e1, e2
    old_a, a = 1, 0
    old_b, b = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_a, a = a, old_a - quotient * a
        old_b, b = b, old_b - quotient * b
    if old_r != 1:
        raise ValueError("public exponents must be coprime")
    return old_a, old_b


def _signed_modular_power(base: int, exponent: int, modulus: int) -> int:
    if exponent >= 0:
        return pow(base, exponent, modulus)
    return pow(pow(base, -1, modulus), -exponent, modulus)


def _recover(c1: int, c2: int, e1: int, e2: int, n: int) -> tuple[int, int, int]:
    _integer(n, "n")
    _integer(c1, "c1")
    _integer(c2, "c2")
    if n <= 3 or n % 2 == 0:
        raise ValueError("RSA modulus must be odd and greater than 3")
    a, b = common_modulus_coefficients(e1, e2)
    if not 0 <= c1 < n or not 0 <= c2 < n:
        raise ValueError("ciphertexts must satisfy 0 <= c < n")
    if c1 == 0 or c2 == 0:
        if c1 == c2 == 0:
            return 0, a, b
        raise ValueError("inconsistent ciphertexts: only one ciphertext is zero")
    if gcd(c1, n) != 1 or gcd(c2, n) != 1:
        raise ValueError("ciphertexts must be invertible modulo n")
    message = (_signed_modular_power(c1, a, n) * _signed_modular_power(c2, b, n)) % n
    if pow(message, e1, n) != c1 or pow(message, e2, n) != c2:
        raise ValueError("inconsistent ciphertexts: candidate does not reencrypt to both inputs")
    return message, a, b


def recover_common_modulus_plaintext(c1: int, c2: int, *, e1: int, e2: int, n: int) -> int:
    """Recover an integer from same-message ciphertexts and public parameters.

    Both ciphertexts must be units modulo n, except that (0, 0) returns
    the zero message. Noncoprime exponents and incompatible inputs fail.
    No private key or plaintext is an argument.
    """
    message, _a, _b = _recover(c1, c2, e1, e2, n)
    return message


def solve_rsa_common_modulus(
    c1: int,
    c2: int,
    *,
    e1: int,
    e2: int,
    n: int,
    byte_length: int | None = None,
) -> SolveResult:
    """Recover hex bytes from public inputs, optionally preserving leading zeros.

    With no byte_length, the integer uses its shortest nonempty big-endian
    encoding. RSA ciphertexts alone do not preserve leading zero bytes.
    """
    if byte_length is not None:
        _integer(byte_length, "byte_length")
        if byte_length <= 0:
            raise ValueError("byte_length must be greater than zero")
    message, a, b = _recover(c1, c2, e1, e2, n)
    minimum = max(1, (message.bit_length() + 7) // 8)
    if byte_length is not None and byte_length < minimum:
        raise ValueError("byte_length is too short for the recovered integer")
    plain = message.to_bytes(minimum if byte_length is None else byte_length, "big")
    return SolveResult(
        method="rsa_common_modulus",
        plaintext=plain.hex(),
        key=f"public n={n};e1={e1};e2={e2}",
        score=0.0,
        details={
            "attack": ATTACK_NAME,
            "mode": "public_parameter_attack",
            "input_encoding": "integers",
            "plaintext_encoding": "hex",
            "plaintext_integer": str(message),
            "plaintext_sha256": hashlib.sha256(plain).hexdigest(),
            "bytes": len(plain),
            "byte_length_mode": "minimal" if byte_length is None else "supplied",
            "modulus": str(n),
            "public_exponents": [e1, e2],
            "bezout_coefficients": [a, b],
            "reencryption_matches": True,
            "source_url": HAC_URL,
            "algorithm_source_url": ALGEBRA_URL,
            "scope": "Same-message textbook RSA with a shared modulus and coprime exponents; no private-key input or randomized-padding removal.",
        },
    )


__all__ = [
    "ALGEBRA_URL",
    "ATTACK_NAME",
    "HAC_URL",
    "common_modulus_coefficients",
    "recover_common_modulus_plaintext",
    "solve_rsa_common_modulus",
]
