"""Do the cells' best Latin decryptions contain Latin words? Not a reading.

A quadgram score cannot separate heavily mistaken Latin from noise: planted
Latin with 16 to 32 wrong cells is recovered but scores -3.3 to -4.0 a letter,
where the cells' best decryptions also sit (latin/latin_errors.py). Words can
separate them. A decryption that is about 90 percent right still has long runs
of real words. A key fitted to noise makes plausible quadgrams but few long
words.

Measure: the share of letters covered by non-overlapping dictionary words of at
least 5 letters (dynamic programming, best cover). The vocabulary is every word
form seen at least twice in the first 90 percent of UD_Latin-ITTB plus UD_Latin-PROIEL
(Vulgate, Caesar, Cicero). It does not include the held-out ITTB tail or
UD_Latin-Perseus, which are what is planted.

Compared:
- planted Latin, keyed square and width-7 columns, 0 to 32 wrong cells, decrypted by the key the search found;
- the printed cells and the regrouping, best decryption under the keyed square and columnar widths 2 to 15 in both directions;
- shuffled cells under the same searches.

Only coverage numbers are stored. No letter string is stored.
"""

from __future__ import annotations

import ctypes
import json
import os
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

_ROOT = Path(os.environ.get("UNDECIPHERED_TEXTS",
                            Path(__file__).resolve().parents[2] / "chasehendrick" / "undeciphered-texts"))
sys.path.insert(0, str(_ROOT))

from engine import dagapeyeff_latin as square  # noqa: E402
from engine.dagapeyeff_add import _cells  # noqa: E402
from engine.dagapeyeff_columnar import _regrouped_cells  # noqa: E402
from engine.dagapeyeff_columnarw import _kernel, encrypt  # noqa: E402
from engine.dagapeyeff_foursquare import PLAIN  # noqa: E402
from engine.dagapeyeff_latin14 import _tables, frequency_key  # noqa: E402
from engine.dagapeyeff_screen import _fetch, fold  # noqa: E402

N = 196
MIN_WORD = 5
SEED = 20261108
WIDTHS = tuple(range(2, 16))
SHUFFLES = 4
ERRORS = (0, 8, 16, 24, 32)
REPEATS = 3


