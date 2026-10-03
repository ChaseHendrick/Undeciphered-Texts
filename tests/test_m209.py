"""M-209 known-key recovery against a published worked example.

Source (fetched 2026-10-02): http://www.jfbouch.fr/crypto/m209/WORK/index.html

The internal key is the TM 11-380 (1944) indicator LP list printed there.
External key PEOPLE. "Attack at dawn" is enciphered as ATTACKZATZDAWN
because the machine replaces a space with Z. Ciphertext WUHDUAJRJQTLRG.

This is a known-key historical machine test. It does not claim a break of
an unsolved intercept, an unknown-script reading, or a reading of army
message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.m209 import (
    BOUCHAUDY_CIPHERTEXT,
    BOUCHAUDY_CIPHERTEXT_GROUPS,
    BOUCHAUDY_EXTERNAL_KEY,
    BOUCHAUDY_LUGS,
    BOUCHAUDY_MATH_URL,
    BOUCHAUDY_PINS,
    BOUCHAUDY_PLAINTEXT,
    BOUCHAUDY_PLAINTEXT_GROUPS,
    BOUCHAUDY_URL,
    m209_decrypt,
    m209_encrypt,
    m209_keystream,
    solve_m209,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "m209_certificate.json"


class M209ScopeTest(unittest.TestCase):
    def test_module_documents_known_key_machine_not_an_unsolved_break(self) -> None:
        import engine.solvers.m209 as m209_mod

        doc = (m209_mod.__doc__ or "").lower()
        self.assertIn("known-key historical machine", doc)
        self.assertIn("not", doc)
        self.assertIn("unsolved intercept", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("jfbouch.fr/crypto/m209/work/index.html", BOUCHAUDY_URL.lower())
        self.assertIn("mathematical.html", BOUCHAUDY_MATH_URL)


class M209PublishedExampleTest(unittest.TestCase):
    """Bouchaudy / TM 11-380 LP: ATTACKZATZDAWN + PEOPLE -> WUHDUAJRJQTLRG."""

    def test_first_keystream_value_matches_the_mathematical_page(self) -> None:
        # Page: K[0] = 23, and (25 + 23) - A = 22 = W.
        stream = m209_keystream(6, BOUCHAUDY_EXTERNAL_KEY, BOUCHAUDY_PINS, BOUCHAUDY_LUGS)
        self.assertEqual(stream[:6], [23, 14, 27, 4, 23, 11])

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = m209_encrypt(
            BOUCHAUDY_PLAINTEXT,
            BOUCHAUDY_EXTERNAL_KEY,
            BOUCHAUDY_PINS,
            BOUCHAUDY_LUGS,
        )
        self.assertEqual(cipher, BOUCHAUDY_CIPHERTEXT)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_m209(
            BOUCHAUDY_CIPHERTEXT,
            external_key=BOUCHAUDY_EXTERNAL_KEY,
            pins=BOUCHAUDY_PINS,
            lugs=BOUCHAUDY_LUGS,
        )
        self.assertEqual(result.plaintext, BOUCHAUDY_PLAINTEXT)
        self.assertEqual(result.plaintext, "ATTACKZATZDAWN")
        self.assertEqual(result.method, "m209")
        self.assertEqual(result.key, BOUCHAUDY_EXTERNAL_KEY)
        self.assertEqual(result.details["source_url"], BOUCHAUDY_URL)
        self.assertEqual(result.details["machine"], "M-209 (Hagelin C-38)")
        scope = result.details["scope"].lower()
        self.assertIn("known-key historical", scope)
        self.assertIn("not a break of an unsolved intercept", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_grouped_ciphertext_keeps_the_published_groups(self) -> None:
        result = solve_m209(
            BOUCHAUDY_CIPHERTEXT_GROUPS,
            external_key=BOUCHAUDY_EXTERNAL_KEY,
            pins=BOUCHAUDY_PINS,
            lugs=BOUCHAUDY_LUGS,
        )
        self.assertEqual(result.plaintext, BOUCHAUDY_PLAINTEXT_GROUPS)

    def test_reciprocal_map_roundtrips(self) -> None:
        again = m209_decrypt(
            m209_encrypt(
                BOUCHAUDY_PLAINTEXT,
                "people",
                BOUCHAUDY_PINS,
                BOUCHAUDY_LUGS,
            ),
            BOUCHAUDY_EXTERNAL_KEY,
            BOUCHAUDY_PINS,
            BOUCHAUDY_LUGS,
        )
        self.assertEqual(again, BOUCHAUDY_PLAINTEXT)

    def test_padded_group_on_the_mathematical_page(self) -> None:
        # That page completes the last group with Z: DAWNZ -> TLRGI.
        cipher = m209_encrypt(
            "ATTACKZATZDAWNZ",
            BOUCHAUDY_EXTERNAL_KEY,
            BOUCHAUDY_PINS,
            BOUCHAUDY_LUGS,
        )
        self.assertEqual(cipher, "WUHDUAJRJQTLRGI")


class M209CertificateTest(unittest.TestCase):
    """Certificate checks the published known-key example, not an unsolved intercept."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "M-209 (Hagelin C-38)")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        settings = self.cert["key_settings"]
        external_key = settings["external_key"]
        pins = settings["pins"]
        lugs = settings["lugs"]
        self.assertEqual(external_key, BOUCHAUDY_EXTERNAL_KEY)
        self.assertEqual(pins, list(BOUCHAUDY_PINS))
        self.assertEqual(lugs, list(BOUCHAUDY_LUGS))
        self.assertEqual(settings["indicator"], "LP")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            m209_decrypt(ciphertext, external_key, pins, lugs),
            plaintext,
        )
        result = solve_m209(ciphertext, external_key=external_key, pins=pins, lugs=lugs)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(result.plaintext, "ATTACKZATZDAWN")
        self.assertEqual(self.cert["source_url"], BOUCHAUDY_URL)
        note = self.cert["note"].lower()
        self.assertIn("known-key", note)
        self.assertIn("not a break of an unsolved intercept", note)
        self.assertIn("not an unknown-script reading", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
