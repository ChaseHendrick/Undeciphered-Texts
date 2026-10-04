"""Wider swarm on the 1939 D'Agapeyeff challenge. Still not a reading.

The pair grid is fixed by engine.dagapeyeff_swarm. This pass asks three
questions that a transposition cannot answer: whether some other 25-letter
merger fits the counts, whether the printed groups were copied out of
order, and whether the cells repeat on a period. Workers cover disjoint
slices of the same search. No slice is allowed to return plaintext.
"""

from __future__ import annotations

import itertools
import random
from collections import Counter

from engine.dagapeyeff_swarm import (
    CHALLENGE,
    CONTROL,
    _ROW,
    _COLUMN,
    best_chi_square,
    challenge_pairs,
)
from engine.language import UNIGRAM

# Wikipedia "Letter frequency", the A-Z text percentages, 4 October 2026.
# Scaled to 1 after the caller merges or drops a letter. Not a corpus we hold.
_PERCENT = {
    "french": (
        7.636, 0.901, 3.260, 3.669, 14.715, 1.066, 0.866, 0.937, 7.529, 0.813,
        0.074, 5.456, 2.968, 7.095, 5.796, 2.521, 1.362, 6.693, 7.948, 7.244,
        6.311, 1.838, 0.049, 0.427, 0.708, 0.326,
    ),
    "german": (
        6.516, 1.886, 2.732, 5.076, 16.396, 1.656, 3.009, 4.577, 6.550, 0.268,
        1.417, 3.437, 2.534, 9.776, 2.594, 0.670, 0.018, 7.003, 7.270, 6.154,
        4.166, 0.846, 1.921, 0.034, 0.039, 1.134,
    ),
    "spanish": (
        11.525, 2.215, 4.019, 5.010, 13.702, 0.692, 1.768, 1.973, 6.247, 0.493,
        0.026, 4.967, 3.157, 6.712, 8.683, 2.510, 0.877, 6.871, 7.977, 4.632,
        3.927, 1.138, 0.027, 0.515, 1.433, 0.467,
    ),
    "italian": (
        11.745, 0.927, 4.501, 3.736, 11.792, 1.153, 1.644, 0.136, 10.143, 0.011,
        0.009, 6.510, 2.512, 6.883, 9.832, 3.056, 0.505, 6.367, 4.981, 5.623,
        2.813, 2.097, 0.033, 0.008, 0.020, 1.181,
    ),
    "portuguese": (
        14.634, 1.043, 3.882, 4.992, 13.101, 1.023, 1.303, 1.281, 6.186, 0.379,
        0.015, 2.779, 4.738, 4.446, 9.735, 2.523, 1.204, 6.530, 6.805, 4.336,
        3.639, 1.575, 0.037, 0.453, 0.006, 0.470,
    ),
    "dutch": (
        7.49, 1.58, 1.24, 5.93, 18.91, 0.81, 3.40, 2.38, 6.50, 1.46,
        2.25, 3.57, 2.21, 10.03, 6.06, 1.57, 0.009, 6.41, 3.73, 6.79,
        1.99, 2.85, 1.52, 0.036, 0.035, 1.39,
    ),
}
_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_SEED = 20261004
_NULL_DRAWS = 200
_PERIODS = range(2, 50)
_WORKER_COUNT = 200


def _rates(language: str) -> tuple[float, ...]:
    if language == "english":
        raw = UNIGRAM
    else:
        raw = tuple(value / 100 for value in _PERCENT[language])
    scale = sum(raw)
    return tuple(value / scale for value in raw)


def _chi(counts: list[int], rates: tuple[float, ...]) -> float:
    """Best assignment of unlabeled counts to a 25-way rate vector."""
    if len(rates) != 25:
        raise ValueError("a 5 by 5 square has 25 cells")
    ordered = sorted(counts, reverse=True)
    if len(ordered) > 25:
        raise ValueError("more counts than cells")
    ordered = ordered + [0] * (25 - len(ordered))
    expected_order = sorted(rates, reverse=True)
    total = sum(ordered)
    score = 0.0
    for count, rate in zip(ordered, expected_order):
        expected = total * rate
        score += (count - expected) ** 2 / expected
    return score


def _shape(rates26: tuple[float, ...], keep: tuple[int, ...]) -> tuple[float, ...]:
    """Merge or drop down to the indexes in keep. The first of a merged pair holds the sum."""
    chosen = []
    for index in keep:
        chosen.append(rates26[index])
    # keep lists the surviving letter. A merged partner is absent; its mass was added by the caller.
    scale = sum(chosen)
    return tuple(value / scale for value in chosen)


