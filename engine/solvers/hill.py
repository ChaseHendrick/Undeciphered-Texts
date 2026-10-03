"""Known-key 2x2 Hill cipher solver.

Lester Hill's 1929 polygraphic cipher multiplies letter pairs by a 2x2
key matrix over Z/26Z (A=0 ... Z=25). With column vectors,

    [c1]   [a b] [p1]
    [c2] = [c d] [p2]   (mod 26)

Decryption multiplies by the inverse matrix. The determinant must be
coprime to 26.

The worked example used here is Arkadii Slinko, Algebra for Cryptology
(University of Auckland, 6 April 2013), "Hill's cryptosystem. Example 2":

  https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf

  K = [[3, 3], [2, 5]], plaintext HELP, ciphertext HIAT.

This module is a **known classical-cipher** solver. It recovers plaintext
only when the 2x2 key is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

import re

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Slinko, Algebra for Cryptology (Auckland, 6 April 2013), fetched 2026-10-02.
# https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf
SLINKO_URL = "https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf"
SLINKO_KEY = "3 3 2 5"
SLINKO_PLAIN = "HELP"
SLINKO_CIPHER = "HIAT"

_SCOPE = (
    "Known classical 2x2 Hill cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

_KEY_SPLIT = re.compile(r"[,\s;]+")


def _mod26(value: int) -> int:
    return value % 26


def _mod_inverse(value: int, modulus: int = 26) -> int:
    value = value % modulus
    for candidate in range(1, modulus):
        if (value * candidate) % modulus == 1:
            return candidate
    raise ValueError(f"no modular inverse of {value} mod {modulus}")


def hill_key(key: str) -> tuple[int, int, int, int]:
    """Parse a 2x2 Hill key into (a, b, c, d), row by row, entries mod 26.

    Accepts four integers separated by spaces, commas, or semicolons,
    for example ``3 3 2 5`` or ``3, 3; 2, 5``. The determinant must be
    coprime to 26 so the matrix is invertible.
    """
    parts = [part for part in _KEY_SPLIT.split(key.strip()) if part]
    if len(parts) != 4:
        raise ValueError("2x2 Hill key must be four integers, for example '3 3 2 5'")
    try:
        numbers = tuple(_mod26(int(part, 10)) for part in parts)
    except ValueError as exc:
        raise ValueError("2x2 Hill key must be four integers, for example '3 3 2 5'") from exc
    determinant = _mod26(numbers[0] * numbers[3] - numbers[1] * numbers[2])
    if determinant == 0:
        raise ValueError("Hill key matrix is not invertible mod 26")
    try:
        _mod_inverse(determinant)
    except ValueError as exc:
        raise ValueError("Hill key matrix is not invertible mod 26") from exc
    return numbers  # type: ignore[return-value]


def hill_inverse(key: str) -> tuple[int, int, int, int]:
    """Inverse of a 2x2 Hill key, row by row, entries mod 26."""
    a, b, c, d = hill_key(key)
    determinant = _mod26(a * d - b * c)
    det_inv = _mod_inverse(determinant)
    return (
        _mod26(det_inv * d),
        _mod26(-det_inv * b),
        _mod26(-det_inv * c),
        _mod26(det_inv * a),
    )


def _multiply_pairs(letters: str, matrix: tuple[int, int, int, int]) -> str:
    a, b, c, d = matrix
    if len(letters) % 2:
        raise ValueError("Hill ciphertext length must be a multiple of 2")
    out: list[str] = []
    for index in range(0, len(letters), 2):
        p1 = ord(letters[index]) - 65
        p2 = ord(letters[index + 1]) - 65
        c1 = _mod26(a * p1 + b * p2)
        c2 = _mod26(c * p1 + d * p2)
        out.append(chr(65 + c1))
        out.append(chr(65 + c2))
    return "".join(out)


def hill_encrypt(text: str, key: str) -> str:
    """Encrypt with a known 2x2 Hill matrix. Non-letters are dropped.

    An odd letter count is padded with a trailing X so the last pair is
    complete. The published HELP example is even and is not padded.
    """
    matrix = hill_key(key)
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    if len(plain) % 2:
        plain += "X"
    return _multiply_pairs(plain, matrix)


def hill_decrypt(text: str, key: str) -> str:
    """Decrypt with a known 2x2 Hill matrix.

    Non-letters are dropped. The letter count must be even: decryption
    does not strip padding, so a trailing X that was added on encrypt
    stays in the recovered letters.
    """
    inverse = hill_inverse(key)
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    return _multiply_pairs(cipher, inverse)


def solve_hill(text: str, *, key: str) -> SolveResult:
    """Recover 2x2 Hill plaintext when the key matrix is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    matrix = hill_key(key)
    rendered_key = " ".join(str(entry) for entry in matrix)
    plain_letters = hill_decrypt(text, rendered_key)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="hill",
        plaintext=rendered,
        key=rendered_key,
        score=float(len(plain_letters)),
        details={
            "key": rendered_key,
            "matrix": [[matrix[0], matrix[1]], [matrix[2], matrix[3]]],
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "block": 2,
            "scope": _SCOPE,
            "source_url": SLINKO_URL,
        },
    )


__all__ = [
    "SLINKO_CIPHER",
    "SLINKO_KEY",
    "SLINKO_PLAIN",
    "SLINKO_URL",
    "hill_decrypt",
    "hill_encrypt",
    "hill_inverse",
    "hill_key",
    "solve_hill",
]
