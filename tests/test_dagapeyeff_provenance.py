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
                ("convert", "a64782364904d7e20b9436212d93d90caa172f851d0b0442045943a013c9e549"),
                ("edits", "f662992893d0108c125b14cac1d20a30f7eafe2c58bf6bcc54e9dbc8b5744688"),
                ("corrections", "bf4a749875d9bbd6d318016e7b2a390778d0854257a2e2bb59c3f6acf524d929"),
                ("regroup", "56066cbfba47752377e800bb6816c837c2745467c1a47774fcb162a303a62309"),
                ("keys", "3fe9d3522a1017aa1348f5fa0dd561ccf8940a1bbff5fe6e8246a180c093ae37"),
                ("model", "0d050d25e8e1d2287335f78b6a8e891c0a10a751e9eaa5b7de93bdf7b1e52cf8"),
            ],
        )
        self.assertEqual(
            report["chain_sha256"],
            "5ff05c351d6dac071d3a572c83bf363be98b2206bd16f4b71783f83f179be40c",
        )
        self.assertEqual(report["entries"][0]["chain_sha256"], report["entries"][0]["content_sha256"])
        self.assertNotEqual(report["entries"][1]["chain_sha256"], report["entries"][1]["content_sha256"])


if __name__ == "__main__":
    unittest.main()
