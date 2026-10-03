"""Exhaustive search over the Caesar and rail-fence certificates.

The solvers are not given the key. They must recover the plaintext and
key already stored in each solver certificate.

Caesar keyspace: 26 shifts. Rail fence keyspace: rails 2 through 6 (5 keys).
This is exhaustive search of a tiny space, not an unsolved-text break.
Enigma, the M-209, army message Nr. 86, and Kryptos K4 are not searched.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.solvers.tiny_exhaustive import (
    CAESAR_KEYSPACE_SIZE,
    RAIL_FENCE_KEYSPACE_SIZE,
    RAIL_FENCE_MAX_RAILS,
    RAIL_FENCE_MIN_RAILS,
    brute_caesar,
    brute_rail_fence,
)


ROOT = Path(__file__).resolve().parents[1]
CAESAR_CERT = ROOT / "engine" / "data" / "caesar_certificate.json"
RAIL_CERT = ROOT / "engine" / "data" / "rail_fence_certificate.json"
SOLVER_PATH = ROOT / "engine" / "solvers" / "tiny_exhaustive.py"


class TinyExhaustiveScopeTest(unittest.TestCase):
    def test_module_documents_tiny_exhaustive_search(self) -> None:
        import engine.solvers.tiny_exhaustive as mod

        doc = mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("26", doc)
        self.assertIn("exhaustive search of a tiny space", lowered)
        self.assertIn("not an unsolved-text break", lowered)
        self.assertIn("enigma", lowered)
        self.assertIn("m-209", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("kryptos k4", lowered)
        self.assertEqual(CAESAR_KEYSPACE_SIZE, 26)
        self.assertEqual(RAIL_FENCE_MIN_RAILS, 2)
        self.assertEqual(RAIL_FENCE_MAX_RAILS, 6)
        self.assertEqual(RAIL_FENCE_KEYSPACE_SIZE, 5)
        source = SOLVER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", source)
        self.assertNotIn("\u2013", source)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)

    def test_search_does_not_target_excluded_ciphers(self) -> None:
        import engine.solvers.tiny_exhaustive as mod

        names = set(dir(mod))
        for banned in ("enigma", "m209", "k4", "nr86"):
            self.assertNotIn(banned, names)


class CaesarExhaustiveCertificateTest(unittest.TestCase):
    def test_recovers_certificate_plaintext_and_key_without_the_shift(self) -> None:
        cert = json.loads(CAESAR_CERT.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "caesar")
        result = brute_caesar(cert["ciphertext"])
        self.assertEqual(result.plaintext, cert["plaintext"])
        self.assertEqual(result.key, str(cert["keys"]["shift"]))
        self.assertEqual(result.details["shift"], cert["keys"]["shift"])
        self.assertEqual(result.details["keyspace_size"], 26)
        self.assertEqual(result.details["trials"], 26)
        self.assertEqual(result.details["search"], "exhaustive")
        scope = result.details["scope"].lower()
        self.assertIn("exhaustive search of a tiny", scope)
        self.assertIn("not an unsolved-text break", scope)
        self.assertIn("enigma", scope)
        self.assertIn("m-209", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("k4", scope)


class RailFenceExhaustiveCertificateTest(unittest.TestCase):
    def test_recovers_certificate_plaintext_and_key_without_the_rails(self) -> None:
        cert = json.loads(RAIL_CERT.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "rail_fence")
        result = brute_rail_fence(cert["ciphertext"])
        self.assertEqual(result.plaintext, cert["plaintext"])
        self.assertEqual(result.key, cert["key"])
        self.assertEqual(result.key, str(cert["keys"]["rails"]))
        self.assertEqual(result.details["rails"], cert["keys"]["rails"])
        self.assertEqual(result.details["keyspace_size"], 5)
        self.assertEqual(result.details["trials"], 5)
        self.assertEqual(result.details["search"], "exhaustive")
        scope = result.details["scope"].lower()
        self.assertIn("not an unsolved-text break", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("k4", scope)


if __name__ == "__main__":
    unittest.main()
