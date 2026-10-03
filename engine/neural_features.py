"""Ciphertext features for the family router.

The row is a fixed vector: classic ciphertext statistics, plus look-ahead
scores that try a certified family's known map and keep only the English
fitness of that trial. The trial string is not returned. K4, Zodiac, Beale,
McCormick, Voynich, and Nr. 86 are not families and are not decrypted here.
"""

from __future__ import annotations

import math

import numpy as np

from engine.solvers import keel_sieve, lumen_braid, prism_latch

_ADFGVX = np.array([ord(ch) - 65 for ch in "ADFGVX"], dtype=np.int64)
_VOWELS = np.array([ord(ch) - 65 for ch in "AEIOU"], dtype=np.int64)


def feature_tables(train_letters: str, english: list[float]) -> dict:
    """Unigram and digraph tables fit on the training letters only."""
    eng = np.asarray(english, dtype=np.float64)
    ints = np.fromiter((ord(ch) - 65 for ch in train_letters), dtype=np.int64, count=len(train_letters))
    dig = np.full((26, 26), 0.5, dtype=np.float64)
    if len(ints) >= 2:
        np.add.at(dig, (ints[:-1], ints[1:]), 1.0)
    dig /= dig.sum(axis=1, keepdims=True)
    return {
        "english": eng,
        "logdig": np.log(dig),
        "mvig": np.array([[eng[(j - shift) % 26] for shift in range(26)] for j in range(26)]),
        "mbeau": np.array([[eng[(key - j) % 26] for key in range(26)] for j in range(26)]),
        "norm": float(np.linalg.norm(eng) + 1e-12),
        "sorted_english": np.sort(eng)[::-1],
        "sorted_norm": float(np.linalg.norm(np.sort(eng)) + 1e-12),
    }


def _digraph_mean(seq: np.ndarray, logdig: np.ndarray) -> float:
    if seq.shape[0] < 3:
        return -10.0
    return float(logdig[seq[:-1], seq[1:]].mean())


def _letters(text: str) -> np.ndarray:
    chars = [ord(ch) - 65 for ch in text if "A" <= ch <= "Z"]
    if not chars:
        raise ValueError("ciphertext is too short to featurize")
    return np.asarray(chars, dtype=np.int64)


