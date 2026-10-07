"""What could the five last-column symbols be? Not a reading.

Five symbols (cells 92, 93, 04, 71, 94; 8 cells in all) occur only in the last
column of the 14 by 14 grid, which is the last cell of each printed line
(Undeciphered-Texts, docs/logs/dagapeyeff-private-2026-10-04.md: 0 of 20,000
shuffles). This pass tests the two readings that can be tested from the digits.

1. Padding (nulls). Without the eight cells, 188 cells use 13 symbols. Counted:
   the fewest different letters in any 188-letter window of Latin and English.
2. Real rare letters. Counted: how often a 196-letter window has five or more
   letters used at most three times, and how often all uses of those letters
   (at least 8) lie inside one 14-letter stretch, which is what a transposition
   turning the last column into a contiguous run of plaintext would need.

Windows are taken every 7 letters (count 1) or 97 letters (count 2). Only
counts are stored. No letter string is stored.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

_ROOT = Path(os.environ.get("UNDECIPHERED_TEXTS",
                            Path(__file__).resolve().parents[2] / "chasehendrick" / "undeciphered-texts"))
sys.path.insert(0, str(_ROOT))

from engine.dagapeyeff_add import _cells  # noqa: E402
from engine.dagapeyeff_foursquare import _HELD, _held  # noqa: E402
from engine.dagapeyeff_latin import texts  # noqa: E402

SIDE = 14
N = 196


def private_symbols(cells: list[int]) -> list[int]:
    return sorted(s for s in set(cells) if all(i % SIDE == SIDE - 1 for i, x in enumerate(cells) if x == s))


def distinct_letters(text: str, length: int, stride: int = 7) -> dict:
    counts = [len(set(text[s:s + length])) for s in range(0, len(text) - length, stride)]
    return {"windows": len(counts), "fewest": min(counts), "median": sorted(counts)[len(counts) // 2],
            "at_most_13": sum(c <= 13 for c in counts)}


def rare_letters(text: str, stride: int = 97) -> dict:
    windows = five_rare = packed = 0
    for s in range(0, len(text) - N, stride):
        window = text[s:s + N]
        counts = Counter(window)
        rare = {ch for ch, n in counts.items() if n <= 3}
        windows += 1
        five_rare += len(rare) >= 5
        places = [i for i, ch in enumerate(window) if ch in rare]
        if len(places) >= 8 and max(places) - min(places) < SIDE:
            packed += 1
    return {"windows": windows, "five_or_more_rare": five_rare, "rare_in_one_14_stretch": packed}


def report() -> dict:
    cells = _cells()
    private = private_symbols(cells)
    rest = [x for x in cells if x not in private]
    corpora = {"Latin, Aquinas (ITTB, first 600,000 letters)": texts()["train"][:600_000],
               "Latin, classical (Perseus)": texts()["classical"],
               "English (held-out)": "".join(_held(name) for name in _HELD)[:600_000]}
    return {
        "solved": False, "claimed_plaintext": None,
        "private_symbols": private, "private_cells": len(cells) - len(rest),
        "last_column_private": sum(cells[r * SIDE + SIDE - 1] in private for r in range(SIDE)),
        "symbols": len(set(cells)), "symbols_without_private": len(set(rest)), "cells_without_private": len(rest),
        "padding_test": {name: distinct_letters(text, len(rest)) for name, text in corpora.items()},
        "rare_letter_test": {name: rare_letters(text) for name, text in corpora.items()},
    }


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "results" / "rare_column.json"
    result = report()
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))
