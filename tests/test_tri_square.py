"""Tri-square known-key recovery against the ACA sheet worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf

PDF SHA-256:
74b8200474df8a50e6782fcc33b4a34517f09d644b3954dc918c373f3f1b4151

Printed plaintext letters "t h r e e k e y s q u a r e s u s e d x".
Trigraphs RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ. Square 1 is
NOVELS down the columns. Square 2 is READING across the rows.
Square 3 is PASTIME in a clockwise spiral. The sheet prints the
squares, not those keyword names.

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
from engine.solvers.tri_square import (
    ACA_CIPHER,
    ACA_FIRST_ROWS,
    ACA_MESSAGE,
    ACA_PDF_SHA256,
    ACA_PLAIN,
    ACA_PRINTED_CIPHER,
    ACA_SQUARE1,
    ACA_SQUARE1_KEYWORD,
    ACA_SQUARE2,
    ACA_SQUARE2_KEYWORD,
    ACA_SQUARE3,
    ACA_SQUARE3_KEYWORD,
    ACA_THIRD_COLS,
    ACA_URL,
    square_clockwise_spiral,
    square_horizontal,
    square_vertical,
    tri_square_decrypt,
    tri_square_encrypt,
    tri_square_groups,
    tri_square_letters,
    solve_tri_square,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "tri_square_certificate.json"
)
DOC_PATH = Path(__file__).resolve().parents[1] / "docs" / "tri-square.md"


class TriSquareScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_an_unsolved_text(self) -> None:
        import engine.solvers.tri_square as tri_mod

        doc = (tri_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not an", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("voynich", doc)
        self.assertIn("linear a", doc)
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/TriSquare.pdf", ACA_URL)
        self.assertEqual(
            ACA_PDF_SHA256,
            "74b8200474df8a50e6782fcc33b4a34517f09d644b3954dc918c373f3f1b4151",
        )
        self.assertNotIn("tri_square", SOLVERS)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class TriSquareSquaresTest(unittest.TestCase):
    def test_keywords_rebuild_the_printed_squares(self) -> None:
        self.assertEqual(square_vertical(ACA_SQUARE1_KEYWORD), ACA_SQUARE1)
        self.assertEqual(square_vertical("novels"), "NSFMUOAGPWVBHQXECIRYLDKTZ")
        self.assertEqual(square_horizontal(ACA_SQUARE2_KEYWORD), ACA_SQUARE2)
        self.assertEqual(square_horizontal("reading"), "READINGBCFHKLMOPQSTUVWXYZ")
        self.assertEqual(square_clockwise_spiral(ACA_SQUARE3_KEYWORD), ACA_SQUARE3)
        self.assertEqual(
            square_clockwise_spiral("pastime"),
            "PASTINOQRMLYZUEKXWVBHGFDC",
        )
        for square in (ACA_SQUARE1, ACA_SQUARE2, ACA_SQUARE3):
            self.assertEqual(len(square), 25)
            self.assertEqual(len(set(square)), 25)
            self.assertNotIn("J", square)


class TriSquarePublishedExampleTest(unittest.TestCase):
    """ACA sheet: three key squares used x -> RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = tri_square_encrypt(
            ACA_MESSAGE,
            ACA_SQUARE1,
            ACA_SQUARE2,
            ACA_SQUARE3,
            ACA_FIRST_ROWS,
            ACA_THIRD_COLS,
        )
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cipher, "RHLQXRLXOEVZBATXSERXDDIUAAABFZ")
        self.assertEqual(tri_square_groups(cipher) + ".", ACA_PRINTED_CIPHER)
        self.assertEqual(
            tri_square_groups(cipher) + ".",
            "RHL QXR LXO EVZ BAT XSE RXD DIU AAA BFZ.",
        )

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = tri_square_decrypt(
            ACA_PRINTED_CIPHER,
            ACA_SQUARE1,
            ACA_SQUARE2,
            ACA_SQUARE3,
        )
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(plain, "THREEKEYSQUARESUSEDX")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_tri_square(
            ACA_PRINTED_CIPHER,
            square1=ACA_SQUARE1,
            square2=ACA_SQUARE2,
            square3=ACA_SQUARE3,
        )
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "tri_square")
        self.assertEqual(
            result.key,
            ACA_SQUARE1 + "/" + ACA_SQUARE2 + "/" + ACA_SQUARE3,
        )
        self.assertEqual(result.details["square1"], ACA_SQUARE1)
        self.assertEqual(result.details["square2"], ACA_SQUARE2)
        self.assertEqual(result.details["square3"], ACA_SQUARE3)
        self.assertEqual(result.details["source_example"], ACA_URL)
        self.assertEqual(result.details["spaces"], "not_enciphered")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("voynich", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])

    def test_other_column_and_row_choices_still_decrypt(self) -> None:
        other = tri_square_encrypt(
            ACA_PLAIN,
            ACA_SQUARE1,
            ACA_SQUARE2,
            ACA_SQUARE3,
        )
        self.assertNotEqual(other, ACA_CIPHER)
        self.assertEqual(
            tri_square_decrypt(other, ACA_SQUARE1, ACA_SQUARE2, ACA_SQUARE3),
            ACA_PLAIN,
        )

    def test_spaces_are_not_enciphered_and_j_folds_to_i(self) -> None:
        self.assertEqual(tri_square_letters(ACA_MESSAGE), ACA_PLAIN)
        self.assertNotIn(" ", ACA_PLAIN)
        self.assertEqual(tri_square_letters("Jazz"), "IAZZ")
        self.assertEqual(
            tri_square_encrypt(
                ACA_MESSAGE,
                ACA_SQUARE1,
                ACA_SQUARE2,
                ACA_SQUARE3,
                ACA_FIRST_ROWS,
                ACA_THIRD_COLS,
            ),
            tri_square_encrypt(
                ACA_PLAIN,
                ACA_SQUARE1,
                ACA_SQUARE2,
                ACA_SQUARE3,
                ACA_FIRST_ROWS,
                ACA_THIRD_COLS,
            ),
        )


