"""Affine known-key solver: E(x) = (a*x + b) mod 26.

Each A-Z letter is a number 0..25. Encryption is the affine map
E(x) = (a*x + b) mod 26. Decryption multiplies by the modular inverse
of a: D(y) = a^{-1} * (y - b) mod 26. a must be coprime to 26.

The published worked example this module is checked against is the
Wikipedia Affine cipher page (fetched 2026-10-02):

  https://en.wikipedia.org/wiki/Affine_cipher

  plaintext  AFFINECIPHER  ("AFFINE CIPHER" with the space dropped)
  a, b       5, 8
  ciphertext IHHWVCSWFRCP

This module is a **known classical-cipher** solver. It recovers plaintext
only when a and b are supplied. It is **not** an unknown-script reading
and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Wikipedia worked example (fetched 2026-10-02).
# https://en.wikipedia.org/wiki/Affine_cipher
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Affine_cipher"
WIKIPEDIA_PLAIN = "AFFINECIPHER"
WIKIPEDIA_CIPHER = "IHHWVCSWFRCP"
WIKIPEDIA_A = 5
WIKIPEDIA_B = 8

_COPRIME_A = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)

_SCOPE = (
    "Known classical affine cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def affine_key(a: int, b: int) -> tuple[int, int]:
    """Normalize a and b into 0..25 and require gcd(a, 26) = 1."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("affine key a and b must be integers")
    try:
        a_i = int(a)
        b_i = int(b)
    except (TypeError, ValueError) as exc:
        raise ValueError("affine key a and b must be integers") from exc
    a_i %= 26
    b_i %= 26
    if a_i not in _COPRIME_A:
        raise ValueError("affine multiplier a must be coprime to 26")
    return a_i, b_i


def mod_inverse(a: int, modulus: int = 26) -> int:
    """Multiplicative inverse of a modulo modulus. a must be coprime to modulus."""
    a_norm = a % modulus
    for inv in range(1, modulus):
        if (a_norm * inv) % modulus == 1:
            return inv
    raise ValueError(f"no modular inverse for {a} mod {modulus}")


def _map_letters(text: str, a: int, b: int, *, decrypt: bool) -> str:
    multiplier, shift = affine_key(a, b)
    stream = letters_only(text)
    if not stream:
        raise ValueError("text has no letters")
    if decrypt:
        inverse = mod_inverse(multiplier)
        nums = [((ord(ch) - 65 - shift) * inverse) % 26 for ch in stream]
    else:
        nums = [(multiplier * (ord(ch) - 65) + shift) % 26 for ch in stream]
    return "".join(chr(65 + n) for n in nums)


def affine_encrypt(text: str, a: int, b: int) -> str:
    """Encrypt with a known affine key. Non-letters are dropped."""
    return _map_letters(text, a, b, decrypt=False)


def affine_decrypt(text: str, a: int, b: int) -> str:
    """Decrypt with a known affine key. Non-letters are dropped."""
    return _map_letters(text, a, b, decrypt=True)


def format_key(a: int, b: int) -> str:
    """Stable key string recorded on SolveResult and in the certificate."""
    multiplier, shift = affine_key(a, b)
    return f"a={multiplier},b={shift}"


def solve_affine(text: str, *, a: int, b: int) -> SolveResult:
    """Recover affine plaintext when a and b are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    multiplier, shift = affine_key(a, b)
    plain_letters = affine_decrypt(text, multiplier, shift)
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    return SolveResult(
        method="affine",
        plaintext=rendered,
        key=format_key(multiplier, shift),
        score=float(len(plain_letters)),
        details={
            "a": multiplier,
            "b": shift,
            "a_inverse": mod_inverse(multiplier),
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "scope": _SCOPE,
            "source_url": WIKIPEDIA_URL,
        },
    )


__all__ = [
    "WIKIPEDIA_A",
    "WIKIPEDIA_B",
    "WIKIPEDIA_CIPHER",
    "WIKIPEDIA_PLAIN",
    "WIKIPEDIA_URL",
    "affine_decrypt",
    "affine_encrypt",
    "affine_key",
    "format_key",
    "mod_inverse",
    "solve_affine",
]
