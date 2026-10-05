"""A spaced triple is echoed in a parallel line."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_echo import echo_report
from engine.solvers.dagapeyeff import consider_echo


class DagapeyeffEchoTest(unittest.TestCase):
    def test_two_spaced_triples_are_echoed(self) -> None:
        report = echo_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["echo_count"], 2)
        first, second = report["echoes"]
        self.assertEqual(first["cell"], "62")
        self.assertEqual(first["axis"], "row")
        self.assertEqual(first["index"], 11)
        self.assertEqual(first["seats"], [6, 8, 10])
        self.assertEqual(first["echo"], 5)
        self.assertEqual(first["echoed"], [6, 8])
        self.assertEqual(second["cell"], "82")
        self.assertEqual(second["axis"], "column")
        self.assertEqual(second["index"], 2)
        self.assertEqual(second["seats"], [0, 6, 12])
        self.assertEqual(second["echo"], 7)
        self.assertEqual(second["echoed"], [6, 12])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 932)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_echo()
        self.assertIs(claim["echo_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
