"""Bounded Fermat factoring and textbook RSA plaintext recovery.

The public modulus, exponent, and ciphertext are sufficient when the RSA
modulus has two close prime factors. No factor or private key is supplied.
The algorithm checks at most max_steps consecutive values of a, beginning
at ceil(sqrt(n)), for a square a*a-n. Success gives n=(a-b)*(a+b).

Primary method source: Hanno Bock, Fermat Factorization in the Wild, 2023,
section 1.2, https://eprint.iacr.org/2023/026.pdf
Independent RSA vector: Handbook of Applied Cryptography, Example 8.4,
https://cacr.uwaterloo.ca/hac/about/chap8.pdf

Inputs are textbook RSA integers with two distinct odd prime factors.
The output is a raw integer and hexadecimal bytes, not decoded text or
RSA padding removal. An exhausted search claims no plaintext. This is
not a general RSA break or a solve of any unresolved historical cipher.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from math import gcd, isqrt

from engine.result import SolveResult


HAC_URL = "https://cacr.uwaterloo.ca/hac/about/chap8.pdf"
FERMAT_URL = "https://eprint.iacr.org/2023/026.pdf"
PRIMALITY_URL = "https://cacr.uwaterloo.ca/hac/about/chap4.pdf"
PRIMALITY_BASES_URL = "https://miller-rabin.appspot.com/"
DEFAULT_MAX_STEPS = 10_000

# Jim Sinclair's seven-base record covers integers below 2**64.
# Above that bound, fixed bases are a probable-prime screen, not a proof.
_DETERMINISTIC_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
_SCREEN_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53)


@dataclass(frozen=True)
class FermatFactorization:
    """Factors or an explicit exhausted square-check budget."""

    modulus: int
    p: int | None
    q: int | None
    checks: int
    max_steps: int
    start_a: int
    last_a: int | None
    prime_validation: str | None

    @property
    def found(self) -> bool:
        return self.p is not None and self.q is not None

    @property
    def exhausted(self) -> bool:
        return not self.found


def _require_integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer, not a boolean")


def _prime_screen(candidate: int) -> bool:
    """Miller-Rabin; deterministic below 2**64, a fixed-base screen above."""
    if candidate < 2:
        return False
    for prime in _SCREEN_BASES:
        if candidate % prime == 0:
            return candidate == prime
    odd_part = candidate - 1
    powers_of_two = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        powers_of_two += 1
    bases = _DETERMINISTIC_BASES if candidate < 2**64 else _SCREEN_BASES
    for base in bases:
        base %= candidate
        if base == 0:
            continue
        value = pow(base, odd_part, candidate)
        if value in (1, candidate - 1):
            continue
        for _ in range(powers_of_two - 1):
            value = pow(value, 2, candidate)
            if value == candidate - 1:
                break
        else:
            return False
    return True


def factor_fermat(modulus: int, *, max_steps: int = DEFAULT_MAX_STEPS) -> FermatFactorization:
    """Find two distinct odd RSA prime factors within a square-check budget.

    max_steps counts actual checks of a*a-modulus, including the first a.
    Zero requests an immediate exhausted result with zero checks. Square
    and even moduli, primes below 2**64, and encountered non-semiprime
    factors raise ValueError. Larger factors receive a probable-prime screen.
    """
    _require_integer(modulus, "modulus")
    _require_integer(max_steps, "max_steps")
    if modulus < 15 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd product of two distinct odd primes")
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")
    root = isqrt(modulus)
    if root * root == modulus:
        raise ValueError("square modulus does not have two distinct RSA primes")
    if modulus < 2**64 and _prime_screen(modulus):
        raise ValueError("prime modulus is not a two-prime RSA modulus")
    start_a = root + 1
    for offset in range(max_steps):
        a = start_a + offset
        squared_b = a * a - modulus
        b = isqrt(squared_b)
        if b * b != squared_b:
            continue
        p, q = a - b, a + b
        if p <= 1 or p == q or not _prime_screen(p) or not _prime_screen(q):
            raise ValueError("encountered factors are not two distinct RSA primes")
        return FermatFactorization(
            modulus=modulus,
            p=p,
            q=q,
            checks=offset + 1,
            max_steps=max_steps,
            start_a=start_a,
            last_a=a,
            prime_validation=(
                "deterministic_below_2_64" if q < 2**64 else "fixed_base_probable_prime_screen"
            ),
        )
    return FermatFactorization(
        modulus=modulus,
        p=None,
        q=None,
        checks=max_steps,
        max_steps=max_steps,
        start_a=start_a,
        last_a=start_a + max_steps - 1 if max_steps else None,
        prime_validation=None,
    )


def solve_rsa_fermat(
    ciphertext: int,
    *,
    modulus: int,
    exponent: int,
    max_steps: int = DEFAULT_MAX_STEPS,
    plaintext_length: int | None = None,
) -> SolveResult:
    """Recover textbook RSA from public parameters within max_steps checks.

    Successful plaintext is lowercase hexadecimal of big-endian bytes.
    The default byte length is minimal, with zero represented by one byte.
    Supply plaintext_length to preserve known leading zero bytes. Search
    exhaustion returns empty plaintext and status exhausted, never a guess.
    """
    _require_integer(ciphertext, "ciphertext")
    _require_integer(modulus, "modulus")
    _require_integer(exponent, "exponent")
    if not 0 <= ciphertext < modulus:
        raise ValueError("ciphertext must satisfy 0 <= ciphertext < modulus")
    if not 1 < exponent < modulus:
        raise ValueError("exponent must satisfy 1 < exponent < modulus")
    if plaintext_length is not None:
        _require_integer(plaintext_length, "plaintext_length")
        if plaintext_length < 1:
            raise ValueError("plaintext_length must be positive")
    factors = factor_fermat(modulus, max_steps=max_steps)
    details = {
        "modulus": modulus,
        "exponent": exponent,
        "ciphertext_integer": ciphertext,
        "checks": factors.checks,
        "max_steps": factors.max_steps,
        "start_a": factors.start_a,
        "last_a": factors.last_a,
        "mode": "bounded_public_parameter_attack",
        "encoding": "hex",
        "hash_encoding": "raw_big_endian_bytes",
        "source_url": HAC_URL,
        "attack_source_url": FERMAT_URL,
        "scope": (
            "Bounded Fermat factoring of close-prime textbook RSA. Public parameters only; "
            "no supplied factors or private key. No padding decoding, general RSA break, "
            "live-target attack, or unresolved historical decipherment."
        ),
    }
    public_key = f"n={modulus} e={exponent}"
    if factors.exhausted:
        details.update({"status": "exhausted", "claimed_plaintext": None})
        return SolveResult(
            method="rsa-fermat", plaintext="", key=public_key, score=0.0, details=details
        )
    p, q = factors.p, factors.q
    assert p is not None and q is not None
    phi = (p - 1) * (q - 1)
    if gcd(exponent, phi) != 1:
        raise ValueError("exponent is not invertible modulo (p-1)*(q-1)")
    private_exponent = pow(exponent, -1, phi)
    message = pow(ciphertext, private_exponent, modulus)
    if pow(message, exponent, modulus) != ciphertext:
        raise ValueError("recovered integer fails RSA reencryption check")
    minimum_length = max(1, (message.bit_length() + 7) // 8)
    byte_length = minimum_length if plaintext_length is None else plaintext_length
    if byte_length < minimum_length:
        raise ValueError("plaintext_length is too short for the recovered integer")
    plaintext = message.to_bytes(byte_length, "big")
    details.update(
        {
            "status": "recovered",
            "plaintext_integer": message,
            "plaintext_hex": plaintext.hex(),
            "plaintext_bytes": byte_length,
            "plaintext_sha256": hashlib.sha256(plaintext).hexdigest(),
            "factors": [p, q],
            "private_exponent": private_exponent,
            "prime_validation": factors.prime_validation,
            "reencryption_matches": True,
        }
    )
    return SolveResult(
        method="rsa-fermat",
        plaintext=plaintext.hex(),
        key=public_key,
        score=float(len(plaintext)),
        details=details,
    )


__all__ = [
    "DEFAULT_MAX_STEPS",
    "FERMAT_URL",
    "FermatFactorization",
    "HAC_URL",
    "PRIMALITY_BASES_URL",
    "PRIMALITY_URL",
    "factor_fermat",
    "solve_rsa_fermat",
]
