"""Hill heldout on K4 must not emit a claimed plaintext.

The 97-letter ciphertext is an odd length. The search records that limit
instead of raising.
"""

from __future__ import annotations

import unittest

from engine.k4_hill_heldout import search_k4_hill_endpoints, search_k4_hill_heldout


class K4HillHeldoutTest(unittest.TestCase):
    def test_odd_length_handling_does_not_claim_a_plaintext(self) -> None:
        report = search_k4_hill_heldout()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["ciphertext_letters"], 97)
        self.assertIsInstance(report["candidates_checked"], int)
        self.assertIsInstance(report["reserved_matches"], int)
        self.assertEqual(report["candidates_checked"], 0)
        self.assertEqual(report["reserved_matches"], 0)
        self.assertIn("two-letter blocks", report["limitation"])
        self.assertEqual(len(report["folds"]), 2)
        for fold in report["folds"]:
            self.assertFalse(fold["reserved_passed_to_fitter"])
            self.assertFalse(fold["search_ran"])
        for item in report["unverified"]:
            self.assertEqual(item["status"], "unverified")

    def test_endpoint_windows_do_not_claim_a_plaintext(self) -> None:
        report = search_k4_hill_endpoints()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["padding"])
        self.assertEqual(report["window_letters"], 96)
        self.assertEqual(len(report["folds"]), 4)
        self.assertEqual(report["reserved_matches"], 0)
        self.assertEqual(report["candidates_checked"], 0)
        for fold in report["folds"]:
            self.assertFalse(fold["reserved_passed_to_fitter"])
            self.assertTrue(fold["search_complete"])
            self.assertEqual(fold["compatible_keys_seen"], 0)


if __name__ == "__main__":
    unittest.main()
