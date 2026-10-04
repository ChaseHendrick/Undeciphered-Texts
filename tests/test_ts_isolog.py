"""A repeated-pair slide can find a planted formula and still claim nothing."""

from __future__ import annotations

import unittest

from engine.ciphers import square_from_keyword, two_square_encrypt
from engine.ts_close_pairs import IASRZ_129
from engine.ts_isolog import search_ts_isolog, slide


class TsIsologTest(unittest.TestCase):
    def test_planted_formula_is_found_and_the_residue_is_not_read(self) -> None:
        planted = two_square_encrypt(
            "XXXXKOMMANDANTXXXXYYYY",
            square_from_keyword("FELD"),
            square_from_keyword("POST"),
        )
        self.assertIn(4, [hit["start"] for hit in slide("KOMMANDANT", planted)])
        report = search_ts_isolog()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["iasrz_joint_agreeing"], 0)
        by_text = {row["text"]: row for row in report["texts"]}
        self.assertEqual(by_text["IASRZ_129"]["informative"], 3)
        self.assertEqual(by_text["IASRZ_130"]["informative"], 0)
        self.assertEqual(by_text["DSZPZ"]["informative"], 0)
        longs = {
            row["phrase"]: row
            for row in by_text["IASRZ_129"]["phrases"]
        }
        self.assertEqual(longs["UNTERKUNFT"]["informative"], 3)
        self.assertEqual(
            [hit["start"] for hit in slide("UNTERKUNFT", IASRZ_129)],
            [40, 60, 64],
        )


if __name__ == "__main__":
    unittest.main()
