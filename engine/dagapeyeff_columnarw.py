"""Columnar transposition at widths 10 to 15 with a letter key, compiled, on the cells. Not a reading.

engine.dagapeyeff_exhaustive tried every column order up to width 10 with a
score a letter key cannot change, and lost its power at width 10.
engine.dagapeyeff_columnar14c closed the complete width 14 with a joint
compiled search. This pass runs the same kind of search
(engine/dagapeyeff_columnarw.c) at widths 10, 11, 12, 13 and 15, where 196
letters leave a short last row: the first 196 % width columns are one letter
longer. Both directions are searched, as in the width-14 pass, and recovery is
counted by the key: at least 90 percent of the cells get their true letter.

Each width and direction gets three planted held-out texts and one with 8
wrong cells. The printed cells and the regrouping get the same search, with
shuffled cells as the control. Wider keys lost their power in scratch runs
and are not searched. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import os
import random
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_columnar14c import DIRECTIONS, _tables, frequency_key
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model

_LETTERS = 196
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_columnarw.c"
_SEED = 20261018
# width: (restarts, steps)
WIDTHS = {10: (4, 16_000_000), 11: (4, 16_000_000), 12: (4, 16_000_000), 13: (4, 16_000_000),
          15: (4, 64_000_000)}
_TEMPERATURE = 12.0
_KEY_SHARE = 0.6
_SHUFFLES = 10
_ERRORS = 8
_RECOVERED = 0.9


def lengths(width: int) -> list[int]:
    rows, extra = -(-_LETTERS // width), _LETTERS % width
    return [rows if extra == 0 or column < extra else rows - 1 for column in range(width)]


def encrypt(symbols: list[int], slot: list[int], width: int, direction: str) -> tuple[list[int], list[int]]:
    """Cipher symbols, and the plaintext position behind each. slot[c] is the place column c is copied in."""
    sizes = lengths(width)
    order = [0] * width
    for column in range(width):
        order[slot[column]] = column
    offset = [0] * width
    running = 0
    for column in order:
        offset[column] = running
        running += sizes[column]
    cells = [0] * _LETTERS
    source = [0] * _LETTERS
    for column in range(width):
        for row in range(sizes[column]):
            if direction == "done":
                at, came = row * width + column, offset[column] + row
            else:
                at, came = offset[column] + row, row * width + column
            cells[at] = symbols[came]
            source[at] = came
    return cells, source


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the columnar search")
    built = Path(tempfile.mkdtemp(prefix="columnarw-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.cw_anneal.restype = ctypes.c_double
    return lib


def anneal(cells: list[int], width: int, direction: str, seed: int) -> tuple[float, list[int]]:
    """Best quadgram score per letter and the key behind it."""
    lib = _kernel()
    logp, letters = _tables()
    restarts, steps = WIDTHS[width]
    order = (ctypes.c_int * 32)()
    key = (ctypes.c_int * 25)()
    plain = (ctypes.c_int * _LETTERS)()
    total = lib.cw_anneal((ctypes.c_int * _LETTERS)(*cells), logp, letters, (ctypes.c_int * 25)(*frequency_key(cells)),
                          width, int(direction == "done"), ctypes.c_ulonglong(seed), restarts, steps,
                          ctypes.c_double(_TEMPERATURE), ctypes.c_double(_KEY_SHARE), order, key, plain)
    return total / (_LETTERS - 3), list(key)


def _jobs(rng: random.Random) -> list[dict]:
    jobs = []
    texts = (("cells", _cells()), ("regrouped", _regrouped_cells()))
    for width in WIDTHS:
        for direction in DIRECTIONS:
            for index, errors in enumerate((0, 0, 0, _ERRORS)):
                prose = _held(_HELD[index % len(_HELD)])
                start = rng.randrange(len(prose) - _LETTERS)
                text = prose[start:start + _LETTERS]
                slot = list(range(width))
                substitution = list(range(25))
                rng.shuffle(slot)
                rng.shuffle(substitution)
                cells, source = encrypt([substitution[PLAIN.index(ch)] for ch in text], slot, width, direction)
                for _ in range(errors):
                    cells[rng.randrange(_LETTERS)] = rng.randrange(25)
                jobs.append({"kind": "planted", "width": width, "direction": direction, "errors": errors,
                             "text": text, "cells": cells, "from": source, "seed": rng.randrange(1 << 40)})
            for label, cells in texts:
                jobs.append({"kind": label, "width": width, "direction": direction, "cells": cells,
                             "seed": rng.randrange(1 << 40)})
                for _ in range(_SHUFFLES):
                    mixed = list(cells)
                    rng.shuffle(mixed)
                    jobs.append({"kind": label, "shuffle": True, "width": width, "direction": direction,
                                 "cells": mixed, "seed": rng.randrange(1 << 40)})
    return jobs


@frozen("dagapeyeff-columnarw")
def columnarw_report() -> dict:
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
            text, cells, source = job["text"], job["cells"], job["from"]
            right = sum(PLAIN[key[cells[i]]] == text[source[i]] for i in range(_LETTERS)) / _LETTERS
            row["planted"].append({
                "errors": job["errors"],
                "true_per_letter": round(_model().score([ord(ch) - 65 for ch in text]) / (_LETTERS - 3), 4),
                "found_per_letter": round(score, 4),
                "cells_right": round(right, 4),
            })
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
        "search": {str(width): {"restarts": value[0], "steps": value[1]} for width, value in WIDTHS.items()},
        "temperature": _TEMPERATURE,
        "rows": list(rows.values()),
        "planted_recovered": sum(row["recovered"] for row in rows.values()),
        "planted": sum(len(row["planted"]) for row in rows.values()),
    }
