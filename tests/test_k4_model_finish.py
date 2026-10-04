"""Import check for the K4 family finish. The default suite does not run it.

finish_k4_models covers 32512 hypotheses per fold. That full run stays behind
engine.k4_model_finish main. A three-check search is enough to show the
tiny call is not the full space and that claimed_plaintext stays None.
"""
from __future__ import annotations

import unittest

from engine.k4_model_finish import classify_reserved, finish_k4_models
from engine.k4_models import search_k4_models
from engine.reverse_engineer import Crib
from engine.solvers.k4_attempt import K4_CIPHERTEXT


class K4ModelFinishTest(unittest.TestCase):
    def test_finish_is_importable_and_a_tiny_search_is_not_the_full_space(self):
        self.assertTrue(callable(finish_k4_models))
        result = search_k4_models(
            K4_CIPHERTEXT,
            cribs=(Crib(21, "EASTNORTHEAST"),),
            families=("repeating",),
            max_checks=3,
            max_period=32,
            max_width=32,
            max_candidates=3,
        )
        self.assertIsNone(result["claimed_plaintext"])
        self.assertEqual(result["checks"], 3)
        self.assertFalse(result["search_complete"])
        self.assertLess(result["checks"], 32512)
        self.assertEqual(result["requested_models"], 8128)
        for candidate in result["candidates"]:
            self.assertIsNone(candidate["claimed_plaintext"])

    def test_reserved_status_counts_contradictions_and_requires_a_complete_key(self):
        reserved = Crib(0, "BERLIN")
        exact = {
            "predicted_plaintext": "BERLIN????",
            "key_complete": True,
            "key_shift_indices": [1, 2],
            "claimed_plaintext": None,
        }
        self.assertEqual(classify_reserved(exact, reserved), "exact")
        self.assertEqual(classify_reserved({
            "predicted_plaintext": "BERLIN????",
            "key_complete": False,
            "key_shift_indices": [1, None],
            "claimed_plaintext": None,
        }, reserved), "incomplete_span_match")
        contradicted = dict(exact)
        contradicted["predicted_plaintext"] = "BXRLIN????"
        self.assertEqual(classify_reserved(contradicted, reserved), "contradiction")
        # A question mark does not hide a determined mismatch.
        self.assertEqual(classify_reserved({
            "predicted_plaintext": "B?RLXN????",
            "key_complete": False,
            "key_shift_indices": [None, None],
            "claimed_plaintext": None,
        }, reserved), "contradiction")
        self.assertEqual(classify_reserved({
            "predicted_plaintext": "BE?LIN????",
            "key_complete": True,
            "key_shift_indices": [1, 2],
            "claimed_plaintext": None,
        }, reserved), "underdetermined")
        self.assertIsNone(exact["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
