"""Boneh / Hastad low-exponent RSA broadcast attack (known-answer).

When the same plaintext integer m is RSA-encrypted under exponent e=3
with three pairwise-coprime moduli n1, n2, n3, and m^3 is smaller than
the product N = n1*n2*n3, the three ciphertexts determine a unique
residue C mod N with C = m^3. Recover m by an integer cube root.

Attack survey (fetched for citation, 2026-10-03):

  Dan Boneh, Twenty Years of Attacks on the RSA Cryptosystem,
  Notices of the AMS 46(2), 1999.
  https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf

The worked instance in this module is synthetic. The moduli, exponent,
ciphertexts, and plaintext are printed in
engine/data/rsa_broadcast_certificate.json so the test is reproducible.
This is a known-answer textbook-weak helper only. It does not attack a
real key, a live server, TLS, or a padding oracle. It does not claim
Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

from math import gcd
from pathlib import Path

from engine.result import SolveResult

BONEH_URL = "https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf"
ATTACK_NAME = "boneh_hastad_low_exponent_broadcast"

# Synthetic textbook-weak instance (printed in the certificate).
SYNTHETIC_PLAINTEXT = "ATTACK AT DAWN"
SYNTHETIC_E = 3
SYNTHETIC_N = (
    85070591730234638555338862520692053003,
    85070591730234640621374198776162121539,
    85070591730234642502942094294536669823,
)
SYNTHETIC_CIPHERTEXT = (
    64274844664854671026954882268024026781,
    5594213272610162248389733474821484004,
    58620680488843068566786338515411794190,
)
SYNTHETIC_PLAINTEXT_INTEGER = int.from_bytes(
    SYNTHETIC_PLAINTEXT.encode("ascii"), "big"
)

_SCOPE = (
    "Known-answer Boneh/Hastad low-exponent RSA broadcast (e=3) on a "
    "synthetic textbook-weak instance only; not an attack on a real key, "
    "live server, TLS, or padding oracle; not an unknown-script reading "
    "and not a claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, "
    "or army message Nr. 86."
)

_CERT_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "rsa_broadcast_certificate.json"
)


def integer_nth_root(value: int, degree: int) -> int:
    """Largest integer r with r**degree <= value. Binary search."""
    if degree < 1:
        raise ValueError("root degree must be at least 1")
    if value < 0:
        raise ValueError("integer root of a negative value is not supported")
    if value <= 1:
        return value
    high = 1 << ((value.bit_length() + degree - 1) // degree)
    low = 0
    while low < high:
        mid = (low + high) // 2
        powered = mid**degree
        if powered == value:
            return mid
        if powered < value:
            low = mid + 1
        else:
            high = mid
    candidate = low
    if candidate**degree > value:
        candidate -= 1
    return candidate


def chinese_remainder(remainders: list[int], moduli: list[int]) -> int:
    """Unique residue mod product(moduli) when the moduli are pairwise coprime."""
    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have the same length")
    if len(moduli) < 2:
        raise ValueError("need at least two moduli")
    for index, mod in enumerate(moduli):
        if mod <= 1:
            raise ValueError("each modulus must be greater than 1")
        for other in moduli[index + 1 :]:
            if gcd(mod, other) != 1:
                raise ValueError("moduli must be pairwise coprime")
    product = 1
    for mod in moduli:
        product *= mod
    total = 0
    for rem, mod in zip(remainders, moduli):
        ni = product // mod
        inv = pow(ni, -1, mod)
        total += rem * ni * inv
    return total % product


def plaintext_to_integer(text: str) -> int:
    """Encode ASCII plaintext as a big-endian integer."""
    data = text.encode("ascii")
    if not data:
        raise ValueError("plaintext must be non-empty ASCII")
    return int.from_bytes(data, "big")


def integer_to_plaintext(value: int) -> str:
    """Decode a big-endian integer back to ASCII plaintext."""
    if value < 0:
        raise ValueError("plaintext integer must be non-negative")
    if value == 0:
        return "\x00"
    length = (value.bit_length() + 7) // 8
    return value.to_bytes(length, "big").decode("ascii")


def rsa_encrypt_integer(message: int, exponent: int, modulus: int) -> int:
    """Textbook RSA: c = m^e mod n. Message must satisfy 0 <= m < n."""
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    if exponent < 1:
        raise ValueError("exponent must be at least 1")
    if message < 0 or message >= modulus:
        raise ValueError("message must satisfy 0 <= m < n")
    return pow(message, exponent, modulus)


def recover_broadcast_plaintext(
    ciphertexts: list[int] | tuple[int, ...],
    moduli: list[int] | tuple[int, ...],
    *,
    exponent: int = 3,
) -> int:
    """Recover m from e=3 broadcast ciphertexts via CRT and an integer cube root.

    Requires pairwise-coprime moduli, len(ciphertexts) == len(moduli) == exponent,
    and m^e < product(moduli) so the cube (or e-th) root is exact.
    """
    cts = [int(c) for c in ciphertexts]
    ns = [int(n) for n in moduli]
    if exponent != 3:
        raise ValueError("this helper implements the e=3 broadcast case only")
    if len(cts) != 3 or len(ns) != 3:
        raise ValueError("e=3 broadcast needs exactly three ciphertexts and moduli")
    for c, n in zip(cts, ns):
        if c < 0 or c >= n:
            raise ValueError("each ciphertext must satisfy 0 <= c < n")
    combined = chinese_remainder(cts, ns)
    root = integer_nth_root(combined, exponent)
    if root**exponent != combined:
        raise ValueError("combined residue is not a perfect e-th power")
    return root


def solve_rsa_broadcast(
    ciphertexts: list[int] | tuple[int, ...] | None = None,
    *,
    moduli: list[int] | tuple[int, ...] | None = None,
    exponent: int = SYNTHETIC_E,
) -> SolveResult:
    """Recover the synthetic (or supplied) broadcast plaintext as ASCII.

    Defaults load the synthetic certificate numbers. Known-answer only.
    """
    if ciphertexts is None:
        ciphertexts = SYNTHETIC_CIPHERTEXT
    if moduli is None:
        moduli = SYNTHETIC_N
    if int(exponent) != SYNTHETIC_E:
        raise ValueError("solve_rsa_broadcast expects e=3")
    message = recover_broadcast_plaintext(
        ciphertexts, moduli, exponent=int(exponent)
    )
    plain = integer_to_plaintext(message)
    return SolveResult(
        method="rsa_broadcast",
        plaintext=plain,
        key=f"e={exponent};n={','.join(str(n) for n in moduli)}",
        score=float(len(plain)),
        details={
            "attack": ATTACK_NAME,
            "e": int(exponent),
            "n": [str(n) for n in moduli],
            "ciphertext": [str(c) for c in ciphertexts],
            "plaintext_integer": str(message),
            "instance": "synthetic",
            "mode": "known_answer_broadcast",
            "scope": _SCOPE,
            "source_url": BONEH_URL,
            "certificate": str(_CERT_PATH.name),
        },
    )


__all__ = [
    "ATTACK_NAME",
    "BONEH_URL",
    "SYNTHETIC_CIPHERTEXT",
    "SYNTHETIC_E",
    "SYNTHETIC_N",
    "SYNTHETIC_PLAINTEXT",
    "SYNTHETIC_PLAINTEXT_INTEGER",
    "chinese_remainder",
    "integer_nth_root",
    "integer_to_plaintext",
    "plaintext_to_integer",
    "recover_broadcast_plaintext",
    "rsa_encrypt_integer",
    "solve_rsa_broadcast",
]
