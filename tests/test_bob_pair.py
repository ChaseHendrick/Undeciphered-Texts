"""The Enigma versus M-209 vote is not allowed to replace Bob."""

from __future__ import annotations

import unittest

from engine.bob_pair import bob_pair_report
from engine.solvers.dagapeyeff import consider_bob_pair

_SHIPPED = "5c271f426812d6307f208a636b80f820201e25b3dc6778333e5d08d4d5aaaf4b"


class BobPairTest(unittest.TestCase):
    def test_the_side_vote_loses_the_older_benchmark(self) -> None:
        report = bob_pair_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["weights_sha256"], _SHIPPED)
        self.assertFalse(report["weights_replaced"])
        self.assertTrue(report["weights_match_shipped"])
        self.assertEqual(report["train_correct"], 155)
        self.assertEqual(report["train_total"], 200)
        self.assertEqual(report["held_before"], 429)
        self.assertEqual(report["held_after"], 435)
        self.assertEqual(report["held_total"], 480)
        self.assertEqual(report["held_flips"], 8)
        self.assertEqual(report["benchmark_before"], 193)
        self.assertEqual(report["benchmark_after"], 192)
        self.assertEqual(report["benchmark_total"], 204)
        self.assertEqual(report["benchmark_flips"], 5)
        self.assertFalse(report["promoted"])
        claim = consider_bob_pair()
        self.assertFalse(claim["bob_pair_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("weights stay", claim["learned"])


if __name__ == "__main__":
    unittest.main()
