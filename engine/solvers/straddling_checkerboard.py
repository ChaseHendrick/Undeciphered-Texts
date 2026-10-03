"""Straddling checkerboard known-key solver.

Wikipedia (fetched 2026-10-02) publishes a worked example of the modern
straddling checkerboard, also called a monome-binome cipher:

  https://en.wikipedia.org/wiki/Straddling_checkerboard

The example board labels columns 0 through 9. Columns 2 and 6 are blank
in the header, and those digits label the two extra rows. The header
letters, read across the other columns, are ETAONRIS:

    0 1 2 3 4 5 6 7 8 9
    E T   A O N   R I S
  2 B C D F G H J K L M
  6 P Q / U V W X Y Z .

A header letter becomes its one column digit. Any other symbol becomes
its row digit followed by its column digit. The article converts the
string "ATTACK AT DAWN" letter by letter (spaces are not encoded) into
3 1 1 3 21 27 3 1 22 3 65 5, and the resulting message is
3113212731223655. Reading those digits with the same board returns
ATTACKATDAWN.

The key form is row,row|HEADER|BODY. For this board it is
2,6|ETAONRIS|BCDFGHJKLMPQ/UVWXYZ.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the board key is supplied.
It is **not** an unknown-script reading and **not** a claim about
army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

# Wikipedia straddling checkerboard article (fetched 2026-10-02).
WIKIPEDIA_CHECKERBOARD_URL = "https://en.wikipedia.org/wiki/Straddling_checkerboard"
WIKIPEDIA_CHECKERBOARD_KEY = "2,6|ETAONRIS|BCDFGHJKLMPQ/UVWXYZ."
WIKIPEDIA_CHECKERBOARD_PLAIN = "ATTACKATDAWN"
WIKIPEDIA_CHECKERBOARD_SOURCE_TEXT = "ATTACK AT DAWN"
WIKIPEDIA_CHECKERBOARD_CIPHER = "3113212731223655"

_SCOPE = (
    "Known classical straddling checkerboard cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)
_EXTRA = "./"


class Checkerboard:
    """One known board: two row digits, eight header symbols, twenty body symbols."""

    __slots__ = ("row_digits", "header", "body", "encode", "decode")

    def __init__(self, row_digits: tuple[str, str], header: str, body: str) -> None:
        self.row_digits = row_digits
        self.header = header
        self.body = body
        encode: dict[str, str] = {}
        single_columns = [str(n) for n in range(10) if str(n) not in row_digits]
        for symbol, column in zip(header, single_columns, strict=True):
            encode[symbol] = column
        for index, symbol in enumerate(body):
            row = row_digits[0] if index < 10 else row_digits[1]
            encode[symbol] = row + str(index % 10)
        if len(encode) != 28:
            raise ValueError("straddling checkerboard symbols must be unique")
        self.encode = encode
        self.decode = {code: symbol for symbol, code in encode.items()}
        if len(self.decode) != 28:
            raise ValueError("straddling checkerboard codes must be unique")


def _symbols(text: str, *, what: str) -> str:
    out: list[str] = []
    for ch in text:
        if ch.isspace():
            continue
        if "A" <= ch <= "Z" or "a" <= ch <= "z":
            out.append(ch.upper())
            continue
        if ch in _EXTRA:
            out.append(ch)
            continue
        raise ValueError(f"{what} has a symbol that is not A-Z, '.', or '/'")
    return "".join(out)


def parse_checkerboard_key(key: str) -> Checkerboard:
    """Parse ``row,row|HEADER8|BODY20`` into a board.

    Column labels are 0 through 9 from left to right. The two row digits
    are the blank header columns, and they label the two extra rows in
    the order given. HEADER8 fills the other columns. BODY20 fills the
    first extra row, then the second, ten symbols each.
    """
    parts = key.split("|")
    if len(parts) != 3:
        raise ValueError("straddling checkerboard key must be row,row|HEADER|BODY")
    row_part, header_part, body_part = parts
    rows = row_part.split(",")
    if len(rows) != 2 or any(len(item) != 1 or item not in "0123456789" for item in rows):
        raise ValueError("row labels must be two digits written as d,d")
    if rows[0] == rows[1]:
        raise ValueError("the two row digits must differ")
    header = _symbols(header_part, what="header")
    body = _symbols(body_part, what="body")
    if len(header) != 8:
        raise ValueError("header must be 8 symbols")
    if len(body) != 20:
        raise ValueError("body must be 20 symbols")
    symbols = header + body
    if len(set(symbols)) != 28:
        raise ValueError("board symbols must be 28 distinct characters")
    return Checkerboard((rows[0], rows[1]), header, body)


def straddling_checkerboard_encrypt(text: str, key: str) -> str:
    """Encrypt with a known straddling checkerboard key.

    Whitespace is dropped, matching the published example, which does not
    encode the spaces in "ATTACK AT DAWN". '.' and '/' stay when they are
    on the board. Any other character is rejected.
    """
    board = parse_checkerboard_key(key)
    symbols = _symbols(text, what="plaintext")
    if not symbols:
        raise ValueError("plaintext has no symbols")
    out: list[str] = []
    for symbol in symbols:
        code = board.encode.get(symbol)
        if code is None:
            raise ValueError(f"plaintext symbol {symbol} is not on the board")
        out.append(code)
    return "".join(out)


def straddling_checkerboard_decrypt(text: str, key: str) -> str:
    """Decrypt a digit stream with a known straddling checkerboard key.

    Non-digits are ignored so a grouped printing still decrypts. A row
    digit consumes the next digit as its column. Any other digit is one
    header symbol. The read is unambiguous for a board built this way.
    """
    board = parse_checkerboard_key(key)
    digits = [ch for ch in text if ch.isdigit()]
    if not digits:
        raise ValueError("ciphertext has no digits")
    rows = set(board.row_digits)
    out: list[str] = []
    index = 0
    while index < len(digits):
        digit = digits[index]
        if digit in rows:
            if index + 1 >= len(digits):
                raise ValueError("ciphertext ends on a row digit")
            code = digit + digits[index + 1]
            index += 2
        else:
            code = digit
            index += 1
        symbol = board.decode.get(code)
        if symbol is None:
            raise ValueError("ciphertext code is not on the board")
        out.append(symbol)
    return "".join(out)


def solve_straddling_checkerboard(text: str, *, key: str) -> SolveResult:
    """Recover a straddling checkerboard reading when the board key is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    plain = straddling_checkerboard_decrypt(text, key)
    board = parse_checkerboard_key(key)
    return SolveResult(
        method="straddling_checkerboard",
        plaintext=plain,
        key=key,
        score=float(len(plain)),
        details={
            "row_digits": ",".join(board.row_digits),
            "header": board.header,
            "source_url": WIKIPEDIA_CHECKERBOARD_URL,
            "mode": "known_board",
            "scope": _SCOPE,
        },
    )


__all__ = [
    "WIKIPEDIA_CHECKERBOARD_CIPHER",
    "WIKIPEDIA_CHECKERBOARD_KEY",
    "WIKIPEDIA_CHECKERBOARD_PLAIN",
    "WIKIPEDIA_CHECKERBOARD_SOURCE_TEXT",
    "WIKIPEDIA_CHECKERBOARD_URL",
    "parse_checkerboard_key",
    "solve_straddling_checkerboard",
    "straddling_checkerboard_decrypt",
    "straddling_checkerboard_encrypt",
]
