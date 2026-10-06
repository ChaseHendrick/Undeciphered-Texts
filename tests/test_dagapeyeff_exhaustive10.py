"""Width 10: power holds only for the done direction, and there the cells do not stand out."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_exhaustive10 import exhaustive10_report
from engine.solvers.dagapeyeff import consider_exhaustive10


class DagapeyeffExhaustive10Test(unittest.TestCase):
    def test_power_is_gone_for_two_families_and_the_cells_are_flat_in_the_third(self) -> None:
        report = exhaustive10_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        rows = {row["family"]: row for row in report["rows"]}
        for family in ("columnar-undone", "periodic"):
            self.assertLess(min(plant["excess"] for plant in rows[family]["planted"]), 0)
        done = rows["columnar-done"]
        weakest = min(plant["excess"] for plant in done["planted"])
        self.assertGreater(weakest, 0.1)
        self.assertLess(done["cells"]["excess"], weakest)
        self.assertLess(done["regrouped"]["excess"], weakest)
        claim = consider_exhaustive10()
        self.assertFalse(claim["exhaustive10_allowed"])


if __name__ == "__main__":
    unittest.main()
