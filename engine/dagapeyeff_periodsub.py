"""Two or three independent letter alphabets in turn, on the cells. Not a reading.

Vigenere, Beaufort, Porta and Quagmire tie their alphabets together. A
periodic substitution does not: cell i is read with alphabet i mod p, and each
alphabet is any permutation of the 25 letters. Plain substitution (p = 1) is
already closed with shown power. This short attack anneals periods 2 and 3
with the compiled kernel in engine/dagapeyeff_subc.c under the default model
with J folded into I.

Planted held-out texts of 196 letters show the power. Shuffled cells under the
same search are the control, because three free alphabets can make word salad
out of anything. The best letters on the cells are stored as a candidate so a
reader can look at them. A stored candidate is not a reading.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held
from engine.dagapeyeff_subc import anneal

PERIODS = (2, 3)
_LETTERS = 196
_SEED = 20261007
_RESTARTS = 8
_STEPS = 250_000
_SHUFFLES = 20
_RECOVERED = 0.9


def encrypt(text: str, keys: list[list[int]]) -> list[int]:
    """Cell i is letter i under alphabet i mod len(keys)."""
    return [keys[i % len(keys)][PLAIN.index(ch)] for i, ch in enumerate(text)]


def _search(cells: list[int], period: int, seed: int) -> dict:
    return anneal(cells, seed, period=period, restarts=_RESTARTS, steps=_STEPS)


@frozen("dagapeyeff-periodsub")
def periodsub_report() -> dict:
    rng = random.Random(_SEED)
    planted = []
    for period in PERIODS:
        for name in _HELD:
            prose = _held(name)
            start = rng.randrange(len(prose) - _LETTERS)
            text = prose[start:start + _LETTERS]
            keys = []
            for _ in range(period):
                key = list(range(25))
                rng.shuffle(key)
                keys.append(key)
            found = _search(encrypt(text, keys), period, rng.randrange(1 << 40))
            share = sum(a == b for a, b in zip(found["letters"], text)) / _LETTERS
            planted.append({
                "period": period,
                "source": name,
                "found_per_letter": round(found["per_letter"], 4),
                "letters_right": round(share, 4),
            })
    searched = {}
    for label, cells in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        for period in PERIODS:
            best = _search(cells, period, rng.randrange(1 << 40))
            scores = []
            for _ in range(_SHUFFLES):
                mixed = list(cells)
                rng.shuffle(mixed)
                scores.append(round(_search(mixed, period, rng.randrange(1 << 40))["per_letter"], 4))
            score = round(best["per_letter"], 4)
            searched[f"{label} period {period}"] = {
                "per_letter": score,
                "shuffles": sorted(scores, reverse=True),
                "shuffles_as_high": sum(s >= score for s in scores),
                "candidate_letters": best["letters"],
            }
    recovered = [row for row in planted if row["letters_right"] >= _RECOVERED]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "candidates_are_readings": False,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "shuffles": _SHUFFLES},
        "planted": planted,
        "planted_recovered": len(recovered),
        "planted_lowest_found": min(row["found_per_letter"] for row in recovered),
        "searched": searched,
    }
