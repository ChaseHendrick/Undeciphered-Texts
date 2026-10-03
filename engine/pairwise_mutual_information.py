"""Pairwise mutual information between adjacent signs.

Unsupervised measurement of an already transcribed sign stream. It ranks
ordered neighbor pairs by how much more often they occur than the product of
their marginal frequencies. It does not decipher Linear A, the Voynich
manuscript, Rongorongo, Indus, or any other ancient script. A top-ranked pair
is a statistic of the tokens you supplied, not a sound, a word, or a reading.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import log2
from typing import Iterable, Sequence


@dataclass(frozen=True)
class AdjacentPairMI:
    """One observed ordered pair and its association with the following sign."""

    left: str
    right: str
    count: int
    pair_total: int
    joint: float
    left_marginal: float
    right_marginal: float
    expected_count: float
    pmi_bits: float
    mi_contribution_bits: float

    @property
    def pair(self) -> tuple[str, str]:
        return (self.left, self.right)

    @property
    def text(self) -> str:
        return f"{self.left} {self.right}"


def adjacent_pairs(signs: Sequence[str]) -> list[tuple[str, str]]:
    """Ordered neighbor pairs inside one flat sign stream.

    Index i pairs with i+1. A stream shorter than two signs yields nothing.
    Callers that must not cross a line or word break should pass each span
    separately and pool with ``pairwise_mutual_information_grouped``.
    """
    if len(signs) < 2:
        return []
    return [(signs[i], signs[i + 1]) for i in range(len(signs) - 1)]


def _rank_from_pairs(pairs: Sequence[tuple[str, str]]) -> list[AdjacentPairMI]:
    total = len(pairs)
    if total == 0:
        return []
    joint: Counter[tuple[str, str]] = Counter(pairs)
    left_counts: Counter[str] = Counter(left for left, _ in pairs)
    right_counts: Counter[str] = Counter(right for _, right in pairs)
    ranked: list[AdjacentPairMI] = []
    for (left, right), count in joint.items():
        p_joint = count / total
        p_left = left_counts[left] / total
        p_right = right_counts[right] / total
        # Both marginals are positive: the pair was observed.
        pmi = log2(p_joint / (p_left * p_right))
        expected = total * p_left * p_right
        ranked.append(
            AdjacentPairMI(
                left=left,
                right=right,
                count=count,
                pair_total=total,
                joint=p_joint,
                left_marginal=p_left,
                right_marginal=p_right,
                expected_count=expected,
                pmi_bits=pmi,
                mi_contribution_bits=p_joint * pmi,
            )
        )
    ranked.sort(key=lambda row: (-row.pmi_bits, -row.count, row.left, row.right))
    return ranked


def pairwise_mutual_information(signs: Sequence[str]) -> list[AdjacentPairMI]:
    """Rank observed adjacent pairs by pointwise mutual information.

    Probabilities are maximum-likelihood counts over the stream of adjacent
    pairs. ``P(left)`` and ``P(right)`` are marginals of that same stream, so
    a sign that only sits at one edge is in one marginal. Unobserved pairs are
    omitted (their count is zero; unsmoothed PMI is undefined). Scores are in
    bits. Sort order is PMI descending, then count descending, then sign text.

    This does not assign values and does not decipher an ancient script.
    """
    return _rank_from_pairs(adjacent_pairs(signs))


def pairwise_mutual_information_grouped(
    spans: Iterable[Sequence[str]],
) -> list[AdjacentPairMI]:
    """Same ranking, pooling spans without counting across span boundaries.

    Use one span per inscription line or word when the break is real. A span
    shorter than two signs adds no pairs.
    """
    pairs: list[tuple[str, str]] = []
    for span in spans:
        pairs.extend(adjacent_pairs(span))
    return _rank_from_pairs(pairs)


def mutual_information_bits(rows: Sequence[AdjacentPairMI]) -> float:
    """Sum of pair contributions, which is I(left; right) in bits.

    Unobserved pairs contribute nothing under maximum likelihood. An empty
    ranking returns 0.0. The number describes dependence inside the pair
    stream. It is not a decipherment score.
    """
    return sum(row.mi_contribution_bits for row in rows)
