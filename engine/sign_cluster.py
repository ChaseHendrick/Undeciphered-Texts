"""Cluster sign symbols by the contexts they keep.

Each symbol is a vector of the symbols that occur beside it. K-means (or
average-linkage hierarchical clustering) then groups symbols with similar
vectors. On a synthetic corpus whose two symbol classes were generated as
vowels versus consonants, those groups can line up with the two classes.

This does not decipher an ancient script. A cluster is not a sound, a word,
or a reading of Linear A, the Indus script, Rongorongo, the Phaistos disc,
or the Voynich manuscript. The method only says which symbols share contexts
in the transcription you gave it.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

# Public reminder. Tests and docs quote this so the limit stays attached to
# the tool, not only to a README line that another edit might drop.
NOT_A_DECIPHERMENT = (
    "This does not decipher an ancient script. "
    "Clusters are distributional groups, not readings."
)

VOWEL_CLASS = "vowel"
CONSONANT_CLASS = "consonant"


@dataclass(frozen=True)
class SyntheticSignCorpus:
    """Token sequences plus the generating class of each symbol.

    ``words`` do not share context across boundaries. ``sign_class`` maps each
    symbol to ``vowel`` or ``consonant``. Clustering functions do not read
    ``sign_class``; it exists so a test can score a partition after the fact.
    """

    words: tuple[tuple[str, ...], ...]
    sign_class: Mapping[str, str]
    seed: int

    @property
    def signs(self) -> tuple[str, ...]:
        return tuple(sorted(self.sign_class))


@dataclass(frozen=True)
class SignClusters:
    """One unsupervised partition of the symbols that actually occurred."""

    signs: tuple[str, ...]
    labels: tuple[int, ...]
    method: str
    k: int

    def label_of(self, sign: str) -> int:
        return self.labels[self.signs.index(sign)]

    def as_dict(self) -> dict[str, int]:
        return dict(zip(self.signs, self.labels))

    def by_cluster(self) -> dict[int, tuple[str, ...]]:
        groups: dict[int, list[str]] = {}
        for sign, label in zip(self.signs, self.labels):
            groups.setdefault(label, []).append(sign)
        return {label: tuple(groups[label]) for label in sorted(groups)}


def generate_vowel_consonant_corpus(
    *,
    n_words: int = 400,
    seed: int = 0,
    vowels: Sequence[str] = ("V0", "V1", "V2", "V3", "V4", "V5"),
    consonants: Sequence[str] = ("C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"),
    syllables: Sequence[int] = (2, 3, 4),
) -> SyntheticSignCorpus:
    """Build words that strictly alternate consonant, vowel, consonant, vowel.

    The two classes are the generating process, not something the clusterer
    is shown. Every vowel token sits between consonants and every consonant
    token sits between vowels, aside from word edges. Symbols are invented
    labels, not letters from a historical script.
    """
    if n_words < 1:
        raise ValueError("n_words must be positive")
    vowel_tuple = tuple(vowels)
    consonant_tuple = tuple(consonants)
    if len(vowel_tuple) < 2 or len(consonant_tuple) < 2:
        raise ValueError("need at least two symbols in each class")
    if set(vowel_tuple) & set(consonant_tuple):
        raise ValueError("vowel and consonant symbol sets must be disjoint")
    syllable_choices = tuple(syllables)
    if not syllable_choices or any(n < 1 for n in syllable_choices):
        raise ValueError("syllables must be positive lengths")

    rng = random.Random(seed)
    words: list[tuple[str, ...]] = []
    for _ in range(n_words):
        pieces: list[str] = []
        for _syl in range(rng.choice(syllable_choices)):
            pieces.append(rng.choice(consonant_tuple))
            pieces.append(rng.choice(vowel_tuple))
        words.append(tuple(pieces))
    sign_class = {sign: VOWEL_CLASS for sign in vowel_tuple}
    sign_class.update({sign: CONSONANT_CLASS for sign in consonant_tuple})
    return SyntheticSignCorpus(words=tuple(words), sign_class=sign_class, seed=seed)


def cooccurrence_vectors(
    words: Sequence[Sequence[str]],
    *,
    window: int = 1,
) -> tuple[tuple[str, ...], np.ndarray]:
    """Row-normalized left-and-right co-occurrence vectors, one row per symbol.

    Context does not cross word boundaries. Column order is left-neighbor
    counts for every symbol, then right-neighbor counts. Rows are L2
    normalized so a frequent symbol is not far from a rare one merely because
    it has more counts.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    vocab_set: list[str] = []
    seen: set[str] = set()
    for word in words:
        for sign in word:
            if sign not in seen:
                seen.add(sign)
                vocab_set.append(sign)
    if not vocab_set:
        raise ValueError("corpus has no signs")
    # Stable order: alphabetical, independent of first-seen order.
    signs = tuple(sorted(vocab_set))
    index = {sign: i for i, sign in enumerate(signs)}
    n = len(signs)
    counts = np.zeros((n, 2 * n), dtype=float)
    for word in words:
        tokens = list(word)
        for i, sign in enumerate(tokens):
            row = index[sign]
            for offset in range(1, window + 1):
                left = i - offset
                if left >= 0:
                    counts[row, index[tokens[left]]] += 1.0
                right = i + offset
                if right < len(tokens):
                    counts[row, n + index[tokens[right]]] += 1.0
    # Light smoothing keeps a symbol that only occurs at an edge from being
    # a zero vector. It does not add class labels.
    counts += 1e-3
    norms = np.linalg.norm(counts, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return signs, counts / norms


def kmeans(
    vectors: np.ndarray,
    k: int = 2,
    *,
    n_iter: int = 40,
    seed: int = 0,
    restarts: int = 8,
) -> np.ndarray:
    """Lloyd k-means. Returns an int label per row.

    The first restart is deterministic farthest-point initialization. Later
    restarts are seeded from ``seed`` so the same matrix always yields the
    same labels. The restart with the lowest within-cluster sum of squares
    is kept.
    """
    matrix = np.asarray(vectors, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("vectors must be a 2-d array")
    n_rows = matrix.shape[0]
    if k < 2 or k > n_rows:
        raise ValueError("k must be between 2 and the number of rows")
    rng = np.random.default_rng(seed)
    best_labels: np.ndarray | None = None
    best_inertia = float("inf")
    for restart in range(restarts):
        if restart == 0:
            centroids = _farthest_centroids(matrix, k)
        else:
            picked = rng.choice(n_rows, size=k, replace=False)
            centroids = matrix[picked].copy()
        labels = _lloyd(matrix, centroids, n_iter=n_iter, rng=rng)
        inertia = _inertia(matrix, labels, k)
        # Tie-break toward the lower restart index via strict <.
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels.copy()
    assert best_labels is not None
    return _compact_labels(best_labels)


def hierarchical_clusters(vectors: np.ndarray, k: int = 2) -> np.ndarray:
    """Average-linkage agglomerative clustering down to ``k`` groups.

    Deterministic given the rows. Distance is Euclidean. Useful as a second
    opinion next to k-means; it is not a decipherment method either.
    """
    matrix = np.asarray(vectors, dtype=float)
    n_rows = matrix.shape[0]
    if matrix.ndim != 2 or k < 2 or k > n_rows:
        raise ValueError("need a 2-d matrix and 2 <= k <= n_rows")
    members: list[list[int]] = [[i] for i in range(n_rows)]
    active = list(range(n_rows))
    while len(active) > k:
        best_i = 0
        best_j = 1
        best_d = float("inf")
        for i in range(len(active)):
            for j in range(i + 1, len(active)):
                dist = _average_linkage(matrix, members[active[i]], members[active[j]])
                if dist < best_d:
                    best_d = dist
                    best_i = i
                    best_j = j
        keep = active[best_i]
        drop = active[best_j]
        members[keep] = members[keep] + members[drop]
        del active[best_j]
    labels = np.zeros(n_rows, dtype=int)
    for label, cluster_index in enumerate(active):
        for row in members[cluster_index]:
            labels[row] = label
    return labels


def cluster_signs(
    words: Sequence[Sequence[str]],
    *,
    k: int = 2,
    method: str = "kmeans",
    window: int = 1,
    seed: int = 0,
) -> SignClusters:
    """Cluster symbols from their co-occurrence vectors.

    ``method`` is ``kmeans`` or ``hierarchical``. Class labels are not an
    argument. See ``NOT_A_DECIPHERMENT``.
    """
    signs, vectors = cooccurrence_vectors(words, window=window)
    if method == "kmeans":
        labels = kmeans(vectors, k, seed=seed)
    elif method == "hierarchical":
        labels = hierarchical_clusters(vectors, k)
    else:
        raise ValueError("method must be 'kmeans' or 'hierarchical'")
    return SignClusters(
        signs=signs,
        labels=tuple(int(label) for label in labels),
        method=method,
        k=k,
    )


def alignment_accuracy(clusters: SignClusters, sign_class: Mapping[str, str]) -> float:
    """Fraction of symbols correct after the best match of clusters to classes.

    For two clusters and two classes this is the better of the two possible
    assignments. The clusterer never sees ``sign_class``.
    """
    pred = clusters.as_dict()
    signs = [sign for sign in clusters.signs if sign in sign_class]
    if len(signs) < 2:
        raise ValueError("need at least two labeled symbols")
    classes = sorted({sign_class[sign] for sign in signs})
    if len(classes) != 2 or clusters.k != 2:
        raise ValueError("alignment_accuracy supports exactly two classes and k=2")
    truth = {sign: (0 if sign_class[sign] == classes[0] else 1) for sign in signs}
    raw = sum(1 for sign in signs if pred[sign] == truth[sign]) / len(signs)
    flipped = sum(1 for sign in signs if pred[sign] != truth[sign]) / len(signs)
    return float(max(raw, flipped))


def chance_alignment_accuracy(
    clusters: SignClusters,
    sign_class: Mapping[str, str],
    *,
    n_perm: int = 400,
    seed: int = 1,
) -> float:
    """Mean best-alignment accuracy when class labels are permuted at random.

    The partition stays fixed. Only the vowel/consonant tags are shuffled, so
    the number of symbols in each class stays the same. That is the chance
    level for "did these clusters recover the generating classes?"
    """
    if n_perm < 1:
        raise ValueError("n_perm must be positive")
    signs = [sign for sign in clusters.signs if sign in sign_class]
    labels = [sign_class[sign] for sign in signs]
    rng = random.Random(seed)
    total = 0.0
    for _ in range(n_perm):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        scrambled = dict(zip(signs, shuffled))
        total += alignment_accuracy(clusters, scrambled)
    return total / n_perm


def _farthest_centroids(matrix: np.ndarray, k: int) -> np.ndarray:
    center = matrix.mean(axis=0)
    first = int(np.argmax(np.sum((matrix - center) ** 2, axis=1)))
    chosen = [first]
    while len(chosen) < k:
        nearest = np.full(matrix.shape[0], np.inf)
        for idx in chosen:
            dist = np.sum((matrix - matrix[idx]) ** 2, axis=1)
            nearest = np.minimum(nearest, dist)
        nearest[chosen] = -1.0
        chosen.append(int(np.argmax(nearest)))
    return matrix[np.array(chosen)].copy()


def _lloyd(
    matrix: np.ndarray,
    centroids: np.ndarray,
    *,
    n_iter: int,
    rng: np.random.Generator,
) -> np.ndarray:
    labels = np.zeros(matrix.shape[0], dtype=int)
    for _ in range(n_iter):
        distances = np.sum((matrix[:, None, :] - centroids[None, :, :]) ** 2, axis=2)
        updated = np.argmin(distances, axis=1).astype(int)
        if np.array_equal(updated, labels):
            # Still refresh once so an empty cluster from a bad init can move,
            # but stop when labels and a full set of centroids are stable.
            labels = updated
            break
        labels = updated
        for cluster in range(centroids.shape[0]):
            members = matrix[labels == cluster]
            if len(members) == 0:
                centroids[cluster] = matrix[int(rng.integers(0, matrix.shape[0]))]
            else:
                centroids[cluster] = members.mean(axis=0)
    return labels


def _inertia(matrix: np.ndarray, labels: np.ndarray, k: int) -> float:
    total = 0.0
    for cluster in range(k):
        members = matrix[labels == cluster]
        if len(members) == 0:
            return float("inf")
        center = members.mean(axis=0)
        total += float(np.sum((members - center) ** 2))
    return total


def _compact_labels(labels: np.ndarray) -> np.ndarray:
    """Renumber labels so the smallest original id becomes 0, in order."""
    order: list[int] = []
    for label in labels.tolist():
        if label not in order:
            order.append(label)
    remap = {old: new for new, old in enumerate(order)}
    return np.array([remap[int(label)] for label in labels], dtype=int)


def _average_linkage(matrix: np.ndarray, left: Sequence[int], right: Sequence[int]) -> float:
    left_rows = matrix[np.array(list(left))]
    right_rows = matrix[np.array(list(right))]
    diff = left_rows[:, None, :] - right_rows[None, :, :]
    return float(np.sqrt(np.sum(diff ** 2, axis=2)).mean())
