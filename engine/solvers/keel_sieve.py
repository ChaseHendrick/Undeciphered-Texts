"""Keel sieve: an original letter cipher for this repository.

The rule is not rows of five, a triangular-index latch, Playfair, bifid,
Vigenère, Porta, or two-square. It is not a reading of any ancient script
and it is not a reading of army message Nr. 86. Encrypt and decrypt are
inverses on the A-Z stream. Spaces and other non-letters stay where they
are. A verification certificate, not a historical source, is what the unit
test checks.
"""

from __future__ import annotations

CIPHER_NAME = "keel-sieve"

# Label for docs and tests. This module does not decipher an inscription.
NOT_A_DECIPHERMENT = (
    "Original method verified by a known-plaintext certificate. "
    "Not a reading of an ancient script or of army message Nr. 86."
)


def _ascii_letter(ch: str) -> bool:
    return len(ch) == 1 and ("A" <= ch <= "Z" or "a" <= ch <= "z")


def _letters(text: str) -> list[int]:
    return [ord(ch.upper()) - ord("A") for ch in text if _ascii_letter(ch)]


def _reinject(template: str, values: list[int]) -> str:
    stream = iter(values)
    out: list[str] = []
    for ch in template:
        if not _ascii_letter(ch):
            out.append(ch)
            continue
        mapped = chr(ord("A") + next(stream))
        out.append(mapped.lower() if ch.islower() else mapped)
    return "".join(out)


def square_indices(n: int) -> list[int]:
    """Positions 0, 1, 4, 9, ... that are strictly less than n."""
    if n < 0:
        raise ValueError("length must be non-negative")
    found: list[int] = []
    k = 0
    while True:
        index = k * k
        if index >= n:
            return found
        found.append(index)
        k += 1


def keel(values: list[int]) -> list[int]:
    """Move perfect-square-index letters to the end; keep the rest in order."""
    picked = set(square_indices(len(values)))
    rest = [values[i] for i in range(len(values)) if i not in picked]
    back = [values[i] for i in range(len(values)) if i in picked]
    return rest + back


def unkeel(values: list[int]) -> list[int]:
    slots = square_indices(len(values))
    picked = set(slots)
    n = len(values)
    plain = [0] * n
    rest_at = 0
    back_at = n - len(slots)
    for i in range(n):
        if i in picked:
            plain[i] = values[back_at]
            back_at += 1
        else:
            plain[i] = values[rest_at]
            rest_at += 1
    return plain


def sieve(values: list[int]) -> list[int]:
    """Chain c0 = 3*p0+1 and ci = pi + 2*p(i-1) + 3*i + 1, all mod 26.

    3 is coprime to 26, so the first step is an affine bijection, and each
    later step names pi once with coefficient 1.
    """
    if not values:
        return []
    out = [(3 * values[0] + 1) % 26]
    for i in range(1, len(values)):
        out.append((values[i] + 2 * values[i - 1] + 3 * i + 1) % 26)
    return out


def unsieve(values: list[int]) -> list[int]:
    """Inverse of sieve. 9 is the inverse of 3 modulo 26."""
    if not values:
        return []
    plain = [(9 * ((values[0] - 1) % 26)) % 26]
    for i in range(1, len(values)):
        plain.append((values[i] - 2 * plain[i - 1] - 3 * i - 1) % 26)
    return plain


def encrypt(text: str) -> str:
    """Move square-index letters to the end, then apply the chain sieve."""
    mixed = sieve(keel(_letters(text)))
    return _reinject(text, mixed)


def decrypt(text: str) -> str:
    """Undo the chain sieve, then restore square-index positions."""
    plain = unkeel(unsieve(_letters(text)))
    return _reinject(text, plain)