def hypotheses(language: str) -> list[tuple[str, tuple[float, ...]]]:
    """Every way to force 26 letters into 25 cells: merge a pair, or drop one."""
    rates = _rates(language)
    found = []
    for left, right in itertools.combinations(range(26), 2):
        merged = list(rates)
        merged[left] += merged[right]
        keep = tuple(index for index in range(26) if index != right)
        label = "merge " + _LETTERS[left] + _LETTERS[right]
        found.append((label, _shape(tuple(merged), keep)))
    for dropped in range(26):
        keep = tuple(index for index in range(26) if index != dropped)
        found.append(("drop " + _LETTERS[dropped], _shape(rates, keep)))
    return found


def _observed_counts() -> list[int]:
    return list(Counter(challenge_pairs()).values())


def language_slice(worker: int, workers: int = _WORKER_COUNT) -> dict:
    """One worker's share of the merger search, for every sourced language."""
    if not 0 <= worker < workers:
        raise ValueError("worker id is outside the swarm")
    observed = _observed_counts()
    best = None
    checked = 0
    for language in ("english", *tuple(_PERCENT)):
        for index, (label, rates) in enumerate(hypotheses(language)):
            if index % workers != worker:
                continue
            checked += 1
            score = _chi(observed, rates)
            if best is None or score < best[0]:
                best = (score, language, label)
    return {"worker": worker, "checked": checked, "best_chi": round(best[0], 2), "language": best[1], "rule": best[2]}


