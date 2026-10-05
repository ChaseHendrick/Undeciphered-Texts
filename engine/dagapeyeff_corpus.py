"""Real 196-letter passages against the cells' letter counts. Not a reading.

Pelling (Cipher Mysteries, 1 May 2021) proposed sliding a 196-letter window
over a large body of real prose and comparing each window's sorted letter
counts with the cells'. Earlier passes compared the cells with letters drawn
independently at English rates, and 0 of 10,000 such draws were as flat.
Real passages vary more than independent draws: names, repeated words and
topic all move the counts. This pass asks the same question of real text.

Every fourth 196-letter window of the 1,916,398-letter public training file
is counted, with J folded into I. Each window gets the same best-assignment
chi-square the swarm gives the cells (34.23), its number of distinct letters
(the cells use 18) and its largest count (the cells' largest is 20). A window
does not have to be English in any other way. No letter string is stored.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from engine.alphabet import letters_only
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import ENGLISH_25, best_chi_square, challenge_pairs

_PUBLIC = Path(__file__).resolve().parent / "data" / "neural_train_public.txt"
_WIDTH = 196
_STRIDE = 4


def _window_counts(ints: np.ndarray) -> np.ndarray:
    starts = np.arange(0, len(ints) - _WIDTH + 1, _STRIDE)
    counts = np.zeros((len(starts), 25), dtype=np.int16)
    for letter in range(25):
        running = np.concatenate([[0], np.cumsum(ints == letter, dtype=np.int32)])
        counts[:, letter] = running[starts + _WIDTH] - running[starts]
    return counts


def _best_chi(counts: np.ndarray) -> np.ndarray:
    rates = np.sort(np.asarray(ENGLISH_25))[::-1] * _WIDTH
    ordered = -np.sort(-counts.astype(np.float64), axis=1)
    return (((ordered - rates) ** 2) / rates).sum(axis=1)


@frozen("dagapeyeff-corpus")
def corpus_report() -> dict:
    text = letters_only(_PUBLIC.read_text(encoding="utf-8")).replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    ints = np.frombuffer(text.encode("ascii"), dtype=np.uint8).astype(np.int64) - 65
    index = np.full(26, -1, dtype=np.int64)
    for position, letter in enumerate(alphabet):
        index[ord(letter) - 65] = position
    ints = index[ints]
    counts = _window_counts(ints)
    chi = _best_chi(counts)
    distinct = (counts > 0).sum(axis=1)
    largest = counts.max(axis=1)
    cells = challenge_pairs()
    cell_chi = best_chi_square(cells)
    cell_distinct = len(set(cells))
    cell_largest = max(cells.count(cell) for cell in set(cells))
    cell_sorted = sorted((cells.count(cell) for cell in set(cells)), reverse=True) + [0] * (25 - cell_distinct)
    window_sorted = -np.sort(-counts.astype(np.int64), axis=1)
    distance = np.abs(window_sorted - np.asarray(cell_sorted)).sum(axis=1)
    as_flat = chi >= cell_chi
    narrow = distinct <= cell_distinct
    low_top = largest <= cell_largest
    return {
        "solved": False,
        "claimed_plaintext": None,
        "corpus_letters": len(text),
        "windows": int(len(counts)),
        "stride": _STRIDE,
        "cell_chi_square": round(cell_chi, 2),
        "windows_as_flat": int(as_flat.sum()),
        "window_chi_max": round(float(chi.max()), 2),
        "window_chi_median": round(float(np.median(chi)), 2),
        "cell_distinct": cell_distinct,
        "windows_as_narrow": int(narrow.sum()),
        "cell_largest": cell_largest,
        "windows_top_as_low": int(low_top.sum()),
        "windows_all_three": int((as_flat & narrow & low_top).sum()),
        "closest_sorted_distance": int(distance.min()),
        "median_sorted_distance": int(np.median(distance)),
        "scope": (
            "Real prose windows, counted with the swarm's own statistic. A window that matches the "
            "counts is not the plaintext, and a transposition cannot change counts. No letter string is stored."
        ),
    }
