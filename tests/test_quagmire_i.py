"""Known-key checks against the ACA Quagmire I sheet, page 71.

https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf
The ciphertext below is transcribed from the sheet, not generated in this test.
"""

import hashlib
import json
import unittest
from pathlib import Path

from engine.alphabet import ALPHABET
from engine.solvers.quagmire_i import (
    quagmire_i_decrypt,
    quagmire_i_encrypt,
    solve_quagmire_i,
)

MESSAGE = (
    "The Quag One is a periodic cipher with a keyed plain alphabet "
    "run against a straight cipher alphabet."
)
PLAIN = (
    "THEQUAGONEISAPERIODICCIPHERWITHAKEYEDPLAINALPHABETRUNAGAINST"
    "ASTRAIGHTCIPHERALPHABET"
)
PRINTED_CIPHER = (
    "QPMGQ RBUJU YIFDM PYAIF QYYJJ JHJYC JLUUT PIDVW YMFSG AESDW HIZRB "
    "LIRVC FCZPE LBPZY YJJJH WLJJL PUP."
)
CIPHER = PRINTED_CIPHER.replace(" ", "").rstrip(".")
KEYS = {"plaintext_keyword": "SPRINGFEVER", "indicator": "FLOWER", "indicator_under": "A"}
CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/quagmire_i_certificate.json"


class QuagmireIPublishedExampleTest(unittest.TestCase):
    def test_encrypt_matches_published_ciphertext(self):
        self.assertEqual(quagmire_i_encrypt(MESSAGE, **KEYS), CIPHER)

    def test_decrypt_recovers_published_plaintext_exactly(self):
        self.assertEqual(quagmire_i_decrypt(PRINTED_CIPHER, **KEYS), PLAIN)

    def test_solver_reports_known_key_and_alphabets(self):
        result = solve_quagmire_i(CIPHER, **KEYS)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.method, "quagmire-i")
        self.assertEqual(result.key, "pt=SPRINGFEVER indicator=FLOWER under=A")
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.details["period"], 6)
        self.assertEqual(result.details["plaintext_alphabet"], "SPRINGFEVABCDHJKLMOQTUWXYZ")
        self.assertEqual(result.details["ciphertext_alphabet"], ALPHABET)

    def test_sheet_keyword_repeats_and_case_are_normalized(self):
        self.assertEqual(
            quagmire_i_encrypt(MESSAGE.lower(), plaintext_keyword="springfev(er)",
                               indicator="flower", indicator_under="a"), CIPHER,
        )

    def test_other_indicator_columns_and_short_periods(self):
        for column in ("S", "A", "Z"):
            for indicator in ("A", "EEL", "LONGERTHANTEXT"):
                with self.subTest(column=column, indicator=indicator):
                    keys = dict(KEYS, indicator=indicator, indicator_under=column)
                    cipher = quagmire_i_encrypt("A z!", **keys)
                    self.assertEqual(len(cipher), 2)
                    self.assertEqual(quagmire_i_decrypt(cipher, **keys), "AZ")
        self.assertNotEqual(
            quagmire_i_encrypt(MESSAGE, **KEYS),
            quagmire_i_encrypt(MESSAGE, **dict(KEYS, indicator_under="S")),
        )

    def test_straight_alphabet_reduces_to_vigenere(self):
        # A standard independent Vigenere vector when both alphabets are straight.
        self.assertEqual(
            quagmire_i_encrypt("ATTACKATDAWN", plaintext_keyword=ALPHABET,
                               indicator="LEMON", indicator_under="A"),
            "LXFOPVEFRNHR",
        )

    def test_empty_and_non_ascii_inputs_are_rejected(self):
        for fn in (quagmire_i_encrypt, quagmire_i_decrypt, solve_quagmire_i):
            for text in ("", "123 !", "caf\u00e9", "\u00df"):
                with self.subTest(function=fn.__name__, text=text):
                    with self.assertRaises(ValueError):
                        fn(text, **KEYS)
            for override in (
                {"plaintext_keyword": "123"}, {"plaintext_keyword": "caf\u00e9"},
                {"indicator": ""}, {"indicator": "\u00df"},
                {"indicator_under": "AB"}, {"indicator_under": ""},
            ):
                with self.subTest(function=fn.__name__, override=override):
                    with self.assertRaises(ValueError):
                        fn(CIPHER, **dict(KEYS, **override))


class QuagmireICertificateTest(unittest.TestCase):
    def test_certificate_decrypts_and_matches_plaintext_hash(self):
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "quagmire-i")
        self.assertEqual(cert["message"], MESSAGE)
        self.assertEqual(cert["plaintext"], PLAIN)
        self.assertEqual(cert["ciphertext"], CIPHER)
        self.assertEqual(cert["source_url"],
                         "https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireI.pdf")
        keys = {name: cert["keys"][name] for name in KEYS}
        self.assertEqual(keys, KEYS)
        recovered = solve_quagmire_i(cert["ciphertext"], **keys)
        self.assertEqual(recovered.plaintext, PLAIN)
        self.assertEqual(recovered.key, cert["key"])
        self.assertEqual(hashlib.sha256(recovered.plaintext.encode("utf-8")).hexdigest(),
                         cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
