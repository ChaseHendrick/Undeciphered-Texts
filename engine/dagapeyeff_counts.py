"""The rare counts sit in order on the square. Not a reading.

One symbol appears three times, one appears twice, and three appear once.
On the 5 by 5 square those counts can sit equally spaced along a row or a
column, in either order, with a step of one or two. Both steps are every
gap that fits. No letter string is stored.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_ROWS = "67890"
_COLS = "12345"
_PLACEMENTS = 25 * 24 * 1771  # C(23, 3) = 1771


def _index(cell: str) -> int:
    return _ROWS.index(cell[0]) * 5 + _COLS.index(cell[1])


def _ordered(count_three: int, count_two: int, singles: tuple[int, ...]) -> bool:
    labels = {count_three: 3, count_two: 2}
    for seat in singles:
        labels[seat] = 1
    for axis in (0, 1):
        for fixed in range(5):
            line = [None] * 5
            for offset in range(5):
                row, column = (offset, fixed) if axis else (fixed, offset)
                line[offset] = labels.get(row * 5 + column)
            for step in (1, 2):
                for start in range(5):
                    window = []
                    for k in range(3):
                        seat = start + k * step
                        if seat >= 5:
                            window = None
                            break
                        window.append(line[seat])
                    if window in ([3, 2, 1], [1, 2, 3]):
                        return True
    return False


def _observed() -> dict:
    counts = Counter(challenge_pairs())
    by_count: dict[int, list[str]] = {}
    for cell, count in counts.items():
        by_count.setdefault(count, []).append(cell)
    three = by_count[3]
    two = by_count[2]
    one = by_count[1]
    return {
        "three": sorted(three),
        "two": sorted(two),
        "one": sorted(one),
        "ordered": _ordered(_index(three[0]), _index(two[0]), tuple(_index(cell) for cell in one)),
    }


def _favorable() -> int:
    found = 0
    for count_three in range(25):
        for count_two in range(25):
            if count_two == count_three:
                continue
            rest = [seat for seat in range(25) if seat not in (count_three, count_two)]
            for singles in combinations(rest, 3):
                if _ordered(count_three, count_two, singles):
                    found += 1
    return found


@frozen("counts")
def counts_report() -> dict:
    observed = _observed()
    favorable = _favorable()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "three": observed["three"],
        "two": observed["two"],
        "one": observed["one"],
        "ordered": observed["ordered"],
        "favorable": favorable,
        "placements": _PLACEMENTS,
        "allowed": observed["ordered"] and favorable / _PLACEMENTS < 0.05,
        "scope": "Counts in order on the square are not a reading. No letter string is stored.",
    }
