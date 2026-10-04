"""One thousand pre-specified attacks on the 1939 cells. Not a reading.

Each attack is a number. Two kinds of shuffle score it: stirring the order
of the cells, and re-pairing the two digits while keeping their totals.
A hit is a score no shuffled copy reached. With this many attacks, a few
hits are the ordinary price of looking. No letter string is stored.
"""

from __future__ import annotations

import math
import random
from collections import Counter

from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261004
_SHUFFLES = 500
_ATTACKS = 1000
_ROW = "67890"
_COLUMN = "12345"
_WIDTHS = range(2, 42)
_THRESHOLDS = range(1, 6)
_WINDOWS = (7, 14, 21, 28, 35, 49, 56, 70, 98, 112)


def _indexes(pairs: list[str]) -> tuple[list[int], list[int]]:
    return (
        [_ROW.index(pair[0]) for pair in pairs],
        [_COLUMN.index(pair[1]) for pair in pairs],
    )


def _abs_corr(left: list[int], right: list[int]) -> float:
    count = len(left)
    if count < 2:
        return 0.0
    mean_left = sum(left) / count
    mean_right = sum(right) / count
    var_left = 0.0
    var_right = 0.0
    cov = 0.0
    for one, two in zip(left, right):
        var_left += (one - mean_left) ** 2
        var_right += (two - mean_right) ** 2
        cov += (one - mean_left) * (two - mean_right)
    if var_left <= 0.0 or var_right <= 0.0:
        return 0.0
    return abs(cov / math.sqrt(var_left * var_right))


def _repeat_rate(symbols: list[int]) -> float:
    if len(symbols) < 2:
        return 0.0
    hits = sum(symbols[index] == symbols[index + 1] for index in range(len(symbols) - 1))
    return hits / (len(symbols) - 1)


def attacks(pairs: list[str]) -> list[float]:
    """One thousand scores. Higher means the chosen kind of structure."""
    count = len(pairs)
    rows = [pair[0] for pair in pairs]
    columns = [pair[1] for pair in pairs]
    row_index, column_index = _indexes(pairs)
    scores = [0.0] * _ATTACKS
    for lag in range(1, 101):
        width = count - lag
        pair_hits = 0
        row_hits = 0
        column_hits = 0
        for index in range(width):
            if pairs[index] == pairs[index + lag]:
                pair_hits += 1
            if rows[index] == rows[index + lag]:
                row_hits += 1
            if columns[index] == columns[index + lag]:
                column_hits += 1
        scores[lag - 1] = pair_hits / width
        scores[100 + lag - 1] = row_hits / width
        scores[200 + lag - 1] = column_hits / width
    totals = Counter(pairs)
    slot = 300
    for width in _WIDTHS:
        tallies = [Counter() for _ in range(width)]
        for index, pair in enumerate(pairs):
            if totals[pair] <= 5:
                tallies[index % width][pair] += 1
        for threshold in _THRESHOLDS:
            best = 0
            for column in range(width):
                piled = sum(seen for symbol, seen in tallies[column].items() if totals[symbol] <= threshold)
                if piled > best:
                    best = piled
            scores[slot] = float(best)
            slot += 1
    for length in _WINDOWS:
        for start in range(20):
            # Fewer distinct cells is the structure direction, so store the negative.
            scores[slot] = -float(len(set(pairs[start:start + length])))
            slot += 1
    for lag in range(100):
        scores[slot] = _abs_corr(row_index[:count - lag], column_index[lag:])
        slot += 1
    for period in range(2, 102):
        kept = [row_index[index] * 5 + column_index[index] for index in range(count) if index % period]
        scores[slot] = _repeat_rate(kept)
        slot += 1
    for key in range(99):
        dr = key % 5
        dc = (key // 5) % 5
        dr2 = (key // 25) % 2
        dc2 = (key // 50) % 2
        shifted = []
        for index, (row, column) in enumerate(zip(row_index, column_index)):
            if index % 2:
                shifted.append(((row - dr2) % 5) * 5 + (column - dc2) % 5)
            else:
                shifted.append(((row - dr) % 5) * 5 + (column - dc) % 5)
        scores[slot] = _repeat_rate(shifted)
        slot += 1
    joint = Counter(pairs)
    row_totals = Counter(rows)
    column_totals = Counter(columns)
    association = 0.0
    for row, row_count in row_totals.items():
        for column, column_count in column_totals.items():
            expected = row_count * column_count / count
            seen = joint.get(row + column, 0)
            association += (seen - expected) ** 2 / expected
    scores[slot] = association
    slot += 1
    if slot != _ATTACKS:
        raise RuntimeError(f"expected {_ATTACKS} attacks, built {slot}")
    return scores


def _family(index: int) -> str:
    if index < 300:
        return "lag"
    if index < 500:
        return "pile"
    if index < 700:
        return "window"
    if index < 800:
        return "cross"
    if index < 900:
        return "deletion"
    if index < 999:
        return "shift"
    return "association"


def _pile_label(index: int) -> str:
    offset = index - 300
    width = 2 + offset // 5
    threshold = 1 + offset % 5
    return f"width {width}, at most {threshold}"


def _structure_tail(real: list[float], copies: list[list[float]]) -> list[int]:
    tails = [0] * _ATTACKS
    for copy in copies:
        for index, value in enumerate(copy):
            if value >= real[index] - 1e-12:
                tails[index] += 1
    return tails
    tails = [0] * _ATTACKS
    for copy in copies:
        for index, value in enumerate(copy):
            if value >= real[index] - 1e-12:
                tails[index] += 1
    return tails


def battery_report() -> dict:
    pairs = list(challenge_pairs())
    real = attacks(pairs)
    drawn = random.Random(_SEED)
    order_copies = []
    repair_copies = []
    for _ in range(_SHUFFLES):
        ordered = pairs[:]
        drawn.shuffle(ordered)
        order_copies.append(attacks(ordered))
        columns = [pair[1] for pair in pairs]
        drawn.shuffle(columns)
        repaired = [pair[0] + column for pair, column in zip(pairs, columns)]
        repair_copies.append(attacks(repaired))
    order_tail = _structure_tail(real, order_copies)
    repair_tail = _structure_tail(real, repair_copies)
    order_hits = tuple(index for index, tail in enumerate(order_tail) if tail == 0)
    repair_hits = tuple(index for index, tail in enumerate(repair_tail) if tail == 0)
    repair_families: dict[str, int] = {}
    for index in repair_hits:
        name = _family(index)
        repair_families[name] = repair_families.get(name, 0) + 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "attacks": _ATTACKS,
        "shuffles": _SHUFFLES,
        "trials": _ATTACKS * _SHUFFLES * 2,
        "order_hits": order_hits,
        "order_hit_labels": tuple(_pile_label(index) for index in order_hits),
        "repair_hit_count": len(repair_hits),
        "repair_families": repair_families,
        "lag1_pair_tail": order_tail[0],
        "pile_14_tail": order_tail[361],
        "association_order_tail": order_tail[999],
        "association_repair_tail": repair_tail[999],
        "scope": (
            "A hit means no shuffled copy matched that one score. "
            "It does not name a letter or a reading. No letter string is stored."
        ),
    }
