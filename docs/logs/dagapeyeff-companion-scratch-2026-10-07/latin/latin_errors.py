"""How many author mistakes can the Latin searches absorb? Not a reading.

Planted held-out Latin (Thomistic tail and classical Perseus) is put under a
random keyed square, then k cells are replaced by random symbols (k up to 48,
a quarter of the text). The keyed-square search of engine.dagapeyeff_latin and
the columnar joint search of engine.dagapeyeff_latinsmall (width 7) are run on
each. Recovery means at least 90 percent of the clean cells get their true
letter. No letter string is stored.
"""

from __future__ import annotations

import json
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_ROOT = Path(os.environ.get("UNDECIPHERED_TEXTS",
                            Path(__file__).resolve().parents[2] / "chasehendrick" / "undeciphered-texts"))
sys.path.insert(0, str(_ROOT))

from engine import dagapeyeff_latin as square  # noqa: E402
from engine import dagapeyeff_latinsmall as small  # noqa: E402
from engine.dagapeyeff_columnarw import encrypt  # noqa: E402
from engine.dagapeyeff_foursquare import PLAIN  # noqa: E402

N = 196
ERRORS = (0, 8, 16, 24, 32, 48)
SOURCES = ("held", "classical")
REPEATS = 3
SEED = 20261107
WIDTH = 7


def job(rng: random.Random, system: str, source: str, errors: int) -> dict:
    prose = square.texts()[source]
    start = rng.randrange(len(prose) - N)
    text = prose[start:start + N]
    sub = list(range(25))
    rng.shuffle(sub)
    symbols = [sub[PLAIN.index(ch)] for ch in text]
    if system == "square":
        cells, origin = symbols, list(range(N))
    else:
        slot = list(range(WIDTH))
        rng.shuffle(slot)
        cells, origin = encrypt(symbols, slot, WIDTH, "undone")
    wrong = set(rng.sample(range(N), errors))
    for i in wrong:
        cells[i] = rng.choice([s for s in range(25) if s != cells[i]])
    return {"system": system, "source": source, "errors": errors, "text": text, "cells": cells,
            "origin": origin, "wrong": wrong, "seed": rng.randrange(1 << 40)}


def run(j: dict) -> dict:
    if j["system"] == "square":
        score, letters = square.anneal(j["cells"], j["seed"])
        right = [chr(65 + letters[i]) == j["text"][i] for i in range(N) if i not in j["wrong"]]
    else:
        score, key = small.anneal(j["cells"], WIDTH, "undone", j["seed"])
        right = [PLAIN[key[j["cells"][i]]] == j["text"][j["origin"][i]] for i in range(N) if i not in j["wrong"]]
    share = sum(right) / len(right)
    return {"system": j["system"], "source": j["source"], "errors": j["errors"], "found_per_letter": round(score, 4),
            "clean_cells_right": round(share, 4), "recovered": share >= 0.9}


def report() -> dict:
    rng = random.Random(SEED)
    jobs = [job(rng, system, source, k) for system in ("square", "columnar7") for source in SOURCES
            for k in ERRORS for _ in range(REPEATS)]
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        rows = list(pool.map(run, jobs))
    table = {}
    for row in rows:
        cell = table.setdefault(f"{row['system']} {row['errors']}", {"recovered": 0, "of": 0, "found": []})
        cell["recovered"] += row["recovered"]
        cell["of"] += 1
        cell["found"].append(row["found_per_letter"])
    return {"solved": False, "claimed_plaintext": None, "rows": rows, "table": table}


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "results" / "latin_errors.json"
    out.parent.mkdir(exist_ok=True)
    result = report()
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result["table"], indent=1))
