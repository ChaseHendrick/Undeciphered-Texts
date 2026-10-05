"""The solver judge blocks a solved flag and checks a forward map."""

from __future__ import annotations

import unittest

from engine.ciphers import caesar_encrypt, vigenere_encrypt
from engine.solver_judge import judge_any, judge_claim, judge_solve_result, reencryption_matches
from engine.solvers.beaufort import beaufort_encrypt
from engine.solvers.caesar import solve_caesar


class SolverJudgeTest(unittest.TestCase):
    def test_a_historical_solved_flag_is_blocked_and_not_copied(self) -> None:
        claim = judge_claim({
            "solved": True,
            "claimed_plaintext": "A SENTENCE THAT MUST NOT COME BACK",
            "target": "dagapeyeff",
            "score": float("nan"),
        })
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertFalse(claim["accepted"])
        self.assertIn("solved_flag", claim["blocks"])
        self.assertIn("plaintext_stored", claim["blocks"])
        self.assertIn("historical_solved", claim["blocks"])
        self.assertIn("nonfinite_score", claim["blocks"])
        self.assertNotIn("SENTENCE", str(claim))

    def test_caesar_vigenere_and_beaufort_roundtrips(self) -> None:
        plain = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        caesar = caesar_encrypt(plain, 5)
        self.assertTrue(reencryption_matches("caesar", plain, "5", caesar))
        self.assertFalse(reencryption_matches("caesar", plain, "4", caesar))
        vigenere = vigenere_encrypt(plain, "SECRET")
        self.assertTrue(reencryption_matches("vigenere", plain, "SECRET", vigenere))
        self.assertFalse(reencryption_matches("vigenere", plain, "SECRETS", vigenere))
        beaufort = beaufort_encrypt(plain, "CODE")
        self.assertTrue(reencryption_matches("beaufort", plain, "CODE", beaufort))
        self.assertIsNone(reencryption_matches("playfair", plain, "CODE", beaufort))
        judged = judge_solve_result(solve_caesar(caesar), caesar)
        self.assertIs(judged["solved"], False)
        self.assertIsNone(judged["claimed_plaintext"])
        self.assertTrue(judged["reencryption_matches"])
        self.assertTrue(judged["accepted"])
        self.assertNotIn("QUICK", str(judged))
        blocked = judge_any({"solved": True, "method": "k4", "reencryption_matches": False})
        self.assertFalse(blocked["accepted"])
        self.assertIs(blocked["solved"], False)


if __name__ == "__main__":
    unittest.main()
