"""What a reading would have to beat. Not a reading.

The book's own solved square is tried on the challenge in every flip of its
axes. The prose scores are the yardstick. Sorting the cells beats that
yardstick and is still not a message, so the score alone is not the goal.
No letter string is stored.
"""

from __future__ import annotations

import math
from collections import Counter

from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

# The solved exercise in the same book. A dot is a blank in that square.
_SQUARE = ("SDUMI", "FWAOY", "VN.TE", "LHRCQ", "BPK..")
_ROW = "67890"
_COLUMN = "12345"


def _ic(pairs: list[str]) -> float:
    count = len(pairs)
    return sum(seen * (seen - 1) for seen in Counter(pairs).values()) / (count * (count - 1))


def _entropy(pairs: list[str]) -> float:
    count = len(pairs)
    total = 0.0
    for seen in Counter(pairs).values():
        share = seen / count
        total -= share * math.log(share)
    return total


def _apply(pairs: list[str], row_order: str, column_order: str, swap: bool) -> tuple[str, int]:
    letters = []
    blanks = 0
    for pair in pairs:
        row = row_order.index(pair[0])
        column = column_order.index(pair[1])
        if swap:
            row, column = column, row
        letter = _SQUARE[row][column]
        if letter == ".":
            blanks += 1
        letters.append(letter)
    return "".join(letters), blanks


def yardstick_report() -> dict:
    pairs = list(challenge_pairs())
    cipher = successive_information(pairs)
    best_mi = None
    best_blanks = None
    worst_mi = None
    orientations = 0
    for row_order in (_ROW, _ROW[::-1]):
        for column_order in (_COLUMN, _COLUMN[::-1]):
            for swap in (False, True):
                letters, blanks = _apply(pairs, row_order, column_order, swap)
                score = successive_information(list(letters))
                orientations += 1
                if best_mi is None or score > best_mi:
                    best_mi = score
                    best_blanks = blanks
                if worst_mi is None or score < worst_mi:
                    worst_mi = score
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cipher_mi": round(cipher, 4),
        "english_mi": round(successive_information(_prose("english.txt", len(pairs))), 4),
        "german_mi": round(successive_information(_prose("german_excerpt.txt", len(pairs))), 4),
        "sorted_mi": round(successive_information(sorted(pairs)), 4),
        "entropy": round(_entropy(pairs), 4),
        "index_of_coincidence": round(_ic(pairs), 6),
        "book_orientations": orientations,
        "book_best_mi": round(best_mi, 4),
        "book_best_blanks": best_blanks,
        "book_worst_mi": round(worst_mi, 4),
        "scope": (
            "A reading has to be language and it has to regenerate these cells. "
            "Beating a score by sorting, or by passing an index-of-coincidence cutoff, does neither. "
            "No letter string is stored."
        ),
    }
