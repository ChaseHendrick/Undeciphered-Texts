"""Cadenus (ACA) known-key solver: 25-row columnar transposition.

Cadenus writes plaintext in rows under a keyword, cycles each column so
the row labeled with that key letter moves to the top, reorders the
columns alphabetically, and reads the ciphertext by rows. The American
Cryptogram Association cipher sheet prints a full worked example:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Cadenus.pdf

Row labels are a 25-letter alphabet with V and W in one cell: A on the
top row, then Z down through B. A repeated keyword letter keeps
left-to-right order when the columns are numbered.

This module encrypts and decrypts only when the keyword is supplied.
It is a known classical-cipher helper for a published fixture. It does
not read ancient scripts, unknown languages, or claim any historical
break of an unsolved ciphertext.
"""

from __future__ import annotations

from engine.result import SolveResult

# Sheet page for keyword EASY. Fetched from the URL below.
# Plaintext on the sheet: "A severe limitation on the usefulness of the
# Cadenus is that every message must be a multiple of twenty-five letters
# long." Spaces and the hyphen are not enciphered.
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Cadenus.pdf"
ACA_KEYWORD = "EASY"
ACA_NUMERIC_KEY = "2-1-3-4"
ACA_PLAIN = (
    "ASEVERELIMITATIONONTHEUSEFULNESSOFTHECADENUSISTHATEVERYMESSAGE"
    "MUSTBEAMULTIPLEOFTWENTYFIVELETTERSLONG"
)
ACA_CIPHER = (
    "SYSTRETOMTATTLUSOATLEEESFIYHEASDFNMSCHBHNEUVSNPMTOFARENUSEIE"
    "EIELTARLMENTIEETOGEVESITFAISLTNGEEUVOWUL"
)
ACA_PRINTED = (
    "A severe limitation on the usefulness of the Cadenus is that every "
    "message must be a multiple of twenty-five letters long."
)

ROWS = 25


def cadenus_letters(text: str) -> str:
    """Uppercase A-Z stream. Spaces, digits, and punctuation are dropped."""
    if not isinstance(text, str):
        raise ValueError("cadenus text must be a string")
    return "".join(ch.upper() for ch in text if ch.isalpha())


def _alphabet_index(letter: str) -> int:
    """Index in the 25-letter alphabet. V and W both return 21. A is 0. Z is 24."""
    ch = letter.upper()
    if ch == "W":
        ch = "V"
    if len(ch) != 1 or not ("A" <= ch <= "Z"):
        raise ValueError("cadenus key letter must be A-Z")
    pos = ord(ch) - ord("A")
    # ASCII leaves a slot for W. After folding W onto V, X/Y/Z move down one.
    if pos >= 23:
        pos -= 1
    return pos


def row_shift(letter: str) -> int:
    """Row of this key letter on the ACA sheet (0 is the top row, labeled A).

    The sheet attaches the 25-letter alphabet to the rows with A at the top
    and then Z, Y, X, V/W, U, and so on down to B. Cycling a column by this
    many letters brings that row to the top. E is row 21, the 22nd row,
    which is the shift printed for the E column of EASY.
    """
    return (ROWS - _alphabet_index(letter)) % ROWS


def keyword_letters(keyword: str) -> str:
    """Keyword as uppercase letters. Other characters are ignored."""
    letters = cadenus_letters(keyword)
    if not letters:
        raise ValueError("cadenus keyword must contain at least one letter")
    return letters


def numeric_key(keyword: str) -> str:
    """1-based column numbers in keyword order, hyphen-separated.

    Letters are ordered alphabetically. A repeated letter keeps
    left-to-right order, so the left copy gets the smaller number.
    EASY is 2-1-3-4, matching the ACA sheet.
    """
    key = keyword_letters(keyword)
    order = sorted(range(len(key)), key=lambda i: (key[i], i))
    ranks = [0] * len(key)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    return "-".join(str(rank) for rank in ranks)


