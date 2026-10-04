"""Column keys and digit reads on the 1939 grid. Not a reading.

Pair order cannot change letter counts. Digit order can, because it builds
new pairs. This swarm asks whether a column key makes neighbors repeat, and
whether a digit read that stays on the square is any better than ungluing
the digits at random. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_swarm import (
    ENGLISH_25,
    best_chi_square,
    challenge_pairs,
    digram_excess,
)

_SEED = 20261004
_KEYS = 10000
_DRAWS = 10000
_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_ROW = set("67890")
_COLUMN = set("12345")
_WIDTHS = range(2, 29)


def _grid(pairs: list[str]) -> list[list[str]]:
    return [pairs[row * 14:(row + 1) * 14] for row in range(14)]


def _row_read(grid: list[list[str]], order: list[int]) -> tuple[str, ...]:
    return tuple(grid[row][column] for row in range(14) for column in order)


def _down_read(grid: list[list[str]], order: list[int]) -> tuple[str, ...]:
    return tuple(grid[row][column] for column in order for row in range(14))


def _digits(pairs: list[str]) -> str:
    return "".join(pairs)


def _digit_read(digits: str, width: int) -> tuple[str, ...]:
    columns = [[] for _ in range(width)]
    for index, char in enumerate(digits):
        columns[index % width].append(char)
    out = "".join("".join(column) for column in columns)
    return tuple(out[index:index + 2] for index in range(0, len(out) - len(out) % 2, 2))


def _legal(pairs: tuple[str, ...]) -> int:
    return sum(1 for pair in pairs if pair[0] in _ROW and pair[1] in _COLUMN)


def _overlap(source: tuple[str, ...], other: tuple[str, ...]) -> int:
    left = Counter(source)
    right = Counter(other)
    return sum((left & right).values())


def _key_sample(grid: list[list[str]], seed: int) -> dict:
    identity = list(range(14))
    printed = digram_excess(_row_read(grid, identity))
    down = digram_excess(_down_read(grid, identity))
    drawn = random.Random(seed)
    row_at_least = 0
    down_at_least = 0
    row_best = 0
    down_best = 0
    for _ in range(_KEYS):
        order = identity[:]
        drawn.shuffle(order)
        row_score = digram_excess(_row_read(grid, order))
        down_score = digram_excess(_down_read(grid, order))
        row_best = max(row_best, row_score)
        down_best = max(down_best, down_score)
        if row_score >= printed:
            row_at_least += 1
        if down_score >= down:
            down_at_least += 1
    return {
        "printed_digrams": printed,
        "down_digrams": down,
        "row_at_least": row_at_least,
        "down_at_least": down_at_least,
        "row_best": row_best,
        "down_best": down_best,
    }


def _common_concentration(seq: list[str]) -> int:
    counts = Counter(seq)
    columns = [Counter() for _ in range(14)]
    for index, symbol in enumerate(seq):
        if counts[symbol] > 2:
            columns[index % 14][symbol] += 1
    total = 0
    for symbol, count in counts.items():
        if count <= 2:
            continue
        total += max(column[symbol] for column in columns)
    return total


def read_report() -> dict:
    pairs = list(challenge_pairs())
    grid = _grid(pairs)
    main = _key_sample(grid, _SEED)
    replica = _key_sample(grid, 2)
    digits = _digits(pairs)
    source = tuple(pairs)
    widths = []
    legal_widths = []
    for width in _WIDTHS:
        produced = _digit_read(digits, width)
        legal = _legal(produced)
        row = {
            "width": width,
            "legal": legal,
            "overlap": _overlap(source, produced),
        }
        widths.append(row)
        if legal == len(produced):
            legal_widths.append(width)
    width_3 = _digit_read(digits, 3)
    width_3_chi = best_chi_square(width_3)
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    drawn = random.Random(_SEED)
    repair_scores = []
    for _ in range(_DRAWS):
        shuffled = columns[:]
        drawn.shuffle(shuffled)
        repaired = tuple(row + column for row, column in zip(rows, shuffled))
        repair_scores.append(best_chi_square(repaired))
    repair_scores.sort()
    drawn = random.Random(_SEED)
    english_as_flat = 0
    for _ in range(_DRAWS):
        letters = tuple(drawn.choices(_ALPHABET, weights=ENGLISH_25, k=len(pairs)))
        if best_chi_square(letters) >= width_3_chi:
            english_as_flat += 1
    observed_common = _common_concentration(pairs)
    drawn = random.Random(_SEED)
    common_as_high = 0
    for _ in range(_DRAWS):
        shuffled = pairs[:]
        drawn.shuffle(shuffled)
        if _common_concentration(shuffled) >= observed_common:
            common_as_high += 1
    as_good = sum(score <= width_3_chi for score in repair_scores)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trials": _KEYS * 2 + _DRAWS * 3,
        "printed_digrams": main["printed_digrams"],
        "down_digrams": main["down_digrams"],
        "row_keys_at_least_printed": main["row_at_least"],
        "down_keys_at_least_straight": main["down_at_least"],
        "row_best": main["row_best"],
        "down_best": main["down_best"],
        "replica_row_best": replica["row_best"],
        "replica_down_best": replica["down_best"],
        "legal_widths": tuple(legal_widths),
        "width_3_chi": round(width_3_chi, 2),
        "width_3_overlap": _overlap(source, width_3),
        "repair_median_chi": round(repair_scores[_DRAWS // 2], 2),
        "repairs_as_good": as_good,
        "english_as_flat_as_width_3": english_as_flat,
        "even_width_legal": {row["width"]: row["legal"] for row in widths if row["width"] in (2, 4, 14)},
        "common_concentration": observed_common,
        "common_as_high": common_as_high,
        "scope": (
            "Even widths split the row digits from the column digits, so the square dies. "
            "Width 3 stays legal and looks less flat only because the original pairs were unglued. "
            "Random ungluing does the same. No letter string is stored."
        ),
    }
