"""The three cells that appear once sit in successive rows. Not a reading.

Those cells are already known to share the last column. This asks only
where in that column they sit. Three distinct rows out of 14 can be
chosen in 364 ways, and 12 of those choices are successive. No letter
string is stored.
"""

from __future__ import annotations

from collections import Counter
from math import comb

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_WIDTH = 14


def _singletons(seq: list[str]) -> list[dict[str, object]]:
    counts = Counter(seq)
    found = []
    for index, cell in enumerate(seq):
        if counts[cell] != 1:
            continue
        row, column = divmod(index, _WIDTH)
        found.append({"cell": cell, "row": row, "column": column})
    return found


def _successive(rows: list[int]) -> bool:
    ordered = sorted(rows)
    return ordered[-1] - ordered[0] == len(ordered) - 1


@frozen("successive")
def successive_report() -> dict:
    found = _singletons(list(challenge_pairs()))
    rows = [item["row"] for item in found]
    choices = comb(_WIDTH, len(rows))
    successive = _WIDTH - len(rows) + 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": found,
        "rows": sorted(rows),
        "successive": _successive(rows),
        "choices": choices,
        "successive_choices": successive,
        "allowed": successive / choices < 0.05 and _successive(rows),
        "scope": "Successive rows in the private column are not a reading. No letter string is stored.",
    }