def _forms(name: str, share: float = 1.0) -> list[str]:
    sentences = []
    for path in sorted(_fetch(name).glob("*.conllu")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# text = "):
                sentences.append(line[len("# text = "):])
    sentences = sentences[:int(len(sentences) * share)]
    return [fold(word) for sentence in sentences for word in sentence.split()]


@lru_cache(maxsize=1)
def vocabulary() -> frozenset[str]:
    counts = Counter(_forms("Latin-ITTB", 0.9) + _forms("Latin-PROIEL"))
    return frozenset(w for w, n in counts.items() if n >= 2 and len(w) >= MIN_WORD)


def coverage(text: str) -> float:
    """Share of letters in the best cover by dictionary words of MIN_WORD letters or more."""
    words = vocabulary()
    longest = max(map(len, words))
    best = [0] * (len(text) + 1)
    for end in range(1, len(text) + 1):
        best[end] = best[end - 1]
        for size in range(MIN_WORD, min(longest, end) + 1):
            if text[end - size:end] in words and best[end - size] + size > best[end]:
                best[end] = best[end - size] + size
    return best[-1] / len(text)


def _columnar(cells: list[int], width: int, direction: str, seed: int) -> tuple[float, str, list[int]]:
    lib = _kernel()
    logp, letters = _tables()
    steps = 4_000_000 if width < 10 else 16_000_000
    plain, key = (ctypes.c_int * N)(), (ctypes.c_int * 25)()
    total = lib.cw_anneal((ctypes.c_int * N)(*cells), logp, letters, (ctypes.c_int * 25)(*frequency_key(cells)),
                          width, int(direction == "done"), ctypes.c_ulonglong(seed), 4, steps, ctypes.c_double(12.0),
                          ctypes.c_double(0.6), (ctypes.c_int * 32)(), key, plain)
    return total / (N - 3), "".join(chr(65 + x) for x in plain), list(key)


def _square(cells: list[int], seed: int) -> tuple[float, str]:
    score, letters = square.anneal(cells, seed)
    return score, "".join(chr(65 + x) for x in letters)


def _plant_jobs(rng: random.Random) -> list[dict]:
    jobs = []
    for system in ("square", "columnar7"):
        for source in ("held", "classical"):
            for k in ERRORS:
                for _ in range(REPEATS):
                    prose = square.texts()[source]
                    start = rng.randrange(len(prose) - N)
                    text = prose[start:start + N]
                    sub = list(range(25))
                    rng.shuffle(sub)
                    symbols = [sub[PLAIN.index(ch)] for ch in text]
                    if system == "square":
                        cells, origin = symbols, list(range(N))
                    else:
                        slot = list(range(7))
                        rng.shuffle(slot)
                        cells, origin = encrypt(symbols, slot, 7, "undone")
                    wrong = set(rng.sample(range(N), k))
                    for i in wrong:
                        cells[i] = rng.choice([s for s in range(25) if s != cells[i]])
                    jobs.append({"kind": "planted", "system": system, "source": source, "errors": k, "text": text,
                                 "cells": cells, "origin": origin, "wrong": wrong, "seed": rng.randrange(1 << 40)})
    return jobs


def _search_jobs(rng: random.Random) -> list[dict]:
    jobs = []
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        sources = [cells]
        for _ in range(SHUFFLES):
            mixed = list(cells)
            rng.shuffle(mixed)
            sources.append(mixed)
        for index, source in enumerate(sources):
            jobs.append({"kind": label, "index": index, "system": "square", "cells": source,
                         "seed": rng.randrange(1 << 40)})
            for width in WIDTHS:
                for direction in ("undone", "done"):
                    jobs.append({"kind": label, "index": index, "system": f"columnar {width} {direction}",
                                 "width": width, "direction": direction, "cells": source,
                                 "seed": rng.randrange(1 << 40)})
    return jobs


def run(job: dict) -> dict:
    if job["kind"] == "planted":
        if job["system"] == "square":
            score, text = _square(job["cells"], job["seed"])
            right = sum(text[i] == job["text"][i] for i in range(N) if i not in job["wrong"])
        else:
            score, text, key = _columnar(job["cells"], 7, "undone", job["seed"])
            right = sum(PLAIN[key[job["cells"][i]]] == job["text"][job["origin"][i]]
                        for i in range(N) if i not in job["wrong"])
        return {"kind": "planted", "system": job["system"], "source": job["source"], "errors": job["errors"],
                "per_letter": round(score, 4), "clean_cells_right": round(right / (N - job["errors"]), 4),
                "coverage": round(coverage(text), 4), "true_coverage": round(coverage(job["text"]), 4)}
    if job["system"] == "square":
        score, text = _square(job["cells"], job["seed"])
    else:
        score, text, _ = _columnar(job["cells"], job["width"], job["direction"], job["seed"])
    return {"kind": job["kind"], "index": job["index"], "system": job["system"], "per_letter": round(score, 4),
            "coverage": round(coverage(text), 4)}


def report() -> dict:
    rng = random.Random(SEED)
    jobs = _plant_jobs(rng) + _search_jobs(rng)
    vocabulary(), _kernel(), _tables(), square._tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        rows = list(pool.map(run, jobs))
    planted = [row for row in rows if row["kind"] == "planted"]
    summary = {}
    for row in planted:
        cell = summary.setdefault(f"{row['system']} {row['errors']}", [])
        cell.append(row["coverage"])
    searched = {}
    for label in ("cells", "regrouped"):
        mine = [row for row in rows if row["kind"] == label]
        printed = [row for row in mine if row["index"] == 0]
        top = max(printed, key=lambda row: row["coverage"])
        shuffle_tops = [max(row["coverage"] for row in mine if row["index"] == i) for i in range(1, SHUFFLES + 1)]
        searched[label] = {"best_coverage": top["coverage"], "best_system": top["system"],
                           "shuffle_best_coverages": sorted(shuffle_tops, reverse=True),
                           "shuffles_as_high": sum(x >= top["coverage"] for x in shuffle_tops)}
    return {"solved": False, "claimed_plaintext": None, "min_word": MIN_WORD, "vocabulary": len(vocabulary()),
            "planted_coverage": summary, "searched": searched, "rows": rows}


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "results" / "latin_words.json"
    result = report()
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=1))
