"""The cells and the scores that depend on them hash to a fixed chain."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_provenance import provenance_report


class DagapeyeffProvenanceTest(unittest.TestCase):
    def test_the_chain_recomputes(self) -> None:
        report = provenance_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(
            [(entry["name"], entry["content_sha256"]) for entry in report["entries"]],
            [
                ("cells", "f2460a6acdf2f50e12fdc8760c39753746d885282cd0bdfd0eec877c56e6fae5"),
                ("yardstick", "e12910ac3d3d0460db9ce76719298d94f261b7a8a17f09fec675dc4cda635d66"),
                ("balls", "3b84e9af30916cf42181a75d847eff6ba0cc992f606a069fe8fcfc5af0227bdd"),
                ("record", "834058b318779e3811b0b19408329f702bbf3577623dc17912af55c62efc80f7"),
            ],
        )
        self.assertEqual(
            report["chain_sha256"],
            "ce7d38c98d060ee26a038f8a7f5b1849b1f30996eeda15c6955c74912370b455",
        )
        self.assertEqual(report["entries"][0]["chain_sha256"], report["entries"][0]["content_sha256"])
        self.assertNotEqual(report["entries"][1]["chain_sha256"], report["entries"][1]["content_sha256"])


if __name__ == "__main__":
    unittest.main()
