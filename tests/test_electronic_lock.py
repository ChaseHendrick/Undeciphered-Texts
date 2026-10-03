"""Simulated electronic lock: recover one planted code from a boolean.

The keypad exists only inside this process. The simulator returns true
or false for a try and nothing else. The search must match the planted
code, and a wrong try must fail.

This opens only the simulated lock inside the test, not a real safe.
It is not a procedure for a physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.electronic_lock import (
    METHOD_NAME,
    PLANTED_CODE,
    PLANTED_CODE_STRING,
    SPACE_SIZE,
    code_string,
    recover_code,
    simulated_electronic_lock,
    solve_electronic_lock,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "electronic_lock_certificate.json"
)
DOC_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "electronic-lock.md"
)

_SCOPE_SENTENCE = (
    "this opens only the simulated lock inside the test, not a real safe"
)


class ElectronicLockScopeTest(unittest.TestCase):
    def test_module_documents_simulated_lock_only(self) -> None:
        import engine.solvers.electronic_lock as elec_mod

        doc = elec_mod.__doc__ or ""
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


class ElectronicLockRecoveryTest(unittest.TestCase):
    def test_recovered_code_matches_planted_and_wrong_try_fails(self) -> None:
        planted = PLANTED_CODE
        self.assertEqual(planted, (4, 8, 1, 6))
        self.assertEqual(code_string(planted), PLANTED_CODE_STRING)
        oracle = simulated_electronic_lock(planted)
        wrong = (4, 8, 1, 7)
        self.assertNotEqual(wrong, planted)
        self.assertIs(oracle(wrong), False)
        self.assertIs(oracle((0, 0, 0, 0)), False)
        self.assertIs(oracle(planted), True)
        found = recover_code(oracle)
        self.assertEqual(found, planted)
        result = solve_electronic_lock(oracle)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.plaintext, PLANTED_CODE_STRING)
        self.assertEqual(result.details["space_size"], SPACE_SIZE)
        self.assertEqual(result.details["oracle"], "boolean_match_only")
        scope = result.details["scope"].lower()
        self.assertIn(_SCOPE_SENTENCE, scope)
        self.assertIn("not a real safe", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])


class ElectronicLockCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = CERT_PATH.read_text(encoding="utf-8")
        self.cert = json.loads(self.raw)

    def test_certificate_code_and_sha256(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["code"], PLANTED_CODE_STRING)
        self.assertEqual(self.cert["digits"], [4, 8, 1, 6])
        digest = hashlib.sha256(
            PLANTED_CODE_STRING.encode("utf-8")
        ).hexdigest()
        self.assertEqual(digest, self.cert["code_sha256"])
        note = self.cert["note"].lower()
        self.assertIn(_SCOPE_SENTENCE, note)
        self.assertIn("not a real safe", note)
        self.assertIn("nr. 86", note)
        self.assertNotIn("\u2014", self.raw)
        self.assertNotIn("\u2013", self.raw)
        oracle = simulated_electronic_lock(tuple(self.cert["digits"]))
        self.assertFalse(oracle((0, 0, 0, 1)))
        self.assertEqual(
            recover_code(oracle),
            tuple(self.cert["digits"]),
        )


if __name__ == "__main__":
    unittest.main()
