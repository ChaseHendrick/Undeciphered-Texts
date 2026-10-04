"""The headless Truppenschlüssel roundtrips a known square and opens no residue."""

from __future__ import annotations

import unittest

from engine.headless_truppenschluessel import (
    HeadlessTruppenschluessel,
    residue_without_squares,
)


class HeadlessTruppenschluesselTest(unittest.TestCase):
    def test_known_squares_roundtrip_and_a_hole_does_not_slide(self) -> None:
        machine = HeadlessTruppenschluessel("FELD", "POST")
        cipher = machine.seal("ABCDEF")
        self.assertEqual(machine.feed(cipher), "ABCDEF")
        holed = cipher[:2] + "-" + cipher[3:]
        self.assertEqual(machine.feed(holed), "AB??EF")
        self.assertEqual(machine.feed(cipher[:2] + "J" + cipher[3:]), "AB??EF")
        self.assertEqual(machine.feed("A"), "?")

    def test_residue_messages_are_not_opened(self) -> None:
        report = residue_without_squares()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["blocked"]), 6)
        self.assertTrue(all(row["squares_published"] is False and row["opened"] is False for row in report["blocked"]))
        self.assertEqual(report["blocked"][0]["name"], "IASRZ_129")


if __name__ == "__main__":
    unittest.main()
