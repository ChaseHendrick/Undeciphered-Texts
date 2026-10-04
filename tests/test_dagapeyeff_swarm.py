"""The D'Agapeyeff challenge is a Polybius grid that does not fit English counts."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_swarm import search_dagapeyeff


class DagapeyeffSwarmTest(unittest.TestCase):
    def test_cells_fit_the_square_and_not_english(self) -> None:
        report = search_dagapeyeff()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["challenge_pairs"], 196)
        self.assertEqual(report["distinct_cells"], 18)
        self.assertEqual(report["grid"], "14 by 14")
        self.assertEqual(report["challenge_chi_square"], 34.23)
        self.assertEqual(report["control_chi_square"], 4.14)
        self.assertIs(report["challenge_closer_to_english"], False)
        self.assertEqual(report["digram_z"], -0.74)
        self.assertEqual(report["shuffles"], 200)


if __name__ == "__main__":
    unittest.main()
