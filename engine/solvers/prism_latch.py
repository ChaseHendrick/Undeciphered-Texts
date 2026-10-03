"""Prism latch: an original letter cipher for this repository.

The rule is not a row of five, Playfair, bifid, Vigenère, two-square, or the
lumen braid. It is not a reading of any ancient script and it is not a
reading of army message Nr. 86. Encrypt and decrypt are inverses on the A-Z
stream. Spaces and other non-letters stay where they are. A verification
certificate, not a historical source, is what the unit test checks.
"""

from __future__ import annotations

CIPHER_NAME = "prism-latch"

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


def triangular_indices(n: int) -> list[int]:
    """Positions 0, 1, 3, 6, ... that are strictly less than n."""
    if n < 0:
        raise ValueError("length must be non-negative")
    found: list[int] = []
    k = 0
    while True:
        index = k * (k + 1) // 2
        if index >= n:
            return found
        found.append(index)
        k += 1


def latch(values: list[int]) -> list[int]:
    """Move triangular-index letters to the front; keep the rest in order."""
    picked = set(triangular_indices(len(values)))
    front = [values[i] for i in range(len(values)) if i in picked]
    rest = [values[i] for i in range(len(values)) if i not in picked]
    return front + rest


def unlatch(values: list[int]) -> list[int]:
    slots = triangular_indices(len(values))
    picked = set(slots)
    plain = [0] * len(values)
    front = 0
    back = len(slots)
    for i in range(len(values)):
        if i in picked:
            plain[i] = values[front]
            front += 1
        else:
            plain[i] = values[back]
            back += 1
    return plain


def _mix4(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    # (a+b, b+c, c+d, d+2a+1) mod 26. Determinant of the linear part is -1.
    return (
        (a + b) % 26,
        (b + c) % 26,
        (c + d) % 26,
        (d + 2 * a + 1) % 26,
    )


def _unmix4(x: int, y: int, z: int, w: int) -> tuple[int, int, int, int]:
    b = (2 * x - y + z + 1 - w) % 26
    a = (x - b) % 26
    c = (y - b) % 26
    d = (z - y + b) % 26
    return a, b, c, d


def _mix3(a: int, b: int, c: int) -> tuple[int, int, int]:
    # Matrix [[1,2,0],[0,1,2],[2,0,1]] has determinant 9, coprime to 26.
    return ((a + 2 * b) % 26, (b + 2 * c) % 26, (c + 2 * a) % 26)


def _unmix3(x: int, y: int, z: int) -> tuple[int, int, int]:
    b = (3 * (4 * x + y - 2 * z)) % 26
    a = (x - 2 * b) % 26
    c = (z - 2 * x + 4 * b) % 26
    return a, b, c


def _mix2(a: int, b: int) -> tuple[int, int]:
    return ((a + b) % 26, (2 * a + b) % 26)


def _unmix2(x: int, y: int) -> tuple[int, int]:
    a = (y - x) % 26
    b = (2 * x - y) % 26
    return a, b


def _mix1(p: int) -> int:
    return (5 * p + 3) % 26


def _unmix1(c: int) -> int:
    return (21 * ((c - 3) % 26)) % 26


def mix_stream(values: list[int]) -> list[int]:
    out: list[int] = []
    n = len(values)
    full = n - (n % 4)
    for i in range(0, full, 4):
        out.extend(_mix4(values[i], values[i + 1], values[i + 2], values[i + 3]))
    rem = values[full:]
    if len(rem) == 1:
        out.append(_mix1(rem[0]))
    elif len(rem) == 2:
        out.extend(_mix2(rem[0], rem[1]))
    elif len(rem) == 3:
        out.extend(_mix3(rem[0], rem[1], rem[2]))
    return out


def unmix_stream(values: list[int]) -> list[int]:
    out: list[int] = []
    n = len(values)
    full = n - (n % 4)
    for i in range(0, full, 4):
        out.extend(_unmix4(values[i], values[i + 1], values[i + 2], values[i + 3]))
    rem = values[full:]
    if len(rem) == 1:
        out.append(_unmix1(rem[0]))
    elif len(rem) == 2:
        out.extend(_unmix2(rem[0], rem[1]))
    elif len(rem) == 3:
        out.extend(_unmix3(rem[0], rem[1], rem[2]))
    return out


def encrypt(text: str) -> str:
    """Latch triangular positions to the front, then mix blocks of four."""
    mixed = mix_stream(latch(_letters(text)))
    return _reinject(text, mixed)


def decrypt(text: str) -> str:
    """Undo the block mix, then restore triangular positions."""
    plain = unlatch(unmix_stream(_letters(text)))
    return _reinject(text, plain)
