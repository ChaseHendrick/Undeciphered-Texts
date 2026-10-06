"""Catalan and Romanian, the next closest languages by letter counts, under a keyed square. Not a reading.

After Latin, the language screen (engine.dagapeyeff_screen) puts Catalan (5
errors at its closest window) and Romanian (7) nearest the cells' letter
counts. For each, a quadgram model is fit on the first 90 percent of its
Universal Dependencies treebank, planted text from the held-out tail (with 0
and 8 digit slips) shows the search's power, and the cells and the regrouping
are solved as a keyed square and under the book's dummy rule, every variant
also run on 8 shuffles of all the cells, best against best. This is the
procedure of engine.dagapeyeff_latin with a different language.

Texts are fetched, not stored. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_errors import corrupt
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_latin import variants
from engine.dagapeyeff_screen import text_of
from engine.language import DiscountedLanguageModel

LANGUAGES = ("Catalan-AnCora", "Romanian-RRT")
_SEED = 20261016
_LETTERS = 196
_TRAIN_SHARE = 0.9
_PLANTED = 3
_SHUFFLES = 8
_RESTARTS = 2
_STEPS = 400_000
_TEMPERATURE = 8.0
_RECOVERED = 0.9


@lru_cache(maxsize=None)
def _split(name: str) -> tuple[str, str]:
    text = text_of(name)
    cut = int(len(text) * _TRAIN_SHARE)
    return text[:cut], text[cut:]


@lru_cache(maxsize=None)
def _tables(name: str):
    model = DiscountedLanguageModel(_split(name)[0])
    return model, (ctypes.c_double * 26 ** 4)(*model.logp), (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])


def anneal(name: str, cells: list[int], seed: int) -> tuple[float, list[int]]:
    _, logp, letters = _tables(name)
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = _kernel().additive_anneal(ints(*cells), n, 1, 0, logp, letters, ctypes.c_ulonglong(seed), _RESTARTS,
                                      _STEPS, ctypes.c_double(_TEMPERATURE), ctypes.c_double(0.0),
                                      (ctypes.c_int * 25)(), ints(), ints(), out)
    return total / (n - 3), list(out)


def _language(name: str, rng: random.Random) -> dict:
    model = _tables(name)[0]
    held = _split(name)[1]
    jobs = []
    for errors in (0, 8):
        for _ in range(_PLANTED):
            start = rng.randrange(len(held) - _LETTERS)
            text = held[start:start + _LETTERS]
            square = rng.sample(range(25), 25)
            where = {PLAIN[square[cell]]: cell for cell in range(25)}
            jobs.append(("planted", errors, text, corrupt([where[ch] for ch in text], errors, rng, "slip"),
                         rng.randrange(1 << 40)))
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        sources = [cells] + [rng.sample(cells, len(cells)) for _ in range(_SHUFFLES)]
        for index, source in enumerate(sources):
            for variant, run in variants(source).items():
                jobs.append((label, index, variant, run, rng.randrange(1 << 40)))
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(name, job[3], job[4]), jobs))
    planted = []
    table: dict[str, dict[str, list]] = {"cells": {}, "regrouped": {}}
    for job, (score, letters) in zip(jobs, results):
        if job[0] == "planted":
            _, errors, text, _, _ = job
            planted.append({"errors": errors,
                            "true_per_letter": round(model.score([ord(c) - 65 for c in text]) / (_LETTERS - 3), 4),
                            "found_per_letter": round(score, 4),
                            "letters_right": round(sum(chr(65 + x) == c for x, c in zip(letters, text)) / _LETTERS, 4)})
        else:
            label, index, variant, _, _ = job
            table[label].setdefault(variant, [None] * (_SHUFFLES + 1))[index] = round(score, 4)
    searched = {}
    for label, rows in table.items():
        best = max(values[0] for values in rows.values())
        bests = sorted((max(values[i] for values in rows.values()) for i in range(1, _SHUFFLES + 1)), reverse=True)
        searched[label] = {"square": rows["square"][0], "best": best,
                           "best_variant": max(rows, key=lambda v: rows[v][0]),
                           "shuffle_bests": bests, "shuffle_bests_as_high": sum(x >= best for x in bests)}
    return {
        "letters": {"train": len(_split(name)[0]), "held": len(held)},
        "planted": planted,
        "planted_recovered": sum(r["letters_right"] >= _RECOVERED for r in planted if r["errors"] == 0),
        "planted_with_errors_recovered": sum(r["letters_right"] >= _RECOVERED for r in planted if r["errors"] == 8),
        "searched": searched,
    }


@frozen("dagapeyeff-tongues")
def tongues_report() -> dict:
    rng = random.Random(_SEED)
    _kernel()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "shuffles": _SHUFFLES},
        "languages": {name: _language(name, rng) for name in LANGUAGES},
    }


_WIDE = 40


@frozen("dagapeyeff-romanian-wide")
def romanian_wide_report() -> dict:
    """The Romanian keyed-square family again, with 40 shuffles instead of 8, because the cells sat high in 8."""
    rng = random.Random(_SEED + 7)
    name = "Romanian-RRT"
    _kernel()
    jobs = []
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        sources = [cells] + [rng.sample(cells, len(cells)) for _ in range(_WIDE)]
        for index, source in enumerate(sources):
            for variant, run in variants(source).items():
                jobs.append((label, index, variant, run, rng.randrange(1 << 40)))
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(name, job[3], job[4])[0], jobs))
    table: dict[str, dict[str, list]] = {"cells": {}, "regrouped": {}}
    for (label, index, variant, _, _), score in zip(jobs, results):
        table[label].setdefault(variant, [None] * (_WIDE + 1))[index] = round(score, 4)
    out = {}
    for label, rows in table.items():
        best = max(values[0] for values in rows.values())
        bests = sorted((max(values[i] for values in rows.values()) for i in range(1, _WIDE + 1)), reverse=True)
        out[label] = {"best": best, "best_variant": max(rows, key=lambda v: rows[v][0]),
                      "shuffle_bests_high": bests[:5], "shuffle_bests_as_high": sum(x >= best for x in bests)}
    return {"solved": False, "claimed_plaintext": None, "shuffles": _WIDE, "searched": out}