class TriSquareRoundtripTest(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip_pads_an_odd_length(self) -> None:
        left = square_vertical("LEFT")
        top = square_horizontal("TOP")
        middle = square_clockwise_spiral("MIDDLE")
        text = "Three squares pad"
        letters = tri_square_letters(text)
        self.assertEqual(len(letters) % 2, 1)
        cipher = tri_square_encrypt(text, left, top, middle)
        self.assertEqual(len(cipher), (len(letters) + 1) // 2 * 3)
        self.assertEqual(
            tri_square_decrypt(cipher, left, top, middle),
            letters + "X",
        )

    def test_bad_length_and_bad_square_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            tri_square_decrypt("ABCD", ACA_SQUARE1, ACA_SQUARE2, ACA_SQUARE3)
        with self.assertRaises(ValueError):
            tri_square_encrypt("", ACA_SQUARE1, ACA_SQUARE2, ACA_SQUARE3)
        with self.assertRaises(ValueError):
            tri_square_decrypt("ABC", "ABCDEFGHIKLMNOPQRSTUVWXY", ACA_SQUARE2, ACA_SQUARE3)
        with self.assertRaises(ValueError):
            square_horizontal("!!!")
        with self.assertRaises(ValueError):
            tri_square_encrypt(
                ACA_PLAIN,
                ACA_SQUARE1,
                ACA_SQUARE2,
                ACA_SQUARE3,
                first_rows=(0,),
            )


class TriSquareCertificateTest(unittest.TestCase):
    """Certificate checks the ACA sheet example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "tri_square")
        self.assertEqual(self.cert["name"], "tri_square")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        keys = self.cert["keys"]
        self.assertEqual(keys["square1_keyword"], ACA_SQUARE1_KEYWORD)
        self.assertEqual(keys["square1_route"], "vertical")
        self.assertEqual(keys["square1"], ACA_SQUARE1)
        self.assertEqual(keys["square2_keyword"], ACA_SQUARE2_KEYWORD)
        self.assertEqual(keys["square2_route"], "horizontal")
        self.assertEqual(keys["square2"], ACA_SQUARE2)
        self.assertEqual(keys["square3_keyword"], ACA_SQUARE3_KEYWORD)
        self.assertEqual(keys["square3_route"], "clockwise_spiral")
        self.assertEqual(keys["square3"], ACA_SQUARE3)
        self.assertEqual(tuple(keys["first_rows"]), ACA_FIRST_ROWS)
        self.assertEqual(tuple(keys["third_cols"]), ACA_THIRD_COLS)
        self.assertEqual(
            self.cert["key"],
            "NOVELS:vertical/READING:horizontal/PASTIME:clockwise_spiral",
        )
        self.assertNotIn(" ", plaintext)
        self.assertEqual(plaintext, "THREEKEYSQUARESUSEDX")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            tri_square_decrypt(
                ciphertext,
                keys["square1"],
                keys["square2"],
                keys["square3"],
            ),
            plaintext,
        )
        self.assertEqual(
            tri_square_encrypt(
                plaintext,
                keys["square1"],
                keys["square2"],
                keys["square3"],
                keys["first_rows"],
                keys["third_cols"],
            ),
            ciphertext,
        )
        result = solve_tri_square(
            ciphertext,
            square1=keys["square1"],
            square2=keys["square2"],
            square3=keys["square3"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        self.assertEqual(self.cert["source_sha256"], ACA_PDF_SHA256)
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
        doc = DOC_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)
        self.assertIn(ACA_PDF_SHA256, doc)


if __name__ == "__main__":
    unittest.main()
