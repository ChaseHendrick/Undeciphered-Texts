"""Four-square with chosen plain squares can give the cells' side counts. Not a reading.

engine.dagapeyeff_foursquare showed that held-out English never reaches the
cells' side counts (13 and 18 symbols) when the plain squares are standard or
drawn at random. The plain squares are part of the key, though, and a key can
be chosen. This probe climbs the two plain squares of each held-out window
toward the cells' side counts. Where it gets there, the side count cannot
exclude four-square with keyed plain squares, or two-square, whose squares
are all keyed. The four-square search searched standard plain squares only.

No letter string is stored.
"""

from __future__ import annotations

import random

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, encrypt, sides

_SEED = 20261013
_LETTERS = 196
_STEP = 2500
_FIRST = 500
_RESTARTS = 3
_SWAPS = 5000
_TARGET = (13, 18)


def _cost(window: str, upper: list[str], lower: list[str]) -> tuple[int, tuple[int, int]]:
    identity = list(range(25))
    low, high = sorted(sides(encrypt(window, identity, identity, "".join(upper), "".join(lower))))
    return max(0, low - _TARGET[0]) + max(0, high - _TARGET[1]), (low, high)


@frozen("dagapeyeff-fskeyed")
def fskeyed_report() -> dict:
    rng = random.Random(_SEED)
    rows = []
    for name in _HELD:
        prose = _held(name)
        for start in range(_FIRST, len(prose) - _LETTERS, _STEP):
            window = prose[start:start + _LETTERS]
            best = None
            for _ in range(_RESTARTS):
                upper, lower = list(PLAIN), list(PLAIN)
                rng.shuffle(upper)
                rng.shuffle(lower)
                cost, found = _cost(window, upper, lower)
                for _ in range(_SWAPS):
                    square = upper if rng.random() < 0.5 else lower
                    i, j = rng.randrange(25), rng.randrange(25)
                    square[i], square[j] = square[j], square[i]
                    trial, trial_sides = _cost(window, upper, lower)
                    if trial <= cost:
                        cost, found = trial, trial_sides
                    else:
                        square[i], square[j] = square[j], square[i]
                if best is None or cost < best[0]:
                    best = (cost, found)
            rows.append({"source": name, "start": start, "sides": list(best[1]), "reaches": best[0] == 0})
    return {
        "solved": False,
        "claimed_plaintext": None,
        "target": list(_TARGET),
        "search": {"restarts": _RESTARTS, "swaps": _SWAPS},
        "windows": len(rows),
        "reaching": sum(row["reaches"] for row in rows),
        "rows": rows,
    }
