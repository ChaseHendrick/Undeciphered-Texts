"""Master Lock 1500-style reducer against a published known combination.

Source (fetched 2026-10-02):
https://jonwestfall.com/wp-content/uploads/2007/08/mlock1.pdf

Jon Westfall's guide records third number 19 and marks 7-9-19 as the
actual combination. The same pages state that the modulus rules leave
100 candidates (10 first numbers, 10 second numbers, 1 third number),
not the full 64,000 dial triples.

This checks that published reduction on one known combination. It is
not instructions for a specific physical lock and not a claim about
Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.master_lock import (
    FULL_BRUTE_FORCE,
    KNOWN_COMBINATION,
    KNOWN_COMBINATION_STRING,
    KNOWN_THIRD,
    METHOD_NAME,
    PUBLISHED_CANDIDATE_COUNT,
    SOURCE_URL,
    first_numbers,
    includes_combination,
    reduce_master_lock,
    second_numbers,
    solve_master_lock,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "master_lock_certificate.json"
)


class MasterLockScopeTest(unittest.TestCase):
    def test_module_documents_published_reduction_not_a_physical_lock(self) -> None:
        import engine.solvers.master_lock as master_lock_mod

        doc = master_lock_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("published math reduction", lowered)
        self.assertIn("not instructions", lowered)
        self.assertIn("specific physical lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("mlock1.pdf", SOURCE_URL)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class MasterLockPublishedReductionTest(unittest.TestCase):
    def test_third_19_matches_the_published_residue_classes(self) -> None:
        self.assertEqual(
            first_numbers(19),
            [3, 7, 11, 15, 19, 23, 27, 31, 35, 39],
        )
        self.assertEqual(
            set(second_numbers(19)),
            {1, 5, 9, 13, 17, 21, 25, 29, 33, 37},
        )

    def test_candidate_count_is_the_published_small_set(self) -> None:
        combos = reduce_master_lock(KNOWN_THIRD)
        self.assertEqual(len(combos), PUBLISHED_CANDIDATE_COUNT)
        self.assertEqual(len(combos), 100)
        self.assertEqual(FULL_BRUTE_FORCE, 64000)
        self.assertNotEqual(len(combos), FULL_BRUTE_FORCE)
        self.assertLess(len(combos), FULL_BRUTE_FORCE)
        for third in range(40):
            self.assertEqual(len(reduce_master_lock(third)), 100)

    def test_known_combination_is_included(self) -> None:
        self.assertEqual(KNOWN_COMBINATION, (7, 9, 19))
        self.assertEqual(KNOWN_COMBINATION_STRING, "7-9-19")
        self.assertIn(KNOWN_COMBINATION, reduce_master_lock(19))
        self.assertTrue(includes_combination(KNOWN_COMBINATION))

    def test_off_residue_triples_are_excluded(self) -> None:
        combos = set(reduce_master_lock(19))
        self.assertNotIn((4, 9, 19), combos)
        self.assertNotIn((7, 8, 19), combos)
        self.assertNotIn((7, 9, 18), combos)

    def test_solver_reports_method_count_and_scope(self) -> None:
        result = solve_master_lock(19)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.details["candidate_count"], 100)
        self.assertEqual(result.details["full_brute_force"], 64000)
        self.assertEqual(result.details["source_url"], SOURCE_URL)
        self.assertIn("7-9-19", result.plaintext)
        scope = result.details["scope"].lower()
        self.assertIn("published math reduction", scope)
        self.assertIn("not instructions", scope)
        self.assertIn("specific physical lock", scope)
        self.assertIn("nr. 86", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])


class MasterLockCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_matches_the_published_known_combination(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["known_combination"], KNOWN_COMBINATION_STRING)
        self.assertEqual(self.cert["third_number"], 19)
        self.assertEqual(self.cert["candidate_count"], 100)
        self.assertEqual(self.cert["source_url"], SOURCE_URL)
        digest = hashlib.sha256(KNOWN_COMBINATION_STRING.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        self.assertIn((7, 9, 19), reduce_master_lock(self.cert["third_number"]))
        self.assertEqual(
            len(reduce_master_lock(self.cert["third_number"])),
            self.cert["candidate_count"],
        )
        self.assertNotEqual(self.cert["candidate_count"], 64000)
        note = self.cert["note"].lower()
        self.assertIn("published math reduction", note)
        self.assertIn("one known combination", note)
        self.assertIn("not instructions for a specific physical lock", note)
        self.assertIn("not a claim about nr. 86", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)


if __name__ == "__main__":
    unittest.main()
