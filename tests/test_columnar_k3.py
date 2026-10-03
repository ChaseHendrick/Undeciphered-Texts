"""Recover published Kryptos K3 plaintext with the columnar transposition solver.

Plaintext and ciphertext are taken from Wikipedia's Kryptos article (Solution
of passage 3 / left-side transcript). The NSA FOIA paper (DOCID 4051151)
prints the same letter stream and classifies the system as keyed columnar
transposition. DESPARATLY is intentional. This file does not claim K4 and
does not modify the keyed Vigenère K1/K2 tests.
"""

from __future__ import annotations

import unittest

from engine.alphabet import letters_only
from engine.solvers.columnar import (
    K3_WIDTHS,
    KRYPTOS_K3_CIPHERTEXT,
    KRYPTOS_K3_PLAINTEXT,
    KRYPTOS_K3_SPACED,
    columnar_decrypt_right_to_left,
    columnar_encrypt_right_to_left,
    double_columnar_decrypt,
    double_columnar_encrypt,
    kryptos_k3_sanborn_decrypt,
    kryptos_k3_sanborn_encrypt,
    solve_columnar,
    solve_kryptos_k3,
)


class ColumnarRoundTripTest(unittest.TestCase):
    def test_single_width_roundtrip(self) -> None:
        plain = "SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRISTHATENCUMBEREDXX"
        self.assertEqual(len(plain) % 8, 0)
        cipher = columnar_encrypt_right_to_left(plain, 8)
        self.assertEqual(columnar_decrypt_right_to_left(cipher, 8), plain)

    def test_double_width_roundtrip_on_k3_lengths(self) -> None:
        cipher = double_columnar_encrypt(
            KRYPTOS_K3_PLAINTEXT, K3_WIDTHS[0], K3_WIDTHS[1]
        )
        self.assertEqual(cipher, KRYPTOS_K3_CIPHERTEXT)
        self.assertEqual(
            double_columnar_decrypt(cipher, K3_WIDTHS[0], K3_WIDTHS[1]),
            KRYPTOS_K3_PLAINTEXT,
        )


class KryptosK3Test(unittest.TestCase):
    def test_recovers_published_k3_plaintext_exactly(self) -> None:
        result = solve_kryptos_k3(KRYPTOS_K3_CIPHERTEXT)
        self.assertEqual(result.plaintext, KRYPTOS_K3_PLAINTEXT)
        self.assertEqual(letters_only(result.plaintext), letters_only(KRYPTOS_K3_SPACED))
        self.assertIn("DESPARATLY", result.plaintext)
        self.assertNotIn("DESPERATELY", result.plaintext)
        self.assertTrue(result.plaintext.endswith("ANYTHINGQ"))
        self.assertEqual(len(result.plaintext), 336)
        self.assertEqual(result.method, "columnar-transposition")
        self.assertEqual(result.key, "21x28")
        self.assertNotIn("k4 plaintext", result.details["scope"].lower())

    def test_default_ciphertext_matches_wikipedia_transcript(self) -> None:
        result = solve_kryptos_k3()
        self.assertEqual(result.plaintext, KRYPTOS_K3_PLAINTEXT)

    def test_sanborn_rotation_form_matches_double_columnar(self) -> None:
        sanborn = kryptos_k3_sanborn_decrypt(KRYPTOS_K3_CIPHERTEXT)
        self.assertEqual(sanborn, KRYPTOS_K3_PLAINTEXT)
        self.assertEqual(
            kryptos_k3_sanborn_encrypt(KRYPTOS_K3_PLAINTEXT),
            KRYPTOS_K3_CIPHERTEXT,
        )

    def test_solve_columnar_exposes_general_widths(self) -> None:
        result = solve_columnar(KRYPTOS_K3_CIPHERTEXT, 21, 28)
        self.assertEqual(result.plaintext, KRYPTOS_K3_PLAINTEXT)
        self.assertEqual(result.details["widths"], (21, 28))


if __name__ == "__main__":
    unittest.main()
