"""CM Bifid known-key recovery against the ACA sheet worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf

PDF SHA-256:
90d3e1133e00d1100fbee3e3b188cdb621cf4282b415a38cab3b4acf5b2dfd89

Printed plaintext "Odd periods are popular." Period groups
FANXZEX FENUKKR BYNKAK. Ciphertext square keyword NOVELTY,
alternating verticals. The plaintext square is the one printed on
the sheet. The Bifid sheet it cites names EXTRAORDINARY in a
clockwise spiral and period 7.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac,
Beale, McCormick, Voynich, Linear A, the Indus script, rongorongo,
or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.bifid import bifid_encrypt
from engine.solvers.cm_bifid import (
    ACA_BIFID_CIPHER,
    ACA_BIFID_URL,
    ACA_CIPHER,
    ACA_CIPHER_KEYWORD,
    ACA_CIPHER_SQUARE,
    ACA_MESSAGE,
    ACA_PDF_SHA256,
    ACA_PERIOD,
    ACA_PLAIN,
    ACA_PLAIN_KEYWORD,
    ACA_PLAIN_SQUARE,
    ACA_PRINTED_CIPHER,
    ACA_URL,
    cm_bifid_decrypt,
    cm_bifid_encrypt,
    cm_bifid_letters,
    solve_cm_bifid,
    square_alternating_verticals,
    square_clockwise_spiral,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "cm_bifid_certificate.json"
)


class CmBifidScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_an_unsolved_text(self) -> None:
        import engine.solvers.cm_bifid as cm_mod

        doc = (cm_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not an", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("voynich", doc)
        self.assertIn("linear a", doc)
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/CMBifid.pdf", ACA_URL)
        self.assertEqual(
            ACA_PDF_SHA256,
            "90d3e1133e00d1100fbee3e3b188cdb621cf4282b415a38cab3b4acf5b2dfd89",
        )
        self.assertNotIn("cm_bifid", SOLVERS)


class CmBifidSquaresTest(unittest.TestCase):
    def test_keywords_rebuild_the_printed_squares(self) -> None:
        self.assertEqual(square_clockwise_spiral(ACA_PLAIN_KEYWORD), ACA_PLAIN_SQUARE)
        self.assertEqual(
            square_clockwise_spiral("extraordinary"),
            "EXTRAKLMPOHWZQDGVUSIFCBYN",
        )
        self.assertEqual(
            square_alternating_verticals(ACA_CIPHER_KEYWORD),
            ACA_CIPHER_SQUARE,
        )
        self.assertEqual(
            square_alternating_verticals("novelty"),
            "NCDRSOBFQUVAGPWEYHMXLTIKZ",
        )
        self.assertEqual(len(ACA_PLAIN_SQUARE), 25)
        self.assertEqual(len(set(ACA_PLAIN_SQUARE)), 25)
        self.assertNotIn("J", ACA_PLAIN_SQUARE)
        self.assertNotIn("J", ACA_CIPHER_SQUARE)


class CmBifidPublishedExampleTest(unittest.TestCase):
    """ACA sheet: Odd periods are popular. -> FANXZEX FENUKKR BYNKAK."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = cm_bifid_encrypt(
            ACA_MESSAGE,
            ACA_PLAIN_SQUARE,
            ACA_CIPHER_SQUARE,
            ACA_PERIOD,
        )
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cipher, "FANXZEXFENUKKRBYNKAK")
        groups = []
        for start in range(0, len(cipher), ACA_PERIOD):
            groups.append(cipher[start : start + ACA_PERIOD])
        self.assertEqual(" ".join(groups), ACA_PRINTED_CIPHER)
        self.assertEqual(" ".join(groups), "FANXZEX FENUKKR BYNKAK")

    def test_same_plaintext_square_matches_the_bifid_sheet(self) -> None:
        # The companion Bifid sheet uses this plaintext square alone.
        ordinary = bifid_encrypt(ACA_MESSAGE, ACA_PLAIN_SQUARE, ACA_PERIOD)
        self.assertEqual(ordinary, ACA_BIFID_CIPHER)
        self.assertEqual(ordinary, "MWEINGIMGEOYYRLVEYWY")
        self.assertIn("Bifid.pdf", ACA_BIFID_URL)
        # Same coordinates, second square: not the ordinary Bifid ciphertext.
        conjugated = cm_bifid_encrypt(
            ACA_PLAIN, ACA_PLAIN_SQUARE, ACA_CIPHER_SQUARE, ACA_PERIOD
        )
        self.assertNotEqual(conjugated, ordinary)

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = cm_bifid_decrypt(
            ACA_PRINTED_CIPHER,
            ACA_PLAIN_SQUARE,
            ACA_CIPHER_SQUARE,
            ACA_PERIOD,
        )
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(plain, "ODDPERIODSAREPOPULAR")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_cm_bifid(
            ACA_PRINTED_CIPHER,
            plain_square=ACA_PLAIN_SQUARE,
            cipher_square=ACA_CIPHER_SQUARE,
            period=ACA_PERIOD,
        )
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "cm_bifid")
        self.assertEqual(
            result.key,
            ACA_PLAIN_SQUARE + "/" + ACA_CIPHER_SQUARE + "/7",
        )
        self.assertEqual(result.details["period"], 7)
        self.assertEqual(result.details["plain_square"], ACA_PLAIN_SQUARE)
        self.assertEqual(result.details["cipher_square"], ACA_CIPHER_SQUARE)
        self.assertEqual(result.details["source_url"], ACA_URL)
        self.assertEqual(result.details["spaces"], "not_enciphered")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("voynich", scope)

    def test_spaces_are_not_enciphered_and_j_folds_to_i(self) -> None:
        self.assertEqual(cm_bifid_letters(ACA_MESSAGE), ACA_PLAIN)
        self.assertNotIn(" ", ACA_PLAIN)
        self.assertEqual(cm_bifid_letters("Jazz"), "IAZZ")
        self.assertEqual(
            cm_bifid_encrypt(ACA_MESSAGE, ACA_PLAIN_SQUARE, ACA_CIPHER_SQUARE, 7),
            cm_bifid_encrypt(ACA_PLAIN, ACA_PLAIN_SQUARE, ACA_CIPHER_SQUARE, 7),
        )


