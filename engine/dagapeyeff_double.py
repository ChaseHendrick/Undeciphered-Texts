"""Every double columnar transposition up to width 6, any language. Not a reading.

Double transposition is the book's own method, copied from Kerckhoffs, and
Pelling (2017) suspected the challenge used it. Two columnar passes with
different keys move single cells, not whole columns. This pass tries every
pair of orders at widths 2 to 6, for both passes undone and for both passes
done (the book's reversed direction), a short last row allowed.

The score is successive-symbol information, which no letter key can change,
so the plaintext language does not matter. Each text is compared with the
best pair of orders on shuffles of its own symbols. Planted English and
German, with a random letter key and random orders, show what a real text
does. No letter string is stored.
"""

from __future__ import annotations

import itertools
import random
from pathlib import Path

import numpy as np

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_exhaustive import _positions, information
from engine.neural_grade import letters_az, load_training_prose

WIDTHS = tuple(range(2, 7))
FAMILIES = ("columnar-undone", "columnar-done")
_N = 196
_SEED = 20261019
_NULLS = 2
_GERMAN = Path(__file__).resolve().parent / "data" / "german_excerpt.txt"


def _all_positions(family: str, width: int) -> np.ndarray:
    orders = np.asarray(list(itertools.permutations(range(width))), dtype=np.int64)
    return _positions(family, width, orders)


def best_pair(cells: np.ndarray, family: str, first: int, second: int) -> float:
    """Best score over every order of the first pass and every order of the second."""
    outer = _all_positions(family, first)
    inner = _all_positions(family, second)
    best = -1.0
    for row in outer:
        # The first pass reads cells[row]; the second reads that result at inner.
        scores = information(cells[row][inner])
        best = max(best, float(scores.max()))
    return best


def _german() -> str:
    raw = _GERMAN.read_text(encoding="utf-8").upper()
    for umlaut, spelled in (("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE"), ("ẞ", "SS"), ("ß", "SS")):
        raw = raw.replace(umlaut, spelled)
    return "".join(ch for ch in letters_only(raw) if "A" <= ch <= "Z").replace("J", "I")


def _plant(prose: str, start: int, family: str, first: int, second: int, rng: random.Random) -> np.ndarray:
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    plain = np.asarray([alphabet.index(ch) for ch in prose[start:start + _N]], dtype=np.int64)
    key = list(range(25))
    rng.shuffle(key)
    plain = np.asarray([key[x] for x in plain], dtype=np.int64)
    order_one = list(range(first))
    rng.shuffle(order_one)
    order_two = list(range(second))
    rng.shuffle(order_two)
    outer = _positions(family, first, np.asarray([order_one]))[0]
    inner = _positions(family, second, np.asarray([order_two]))[0]
    combined = outer[inner]
    cipher = np.empty(_N, dtype=np.int64)
    cipher[combined] = plain
    assert np.array_equal(cipher[outer][inner], plain)
    return cipher


def _excess(cells: np.ndarray, family: str, first: int, second: int, rng: random.Random, draws: int) -> dict:
    best = best_pair(cells, family, first, second)
    shuffled = []
    for _ in range(draws):
        sample = cells.copy()
        rng.shuffle(sample)
        shuffled.append(round(best_pair(sample, family, first, second), 4))
    return {"best_mi": round(best, 4), "shuffled_best_mi": shuffled, "excess": round(best - max(shuffled), 4)}


@frozen("dagapeyeff-double")
def double_report() -> dict:
    rng = random.Random(_SEED)
    english = letters_az(load_training_prose()).replace("J", "I")
    german = _german()
    cells = np.asarray(_cells(), dtype=np.int64)
    rows = []
    for family in FAMILIES:
        for first in WIDTHS:
            for second in WIDTHS:
                planted = []
                for language, prose, start in (("english", english, 3000 + 31 * first + 7 * second),
                                               ("german", german, 40 + 9 * first + 5 * second)):
                    cipher = _plant(prose, start, family, first, second, rng)
                    row = _excess(cipher, family, first, second, rng, draws=1)
                    row["language"] = language
                    planted.append(row)
                rows.append({
                    "family": family,
                    "first": first,
                    "second": second,
                    "planted": planted,
                    "cells": _excess(cells, family, first, second, rng, draws=_NULLS),
                })
    below = sum(
        row["cells"]["excess"] < min(plant["excess"] for plant in row["planted"]) for row in rows
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "widths": list(WIDTHS),
        "families": list(FAMILIES),
        "rows": rows,
        "cases": len(rows),
        "cases_cells_below_planted": below,
        "planted_smallest_excess": min(plant["excess"] for row in rows for plant in row["planted"]),
        "cells_largest_excess": max(row["cells"]["excess"] for row in rows),
        "scope": (
            "Every pair of column orders at widths 2 to 6, both passes undone or both done, scored by a measure "
            "no letter key can change. Not a reading. No letter string is stored."
        ),
    }
