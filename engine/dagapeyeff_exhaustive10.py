"""Every column order at width 10, any language. Not a reading.

The same three families and the same score as engine.dagapeyeff_exhaustive,
at width 10: 3,628,800 orders a family. More orders lift the best score of
pure noise, so planted English and German show how much power is left.
No letter string is stored.
"""

from __future__ import annotations

import random

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_double import _german
from engine.dagapeyeff_exhaustive import FAMILIES, _excess, _plant, _positions, information
from engine.neural_grade import letters_az, load_training_prose

_WIDTH = 10
_SEED = 20261020
_NULLS = 2


@frozen("dagapeyeff-exhaustive10")
def exhaustive10_report() -> dict:
    rng = random.Random(_SEED)
    english = letters_az(load_training_prose()).replace("J", "I")
    german = _german()
    cells = np.asarray(_cells(), dtype=np.int64)
    regrouped = np.asarray(_regrouped_cells(), dtype=np.int64)
    rows = []
    for family in FAMILIES:
        planted = []
        for language, prose, start in (("english", english, 4100), ("german", german, 160)):
            cipher, order = _plant(prose, start, family, _WIDTH, rng)
            true_positions = _positions(family, _WIDTH, np.asarray([order], dtype=np.int64))
            row = _excess(cipher, family, _WIDTH, rng, draws=1)
            row["language"] = language
            row["true_mi"] = round(float(information(cipher[true_positions])[0]), 4)
            planted.append(row)
        rows.append({
            "width": _WIDTH,
            "family": family,
            "planted": planted,
            "cells": _excess(cells, family, _WIDTH, rng, draws=_NULLS),
            "regrouped": _excess(regrouped, family, _WIDTH, rng, draws=_NULLS),
        })
    return {
        "solved": False,
        "claimed_plaintext": None,
        "width": _WIDTH,
        "orders_per_family": 3628800,
        "rows": rows,
        "cases_cells_below_planted": sum(
            row["cells"]["excess"] < min(plant["excess"] for plant in row["planted"])
            and row["regrouped"]["excess"] < min(plant["excess"] for plant in row["planted"])
            for row in rows
        ),
        "scope": (
            "Every order at width 10 in three families, scored by a measure no letter key can change, against "
            "shuffles of the same symbols. Not a reading. No letter string is stored."
        ),
    }
