"""Index of coincidence, Friedman estimate, n-gram counts, and Kasiski."""

from __future__ import annotations

from collections import Counter

from engine.alphabet import letters_only

# English and random-text coincidence constants used by the Friedman estimate.
ENGLISH_IC = 0.0667
RANDOM_IC = 1.0 / 26.0


def counts(letters: str) -> list[int]:
    tally = [0] * 26
    for ch in letters:
        tally[ord(ch) - 65] += 1
    return tally


def index_of_coincidence(text: str) -> float:
    """Friedman index of coincidence on the alphabetic stream."""
    letters = letters_only(text)
    n = len(letters)
    if n < 2:
        return 0.0
    total = sum(c * (c - 1) for c in counts(letters))
    return total / (n * (n - 1))


def friedman_period(text: str) -> float:
    """Rough keyword length from the overall index of coincidence.

    k ≈ 0.0265 n / ((n - 1) IC - 0.0385 n + 0.065). Returns 0 when the
    denominator is not positive (text too short or too flat).
    """
    letters = letters_only(text)
    n = len(letters)
    if n < 2:
        return 0.0
    ic = index_of_coincidence(letters)
    denom = (n - 1) * ic - 0.0385 * n + 0.065
    if denom <= 1e-9:
        return 0.0
    return (0.0265 * n) / denom


def ngram_counts(text: str, n: int, limit: int = 12) -> list[tuple[str, int]]:
    letters = letters_only(text)
    if n < 1 or len(letters) < n:
        return []
    bag: Counter[str] = Counter(letters[i : i + n] for i in range(len(letters) - n + 1))
    return bag.most_common(limit)


def repeated_distances(letters: str, size: int) -> list[int]:
    """Distances between successive repeats of each n-gram, in letter positions."""
    positions: dict[str, list[int]] = {}
    for i in range(len(letters) - size + 1):
        gram = letters[i : i + size]
        positions.setdefault(gram, []).append(i)
    distances: list[int] = []
    for pos in positions.values():
        if len(pos) < 2:
            continue
        for left, right in zip(pos, pos[1:]):
            gap = right - left
            if gap > 0:
                distances.append(gap)
    return distances


def kasiski_factors(text: str, max_period: int = 16, sizes: tuple[int, ...] = (3, 4, 5)) -> list[tuple[int, int]]:
    """Vote for periods that divide gaps between repeated n-grams.

    Returns (period, votes) sorted by votes descending, then period ascending.
    Period 1 is omitted. This is Kasiski examination, not a decrypt by itself.
    """
    letters = letters_only(text)
    votes: Counter[int] = Counter()
    for size in sizes:
        if len(letters) < size + 1:
            continue
        for gap in repeated_distances(letters, size):
            for period in range(2, max_period + 1):
                if gap % period == 0:
                    votes[period] += 1
    ranked = sorted(votes.items(), key=lambda item: (-item[1], item[0]))
    return ranked


def column_mean_ic(letters: str, period: int) -> float:
    """Mean index of coincidence of the period columns (letter stream)."""
    if period < 1 or len(letters) < period + 1:
        return 0.0
    scores: list[float] = []
    for offset in range(period):
        column = letters[offset::period]
        if len(column) >= 2:
            scores.append(index_of_coincidence(column))
    if not scores:
        return 0.0
    return sum(scores) / len(scores)
