"""Rail-fence known-key solver: zigzag transposition across a fixed rail count.

The plaintext is written downward on successive rails, then upward, and the
ciphertext is read off one rail at a time from top to bottom. The key is the
number of rails. With A…Z letters only and rails = 3, the row of letter i is

    cycle = 2 * (rails - 1)
    row = i mod cycle, or cycle - (i mod cycle) once the fence turns upward.

The worked example used here is the one on Practical Cryptography
(fetched 2026-10-02):

  http://practicalcryptography.com/ciphers/classical-era/rail-fence/

  key 3, "defend the east wall of the castle" → dnetlhseedheswloteateftaafcl

This module is a **known classical-cipher** solver. It recovers plaintext
only when the rail count is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Practical Cryptography worked example (fetched 2026-10-02).
# http://practicalcryptography.com/ciphers/classical-era/rail-fence/
PRACTICAL_CRYPTOGRAPHY_URL = "http://practicalcryptography.com/ciphers/classical-era/rail-fence/"
PRACTICAL_CRYPTOGRAPHY_KEY = "3"
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "DNETLHSEEDHESWLOTEATEFTAAFCL"

_SCOPE = (
    "Known classical rail-fence cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def rail_fence_key(key: str | int) -> int:
    """Rail count. Must be an integer of at least 2."""
    if isinstance(key, int):
        rails = key
    else:
        text = str(key).strip()
        if not text.isdigit():
            raise ValueError("Rail-fence key must be the number of rails")
        rails = int(text)
    if rails < 2:
        raise ValueError("Rail-fence key must be at least 2 rails")
    return rails


def _row_of(index: int, rails: int) -> int:
    cycle = 2 * (rails - 1)
    position = index % cycle
    if position < rails:
        return position
    return cycle - position


def rail_fence_encrypt(text: str, key: str | int) -> str:
    """Encrypt with a known rail count. Non-letters are dropped.

    Letters are written in zigzag order and read off by rail from the top.
    """
    rails = rail_fence_key(key)
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    rows: list[list[str]] = [[] for _ in range(rails)]
    for index, letter in enumerate(plain):
        rows[_row_of(index, rails)].append(letter)
    return "".join("".join(row) for row in rows)


def rail_fence_decrypt(text: str, key: str | int) -> str:
    """Decrypt with a known rail count.

    The zigzag assigns each position to a rail. Ciphertext is split into
    those rail lengths, then read back in zigzag order.
    """
    rails = rail_fence_key(key)
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    rows_index = [_row_of(index, rails) for index in range(len(cipher))]
    counts = [rows_index.count(row) for row in range(rails)]
    if sum(counts) != len(cipher):
        raise ValueError("Rail lengths do not cover the ciphertext")
    offset = 0
    buckets: list[list[str]] = []
    for count in counts:
        buckets.append(list(cipher[offset : offset + count]))
        offset += count
    plain: list[str] = []
    for row in rows_index:
        if not buckets[row]:
            raise ValueError("Rail was exhausted before the ciphertext ended")
        plain.append(buckets[row].pop(0))
    return "".join(plain)


def solve_rail_fence(text: str, *, key: str | int) -> SolveResult:
    """Recover rail-fence plaintext when the number of rails is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    rails = rail_fence_key(key)
    plain_letters = rail_fence_decrypt(text, rails)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    return SolveResult(
        method="rail_fence",
        plaintext=rendered,
        key=str(rails),
        score=float(len(plain_letters)),
        details={
            "key": str(rails),
            "rails": rails,
            "letters": len(letters_only(text)),
            "mode": "known_rails",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "rail_fence_decrypt",
    "rail_fence_encrypt",
    "rail_fence_key",
    "solve_rail_fence",
]
