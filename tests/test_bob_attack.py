"""Pentest counts for the lifted ranking. The weight file stays."""

from __future__ import annotations

import unittest

from engine.bob_attack import bob_attack_report
from engine.bob_harden import accept_call, bob_harden_report, route_hardened
from engine.bob_lift import lifted_family
from engine.solvers.dagapeyeff import consider_bob_attack

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobAttackTest(unittest.TestCase):
    def test_disagreement_withholds_and_a_sure_lift_may_stand(self) -> None:
        self.assertFalse(accept_call("caesar", "vigenere", 0.9, False))
        self.assertFalse(accept_call("caesar", "caesar", 0.49, False))
        self.assertTrue(accept_call("caesar", "caesar", 0.5, False))
        self.assertTrue(accept_call("enigma", "enigma", 0.1, True))
        self.assertFalse(accept_call("enigma", "m209", 0.99, True))

    def test_lower_case_matches_the_folded_call(self) -> None:
        text = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG" * 3
        spaced = " ".join(text[index:index + 5] for index in range(0, len(text), 5)).lower()
        self.assertEqual(lifted_family(text), lifted_family(spaced))
        hardened = route_hardened(text)
        self.assertIsNone(hardened["claimed_plaintext"])
        self.assertFalse(hardened["weights_replaced"])
        self.assertIn("accepted", hardened)

    def test_attack_counts_and_the_gate_is_not_a_higher_score(self) -> None:
        report = bob_attack_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertEqual(report["texts"], 40)
        self.assertEqual(report["clean_correct"], 38)
        self.assertEqual(report["deletion_flips"], 14)
        self.assertEqual(report["reverse_flips"], 18)
        self.assertEqual(report["insertion_flips"], 18)
        self.assertEqual(report["case_mismatches"], 0)
        self.assertEqual(report["hardened_correct"], 24)
        self.assertEqual(report["hardened_withheld"], 15)
        self.assertEqual(report["hardened_wrong"], 1)
        self.assertEqual(report["plain_certain"], 20)
        self.assertEqual(report["plain_draws"], 20)
        self.assertEqual(report["plain_peak"], 0.94)
        self.assertEqual(report["random_certain"], 6)
        self.assertEqual(report["random_draws"], 8)
        self.assertEqual(report["random_peak"], 0.9814)
        self.assertTrue(report["short_rejected"])
        self.assertTrue(report["digit_rejected"])
        self.assertFalse(report["hardened_promoted_as_accuracy"])
        gate = bob_harden_report()
        self.assertFalse(gate["promoted_as_accuracy"])
        self.assertEqual(gate["probability_cutoff"], 0.5)
        self.assertEqual(gate["weights_sha256"], _SHIPPED)
        claim = consider_bob_attack()
        self.assertFalse(claim["bob_attack_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
