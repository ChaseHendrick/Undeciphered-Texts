"""CM Bifid (Conjugated Matrix Bifid) known-key solver.

CM Bifid follows Bifid fractionation, then reads each new coordinate
pair in a second 5 by 5 square. The American Cryptogram Association
sheet states the rule and prints a worked example:

  https://www.cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf

The sheet says to proceed as for Bifid, and after the numbers are read
horizontally, to take the letter from the second Polybius square. The
ciphertext square on the sheet is keyword NOVELTY written in
alternating verticals. The plaintext square is the square printed on
that sheet. The companion Bifid sheet, which this sheet cites
("See: BIFID"), names that square as keyword EXTRAORDINARY written in
a clockwise spiral and sets the same example's period at 7:

  https://www.cryptogram.org/downloads/aca.info/ciphers/Bifid.pdf

The CM sheet writes the ciphertext in period-length groups. The first
two groups have 7 letters, and the last group is the short remainder.

This module is a known classical-cipher solver. It recovers plaintext
only when both squares and the period are supplied. It is not an
unknown-script reading. It does not claim a solution of Kryptos K4,
Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script,
rongorongo, or army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# 25-letter alphabet: J is folded into I, as on the ACA 5 by 5 squares.
CM_BIFID_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# ACA CM Bifid sheet (fetched 2026-10-03). One page, PDF 1.6.
# SHA-256 90d3e1133e00d1100fbee3e3b188cdb621cf4282b415a38cab3b4acf5b2dfd89
ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf"
ACA_PDF_SHA256 = "90d3e1133e00d1100fbee3e3b188cdb621cf4282b415a38cab3b4acf5b2dfd89"
ACA_BIFID_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Bifid.pdf"
ACA_PLAIN_KEYWORD = "EXTRAORDINARY"
ACA_PLAIN_ROUTE = "clockwise_spiral"
ACA_CIPHER_KEYWORD = "NOVELTY"
ACA_CIPHER_ROUTE = "alternating_verticals"
ACA_PERIOD = 7
# Spaces in "Odd periods are popular." are not enciphered.
ACA_PLAIN = "ODDPERIODSAREPOPULAR"
ACA_MESSAGE = "Odd periods are popular."
# Period groups on the sheet: FANXZEX FENUKKR BYNKAK.
ACA_CIPHER = "FANXZEXFENUKKRBYNKAK"
ACA_PRINTED_CIPHER = "FANXZEX FENUKKR BYNKAK"
# Row-major squares printed on the CM Bifid sheet.
ACA_PLAIN_SQUARE = "EXTRAKLMPOHWZQDGVUSIFCBYN"
ACA_CIPHER_SQUARE = "NCDRSOBFQUVAGPWEYHMXLTIKZ"
# Ordinary Bifid of the same plaintext and plaintext square (Bifid sheet).
ACA_BIFID_CIPHER = "MWEINGIMGEOYYRLVEYWY"

_SCOPE = (
    "Known classical CM Bifid cipher solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, Linear A, the Indus script, "
    "rongorongo, or army message Nr. 86."
)


def cm_bifid_letters(text: str) -> str:
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
    cells = cm_bifid_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25:
        raise ValueError("CM Bifid square must be 25 distinct letters without J")
    missing = [ch for ch in CM_BIFID_ALPHABET if ch not in cells]
    if missing:
        raise ValueError("CM Bifid square missing letters: " + "".join(missing))
    return cells


def _keyword_then_rest(keyword: str) -> str:
    cleaned = cm_bifid_letters(keyword)
    if not cleaned:
        raise ValueError("CM Bifid keyword must contain at least one letter")
    seen: set[str] = set()
    head: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            head.append(ch)
    rest = [ch for ch in CM_BIFID_ALPHABET if ch not in seen]
    stream = "".join(head) + "".join(rest)
    if len(stream) != 25:
        raise ValueError("CM Bifid square fill must be 25 letters")
    return stream


def _place(order: list[tuple[int, int]], stream: str) -> str:
    if len(order) != 25 or len(stream) != 25:
        raise ValueError("CM Bifid route must cover 25 cells")
    grid = [[""] * 5 for _ in range(5)]
    for (row, col), ch in zip(order, stream):
        grid[row][col] = ch
    return "".join("".join(row) for row in grid)


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


def alternating_verticals_order() -> list[tuple[int, int]]:
    """Down column 1, up column 2, down column 3, and so on."""
    order: list[tuple[int, int]] = []
    for col in range(5):
        rows = range(5) if col % 2 == 0 else range(4, -1, -1)
        for row in rows:
            order.append((row, col))
    return order


def square_clockwise_spiral(keyword: str) -> str:
    """5 by 5 square: keyword, then unused letters, in a clockwise spiral."""
    return _place(clockwise_spiral_order(), _keyword_then_rest(keyword))


def square_alternating_verticals(keyword: str) -> str:
    """5 by 5 square: keyword, then unused letters, in alternating verticals."""
    return _place(alternating_verticals_order(), _keyword_then_rest(keyword))


def _coords(square: str) -> dict[str, tuple[int, int]]:
    return {ch: divmod(i, 5) for i, ch in enumerate(square)}


def _require_period(period: int) -> int:
    if not isinstance(period, int) or isinstance(period, bool) or period < 1:
        raise ValueError("period must be an integer of at least 1")
    return period


def cm_bifid_encrypt(
    text: str,
    plain_square: str,
    cipher_square: str,
    period: int,
) -> str:
    """Encrypt with two known squares and a period.

    Coordinates come from the plaintext square. Each new pair is read
    in the ciphertext square. Spaces and other non-letters are dropped.
    """
    _require_period(period)
    plain = normalize_square(plain_square)
    cipher = normalize_square(cipher_square)
    pos = _coords(plain)
    stream = cm_bifid_letters(text)
    if not stream:
        raise ValueError("plaintext has no letters")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        rows: list[int] = []
        cols: list[int] = []
        for ch in block:
            row, col = pos[ch]
            rows.append(row)
            cols.append(col)
        digits = rows + cols
        for i in range(0, len(digits), 2):
            out.append(cipher[digits[i] * 5 + digits[i + 1]])
    return "".join(out)


def cm_bifid_decrypt(
    text: str,
    plain_square: str,
    cipher_square: str,
    period: int,
) -> str:
    """Decrypt with two known squares and a period.

    Ciphertext letters are located in the ciphertext square. The digit
    stream splits into rows and columns, which are read in the plaintext
    square. Spaces in the ciphertext are grouping only and are dropped.
    """
    _require_period(period)
    plain = normalize_square(plain_square)
    cipher = normalize_square(cipher_square)
    pos = _coords(cipher)
    stream = cm_bifid_letters(text)
    if not stream:
        raise ValueError("ciphertext has no letters")
    out: list[str] = []
    for start in range(0, len(stream), period):
        block = stream[start : start + period]
        digits: list[int] = []
        for ch in block:
            row, col = pos[ch]
            digits.extend((row, col))
        n = len(block)
        rows = digits[:n]
        cols = digits[n:]
        for row, col in zip(rows, cols):
            out.append(plain[row * 5 + col])
    return "".join(out)


def solve_cm_bifid(
    text: str,
    *,
    plain_square: str,
    cipher_square: str,
    period: int,
) -> SolveResult:
    """Recover CM Bifid plaintext when both squares and the period are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about an unsolved historical ciphertext.
    """
    plain_key = normalize_square(plain_square)
    cipher_key = normalize_square(cipher_square)
    _require_period(period)
    stream = cm_bifid_letters(text)
    plain = cm_bifid_decrypt(stream, plain_key, cipher_key, period)
    return SolveResult(
        method="cm_bifid",
        plaintext=plain,
        key=f"{plain_key}/{cipher_key}/{period}",
        score=float(len(plain)),
        details={
            "plain_square": plain_key,
            "cipher_square": cipher_key,
            "period": period,
            "letters": len(stream),
            "mode": "known_squares_and_period",
            "scope": _SCOPE,
            "source_url": ACA_URL,
            "spaces": "not_enciphered",
        },
    )


__all__ = [
    "ACA_BIFID_CIPHER",
    "ACA_BIFID_URL",
    "ACA_CIPHER",
    "ACA_CIPHER_KEYWORD",
    "ACA_CIPHER_ROUTE",
    "ACA_CIPHER_SQUARE",
    "ACA_MESSAGE",
    "ACA_PDF_SHA256",
    "ACA_PERIOD",
    "ACA_PLAIN",
    "ACA_PLAIN_KEYWORD",
    "ACA_PLAIN_ROUTE",
    "ACA_PLAIN_SQUARE",
    "ACA_PRINTED_CIPHER",
    "ACA_URL",
    "CM_BIFID_ALPHABET",
    "alternating_verticals_order",
    "clockwise_spiral_order",
    "cm_bifid_decrypt",
    "cm_bifid_encrypt",
    "cm_bifid_letters",
    "normalize_square",
    "solve_cm_bifid",
    "square_alternating_verticals",
    "square_clockwise_spiral",
]