class CmBifidRoundtripTest(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip_with_a_short_last_block(self) -> None:
        plain_square = square_clockwise_spiral("SPIRAL")
        cipher_square = square_alternating_verticals("COLUMNS")
        text = "Conjugated matrix bifid keeps a short final group."
        letters = cm_bifid_letters(text)
        self.assertNotEqual(len(letters) % 5, 0)
        cipher = cm_bifid_encrypt(text, plain_square, cipher_square, 5)
        self.assertEqual(
            cm_bifid_decrypt(cipher, plain_square, cipher_square, 5),
            letters,
        )
        # Identical squares are ordinary Bifid.
        self.assertEqual(
            cm_bifid_encrypt(letters, plain_square, plain_square, 5),
            bifid_encrypt(letters, plain_square, 5),
        )

    def test_bad_period_and_bad_square_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cm_bifid_encrypt(ACA_PLAIN, ACA_PLAIN_SQUARE, ACA_CIPHER_SQUARE, 0)
        with self.assertRaises(ValueError):
            cm_bifid_decrypt("ABC", "ABCDEFGHIKLMNOPQRSTUVWXY", ACA_CIPHER_SQUARE, 3)
        with self.assertRaises(ValueError):
            square_clockwise_spiral("!!!")


class CmBifidCertificateTest(unittest.TestCase):
    """Certificate checks the ACA sheet example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "cm_bifid")
        self.assertEqual(self.cert["name"], "cm_bifid")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        keys = self.cert["keys"]
        self.assertEqual(keys["plain_keyword"], ACA_PLAIN_KEYWORD)
        self.assertEqual(keys["plain_route"], "clockwise_spiral")
        self.assertEqual(keys["plain_square"], ACA_PLAIN_SQUARE)
        self.assertEqual(keys["cipher_keyword"], ACA_CIPHER_KEYWORD)
        self.assertEqual(keys["cipher_route"], "alternating_verticals")
        self.assertEqual(keys["cipher_square"], ACA_CIPHER_SQUARE)
        self.assertEqual(keys["period"], 7)
        self.assertEqual(
            self.cert["key"],
            "EXTRAORDINARY:clockwise_spiral/NOVELTY:alternating_verticals/7",
        )
        self.assertNotIn(" ", plaintext)
        self.assertEqual(plaintext, "ODDPERIODSAREPOPULAR")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            cm_bifid_decrypt(
                ciphertext,
                keys["plain_square"],
                keys["cipher_square"],
                keys["period"],
            ),
            plaintext,
        )
        self.assertEqual(
            cm_bifid_encrypt(
                plaintext,
                keys["plain_square"],
                keys["cipher_square"],
                keys["period"],
            ),
            ciphertext,
        )
        result = solve_cm_bifid(
            ciphertext,
            plain_square=keys["plain_square"],
            cipher_square=keys["cipher_square"],
            period=keys["period"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        self.assertEqual(self.cert["source_sha256"], ACA_PDF_SHA256)
        self.assertEqual(self.cert["plain_square_source_url"], ACA_BIFID_URL)
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
        self.assertNotIn("\u2014", self.cert["note"])
        self.assertNotIn("\u2013", self.cert["note"])


if __name__ == "__main__":
    unittest.main()
