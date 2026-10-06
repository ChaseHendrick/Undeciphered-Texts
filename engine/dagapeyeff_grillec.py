"""A compiled turning-grille search, power only, not run on the cells. Not a reading.

engine.dagapeyeff_grille anneals a 14 by 14 Fleissner grille in Python and
recovered 1 of 3 planted grilles with the letter key given, and 0 of 2 with
the key unknown. This pass compiles the same grille convention
(engine/dagapeyeff_grillec.c) and gives it far more steps, under the default
model with J folded into I.

Three planted cases, all on held-out prose of 196 letters:

1. The letter key given. This is the power of the grille search itself.
2. Grille and key both unknown, the key starting from letter frequencies.
3. A key seeded without the grille, then held fixed. Two cells side by side
   in a row of the square are consecutive plaintext letters whenever their
   holes open in the same turn, about one time in four, whatever the grille.
   A key climbed on those pairs (and on pairs two and three apart) starts
   closer than a frequency key.

A search that cannot find a planted grille closes nothing, so the cells are
not searched here. Agreement is counted up to the turn the grille starts in.
No letter string is stored.
"""

from __future__ import annotations

import ctypes
import math
import os
import random
import shutil
import subprocess
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from engine.alphabet import letters_only
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar14c import frequency_key
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model
from engine.dagapeyeff_grille import ORBITS, SIDE, agreement, grille_order
from engine.language import _PUBLIC

_LETTERS = SIDE * SIDE
_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_grillec.c"
_SEED = 20261017
_PER_CASE = 4
_KEY_SHARE = 0.6
# (restarts, steps, temperature) for each case
_KNOWN = (4, 2_000_000, 10.0)
_JOINT = (4, 8_000_000, 12.0)
_SEEDED = (4, 2_000_000, 8.0)
_SEED_STEPS = 40_000
_SEED_RESTARTS = 4
_RECOVERED = 0.9


