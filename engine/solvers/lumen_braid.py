"""Lumen braid: an original letter cipher for this repository.

The rule is not Playfair, bifid, Vigenère, two-square, or a reading of any
ancient script. It is not a reading of army message Nr. 86. Encrypt and
decrypt are inverses on the A-Z stream. Spaces and other non-letters stay
where they are. A verification certificate, not a historical source, is what
the unit test checks.
"""

from __future__ import annotations

WIDTH = 5
EVEN_ROW = (0, 2, 4, 1, 3)
ODD_ROW = (3, 1, 4, 2, 0)

CIPHER_NAME = "lumen-braid"

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


def braid_sources(n: int) -> list[int]:
    """Source index for each position of the braided stream.

    Rows are five letters wide. Even rows are read as columns 0, 2, 4, 1, 3.
    Odd rows are read as columns 3, 1, 4, 2, 0. A short last row skips columns
    that have no letter. Every index in 0..n-1 appears once.
    """
    if n < 0:
        raise ValueError("length must be non-negative")
    sources: list[int] = []
    rows = (n + WIDTH - 1) // WIDTH if n else 0
    for row in range(rows):
        order = EVEN_ROW if row % 2 == 0 else ODD_ROW
        for col in order:
            index = row * WIDTH + col
            if index < n:
                sources.append(index)
    return sources


def braid(values: list[int]) -> list[int]:
    return [values[i] for i in braid_sources(len(values))]


def unbraid(values: list[int]) -> list[int]:
    plain = [0] * len(values)
    for dest, src in enumerate(braid_sources(len(values))):
        plain[src] = values[dest]
    return plain


def _mix_block(a: int, b: int, c: int) -> tuple[int, int, int]:
    # (a+c, a+b+c, a+b) mod 26. The sums are an invertible triad, then rotated.
    total = (a + b + c) % 26
    return ((a + c) % 26, total, (a + b) % 26)


def _unmix_block(x: int, y: int, z: int) -> tuple[int, int, int]:
    # Cipher block is (w, u, v) = (a+c, a+b+c, a+b).
    w, u, v = x, y, z
    a = (v + w - u) % 26
    b = (u - w) % 26
    c = (u - v) % 26
    return a, b, c


def _mix_pair(a: int, b: int) -> tuple[int, int]:
    return ((a + b) % 26, (a + 2 * b) % 26)


def _unmix_pair(u: int, v: int) -> tuple[int, int]:
    return ((2 * u - v) % 26, (v - u) % 26)


def _mix_single(p: int) -> int:
    return (3 * p + 1) % 26


def _unmix_single(c: int) -> int:
    return (9 * ((c - 1) % 26)) % 26


def mix_stream(values: list[int]) -> list[int]:
    out: list[int] = []
    n = len(values)
    full = n - (n % 3)
    for i in range(0, full, 3):
        out.extend(_mix_block(values[i], values[i + 1], values[i + 2]))
    rem = values[full:]
    if len(rem) == 1:
        out.append(_mix_single(rem[0]))
    elif len(rem) == 2:
        out.extend(_mix_pair(rem[0], rem[1]))
    return out


def unmix_stream(values: list[int]) -> list[int]:
    out: list[int] = []
    n = len(values)
    full = n - (n % 3)
    for i in range(0, full, 3):
        out.extend(_unmix_block(values[i], values[i + 1], values[i + 2]))
    rem = values[full:]
    if len(rem) == 1:
        out.append(_unmix_single(rem[0]))
    elif len(rem) == 2:
        out.extend(_unmix_pair(rem[0], rem[1]))
    return out


def encrypt(text: str) -> str:
    """Braid the A-Z stream, then mix triads. Non-letters stay in place."""
    mixed = mix_stream(braid(_letters(text)))
    return _reinject(text, mixed)


def decrypt(text: str) -> str:
    """Invert the triad mix, then invert the braid. Non-letters stay in place."""
    plain = unbraid(unmix_stream(_letters(text)))
    return _reinject(text, plain)
