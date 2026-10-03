"""Synthetic click-train lock: recover one planted combination.

The click waveform is generated in code. The solver is given only that
waveform. The signals are synthetic and this does not open a real safe.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import unittest
from pathlib import Path

from engine.solvers.click_lock import (
    METHOD_NAME,
    PLANTED_COMBINATION,
    PLANTED_COMBINATION_STRING,
    combination_string,
    planted_click_signal,
    recover_click_combination,
    solve_click_lock,
    synthesize_clicks,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "click_lock_certificate.json"
)


class ClickLockScopeTest(unittest.TestCase):
    def test_module_documents_synthetic_signal_not_a_real_safe(self) -> None:
        import engine.solvers.click_lock as click_lock_mod

        doc = click_lock_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("synthetic", lowered)
        self.assertIn("does not open a real safe", lowered)
        self.assertIn("not instructions", lowered)
        self.assertIn("specific physical lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class ClickLockRecoveryTest(unittest.TestCase):
    def test_solver_signature_accepts_only_the_signal(self) -> None:
        params = list(inspect.signature(solve_click_lock).parameters)
        self.assertEqual(params, ["signal"])
        recover_params = list(inspect.signature(recover_click_combination).parameters)
        self.assertEqual(recover_params, ["signal"])

    def test_planted_signal_recovers_the_planted_combination(self) -> None:
        signal = planted_click_signal()
        self.assertEqual(recover_click_combination(signal), PLANTED_COMBINATION)
        result = solve_click_lock(signal)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.plaintext, PLANTED_COMBINATION_STRING)
        self.assertEqual(result.key, PLANTED_COMBINATION_STRING)
        self.assertEqual(result.details["signal_kind"], "synthetic_clicks")
        self.assertEqual(result.details["combination"], PLANTED_COMBINATION_STRING)
        scope = result.details["scope"].lower()
        self.assertIn("synthetic", scope)
        self.assertIn("does not open a real safe", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])

    def test_another_combination_is_read_from_its_own_signal(self) -> None:
        other = (0, 39, 1)
        signal = synthesize_clicks(other)
        self.assertEqual(recover_click_combination(signal), other)
        self.assertEqual(solve_click_lock(signal).plaintext, combination_string(other))

    def test_empty_signal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_click_lock([])


class ClickLockCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_matches_the_planted_combination(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["combination"], PLANTED_COMBINATION_STRING)
        digest = hashlib.sha256(PLANTED_COMBINATION_STRING.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["combination_sha256"])
        signal = planted_click_signal()
        self.assertEqual(
            combination_string(recover_click_combination(signal)),
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
