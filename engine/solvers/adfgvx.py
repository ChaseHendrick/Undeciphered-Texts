"""ADFGVX known-key fractionating transposition solver.

Decrypts the World War I ADFGVX field cipher when both keys are supplied:
a 6×6 substitution square (A-Z and digits 0-9, labeled by A D F G V X) and
a columnar transposition keyword.

The worked example is the Wikipedia **ADFGVX** section (not the earlier
5×5 ADFGX example). Fractionation keyword ``nachtbommenwerper``,
transposition keyword ``PRIVACY``, message ``attack at 1200am``:

https://en.wikipedia.org/wiki/ADFGVX_cipher

This module decrypts when those keys are supplied. It is a **known-cipher**
solver for that classical system. It does **not** read an unknown script,
and it does not claim a cryptanalysis of an unsolved historical ADFGVX
message (Painvin's break is a different problem and is not implemented).
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.language import get_model
from engine.result import SolveResult

# Wikipedia "ADFGVX" section (fetched 2026-10-02, America/New_York).
WIKIPEDIA_SOURCE_URL = "https://en.wikipedia.org/wiki/ADFGVX_cipher"
WIKIPEDIA_FRACTIONATION_KEYWORD = "nachtbommenwerper"
WIKIPEDIA_TRANSPOSITION_KEY = "PRIVACY"
# Article message "attack at 1200am". Spaces are not enciphered.
WIKIPEDIA_MESSAGE = "attack at 1200am"
WIKIPEDIA_PLAINTEXT = "ATTACKAT1200AM"
# Column-read groups: DGDD DAGD DGAF ADDF DADV DVFA ADVX
WIKIPEDIA_CIPHERTEXT = "DGDDDAGDDGAFADDFDADVDVFAADVX"
# Row-major 6×6 square printed in that section.
WIKIPEDIA_SQUARE = "NA1C3H8TB2OME5WRPD4F6G7I9J0KLQSUVXYZ"

ADFGVX_LABELS = "ADFGVX"
_LABEL_INDEX = {ch: i for i, ch in enumerate(ADFGVX_LABELS)}
_SQUARE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def _letters(keyword: str) -> str:
    return "".join(ch.upper() for ch in keyword if ch.isalpha())


def square_from_fractionation_keyword(keyword: str) -> str:
    """Build the 36-cell square the Wikipedia ADFGVX example describes.

    Unique keyword letters, then the unused letters of A-Z. Digits are then
    inserted after the first A-J: A→1, B→2, … I→9, J→0. That is the filling
    rule stated for ``nachtbommenwerper``, not a second historical cipher.
    """
    cleaned = _letters(keyword)
    if not cleaned:
        raise ValueError("fractionation keyword must contain a letter")
    seen: set[str] = set()
    cells: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            cells.append(ch)
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            cells.append(ch)
    if len(cells) != 26 or len(set(cells)) != 26:
        raise ValueError("fractionation keyword must yield the 26 letters")
    digits = {chr(ord("A") + i): ("0" if i == 9 else str(i + 1)) for i in range(10)}
    expanded: list[str] = []
    for ch in cells:
        expanded.append(ch)
        if ch in digits:
            expanded.append(digits[ch])
    square = "".join(expanded)
    return _require_square(square)


def _require_square(square: str) -> str:
    cells = "".join(ch.upper() for ch in square if ch.isalnum())
    if len(cells) != 36 or len(set(cells)) != 36:
        raise ValueError("ADFGVX square must be 36 distinct letters and digits")
    if any(ch not in _SQUARE_ALPHABET for ch in cells):
        raise ValueError("ADFGVX square must use A-Z and 0-9 only")
    return cells


def _positions(square: str) -> dict[str, tuple[int, int]]:
    cells = _require_square(square)
    return {ch: divmod(i, 6) for i, ch in enumerate(cells)}


def _normalize_plaintext(text: str) -> str:
    out: list[str] = []
    for ch in text:
        if ch.isalpha() or ch.isdigit():
            out.append(ch.upper())
    if not out:
        raise ValueError("plaintext must contain a letter or digit")
    return "".join(out)


def _normalize_ciphertext(text: str) -> str:
    out = []
    for ch in text:
        up = ch.upper()
        if up in _LABEL_INDEX:
            out.append(up)
        elif ch.isalpha() or ch.isdigit():
            raise ValueError("ADFGVX ciphertext may contain only A D F G V X")
    if not out:
        raise ValueError("ciphertext must contain ADFGVX letters")
    if len(out) % 2 == 1:
        raise ValueError("ADFGVX ciphertext length must be even")
    return "".join(out)


def _transposition_key(key: str) -> str:
    cleaned = _letters(key)
    if not cleaned:
        raise ValueError("transposition key must contain a letter")
    return cleaned


def _column_order(key: str) -> list[int]:
    """Read order: columns sorted by key letter, ties keep left-to-right order."""
    return sorted(range(len(key)), key=lambda i: key[i])


def _column_heights(n: int, width: int) -> list[int]:
    rows, rem = divmod(n, width)
    return [rows + (1 if i < rem else 0) for i in range(width)]


def columnar_encrypt(text: str, key: str) -> str:
    """Row-write, column-read transposition. A short last row stops on the right."""
    width = len(key)
    heights = _column_heights(len(text), width)
    columns: list[list[str]] = [[] for _ in range(width)]
    index = 0
    for row in range(max(heights, default=0)):
        for col in range(width):
            if row < heights[col]:
                columns[col].append(text[index])
                index += 1
    if index != len(text):
        raise ValueError("columnar encrypt did not consume the text")
    out: list[str] = []
    for col in _column_order(key):
        out.extend(columns[col])
    return "".join(out)


def columnar_decrypt(text: str, key: str) -> str:
    """Inverse of :func:`columnar_encrypt`."""
    width = len(key)
    heights = _column_heights(len(text), width)
    columns = [""] * width
    index = 0
    for col in _column_order(key):
        height = heights[col]
        columns[col] = text[index : index + height]
        index += height
    if index != len(text):
        raise ValueError("columnar decrypt did not consume the text")
    out: list[str] = []
    for row in range(max(heights, default=0)):
        for col in range(width):
            if row < heights[col]:
                out.append(columns[col][row])
    return "".join(out)


def adfgvx_encrypt(
    text: str,
    transposition_key: str,
    fractionation_keyword: str | None = None,
    square: str | None = None,
) -> str:
    """Encrypt with a known ADFGVX square and transposition keyword."""
    grid = _resolve_square(fractionation_keyword, square)
    pos = _positions(grid)
    key = _transposition_key(transposition_key)
    pairs: list[str] = []
    for ch in _normalize_plaintext(text):
        if ch not in pos:
            raise ValueError(f"plaintext symbol {ch!r} is not in the square")
        row, col = pos[ch]
        pairs.append(ADFGVX_LABELS[row] + ADFGVX_LABELS[col])
    return columnar_encrypt("".join(pairs), key)


def adfgvx_decrypt(
    ciphertext: str,
    transposition_key: str,
    fractionation_keyword: str | None = None,
    square: str | None = None,
) -> str:
    """Decrypt an ADFGVX ciphertext with a known square and transposition key.

    Returns the letter-and-digit stream. Spaces and punctuation are not in
    the cipher alphabet, so they are not restored.
    """
    grid = _resolve_square(fractionation_keyword, square)
    cells = _require_square(grid)
    key = _transposition_key(transposition_key)
    stream = _normalize_ciphertext(ciphertext)
    fractionated = columnar_decrypt(stream, key)
    if len(fractionated) % 2 == 1:
        raise ValueError("fractionated ADFGVX text length must be even")
    out: list[str] = []
    for i in range(0, len(fractionated), 2):
        row = _LABEL_INDEX[fractionated[i]]
        col = _LABEL_INDEX[fractionated[i + 1]]
        out.append(cells[row * 6 + col])
    return "".join(out)


def _resolve_square(fractionation_keyword: str | None, square: str | None) -> str:
    if square is not None:
        return _require_square(square)
    if fractionation_keyword is not None:
        return square_from_fractionation_keyword(fractionation_keyword)
    raise ValueError("provide a 36-character square or a fractionation keyword")


def solve_adfgvx(
    text: str,
    transposition_key: str,
    fractionation_keyword: str | None = None,
    square: str | None = None,
) -> SolveResult:
    """Recover plaintext from ADFGVX ciphertext when both keys are known.

    This is a known-cipher, known-key decrypt. It does not search for an
    unknown key and does not read an unknown script.
    """
    grid = _resolve_square(fractionation_keyword, square)
    plaintext = adfgvx_decrypt(
        text,
        transposition_key,
        square=grid,
    )
    key = _transposition_key(transposition_key)
    letters = letters_only(plaintext)
    az = [ord(ch) - 65 for ch in letters]
    return SolveResult(
        method="adfgvx",
        plaintext=plaintext,
        key=key,
        score=get_model().score(az) if az else 0.0,
        details={
            "transposition_key": key,
            "fractionation_keyword": fractionation_keyword,
            "square": grid,
            "letters": len(az),
            "source_example": WIKIPEDIA_SOURCE_URL,
            "scope": (
                "known-key ADFGVX fractionating transposition decrypt; "
                "classical cipher only; does not read an unknown script"
            ),
        },
    )


__all__ = [
    "ADFGVX_LABELS",
    "WIKIPEDIA_CIPHERTEXT",
    "WIKIPEDIA_FRACTIONATION_KEYWORD",
    "WIKIPEDIA_MESSAGE",
    "WIKIPEDIA_PLAINTEXT",
    "WIKIPEDIA_SOURCE_URL",
    "WIKIPEDIA_SQUARE",
    "WIKIPEDIA_TRANSPOSITION_KEY",
    "adfgvx_decrypt",
    "adfgvx_encrypt",
    "columnar_decrypt",
    "columnar_encrypt",
    "solve_adfgvx",
    "square_from_fractionation_keyword",
]
