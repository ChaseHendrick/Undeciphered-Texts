"""Published readings checked against the counts the cells force."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_claims import claims_report
from engine.solvers.dagapeyeff import consider_claims


class DagapeyeffClaimsTest(unittest.TestCase):
    def test_no_published_reading_survives_the_counts(self) -> None:
        report = claims_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cell_profile"], [20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11, 11, 9, 3, 2, 1, 1, 1])
        rows = {row["id"]: row for row in report["claims"]}
        self.assertEqual(rows["tony-2014"]["letters"], 196)
        self.assertEqual(rows["tony-2014"]["distinct_letters"], 23)
        self.assertFalse(rows["tony-2014"]["fits_inside_cells"])
        self.assertGreater(rows["vento-2026"]["distinct_letters"], 18)
        self.assertEqual(len(rows["vento-2026"]["one_coordinate_many_letters"]["(1,4) (2,3)"]), 4)
        self.assertIn("N", rows["officialchaos-2026"]["letters_outside_own_key"])
        self.assertFalse(rows["triggernick"]["inside_book_dummy_rule"])
        self.assertEqual(rows["uygun-2026"]["cribs_imposed"], ["ASSESSED", "ATTACK"])
        self.assertEqual(report["full_length_claims_with_cell_profile"], 0)
        claim = consider_claims()
        self.assertFalse(claim["claims_allowed"])
        self.assertIs(claim["solved"], False)


if __name__ == "__main__":
    unittest.main()
