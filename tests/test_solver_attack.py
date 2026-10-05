"""Solver drills stay forward checks. A wrong key can still re-encrypt."""

from __future__ import annotations

import unittest

from engine.solver_attack import harden_result, solver_attack_report
from engine.solvers.beaufort import beaufort_encrypt, solve_beaufort
from engine.solvers.dagapeyeff import consider_solver_attack


class SolverAttackTest(unittest.TestCase):
    def test_a_wrong_beaufort_key_still_reencrypts_and_is_not_exact(self) -> None:
        cipher = beaufort_encrypt("DEFENDTHEEASTWALLOFTHECASTLE", "FORTIFICATION")
        wrong = solve_beaufort(cipher, key="QQQQ")
        judged = harden_result(wrong, cipher)
        self.assertTrue(judged["consistent"])
        self.assertTrue(judged["kept"])
        self.assertIs(judged["solved"], False)
        self.assertIsNone(judged["claimed_plaintext"])
        self.assertTrue(judged["reading_flag_is_not_a_recovery"])

    def test_the_drill_is_not_an_accuracy_promotion(self) -> None:
        report = solver_attack_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["weights_replaced"])
        self.assertFalse(report["promoted_as_accuracy"])
        self.assertTrue(report["reading_flag_is_not_a_recovery"])
        self.assertTrue(report["reencryption_cannot_see_a_wrong_key"])
        self.assertEqual(report["caesar_exact"], 8)
        self.assertEqual(report["caesar_delete_holds"], 8)
        self.assertEqual(report["caesar_case_exact"], 8)
        self.assertEqual(report["vigenere_exact"], 6)
        self.assertEqual(report["vigenere_delete_holds"], 0)
        self.assertEqual(report["vigenere_case_exact"], 6)
        self.assertEqual(report["caesar_on_vigenere_exact"], 0)
        self.assertEqual(report["beaufort_exact"], 6)
        self.assertEqual(report["beaufort_wrong_key_exact"], 0)
        self.assertEqual(report["beaufort_wrong_key_still_consistent"], 6)
        self.assertEqual(report["affine_exact"], 4)
        self.assertEqual(report["affine_wrong_key_exact"], 0)
        self.assertEqual(report["affine_wrong_key_still_consistent"], 4)
        self.assertTrue(report["affine_wikipedia_roundtrip"])
        self.assertEqual(report["substitution_exact"], 0)
        self.assertEqual(report["substitution_consistent"], 2)
        self.assertEqual(report["substitution_reading_flag"], 2)
        self.assertEqual(report["substitution_reading_but_wrong"], 2)
        self.assertEqual(report["rejected_inputs"], 3)
        claim = consider_solver_attack()
        self.assertFalse(claim["solver_attack_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
