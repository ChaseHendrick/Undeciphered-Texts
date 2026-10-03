"""Simplex five-button enumerator against a published factory default.

Source (fetched 2026-10-02):
https://ekman.cx/articles/simplex_locks/

Patrick Ekman's pattern table sums to 1081. The same page names the
factory default "2+4, 3". A sequence-only reading of all five buttons
is 120, which the page gives as the first-glance figure.

This checks that published set on one known combination. It is not
instructions for a specific physical lock and not a claim about
Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from itertools import permutations
from pathlib import Path

from engine.solvers.simplex_lock import (
    KNOWN_COMBINATION_STRING,
    METHOD_NAME,
    PUBLISHED_CANDIDATE_COUNT,
    SEQUENCE_ONLY_ALL_FIVE,
    SOURCE_URL,
    includes_combination,
    reduce_simplex,
    solve_simplex,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "simplex_lock_certificate.json"
)


class SimplexScopeTest(unittest.TestCase):
    def test_module_documents_published_set_not_a_physical_lock(self) -> None:
        import engine.solvers.simplex_lock as simplex_mod

        doc = simplex_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("published math", lowered)
        self.assertIn("not instructions", lowered)
        self.assertIn("specific physical lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("ekman.cx/articles/simplex_locks", SOURCE_URL)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class SimplexPublishedSetTest(unittest.TestCase):
    def test_candidate_count_is_the_published_total(self) -> None:
        combos = reduce_simplex()
        self.assertEqual(len(combos), PUBLISHED_CANDIDATE_COUNT)
        self.assertEqual(len(combos), 1081)
        self.assertEqual(len(set(combos)), 1081)
        self.assertEqual(SEQUENCE_ONLY_ALL_FIVE, 120)
        self.assertGreater(len(combos), SEQUENCE_ONLY_ALL_FIVE)

    def test_known_factory_default_is_included(self) -> None:
        self.assertEqual(KNOWN_COMBINATION_STRING, "2+4, 3")
        self.assertIn(KNOWN_COMBINATION_STRING, reduce_simplex())
        self.assertTrue(includes_combination(KNOWN_COMBINATION_STRING))

    def test_all_five_sequences_are_included_and_repeats_are_not(self) -> None:
        combos = set(reduce_simplex())
        sequences = [
            ", ".join(str(button) for button in perm)
            for perm in permutations((1, 2, 3, 4, 5), 5)
        ]
        self.assertEqual(len(sequences), 120)
        self.assertTrue(all(seq in combos for seq in sequences))
        self.assertIn("3", combos)
        self.assertNotIn("2+4, 2", combos)
        self.assertNotIn("4+2, 3", combos)

    def test_solver_reports_method_count_and_scope(self) -> None:
        result = solve_simplex()
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.details["candidate_count"], 1081)
        self.assertEqual(result.details["sequence_only_all_five"], 120)
        self.assertEqual(result.details["source_url"], SOURCE_URL)
        self.assertIn("2+4, 3", result.plaintext.splitlines())
        scope = result.details["scope"].lower()
        self.assertIn("published math", scope)
        self.assertIn("not instructions", scope)
        self.assertIn("specific physical lock", scope)
        self.assertIn("nr. 86", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])


class SimplexCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_matches_the_published_factory_default(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["known_combination"], KNOWN_COMBINATION_STRING)
        self.assertEqual(self.cert["candidate_count"], 1081)
        self.assertEqual(self.cert["source_url"], SOURCE_URL)
        digest = hashlib.sha256(KNOWN_COMBINATION_STRING.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        self.assertIn("2+4, 3", reduce_simplex())
        self.assertEqual(len(reduce_simplex()), self.cert["candidate_count"])
        self.assertNotEqual(self.cert["candidate_count"], 120)
        note = self.cert["note"].lower()
        self.assertIn("published math", note)
        self.assertIn("one known combination", note)
        self.assertIn("not instructions for a specific physical lock", note)
        self.assertIn("not a claim about nr. 86", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)


if __name__ == "__main__":
    unittest.main()
