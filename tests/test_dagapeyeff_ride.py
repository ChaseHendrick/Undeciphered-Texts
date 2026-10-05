"""An echoed triple rides on another spaced triple."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_ride import ride_report
from engine.solvers.dagapeyeff import consider_ride


class DagapeyeffRideTest(unittest.TestCase):
    def test_the_echo_rides_on_a_triple(self) -> None:
        report = ride_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["ride_count"], 1)
        ride = report["rides"][0]
        self.assertEqual(ride["echo_cell"], "62")
        self.assertEqual(ride["echo_axis"], "row")
        self.assertEqual(ride["lines"], [5, 11])
        self.assertEqual(ride["carrier_cell"], "85")
        self.assertEqual(ride["carrier_axis"], "column")
        self.assertEqual(ride["carrier_seats"], [5, 8, 11])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 335)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_ride()
        self.assertIs(claim["ride_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