def merger_null(draws: int = _NULL_DRAWS) -> dict:
    """How often real English, allowed its best merger, scores as badly as the challenge.

    Counts are unlabeled on both sides. A merger is applied before the score,
    so a 26-letter sample is never asked to fill 26 cells of a 25-cell square.
    """
    observed = _observed_counts()
    tables = {language: hypotheses(language) for language in ("english", *tuple(_PERCENT))}
    challenge_best = None
    challenge_rule = None
    for language, rows in tables.items():
        for label, rates in rows:
            score = _chi(observed, rates)
            if challenge_best is None or score < challenge_best:
                challenge_best = score
                challenge_rule = (language, label)
    drawn = random.Random(_SEED)
    wins = 0
    null_best = []
    cached = [(language, label, rates) for language, rows in tables.items() for label, rates in rows]
    for _ in range(draws):
        base = [0] * 26
        for letter in drawn.choices(range(26), weights=_rates("english"), k=196):
            base[letter] += 1
        friendly = None
        for language, label, rates in cached:
            if label.startswith("merge "):
                left = _LETTERS.index(label[-2])
                right = _LETTERS.index(label[-1])
                counts = []
                for index in range(26):
                    if index == right:
                        continue
                    if index == left:
                        counts.append(base[left] + base[right])
                    else:
                        counts.append(base[index])
            else:
                dropped = _LETTERS.index(label[-1])
                counts = [base[index] for index in range(26) if index != dropped]
            score = _chi(counts, rates)
            if friendly is None or score < friendly:
                friendly = score
        null_best.append(friendly)
        if friendly >= challenge_best:
            wins += 1
    return {
        "hypotheses": len(cached),
        "challenge_best_chi": round(challenge_best, 2),
        "challenge_language": challenge_rule[0],
        "challenge_rule": challenge_rule[1],
        "null_draws": draws,
        "null_as_bad": wins,
        "null_median": round(sorted(null_best)[draws // 2], 2),
    }


def group_reorders() -> dict:
    """Apply one rearrangement inside every printed group of five.

    The row digit and the column digit alternate in the printed line. A
    rearrangement that breaks the alternation is not the square he taught.
    """
    groups = CHALLENGE.split()
    legal = 0
    best = None
    identity_legal = False
    for perm in itertools.permutations(range(5)):
        stream = "".join("".join(group[index] for index in perm) for group in groups)
        if stream.endswith("000"):
            stream = stream[:-3]
        if len(stream) % 2:
            continue
        pairs = [stream[index:index + 2] for index in range(0, len(stream), 2)]
        if not pairs:
            continue
        if all(pair[0] in _ROW and pair[1] in _COLUMN for pair in pairs):
            legal += 1
            score = best_chi_square(tuple(pairs))
            if perm == (0, 1, 2, 3, 4):
                identity_legal = True
            if best is None or score < best[0]:
                best = (score, "".join(str(index) for index in perm))
    return {
        "reorders": 120,
        "still_a_square": legal,
        "identity_kept": identity_legal,
        "best_legal_chi": None if best is None else round(best[0], 2),
        "best_reorder": None if best is None else best[1],
        "control": control_group_reorders(),
    }


def control_group_reorders() -> dict:
    """The book's solved example, grouped the same 120 ways.

    Its printed order is already English. A reorder that only helps the
    challenge, and hurts this example, is not his grouping rule.
    """
    groups = CONTROL.split()
    scores = []
    for perm in itertools.permutations(range(5)):
        stream = []
        for group in groups:
            if len(group) == 5:
                stream.append("".join(group[index] for index in perm))
            else:
                stream.append(group)
        text = "".join(stream)
        if len(text) % 2:
            text = text[:-1]
        pairs = tuple(text[index:index + 2] for index in range(0, len(text), 2))
        scores.append((best_chi_square(pairs), "".join(str(index) for index in perm)))
    printed = next(score for score, label in scores if label == "01234")
    flipped = next(score for score, label in scores if label == "01432")
    return {
        "printed_chi": round(printed, 2),
        "flipped_chi": round(flipped, 2),
        "better_than_printed": sum(1 for score, _ in scores if score < printed - 1e-9),
    }


def period_slice(worker: int, workers: int = _WORKER_COUNT) -> dict:
    """Mean column index of coincidence for the periods assigned to one worker."""
    symbols = challenge_pairs()
    rows = []
    for period in _PERIODS:
        if period % workers != worker:
            continue
        columns: list[list[str]] = [[] for _ in range(period)]
        for index, symbol in enumerate(symbols):
            columns[index % period].append(symbol)
        scores = []
        for column in columns:
            counts = Counter(column)
            width = len(column)
            scores.append(sum(value * (value - 1) for value in counts.values()) / (width * (width - 1)))
        rows.append((period, sum(scores) / len(scores)))
    if not rows:
        return {"worker": worker, "periods": 0, "best_period": None, "best_ic": None}
    period, score = max(rows, key=lambda item: item[1])
    return {"worker": worker, "periods": len(rows), "best_period": period, "best_ic": round(score, 4)}


def _period_peak(symbols: tuple[str, ...] | list[str]) -> float:
    best = 0.0
    for period in _PERIODS:
        columns: list[list[str]] = [[] for _ in range(period)]
        for index, symbol in enumerate(symbols):
            columns[index % period].append(symbol)
        scores = []
        for column in columns:
            counts = Counter(column)
            width = len(column)
            scores.append(sum(value * (value - 1) for value in counts.values()) / (width * (width - 1)))
        score = sum(scores) / len(scores)
        if score > best:
            best = score
    return best


def period_null(draws: int = _NULL_DRAWS) -> dict:
    """Whether the best period beats a shuffle of the same cells."""
    symbols = list(challenge_pairs())
    observed = _period_peak(symbols)
    drawn = random.Random(_SEED + 1)
    wins = 0
    for _ in range(draws):
        drawn.shuffle(symbols)
        if _period_peak(symbols) >= observed:
            wins += 1
    counts = Counter(challenge_pairs())
    width = len(symbols)
    ic = sum(value * (value - 1) for value in counts.values()) / (width * (width - 1))
    return {
        "overall_ic": round(ic, 4),
        "best_period_ic": round(observed, 4),
        "null_draws": draws,
        "shuffles_as_high": wins,
    }


def search_more() -> dict:
    """Run the wider swarm in-process. Workers below cover the same slices."""
    languages = {}
    observed = _observed_counts()
    for language in ("english", *tuple(_PERCENT)):
        score, label = min(((_chi(observed, rates), label) for label, rates in hypotheses(language)))
        languages[language] = {"chi": round(score, 2), "rule": label}
    mergers = merger_null()
    groups = group_reorders()
    periods = period_null()
    return {
        "claimed_plaintext": None,
        "solved": False,
        "languages": languages,
        "merger": mergers,
        "groups": groups,
        "periods": {
            "overall_ic": periods["overall_ic"],
            "best_period_ic": periods["best_period_ic"],
            "null_draws": periods["null_draws"],
            "shuffles_as_high": periods["shuffles_as_high"],
        },
        "workers": _WORKER_COUNT,
        "scope": (
            "No language, no 25-cell merger, no group reorder, and no period "
            "is returned as plaintext. Esperanto has 28 letters and does not "
            "fit this square, so it is not scored as a one-cell alphabet."
        ),
    }


def worker_report(worker: int) -> dict:
    """The slice one subagent owns. Plaintext is not in it."""
    return {
        "merger": language_slice(worker),
        "period": period_slice(worker),
        "claimed_plaintext": None,
    }
