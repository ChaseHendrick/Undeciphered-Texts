"""What could the five last-column symbols be? Two readings counted. Not a reading.

Five symbols, eight cells in all, occur only in the last column of the 14 by
14 grid (docs/logs/dagapeyeff-private-2026-10-04.md). Two readings can be
tested from the digits and the corpora alone.

1. Padding (nulls). Without the eight cells, 188 cells use 13 symbols. Under a
   one-to-one key the message would use 13 letters. Counted: the fewest
   different letters in any window of 188 letters, every 7th letter.
2. Real rare letters. Their counts (3, 2, 1, 1, 1) look ordinary. Counted, in
   windows of 196 letters every 97th letter: how many have five or more
   letters used at most three times, and how many have every use of those
   letters (at least eight) inside one 14-letter stretch. A transposition
   that turns the last column into one run of plaintext would need that.

A third reading, a habit of the maker or the printer at line ends, cannot be
tested from the digits. Only counts are stored. No letter string is stored.
"""

from __future__ import annotations

from collections import Counter

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import _HELD, _held
from engine.dagapeyeff_latin import texts

SIDE = 14
_LETTERS = 196
_STRIDE_DISTINCT = 7
_STRIDE_RARE = 97
_RARE_AT_MOST = 3
_LATIN_LETTERS = 600_000


def private_symbols(cells: list[int]) -> list[int]:
    """Symbols found only in the last column of the 14 by 14 grid."""
    return sorted(s for s in set(cells) if all(i % SIDE == SIDE - 1 for i, x in enumerate(cells) if x == s))


def distinct_letters(text: str, length: int) -> dict:
    counts = [len(set(text[s:s + length])) for s in range(0, len(text) - length + 1, _STRIDE_DISTINCT)]
    return {"windows": len(counts), "fewest": min(counts), "median": sorted(counts)[len(counts) // 2],
            "at_most": sum(c <= 13 for c in counts)}


def rare_letters(text: str, uses: int) -> dict:
    windows = enough = packed = 0
    for s in range(0, len(text) - _LETTERS + 1, _STRIDE_RARE):
        window = text[s:s + _LETTERS]
        counts = Counter(window)
        rare = {ch for ch, k in counts.items() if k <= _RARE_AT_MOST}
        windows += 1
        enough += len(rare) >= 5
        places = [i for i, ch in enumerate(window) if ch in rare]
        packed += len(places) >= uses and max(places) - min(places) < SIDE
    return {"windows": windows, "five_or_more_rare": enough, "rare_in_one_stretch": packed}


def corpora() -> dict[str, str]:
    out = {"Latin, Thomas Aquinas (UD_Latin-ITTB, first 600,000 letters)": texts()["train"][:_LATIN_LETTERS],
           "Latin, classical (UD_Latin-Perseus)": texts()["classical"]}
    for name in _HELD:
        out[f"English, {name.removesuffix('.txt')}"] = _held(name)
    return out


@frozen("dagapeyeff-rarecolumn")
def rarecolumn_report() -> dict:
    cells = _cells()
    private = private_symbols(cells)
    rest = [x for x in cells if x not in private]
    counts = Counter(cells)
    text = corpora()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "private_symbols": private,
        "private_counts": sorted((counts[s] for s in private), reverse=True),
        "private_cells": len(cells) - len(rest),
        "last_column_private": sum(cells[r * SIDE + SIDE - 1] in private for r in range(SIDE)),
        "symbols": len(counts),
        "symbols_without_private": len(set(rest)),
        "cells_without_private": len(rest),
        "padding": {name: distinct_letters(t, len(rest)) for name, t in text.items()},
        "rare_letters": {name: rare_letters(t, len(cells) - len(rest)) for name, t in text.items()},
    }
