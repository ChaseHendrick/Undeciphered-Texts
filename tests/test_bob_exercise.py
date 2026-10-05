"""Bob sees order in the solved exercise and not in the challenge."""

from __future__ import annotations

import unittest

from engine.bob_caution import bob_caution_report
from engine.bob_exercise import bob_exercise_report
from engine.solvers.dagapeyeff import consider_bob_exercise


class BobExerciseTest(unittest.TestCase):
    def test_the_exercise_uses_order_and_the_challenge_call_does_not(self) -> None:
        exercise = bob_exercise_report()
        challenge = bob_caution_report()
        self.assertIs(exercise["solved"], False)
        self.assertIsNone(exercise["claimed_plaintext"])
        self.assertTrue(exercise["weights_match_shipped"])
        self.assertFalse(exercise["weights_replaced"])
        self.assertEqual(exercise["exercise_family"], "substitution")
        self.assertEqual(exercise["exercise_shuffles_same_family"], 12)
        self.assertEqual(exercise["draws"], 40)
        self.assertTrue(exercise["exercise_uses_order"])
        self.assertEqual(challenge["challenge_shuffles_same_family"], 40)
        self.assertFalse(challenge["challenge_uses_order"])
        claim = consider_bob_exercise()
        self.assertTrue(claim["bob_exercise_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
