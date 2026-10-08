"""Latin under a 14 by 14 turning grille with a letter key. Not a reading.

The Undeciphered-Texts grille search (engine.dagapeyeff_grillec) recovers
planted grilles with the letter key given, but 0 of 7 with grille and key both
unknown: it settles at 13 to 20 of 49 holes. This search re-solves the letter
key at every grille move (greedy swaps on the grille's symbol-pair counts under
a Latin letter-pair model), so a grille is judged by its best key, then
polishes grille and key together under the Latin quadgram model of
engine.dagapeyeff_latin. Planted held-out Latin gives the power; shuffled cells
are the control. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from functools import lru_cache
from pathlib import Path

_ROOT = Path(os.environ.get("UNDECIPHERED_TEXTS",
                            Path(__file__).resolve().parents[2] / "chasehendrick" / "undeciphered-texts"))
sys.path.insert(0, str(_ROOT))

from engine.dagapeyeff_columnar14c import frequency_key  # noqa: E402
from engine.dagapeyeff_foursquare import PLAIN  # noqa: E402
from engine.dagapeyeff_grille import ORBITS, agreement  # noqa: E402
from engine.dagapeyeff_grillec import encrypt  # noqa: E402
from engine.dagapeyeff_latin import _model, texts  # noqa: E402
from engine.dagapeyeff_latin14 import _tables  # noqa: E402

N = 196
_SOURCE = Path(__file__).resolve().parent / "latin_grille.c"
_I, _D = ctypes.c_int, ctypes.c_double


@lru_cache(maxsize=1)
def kernel():
    out = Path(tempfile.gettempdir()) / f"latin_grille_{os.getpid()}.so"
    subprocess.run([shutil.which("cc") or shutil.which("gcc"), "-O3", "-march=native", "-shared", "-fPIC",
                    "-o", str(out), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(out))
    p_i, p_d = ctypes.POINTER(_I), ctypes.POINTER(_D)
    lib.grille_nested.restype = _D
    lib.grille_nested.argtypes = [p_i, p_d, p_i, ctypes.c_ulonglong, _I, _I, _D, p_i, p_i]
    lib.grille_nestq.restype = _D
    lib.grille_nestq.argtypes = [p_i, p_d, p_i, p_i, ctypes.c_ulonglong, _I, _I, _D, _I, p_i, p_i]
    lib.grille_polish.restype = _D
    lib.grille_polish.argtypes = [p_i, p_d, p_i, p_i, p_i, ctypes.c_ulonglong, _I, _D, _D, p_i, p_i]
    return lib


@lru_cache(maxsize=1)
def pair_table():
    """Latin letter-pair log probabilities, log P(b | a), on PLAIN indices."""
    text = texts()["train"]
    pairs = Counter(zip(text, text[1:]))
    singles = Counter(text[:-1])
    table = []
    for a in PLAIN:
        for b in PLAIN:
            table.append(math.log((pairs[(a, b)] + 0.5) / (singles[a] + 12.5)))
    return (_D * 625)(*table)


def search(cells: list[int], seed: int, restarts: int = 8, steps: int = 20_000, temperature: float = 3.0,
           polish_steps: int = 2_000_000, polish_temperature: float = 6.0, model: str = "quad",
           max_pass: int = 2) -> dict:
    lib = kernel()
    logp, letters = _tables()
    choice, key = (_I * ORBITS)(), (_I * 25)()
    if model == "quad":
        nested = lib.grille_nestq((_I * N)(*cells), logp, letters, (_I * 25)(*frequency_key(cells)), seed,
                                  restarts, steps, temperature, max_pass, choice, key)
    else:
        nested = lib.grille_nested((_I * N)(*cells), pair_table(), (_I * 25)(*frequency_key(cells)), seed,
                                   restarts, steps, temperature, choice, key)
    first = list(choice)
    out_choice, out_key = (_I * ORBITS)(), (_I * 25)()
    total = lib.grille_polish((_I * N)(*cells), logp, letters, choice, key, seed + 1, polish_steps,
                              polish_temperature, 0.5, out_choice, out_key)
    return {"nested": nested, "nested_choice": first, "per_letter": total / (N - 3),
            "choice": list(out_choice), "key": list(out_key)}


def plant(rng: random.Random, source: str, errors: int) -> dict:
    prose = texts()[source]
    start = rng.randrange(len(prose) - N)
    text = prose[start:start + N]
    choice = [rng.randrange(4) for _ in range(ORBITS)]
    sub = list(range(25))
    rng.shuffle(sub)
    cells, origin = encrypt([sub[PLAIN.index(ch)] for ch in text], choice)
    for i in rng.sample(range(N), errors):
        cells[i] = rng.choice([s for s in range(25) if s != cells[i]])
    return {"source": source, "errors": errors, "text": text, "choice": choice, "cells": cells, "origin": origin,
            "seed": rng.randrange(1 << 40)}


def judge(job: dict, found: dict) -> dict:
    right = sum(PLAIN[found["key"][c]] == job["text"][o] for c, o in zip(job["cells"], job["origin"])) / N
    return {"source": job["source"], "errors": job["errors"],
            "true_per_letter": round(_model().score([ord(ch) - 65 for ch in job["text"]]) / (N - 3), 4),
            "found_per_letter": round(found["per_letter"], 4),
            "holes_after_nested": agreement(found["nested_choice"], job["choice"]),
            "holes_right": agreement(found["choice"], job["choice"]), "cells_right": round(right, 4)}


def _true_key(job: dict) -> list[int]:
    key = [0] * 25
    for c, o in zip(job["cells"], job["origin"]):
        key[c] = PLAIN.index(job["text"][o])
    return key


def _spoil(key: list[int], cells: list[int], share: float, rng: random.Random) -> list[int]:
    """Rotate the letters of random symbols until about `share` of the cells are wrong."""
    counts = Counter(cells)
    symbols = list(counts)
    rng.shuffle(symbols)
    chosen, covered = [], 0
    for symbol in symbols:
        if covered >= share * N:
            break
        chosen.append(symbol)
        covered += counts[symbol]
    key = key[:]
    if len(chosen) > 1:
        letters = [key[s] for s in chosen]
        for symbol, letter in zip(chosen, letters[1:] + letters[:1]):
            key[symbol] = letter
    return key


def _fixed(job: dict, key: list[int], seed: int, restarts: int = 4, steps: int = 2_000_000) -> tuple[float, list]:
    lib = kernel()
    logp, letters = _tables()
    best = (-1e300, [])
    for r in range(restarts):
        start = [random.Random(seed + r).randrange(4) for _ in range(ORBITS)]
        choice, out_key = (_I * ORBITS)(), (_I * 25)()
        score = lib.grille_polish((_I * N)(*job["cells"]), logp, letters, (_I * ORBITS)(*start), (_I * 25)(*key),
                                  seed + r, steps, 8.0, 0.0, choice, out_key)
        if score > best[0]:
            best = (score, list(choice))
    return best[0] / (N - 3), best[1]


def report(seed: int = 20261107) -> dict:
    from concurrent.futures import ThreadPoolExecutor

    rng = random.Random(seed)
    kernel(), _tables()
    planted = [plant(rng, "held", 0) for _ in range(4)]
    fixed_jobs = []
    for job in planted:
        for share in (0.0, 0.15, 0.3):
            key = _spoil(_true_key(job), job["cells"], share, rng)
            fixed_jobs.append((job, share, key, rng.randrange(1 << 40)))

    def run_fixed(item):
        job, share, key, s = item
        score, choice = _fixed(job, key, s)
        right = sum(PLAIN[key[c]] == job["text"][o] for c, o in zip(job["cells"], job["origin"])) / N
        return {"spoiled": share, "key_cells_right": round(right, 4), "found_per_letter": round(score, 4),
                "holes_right": agreement(choice, job["choice"])}

    def run_joint(job):
        return judge(job, search(job["cells"], job["seed"], restarts=2, steps=60_000, temperature=6.0))

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        fixed = list(pool.map(run_fixed, fixed_jobs))
        joint = list(pool.map(run_joint, planted))
    return {
        "solved": False, "claimed_plaintext": None, "cells_searched": False,
        "language": "Latin (UD_Latin-ITTB model, held-out tail planted)",
        "fixed_key": fixed,
        "joint_nested_quadgram": joint,
        "joint_recovered": sum(row["holes_right"] == ORBITS for row in joint),
    }


if __name__ == "__main__":
    import json

    out = Path(__file__).resolve().parents[1] / "results" / "latin_grille.json"
    out.parent.mkdir(exist_ok=True)
    result = report()
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))
