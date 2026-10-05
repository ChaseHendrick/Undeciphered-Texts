"""The book's own square applied to the 1939 cells. Not a reading.

The worked Polybius exercise earlier in the same book has a public plaintext.
Aligning its pairs with that plaintext rebuilds the square it used. If the
challenge reused that square, the cells would become letters with no search
at all, and a transposition could not change their counts. So the counts
are the whole test.

The exercise as transcribed in engine.dagapeyeff_swarm does not align
cleanly. Three plaintext letters have no pair and one pair stands for the
wrong letter. The alignment below skips a plaintext letter when the next two
pairs agree after the skip, and otherwise records a wrong pair without
learning from it. Those faults are reported, not repaired in the
transcription.

The challenge digits are mapped onto the exercise's A to E coordinates in
all 8 ways: row digits 67890 forward or reversed, column digits 12345
forward or reversed, and rows and columns swapped or not. The three square
cells the exercise never uses take G, X and Z in every order. No letter
string is stored.
"""

from __future__ import annotations

import itertools
import random

from engine.alphabet import letters_only
from engine.dagapeyeff_add import _PROSE
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, ENGLISH_25, _pairs, challenge_pairs

_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_COORDS = "ABCDE"
_DRAWS = 2000
_SEED = 20261011


def align_exercise() -> dict:
    """Rebuild the exercise square. Returns the square and the alignment faults."""
    pairs = _pairs(CONTROL, _COORDS)
    plain = letters_only(_PROSE).replace("J", "I")
    square: dict[str, str] = {}
    letter_of: dict[str, str] = {}

    def fits(pair: str, letter: str) -> bool:
        return square.get(pair, letter) == letter and letter_of.get(letter, pair) == pair

    dropped: list[int] = []
    wrong: list[int] = []
    i = j = 0
    while i < len(pairs) and j < len(plain):
        if fits(pairs[i], plain[j]):
            square[pairs[i]] = plain[j]
            letter_of[plain[j]] = pairs[i]
            i += 1
            j += 1
            continue
        if (j + 2 < len(plain) and i + 1 < len(pairs)
                and fits(pairs[i], plain[j + 1]) and fits(pairs[i + 1], plain[j + 2])):
            dropped.append(j)
            j += 1
            continue
        wrong.append(i)
        i += 1
        j += 1
    dropped.extend(range(j, len(plain)))
    return {
        "square": square,
        "pairs": len(pairs),
        "plaintext_letters": len(plain),
        "dropped": dropped,
        "wrong": wrong,
    }


def _chi(counts: dict[str, int], total: int) -> float:
    score = 0.0
    for letter, rate in zip(_ALPHABET, ENGLISH_25):
        expected = total * rate
        observed = counts.get(letter, 0)
        score += (observed - expected) ** 2 / expected
    return score


def _labelings():
    rows, columns = "67890", "12345"
    for row_reversed, column_reversed, swapped in itertools.product((False, True), repeat=3):
        row_digits = rows[::-1] if row_reversed else rows
        column_digits = columns[::-1] if column_reversed else columns
        yield (row_reversed, column_reversed, swapped), row_digits, column_digits


@frozen("dagapeyeff-booksquare")
def booksquare_report() -> dict:
    aligned = align_exercise()
    square = aligned["square"]
    missing_cells = [r + c for r in _COORDS for c in _COORDS if r + c not in square]
    missing_letters = [letter for letter in _ALPHABET if letter not in square.values()]
    exercise_counts: dict[str, int] = {}
    for pair in _pairs(CONTROL, _COORDS):
        if pair in square:
            exercise_counts[square[pair]] = exercise_counts.get(square[pair], 0) + 1
    exercise_chi = _chi(exercise_counts, sum(exercise_counts.values()))

    cells = challenge_pairs()
    labelings = []
    for flags, row_digits, column_digits in _labelings():
        coordinates = []
        for pair in cells:
            row = _COORDS[row_digits.index(pair[0])]
            column = _COORDS[column_digits.index(pair[1])]
            coordinates.append(column + row if flags[2] else row + column)
        best = None
        for fill in itertools.permutations(missing_letters):
            filled = dict(square)
            filled.update(zip(missing_cells, fill))
            counts: dict[str, int] = {}
            for coordinate in coordinates:
                counts[filled[coordinate]] = counts.get(filled[coordinate], 0) + 1
            score = _chi(counts, len(coordinates))
            if best is None or score < best[0]:
                best = (score, len(counts))
        labelings.append({
            "rows_reversed": flags[0],
            "columns_reversed": flags[1],
            "swapped": flags[2],
            "chi_square": round(best[0], 2),
            "distinct_letters": best[1],
        })

    drawn = random.Random(_SEED)
    draws = []
    exercise_draws = []
    for _ in range(_DRAWS):
        sample = drawn.choices(_ALPHABET, weights=ENGLISH_25, k=len(cells))
        counts: dict[str, int] = {}
        for letter in sample:
            counts[letter] = counts.get(letter, 0) + 1
        draws.append(_chi(counts, len(cells)))
        short = drawn.choices(_ALPHABET, weights=ENGLISH_25, k=sum(exercise_counts.values()))
        short_counts: dict[str, int] = {}
        for letter in short:
            short_counts[letter] = short_counts.get(letter, 0) + 1
        exercise_draws.append(_chi(short_counts, len(short)))
    best_labeling = min(row["chi_square"] for row in labelings)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "exercise_pairs": aligned["pairs"],
        "exercise_plaintext_letters": aligned["plaintext_letters"],
        "exercise_dropped_letters": len(aligned["dropped"]),
        "exercise_wrong_pairs": len(aligned["wrong"]),
        "square_cells_known": len(square),
        "square_cells_unused": len(missing_cells),
        "exercise_chi_square": round(exercise_chi, 2),
        "exercise_draws_as_high": sum(score >= exercise_chi for score in exercise_draws),
        "labelings": labelings,
        "best_chi_square": best_labeling,
        "english_draws": _DRAWS,
        "english_chi_max": round(max(draws), 2),
        "english_draws_as_high_as_best": sum(score >= best_labeling for score in draws),
        "scope": (
            "The book's own square, under every digit labeling, does not give English letter counts. "
            "A transposition cannot change counts. Not a reading. No letter string is stored."
        ),
    }
