"""A direction swarm: old leads rerun with a strong solver and family-wise controls. Not a reading.

Several earlier probes left faint leads, scored with the 8,689-letter legacy
model and without planted texts: a delay of 79 between the row and column
digits (3 of 200 shuffles as high), nulls by place, rail and column reads.
This swarm reruns those families as transforms of the cells, each solved as a
keyed Polybius square by engine/dagapeyeff_additive.c at period 1 under the
default model:

- delay d: the column digits rotated d places against the row digits, 1 to 195;
- nulls p:f: every cell at place i with i mod p = f dropped, p from 2 to 14;
- rail r: a rail fence of r rails, 2 to 14, undone or done;
- columns w: rows of w written across and read down, 10 to 28, undone or done.

Each family has a planted held-out English text with a random parameter. The
control runs every transform on shuffles of all 196 cells, so the cells' best
is compared with each shuffle's best, per family and overall. No letter string
is stored.
"""

from __future__ import annotations

import os
import random
import statistics
from concurrent.futures import ThreadPoolExecutor

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel, _tables, anneal
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model

_SEED = 20261008
_RESTARTS = 2
_STEPS = 300_000
_SHUFFLES = 8
_RECOVERED = 0.9
_PROSE_FLOOR = -2.5
_LETTERS = 196


def delay(cells: list, d: int) -> list:
    n = len(cells)
    return [(cells[i] // 5) * 5 + cells[(i + d) % n] % 5 for i in range(n)]


def undelay(cells: list, d: int) -> list:
    n = len(cells)
    out = [0] * n
    for i in range(n):
        out[i] = (cells[i] // 5) * 5
    for i in range(n):
        out[(i + d) % n] += cells[i] % 5
    return out


def drop(cells: list, p: int, f: int) -> list:
    return [cell for i, cell in enumerate(cells) if i % p != f]


def _rail_order(n: int, rails: int) -> list[int]:
    """Plaintext places in the order a rail fence writes them out."""
    cycle = 2 * (rails - 1)
    rows = [min(i % cycle, cycle - i % cycle) for i in range(n)]
    return sorted(range(n), key=lambda i: (rows[i], i))


def _column_order(n: int, width: int) -> list[int]:
    """Plaintext places in the order rows of width are read down the columns."""
    return sorted(range(n), key=lambda i: (i % width, i // width))


def undo(cells: list, order: list[int]) -> list:
    out = [0] * len(cells)
    for k, place in enumerate(order):
        out[place] = cells[k]
    return out


def do(cells: list, order: list[int]) -> list:
    return [cells[place] for place in order]


def transforms(cells: list) -> dict[str, tuple[str, list]]:
    n = len(cells)
    out = {}
    for d in range(1, n):
        out[f"delay {d}"] = ("delay", delay(cells, d))
    for p in range(2, 15):
        for f in range(p):
            out[f"nulls {p}:{f}"] = ("nulls", drop(cells, p, f))
    for rails in range(2, 15):
        order = _rail_order(n, rails)
        out[f"rail {rails} undone"] = ("rail", undo(cells, order))
        out[f"rail {rails} done"] = ("rail", do(cells, order))
    for width in range(10, 29):
        order = _column_order(n, width)
        out[f"columns {width} undone"] = ("columns", undo(cells, order))
        out[f"columns {width} done"] = ("columns", do(cells, order))
    return out


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def _plant(rng: random.Random, family: str, length: int) -> tuple[str, list[int], str]:
    """A planted cipher whose named transform gives back a keyed-square text."""
    prose = _held(_HELD[rng.randrange(len(_HELD))])
    while True:
        start = rng.randrange(len(prose) - length)
        text = prose[start:start + length]
        if _per_letter(text) >= _PROSE_FLOOR:
            break
    square = list(range(25))
    rng.shuffle(square)
    where = {PLAIN[square[cell]]: cell for cell in range(25)}
    plain = [where[ch] for ch in text]
    if family == "delay":
        d = rng.randrange(1, length)
        return text, undelay(plain, d), f"delay {d}"
    if family == "nulls":
        p = rng.randrange(2, 15)
        f = rng.randrange(p)
        cipher = []
        source = iter(plain)
        while len(cipher) < _LETTERS:
            cipher.append(rng.randrange(25) if len(cipher) % p == f else next(source))
        kept = len(drop(cipher, p, f))
        return text[:kept], cipher, f"nulls {p}:{f}"
    if family == "rail":
        rails = rng.randrange(2, 15)
        return text, do(plain, _rail_order(length, rails)), f"rail {rails} undone"
    width = rng.randrange(10, 29)
    return text, do(plain, _column_order(length, width)), f"columns {width} undone"


@frozen("dagapeyeff-direction")
def direction_report() -> dict:
    rng = random.Random(_SEED)
    cells = _cells()
    jobs = []
    for family in ("delay", "nulls", "rail", "columns"):
        text, cipher, label = _plant(rng, family, _LETTERS)
        run = transforms(cipher)[label][1][:len(text)]
        jobs.append(("planted", family, label, run, text, rng.randrange(1 << 40)))
    sources = [cells]
    for _ in range(_SHUFFLES):
        mixed = list(cells)
        rng.shuffle(mixed)
        sources.append(mixed)
    for index, source in enumerate(sources):
        for label, (family, run) in transforms(source).items():
            jobs.append((index, family, label, run, None, rng.randrange(1 << 40)))

    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[3], 1, "both", job[5], _RESTARTS, _STEPS)[0]
                                if job[0] != "planted" else anneal(job[3], 1, "both", job[5], _RESTARTS, _STEPS),
                                jobs))

    planted = []
    scores: dict[str, list[float]] = {}
    families: dict[str, str] = {}
    for (index, family, label, run, text, _), result in zip(jobs, results):
        if index == "planted":
            score, letters = result
            planted.append({
                "family": family,
                "transform": label,
                "letters": len(text),
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / len(text), 4),
            })
            continue
        scores.setdefault(label, [None] * len(sources))[index] = round(result, 4)
        families[label] = family

    rows = []
    for label, values in scores.items():
        cell, shuffled = values[0], values[1:]
        spread = statistics.pstdev(shuffled) or 1e-9
        rows.append({
            "transform": label,
            "family": families[label],
            "per_letter": cell,
            "shuffles_as_high": sum(x >= cell for x in shuffled),
            "z": round((cell - statistics.mean(shuffled)) / spread, 2),
        })
    rows.sort(key=lambda row: -row["z"])

    def best(index: int, family: str | None = None) -> float:
        return max(values[index] for label, values in scores.items() if family in (None, families[label]))

    by_family = {}
    for family in ("delay", "nulls", "rail", "columns", None):
        name = family or "all"
        cell_best = best(0, family)
        shuffle_bests = sorted((best(i, family) for i in range(1, len(sources))), reverse=True)
        by_family[name] = {
            "cells_best": cell_best,
            "shuffle_bests": shuffle_bests,
            "shuffle_bests_as_high": sum(x >= cell_best for x in shuffle_bests),
        }
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "transforms": len(scores), "shuffles": _SHUFFLES},
        "planted": planted,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in planted),
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "families": by_family,
        "top": rows[:12],
    }
