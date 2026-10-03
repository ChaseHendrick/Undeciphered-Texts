"""Swagman known-key solver: Latin-square column transposition.

The Swagman cipher was proposed by ACA member BUNYIP (The Cryptogram,
Sep-Oct 1977). The key is a square of height n filled with the numbers
1 through n so that no number repeats in a row or in a column (a Latin
square). ACA sheets use n from 4 to 8.

Plaintext letters are written left to right in n rows. If the letter
count is not a multiple of n, X nulls fill the last row. Each column
is reordered by the key column above it (the square repeats across the
width): the letter whose key number is 1 moves to the top, then 2, and
so on. Ciphertext is read down those columns.

Decryption puts each ciphertext column back into the rows selected by
those key numbers and reads the rows left to right.

The worked example is the American Cryptogram Association Swagman sheet
(fetched 2026-10-02):

  https://www.cryptogram.org/downloads/aca.info/ciphers/Swagman.pdf

Key square:

  3 2 1 4 5
  1 5 3 2 4
  2 4 5 3 1
  5 3 4 1 2
  4 1 2 5 3

Plaintext on that sheet: "Don't be afraid to take a big leap if one is
indicated. You cannot cross a river or a chasm in two small jumps."
Spaces and punctuation are not enciphered. The letter stream is

  DONTBEAFRAIDTOTAKEABIGLEAPIFONEISINDICATEDYOUCANNOTCROSSARIVERORACHASMINTWOSMALLJUMPS

Ciphertext (5-letter groups on the sheet):

  ENDSC MORDA NIBOI SICTN ASTGB LTEWA OAREE FSAID VPYRM OEAIA FUILR
  LDOCO TJNRA AENOU NCMIT SOAPH SKATI

This module is a known-cipher solver for a known classical cipher. It
recovers plaintext only when the numeric key square is supplied. It is
not an unknown-script reading and not a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.result import SolveResult

# ACA Swagman sheet (fetched 2026-10-02).
ACA_SWAGMAN_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Swagman.pdf"
)
ACA_SWAGMAN_KEY = "32145 15324 24531 53412 41253"
ACA_SWAGMAN_PLAIN = (
    "DONTBEAFRAIDTOTAKEABIGLEAPIFONEISINDICATED"
    "YOUCANNOTCROSSARIVERORACHASMINTWOSMALLJUMPS"
)
ACA_SWAGMAN_CIPHER = (
    "ENDSCMORDANIBOISICTNASTGBLTEWAOAREEFSAIDVPYRM"
    "OEAIAFUILRLDOCOTJNRAAENOUNCMITSOAPHSKATI"
)

_SCOPE = (
    "Known classical Swagman cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)
_NULL = "X"


def parse_swagman_key(key: str) -> tuple[tuple[int, ...], ...]:
    """Parse a Latin square written as digit rows.

    Rows are separated by spaces, commas, slashes, or newlines. Each row
    is a string of digits 1..n with no repeats. The square must be n by n
    and no digit may repeat down a column. n is from 2 to 9.
    """
    raw = key.strip()
    if not raw:
        raise ValueError("Swagman key square must contain at least one row")
    rows_text: list[str] = []
    for line in raw.replace(",", " ").replace("/", " ").split():
        digits = "".join(ch for ch in line if ch.isdigit())
        if not digits or len(digits) != len(line.strip()):
            # A token may be a whole row ("32145") or already split.
            if digits and all(ch.isdigit() for ch in line.strip()):
                rows_text.append(digits)
            elif not digits:
                continue
            else:
                raise ValueError(
                    "Swagman key rows must be digits only, one row per token"
                )
        else:
            rows_text.append(digits)
    if not rows_text:
        raise ValueError("Swagman key square must contain at least one row")
    n = len(rows_text)
    if n < 2 or n > 9:
        raise ValueError("Swagman key square height must be from 2 to 9")
    square: list[tuple[int, ...]] = []
    expected = set(range(1, n + 1))
    for row_text in rows_text:
        if len(row_text) != n:
            raise ValueError(
                "Swagman key must be a square: each row needs "
                f"{n} digits, got {len(row_text)}"
            )
        row = tuple(int(ch) for ch in row_text)
        if set(row) != expected or len(set(row)) != n:
            raise ValueError(
                "each Swagman key row must contain 1..n once"
            )
        square.append(row)
    for c in range(n):
        col = [square[r][c] for r in range(n)]
        if set(col) != expected:
            raise ValueError(
                "each Swagman key column must contain 1..n once"
            )
    return tuple(square)


def format_swagman_key(square: tuple[tuple[int, ...], ...]) -> str:
    """Canonical key: one digit-row per space-separated token."""
    return " ".join("".join(str(n) for n in row) for row in square)


def _rows(letters: str, n: int) -> list[list[str]]:
    width = len(letters) // n
    return [
        list(letters[r * width : (r + 1) * width])
        for r in range(n)
    ]


def swagman_encrypt(text: str, key: str) -> str:
    """Encrypt with a known Swagman key square. Non-letters are dropped.

    Incomplete final rows are filled with X so the rectangle height
    matches the key square. The published ACA example needs no nulls.
    """
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    square = parse_swagman_key(key)
    n = len(square)
    pad = (-len(letters)) % n
    letters = letters + (_NULL * pad)
    grid = _rows(letters, n)
    width = len(grid[0])
    out: list[str] = []
    for c in range(width):
        key_col = [square[r][c % n] for r in range(n)]
        for number in range(1, n + 1):
            row = key_col.index(number)
            out.append(grid[row][c])
    return "".join(out)


def swagman_decrypt(text: str, key: str) -> str:
    """Decrypt with a known Swagman key square.

    Ciphertext length must be a multiple of the square height (nulls, if
    any, are already in the ciphertext). Letters are restored to the row
    selected by each key number, then read left to right.
    """
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    square = parse_swagman_key(key)
    n = len(square)
    if len(letters) % n != 0:
        raise ValueError(
            "Swagman ciphertext length must be a multiple of the key height"
        )
    width = len(letters) // n
    grid = [[""] * width for _ in range(n)]
    index = 0
    for c in range(width):
        key_col = [square[r][c % n] for r in range(n)]
        for number in range(1, n + 1):
            row = key_col.index(number)
            grid[row][c] = letters[index]
            index += 1
    return "".join("".join(row) for row in grid)


def solve_swagman(text: str, *, key: str) -> SolveResult:
    """Recover Swagman plaintext when the numeric key square is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    square = parse_swagman_key(key)
    cleaned = format_swagman_key(square)
    plain_letters = swagman_decrypt(text, cleaned)
    return SolveResult(
        method="swagman",
        plaintext=plain_letters,
        key=cleaned,
        score=float(len(plain_letters)),
        details={
            "key": cleaned,
            "height": len(square),
            "letters": len(letters_only(text)),
            "mode": "known_swagman",
            "variant": "latin_square_column_permutation",
            "scope": _SCOPE,
            "source_url": ACA_SWAGMAN_URL,
        },
    )


__all__ = [
    "ACA_SWAGMAN_CIPHER",
    "ACA_SWAGMAN_KEY",
    "ACA_SWAGMAN_PLAIN",
    "ACA_SWAGMAN_URL",
    "format_swagman_key",
    "parse_swagman_key",
    "solve_swagman",
    "swagman_decrypt",
    "swagman_encrypt",
]