def encrypt(symbols: list[int], choice: list[int]) -> tuple[list[int], list[int]]:
    """Plaintext into the holes turn by turn, square read in row order, as engine.dagapeyeff_grille."""
    cells = [0] * _LETTERS
    source = [0] * _LETTERS
    for index, position in enumerate(grille_order(choice)):
        cells[position] = symbols[index]
        source[position] = index
    return cells, source


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the grille search")
    built = Path(tempfile.mkdtemp(prefix="grille-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.grille_anneal.restype = ctypes.c_double
    return lib


@lru_cache(maxsize=1)
def _tables():
    logp = (ctypes.c_double * 26 ** 4)(*_model().logp)
    letters = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    return logp, letters


def anneal(cells: list[int], start_key: list[int], fixed_key: bool, seed: int,
           settings: tuple[int, int, float]) -> tuple[float, list[int], list[int]]:
    """Best quadgram score per letter, the key and the grille behind it."""
    lib = _kernel()
    logp, letters = _tables()
    restarts, steps, temperature = settings
    choice = (ctypes.c_int * ORBITS)()
    key = (ctypes.c_int * 25)()
    plain = (ctypes.c_int * _LETTERS)()
    total = lib.grille_anneal((ctypes.c_int * _LETTERS)(*cells), logp, letters, (ctypes.c_int * 25)(*start_key),
                              int(fixed_key), 0, ctypes.c_ulonglong(seed), restarts, steps,
                              ctypes.c_double(temperature), ctypes.c_double(_KEY_SHARE), choice, key, plain)
    return total / (_LETTERS - 3), list(key), list(choice)


@lru_cache(maxsize=1)
def _pair_tables() -> tuple[list[float], list[list[list[float]]]]:
    """Letter rates and mixed pair weights for cells one, two and three apart in a row."""
    text = letters_only(_PUBLIC.read_text(encoding="utf-8")).replace("J", "I")
    singles = Counter(text)
    pairs = Counter(zip(text, text[1:]))
    total = len(text)
    rate = [(singles[ch] + 1) / (total + 25) for ch in PLAIN]
    joint = [[(pairs[(a, b)] + 0.1) / (total + 62.5) for b in PLAIN] for a in PLAIN]
    tables = []
    for share in (1 / 4, 3 / 16, 9 / 64):
        tables.append([[math.log(share * joint[a][b] / (rate[a] * rate[b]) + 1 - share) for b in range(25)]
                       for a in range(25)])
    return [math.log(value) for value in rate], tables


def seeded_key(cells: list[int], rng: random.Random) -> list[int]:
    """A key climbed on row neighbours, which a grille leaves as plaintext pairs about one time in four."""
    rates, tables = _pair_tables()
    groups = [
        (table, [(cells[row * SIDE + column], cells[row * SIDE + column + gap])
                 for row in range(SIDE) for column in range(SIDE - gap)])
        for gap, table in zip((1, 2, 3), tables)
    ]

    def score(key: list[int]) -> float:
        total = sum(rates[key[symbol]] for symbol in cells)
        for table, pairs in groups:
            total += sum(table[key[a]][key[b]] for a, b in pairs)
        return total

    best = (-math.inf, [])
    for _ in range(_SEED_RESTARTS):
        key = frequency_key(cells)
        current = score(key)
        top = (current, key[:])
        for step in range(_SEED_STEPS):
            temperature = 3.0 * (1 - step / _SEED_STEPS) + 0.01
            i, j = rng.randrange(25), rng.randrange(25)
            key[i], key[j] = key[j], key[i]
            trial = score(key)
            if trial >= current or rng.random() < math.exp((trial - current) / temperature):
                current = trial
                if current > top[0]:
                    top = (current, key[:])
            else:
                key[i], key[j] = key[j], key[i]
        if top[0] > best[0]:
            best = top
    return best[1]


def _cells_right(key: list[int], cells: list[int], source: list[int], text: str) -> float:
    return sum(PLAIN[key[cells[i]]] == text[source[i]] for i in range(_LETTERS)) / _LETTERS


@frozen("dagapeyeff-grillec")
def grillec_report() -> dict:
    rng = random.Random(_SEED)
    jobs = []
    for case in ("known", "joint", "seeded"):
        for index in range(_PER_CASE):
            prose = _held(_HELD[index % len(_HELD)])
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS]
            choice = [rng.randrange(4) for _ in range(ORBITS)]
            substitution = list(range(25))
            rng.shuffle(substitution)
            cells, source = encrypt([substitution[PLAIN.index(ch)] for ch in text], choice)
            if case == "known":
                key = [0] * 25
                for letter, symbol in enumerate(substitution):
                    key[symbol] = letter
            elif case == "seeded":
                key = seeded_key(cells, random.Random(rng.randrange(1 << 40)))
            else:
                key = frequency_key(cells)
            jobs.append({"case": case, "text": text, "choice": choice, "cells": cells, "source": source,
                         "start_key": key, "seed": rng.randrange(1 << 40)})
    settings = {"known": _KNOWN, "joint": _JOINT, "seeded": _SEEDED}
    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        found = list(pool.map(lambda job: anneal(job["cells"], job["start_key"], job["case"] != "joint",
                                                 job["seed"], settings[job["case"]]), jobs))
    rows = []
    for job, (score, key, choice) in zip(jobs, found):
        rows.append({
            "case": job["case"],
            "true_per_letter": round(_model().score([ord(ch) - 65 for ch in job["text"]]) / (_LETTERS - 3), 4),
            "found_per_letter": round(score, 4),
            "start_cells_right": round(_cells_right(job["start_key"], job["cells"], job["source"], job["text"]), 4),
            "cells_right": round(_cells_right(key, job["cells"], job["source"], job["text"]), 4),
            "holes_right": agreement(choice, job["choice"]),
        })
    recovered = {}
    for row in rows:
        tally = recovered.setdefault(row["case"], [0, 0])
        tally[0] += row["holes_right"] == ORBITS and row["cells_right"] >= _RECOVERED
        tally[1] += 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {name: {"restarts": value[0], "steps": value[1], "temperature": value[2]}
                   for name, value in settings.items()},
        "planted": rows,
        "recovered": recovered,
        "cells_searched": False,
        "scope": (
            "Power only. With the key given the grille comes back; with the key unknown it does not, so a "
            "grille on the cells is neither found nor excluded. No letter string is stored."
        ),
    }
