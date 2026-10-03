"""Simulated pin-tumbler, wafer, and keypad locks.

Each model returns only yes or no. The search must recover the planted
secret for that model, and a wrong guess must be false.

This opens only the simulated lock inside the test, not a real lock.
It is not a procedure for a physical lock and not a claim about Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.lockpicks import (
    METHOD_NAME,
    PLANTED_KEYPAD_DIGITS,
    PLANTED_KEYPAD_KEY,
    PLANTED_PIN_BINDING,
    PLANTED_PIN_CUTS,
    PLANTED_PIN_KEY,
    PLANTED_WAFER_KEY,
    PLANTED_WAFER_LIFTS,
    PLANTED_WAFER_ORDER,
    KeypadModel,
    PinTumblerModel,
    WaferModel,
    recover_keypad_code,
    recover_pin_tumbler_key,
    recover_wafer_key,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "lockpicks_certificate.json"
)
DOC_PATH = Path(__file__).resolve().parents[1] / "docs" / "lockpicks.md"

_SCOPE_SENTENCE = (
    "this opens only the simulated lock inside the test, not a real lock"
)
_SOURCE = "https://en.wikipedia.org/wiki/Lock_picking"


class _BoolOnly:
    """Expose named yes or no methods and nothing else."""

    def __init__(self, inner: object, names: tuple[str, ...]) -> None:
        self._inner = inner
        self._names = names

    def __getattr__(self, name: str):
        if name in self._names:
            return getattr(self._inner, name)
        raise AttributeError(name)


class LockpicksScopeTest(unittest.TestCase):
    def test_module_and_doc_limit_scope_to_the_simulated_lock(self) -> None:
        import engine.solvers.lockpicks as mod

        doc = mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn(_SCOPE_SENTENCE, lowered)
        self.assertIn("not a real lock", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("yes or no", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)
        note = DOC_PATH.read_text(encoding="utf-8")
        note_l = note.lower()
        self.assertIn(_SCOPE_SENTENCE, note_l)
        self.assertIn(_SOURCE, note)
        for name in (
            "half-diamond",
            "hook pick",
            "ball pick",
            "city rake",
            "snake",
            "bogota",
            "comb pick",
            "bump key",
            "tension wrench",
            "pick gun",
            "tubular lock pick",
        ):
            self.assertIn(name, note_l)
        self.assertIn("does not give steps for opening a real lock", note_l)
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


class LockpicksRecoveryTest(unittest.TestCase):
    def test_recovered_pin_wafer_and_keypad_secrets_match(self) -> None:
        pin = PinTumblerModel(PLANTED_PIN_CUTS, PLANTED_PIN_BINDING)
        pin_view = _BoolOnly(pin, ("pin_is_next", "depth_sets"))
        self.assertEqual(recover_pin_tumbler_key(pin_view), PLANTED_PIN_KEY)
        self.assertEqual(PLANTED_PIN_KEY, "3-1-5-0")

        wafer = WaferModel(PLANTED_WAFER_LIFTS, PLANTED_WAFER_ORDER)
        wafer_view = _BoolOnly(wafer, ("wafer_is_next", "lift_sets"))
        self.assertEqual(recover_wafer_key(wafer_view), PLANTED_WAFER_KEY)
        self.assertEqual(PLANTED_WAFER_KEY, "1-3-2")

        pad = KeypadModel(PLANTED_KEYPAD_DIGITS)
        pad_view = _BoolOnly(pad, ("code_matches",))
        self.assertEqual(recover_keypad_code(pad_view), PLANTED_KEYPAD_KEY)
        self.assertEqual(PLANTED_KEYPAD_KEY, "7395")

    def test_wrong_answers_stay_false_and_do_not_advance(self) -> None:
        pin = PinTumblerModel(PLANTED_PIN_CUTS, PLANTED_PIN_BINDING)
        first = PLANTED_PIN_BINDING[0]
        other = PLANTED_PIN_BINDING[1]
        self.assertIs(pin.pin_is_next(other), False)
        self.assertIs(pin.pin_is_next(first), True)
        wrong_depth = PLANTED_PIN_CUTS[first] + 1
        if wrong_depth > 5:
            wrong_depth = 0
        self.assertNotEqual(wrong_depth, PLANTED_PIN_CUTS[first])
        self.assertIs(pin.depth_sets(wrong_depth), False)
        self.assertIs(pin.pin_is_next(first), True)

        wafer = WaferModel(PLANTED_WAFER_LIFTS, PLANTED_WAFER_ORDER)
        wfirst = PLANTED_WAFER_ORDER[0]
        wother = PLANTED_WAFER_ORDER[1]
        self.assertIs(wafer.wafer_is_next(wother), False)
        self.assertIs(wafer.lift_sets(PLANTED_WAFER_LIFTS[wfirst] + 1), False)
        self.assertIs(wafer.wafer_is_next(wfirst), True)

        pad = KeypadModel(PLANTED_KEYPAD_DIGITS)
        self.assertIs(pad.code_matches((0, 0, 0, 0)), False)
        self.assertIs(pad.code_matches((7, 3, 9, 6)), False)
        self.assertIs(pad.code_matches(PLANTED_KEYPAD_DIGITS), True)


class LockpicksCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = CERT_PATH.read_text(encoding="utf-8")
        self.cert = json.loads(self.raw)

    def test_certificate_key_strings_and_sha256(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["pick_types_source"], _SOURCE)
        pairs = (
            ("pin_tumbler_key", "pin_tumbler_key_sha256", PLANTED_PIN_KEY),
            ("wafer_key", "wafer_key_sha256", PLANTED_WAFER_KEY),
            ("keypad_key", "keypad_key_sha256", PLANTED_KEYPAD_KEY),
        )
        for key_field, hash_field, expected in pairs:
            self.assertEqual(self.cert[key_field], expected)
            digest = hashlib.sha256(expected.encode("utf-8")).hexdigest()
            self.assertEqual(digest, self.cert[hash_field])
        note = self.cert["note"].lower()
        self.assertIn(_SCOPE_SENTENCE, note)
        self.assertIn("not a real lock", note)
        self.assertIn("nr. 86", note)
        self.assertNotIn("\u2014", self.raw)
        self.assertNotIn("\u2013", self.raw)

        pin = PinTumblerModel(
            tuple(self.cert["pin_cuts"]),
            tuple(self.cert["pin_binding_order"]),
        )
        self.assertEqual(
            recover_pin_tumbler_key(pin), self.cert["pin_tumbler_key"]
        )
        wafer = WaferModel(
            tuple(self.cert["wafer_lifts"]),
            tuple(self.cert["wafer_order"]),
        )
        self.assertEqual(recover_wafer_key(wafer), self.cert["wafer_key"])
        pad = KeypadModel(tuple(self.cert["keypad_digits"]))
        self.assertEqual(recover_keypad_code(pad), self.cert["keypad_key"])


if __name__ == "__main__":
    unittest.main()
