"""Phillips known-key solver: eight shifted 5x5 squares.

The Phillips cipher (ACA / classroom form) starts from one 5x5 Polybius
square. A keyword is written left to right, duplicates dropped, J omitted
so I stands for both I and J, then the rest of the alphabet fills the
square left to right. Eight grids are made by shifting rows:

    1: 1 2 3 4 5
    2: 2 1 3 4 5
    3: 2 3 1 4 5
    4: 2 3 4 1 5
    5: 2 3 4 5 1
    6: 3 2 4 5 1
    7: 3 4 2 5 1
    8: 3 4 5 2 1

Each grid enciphers five plaintext letters, then the next grid is used.
After grid 8 the cycle returns to grid 1. A letter is replaced by the
letter one row down and one column to the right, wrapping at the edges.
Decryption steps one row up and one column to the left on the same grid.

The worked example is the Central Washington University Kryptos challenge
sheet (fetched 2026-10-02):

  https://www.cwu.edu/academics/math/_documents/kryptos-challenges/cwu-kryptos-challenge-phillips-cipher.pdf

Keyword COMPETE, left-to-right fill. Plaintext "squares one and five are
the same and so are two and eight". The letter-by-letter rows on that
sheet give ciphertext

  ZXVIYGZIWGIWLGPAVIPVHRTZIKGRWUFIXDGOBIMWLTSQRO

The one-line summary at the bottom of the same page writes TWQRO where
those rows show TSQRO. This solver follows the letter rows, which match
the rules printed above them.

This module is a **known classical-cipher** solver. It recovers plaintext
only when the keyword is supplied. It is **not** an unknown-script
reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# 25-letter alphabet: J folded into I.
PHILLIPS_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Row index orders for grids 1..8 (0-based rows of the base square).
PHILLIPS_ROW_ORDERS: tuple[tuple[int, ...], ...] = (
    (0, 1, 2, 3, 4),
    (1, 0, 2, 3, 4),
    (1, 2, 0, 3, 4),
    (1, 2, 3, 0, 4),
    (1, 2, 3, 4, 0),
    (2, 1, 3, 4, 0),
    (2, 3, 1, 4, 0),
    (2, 3, 4, 1, 0),
)

# CWU Kryptos challenge Phillips sheet (fetched 2026-10-02).
# Letter-by-letter rows, not the one-line summary (that line has TWQRO).
CWU_PHILLIPS_URL = (
    "https://www.cwu.edu/academics/math/_documents/kryptos-challenges/"
    "cwu-kryptos-challenge-phillips-cipher.pdf"
)
CWU_PHILLIPS_KEY = "COMPETE"
CWU_PHILLIPS_PLAIN = "SQUARESONEANDFIVEARETHESAMEANDSOARETWOANDEIGHT"
CWU_PHILLIPS_CIPHER = "ZXVIYGZIWGIWLGPAVIPVHRTZIKGRWUFIXDGOBIMWLTSQRO"

_SCOPE = (
    "Known classical Phillips cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)


def phillips_keyword(key: str) -> str:
    """A-Z keyword with J folded to I. Duplicate letters stay in the key.

    The square drops repeats when it is filled. At least one letter is required.
    """
    cleaned = []
    for ch in letters_only(key):
        cleaned.append("I" if ch == "J" else ch)
    if not cleaned:
        raise ValueError("Phillips keyword must contain at least one letter")
    return "".join(cleaned)


def phillips_square(key: str) -> tuple[str, ...]:
    """5x5 square, left to right, keyword first, duplicate letters and J omitted."""
    used = []
    for ch in phillips_keyword(key):
        if ch not in used:
            used.append(ch)
    used_s = "".join(used)
    rest = [ch for ch in PHILLIPS_ALPHABET if ch not in used_s]
    flat = used_s + "".join(rest)
    if len(flat) != 25 or len(set(flat)) != 25:
        raise ValueError("Phillips square must contain 25 distinct letters")
    return tuple(flat[i : i + 5] for i in range(0, 25, 5))


def phillips_grids(key: str) -> tuple[tuple[str, ...], ...]:
    """Eight grids from the base square, using the standard row shifts."""
    base = phillips_square(key)
    return tuple(tuple(base[i] for i in order) for order in PHILLIPS_ROW_ORDERS)


def _fold(ch: str) -> str:
    ch = ch.upper()
    if ch == "J":
        return "I"
    return ch


def _step(grid: tuple[str, ...], ch: str, down: int, right: int) -> str:
    for r, row in enumerate(grid):
        c = row.find(ch)
        if c != -1:
            return grid[(r + down) % 5][(c + right) % 5]
    raise ValueError(f"letter {ch} is not in the Phillips square")


def _transform(text: str, key: str, down: int, right: int) -> str:
    letters = [_fold(ch) for ch in letters_only(text)]
    if not letters:
        raise ValueError("text has no letters")
    grids = phillips_grids(key)
    out = []
    for i, ch in enumerate(letters):
        grid = grids[(i // 5) % 8]
        out.append(_step(grid, ch, down, right))
    return "".join(out)


def phillips_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Phillips keyword. Non-letters are dropped.

    Each block of five letters uses the next of the eight grids. The
    substitute is one row down and one column to the right.
    """
    return _transform(text, key, 1, 1)


def phillips_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Phillips keyword.

    Same grids as encryption. The substitute is one row up and one
    column to the left.
    """
    return _transform(text, key, -1, -1)


def solve_phillips(text: str, *, key: str) -> SolveResult:
    """Recover Phillips plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    cleaned = phillips_keyword(key)
    plain_letters = phillips_decrypt(text, cleaned)
    rendered = (
        reinject(text, plain_letters)
        if any(not ch.isalpha() for ch in text)
        else plain_letters
    )
    return SolveResult(
        method="phillips",
        plaintext=rendered,
        key=cleaned,
        score=float(len(plain_letters)),
        details={
            "key": cleaned,
            "letters": len(letters_only(text)),
            "mode": "known_phillips",
            "variant": "eight_row_shifted_squares",
            "scope": _SCOPE,
            "source_url": CWU_PHILLIPS_URL,
        },
    )


__all__ = [
    "CWU_PHILLIPS_CIPHER",
    "CWU_PHILLIPS_KEY",
    "CWU_PHILLIPS_PLAIN",
    "CWU_PHILLIPS_URL",
    "PHILLIPS_ALPHABET",
    "PHILLIPS_ROW_ORDERS",
    "phillips_decrypt",
    "phillips_encrypt",
    "phillips_grids",
    "phillips_keyword",
    "phillips_square",
    "solve_phillips",
]
