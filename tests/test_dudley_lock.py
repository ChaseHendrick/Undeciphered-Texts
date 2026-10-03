"""Dudley 60-position reducer against a published worked pair list.

Source (fetched 2026-10-02):
https://jameshowell.wordpress.com/2010/09/04/hack-a-dudley-lock-in-10-minutes/

James Howell's worked example uses positions 2, 8, 14, 20, 26, 32, 38,
44, 50, and 56. He prints 45 pairs whose second number is lower than
the first, beginning with 8-2, and he states the sum
9+8+7+6+5+4+3+2+1 is 45. He does not mark one pair as the combination
that opened the lock.

This checks that published list on the pair the page prints first.
It is not instructions for a specific physical lock and not a claim
about Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.dudley_lock import (
    FULL_BRUTE_FORCE,
    KNOWN_COMBINATION,
    KNOWN_COMBINATION_STRING,
    METHOD_NAME,
    PUBLISHED_CANDIDATE_COUNT,
    PUBLISHED_POSITIONS,
    SOURCE_URL,
    WORKED_FIRST_POSITION,
    combination_string,
    dial_positions,
    includes_combination,
    reduce_dudley,
    solve_dudley,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "dudley_lock_certificate.json"
)

# The 45 pairs printed on the page, in the page's order.
PUBLISHED_PAIRS = [
    "8-2", "14-2", "20-2", "26-2", "32-2", "38-2", "44-2", "50-2", "56-2",
    "14-8", "20-8", "26-8", "32-8", "38-8", "44-8", "50-8", "56-8",
    "20-14", "26-14", "32-14", "38-14", "44-14", "50-14", "56-14",
    "26-20", "32-20", "38-20", "44-20", "50-20", "56-20",
    "32-26", "38-26", "44-26", "50-26", "56-26",
    "38-32", "44-32", "50-32", "56-32",
    "44-38", "50-38", "56-38",
    "50-44", "56-44",
    "56-50",
]


class DudleyScopeTest(unittest.TestCase):
    def test_module_documents_published_reduction_not_a_physical_lock(self) -> None:
        import engine.solvers.dudley_lock as dudley_mod

        doc = dudley_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("published math", lowered)
        self.assertIn("not instructions", lowered)
        self.assertIn("specific physical lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("hack-a-dudley-lock-in-10-minutes", SOURCE_URL)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class DudleyPublishedReductionTest(unittest.TestCase):
    def test_worked_positions_match_the_page(self) -> None:
        self.assertEqual(dial_positions(WORKED_FIRST_POSITION), list(PUBLISHED_POSITIONS))
        self.assertEqual(
            list(PUBLISHED_POSITIONS),
            [2, 8, 14, 20, 26, 32, 38, 44, 50, 56],
        )

    def test_candidate_count_is_the_published_small_set(self) -> None:
        combos = reduce_dudley(WORKED_FIRST_POSITION)
        self.assertEqual(len(combos), PUBLISHED_CANDIDATE_COUNT)
        self.assertEqual(len(combos), 45)
        self.assertEqual(len(PUBLISHED_PAIRS), 45)
        self.assertEqual(FULL_BRUTE_FORCE, 216000)
        self.assertLess(len(combos), FULL_BRUTE_FORCE)
        self.assertEqual(
            [combination_string(combo) for combo in combos],
            PUBLISHED_PAIRS,
        )

    def test_known_combination_is_included(self) -> None:
        self.assertEqual(KNOWN_COMBINATION, (8, 2))
        self.assertEqual(KNOWN_COMBINATION_STRING, "8-2")
        self.assertIn(KNOWN_COMBINATION, reduce_dudley(2))
        self.assertTrue(includes_combination(KNOWN_COMBINATION))

    def test_pairs_outside_the_rule_are_excluded(self) -> None:
        combos = set(reduce_dudley(2))
        self.assertNotIn((2, 8), combos)
        self.assertNotIn((8, 14), combos)
        self.assertNotIn((7, 2), combos)

    def test_solver_reports_method_count_and_scope(self) -> None:
        result = solve_dudley(2)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.details["candidate_count"], 45)
        self.assertEqual(result.details["full_brute_force"], 216000)
        self.assertEqual(result.details["source_url"], SOURCE_URL)
        self.assertIn("8-2", result.plaintext.splitlines())
        scope = result.details["scope"].lower()
        self.assertIn("published math", scope)
        self.assertIn("not instructions", scope)
        self.assertIn("specific physical lock", scope)
        self.assertIn("nr. 86", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])


class DudleyCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_matches_the_published_worked_pair(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["known_combination"], KNOWN_COMBINATION_STRING)
        self.assertEqual(self.cert["first_position"], 2)
        self.assertEqual(self.cert["candidate_count"], 45)
        self.assertEqual(self.cert["source_url"], SOURCE_URL)
        digest = hashlib.sha256(KNOWN_COMBINATION_STRING.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        self.assertIn((8, 2), reduce_dudley(self.cert["first_position"]))
        self.assertEqual(
            len(reduce_dudley(self.cert["first_position"])),
            self.cert["candidate_count"],
        )
        self.assertNotEqual(self.cert["candidate_count"], 216000)
        note = self.cert["note"].lower()
        self.assertIn("published math", note)
        self.assertIn("worked example", note)
        self.assertIn("not instructions for a specific physical lock", note)
        self.assertIn("not a claim about nr. 86", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)


if __name__ == "__main__":
    unittest.main()
