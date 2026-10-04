"""Innovative K4 lanes stay unsolved, and the Gromark obstruction has a control."""

from __future__ import annotations

import unittest

from engine.k4_gromark_obstruction import (
    empty_domain_letters,
    crib_pairs,
    search_k4_gromark_obstruction,
)
from engine.k4_quagmire_panel import search_k4_quagmire_panel
from engine.solvers.gromark import gromark_encrypt
from engine.solvers.k4_attempt import K4_CIPHERTEXT


def _synthetic_plain() -> str:
    body = ["A"] * 97
    for start, word in ((21, "EASTNORTHEAST"), (63, "BERLINCLOCK")):
        body[start : start + len(word)] = list(word)
    return "".join(body)


class K4GromarkObstructionTest(unittest.TestCase):
    def test_synthetic_gromark_is_not_blocked(self) -> None:
        cipher = gromark_encrypt(_synthetic_plain(), "KRYPTOS 12345")
        self.assertEqual(empty_domain_letters(crib_pairs(cipher)), ())

    def test_k4_gromark_lane_blocks_without_claiming_plaintext(self) -> None:
        report = search_k4_gromark_obstruction()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["in_place_blocked_letters"], ("F", "K", "P"))
        self.assertEqual(report["periodic_crib_hits"], 0)
        self.assertEqual(report["myszkowski_crib_hits"], 0)
        self.assertEqual(len(report["compositions"]), 3)
        for row in report["compositions"]:
            self.assertTrue(row["gromark_myszkowski_blocked"])
            self.assertTrue(row["orders_agree"])
        self.assertEqual(len(K4_CIPHERTEXT), 97)


class K4QuagmirePanelTest(unittest.TestCase):
    def test_panel_covers_the_declared_settings_and_claims_nothing(self) -> None:
        report = search_k4_quagmire_panel()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["crib_hits"], 0)
        for name, tally in report["tallies"].items():
            self.assertEqual(tally["tried"] + tally["rejected"], report["expected"][name])
            self.assertEqual(tally["crib_hits"], 0)
            self.assertGreater(tally["tried"], 0)


if __name__ == "__main__":
    unittest.main()