def _ranks(key: str) -> list[int]:
    """0-based alphabetical rank of each keyword letter. Ties stay left to right."""
    order = sorted(range(len(key)), key=lambda i: (key[i], i))
    ranks = [0] * len(key)
    for rank, index in enumerate(order):
        ranks[index] = rank
    return ranks


def _require_block(stream: str, width: int, role: str) -> None:
    block = ROWS * width
    if not stream:
        raise ValueError(f"cadenus {role} has no letters")
    if len(stream) % block != 0:
        raise ValueError(
            f"cadenus {role} length must be a multiple of 25 times the "
            f"keyword length ({block} for this keyword); got {len(stream)}"
        )


def _columns_from_rows(stream: str, width: int) -> list[str]:
    columns = [""] * width
    for index, ch in enumerate(stream):
        columns[index % width] += ch
    return columns


def _read_rows(columns: list[str]) -> str:
    width = len(columns)
    out: list[str] = []
    for row in range(ROWS):
        for col in range(width):
            out.append(columns[col][row])
    return "".join(out)


def _cycle_up(column: str, shift: int) -> str:
    if shift == 0:
        return column
    return column[shift:] + column[:shift]


def _cycle_down(column: str, shift: int) -> str:
    if shift == 0:
        return column
    return column[-shift:] + column[:-shift]


def cadenus_encrypt(text: str, keyword: str) -> str:
    """Encrypt with a known keyword. Non-letters in the text are dropped."""
    key = keyword_letters(keyword)
    stream = cadenus_letters(text)
    width = len(key)
    _require_block(stream, width, "plaintext")
    ranks = _ranks(key)
    blocks: list[str] = []
    block = ROWS * width
    for start in range(0, len(stream), block):
        columns = _columns_from_rows(stream[start : start + block], width)
        rotated = [_cycle_up(columns[i], row_shift(key[i])) for i in range(width)]
        ordered = [""] * width
        for index, rank in enumerate(ranks):
            ordered[rank] = rotated[index]
        blocks.append(_read_rows(ordered))
    return "".join(blocks)


def cadenus_decrypt(text: str, keyword: str) -> str:
    """Decrypt with a known keyword. Non-letters in the text are dropped."""
    key = keyword_letters(keyword)
    stream = cadenus_letters(text)
    width = len(key)
    _require_block(stream, width, "ciphertext")
    ranks = _ranks(key)
    blocks: list[str] = []
    block = ROWS * width
    for start in range(0, len(stream), block):
        ordered = _columns_from_rows(stream[start : start + block], width)
        columns = [""] * width
        for index, rank in enumerate(ranks):
            columns[index] = ordered[rank]
        restored = [_cycle_down(columns[i], row_shift(key[i])) for i in range(width)]
        blocks.append(_read_rows(restored))
    return "".join(blocks)


def solve_cadenus(text: str, *, keyword: str) -> SolveResult:
    """Recover Cadenus plaintext when the keyword is known.

    This is a known-cipher decrypt, not a blind cryptanalysis search and not
    an ancient-script reading. The keyword is the only key.
    """
    key = keyword_letters(keyword)
    stream = cadenus_letters(text)
    plain = cadenus_decrypt(stream, key)
    numbers = numeric_key(key)
    return SolveResult(
        method="cadenus",
        plaintext=plain,
        key=key,
        score=float(len(plain)),
        details={
            "keyword": key,
            "numeric_key": numbers,
            "width": len(key),
            "letters": len(stream),
            "mode": "known_keyword",
            "scope": (
                "Known classical Cadenus decrypt only; "
                "not an ancient-script or unknown-language reading."
            ),
            "source_url": ACA_URL,
        },
    )


__all__ = [
    "ACA_CIPHER",
    "ACA_KEYWORD",
    "ACA_NUMERIC_KEY",
    "ACA_PLAIN",
    "ACA_PRINTED",
    "ACA_URL",
    "ROWS",
    "cadenus_decrypt",
    "cadenus_encrypt",
    "cadenus_letters",
    "keyword_letters",
    "numeric_key",
    "row_shift",
    "solve_cadenus",
]
