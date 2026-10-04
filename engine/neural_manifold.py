"""A small doubly stochastic residual mix. Not a new router, and not a reading.

DeepSeek's mHC keeps a widened residual from amplifying by projecting the
mix onto the doubly stochastic manifold, with Sinkhorn. A later measurement
of DeepSeek-V4-Flash found that a block usually uses about two of the four
streams, and that late mixing is nearly the identity.

Bob is two layers deep, not a stack of sixty. Four streams would be the
unused part of that result. This module mixes two streams and forces the
mix through Sinkhorn, so a stack cannot grow the L1 norm. The shipped
format 5 weights are not read and not replaced.
"""

from __future__ import annotations

import numpy as np


def sinkhorn(logits: np.ndarray, steps: int = 20) -> np.ndarray:
    """Project a square matrix onto nonnegative row-and-column sums of 1."""
    matrix = np.asarray(logits, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not 2 <= matrix.shape[0] <= 8:
        raise ValueError("sinkhorn expects a square matrix of width 2 to 8")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("sinkhorn expects finite logits")
    positive = np.exp(np.clip(matrix, -40.0, 40.0))
    for _ in range(steps):
        positive /= positive.sum(axis=1, keepdims=True)
        positive /= positive.sum(axis=0, keepdims=True)
    return positive


def two_stream_mix(streams: np.ndarray, logits: np.ndarray, steps: int = 20) -> np.ndarray:
    """Mix two residual streams with a doubly stochastic matrix.

    streams has shape (batch, 2, width). The mix is the same for every row.
    An identity mix leaves both streams unchanged.
    """
    values = np.asarray(streams, dtype=np.float64)
    if values.ndim != 3 or values.shape[1] != 2:
        raise ValueError("two streams are required")
    mix = sinkhorn(np.asarray(logits, dtype=np.float64), steps=steps)
    if mix.shape != (2, 2):
        raise ValueError("a two-stream mix is a 2 by 2 matrix")
    return np.einsum("ij,bjw->biw", mix, values)


def stack_l1(streams: np.ndarray, mixes: list[np.ndarray], steps: int = 20) -> float:
    """L1 norm after several mixes. Doubly stochastic mixes do not increase it."""
    values = np.asarray(streams, dtype=np.float64)
    for logits in mixes:
        values = two_stream_mix(values, logits, steps=steps)
    return float(np.sum(np.abs(values)))
