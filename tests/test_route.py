"""Route cipher known-key recovery against a published worked example.

Source (fetched 2026-10-02):
http://www.crypto-it.net/eng/simple/route-cipher.html

Crypto-IT, "Route Cipher" (page dated 2020-03-09): width 3, letters written
row by row, clockwise inward spiral from the top right. "Brighton and Hove"
becomes BRIGHTONANDHOVE and encrypts to ITAHEVONOGBRHND.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.route import (
    CRYPTO_IT_CIPHER,
    CRYPTO_IT_KEY,
    CRYPTO_IT_PLAIN,
    CRYPTO_IT_URL,
    WIKIPEDIA_CIPHER,
    WIKIPEDIA_KEY,
    WIKIPEDIA_PLAIN,
    WIKIPEDIA_URL,
    route_decrypt,
    route_encrypt,
    solve_route,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "route_certificate.json"


class RouteScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.route as route_mod

        doc = (route_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("crypto-it.net/eng/simple/route-cipher", CRYPTO_IT_URL)


class RoutePublishedExampleTest(unittest.TestCase):
    """Crypto-IT: BRIGHTONANDHOVE, width 3, spiral clockwise from the top right."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = route_encrypt(CRYPTO_IT_PLAIN, CRYPTO_IT_KEY)
        self.assertEqual(cipher, CRYPTO_IT_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_route(CRYPTO_IT_CIPHER, key=CRYPTO_IT_KEY)
        self.assertEqual(result.plaintext, CRYPTO_IT_PLAIN)
        self.assertEqual(result.method, "route")
        self.assertEqual(result.key, CRYPTO_IT_KEY)
        self.assertEqual(result.details["source_url"], CRYPTO_IT_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_uses_the_published_key(self) -> None:
        again = route_decrypt(route_encrypt(CRYPTO_IT_PLAIN, CRYPTO_IT_KEY), CRYPTO_IT_KEY)
        self.assertEqual(again, CRYPTO_IT_PLAIN)

    def test_spaced_plaintext_encrypts_to_the_published_ciphertext(self) -> None:
        cipher = route_encrypt("Brighton and Hove", CRYPTO_IT_KEY)
        self.assertEqual(cipher, CRYPTO_IT_CIPHER)
        self.assertEqual(route_decrypt(cipher, CRYPTO_IT_KEY), CRYPTO_IT_PLAIN)

    def test_wikipedia_grid_including_the_shown_nulls(self) -> None:
        # Wikipedia Transposition cipher, "Route cipher": same spiral, columns.
        # The page draws J and X in the grid after the sentence. Recovering
        # the grid letters is not a reading of an unknown script.
        self.assertIn("wikipedia.org/wiki/Transposition_cipher", WIKIPEDIA_URL)
        cipher = route_encrypt(WIKIPEDIA_PLAIN, WIKIPEDIA_KEY)
        self.assertEqual(cipher, WIKIPEDIA_CIPHER)
        result = solve_route(WIKIPEDIA_CIPHER, key=WIKIPEDIA_KEY)
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAIN)


class RouteCertificateTest(unittest.TestCase):
    """Certificate checks the published Crypto-IT example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "route")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(route_decrypt(ciphertext, key), plaintext)
        result = solve_route(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], CRYPTO_IT_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
