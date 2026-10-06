"""Latin under columnar transposition at widths 10 to 13 and 15 with a letter key. Not a reading.

Latin fits the cells' letter counts best of 39 languages
(engine.dagapeyeff_screen), and a transposition keeps letter counts.
engine.dagapeyeff_latin14 closed Latin under the complete width 14. This pass
runs the short-last-row kernel of engine.dagapeyeff_columnarw at widths 10,
11, 12, 13 and 15 under the Latin quadgram model of engine.dagapeyeff_latin,
starting from a Latin frequency key.

Each width and direction gets planted held-out Latin: two Thomistic windows,
one classical window, and one Thomistic window with 8 wrong cells. Recovery
means at least 90 percent of the cells get their true letter. The printed
cells and the regrouping get the same search, with shuffled cells as the
control. Texts are fetched, not stored. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
from concurrent.futures import ThreadPoolExecutor

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_columnar14c import DIRECTIONS
from engine.dagapeyeff_columnarw import WIDTHS, _kernel, encrypt
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_latin import _model, texts
from engine.dagapeyeff_latin14 import _tables, frequency_key

_LETTERS = 196
_SEED = 20261020
_TEMPERATURE = 12.0
_KEY_SHARE = 0.6
_SHUFFLES = 10
_ERRORS = 8
_RECOVERED = 0.9
_PLANTED = (("held", 0), ("held", 0), ("classical", 0), ("held", _ERRORS))


def anneal(cells: list[int], width: int, direction: str, seed: int) -> tuple[float, list[int]]:
    """Best Latin quadgram score per letter and the key behind it."""
    lib = _kernel()
    logp, letters = _tables()
    restarts, steps = WIDTHS[width]
    total = lib.cw_anneal((ctypes.c_int * _LETTERS)(*cells), logp, letters, (ctypes.c_int * 25)(*frequency_key(cells)),
                          width, int(direction == "done"), ctypes.c_ulonglong(seed), restarts, steps,
                          ctypes.c_double(_TEMPERATURE), ctypes.c_double(_KEY_SHARE), (ctypes.c_int * 32)(),
                          key := (ctypes.c_int * 25)(), (ctypes.c_int * _LETTERS)())
    return total / (_LETTERS - 3), list(key)


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (_LETTERS - 3)


def _jobs(rng: random.Random) -> list[dict]:
    jobs = []
    for width in WIDTHS:
        for direction in DIRECTIONS:
            for source, errors in _PLANTED:
                prose = texts()[source]
                start = rng.randrange(len(prose) - _LETTERS)
                text = prose[start:start + _LETTERS]
                slot = list(range(width))
                substitution = list(range(25))
                rng.shuffle(slot)
                rng.shuffle(substitution)
                cells, origin = encrypt([substitution[PLAIN.index(ch)] for ch in text], slot, width, direction)
                for _ in range(errors):
                    cells[rng.randrange(_LETTERS)] = rng.randrange(25)
                jobs.append({"kind": "planted", "width": width, "direction": direction, "source": source,
                             "errors": errors, "text": text, "cells": cells, "from": origin,
                             "seed": rng.randrange(1 << 40)})
            for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
                jobs.append({"kind": label, "width": width, "direction": direction, "cells": cells,
                             "seed": rng.randrange(1 << 40)})
                for _ in range(_SHUFFLES):
                    mixed = list(cells)
                    rng.shuffle(mixed)
                    jobs.append({"kind": label, "shuffle": True, "width": width, "direction": direction,
                                 "cells": mixed, "seed": rng.randrange(1 << 40)})
    return jobs


@frozen("dagapeyeff-latinw")
def latinw_report() -> dict:
    jobs = _jobs(random.Random(_SEED))
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["cells"], job["width"], job["direction"], job["seed"]), jobs))
    rows = {}
    for job, (score, key) in zip(jobs, found):
        row = rows.setdefault(f"{job['width']} {job['direction']}", {
            "width": job["width"], "direction": job["direction"], "planted": [],
            "cells": {"per_letter": None, "shuffles": []}, "regrouped": {"per_letter": None, "shuffles": []},
        })
        if job["kind"] == "planted":
            text, cells, origin = job["text"], job["cells"], job["from"]
            right = sum(PLAIN[key[cells[i]]] == text[origin[i]] for i in range(_LETTERS)) / _LETTERS
            row["planted"].append({"source": job["source"], "errors": job["errors"],
                                   "true_per_letter": round(_per_letter(text), 4),
                                   "found_per_letter": round(score, 4), "cells_right": round(right, 4)})
        elif job.get("shuffle"):
            row[job["kind"]]["shuffles"].append(round(score, 4))
        else:
            row[job["kind"]]["per_letter"] = round(score, 4)
    for row in rows.values():
        row["recovered"] = sum(plant["cells_right"] >= _RECOVERED for plant in row["planted"])
        row["weakest_planted_found"] = min(plant["found_per_letter"] for plant in row["planted"])
        for label in ("cells", "regrouped"):
            searched = row[label]
            searched["shuffles"].sort(reverse=True)
            searched["shuffles_as_high"] = sum(score >= searched["per_letter"] for score in searched["shuffles"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "language": "Latin (UD_Latin-ITTB model)",
        "search": {str(width): {"restarts": value[0], "steps": value[1]} for width, value in WIDTHS.items()},
        "temperature": _TEMPERATURE,
        "rows": list(rows.values()),
        "planted_recovered": sum(row["recovered"] for row in rows.values()),
        "planted": sum(len(row["planted"]) for row in rows.values()),
    }
