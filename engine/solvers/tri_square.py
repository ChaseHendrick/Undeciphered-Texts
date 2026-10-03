"""Tri-square known-key solver.

Three 5 by 5 Polybius squares. Plaintext is taken in pairs. The first
letter is found in square 1 and the second in square 2. Each pair
becomes a ciphertext trigraph:

- the first cipher letter is any letter in the same column of square 1
- the second cipher letter is the square 3 cell at the row of the first
  plaintext letter and the column of the second plaintext letter
- the third cipher letter is any letter in the same row of square 2

The American Cryptogram Association sheet prints the squares and one
worked example:

  https://www.cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf

The sheet does not print keyword names. The printed squares are the
fills below. Square 1 is NOVELS written down the columns. Square 2 is
READING written across the rows. Square 3 is PASTIME written in a
clockwise spiral. J is omitted. Those fills match the sheet.

This module is a known classical-cipher solver. It recovers plaintext
only when the three squares are supplied. The first and third cipher
letters are not unique, so encryption records which row and column were
chosen. Decryption does not need that choice. It is not an
unknown-script reading. It does not claim a solution of Kryptos K4,
Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script,
rongorongo, or army message Nr. 86.
"""

from __future__ import annotations

from collections.abc import Sequence

from engine.language import get_model
from engine.result import SolveResult

# 25-letter alphabet: J is folded into I, as on the ACA 5 by 5 squares.
TRI_SQUARE_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# ACA Tri-square sheet (fetched 2026-10-03). One page, PDF 1.6, page 86.
# SHA-256 74b8200474df8a50e6782fcc33b4a34517f09d644b3954dc918c373f3f1b4151
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf"
ACA_PDF_SHA256 = "74b8200474df8a50e6782fcc33b4a34517f09d644b3954dc918c373f3f1b4151"
ACA_SQUARE1_KEYWORD = "NOVELS"
ACA_SQUARE1_ROUTE = "vertical"
ACA_SQUARE2_KEYWORD = "READING"
ACA_SQUARE2_ROUTE = "horizontal"
ACA_SQUARE3_KEYWORD = "PASTIME"
ACA_SQUARE3_ROUTE = "clockwise_spiral"
# Spaced letters on the sheet: t h r e e k e y s q u a r e s u s e d x
ACA_PLAIN = "THREEKEYSQUARESUSEDX"
ACA_MESSAGE = "three key squares used x"
# Trigraph groups on the sheet: RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ.
ACA_CIPHER = "RHLQXRLXOEVZBATXSERXDDIUAAABFZ"
ACA_PRINTED_CIPHER = "RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ."
# Row-major squares printed on the sheet.
ACA_SQUARE1 = "NSFMUOAGPWVBHQXECIRYLDKTZ"
ACA_SQUARE2 = "READINGBCFHKLMOPQSTUVWXYZ"
ACA_SQUARE3 = "PASTINOQRMLYZUEKXWVBHGFDC"
# Which letter of the column (from the top) and of the row (from the left)
# the sheet used. The rule allows any letter in that column or row.
ACA_FIRST_ROWS = (3, 2, 4, 3, 2, 2, 3, 4, 1, 2)
ACA_THIRD_COLS = (2, 0, 4, 4, 3, 1, 3, 4, 2, 4)

_SCOPE = (
    "Known classical tri-square cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script, "
    "rongorongo, or army message Nr. 86."
)


def tri_square_letters(text: str) -> str:
    """A-Z stream: non-letters dropped, J folded to I."""
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            continue
        up = ch.upper()
        out.append("I" if up == "J" else up)
    return "".join(out)


def normalize_square(square: str) -> str:
    """Return a 25-letter keysquare with no J, or raise ValueError."""
    cells = tri_square_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25:
        raise ValueError("tri-square square must be 25 distinct letters without J")
    missing = [ch for ch in TRI_SQUARE_ALPHABET if ch not in cells]
    if missing:
        raise ValueError("tri-square square missing letters: " + "".join(missing))
    return cells


def _keyword_then_rest(keyword: str) -> str:
    cleaned = tri_square_letters(keyword)
    if not cleaned:
        raise ValueError("tri-square keyword must contain at least one letter")
    seen: set[str] = set()
    head: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            head.append(ch)
    rest = [ch for ch in TRI_SQUARE_ALPHABET if ch not in seen]
    stream = "".join(head) + "".join(rest)
    if len(stream) != 25:
        raise ValueError("tri-square square fill must be 25 letters")
    return stream


def _place(order: list[tuple[int, int]], stream: str) -> str:
    if len(order) != 25 or len(stream) != 25:
        raise ValueError("tri-square route must cover 25 cells")
    grid = [[""] * 5 for _ in range(5)]
    for (row, col), ch in zip(order, stream):
        grid[row][col] = ch
    return "".join("".join(row) for row in grid)


def horizontal_order() -> list[tuple[int, int]]:
    """Left to right, top row first."""
    return [(row, col) for row in range(5) for col in range(5)]


def vertical_order() -> list[tuple[int, int]]:
    """Down column 1, then down column 2, and so on."""
    return [(row, col) for col in range(5) for row in range(5)]


def clockwise_spiral_order() -> list[tuple[int, int]]:
    """Cell order for a clockwise spiral, starting at the top left."""
    top, left, bottom, right = 0, 0, 4, 4
    order: list[tuple[int, int]] = []
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            order.append((top, col))
        top += 1
        for row in range(top, bottom + 1):
            order.append((row, right))
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                order.append((bottom, col))
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                order.append((row, left))
            left += 1
    return order


