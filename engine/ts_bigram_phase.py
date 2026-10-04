"""Which letter-pair grid the Truppenschlüssel residue actually repeats.

A two-square cipher pairs letters and repeats a pair only when the plaintext
pair repeats. The designator is five letters, so dropping it shifts the pairs
by one. This module counts repeated pairs on both grids and does not search
a square. solved stays false.
"""

from __future__ import annotations

import random

from engine.german import german_letters, load_training_prose
from engine.ts_close_pairs import (
    ALPHABET,
    DEZPS_KNOWN,
    DSZPZ,
    HOHOX,
    IASRZ_129,
    IASRZ_130,
    SSKFV,
    alignment_matches,
)

TRIALS = 400
SEED = 20261004
MESSAGES = (
    ("IASRZ_129", IASRZ_129),
    ("IASRZ_130", IASRZ_130),
    ("DSZPZ", DSZPZ),
    ("DEZPS", DEZPS_KNOWN),
    ("SSKFV", SSKFV),
    ("HOHOX", HOHOX),
)


def extra_repeats(text: str) -> int:
    """How many paired letters are copies of an earlier pair.

    Pairs start on the first letter. An odd final letter is left over.
    """
    width = len(text) - (len(text) % 2)
    grams = [text[index : index + 2] for index in range(0, width, 2)]
    return len(grams) - len(set(grams))


def _median(values: list[int]) -> int:
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def random_at_least(length: int, copies: int, *, trials: int = TRIALS, seed: int = SEED) -> int:
    """How many random J-free strings repeat pairs at least `copies` times."""
    width = length - (length % 2)
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        text = "".join(rng.choice(ALPHABET) for _ in range(width))
        if extra_repeats(text) >= copies:
            hits += 1
    return hits


def german_repeat_range(length: int) -> dict:
    """Repeat counts of non-overlapping Grimm slices of the same paired length."""
    prose = german_letters(load_training_prose())
    width = length - (length % 2)
    slices = [
        extra_repeats(prose[start : start + width])
        for start in range(0, len(prose) - width, width)
    ]
    if not slices:
        raise ValueError("German excerpt is shorter than the message")
    return {"slices": len(slices), "low": min(slices), "median": _median(slices), "high": max(slices)}


def _phase_row(name: str, text: str, drop_designator: bool) -> dict:
    body = text[5:] if drop_designator else text
    copies = extra_repeats(body)
    return {
        "message": name,
        "drop_designator": drop_designator,
        "length": len(body),
        "extra_repeats": copies,
        "random_at_least": random_at_least(len(body), copies),
        "random_trials": TRIALS,
        "german": german_repeat_range(len(body)),
    }


def alignment_pair_cluster() -> dict:
    """Do the 1735 agreements clump any tighter than the same number of random hits?"""
    left = DSZPZ[5:]
    right = DEZPS_KNOWN[5:]
    hits = alignment_matches(left, right)
    # Rebuild the left-hand match indexes with the same penalties.
    n, m = len(left), len(right)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = -2 * i
        move[i][0] = 1
    for j in range(1, m + 1):
        score[0][j] = -2 * j
        move[0][j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            step = 2 if left[i - 1] == right[j - 1] else -1
            options = (
                (score[i - 1][j - 1] + step, 0),
                (score[i - 1][j] - 2, 1),
                (score[i][j - 1] - 2, 2),
            )
            score[i][j], move[i][j] = max(options)
    i, j = n, m
    matched: list[int] = []
    while i or j:
        step = move[i][j]
        if step == 0:
            if left[i - 1] == right[j - 1]:
                matched.append(i - 1)
            i -= 1
            j -= 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    found = set(matched)
    duos = sum(1 for index in found if index + 1 in found)
    rng = random.Random(SEED)
    null = []
    for _ in range(200):
        pick = set(rng.sample(range(len(left)), hits))
        null.append(sum(1 for index in pick if index + 1 in pick))
    return {
        "alignment_matches": hits,
        "consecutive_duos": duos,
        "null_draws": 200,
        "null_low": min(null),
        "null_median": _median(null),
        "null_high": max(null),
        "tighter_than_null": duos > max(null),
    }


def search_ts_bigram_phase() -> dict:
    """Count repeated pairs on both grids. No plaintext is produced."""
    rows = []
    for name, text in MESSAGES:
        rows.append(_phase_row(name, text, False))
        rows.append(_phase_row(name, text, True))
    return {
        "claimed_plaintext": None,
        "solved": False,
        "rows": rows,
        "alignment": alignment_pair_cluster(),
        "scope": "Repeat counts only. Matching the Grimm range is not a reading and not a square.",
    }
