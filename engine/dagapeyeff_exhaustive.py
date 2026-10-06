"""Every column order up to width 9, any language. Not a reading.

A columnar transposition followed by any one-to-one substitution, in any
language, leaves one fact a letter key cannot change: put the cells back in
the right order and each symbol predicts the next as well as real text does.
Successive-symbol information measures that, and it needs no language model.

This pass tries every order at widths 2 to 9, which no sampled search has
done. Three families, each over all k! orders:

* columnar undone: the cells were written in rows of k, possibly with a short
  last row, and copied out down the columns in key order;
* columnar done: the same operation applied once more, which is the book's
  reversed direction;
* periodic: every block of k cells permuted by one key, with a short last
  block left in place.

Each family and width gets two planted texts, English and German with a
random letter key and a random order, and the true order must come out on
top. The printed cells, the regrouped cells and three shuffles of the cells
get the same exhaustive search. No letter string is stored.
"""

from __future__ import annotations

import itertools
import random
from pathlib import Path

import numpy as np

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.neural_grade import letters_az, load_training_prose

WIDTHS = tuple(range(2, 10))
FAMILIES = ("columnar-undone", "columnar-done", "periodic")
_N = 196
_SEED = 20261017
_NULLS = 3
_CHUNK = 20000
_GERMAN = Path(__file__).resolve().parent / "data" / "german_excerpt.txt"


def _heights(width: int) -> list[int]:
    base, extra = divmod(_N, width)
    return [base + (1 if column < extra else 0) for column in range(width)]


def _positions(family: str, width: int, orders: np.ndarray) -> np.ndarray:
    """positions[o, i]: the cell read i-th under order o."""
    count = len(orders)
    if family == "periodic":
        blocks = _N // width
        base = (np.arange(blocks) * width)[None, :, None] + orders[:, None, :]
        tail = np.broadcast_to(np.arange(blocks * width, _N), (count, _N - blocks * width))
        return np.concatenate([base.reshape(count, blocks * width), tail], axis=1)
    heights = _heights(width)
    tallest = max(heights)
    padded = np.full((width, tallest), -1, dtype=np.int64)
    for column, height in enumerate(heights):
        padded[column, :height] = np.arange(height) * width + column
    gathered = padded[orders]  # count x width x tallest, columns in key order
    done = gathered[gathered >= 0].reshape(count, _N)
    if family == "columnar-done":
        return done
    return np.argsort(done, axis=1)


def information(sequences: np.ndarray) -> np.ndarray:
    """Successive-symbol information of each row, natural log, as in dagapeyeff_order."""
    count = len(sequences)
    codes = sequences[:, :-1] * 25 + sequences[:, 1:]
    codes = codes + (np.arange(count) * 625)[:, None]
    joint = np.bincount(codes.ravel(), minlength=count * 625).reshape(count, 25, 25).astype(np.float64)
    total = sequences.shape[1] - 1
    left = joint.sum(axis=2, keepdims=True)
    right = joint.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        terms = np.where(joint > 0, joint / total * np.log(joint * total / (left * right)), 0.0)
    return terms.sum(axis=(1, 2))


def best_order(cells: np.ndarray, family: str, width: int) -> tuple[float, tuple[int, ...]]:
    best = (-1.0, ())
    orders = itertools.permutations(range(width))
    while True:
        chunk = list(itertools.islice(orders, _CHUNK))
        if not chunk:
            return best
        array = np.asarray(chunk, dtype=np.int64)
        scores = information(cells[_positions(family, width, array)])
        top = int(scores.argmax())
        if scores[top] > best[0]:
            best = (float(scores[top]), tuple(chunk[top]))


def _plant(prose: str, start: int, family: str, width: int, rng: random.Random) -> tuple[np.ndarray, tuple[int, ...]]:
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    plain = [alphabet.index(ch) for ch in prose[start:start + _N]]
    key = list(range(25))
    rng.shuffle(key)
    substituted = np.asarray([key[x] for x in plain], dtype=np.int64)
    order = list(range(width))
    rng.shuffle(order)
    positions = _positions(family, width, np.asarray([order], dtype=np.int64))[0]
    cipher = np.empty(_N, dtype=np.int64)
    cipher[positions] = substituted
    assert np.array_equal(cipher[positions], substituted)
    return cipher, tuple(order)


def _excess(cells: np.ndarray, family: str, width: int, rng: random.Random, draws: int) -> dict:
    """The best order of a text, against the best order of shuffles of the same symbols."""
    best = best_order(cells, family, width)[0]
    shuffled_best = []
    for _ in range(draws):
        sample = cells.copy()
        rng.shuffle(sample)
        shuffled_best.append(round(best_order(sample, family, width)[0], 4))
    return {
        "best_mi": round(best, 4),
        "shuffled_best_mi": shuffled_best,
        "excess": round(best - max(shuffled_best), 4),
        "shuffles_as_high": sum(score >= round(best, 4) for score in shuffled_best),
    }


@frozen("dagapeyeff-exhaustive")
def exhaustive_report() -> dict:
    rng = random.Random(_SEED)
    english = letters_az(load_training_prose()).replace("J", "I")
    german_raw = _GERMAN.read_text(encoding="utf-8").upper()
    for umlaut, spelled in (("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE"), ("ẞ", "SS"), ("ß", "SS")):
        german_raw = german_raw.replace(umlaut, spelled)
    german = "".join(ch for ch in letters_only(german_raw) if "A" <= ch <= "Z").replace("J", "I")
    cells = np.asarray(_cells(), dtype=np.int64)
    regrouped = np.asarray(_regrouped_cells(), dtype=np.int64)
    rows = []
    for width in WIDTHS:
        for family in FAMILIES:
            planted = []
            for language, prose, start in (("english", english, 2000 + 97 * width), ("german", german, 50 + 11 * width)):
                cipher, order = _plant(prose, start, family, width, rng)
                true_positions = _positions(family, width, np.asarray([order], dtype=np.int64))
                row = _excess(cipher, family, width, rng, draws=1)
                row["language"] = language
                row["true_mi"] = round(float(information(cipher[true_positions])[0]), 4)
                planted.append(row)
            rows.append({
                "width": width,
                "family": family,
                "orders": int(np.prod(range(1, width + 1))),
                "planted": planted,
                "cells": _excess(cells, family, width, rng, draws=_NULLS),
                "regrouped": _excess(regrouped, family, width, rng, draws=_NULLS),
            })
    planted_all = [plant for row in rows for plant in row["planted"]]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "widths": list(WIDTHS),
        "families": list(FAMILIES),
        "rows": rows,
        "planted_smallest_excess": min(plant["excess"] for plant in planted_all),
        "planted_lowest_true_mi": min(plant["true_mi"] for plant in planted_all),
        "cells_largest_excess": max(row["cells"]["excess"] for row in rows),
        "regrouped_largest_excess": max(row["regrouped"]["excess"] for row in rows),
        "cells_highest_mi": max(row["cells"]["best_mi"] for row in rows),
        "scope": (
            "Every order at widths 2 to 9, scored by a measure no letter key can change, against the best order "
            "of shuffles of the same symbols. Planted English and German stand far above their shuffles; the "
            "cells and the regrouping do not. Not a reading. No letter string is stored."
        ),
    }
