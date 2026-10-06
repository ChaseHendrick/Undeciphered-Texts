"""Any one-to-one pair cipher keeps the number of different pairs. Not a reading.

A cipher that sends each plaintext pair to one cipher pair, the same way every
time, cannot change how many different pairs a text uses. Four-square,
two-square, Playfair after its padding, a 2 by 2 Hill matrix and a keyed table
of 625 pairs all work this way, whatever the key. So the cells' count of
different pairs has to be one that real prose of the same length reaches.

Every fourth 196-letter window of the 1,916,398-letter public training file is
counted, with J folded into I, at both pair phases: pairs from the first
letter, and pairs from the second with the first and last letters left over.
Four-square with random keys on held-out windows shows the count does not move.
No letter string is stored.
"""

from __future__ import annotations

import random

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_columnar import _regrouped_cells
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, encrypt
from engine.language import _PUBLIC

_WIDTH = 196
_STRIDE = 4
_SEED = 20261006
_KEYED_PER_SOURCE = 67


def different_pairs(run, phase: int) -> int:
    """Different pairs, taking pairs from the first symbol (0) or the second (1)."""
    stop = len(run) - 1 if phase == 0 else len(run) - 2
    return len({(run[k], run[k + 1]) for k in range(phase, stop, 2)})


def _tail(counts: dict[int, int], at_least: int) -> int:
    return sum(windows for count, windows in counts.items() if count >= at_least)


def _kept_by_foursquare() -> dict:
    """Four-square with random squares never changes the count."""
    rng = random.Random(_SEED)
    checked = 0
    moved = 0
    for name in _HELD:
        prose = _held(name)
        for _ in range(_KEYED_PER_SOURCE):
            start = rng.randrange(len(prose) - _WIDTH)
            window = prose[start:start + _WIDTH]
            squares = []
            for _ in range(4):
                square = list(range(25))
                rng.shuffle(square)
                squares.append(square)
            upper_left = "".join(PLAIN[i] for i in squares[2])
            lower_right = "".join(PLAIN[i] for i in squares[3])
            cipher = encrypt(window, squares[0], squares[1], upper_left, lower_right)
            checked += 1
            moved += different_pairs(cipher, 0) != different_pairs(window, 0)
    return {"windows": checked, "count_moved": moved}


@frozen("dagapeyeff-pairmap")
def pairmap_report() -> dict:
    text = letters_only(_PUBLIC.read_text(encoding="utf-8")).replace("J", "I")
    by_phase = {0: {}, 1: {}}
    windows = 0
    for start in range(0, len(text) - _WIDTH + 1, _STRIDE):
        window = text[start:start + _WIDTH]
        windows += 1
        for phase, counts in by_phase.items():
            count = different_pairs(window, phase)
            counts[count] = counts.get(count, 0) + 1
    texts = {}
    for label, run in (("cells", _cells()), ("regrouped", _regrouped_cells())):
        rows = {}
        for phase, counts in by_phase.items():
            count = different_pairs(run, phase)
            rows[f"phase {phase}"] = {
                "different_pairs": count,
                "windows_as_many": _tail(counts, count),
                "windows_as_few": sum(windows for value, windows in counts.items() if value <= count),
            }
        texts[label] = rows
    return {
        "solved": False,
        "claimed_plaintext": None,
        "corpus_letters": len(text),
        "windows": windows,
        "stride": _STRIDE,
        "window_range": {
            f"phase {phase}": [min(counts), max(counts)] for phase, counts in by_phase.items()
        },
        "texts": texts,
        "kept_by_foursquare": _kept_by_foursquare(),
        "scope": (
            "A count every one-to-one pair cipher keeps, for any key. A window with the cells' count is not "
            "the plaintext. A cipher that changes its pairing as it goes, or mixes in nulls, is not covered. "
            "No letter string is stored."
        ),
    }
