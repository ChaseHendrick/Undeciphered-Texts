"""AMSCO (ACA) known-key solver: incomplete columnar with alternating cells.

AMSCO writes plaintext in rows under a numeric key. Cells alternate between
a single letter and a digraph. The first cell may be either one. In both
even and odd periods the first column and the first row always alternate,
so a cell is a digraph when (row + column) has the same parity as the first
cell. Columns are then read in key order, top to bottom. A final cell may
be shorter than its pattern. A null is not required.

The American Cryptogram Association cipher sheet prints a worked example:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf

Key 41325. The plaintext on the sheet is "Incomplete columnar with
alternating single letters and digraphs." The first cell is the digraph
IN. Spaces are not enciphered.

This module encrypts and decrypts only when the numeric key and the first
cell size are supplied. It is a known classical-cipher solver (a
known-cipher solver). It does not read ancient scripts, unknown languages,
or claim any historical break of an unsolved ciphertext. It is not a claim
about Kryptos K4, Zodiac Z13, Zodiac Z32, the Beale ciphers, the McCormick
cipher, the Voynich manuscript, or army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# Sheet page for key 41325. Fetched from the URL below.
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf"
ACA_KEY = "41325"
# The sheet's first cell is the digraph "in", not a single letter.
ACA_START = "digraph"
ACA_PLAIN = "INCOMPLETECOLUMNARWITHALTERNATINGSINGLELETTERSANDDIGRAPHS"
ACA_PRINTED = (
    "Incomplete columnar with alternating single letters and digraphs."
)
# Grouping spaces and the final period on the sheet are not ciphertext.
ACA_CIPHER = "CECRTEGLENPHPLUTNANTEIOMOWIRSITDDSINTNALINESAALEMHATGLRGR"
ACA_CIPHER_GROUPS = (
    "CECRT EGLEN PHPLU TNANT EIOMO WIRSI TDDSI NTNAL INESA ALEMH ATGLR GR"
)

_SCOPE = (
    "Known classical AMSCO cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac Z13, Zodiac Z32, the Beale ciphers, the McCormick cipher, "
    "the Voynich manuscript, or army message Nr. 86."
)


def amsco_letters(text: str) -> str:
    """Uppercase A-Z stream. Spaces, digits, and punctuation are dropped."""
    if not isinstance(text, str):
        raise ValueError("amsco text must be a string")
    return "".join(ch.upper() for ch in text if ch.isalpha())


def normalize_key(key: str) -> str:
    """Numeric key as a permutation of 1..n, one digit per column.

    "41325" means five columns read in the order column 2, column 4,
    column 3, column 1, column 5 (1-based positions of those digits).
    """
    if not isinstance(key, str):
        raise ValueError("amsco key must be a string of digits")
    digits = key.strip()
    if not digits.isdigit() or len(digits) < 2 or len(digits) > 9:
        raise ValueError("amsco key must be 2 to 9 digits")
    if len(set(digits)) != len(digits):
        raise ValueError("amsco key digits must be unique")
    expected = "".join(str(i) for i in range(1, len(digits) + 1))
    if "".join(sorted(digits)) != expected:
        raise ValueError("amsco key must be a permutation of 1..n")
    return digits


def normalize_start(start: str) -> str:
    """Return "digraph" or "single"."""
    if not isinstance(start, str):
        raise ValueError("amsco start must be 'digraph' or 'single'")
    name = start.strip().lower()
    if name in {"digraph", "d", "2", "pair"}:
        return "digraph"
    if name in {"single", "s", "1", "letter"}:
        return "single"
    raise ValueError("amsco start must be 'digraph' or 'single'")


def _widths(n_letters: int, width: int, start_digraph: bool) -> list[list[int]]:
    """Cell widths, row by row. The last cell may be shorter than that pattern."""
    if n_letters < 1:
        raise ValueError("amsco text has no letters")
    rows: list[list[int]] = []
    left = n_letters
    row_index = 0
    while left > 0:
        row: list[int] = []
        for col in range(width):
            if left <= 0:
                break
            same_parity = (row_index + col) % 2 == 0
            nominal = 2 if same_parity == start_digraph else 1
            take = nominal if left >= nominal else left
            row.append(take)
            left -= take
        rows.append(row)
        row_index += 1
    return rows


def _column_order(key: str) -> list[int]:
    """Column indexes in the order their key digits are read (1, then 2, ...)."""
    return sorted(range(len(key)), key=lambda index: int(key[index]))


def _take_columns(stream: str, widths: list[list[int]], key: str) -> str:
    columns = [""] * len(key)
    cursor = 0
    for row in widths:
        for col, size in enumerate(row):
            columns[col] += stream[cursor : cursor + size]
            cursor += size
    return "".join(columns[index] for index in _column_order(key))


def _read_columns(stream: str, widths: list[list[int]], key: str) -> str:
    lengths = [0] * len(key)
    for row in widths:
        for col, size in enumerate(row):
            lengths[col] += size
    columns = [""] * len(key)
    cursor = 0
    for index in _column_order(key):
        size = lengths[index]
        columns[index] = stream[cursor : cursor + size]
        cursor += size
    if cursor != len(stream):
        raise ValueError("amsco ciphertext length does not match the grid")
    plain: list[str] = []
    cursors = [0] * len(key)
    for row in widths:
        for col, size in enumerate(row):
            start = cursors[col]
            plain.append(columns[col][start : start + size])
            cursors[col] = start + size
    return "".join(plain)


def amsco_encrypt(text: str, key: str, *, start: str = ACA_START) -> str:
    """Encrypt with a known numeric key. Non-letters in the text are dropped."""
    numeric = normalize_key(key)
    start_name = normalize_start(start)
    stream = amsco_letters(text)
    widths = _widths(len(stream), len(numeric), start_name == "digraph")
    return _take_columns(stream, widths, numeric)


def amsco_decrypt(text: str, key: str, *, start: str = ACA_START) -> str:
    """Decrypt with a known numeric key. Non-letters in the text are dropped."""
    numeric = normalize_key(key)
    start_name = normalize_start(start)
    stream = amsco_letters(text)
    widths = _widths(len(stream), len(numeric), start_name == "digraph")
    return _read_columns(stream, widths, numeric)


def solve_amsco(text: str, *, key: str, start: str = ACA_START) -> SolveResult:
    """Recover AMSCO plaintext when the numeric key and first cell are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac Z13, Zodiac Z32, the Beale ciphers,
    the McCormick cipher, the Voynich manuscript, or army message Nr. 86.
    """
    numeric = normalize_key(key)
    start_name = normalize_start(start)
    stream = amsco_letters(text)
    plain = amsco_decrypt(stream, numeric, start=start_name)
    return SolveResult(
        method="amsco",
        plaintext=plain,
        key=f"{numeric}/{start_name}",
        score=float(len(plain)),
        details={
            "key": numeric,
            "numeric_key": numeric,
            "start": start_name,
            "period": len(numeric),
            "letters": len(stream),
            "mode": "known_numeric_key",
            "scope": _SCOPE,
            "source_url": ACA_URL,
            "spaces": "not_enciphered",
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_CIPHER_GROUPS",
    "ACA_KEY",
    "ACA_PLAIN",
    "ACA_PRINTED",
    "ACA_START",
    "ACA_URL",
    "amsco_decrypt",
    "amsco_encrypt",
    "amsco_letters",
    "normalize_key",
    "normalize_start",
    "solve_amsco",
]
