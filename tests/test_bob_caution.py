"""Bob refuses a family call that a shuffle also gets. Weights stay put."""

from __future__ import annotations

import unittest

from engine.bob_caution import bob_caution_report
from engine.solvers.dagapeyeff import consider_bob

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobCautionTest(unittest.TestCase):
    def test_the_challenge_call_does_not_use_order(self) -> None:
        report = bob_caution_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["draws"], 40)
        self.assertEqual(report["challenge_family"], "substitution")
        self.assertEqual(report["challenge_probability"], 0.969)
        self.assertIs(report["challenge_uncertain"], False)
        self.assertEqual(report["challenge_shuffles_same_family"], 40)
        self.assertEqual(report["challenge_shuffles_as_confident"], 25)
        self.assertFalse(report["challenge_uses_order"])
        self.assertEqual(report["control_family"], "caesar")
        self.assertEqual(report["control_probability"], 0.9492)
        self.assertEqual(report["control_shuffles_same_family"], 0)
        self.assertTrue(report["control_uses_order"])
        claim = consider_bob()
        self.assertFalse(claim["bob_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
