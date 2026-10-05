"""Two blocks copy a 2 by 2 of the square."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_tile import tile_report
from engine.solvers.dagapeyeff import consider_tile


class DagapeyeffTileTest(unittest.TestCase):
    def test_two_blocks_copy_one_square(self) -> None:
        report = tile_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["tiles"], 2)
        self.assertEqual(report["found"][0]["cells"], ["85", "84", "75", "74"])
        self.assertEqual(report["found"][1]["cells"], ["84", "75", "74", "85"])
        self.assertEqual(report["found"][0]["row"], 12)
        self.assertEqual(report["found"][0]["col"], 8)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 743)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_tile()
        self.assertIs(claim["tile_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
