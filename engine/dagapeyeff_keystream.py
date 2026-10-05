"""Use one printed column as the key for the other cells in its row.

The fourth column repeats, and dropping it made the score worse, so it is
not filler. This asks whether it, or any column, is a key. A shuffled grid
may pick its own best column. No letter string is stored.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.language import ENGLISH_ORDER, get_legacy_model

_SEED = 20261004
_DRAWS = 80
_WIDTH = 14


def _quad(seq: list[int], logp: list[float], english: list[int]) -> float:
    counts = [0] * 25
    for cell in seq:
        counts[cell] += 1
    order = sorted(range(25), key=lambda cell: (-counts[cell], cell))
    mapping = [0] * 25
    rank = 0
    for cell in order:
        if counts[cell] == 0:
            continue
        mapping[cell] = english[rank]
        rank += 1
    plain = [mapping[cell] for cell in seq]
    left, mid, right = plain[0], plain[1], plain[2]
    total = 0.0
    for nxt in plain[3:]:
        total += logp[((left * 26 + mid) * 26 + right) * 26 + nxt]
        left, mid, right = mid, right, nxt
    return total / (len(plain) - 3)


def _keyed(cells: list[int], column: int, sign: int) -> list[int]:
    plain = []
    for row in range(_WIDTH):
        start = row * _WIDTH
        key = cells[start + column]
        for offset in range(_WIDTH):
            if offset == column:
                continue
            plain.append((cells[start + offset] + sign * key) % 25)
    return plain


def _best(cells: list[int], logp: list[float], english: list[int]) -> tuple[float, int, str]:
    best = float("-inf")
    best_column = 0
    best_rule = "sub"
    for column in range(_WIDTH):
        for rule, sign in (("sub", -1), ("add", 1)):
            score = _quad(_keyed(cells, column, sign), logp, english)
            if score > best:
                best = score
                best_column = column
                best_rule = rule
    return best, best_column, best_rule


@frozen("keystream")
def keystream_report() -> dict:
    logp = get_legacy_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    if len(cells) != _WIDTH * _WIDTH:
        raise ValueError("the grid is expected to be 14 by 14")
    best, column, rule = _best(cells, logp, english)
    fourth = max(
        _quad(_keyed(cells, 3, -1), logp, english),
        _quad(_keyed(cells, 3, 1), logp, english),
    )
    prose = to_ints(letters_only(_PROSE))
    prose_score = get_legacy_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    best_as_high = 0
    fourth_as_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        shuffle_best, _column, _rule = _best(shuffled, logp, english)
        if shuffle_best >= best:
            best_as_high += 1
        shuffle_fourth = max(
            _quad(_keyed(shuffled, 3, -1), logp, english),
            _quad(_keyed(shuffled, 3, 1), logp, english),
        )
        if shuffle_fourth >= fourth:
            fourth_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "columns": _WIDTH,
        "kept": _WIDTH * (_WIDTH - 1),
        "best_column": column,
        "best_rule": rule,
        "best_quadgram": round(best, 4),
        "fourth_column": 3,
        "fourth_quadgram": round(fourth, 4),
        "prose_quadgram": round(prose_score, 4),
        "reaches_prose": best >= prose_score or fourth >= prose_score,
        "draws": _DRAWS,
        "best_shuffles_as_high": best_as_high,
        "fourth_shuffles_as_high": fourth_as_high,
        "scope": "A column used as a key is not a reading. No letter string is stored.",
    }
