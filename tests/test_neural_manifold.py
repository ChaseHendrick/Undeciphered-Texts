"""The two-stream mix cannot amplify. The shipped router is not touched."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

from engine.neural_manifold import sinkhorn, stack_l1, two_stream_mix


class NeuralManifoldTest(unittest.TestCase):
    def test_sinkhorn_lands_on_the_manifold(self) -> None:
        drawn = np.random.default_rng(20261004)
        for width in (2, 4):
            got = sinkhorn(drawn.normal(size=(width, width)), steps=20)
            self.assertTrue(np.all(got >= 0))
            np.testing.assert_allclose(got.sum(axis=1), np.ones(width), atol=1e-8)
            np.testing.assert_allclose(got.sum(axis=0), np.ones(width), atol=1e-8)

    def test_a_deep_stack_does_not_grow(self) -> None:
        streams = np.array([[[1.0, -2.0, 0.5], [-0.5, 2.0, -0.5]]])
        start = float(np.sum(np.abs(streams)))
        mixes = [np.array([[5.0, 4.0], [-3.0, 6.0]]) for _ in range(32)]
        self.assertLessEqual(stack_l1(streams, mixes), start + 1e-6)

    def test_a_strong_diagonal_stays_near_the_identity(self) -> None:
        mix = sinkhorn(np.array([[30.0, -30.0], [-30.0, 30.0]]), steps=12)
        np.testing.assert_allclose(mix, np.eye(2), atol=1e-6)
        streams = np.array([[[3.0, 1.0], [4.0, 2.0]]])
        mixed = two_stream_mix(streams, np.array([[30.0, -30.0], [-30.0, 30.0]]), steps=12)
        np.testing.assert_allclose(mixed, streams, atol=1e-5)

    def test_the_shipped_weights_are_not_named(self) -> None:
        source = Path(__import__("engine.neural_manifold", fromlist=["sinkhorn"]).__file__).read_text(encoding="utf-8")
        self.assertNotIn("neural_router_v2_weights", source)
        self.assertNotIn("claimed_plaintext", source)


if __name__ == "__main__":
    unittest.main()