def square_horizontal(keyword: str) -> str:
    """5 by 5 square: keyword, then unused letters, by rows."""
    return _place(horizontal_order(), _keyword_then_rest(keyword))


def square_vertical(keyword: str) -> str:
    """5 by 5 square: keyword, then unused letters, down the columns."""
    return _place(vertical_order(), _keyword_then_rest(keyword))


def square_clockwise_spiral(keyword: str) -> str:
    """5 by 5 square: keyword, then unused letters, in a clockwise spiral."""
    return _place(clockwise_spiral_order(), _keyword_then_rest(keyword))


def _coords(square: str) -> dict[str, tuple[int, int]]:
    return {ch: divmod(i, 5) for i, ch in enumerate(square)}


def _choice_indexes(choices: Sequence[int] | None, count: int, label: str) -> list[int]:
    if choices is None:
        return [0] * count
    if isinstance(choices, (str, bytes)) or len(choices) != count:
        raise ValueError(f"{label} must list {count} indexes")
    out: list[int] = []
    for item in choices:
        if isinstance(item, bool) or not isinstance(item, int) or item < 0 or item > 4:
            raise ValueError(f"{label} indexes must be integers from 0 through 4")
        out.append(item)
    return out


def tri_square_encrypt(
    text: str,
    square1: str,
    square2: str,
    square3: str,
    first_rows: Sequence[int] | None = None,
    third_cols: Sequence[int] | None = None,
) -> str:
    """Encrypt with three known squares.

    An odd letter count is padded with X, as the sheet does for this
    example. first_rows picks the cipher letter in the square 1 column,
    counting from the top. third_cols picks the cipher letter in the
    square 2 row, counting from the left. Both default to 0. Spaces and
    other non-letters are dropped.
    """
    left = normalize_square(square1)
    top = normalize_square(square2)
    middle = normalize_square(square3)
    left_at = _coords(left)
    top_at = _coords(top)
    stream = tri_square_letters(text)
    if not stream:
        raise ValueError("plaintext has no letters")
    if len(stream) % 2 == 1:
        stream += "X"
    pairs = len(stream) // 2
    row_choice = _choice_indexes(first_rows, pairs, "first_rows")
    col_choice = _choice_indexes(third_cols, pairs, "third_cols")
    out: list[str] = []
    for index in range(pairs):
        first = stream[2 * index]
        second = stream[2 * index + 1]
        row1, col1 = left_at[first]
        row2, col2 = top_at[second]
        out.append(left[row_choice[index] * 5 + col1])
        out.append(middle[row1 * 5 + col2])
        out.append(top[row2 * 5 + col_choice[index]])
    return "".join(out)


def tri_square_decrypt(
    text: str,
    square1: str,
    square2: str,
    square3: str,
) -> str:
    """Decrypt with three known squares.

    The middle cipher letter fixes the row in square 1 and the column in
    square 2. The first cipher letter fixes the column in square 1. The
    third cipher letter fixes the row in square 2. Spaces in the
    ciphertext are grouping only and are dropped.
    """
    left = normalize_square(square1)
    top = normalize_square(square2)
    middle = normalize_square(square3)
    left_at = _coords(left)
    top_at = _coords(top)
    middle_at = _coords(middle)
    stream = tri_square_letters(text)
    if not stream or len(stream) % 3 != 0:
        raise ValueError("tri-square ciphertext needs a positive multiple of 3 letters")
    out: list[str] = []
    for index in range(0, len(stream), 3):
        c1, c2, c3 = stream[index], stream[index + 1], stream[index + 2]
        if c1 not in left_at or c2 not in middle_at or c3 not in top_at:
            raise ValueError("ciphertext letter is not in the matching square")
        row3, col3 = middle_at[c2]
        _row1, col1 = left_at[c1]
        row2, _col2 = top_at[c3]
        out.append(left[row3 * 5 + col1])
        out.append(top[row2 * 5 + col3])
    return "".join(out)


def tri_square_groups(ciphertext: str) -> str:
    """Insert a space between trigraphs. Does not add the sheet's period."""
    letters = tri_square_letters(ciphertext)
    return " ".join(letters[i : i + 3] for i in range(0, len(letters), 3))


def solve_tri_square(
    text: str,
    *,
    square1: str,
    square2: str,
    square3: str,
) -> SolveResult:
    """Recover plaintext from a tri-square ciphertext when the squares are known.

    This is a known-cipher, known-key decrypt. It does not search for an
    unknown key, does not read an unknown script, and does not claim a
    reading of army message Nr. 86.
    """
    left = normalize_square(square1)
    top = normalize_square(square2)
    middle = normalize_square(square3)
    plaintext = tri_square_decrypt(text, left, top, middle)
    az = [ord(ch) - 65 for ch in plaintext]
    return SolveResult(
        method="tri_square",
        plaintext=plaintext,
        key=left + "/" + top + "/" + middle,
        score=get_model().score(az) if az else 0.0,
        details={
            "square1": left,
            "square2": top,
            "square3": middle,
            "omitted_letter": "J",
            "letters": len(az),
            "source_example": ACA_URL,
            "spaces": "not_enciphered",
            "scope": _SCOPE,
        },
    )
