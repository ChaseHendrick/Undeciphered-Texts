"""Adversary attacks on the gates, and the regression that follows them."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_adversary import adversary_report


class DagapeyeffAdversaryTest(unittest.TestCase):
    def test_every_attack_is_blocked(self) -> None:
        report = adversary_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertTrue(report["all_blocked"])
        self.assertEqual(
            [attack["id"] for attack in report["attacks"]],
            [
                "disguised-check",
                "plaintext-on-a-refusal",
                "solved-flag-on-a-refusal",
                "frequency-clears-the-line",
                "solver-claims",
                "regression",
            ],
        )
        self.assertTrue(all(attack["blocked"] is True for attack in report["attacks"]))


if __name__ == "__main__":
    unittest.main()
