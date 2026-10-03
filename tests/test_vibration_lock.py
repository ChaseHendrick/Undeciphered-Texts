"""Synthetic vibration-trace lock: recover one planted combination.

The vibration trace is generated in code. The solver is given only that
trace. The signals are synthetic and this does not open a real safe.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import unittest
from pathlib import Path

from engine.solvers.vibration_lock import (
    METHOD_NAME,
    PLANTED_COMBINATION,
    PLANTED_COMBINATION_STRING,
    combination_string,
    planted_vibration_signal,
    recover_vibration_combination,
    solve_vibration_lock,
    synthesize_vibration,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "vibration_lock_certificate.json"
)


class VibrationLockScopeTest(unittest.TestCase):
    def test_module_documents_synthetic_signal_not_a_real_safe(self) -> None:
        import engine.solvers.vibration_lock as vibration_lock_mod

        doc = vibration_lock_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("synthetic", lowered)
        self.assertIn("does not open a real safe", lowered)
        self.assertIn("not instructions", lowered)
        self.assertIn("specific physical lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class VibrationLockRecoveryTest(unittest.TestCase):
    def test_solver_signature_accepts_only_the_signal(self) -> None:
        params = list(inspect.signature(solve_vibration_lock).parameters)
        self.assertEqual(params, ["signal"])
        recover_params = list(
            inspect.signature(recover_vibration_combination).parameters
        )
        self.assertEqual(recover_params, ["signal"])

    def test_planted_signal_recovers_the_planted_combination(self) -> None:
        signal = planted_vibration_signal()
        self.assertEqual(recover_vibration_combination(signal), PLANTED_COMBINATION)
        result = solve_vibration_lock(signal)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.plaintext, PLANTED_COMBINATION_STRING)
        self.assertEqual(result.key, PLANTED_COMBINATION_STRING)
        self.assertEqual(result.details["signal_kind"], "synthetic_vibration")
        self.assertEqual(result.details["combination"], PLANTED_COMBINATION_STRING)
        scope = result.details["scope"].lower()
        self.assertIn("synthetic", scope)
        self.assertIn("does not open a real safe", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])

    def test_each_dial_number_roundtrips_in_every_window(self) -> None:
        for number in range(40):
            combination = (number, (number + 7) % 40, (number + 19) % 40)
            signal = synthesize_vibration(combination)
            self.assertEqual(recover_vibration_combination(signal), combination)

    def test_short_trace_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_vibration_lock([0.0, 1.0])


class VibrationLockCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_matches_the_planted_combination(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["combination"], PLANTED_COMBINATION_STRING)
        digest = hashlib.sha256(
            PLANTED_COMBINATION_STRING.encode("utf-8")
        ).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        signal = planted_vibration_signal()
        self.assertEqual(
            combination_string(recover_vibration_combination(signal)),
            self.cert["combination"],
        )
        note = self.cert["note"].lower()
        self.assertIn("synthetic", note)
        self.assertIn("does not open a real safe", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)


if __name__ == "__main__":
    unittest.main()
