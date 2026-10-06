"""Latin under a complete 14-column transposition with a letter key. Not a reading.

Latin is the language closest to the cells' letter counts
(engine.dagapeyeff_screen), and under a one-to-one key alone it does not read
them (engine.dagapeyeff_latin). A transposition keeps letter counts, so Latin
under a 14-column key is the next search. engine.dagapeyeff_columnar14c closed
that family for English only. This pass runs the same compiled kernel
(engine/dagapeyeff_columnar14c.c) under the Latin quadgram model of
engine.dagapeyeff_latin, starting from a Latin frequency key.

Planted held-out Latin (the Thomistic tail and classical Latin, both
directions, some with 8 wrong cells) shows the search's power; the cells and
the regrouping are run with shuffles. Texts are fetched, not stored. No letter
string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_columnar14c import DIRECTIONS, WIDTH, _kernel, encrypt
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_latin import _model, texts

_SEED = 20261014
_LETTERS = WIDTH * WIDTH
_RESTARTS = 8
_STEPS = 16_000_000
_TEMPERATURE = 12.0
_KEY_SHARE = 0.6
_SHUFFLES = 10
_RECOVERED = 0.9
_PLANTED = ((0, 1), (8, 1))


@lru_cache(maxsize=1)
def latin_order() -> str:
    counts = Counter(texts()["train"])
    return "".join(sorted(PLAIN, key=lambda ch: (-counts[ch], ch)))


def frequency_key(cells: list[int]) -> list[int]:
    counts = Counter(cells)
    ranked = sorted(range(25), key=lambda symbol: (-counts[symbol], symbol))
    key = [0] * 25
    for rank, symbol in enumerate(ranked):
        key[symbol] = PLAIN.index(latin_order()[rank])
    return key


@lru_cache(maxsize=1)
def _tables():
    return (ctypes.c_double * 26 ** 4)(*_model().logp), (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])


def anneal(cells: list[int], direction: str, seed: int) -> tuple[float, list[int]]:
    lib = _kernel()
    logp, letters = _tables()
    total = lib.c14_anneal((ctypes.c_int * _LETTERS)(*cells), logp, letters,
                           (ctypes.c_int * 25)(*frequency_key(cells)), int(direction == "done"),
                           ctypes.c_ulonglong(seed), _RESTARTS, _STEPS, ctypes.c_double(_TEMPERATURE),
                           ctypes.c_double(_KEY_SHARE), (ctypes.c_int * WIDTH)(), key := (ctypes.c_int * 25)(),
                           (ctypes.c_int * _LETTERS)())
    return total / (_LETTERS - 3), list(key)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


@frozen("dagapeyeff-latin14")
def latin14_report() -> dict:
    rng = random.Random(_SEED)
    planted_jobs = []
    for direction in DIRECTIONS:
        for errors, per_source in _PLANTED:
            for source in ("held", "classical"):
                prose = texts()[source]
                for _ in range(per_source):
                    start = rng.randrange(len(prose) - _LETTERS)
                    text = prose[start:start + _LETTERS]
                    order = list(range(WIDTH))
                    substitution = list(range(25))
                    rng.shuffle(order)
                    rng.shuffle(substitution)
                    cells, origin = encrypt([substitution[PLAIN.index(ch)] for ch in text], order, direction)
                    for _ in range(errors):
                        cells[rng.randrange(_LETTERS)] = rng.randrange(25)
                    planted_jobs.append({"source": source, "direction": direction, "errors": errors, "text": text,
                                         "cells": cells, "from": origin, "seed": rng.randrange(1 << 40)})
    searched_jobs = []
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        for direction in DIRECTIONS:
            searched_jobs.append({"label": f"{label} {direction}", "direction": direction, "cells": cells,
                                  "seed": rng.randrange(1 << 40)})
            for _ in range(_SHUFFLES):
                mixed = list(cells)
                rng.shuffle(mixed)
                searched_jobs.append({"label": f"{label} {direction}", "direction": direction, "cells": mixed,
                                      "shuffle": True, "seed": rng.randrange(1 << 40)})
    jobs = planted_jobs + searched_jobs
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["cells"], job["direction"], job["seed"]), jobs))
    planted = []
    for job, (score, key) in zip(planted_jobs, found):
        text, cells, origin = job["text"], job["cells"], job["from"]
        right = sum(PLAIN[key[cells[i]]] == text[origin[i]] for i in range(_LETTERS)) / _LETTERS
        planted.append({"source": job["source"], "direction": job["direction"], "errors": job["errors"],
                        "true_per_letter": round(_per_letter(text), 4), "found_per_letter": round(score, 4),
                        "cells_right": round(right, 4)})
    searched = {}
    for job, (score, _) in zip(searched_jobs, found[len(planted_jobs):]):
        row = searched.setdefault(job["label"], {"per_letter": None, "shuffles": []})
        if job.get("shuffle"):
            row["shuffles"].append(round(score, 4))
        else:
            row["per_letter"] = round(score, 4)
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(score >= row["per_letter"] for score in row["shuffles"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE},
        "planted": planted,
        "planted_recovered": sum(row["cells_right"] >= _RECOVERED for row in planted),
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
    }
