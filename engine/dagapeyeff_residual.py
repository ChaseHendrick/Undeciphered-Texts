"""Order scores with the rare cells left in place. Not a reading.

Cells that appear at most three times stay in their seats. The other cells
are shuffled. Seven scores were fixed before the draws. The solved exercise
is scored with nothing pinned, so a real reading order can still show. No
letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs

_SEED = 20261004
_DRAWS = 10000
_NAMES = ("adjacent", "lag", "step", "run", "knight", "gap", "trigram")


def _repeated(seq: list[str]) -> int:
    grams: dict[tuple[str, ...], int] = {}
    for index in range(len(seq) - 2):
        key = (seq[index], seq[index + 1], seq[index + 2])
        grams[key] = grams.get(key, 0) + 1
    return sum(count > 1 for count in grams.values())


def _score(seq: list[str], mode: str, row_keys: str, column_keys: str) -> tuple[int, ...]:
    length = len(seq)
    adjacent = sum(seq[index] == seq[index + 1] for index in range(length - 1))
    lag = max(
        sum(seq[index] == seq[index + shift] for index in range(length - shift))
        for shift in range(1, 14)
    )
    steps: dict[tuple[str, str], int] = {}
    knight = 0
    for index in range(length - 1):
        pair = (seq[index][1], seq[index + 1][1])
        steps[pair] = steps.get(pair, 0) + 1
        row_step = abs(row_keys.index(seq[index][0]) - row_keys.index(seq[index + 1][0]))
        column_step = abs(column_keys.index(seq[index][1]) - column_keys.index(seq[index + 1][1]))
        knight += (row_step, column_step) in ((1, 2), (2, 1))
    run = 1
    best_run = 1
    for index in range(1, length):
        if seq[index] == seq[index - 1]:
            run += 1
            best_run = max(best_run, run)
        else:
            run = 1
    places = [index for index, cell in enumerate(seq) if cell == mode]
    gaps = [right - left for left, right in zip(places, places[1:])] or [0]
    return (adjacent, lag, max(steps.values()), best_run, knight, max(gaps), _repeated(seq))


def _tails(
    seq: list[str],
    mode: str,
    row_keys: str,
    column_keys: str,
    pinned: set[int],
) -> tuple[tuple[int, ...], list[int], list[int]]:
    observed = _score(seq, mode, row_keys, column_keys)
    free = [index for index in range(len(seq)) if index not in pinned]
    free_cells = [seq[index] for index in free]
    drawn = random.Random(_SEED)
    low = [0] * len(observed)
    high = [0] * len(observed)
    for _ in range(_DRAWS):
        shuffled = free_cells[:]
        drawn.shuffle(shuffled)
        trial = list(seq)
        for index, cell in zip(free, shuffled):
            trial[index] = cell
        got = _score(trial, mode, row_keys, column_keys)
        for index, (mark, value) in enumerate(zip(observed, got)):
            low[index] += value <= mark
            high[index] += value >= mark
    return observed, low, high


def _control_pairs() -> list[str]:
    letters = "".join(char for char in CONTROL if char.isalpha())
    even = len(letters) - (len(letters) % 2)
    return [letters[index:index + 2] for index in range(0, even, 2)]


@frozen("residual")
def residual_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    low_cells = {cell for cell, count in counts.items() if count <= 3}
    pinned = {index for index, cell in enumerate(pairs) if cell in low_cells}
    mode = counts.most_common(1)[0][0]
    observed, low, high = _tails(pairs, mode, "67890", "12345", pinned)
    control = _control_pairs()
    alphabet = "".join(sorted({letter for pair in control for letter in pair}))
    control_mode = Counter(control).most_common(1)[0][0]
    control_observed, control_low, control_high = _tails(control, control_mode, alphabet, alphabet, set())
    scores = []
    best_tail = _DRAWS
    best_name = _NAMES[0]
    for name, mark, low_count, high_count in zip(_NAMES, observed, low, high):
        tail = min(low_count, high_count)
        scores.append({
            "name": name,
            "observed": mark,
            "low": low_count,
            "high": high_count,
            "tail": tail,
        })
        if tail < best_tail:
            best_tail = tail
            best_name = name
    trigram_index = _NAMES.index("trigram")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "draws": _DRAWS,
        "pinned": len(pinned),
        "scores": scores,
        "best_name": best_name,
        "best_tail": best_tail,
        "control_trigram_observed": control_observed[trigram_index],
        "control_trigram_low": control_low[trigram_index],
        "control_trigram_high": control_high[trigram_index],
        "scope": (
            "A residual order score is not a reading. "
            "No letter string is stored."
        ),
    }
