"""If there is no message: test the cells against a no-message generator, with shown power. Not a reading.

Van Eykelen (MsgTrail XV) found a hand procedure with no plaintext that
reproduces fourteen statistics of the cells: tally 18 pairs with fixed counts,
deal them onto the 14 by 14 grid at random, and move a rare pair that lands
mid-row to the end of its row. Its simplest form is taken here as the null:
the cells' own symbols dealt at random, with the 8 rare cells held in their
places in the last column. Under it the letter counts are fixed, so only the
order of the cells can tell a message from no message.

Thirty order statistics are declared before any score is read: the share of
equal symbols at lags 1 to 14, the mutual information of symbols at lags 1 to
14, the number of different neighbouring pairs and the number of repeated
triples. Each gets a two-sided rank p-value against the null; the family-wise
p-value is the share of null draws whose smallest p-value is as small as the
cells'.

Power: the same test is run on planted held-out English hidden by five message
systems (a keyed square; 14-column transposition, undone and done; a 14 by 14
turning grille; a repeating coordinate shift of period 2 to 14), each against
dealings of its own symbols. A random transposition of the planted text is the
calibration case: it is a no-message dealing, so it should be flagged about 5
percent of the time. The statistics are unchanged by any one-to-one key.

No letter string is stored.
"""

from __future__ import annotations

import random

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _random_key
from engine.dagapeyeff_additive import encrypt as shift_encrypt
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar14c import encrypt as columnar_encrypt
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_grillec import encrypt as grille_encrypt
from engine.dagapeyeff_quick import rare_symbols

_SEED = 20261018
_LETTERS = 196
_LAGS = range(1, 15)
_CELL_NULL = 20_000
_PLANT_NULL = 2_000
_PLANTED = 20
_ALPHA = 0.05
_CHUNK = 1_000
SYSTEMS = ("keyed square", "columnar 14 undone", "columnar 14 done", "turning grille", "repeating shift",
           "random transposition")


def statistic_names() -> list[str]:
    return ([f"equal lag {k}" for k in _LAGS] + [f"information lag {k}" for k in _LAGS]
            + ["different neighbour pairs", "repeated triples"])


def _information(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    rows, n = left.shape
    codes = (left * 25 + right) + (np.arange(rows) * 625)[:, None]
    joint = np.bincount(codes.ravel(), minlength=rows * 625).reshape(rows, 25, 25).astype(np.float64) / n
    a = joint.sum(axis=2, keepdims=True)
    b = joint.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        terms = np.where(joint > 0, joint * np.log(joint / (a * b)), 0.0)
    return terms.sum(axis=(1, 2))


def statistics(batch: np.ndarray) -> np.ndarray:
    """One row of 30 statistics for each row of symbols."""
    out = []
    for start in range(0, len(batch), _CHUNK):
        s = batch[start:start + _CHUNK]
        rows = len(s)
        cols = [(s[:, :-k] == s[:, k:]).mean(axis=1) for k in _LAGS]
        cols += [_information(s[:, :-k], s[:, k:]) for k in _LAGS]
        pairs = s[:, :-1] * 25 + s[:, 1:] + (np.arange(rows) * 625)[:, None]
        cols.append((np.bincount(pairs.ravel(), minlength=rows * 625).reshape(rows, 625) > 0).sum(axis=1))
        triples = s[:, :-2] * 625 + s[:, 1:-1] * 25 + s[:, 2:] + (np.arange(rows) * 15625)[:, None]
        cols.append((np.bincount(triples.ravel(), minlength=rows * 15625).reshape(rows, 15625) > 1).sum(axis=1))
        out.append(np.stack(cols, axis=1).astype(np.float64))
    return np.concatenate(out)


def _p_values(null: np.ndarray, values: np.ndarray) -> np.ndarray:
    """Two-sided rank p-values of each row of values against the null, statistic by statistic."""
    count = len(null)
    out = np.empty_like(values)
    for j in range(null.shape[1]):
        ordered = np.sort(null[:, j])
        low = np.searchsorted(ordered, values[:, j], side="right")
        high = count - np.searchsorted(ordered, values[:, j], side="left")
        out[:, j] = np.minimum(1.0, 2 * (np.minimum(low, high) + 1) / (count + 1))
    return out


def dealings(symbols: list[int], fixed: set[int], draws: int, rng: np.random.Generator) -> np.ndarray:
    """The symbols dealt at random, with the places in fixed kept."""
    base = np.asarray(symbols)
    free = np.asarray([i for i in range(len(symbols)) if i not in fixed])
    out = np.tile(base, (draws, 1))
    keys = rng.random((draws, len(free)))
    out[:, free] = base[free][np.argsort(keys, axis=1)]
    return out


def family_test(symbols: list[int], fixed: set[int], draws: int, rng: np.random.Generator) -> dict:
    null = statistics(dealings(symbols, fixed, draws, rng))
    observed = statistics(np.asarray([symbols]))
    p = _p_values(null, observed)[0]
    null_min = _p_values(null, null).min(axis=1)
    smallest = int(np.argmin(p))
    return {
        "family_p": round(float((np.sum(null_min <= p.min()) + 1) / (draws + 1)), 4),
        "smallest_p": round(float(p.min()), 5),
        "smallest_statistic": statistic_names()[smallest],
        "p_values": [round(float(x), 4) for x in p],
    }


def _plant(system: str, text: str, rng: random.Random) -> list[int]:
    symbols = [PLAIN.index(ch) for ch in text]
    if system == "keyed square":
        return symbols
    if system.startswith("columnar"):
        order = rng.sample(range(14), 14)
        return columnar_encrypt(symbols, order, system.split()[-1])[0]
    if system == "turning grille":
        return grille_encrypt(symbols, [rng.randrange(4) for _ in range(49)])[0]
    if system == "repeating shift":
        period = rng.choice((2, 3, 4, 5, 7, 14))
        return shift_encrypt(text, rng.sample(range(25), 25), _random_key(period, rng.choice(("both", "column")), rng))
    return rng.sample(symbols, len(symbols))


@frozen("dagapeyeff-nomessage")
def nomessage_report() -> dict:
    rng = random.Random(_SEED)
    gen = np.random.default_rng(_SEED)
    cells = _cells()
    rare = rare_symbols(cells)
    fixed = {i for i, cell in enumerate(cells) if cell in rare}
    cell_test = family_test(cells, fixed, _CELL_NULL, gen)
    power = {}
    for system in SYSTEMS:
        flagged = []
        for k in range(_PLANTED):
            prose = _held(_HELD[k % len(_HELD)])
            start = rng.randrange(len(prose) - _LETTERS)
            result = family_test(_plant(system, prose[start:start + _LETTERS], rng), set(), _PLANT_NULL, gen)
            flagged.append(result["family_p"])
        power[system] = {"planted": _PLANTED, "flagged": sum(p <= _ALPHA for p in flagged),
                         "median_family_p": round(float(np.median(flagged)), 4)}
    return {
        "solved": False,
        "claimed_plaintext": None,
        "statistics": statistic_names(),
        "fixed_places": sorted(fixed),
        "cells": cell_test,
        "power": power,
        "alpha": _ALPHA,
    }
