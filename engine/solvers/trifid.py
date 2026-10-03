"""Trifid (Delastelle 3x3x3) known-key solver.

Trifid writes each symbol as three coordinates in a 3 by 3 by 3 cube,
then, inside each period block, reads those coordinates by rows
(all layers, then all rows, then all columns) and turns each new
triplet back into a symbol. See Practical Cryptography's worked
example:

  http://practicalcryptography.com/ciphers/trifid-cipher/

The cube on that page is filled from this 27-symbol key, three
squares of nine, each square row by row:

  EPSDUCVWYM.ZLKXNBTFGORIJHAQ

  square 1   square 2   square 3
    E P S      M . Z      F G O
    D U C      L K X      R I J
    V W Y      N B T      H A Q

The 27th symbol is the period character. Spaces are not enciphered:
they are dropped, not copied into the ciphertext. The page's
plaintext "DEFEND THE EAST WALL OF THE CASTLE." with period 5
becomes "SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP". Those ciphertext
spaces are groups of the period, not word spaces.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers plaintext only when the cube and the period are
supplied. It is **not** an unknown-script reading and **not** a claim
about army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# 26 letters plus the period character, the 27 cells of a Trifid cube.
TRIFID_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ."

# Practical Cryptography worked example (fetched 2026-10-03).
# URL: http://practicalcryptography.com/ciphers/trifid-cipher/
PRACTICAL_CRYPTOGRAPHY_KEY = "EPSDUCVWYM.ZLKXNBTFGORIJHAQ"
PRACTICAL_CRYPTOGRAPHY_PERIOD = 5
# Spaces are not included. The final period is a cube symbol and is included.
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE."
# Grouping spaces from the page are not included.
PRACTICAL_CRYPTOGRAPHY_CIPHER = "SUEFECPHSEGYYJIXIMFOFOCEJLBSP"
PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS = "SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP"
PRACTICAL_CRYPTOGRAPHY_URL = "http://practicalcryptography.com/ciphers/trifid-cipher/"

_SCOPE = (
    "Known classical Trifid cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def trifid_symbols(text: str) -> str:
    """A-Z and '.' only. Spaces and other characters are not enciphered."""
    out: list[str] = []
    for ch in text:
        if ch == ".":
            out.append(".")
        elif ch.isalpha():
            out.append(ch.upper())
    return "".join(out)


def normalize_key(key: str) -> str:
    """Return the 27-symbol cube key, or raise ValueError."""
    cells = trifid_symbols(key)
    if len(cells) != 27 or len(set(cells)) != 27:
        raise ValueError("trifid key must be 27 distinct symbols (A-Z and .)")
    missing = [ch for ch in TRIFID_ALPHABET if ch not in cells]
    if missing:
        raise ValueError("trifid key missing symbols: " + "".join(missing))
    return cells


def _coords(key: str) -> dict[str, tuple[int, int, int]]:
    pos: dict[str, tuple[int, int, int]] = {}
    for i, ch in enumerate(key):
        layer, rem = divmod(i, 9)
        row, col = divmod(rem, 3)
        pos[ch] = (layer, row, col)
    return pos


def _symbol(key: str, layer: int, row: int, col: int) -> str:
    return key[layer * 9 + row * 3 + col]


def trifid_encrypt(text: str, key: str, period: int) -> str:
    """Encrypt with a known Trifid cube and period.

    Spaces are dropped. The period character is a cube symbol and is kept.
    """
    if period < 1:
        raise ValueError("period must be at least 1")
    cube = normalize_key(key)
    pos = _coords(cube)
    stream = trifid_symbols(text)
    if not stream:
        raise ValueError("plaintext has no trifid symbols")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        layers: list[int] = []
        rows: list[int] = []
        cols: list[int] = []
        for ch in block:
            layer, row, col = pos[ch]
            layers.append(layer)
            rows.append(row)
            cols.append(col)
        digits = layers + rows + cols
        for i in range(0, len(digits), 3):
            out.append(_symbol(cube, digits[i], digits[i + 1], digits[i + 2]))
    return "".join(out)


def trifid_decrypt(text: str, key: str, period: int) -> str:
    """Decrypt with a known Trifid cube and period.

    Spaces in the ciphertext are ignored. They are not word spaces.
    """
    if period < 1:
        raise ValueError("period must be at least 1")
    cube = normalize_key(key)
    pos = _coords(cube)
    stream = trifid_symbols(text)
    if not stream:
        raise ValueError("ciphertext has no trifid symbols")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        digits: list[int] = []
        for ch in block:
            layer, row, col = pos[ch]
            digits.extend((layer, row, col))
        n = len(block)
        layers = digits[:n]
        rows = digits[n : 2 * n]
        cols = digits[2 * n :]
        for layer, row, col in zip(layers, rows, cols):
            out.append(_symbol(cube, layer, row, col))
    return "".join(out)


def solve_trifid(text: str, *, key: str, period: int) -> SolveResult:
    """Recover Trifid plaintext when the cube and period are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    cube = normalize_key(key)
    stream = trifid_symbols(text)
    plain = trifid_decrypt(stream, cube, period)
    return SolveResult(
        method="trifid",
        plaintext=plain,
        key=f"{cube}/{period}",
        score=float(len(plain)),
        details={
            "key": cube,
            "alphabet": cube,
            "period": period,
            "letters": len(stream),
            "mode": "known_cube_and_period",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
            "spaces": "not_enciphered",
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_PERIOD",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "TRIFID_ALPHABET",
    "normalize_key",
    "solve_trifid",
    "trifid_decrypt",
    "trifid_encrypt",
    "trifid_symbols",
]
