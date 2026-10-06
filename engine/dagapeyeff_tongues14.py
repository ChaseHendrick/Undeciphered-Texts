"""Catalan and Romanian under a complete 14-column transposition with a letter key. Not a reading.

After Latin, Catalan and Romanian come closest to the cells' letter counts
(engine.dagapeyeff_screen: 5 and 7 errors at their closest windows), and under
a one-to-one key alone neither reads the cells (engine.dagapeyeff_tongues). A
transposition keeps letter counts, so a 14-column key is the next search, as
engine.dagapeyeff_latin14 did for Latin. This pass runs the same compiled
kernel (engine/dagapeyeff_columnar14c.c) under each language's quadgram model
(the first 90 percent of its Universal Dependencies treebank), starting from a
frequency key in that language.

Planted held-out text from each treebank's last 10 percent, both directions,
some with 8 wrong cells, shows the search's power; the cells and the
regrouping are run with shuffles. Texts are fetched, not stored. No letter
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
from engine.dagapeyeff_tongues import LANGUAGES, _split, _tables

_SEED = 20261022
_LETTERS = WIDTH * WIDTH
_RESTARTS = 8
_STEPS = 16_000_000
_TEMPERATURE = 12.0
_KEY_SHARE = 0.6
_SHUFFLES = 8
_RECOVERED = 0.9
_PLANTED = ((0, 2), (8, 1))


@lru_cache(maxsize=None)
def _order(name: str) -> str:
    counts = Counter(_split(name)[0])
    return "".join(sorted(PLAIN, key=lambda ch: (-counts[ch], ch)))


def frequency_key(name: str, cells: list[int]) -> list[int]:
    counts = Counter(cells)
    ranked = sorted(range(25), key=lambda symbol: (-counts[symbol], symbol))
    key = [0] * 25
    for rank, symbol in enumerate(ranked):
        key[symbol] = PLAIN.index(_order(name)[rank])
    return key


def anneal(name: str, cells: list[int], direction: str, seed: int) -> tuple[float, list[int]]:
    _, logp, letters = _tables(name)
    total = _kernel().c14_anneal((ctypes.c_int * _LETTERS)(*cells), logp, letters,
                                 (ctypes.c_int * 25)(*frequency_key(name, cells)), int(direction == "done"),
                                 ctypes.c_ulonglong(seed), _RESTARTS, _STEPS, ctypes.c_double(_TEMPERATURE),
                                 ctypes.c_double(_KEY_SHARE), (ctypes.c_int * WIDTH)(), key := (ctypes.c_int * 25)(),
                                 (ctypes.c_int * _LETTERS)())
    return total / (_LETTERS - 3), list(key)


def _jobs(rng: random.Random) -> list[dict]:
    jobs = []
    for name in LANGUAGES:
        held = _split(name)[1]
        for direction in DIRECTIONS:
            for errors, count in _PLANTED:
                for _ in range(count):
                    start = rng.randrange(len(held) - _LETTERS)
                    text = held[start:start + _LETTERS]
                    order = list(range(WIDTH))
                    substitution = list(range(25))
                    rng.shuffle(order)
                    rng.shuffle(substitution)
                    cells, origin = encrypt([substitution[PLAIN.index(ch)] for ch in text], order, direction)
                    for _ in range(errors):
                        cells[rng.randrange(_LETTERS)] = rng.randrange(25)
                    jobs.append({"language": name, "kind": "planted", "direction": direction, "errors": errors,
                                 "text": text, "cells": cells, "from": origin, "seed": rng.randrange(1 << 40)})
            for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
                jobs.append({"language": name, "kind": label, "direction": direction, "cells": cells,
                             "seed": rng.randrange(1 << 40)})
                for _ in range(_SHUFFLES):
                    mixed = list(cells)
                    rng.shuffle(mixed)
                    jobs.append({"language": name, "kind": label, "shuffle": True, "direction": direction,
                                 "cells": mixed, "seed": rng.randrange(1 << 40)})
    return jobs


@frozen("dagapeyeff-tongues14")
def tongues14_report() -> dict:
    jobs = _jobs(random.Random(_SEED))
    _kernel()
    for name in LANGUAGES:
        _tables(name)
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["language"], job["cells"], job["direction"], job["seed"]), jobs))
    out = {name: {"planted": [], "searched": {}} for name in LANGUAGES}
    for job, (score, key) in zip(jobs, found):
        row = out[job["language"]]
        if job["kind"] == "planted":
            model = _tables(job["language"])[0]
            text, cells, origin = job["text"], job["cells"], job["from"]
            right = sum(PLAIN[key[cells[i]]] == text[origin[i]] for i in range(_LETTERS)) / _LETTERS
            row["planted"].append({"direction": job["direction"], "errors": job["errors"],
                                   "true_per_letter": round(model.score([ord(c) - 65 for c in text]) / (_LETTERS - 3), 4),
                                   "found_per_letter": round(score, 4), "cells_right": round(right, 4)})
            continue
        searched = row["searched"].setdefault(f"{job['kind']} {job['direction']}", {"per_letter": None, "shuffles": []})
        if job.get("shuffle"):
            searched["shuffles"].append(round(score, 4))
        else:
            searched["per_letter"] = round(score, 4)
    for row in out.values():
        row["planted_recovered"] = sum(p["cells_right"] >= _RECOVERED for p in row["planted"])
        for searched in row["searched"].values():
            searched["shuffles"].sort(reverse=True)
            searched["shuffles_as_high"] = sum(s >= searched["per_letter"] for s in searched["shuffles"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "temperature": _TEMPERATURE, "key_share": _KEY_SHARE},
        "languages": out,
    }
