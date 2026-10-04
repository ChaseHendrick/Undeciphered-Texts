"""Three angles that are not a key and not an order of the cells. Not a reading.

The first reads each step from one cell to the next as the symbol. The
second asks whether the seven unused cells of the square empty a line.
The third asks whether consecutive cells could be a Playfair pair, which
forbids a repeated cell. A shuffle, or every way to place seven holes, is
the control. No letter string is stored.
"""

from __future__ import annotations

import random
from functools import lru_cache
from itertools import combinations

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.language import ENGLISH_ORDER, get_model

_SEED = 20261004
_NULL = 40
_DIGRAPHS = 400


def _steps(seq: list[int]) -> list[int]:
    out = []
    for left, right in zip(seq, seq[1:]):
        row = (right // 5 - left // 5) % 5
        column = (right % 5 - left % 5) % 5
        out.append(row * 5 + column)
    return out


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


def _holes(cells: list[int]) -> tuple[int, int]:
    used = set(cells)
    missing = [cell for cell in range(25) if cell not in used]
    rows = [0] * 5
    columns = [0] * 5
    for cell in missing:
        rows[cell // 5] += 1
        columns[cell % 5] += 1
    return max(rows), len(missing)


def _line_null(holes: int, crowded: int) -> tuple[int, int]:
    as_crowded = 0
    total = 0
    for choice in combinations(range(25), holes):
        rows = [0] * 5
        for cell in choice:
            rows[cell // 5] += 1
        total += 1
        if max(rows) >= crowded:
            as_crowded += 1
    return as_crowded, total


def _identical(seq: list[int]) -> int:
    return sum(left == right for left, right in zip(seq[0::2], seq[1::2]))


@lru_cache(maxsize=1)
def angle_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    stepped = _steps(cells)
    best = _quad(stepped, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_quad = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    as_high = 0
    for _ in range(_NULL):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        if _quad(_steps(shuffled), logp, english) >= best:
            as_high += 1
    crowded, holes = _holes(cells)
    line_as_crowded, line_total = _line_null(holes, crowded)
    identical = _identical(cells)
    digraphs = len(cells) // 2
    pair_draw = random.Random(_SEED)
    as_few = 0
    for _ in range(_DIGRAPHS):
        shuffled = cells[:]
        pair_draw.shuffle(shuffled)
        if _identical(shuffled) <= identical:
            as_few += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "steps": len(stepped),
        "step_quadgram": round(best, 4),
        "prose_quadgram": round(prose_quad, 4),
        "reaches_prose": best >= prose_quad,
        "null_texts": _NULL,
        "shuffles_as_high": as_high,
        "unused_cells": holes,
        "most_in_one_row": crowded,
        "placements": line_total,
        "placements_as_crowded": line_as_crowded,
        "digraphs": digraphs,
        "identical_digraphs": identical,
        "digraph_draws": _DIGRAPHS,
        "shuffles_as_few_identical": as_few,
        "scope": "A step, a row of holes, or a Playfair ban is not a reading. No letter string is stored.",
    }
