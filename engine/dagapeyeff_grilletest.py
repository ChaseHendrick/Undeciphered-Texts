"""Can any order statistic tell a turning-grille message from a no-message dealing? Not a reading.

engine.dagapeyeff_nomessage flags a planted grille message only 3 times in 20.
A grille is not random: about a quarter of row neighbours are true plaintext
pairs, and the cells fall into 49 rotation orbits. This probe uses the
statistic built for it, the largest successive-symbol information over all
grilles (engine.dagapeyeff_grille.climb_information), which overfits as a
search but could still separate as a test. Each planted grille message is
compared with random dealings of its own symbols, and the cells with dealings
of theirs, the rare column held.

No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_grille import climb_information
from engine.dagapeyeff_grillec import encrypt as grille_encrypt
from engine.dagapeyeff_quick import rare_symbols

_SEED = 20261019
_LETTERS = 196
_PLANTED = 12
_DEALINGS = 10
_CELL_DEALINGS = 40
_RESTARTS = 4
_STEPS = 1500


def _stat(cells: list[int], rng: random.Random) -> float:
    return climb_information(cells, rng, _RESTARTS, _STEPS)[0]


def _dealing(cells: list[int], fixed: set[int], rng: random.Random) -> list[int]:
    free = [i for i in range(len(cells)) if i not in fixed]
    values = [cells[i] for i in free]
    rng.shuffle(values)
    out = list(cells)
    for i, value in zip(free, values):
        out[i] = value
    return out


@frozen("dagapeyeff-grilletest")
def grilletest_report() -> dict:
    rng = random.Random(_SEED)
    planted = []
    for k in range(_PLANTED):
        prose = _held(_HELD[k % len(_HELD)])
        start = rng.randrange(len(prose) - _LETTERS)
        symbols = [PLAIN.index(ch) for ch in prose[start:start + _LETTERS]]
        cells = grille_encrypt(symbols, [rng.randrange(4) for _ in range(49)])[0]
        observed = _stat(cells, rng)
        dealt = [_stat(_dealing(cells, set(), rng), rng) for _ in range(_DEALINGS)]
        planted.append({"statistic": round(observed, 4), "dealings_as_high": sum(x >= observed for x in dealt)})
    cells = _cells()
    rare = rare_symbols(cells)
    fixed = {i for i, cell in enumerate(cells) if cell in rare}
    observed = _stat(cells, rng)
    dealt = [_stat(_dealing(cells, fixed, rng), rng) for _ in range(_CELL_DEALINGS)]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "dealings": _DEALINGS},
        "planted": planted,
        "planted_above_all_dealings": sum(row["dealings_as_high"] == 0 for row in planted),
        "cells": {"statistic": round(observed, 4), "dealings": _CELL_DEALINGS,
                  "dealings_as_high": sum(x >= observed for x in dealt)},
    }
