"""The repeating coordinate shift at the periods left out: 6 and 8 to 13. Not a reading.

engine.dagapeyeff_additive (English) and engine.dagapeyeff_latinmore (Latin)
counted and searched a repeating shift on a keyed square at periods 2, 3, 4,
5, 7 and 14 only. This pass runs the same count and the same compiled search
at periods 6, 8, 9, 10, 11, 12 and 13, under the English and the Latin
quadgram models, shifting both coordinates or the column only.

The count: a repeating shift spreads each letter over several cells, so it
raises the number of different symbols; the cells use 18. Planted held-out
text under random squares and keys sets the range. The search: planted texts
show its power, shuffled cells are the control. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from concurrent.futures import ThreadPoolExecutor

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import MODES, _kernel, _random_key, _shape, encrypt
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_foursquare import _model as english_model
from engine.dagapeyeff_latin import _model as latin_model
from engine.dagapeyeff_latin import texts as latin_texts

PERIODS = (6, 8, 9, 10, 11, 12, 13)
_SEARCHED_MODES = ("both", "column")
_SEED = 20261021
_LETTERS = 196
_COUNT_STEP = 997
_COUNT_DRAWS = 3
_PLANTED = 2
_SHUFFLES = 3
_RESTARTS = 4
_STEPS = 4_000_000
_TEMPERATURE = 8.0
_KEY_SHARE = 0.3
_RECOVERED = 0.9


def _sources(language: str) -> list[str]:
    if language == "english":
        return [_held(name) for name in _HELD]
    return [latin_texts()["held"], latin_texts()["classical"]]


def _model(language: str):
    return english_model() if language == "english" else latin_model()


_TABLES: dict = {}


def _tables(language: str):
    if language not in _TABLES:
        _TABLES[language] = ((ctypes.c_double * 26 ** 4)(*_model(language).logp),
                             (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN]))
    return _TABLES[language]


def counts(language: str, rng: random.Random) -> list[dict]:
    cells = _shape(_cells())
    windows = [text[s:s + _LETTERS] for text in _sources(language) for s in range(0, len(text) - _LETTERS, _COUNT_STEP)]
    rows = []
    for mode in MODES:
        for period in PERIODS:
            draws = [_shape(encrypt(window, rng.sample(range(25), 25), _random_key(period, mode, rng)))
                     for window in windows for _ in range(_COUNT_DRAWS)]
            rows.append({"mode": mode, "period": period, "draws": len(draws),
                         "fewest_distinct": min(d["distinct"] for d in draws),
                         "reaching_cells": sum(d["distinct"] <= cells["distinct"]
                                               and d["top_three_rows"] >= cells["top_three_rows"] for d in draws)})
    return rows


def anneal(language: str, cells: list[int], period: int, mode: str, seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp, letters = _tables(language)
    n = len(cells)
    ints = ctypes.c_int * n
    out = ints()
    total = lib.additive_anneal(ints(*cells), n, period, MODES[mode], logp, letters, ctypes.c_ulonglong(seed),
                                _RESTARTS, _STEPS, ctypes.c_double(_TEMPERATURE), ctypes.c_double(_KEY_SHARE),
                                (ctypes.c_int * 25)(), ints(), ints(), out)
    return total / (n - 3), list(out)


def _search(language: str, rng: random.Random) -> dict:
    sources = _sources(language)
    jobs = []
    for mode in _SEARCHED_MODES:
        for period in PERIODS:
            for index in range(_PLANTED):
                source = sources[(len(jobs) + index) % len(sources)]
                start = rng.randrange(len(source) - _LETTERS)
                text = source[start:start + _LETTERS]
                cipher = encrypt(text, rng.sample(range(25), 25), _random_key(period, mode, rng))
                jobs.append(("planted", mode, period, text, cipher, rng.randrange(1 << 40)))
            for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
                jobs.append((label, mode, period, None, cells, rng.randrange(1 << 40)))
                for _ in range(_SHUFFLES):
                    jobs.append((label + " shuffle", mode, period, None, rng.sample(cells, len(cells)),
                                 rng.randrange(1 << 40)))
    _kernel()
    _tables(language)
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(language, job[4], job[2], job[1], job[5]), jobs))
    model = _model(language)
    planted, searched = [], {}
    for (label, mode, period, text, _, _), (score, letters) in zip(jobs, results):
        if label == "planted":
            planted.append({"mode": mode, "period": period,
                            "true_per_letter": round(model.score([ord(c) - 65 for c in text]) / (_LETTERS - 3), 4),
                            "found_per_letter": round(score, 4),
                            "letters_right": round(sum(chr(65 + x) == c for x, c in zip(letters, text)) / _LETTERS, 4)})
            continue
        row = searched.setdefault(f"{label.replace(' shuffle', '')} {mode} {period}", {"per_letter": None, "shuffles": []})
        if label.endswith("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(x >= row["per_letter"] for x in row["shuffles"])
    best = max(searched, key=lambda k: searched[k]["per_letter"])
    return {
        "planted": planted,
        "planted_recovered": sum(r["letters_right"] >= _RECOVERED for r in planted),
        "searched": searched,
        "searched_best": {"case": best, **searched[best]},
        "cases_cells_above_all_shuffles": sum(r["shuffles_as_high"] == 0 for r in searched.values()),
    }


@frozen("dagapeyeff-shiftgap")
def shiftgap_report() -> dict:
    rng = random.Random(_SEED)
    out = {"solved": False, "claimed_plaintext": None, "periods": list(PERIODS),
           "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE}}
    for language in ("english", "latin"):
        out[language] = {"counts": counts(language, rng), **_search(language, rng)}
    return out
