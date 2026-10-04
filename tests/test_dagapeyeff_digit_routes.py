"""Routes of the digits do not beat prose, or a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_digit_routes import digit_route_report
from engine.solvers.dagapeyeff import consider_digit_routes


class DagapeyeffDigitRouteTest(unittest.TestCase):
    def test_the_digit_routes_lose_to_a_shuffle(self) -> None:
        report = digit_route_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["routes"], 46)
        self.assertEqual(report["routes_on_square"], 46)
        self.assertEqual(report["best_route"], "rail-both-4")
        self.assertEqual(report["best_quadgram"], -3.4242)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 40)
        self.assertEqual(report["shuffles_as_high"], 29)
        claim = consider_digit_routes()
        self.assertFalse(claim["digit_routes_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