def _look_ahead(values: np.ndarray, tables: dict) -> list[float]:
    """Fitness of certified trial maps. The trial plaintext is discarded."""
    english = tables["english"]
    norm = tables["norm"]
    logdig = tables["logdig"]
    sorted_english = tables["sorted_english"]
    sorted_norm = tables["sorted_norm"]
    n = int(values.shape[0])
    kappas = [float(np.mean(values[lag:] == values[:-lag])) for lag in range(2, 10)]
    period = int(np.argmax(kappas)) + 2
    usable = n - (n % period)
    rows = max(usable // period, 1)
    cols = values[:usable].reshape(rows, period)
    flat_index = cols + np.arange(period) * 26
    counts = np.bincount(flat_index.ravel(), minlength=period * 26).reshape(period, 26).astype(np.float64)
    freq = counts / rows
    freq_norm = np.linalg.norm(freq, axis=1) + 1e-12
    vig_cos = (freq @ tables["mvig"]) / (freq_norm[:, None] * norm)
    shifts = vig_cos.argmax(axis=1)
    positions = np.arange(usable) % period
    vig_plain = (values[:usable] - shifts[positions]) % 26
    vig_score = _digraph_mean(vig_plain, logdig)
    beau_cos = (freq @ tables["mbeau"]) / (freq_norm[:, None] * norm)
    beau_keys = beau_cos.argmax(axis=1)
    beau_plain = (beau_keys[positions] - values[:usable]) % 26
    beau_score = _digraph_mean(beau_plain, logdig)
    sorted_freq = np.sort(freq, axis=1)[:, ::-1]
    sorted_cos = (sorted_freq @ sorted_english) / (np.linalg.norm(sorted_freq, axis=1) * sorted_norm)
    gap = float((sorted_cos - vig_cos.max(axis=1)).mean())
    # Porta rows 0..12. Each column keeps the row whose decrypted unigram
    # best matches the training unigram. Only the digraph fitness is kept.
    row_ids = np.arange(13)[:, None, None]
    cipher_cols = cols[None, :, :]
    porta_plain_cols = np.where(
        cipher_cols >= 13,
        (cipher_cols - 13 - row_ids) % 13,
        13 + (cipher_cols + row_ids) % 13,
    )
    porta_fit = english[porta_plain_cols].mean(axis=1)
    best_rows = porta_fit.argmax(axis=0)
    chosen = porta_plain_cols[
        best_rows[None, :],
        np.arange(rows)[:, None],
        np.arange(period)[None, :],
    ]
    porta_score = _digraph_mean(chosen.reshape(-1), logdig)
    raw = (values.astype(np.uint8) + 65).tobytes().decode("ascii")

    def inverse_score(fn) -> float:
        try:
            recovered = fn(raw)
        except (ValueError, ZeroDivisionError):
            return -10.0
        letters = [ord(ch) - 65 for ch in recovered if "A" <= ch <= "Z"]
        if len(letters) < 3:
            return -10.0
        return _digraph_mean(np.asarray(letters, dtype=np.int64), logdig)

    keel_score = inverse_score(keel_sieve.decrypt)
    lumen_score = inverse_score(lumen_braid.decrypt)
    prism_score = inverse_score(prism_latch.decrypt)
    return [
        vig_score,
        beau_score,
        vig_score - beau_score,
        gap,
        porta_score,
        float(vig_cos.max(axis=1).mean()),
        float(period),
        keel_score,
        lumen_score,
        prism_score,
    ]


def _base_features(values: np.ndarray, tables: dict) -> list[float]:
    """Small ciphertext summary. The expensive period trials live in look-ahead."""
    english = tables["english"]
    norm = tables["norm"]
    n = int(values.shape[0])
    counts = np.bincount(values, minlength=26).astype(np.float64)
    freq = counts / n
    ic = float((counts * (counts - 1)).sum() / (n * (n - 1)))
    positive = freq[freq > 0.0]
    entropy = float(-(positive * np.log(positive)).sum())
    freq_norm = float(np.linalg.norm(freq) + 1e-12)
    vig_dot = freq @ tables["mvig"]
    best_shift_cos = float(vig_dot.max() / (freq_norm * norm))
    cos0 = float(freq @ english / (freq_norm * norm))
    sorted_freq = np.sort(freq)[::-1]
    sorted_cos = float(
        sorted_freq @ tables["sorted_english"] / (np.linalg.norm(sorted_freq) * tables["sorted_norm"])
    )
    doubles = float(np.mean(values[1:] == values[:-1])) if n > 1 else 0.0
    even = values[0::2]
    odd = values[1::2]
    pair_doubles = float(np.mean(even[: odd.shape[0]] == odd)) if odd.shape[0] else 0.0
    adfgvx = float(np.isin(values, _ADFGVX).mean())
    j_frac = float(counts[ord("J") - 65] / n)
    q_frac = float(counts[ord("Q") - 65] / n)
    vowels = float(counts[_VOWELS].sum() / n)
    unique = float((counts > 0).mean())
    top = float(counts.max() / n)
    even_counts = np.bincount(even, minlength=26).astype(np.float64)
    odd_counts = np.bincount(odd, minlength=26).astype(np.float64)
    even_n = even_counts.sum() or 1.0
    odd_n = odd_counts.sum() or 1.0
    even_odd = float(np.abs(even_counts / even_n - odd_counts / odd_n).sum())
    if odd.shape[0]:
        pairs = even[: odd.shape[0]] * 26 + odd
        pair_counts = np.bincount(pairs, minlength=26 * 26)
        digraph_repeat = float(pair_counts[pair_counts > 1].sum() / odd.shape[0])
    else:
        digraph_repeat = 0.0
    # Column IC at periods 2..8, one bincount each. No Caesar search here.
    slice_ics = []
    for period in range(2, 9):
        rows = n // period
        if rows < 4:
            slice_ics.append(0.0)
            continue
        usable = rows * period
        cols = values[:usable].reshape(rows, period)
        flat_index = cols + np.arange(period) * 26
        column_counts = np.bincount(flat_index.ravel(), minlength=period * 26).reshape(period, 26).astype(np.float64)
        column_ic = (column_counts * (column_counts - 1)).sum(axis=1) / (rows * (rows - 1))
        slice_ics.append(float(column_ic.mean()))
    kappas = [float(np.mean(values[lag:] == values[:-lag])) for lag in (1, 2, 3, 4, 5)]
    return [
        ic,
        entropy,
        best_shift_cos,
        cos0,
        sorted_cos,
        doubles,
        pair_doubles,
        adfgvx,
        j_frac,
        q_frac,
        vowels,
        unique,
        top,
        even_odd,
        digraph_repeat,
        max(slice_ics),
        *slice_ics,
        *kappas,
    ]


def router_features(text: str, english: list[float], tables: dict | None = None) -> list[float]:
    """Fixed feature row. `english` is the training unigram, never the held-out text."""
    if len(text) < 16 and sum(ch.isalpha() for ch in text) < 16:
        raise ValueError("ciphertext is too short to featurize")
    if tables is None:
        from engine.neural_grade import ciphertext_features

        return ciphertext_features(text, english)
    values = _letters(text)
    if values.shape[0] < 16:
        raise ValueError("ciphertext is too short to featurize")
    return _base_features(values, tables) + _look_ahead(values, tables)

