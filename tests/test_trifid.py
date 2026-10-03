"""Trifid known-key recovery against a published worked example.

Source (fetched 2026-10-03):
http://practicalcryptography.com/ciphers/trifid-cipher/

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.trifid import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS,
    PRACTICAL_CRYPTOGRAPHY_KEY,
    PRACTICAL_CRYPTOGRAPHY_PERIOD,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_URL,
    trifid_decrypt,
    trifid_encrypt,
    trifid_symbols,
    solve_trifid,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "trifid_certificate.json"
)


class TrifidScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.trifid as trifid_mod

        doc = (trifid_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("practicalcryptography.com/ciphers/trifid-cipher", PRACTICAL_CRYPTOGRAPHY_URL)
        self.assertNotIn("trifid", SOLVERS)


class TrifidPublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: defend the east wall, period 5."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = trifid_encrypt(
            "DEFEND THE EAST WALL OF THE CASTLE.",
            PRACTICAL_CRYPTOGRAPHY_KEY,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)
        self.assertEqual(cipher, "SUEFECPHSEGYYJIXIMFOFOCEJLBSP")
        grouped = " ".join(cipher[i : i + 5] for i in range(0, len(cipher), 5))
        self.assertEqual(grouped, PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS)
        self.assertEqual(grouped, "SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP")

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = trifid_decrypt(
            PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS,
            PRACTICAL_CRYPTOGRAPHY_KEY,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(plain, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(plain, "DEFENDTHEEASTWALLOFTHECASTLE.")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_trifid(
            PRACTICAL_CRYPTOGRAPHY_CIPHER_GROUPS,
            key=PRACTICAL_CRYPTOGRAPHY_KEY,
            period=PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "trifid")
        self.assertEqual(result.key, PRACTICAL_CRYPTOGRAPHY_KEY + "/5")
        self.assertEqual(result.details["period"], 5)
        self.assertEqual(result.details["alphabet"], PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        self.assertEqual(result.details["spaces"], "not_enciphered")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_spaces_are_not_enciphered(self) -> None:
        spaced = "DEFEND THE EAST WALL OF THE CASTLE."
        self.assertNotEqual(trifid_symbols(spaced), spaced)
        self.assertEqual(trifid_symbols(spaced), PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertNotIn(" ", trifid_encrypt(spaced, PRACTICAL_CRYPTOGRAPHY_KEY, 5))
        self.assertEqual(
            trifid_encrypt(spaced, PRACTICAL_CRYPTOGRAPHY_KEY, 5),
            trifid_encrypt(PRACTICAL_CRYPTOGRAPHY_PLAIN, PRACTICAL_CRYPTOGRAPHY_KEY, 5),
        )


class TrifidCertificateTest(unittest.TestCase):
    """Certificate checks the published example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "trifid")
        self.assertEqual(self.cert["name"], "trifid")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        alphabet, period_text = key.split("/")
        period = int(period_text)
        self.assertEqual(self.cert["keys"]["alphabet"], alphabet)
        self.assertEqual(self.cert["keys"]["period"], period)
        self.assertEqual(alphabet, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(period, 5)
        # Spaces are not included in the stored plaintext.
        self.assertNotIn(" ", plaintext)
        self.assertTrue(plaintext.endswith("."))
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(trifid_decrypt(ciphertext, alphabet, period), plaintext)
        result = solve_trifid(ciphertext, key=alphabet, period=period)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(
            trifid_encrypt(plaintext, alphabet, period),
            ciphertext,
        )
        self.assertEqual(self.cert["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        note = self.cert["note"].lower()
        self.assertIn("spaces are not enciphered", note)
        self.assertIn("not included", note)
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)


if __name__ == "__main__":
    unittest.main()
