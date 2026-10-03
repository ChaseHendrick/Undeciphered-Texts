"""Porta known-key recovery against a published worked example.

Source (fetched 2026-10-02): https://www.boxentriq.com/ciphers/porta-cipher

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.porta import (
    BOXENTRIQ_CIPHER,
    BOXENTRIQ_KEY,
    BOXENTRIQ_PLAIN,
    BOXENTRIQ_URL,
    porta_decrypt,
    porta_encrypt,
    porta_substitute,
    solve_porta,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "porta_certificate.json"


class PortaScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.porta as porta_mod

        doc = (porta_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("boxentriq.com/ciphers/porta-cipher", BOXENTRIQ_URL)


class PortaPublishedExampleTest(unittest.TestCase):
    """Boxentriq: DEFENDTHEEASTWALLOFTHECASTLE + FORTIFICATION → SYNNJS…"""

    def test_first_lookups_match_the_published_walkthrough(self) -> None:
        # Page section "Look up the first letters": D+F=S, E+O=Y, F+R=N.
        self.assertEqual(porta_substitute("D", "F"), "S")
        self.assertEqual(porta_substitute("E", "O"), "Y")
        self.assertEqual(porta_substitute("F", "R"), "N")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = porta_encrypt(BOXENTRIQ_PLAIN, BOXENTRIQ_KEY)
        self.assertEqual(cipher, BOXENTRIQ_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_porta(BOXENTRIQ_CIPHER, key=BOXENTRIQ_KEY)
        self.assertEqual(result.plaintext, BOXENTRIQ_PLAIN)
        self.assertEqual(result.method, "porta")
        self.assertEqual(result.key, BOXENTRIQ_KEY)
        self.assertEqual(result.details["source_url"], BOXENTRIQ_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_reciprocal_map_roundtrips(self) -> None:
        again = porta_decrypt(porta_encrypt(BOXENTRIQ_PLAIN, BOXENTRIQ_KEY), "fortification")
        self.assertEqual(again, BOXENTRIQ_PLAIN)


class PortaCertificateTest(unittest.TestCase):
    """Certificate checks the published Boxentriq example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "porta")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(porta_decrypt(ciphertext, key), plaintext)
        result = solve_porta(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], BOXENTRIQ_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
