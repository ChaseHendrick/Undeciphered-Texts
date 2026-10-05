"""A delay between the two coordinates, and a progressive shift. Not a reading.

The delay rotates the row digits against the column digits and pairs them
again. The progressive shift adds or subtracts a count that grows by one
each cell. Neither is a repeating key and neither reorders the old cells.
Shuffled coordinates and shuffled cells get the same searches. No letter
string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_swarm import CHALLENGE, _digits
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_NULL = 200
_ROW = "67890"
_COLUMN = "12345"


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


def _pair(row_digits: str, column_digits: str) -> list[int] | None:
    cells = []
    for row_digit, column_digit in zip(row_digits, column_digits):
        if row_digit not in _ROW or column_digit not in _COLUMN:
            return None
        cells.append(_ROW.index(row_digit) * 5 + _COLUMN.index(column_digit))
    return cells


def _best_delay(row_digits: str, column_digits: str, logp: list[float], english: list[int]) -> tuple[float, int]:
    best = float("-inf")
    best_delay = 0
    width = len(row_digits)
    for delay in range(width):
        shifted = row_digits[delay:] + row_digits[:delay]
        cells = _pair(shifted, column_digits)
        if cells is None:
            continue
        score = _quad(cells, logp, english)
        if score > best:
            best = score
            best_delay = delay
    return best, best_delay


def _best_progressive(cells: list[int], logp: list[float], english: list[int]) -> tuple[float, str]:
    best = float("-inf")
    best_rule = ""
    count = len(cells)
    for rule in ("sub", "add"):
        for seed in range(25):
            if rule == "sub":
                plain = [(cell - (seed + index)) % 25 for index, cell in enumerate(cells)]
            else:
                plain = [(cell + (seed + index)) % 25 for index, cell in enumerate(cells)]
            if len(plain) != count:
                raise ValueError("a progressive shift changed the length")
            score = _quad(plain, logp, english)
            if score > best:
                best = score
                best_rule = rule
    return best, best_rule


def _coordinates() -> tuple[str, str]:
    digits = _digits(CHALLENGE)
    if not digits.endswith("000"):
        raise ValueError("the printed challenge is expected to end in the filler 000")
    digits = digits[:-3]
    return digits[0::2], digits[1::2]


@frozen("delay")
def delay_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    row_digits, column_digits = _coordinates()
    delay_score, delay = _best_delay(row_digits, column_digits, logp, english)
    cells = _cells()
    progressive_score, rule = _best_progressive(cells, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    delay_as_high = 0
    for _ in range(_NULL):
        shuffled_row = list(row_digits)
        shuffled_column = list(column_digits)
        drawn.shuffle(shuffled_row)
        drawn.shuffle(shuffled_column)
        score, _delay = _best_delay("".join(shuffled_row), "".join(shuffled_column), logp, english)
        if score >= delay_score:
            delay_as_high += 1
    run = random.Random(_SEED)
    progressive_as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        run.shuffle(shuffled)
        score, _rule = _best_progressive(shuffled, logp, english)
        if score >= progressive_score:
            progressive_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "delays": len(row_digits),
        "best_delay": delay,
        "delay_quadgram": round(delay_score, 4),
        "delay_draws": _NULL,
        "delay_shuffles_as_high": delay_as_high,
        "progressive_rule": rule,
        "progressive_quadgram": round(progressive_score, 4),
        "progressive_draws": _NULL,
        "progressive_shuffles_as_high": progressive_as_high,
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": delay_score >= prose_quad or progressive_score >= prose_quad,
        "scope": "A delay or a progressive shift is not a reading. No letter string is stored.",
    }
