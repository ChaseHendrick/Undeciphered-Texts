"""Pressure and pinpricks are read only when the caller supplies the channel."""

from __future__ import annotations

import unittest

from engine.pen_pressure import ink_alone, read_pinpricks, read_pressure
from engine.solvers.baconian import baconian_encode


class PenPressureTest(unittest.TestCase):
    def test_heavy_and_light_roundtrip_and_ink_does_not(self) -> None:
        marks = baconian_encode("HI", variant="24").upper().replace("A", "L").replace("B", "H")
        report = read_pressure(marks)
        self.assertEqual(report["text"], "HI")
        self.assertIs(report["solved"], False)
        self.assertIsNone(ink_alone("HELLO")["text"])
        with self.assertRaises(ValueError):
            read_pressure("HELLO")

    def test_pinpricks_are_positions_not_a_guess(self) -> None:
        report = read_pinpricks("the cat", [4, 5, 6])
        self.assertEqual(report["text"], "CAT")
        self.assertIs(report["solved"], False)
        with self.assertRaises(ValueError):
            read_pinpricks("the cat", [])


if __name__ == "__main__":
    unittest.main()
