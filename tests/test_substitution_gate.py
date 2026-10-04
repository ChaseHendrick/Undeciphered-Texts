"""The substitution solver refuses an order a shuffle can match."""

from __future__ import annotations

import random
import unittest

from engine.ciphers import substitution_encrypt
from engine.dagapeyeff_swarm import challenge_pairs
from engine.fixtures import SUBSTITUTION_KEY, SUBSTITUTION_PLAIN
from engine.solvers.substitution import solve_substitution, substitution_order_gate
from engine.stats import successive_information


class SubstitutionGateTest(unittest.TestCase):
    def test_a_real_substitution_keeps_its_order(self) -> None:
        cipher = substitution_encrypt(SUBSTITUTION_PLAIN, SUBSTITUTION_KEY)
        gate = substitution_order_gate(cipher, seed=20261004)
        plain = substitution_order_gate(SUBSTITUTION_PLAIN, seed=20261004)
        self.assertEqual(gate["order_mi"], 0.7991)
        self.assertEqual(gate["order_mi"], plain["order_mi"])
        self.assertEqual(gate["order_as_predictable"], 0)
        self.assertIs(gate["reading"], True)
        result = solve_substitution(cipher, restarts=1, steps=1, seed=20261002)
        self.assertIs(result.details["reading"], True)
        self.assertEqual(result.details["order_mi"], gate["order_mi"])

    def test_the_1939_pairs_are_refused(self) -> None:
        symbols = list(challenge_pairs())
        observed = successive_information(symbols)
        self.assertEqual(round(observed, 4), 0.5706)
        drawn = random.Random(20261004)
        as_high = 0
        for _ in range(200):
            shuffled = symbols[:]
            drawn.shuffle(shuffled)
            if successive_information(shuffled) >= observed - 1e-15:
                as_high += 1
        self.assertEqual(as_high, 170)
        self.assertIs(as_high * 20 < 200, False)


if __name__ == "__main__":
    unittest.main()
