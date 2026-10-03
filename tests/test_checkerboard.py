"""Literal ACA coordinate examples and strict supplied-square controls."""
import hashlib
import json
from pathlib import Path
import unittest

from engine.solvers.checkerboard import checkerboard_encrypt, checkerboard_decrypt, solve_checkerboard

SQUARE = "KNIGHPQRSTOYZUAMXWVBLFEDC"
PLAIN = "NUMBERSCANALSOBEUSEDASCOORDINATES"
SIMPLE = "BH AT CW CE KI LI LT KE AE BH AE KW LT AW CE KI AT LT KI KT AE LT KE AW AW LI KT BI BH AE LE KI LT."
COMPLEX = "HR RY CG SS EA LA OT KS RS BR AS EG LY AG CS EI AT LT KA ET RE OY EE RG AG LA KY HI HH RS OS EI LY."


class CheckerboardTest(unittest.TestCase):
    def test_simple_printed_coordinate_vector(self):
        options = {"square": SQUARE, "row_labels": ("BLACK",), "column_labels": ("WHITE",)}
        self.assertEqual(checkerboard_encrypt(PLAIN, **options), SIMPLE[:-1].replace(" ", ""))
        self.assertEqual(checkerboard_decrypt(SIMPLE, terminal_period=True, **options), PLAIN)

    def test_complex_printed_homophones_and_supplied_choices(self):
        rows, columns = ("HORSE", "BLACK"), ("GRAYS", "WHITE")
        options = {"square": SQUARE, "row_labels": rows, "column_labels": columns}
        pairs = COMPLEX[:-1].split()
        choices = tuple((int(pair[0] in rows[1]), int(pair[1] in columns[1])) for pair in pairs)
        self.assertEqual(checkerboard_encrypt(PLAIN, choices=choices, **options), "".join(pairs))
        self.assertEqual(checkerboard_decrypt(COMPLEX, terminal_period=True, **options), PLAIN)
        alternate = checkerboard_encrypt(PLAIN, **options)
        self.assertNotEqual(alternate, "".join(pairs))
        self.assertEqual(checkerboard_decrypt(alternate, **options), PLAIN)

    def test_numeric_coordinate_labels_and_merged_j(self):
        options = {"square": "ABCDEFGHIKLMNOPQRSTUVWXYZ", "row_labels": ("12345",), "column_labels": ("67890",)}
        self.assertEqual(checkerboard_encrypt("A J Z", **options), "162950")
        self.assertEqual(checkerboard_decrypt("16 29 50", **options), "AIZ")

    def test_all_cells_and_every_complex_label_combination(self):
        rows, columns = ("HORSE", "BLACK"), ("GRAYS", "WHITE")
        for row_variant in range(2):
            for col_variant in range(2):
                choices = ((row_variant, col_variant),) * 25
                cipher = checkerboard_encrypt(SQUARE, square=SQUARE, row_labels=rows, column_labels=columns, choices=choices)
                expected = "".join(rows[row_variant][i // 5] + columns[col_variant][i % 5] for i in range(25))
                self.assertEqual(cipher, expected)
                self.assertEqual(checkerboard_decrypt(cipher, square=SQUARE, row_labels=rows, column_labels=columns), SQUARE)

    def test_certificate_hashes_actual_recovered_output(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/checkerboard_certificate.json").read_text())
        for vector in cert["vectors"]:
            result = solve_checkerboard(vector["ciphertext"], **vector["keys"])
            self.assertEqual(result.plaintext, PLAIN)
            self.assertEqual(hashlib.sha256(result.plaintext.encode("ascii")).hexdigest(), vector["plaintext_sha256"])
            self.assertEqual(result.details["mode"], "supplied_key")
            self.assertTrue(result.details["lost_word_spaces"])

    def test_invalid_squares_labels_and_selections(self):
        base = {"square": SQUARE, "row_labels": ("BLACK",), "column_labels": ("WHITE",)}
        for changes in ({"square": "A" * 25}, {"square": SQUARE[:-1]}, {"square": "\u03b1" * 25},
                        {"row_labels": "BLACK"}, {"row_labels": ("BLACK", "BLACK")},
                        {"column_labels": ("WHITE", "12344")}, {"column_labels": ("W HI T",)},
                        {"choices": ((True, 0),)}, {"choices": ((1, 0),)}, {"choices": ()}):
            with self.subTest(changes=changes), self.assertRaises((ValueError, TypeError)):
                checkerboard_encrypt("A", **{**base, **changes})

    def test_framing_pair_order_and_input_bounds(self):
        base = {"square": SQUARE, "row_labels": ("BLACK",), "column_labels": ("WHITE",)}
        for cipher in ("", "B", "XB", "HB", "BH!", "BH.", "B\u0397"):
            with self.subTest(cipher=cipher), self.assertRaises(ValueError):
                checkerboard_decrypt(cipher, **base)
        for plain in ("", "123", "caf\u00e9", "A\x00", "A" * 4097):
            with self.assertRaises(ValueError):
                checkerboard_encrypt(plain, **base)
        with self.assertRaises(TypeError):
            checkerboard_decrypt("BH", terminal_period=1, **base)


if __name__ == "__main__":
    unittest.main()
