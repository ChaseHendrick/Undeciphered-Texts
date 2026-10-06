"""A letter key with some symbols as nulls, on the cells. Not a reading.

The 1939 book allows dummy letters. Fixed schedules of dummies were already
deleted by position (engine.dagapeyeff_nulls). This short attack instead lets
up to four of the cells' symbols be nulls wherever they fall, and anneals the
letter key and the null set together with the compiled kernel in
engine/dagapeyeff_subc.c, under the default model with J folded into I. At
least 140 letters must remain.

Dropping symbols that do not fit always raises the score per letter, so the
cells are compared only with shuffled cells given the same freedom. Planted
held-out English with two or three null symbols scattered through it shows the
power. The best letters on the cells are stored as a candidate so a reader can
look at them. A stored candidate is not a reading.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_subc import anneal

MAX_NULLS = 4
MIN_LETTERS = 140
_LETTERS = 196
_SEED = 20261008
_RESTARTS = 8
_STEPS = 300_000
_SHUFFLES = 20
_RECOVERED = 0.95
_PLANTS = ((2, 16), (3, 30))


def plant(text: str, key: list[int], null_symbols: list[int], count: int,
          rng: random.Random) -> tuple[list[int], list[str | None]]:
    """Encipher text and scatter `count` nulls; return cells and the truth per cell."""
    cells = [key[PLAIN.index(ch)] for ch in text]
    truth: list[str | None] = list(text)
    for _ in range(count):
        at = rng.randrange(len(cells) + 1)
        cells.insert(at, rng.choice(null_symbols))
        truth.insert(at, None)
    return cells, truth


def read(cells: list[int], found: dict) -> list[str | None]:
    """What the found key says each cell is, None for a null."""
    nulls = set(found["nulls"])
    return [None if s in nulls else found["key"][s] for s in cells]


def _search(cells: list[int], seed: int) -> dict:
    return anneal(cells, seed, max_nulls=MAX_NULLS, min_letters=MIN_LETTERS,
                  restarts=_RESTARTS, steps=_STEPS)


@frozen("dagapeyeff-nullsub")
def nullsub_report() -> dict:
    rng = random.Random(_SEED)
    planted = []
    for null_count, inserted in _PLANTS:
        for name in _HELD:
            prose = _held(name)
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS - inserted]
            key = list(range(25))
            rng.shuffle(key)
            spare = [key[PLAIN.index(ch)] for ch in PLAIN if ch not in set(text)]
            rng.shuffle(spare)
            null_symbols = spare[:null_count]
            cells, truth = plant(text, key, null_symbols, inserted, rng)
            found = _search(cells, rng.randrange(1 << 40))
            share = sum(a == b for a, b in zip(read(cells, found), truth)) / len(cells)
            planted.append({
                "null_symbols": len(null_symbols),
                "nulls_inserted": inserted,
                "source": name,
                "found_per_letter": round(found["per_letter"], 4),
                "nulls_found": sorted(found["nulls"]) == sorted(null_symbols),
                "cells_right": round(share, 4),
            })
    searched = {}
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        best = _search(cells, rng.randrange(1 << 40))
        scores = []
        for _ in range(_SHUFFLES):
            mixed = list(cells)
            rng.shuffle(mixed)
            scores.append(round(_search(mixed, rng.randrange(1 << 40))["per_letter"], 4))
        score = round(best["per_letter"], 4)
        searched[label] = {
            "per_letter": score,
            "null_symbols": best["nulls"],
            "cells_dropped": sum(s in set(best["nulls"]) for s in cells),
            "shuffles": sorted(scores, reverse=True),
            "shuffles_as_high": sum(s >= score for s in scores),
            "candidate_letters": best["letters"],
        }
    recovered = [row for row in planted if row["cells_right"] >= _RECOVERED]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "candidates_are_readings": False,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "shuffles": _SHUFFLES,
                   "max_nulls": MAX_NULLS, "min_letters": MIN_LETTERS},
        "planted": planted,
        "planted_recovered": len(recovered),
        "planted_lowest_found": min(row["found_per_letter"] for row in recovered),
        "searched": searched,
    }
