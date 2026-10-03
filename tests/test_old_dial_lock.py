"""Simulated old dial lock: recover one planted combination from a boolean.

The dial exists only inside this process. The simulator returns true
or false for a try and nothing else. The search must match the planted
combination, and a wrong try must fail.

This opens only the simulated lock inside the test, not a real safe.
It is not a procedure for a physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.old_dial_lock import (
    METHOD_NAME,
    PLANTED_COMBINATION,
    PLANTED_COMBINATION_STRING,
    SPACE_SIZE,
    combination_string,
    recover_combination,
    simulated_old_dial,
    solve_old_dial_lock,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "old_dial_lock_certificate.json"
)
DOC_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "old-dial-lock.md"
)

_SCOPE_SENTENCE = (
    "this opens only the simulated lock inside the test, not a real safe"
)


class OldDialLockScopeTest(unittest.TestCase):
    def test_module_documents_simulated_lock_only(self) -> None:
        import engine.solvers.old_dial_lock as dial_mod

        doc = dial_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn(_SCOPE_SENTENCE, lowered)
        self.assertIn("not a real safe", lowered)
        self.assertIn("boolean", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)
        note = DOC_PATH.read_text(encoding="utf-8")
        self.assertIn(_SCOPE_SENTENCE, note.lower())
        self.assertIn("not a real safe", note.lower())
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


class OldDialLockRecoveryTest(unittest.TestCase):
    def test_recovered_combination_matches_planted_and_wrong_try_fails(self) -> None:
        planted = PLANTED_COMBINATION
        self.assertEqual(planted, (3, 11, 7))
        self.assertEqual(combination_string(planted), PLANTED_COMBINATION_STRING)
        oracle = simulated_old_dial(planted)
        wrong = (3, 11, 8)
        self.assertNotEqual(wrong, planted)
        self.assertIs(oracle(wrong), False)
        self.assertIs(oracle((0, 0, 0)), False)
        self.assertIs(oracle(planted), True)
        found = recover_combination(oracle)
        self.assertEqual(found, planted)
        result = solve_old_dial_lock(oracle)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.plaintext, PLANTED_COMBINATION_STRING)
        self.assertEqual(result.details["space_size"], SPACE_SIZE)
        self.assertEqual(result.details["oracle"], "boolean_match_only")
        scope = result.details["scope"].lower()
        self.assertIn(_SCOPE_SENTENCE, scope)
        self.assertIn("not a real safe", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])


class OldDialLockCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = CERT_PATH.read_text(encoding="utf-8")
        self.cert = json.loads(self.raw)

    def test_certificate_combination_and_sha256(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["combination"], PLANTED_COMBINATION_STRING)
        self.assertEqual(self.cert["numbers"], [3, 11, 7])
        digest = hashlib.sha256(
            PLANTED_COMBINATION_STRING.encode("utf-8")
        ).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        note = self.cert["note"].lower()
        self.assertIn(_SCOPE_SENTENCE, note)
        self.assertIn("not a real safe", note)
        self.assertIn("nr. 86", note)
        self.assertNotIn("\u2014", self.raw)
        self.assertNotIn("\u2013", self.raw)
        oracle = simulated_old_dial(tuple(self.cert["numbers"]))
        self.assertFalse(oracle((0, 0, 1)))
        self.assertEqual(
            recover_combination(oracle),
            tuple(self.cert["numbers"]),
        )


if __name__ == "__main__":
    unittest.main()
