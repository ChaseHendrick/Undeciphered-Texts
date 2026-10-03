"""Myszkowski transposition known-key solver.

The American Cryptogram Association cipher sheet (fetched 2026-10-03)
describes Myszkowski transposition:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf

Choose a keyword with repeated letters. Number the letters in
alphabetical order. Repeated letters take the same number. Write the
plaintext in rows under the keyword. An incomplete last row is allowed.
Take the ciphertext off by key number. Columns that share a number are
read by rows, left to right and top to bottom, not one column at a time.

On that sheet the keyword is BANANA, numbered 2 1 3 1 3 1. The plaintext
begins "Incomplete columnar with pattern word key". The printed
ciphertext is grouped in fives and ends with a period. The period is
not a letter. Spaces and case are not enciphered.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the keyword is supplied.
It is **not** an unknown-script reading. It does **not** claim
Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick
cipher, the Voynich manuscript, or army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# ACA Myszkowski sheet (fetched 2026-10-03).
ACA_MYSZKOWSKI_URL = (
    "https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf"
)
ACA_MYSZKOWSKI_KEYWORD = "BANANA"
ACA_MYSZKOWSKI_NUMERIC = "2-1-3-1-3-1"
ACA_MYSZKOWSKI_SHEET_PLAIN = (
    "Incomplete columnar with pattern word key and letters under "
    "same number taken off by row from top to bottom."
)
ACA_MYSZKOWSKI_PLAIN = (
    "INCOMPLETECOLUMNARWITHPATTERNWORDKEYANDLETTERSUNDER"
    "SAMENUMBERTAKENOFFBYROWFROMTOPTOBOTTOM"
)
ACA_MYSZKOWSKI_CIPHER = (
    "NOPEE OUNRI HATRW RKYNL TESNE SMNME TKNFB RWRMO TBTOI LLWTO ATDER "
    "OOTOC MTCMA TPEND EDERU RAUBA EFYFO POTM"
)

_GROUP = 5

_SCOPE = (
    "Known classical Myszkowski transposition solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "the Zodiac ciphers, the Beale ciphers, the McCormick cipher, "
    "the Voynich manuscript, or army message Nr. 86."
)


def _letters(text: str) -> str:
    """Uppercase A-Z letters, in order. Spaces and punctuation are dropped."""
    if not isinstance(text, str):
        raise ValueError("myszkowski text must be a string")
    return "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())


def myszkowski_numbers(keyword: str) -> list[int]:
    """1-based alphabetical numbers. Identical letters share one number.

    BANANA is 2, 1, 3, 1, 3, 1: A is 1, B is 2, and N is 3. The ACA sheet
    calls this "the same number as their first appearance."
    """
    letters = _letters(keyword)
    if not letters:
        raise ValueError("myszkowski keyword must contain at least one letter")
    rank = {ch: index for index, ch in enumerate(sorted(set(letters)), start=1)}
    return [rank[ch] for ch in letters]


def numeric_key(keyword: str) -> str:
    """Hyphen-joined numbers, as in 2-1-3-1-3-1 for BANANA."""
    return "-".join(str(number) for number in myszkowski_numbers(keyword))


def keyword_key(keyword: str) -> str:
    """Canonical keyword: uppercase A-Z letters only."""
    letters = _letters(keyword)
    if not letters:
        raise ValueError("myszkowski keyword must contain at least one letter")
    return letters


def _heights(length: int, width: int) -> list[int]:
    """How many letters each column holds in an incomplete row-wise grid."""
    if length < 1:
        raise ValueError("myszkowski text must contain at least one letter")
    if width < 1:
        raise ValueError("myszkowski keyword must contain at least one letter")
    full, extra = divmod(length, width)
    return [full + (1 if column < extra else 0) for column in range(width)]


def _group(letters: str) -> str:
    """ACA groups of five. A short final group is kept."""
    return " ".join(
        letters[index : index + _GROUP] for index in range(0, len(letters), _GROUP)
    )


def _columns_by_number(numbers: list[int]) -> list[list[int]]:
    """Column indexes grouped by key number, each group left to right."""
    return [
        [index for index, number in enumerate(numbers) if number == value]
        for value in sorted(set(numbers))
    ]


def myszkowski_encrypt(text: str, keyword: str) -> str:
    """Encrypt with a known Myszkowski keyword.

    Letters are written in rows. Columns that share a key number are read
    by rows from top to bottom. The result is grouped in fives. Spaces
    and punctuation in the plaintext are not enciphered.
    """
    letters = _letters(text)
    numbers = myszkowski_numbers(keyword)
    width = len(numbers)
    heights = _heights(len(letters), width)
    rows = max(heights)
    grid = [[""] * width for _ in range(rows)]
    cursor = 0
    for row in range(rows):
        for column in range(width):
            if row < heights[column]:
                grid[row][column] = letters[cursor]
                cursor += 1
    out: list[str] = []
    for columns in _columns_by_number(numbers):
        for row in range(rows):
            for column in columns:
                if row < heights[column]:
                    out.append(grid[row][column])
    return _group("".join(out))


def myszkowski_decrypt(text: str, keyword: str) -> str:
    """Decrypt with a known Myszkowski keyword.

    Ciphertext fills same-numbered columns by rows, in key-number order.
    Plaintext is the restored grid read by rows. Group spaces and a
    trailing period are ignored.
    """
    letters = _letters(text)
    numbers = myszkowski_numbers(keyword)
    width = len(numbers)
    heights = _heights(len(letters), width)
    rows = max(heights)
    grid = [[""] * width for _ in range(rows)]
    cursor = 0
    for columns in _columns_by_number(numbers):
        for row in range(rows):
            for column in columns:
                if row < heights[column]:
                    grid[row][column] = letters[cursor]
                    cursor += 1
    if cursor != len(letters):
        raise ValueError("myszkowski ciphertext did not fill the grid")
    return "".join(
        grid[row][column]
        for row in range(rows)
        for column in range(width)
        if row < heights[column]
    )


def solve_myszkowski(text: str, *, keyword: str) -> SolveResult:
    """Recover Myszkowski plaintext when the keyword is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or Nr. 86.
    """
    key = keyword_key(keyword)
    plain = myszkowski_decrypt(text, key)
    return SolveResult(
        method="myszkowski",
        plaintext=plain,
        key=key,
        score=float(len(plain)),
        details={
            "key": key,
            "keyword": key,
            "numeric_key": numeric_key(key),
            "width": len(key),
            "letters": len(plain),
            "mode": "known_myszkowski",
            "variant": "aca_myszkowski",
            "scope": _SCOPE,
            "source_url": ACA_MYSZKOWSKI_URL,
        },
    )


__all__ = [
    "ACA_MYSZKOWSKI_CIPHER",
    "ACA_MYSZKOWSKI_KEYWORD",
    "ACA_MYSZKOWSKI_NUMERIC",
    "ACA_MYSZKOWSKI_PLAIN",
    "ACA_MYSZKOWSKI_SHEET_PLAIN",
    "ACA_MYSZKOWSKI_URL",
    "keyword_key",
    "myszkowski_decrypt",
    "myszkowski_encrypt",
    "myszkowski_numbers",
    "numeric_key",
    "solve_myszkowski",
]
