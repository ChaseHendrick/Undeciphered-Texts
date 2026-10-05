"""Routes of the digits, then a new pairing. Not a reading.

These are not orders of the 196 cells. The row digits are rearranged,
or the column digits, and the cells are paired again. A route that leaves
the book square is discarded. Shuffled row and column digits get the same
routes. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_swarm import CHALLENGE, _digits
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_NULL = 40
_ROW = "67890"
_COLUMN = "12345"


def _stream() -> str:
    digits = _digits(CHALLENGE)
    if not digits.endswith("000"):
        raise ValueError("the printed challenge is expected to end in the filler 000")
    return digits[:-3]


def _rail(text: str, period: int) -> str:
    rows = [[] for _ in range(period)]
    for index, char in enumerate(text):
        rows[index % period].append(char)
    return "".join("".join(row) for row in rows)


def _cells(row_digits: str, column_digits: str) -> list[int] | None:
    if len(row_digits) != len(column_digits):
        return None
    cells = []
    for row_digit, column_digit in zip(row_digits, column_digits):
        if row_digit not in _ROW or column_digit not in _COLUMN:
            return None
        cells.append(_ROW.index(row_digit) * 5 + _COLUMN.index(column_digit))
    return cells


def _quad(plain_cells: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in plain_cells:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in plain_cells]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _routes(row_digits: str, column_digits: str) -> list[tuple[str, str, str]]:
    found = [("identity", row_digits, column_digits), ("reverse-row", row_digits[::-1], column_digits)]
    found.append(("reverse-column", row_digits, column_digits[::-1]))
    found.append(("reverse-both", row_digits[::-1], column_digits[::-1]))
    for period in range(2, 16):
        found.append((f"rail-row-{period}", _rail(row_digits, period), column_digits))
        found.append((f"rail-column-{period}", row_digits, _rail(column_digits, period)))
        found.append((f"rail-both-{period}", _rail(row_digits, period), _rail(column_digits, period)))
    return found


def _best(row_digits: str, column_digits: str, logp: list[float], english: list[int]) -> tuple[float, str, int]:
    best = float("-inf")
    best_name = ""
    kept = 0
    for name, row, column in _routes(row_digits, column_digits):
        cells = _cells(row, column)
        if cells is None:
            continue
        kept += 1
        score = _quad(cells, logp, english)
        if score > best:
            best = score
            best_name = name
    return best, best_name, kept


@frozen("digit-routes")
def digit_route_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    digits = _stream()
    row_digits, column_digits = digits[0::2], digits[1::2]
    menu = len(_routes(row_digits, column_digits))
    best, name, kept = _best(row_digits, column_digits, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled_row = list(row_digits)
        shuffled_column = list(column_digits)
        drawn.shuffle(shuffled_row)
        drawn.shuffle(shuffled_column)
        score, _name, _kept = _best("".join(shuffled_row), "".join(shuffled_column), logp, english)
        if score >= best:
            as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "routes": menu,
        "routes_on_square": kept,
        "best_route": name,
        "best_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "scope": "A digit route is not a reading. No letter string is stored.",
    }
