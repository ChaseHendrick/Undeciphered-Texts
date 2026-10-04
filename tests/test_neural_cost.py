"""Cost-sensitive weights stay off unless a warm start asks for them."""

from __future__ import annotations

import unittest

import numpy as np

from engine.neural_router_v2 import fit_residual_network, train_router


class CostSensitiveTest(unittest.TestCase):
    def test_the_flag_refuses_a_cold_start(self) -> None:
        with self.assertRaises(ValueError):
            train_router(cost_sensitive=True, warm_start=False, write=False)
        features = np.array([[0., 1.], [1., 0.], [0., 0.], [1., 1.]], dtype=float)
        labels = np.array([0, 1, 0, 1])
        with self.assertRaises(ValueError):
            fit_residual_network(features, labels, features, labels, hidden=2, epochs=1, cost_sensitive=True)


if __name__ == "__main__":
    unittest.main()
