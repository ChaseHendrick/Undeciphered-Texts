"""Bifid (Delastelle) known-key solver: Polybius square + period fractionation.

The Bifid cipher combines a 5×5 Polybius square (I/J merged) with a period
block that writes all row digits of the block, then all column digits, and
reads those digits back in pairs as new coordinates. See Practical
Cryptography's worked example:

  http://practicalcryptography.com/ciphers/bifid-cipher/

This module recovers plaintext only when the keysquare and period are
supplied. It is a **known classical-cipher** decrypt helper for published
fixtures. It does **not** read ancient scripts, unknown languages, or claim
any historical break of an unsolved ciphertext.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.result import SolveResult

# 25-letter alphabet: J folded into I (standard Bifid Polybius).
BIFID_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Practical Cryptography worked example (fetched 2026-10-02).
# URL: http://practicalcryptography.com/ciphers/bifid-cipher/
PRACTICAL_CRYPTOGRAPHY_SQUARE = "PHQGMEAYLNOFDXKRCVSZWBUTI"
PRACTICAL_CRYPTOGRAPHY_PERIOD = 5
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFENDTHEEASTWALLOFTHECASTLE"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "FFYHMKHYCPLIASHADTRLHCCHLBLR"
PRACTICAL_CRYPTOGRAPHY_URL = "http://practicalcryptography.com/ciphers/bifid-cipher/"


def bifid_letters(text: str) -> str:
    """A–Z stream for Bifid: non-letters dropped, J folded to I."""
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            continue
        up = ch.upper()
        out.append("I" if up == "J" else up)
    return "".join(out)


def normalize_square(square: str) -> str:
    """Return a 25-letter keysquare (no J) or raise ValueError."""
    cells = bifid_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25:
        raise ValueError("bifid keysquare must be 25 distinct letters without J")
    missing = [ch for ch in BIFID_ALPHABET if ch not in cells]
    if missing:
        raise ValueError(f"bifid keysquare missing letters: {''.join(missing)}")
    return cells


def square_from_keyword(keyword: str) -> str:
    """Build a 5×5 Bifid keysquare from a keyword (J→I), then unused letters."""
    cleaned = bifid_letters(keyword)
    seen: set[str] = set()
    cells: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            cells.append(ch)
    for ch in BIFID_ALPHABET:
        if ch not in seen:
            cells.append(ch)
    return "".join(cells)


def _coords(square: str) -> dict[str, tuple[int, int]]:
    return {ch: divmod(i, 5) for i, ch in enumerate(square)}


def bifid_encrypt(text: str, square: str, period: int) -> str:
    """Encrypt with a known Bifid keysquare and period (published forward map)."""
    if period < 1:
        raise ValueError("period must be at least 1")
    keysquare = normalize_square(square)
    pos = _coords(keysquare)
    stream = bifid_letters(text)
    if not stream:
        raise ValueError("plaintext has no letters")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        rows: list[int] = []
        cols: list[int] = []
        for ch in block:
            r, c = pos[ch]
            rows.append(r)
            cols.append(c)
        digits = rows + cols
        for i in range(0, len(digits), 2):
            out.append(keysquare[digits[i] * 5 + digits[i + 1]])
    return "".join(out)


def bifid_decrypt(text: str, square: str, period: int) -> str:
    """Decrypt with a known Bifid keysquare and period."""
    if period < 1:
        raise ValueError("period must be at least 1")
    keysquare = normalize_square(square)
    pos = _coords(keysquare)
    stream = bifid_letters(text)
    if not stream:
        raise ValueError("ciphertext has no letters")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        digits: list[int] = []
        for ch in block:
            r, c = pos[ch]
            digits.extend((r, c))
        n = len(block)
        rows = digits[:n]
        cols = digits[n:]
        for r, c in zip(rows, cols):
            out.append(keysquare[r * 5 + c])
    return "".join(out)


def solve_bifid(
    text: str,
    *,
    square: str,
    period: int,
) -> SolveResult:
    """Recover Bifid plaintext when the keysquare and period are known.

    This is a known-cipher decrypt, not a blind cryptanalysis search and not
    an ancient-script reading.
    """
    stream = bifid_letters(text)
    keysquare = normalize_square(square)
    plain = bifid_decrypt(stream, keysquare, period)
    return SolveResult(
        method="bifid",
        plaintext=plain,
        key=f"{keysquare}/{period}",
        score=float(len(plain)),
        details={
            "square": keysquare,
            "period": period,
            "letters": len(stream),
            "mode": "known_square_and_period",
            "scope": (
                "Known classical Bifid decrypt only; "
                "not an ancient-script or unknown-language reading."
            ),
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "BIFID_ALPHABET",
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_PERIOD",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_SQUARE",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "bifid_decrypt",
    "bifid_encrypt",
    "bifid_letters",
    "normalize_square",
    "solve_bifid",
    "square_from_keyword",
]
