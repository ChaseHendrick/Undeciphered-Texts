"""Wiener continued-fraction recovery of weak RSA private exponents.

Uses public n,e only. Each continued-fraction term tests its ordinary
convergent and Wiener's even-index increment. The latter also recovers
the lambda(n) key in Section V of the original paper: n=8927,e=2621,
d=5,p=113,q=79,k=3,g=2. This is a bounded weak-instance attack, not a
general RSA break, padding decoder, or historical decipherment.

Primary sources inspected 2026-10-03:
https://www.jannaud.fr/static/download/Travail/wiener.pdf (original 1990 paper)
https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf (Boneh, Section 3)
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from math import gcd, isqrt, lcm

from engine.result import SolveResult
from engine.solvers.rsa_fermat import _prime_screen

WIENER_URL = "https://www.jannaud.fr/static/download/Travail/wiener.pdf"
SURVEY_URL = "https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf"
MAX_BITS = 4096


@dataclass(frozen=True)
class WienerKey:
    modulus: int
    exponent: int
    status: str
    steps: int
    max_steps: int
    search_complete: bool
    p: int | None = None
    q: int | None = None
    private_exponent: int | None = None
    k: int | None = None
    g: int | None = None
    prime_validation: str | None = None


def _integer(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")


def _probe(n: int, e: int, k: int, denominator: int) -> tuple[int, int, int, int] | None:
    if k <= 0 or denominator <= 0:
        return None
    product = e * denominator
    phi, g = divmod(product, k)
    candidates = [(phi, g)]
    if (product - 1) % k == 0:
        candidates.append(((product - 1) // k, 1))
    for phi, g in candidates:
        if phi <= 0 or g <= 0 or denominator % g:
            continue
        total = n - phi + 1
        discriminant = total * total - 4 * n
        if total <= 0 or discriminant <= 0:
            continue
        root = isqrt(discriminant)
        if root * root != discriminant or (total - root) % 2:
            continue
        p, q = (total - root) // 2, (total + root) // 2
        if p <= 2 or p == q or p * q != n:
            continue
        d = denominator // g
        if d <= 1 or (e * d - 1) % lcm(p - 1, q - 1):
            continue
        if not _prime_screen(p) or not _prime_screen(q):
            continue
        return p, q, d, g
    return None


def recover_wiener_key(modulus: int, exponent: int, *, max_steps: int = 10000) -> WienerKey:
    """Recover a short exponent with exact factor and exponent checks.

max_steps counts generated continued-fraction terms, including the first.
Each term uses at most two probes. Bounds are 4096-bit n and 10000 terms.
A completed negative search only rules out these continued-fraction probes.
Factors below2**64 are deterministically screened; larger ones are probable.
"""
    for value, name in ((modulus, "modulus"), (exponent, "exponent"), (max_steps, "max_steps")):
        _integer(value, name)
    if modulus < 15 or modulus % 2 == 0 or modulus.bit_length() > MAX_BITS:
        raise ValueError("modulus must be odd, at least15, and at most4096 bits")
    if isqrt(modulus) ** 2 == modulus or (modulus < 2**64 and _prime_screen(modulus)):
        raise ValueError("modulus must be a product of two distinct odd primes")
    if not 1 < exponent < modulus:
        raise ValueError("exponent must satisfy1 < exponent < modulus")
    if not 0 <= max_steps <= 10000:
        raise ValueError("max_steps must be between0 and10000")
    numerator, denominator = exponent, modulus
    h_prev2, h_prev = 0, 1
    k_prev2, k_prev = 1, 0
    steps = 0
    while denominator and steps < max_steps:
        quotient, remainder = divmod(numerator, denominator)
        h = quotient * h_prev + h_prev2
        k = quotient * k_prev + k_prev2
        probes = [(h, k)]
        if steps % 2 == 0:
            probes.append((h + h_prev, k + k_prev))
        steps += 1
        for candidate_k, candidate_denominator in probes:
            found = _probe(modulus, exponent, candidate_k, candidate_denominator)
            if found is not None:
                p, q, d, g = found
                return WienerKey(modulus, exponent, "recovered", steps, max_steps, True,
                                 p, q, d, candidate_k, g,
                                 "deterministic_below_2_64" if q < 2**64 else "fixed_base_probable_prime_screen")
        h_prev2, h_prev = h_prev, h
        k_prev2, k_prev = k_prev, k
        numerator, denominator = denominator, remainder
    complete = denominator == 0
    return WienerKey(modulus, exponent, "not-found" if complete else "incomplete",
                     steps, max_steps, complete)


def solve_rsa_wiener(ciphertext: int, *, modulus: int, exponent: int,
                     max_steps: int = 10000, plaintext_length: int | None = None) -> SolveResult:
    """Decrypt raw textbook RSA bytes after recovering a weak private key."""
    _integer(ciphertext, "ciphertext")
    _integer(modulus, "modulus")
    if not 0 <= ciphertext < modulus:
        raise ValueError("ciphertext must satisfy0 <= ciphertext < modulus")
    if plaintext_length is not None:
        _integer(plaintext_length, "plaintext_length")
        if not 1 <= plaintext_length <= 4096:
            raise ValueError("plaintext_length must be between1 and4096 bytes")
    recovered = recover_wiener_key(modulus, exponent, max_steps=max_steps)
    details = {"mode": "bounded_public_parameter_attack", "status": recovered.status,
               "steps": recovered.steps, "max_steps": max_steps,
               "search_complete": recovered.search_complete,
               "claimed_plaintext": None, "encoding": "hex",
               "source_url": WIENER_URL, "survey_url": SURVEY_URL,
               "scope": "Short-exponent textbook RSA only; no general RSA break or padding decoding."}
    if recovered.private_exponent is None:
        return SolveResult("rsa-wiener", "", f"n={modulus} e={exponent}", 0.0, details)
    message = pow(ciphertext, recovered.private_exponent, modulus)
    if pow(message, exponent, modulus) != ciphertext:
        raise ValueError("recovered integer failed reencryption")
    minimum = max(1, (message.bit_length() + 7) // 8)
    if plaintext_length is not None and plaintext_length < minimum:
        raise ValueError("plaintext_length is too short for the recovered integer")
    plain = message.to_bytes(minimum if plaintext_length is None else plaintext_length, "big")
    details.update({"plaintext_integer": message, "plaintext_sha256": hashlib.sha256(plain).hexdigest(),
                    "plaintext_bytes": len(plain), "private_exponent": recovered.private_exponent,
                    "factors": [recovered.p, recovered.q], "k": recovered.k, "g": recovered.g,
                    "prime_validation": recovered.prime_validation, "reencryption_matches": True})
    return SolveResult("rsa-wiener", plain.hex(), f"d={recovered.private_exponent}", 0.0, details)


__all__ = ["WIENER_URL", "SURVEY_URL", "WienerKey", "recover_wiener_key", "solve_rsa_wiener"]
