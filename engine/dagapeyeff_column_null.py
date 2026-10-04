"""Drop one column of the printed grid, and drop a repeated symbol. Not a reading.

The fourth column repeats one symbol six times. This asks whether that
column, or any column, is filler. A shuffled grid is allowed to drop its
best column too. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.alphabet import letters_only, to_ints
from engine.dagapeyeff_add import _PROSE, _cells
from engine.dagapeyeff_cache import frozen
from engine.language import ENGLISH_ORDER, get_model

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


def _drop_column(cells: list[int], index: int) -> list[int]:
    return [cell for position, cell in enumerate(cells) if position % _WIDTH != index]


def _best_drop(cells: list[int], logp: list[float], english: list[int]) -> tuple[float, int]:
    best = float("-inf")
    best_index = 0
    for index in range(_WIDTH):
        score = _quad(_drop_column(cells, index), logp, english)
        if score > best:
            best = score
            best_index = index
    return best, best_index


def _drop_mode(cells: list[int], index: int) -> tuple[list[int], int]:
    column = cells[index::_WIDTH]
    symbol = Counter(column).most_common(1)[0][0]
    kept = []
    dropped = 0
    for position, cell in enumerate(cells):
        if position % _WIDTH == index and cell == symbol:
            dropped += 1
            continue
        kept.append(cell)
    return kept, dropped


@frozen("column-null")
def column_null_report() -> dict:
    logp = get_model().logp
    english = [ord(char) - 65 for char in ENGLISH_ORDER]
    cells = _cells()
    if len(cells) != _WIDTH * _WIDTH:
        raise ValueError("the grid is expected to be 14 by 14")
    best, best_index = _best_drop(cells, logp, english)
    fourth = _quad(_drop_column(cells, 3), logp, english)
    mode_kept, mode_dropped = _drop_mode(cells, 3)
    mode_score = _quad(mode_kept, logp, english)
    prose = to_ints(letters_only(_PROSE))
    prose_score = get_model().score(prose) / (len(prose) - 3)
    drawn = random.Random(_SEED)
    best_as_high = 0
    fourth_as_high = 0
    mode_as_high = 0
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        shuffle_best, _index = _best_drop(shuffled, logp, english)
        if shuffle_best >= best:
            best_as_high += 1
        if _quad(_drop_column(shuffled, 3), logp, english) >= fourth:
            fourth_as_high += 1
        kept, _dropped = _drop_mode(shuffled, 3)
        if _quad(kept, logp, english) >= mode_score:
            mode_as_high += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "columns": _WIDTH,
        "kept_after_column": len(cells) - _WIDTH,
        "best_column": best_index,
        "best_quadgram": round(best, 4),
        "fourth_column": 3,
        "fourth_quadgram": round(fourth, 4),
        "mode_dropped": mode_dropped,
        "mode_quadgram": round(mode_score, 4),
        "prose_quadgram": round(prose_score, 4),
        "reaches_prose": best >= prose_score or mode_score >= prose_score,
        "draws": _DRAWS,
        "best_shuffles_as_high": best_as_high,
        "fourth_shuffles_as_high": fourth_as_high,
        "mode_shuffles_as_high": mode_as_high,
        "scope": "Dropping a column is not a reading. No letter string is stored.",
    }
