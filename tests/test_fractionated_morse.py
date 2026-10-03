"""Fractionated Morse known-key recovery against a published worked example.

Source (fetched 2026-10-02):
http://practicalcryptography.com/ciphers/fractionated-morse-cipher/

Practical Cryptography, Fractionated Morse cipher: key
ROUNDTABLECFGHIJKMPQSVWXYZ encrypts "defend the east" to
ESOAVVLJRSSTRX. The Morse line on that page is
-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-x
(the final x is padding). The first group "-.." is E and the next
group "x.x" is S. Decryption keeps the word spaces.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.fractionated_morse import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_KEY,
    PRACTICAL_CRYPTOGRAPHY_MORSE,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_URL,
    fractionated_morse_decrypt,
    fractionated_morse_encrypt,
    fractionated_morse_key,
    solve_fractionated_morse,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "fractionated_morse_certificate.json"
)


class FractionatedMorseScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.fractionated_morse as fractionated_morse_mod

        doc = (fractionated_morse_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn(
            "practicalcryptography.com/ciphers/fractionated-morse-cipher/",
            PRACTICAL_CRYPTOGRAPHY_URL,
        )


class FractionatedMorsePublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: defend the east -> ESOAVVLJRSSTRX."""

    def test_morse_line_matches_the_published_page(self) -> None:
        from engine.solvers.fractionated_morse import _encode_morse

        self.assertEqual(
            _encode_morse("defend the east"),
            PRACTICAL_CRYPTOGRAPHY_MORSE,
        )

    def test_first_groups_match_the_published_walkthrough(self) -> None:
        # Page: "-.." is the column E, and "x.x" is the column S.
        self.assertEqual(
            fractionated_morse_encrypt("D", PRACTICAL_CRYPTOGRAPHY_KEY)[:1],
            "E",
        )
        alphabet = fractionated_morse_key(PRACTICAL_CRYPTOGRAPHY_KEY)
        from engine.solvers.fractionated_morse import _TRIPLES

        self.assertEqual(alphabet[_TRIPLES.index("-..")], "E")
        self.assertEqual(alphabet[_TRIPLES.index("x.x")], "S")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = fractionated_morse_encrypt(
            "defend the east",
            PRACTICAL_CRYPTOGRAPHY_KEY,
        )
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_fractionated_morse(
            PRACTICAL_CRYPTOGRAPHY_CIPHER,
            key=PRACTICAL_CRYPTOGRAPHY_KEY,
        )
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "fractionated_morse")
        self.assertEqual(result.key, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_recovers_published_plaintext(self) -> None:
        # Keyword ROUNDTABLE expands to the same mixed alphabet the page prints.
        again = fractionated_morse_decrypt(
            fractionated_morse_encrypt(
                PRACTICAL_CRYPTOGRAPHY_PLAIN,
                "ROUNDTABLE",
            ),
            "ROUNDTABLE",
        )
        self.assertEqual(again, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(fractionated_morse_key("ROUNDTABLE"), PRACTICAL_CRYPTOGRAPHY_KEY)


class FractionatedMorseCertificateTest(unittest.TestCase):
    """Certificate checks the published example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "fractionated_morse")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(fractionated_morse_decrypt(ciphertext, key), plaintext)
        result = solve_fractionated_morse(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
