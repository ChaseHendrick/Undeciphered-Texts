"""A wider control for width 14. Not a reading.

In the columnar search, the cells at width 14 scored -3.4168 a letter and 0
of 4 shuffles reached it, while planted English scores about -2 and the
search recovered 0 of 2 planted texts at that width. Reading width 14 takes
the printed square down its columns, so the column that holds every rare
symbol becomes one contiguous run of 14 cells.

Two controls at the same search budget, with the cells searched again under
a new seed. Twenty plain shuffles. Twenty shuffles that keep the fourteen
cells of that column in place and shuffle only the other 182. No letter
string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import anneal

_SEED = 20261015
_DRAWS = 20
_WIDTH = 14
_LETTERS = 196


def _per_letter(score: float) -> float:
    return round(score / (_LETTERS - 3), 4)


@frozen("dagapeyeff-columnar14")
def columnar14_report() -> dict:
    cells = _cells()
    drawn = random.Random(_SEED)
    cell_score = _per_letter(anneal(cells, _WIDTH, random.Random(drawn.randrange(1 << 30)))[0])
    column = [index for index in range(_LETTERS) if index % _WIDTH == _WIDTH - 1]
    rest = [index for index in range(_LETTERS) if index % _WIDTH != _WIDTH - 1]
    plain, kept = [], []
    for _ in range(_DRAWS):
        shuffled = cells[:]
        drawn.shuffle(shuffled)
        plain.append(_per_letter(anneal(shuffled, _WIDTH, random.Random(drawn.randrange(1 << 30)))[0]))
        values = [cells[i] for i in rest]
        drawn.shuffle(values)
        held = cells[:]
        for index, value in zip(rest, values):
            held[index] = value
        assert [held[i] for i in column] == [cells[i] for i in column]
        kept.append(_per_letter(anneal(held, _WIDTH, random.Random(drawn.randrange(1 << 30)))[0]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "width": _WIDTH,
        "cells_per_letter": cell_score,
        "draws": _DRAWS,
        "plain_shuffles_as_high": sum(score >= cell_score for score in plain),
        "plain_shuffle_best": max(plain),
        "kept_column_shuffles_as_high": sum(score >= cell_score for score in kept),
        "kept_column_best": max(kept),
        "scope": (
            "Under a new seed the cells score lower than the first run, and most shuffles of either "
            "kind reach them. The earlier 0 of 4 was a small draw. Not a reading. No letter string is stored."
        ),
    }
