"""Known-key recovery for the independently printed ACA Quagmire III example.

Source, inspected 2026-10-03:
https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIII.pdf
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.quagmire_iii import (
    ACA_ALPHABET,
    ACA_CIPHER,
    ACA_INDICATOR,
    ACA_INDICATOR_UNDER,
    ACA_KEY,
    ACA_KEYWORD,
    ACA_MESSAGE,
    ACA_PLAIN,
    ACA_PRINTED_CIPHER,
    ACA_URL,
    quagmire_iii_alphabet,
    quagmire_iii_decrypt,
    quagmire_iii_encrypt,
    quagmire_iii_key,
    quagmire_iii_row,
    solve_quagmire_iii,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "quagmire_iii_certificate.json"
)

_SHEET_ROWS = (
    "HJKNPQRSVWXYZAUTOMBILECDFG",
    "ILECDFGHJKNPQRSVWXYZAUTOMB",
    "GHJKNPQRSVWXYZAUTOMBILECDF",
    "HJKNPQRSVWXYZAUTOMBILECDFG",
    "WXYZAUTOMBILECDFGHJKNPQRSV",
    "AUTOMBILECDFGHJKNPQRSVWXYZ",
    "YZAUTOMBILECDFGHJKNPQRSVWX",
)


def _args(**overrides: str) -> dict[str, str]:
    args = {
        "keyword": ACA_KEYWORD,
        "indicator": ACA_INDICATOR,
        "indicator_under": ACA_INDICATOR_UNDER,
    }
    args.update(overrides)
    return args


class QuagmireIiiPublishedExampleTest(unittest.TestCase):
    def test_keyed_alphabet_and_rows_match_the_printed_block(self) -> None:
        self.assertEqual(quagmire_iii_alphabet("AUTOMOBILE"), ACA_ALPHABET)
        self.assertEqual(ACA_ALPHABET, "AUTOMBILECDFGHJKNPQRSVWXYZ")
        under_index = ACA_ALPHABET.index("A")
        for letter, expected in zip("HIGHWAY", _SHEET_ROWS):
            with self.subTest(indicator=letter):
                self.assertEqual(quagmire_iii_row(ACA_ALPHABET, letter, under_index), expected)

    def test_encrypt_matches_the_independent_printed_ciphertext(self) -> None:
        printed = "KRSLW MITJD VIABM RGQMT MLLIV IFUIX RHTNY ONVRH HIIIR MCAOV EI"
        self.assertEqual(ACA_PRINTED_CIPHER, printed)
        self.assertEqual(ACA_CIPHER, printed.replace(" ", ""))
        self.assertEqual(quagmire_iii_encrypt(ACA_MESSAGE, **_args()), ACA_CIPHER)

    def test_decrypt_recovers_the_independent_printed_plaintext(self) -> None:
        expected = "THESAMEKEYEDALPHABETISUSEDFORPLAINANDCIPHERALPHABETS"
        self.assertEqual(ACA_PLAIN, expected)
        self.assertEqual(quagmire_iii_decrypt(ACA_PRINTED_CIPHER + ".", **_args()), expected)

    def test_solver_reports_known_key_recovery_and_source(self) -> None:
        result = solve_quagmire_iii(ACA_CIPHER, **_args())
        self.assertEqual(result.method, "quagmire-iii")
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.key, ACA_KEY)
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.details["source_url"], ACA_URL)
        self.assertEqual(result.details["keyword"], ACA_KEYWORD)
        self.assertEqual(result.details["plaintext_alphabet"], ACA_ALPHABET)
        self.assertEqual(result.details["ciphertext_alphabet"], ACA_ALPHABET)
        self.assertEqual(result.details["period"], 7)
        self.assertEqual(result.details["indicator_under"], "A")
        self.assertEqual(result.details["letters"], 52)

    def test_general_keys_and_nonfirst_indicator_column_roundtrip(self) -> None:
        args = _args(keyword="sensory", indicator="e-e-l", indicator_under="y")
        plain = "THEEARLYBIRDCATCHESAWORM"
        cipher = quagmire_iii_encrypt("The early bird catches a worm!", **args)
        self.assertEqual(quagmire_iii_decrypt(cipher, **args), plain)
        self.assertNotEqual(cipher, quagmire_iii_encrypt(plain, **{**args, "indicator_under": "A"}))
        self.assertNotEqual(cipher, quagmire_iii_encrypt(plain, **{**args, "indicator": "EL"}))
        self.assertEqual(quagmire_iii_key(**args), "keyword=SENSORY indicator=EEL under=Y")
        self.assertEqual(len(cipher), len(plain))


class QuagmireIiiInvalidInputTest(unittest.TestCase):
    def test_letterless_and_non_ascii_letter_inputs_are_rejected(self) -> None:
        for transform in (quagmire_iii_encrypt, quagmire_iii_decrypt, solve_quagmire_iii):
            for bad in ("", "123 !", "caf\u00e9", "stra\u00dfe"):
                with self.subTest(transform=transform.__name__, text=bad):
                    with self.assertRaises(ValueError):
                        transform(bad, **_args())
            for name, bad in (
                ("keyword", "123"),
                ("keyword", "caf\u00e9"),
                ("indicator", "!!!"),
                ("indicator", "\u00df"),
                ("indicator_under", "AB"),
                ("indicator_under", "123"),
                ("indicator_under", "\u00e9"),
            ):
                with self.subTest(transform=transform.__name__, name=name, value=bad):
                    with self.assertRaises(ValueError):
                        transform(ACA_CIPHER, **_args(**{name: bad}))

    def test_nonstring_parameters_are_rejected_clearly(self) -> None:
        for name in ("keyword", "indicator", "indicator_under"):
            with self.subTest(name=name):
                with self.assertRaises(TypeError):
                    quagmire_iii_encrypt(ACA_PLAIN, **_args(**{name: None}))
        with self.assertRaises(TypeError):
            quagmire_iii_decrypt(None, **_args())

    def test_invalid_row_alphabet_or_column_is_rejected(self) -> None:
        for alphabet in ("A" * 26, "ABCDEFGHIJKLMNOPQRSTUVWXY!", ACA_ALPHABET.lower()):
            with self.subTest(alphabet=alphabet):
                with self.assertRaises(ValueError):
                    quagmire_iii_row(alphabet, "A", 0)
        for index in (-1, 26):
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    quagmire_iii_row(ACA_ALPHABET, "A", index)


class QuagmireIiiCertificateTest(unittest.TestCase):
    def test_certificate_decrypts_and_hashes_the_recovered_plaintext(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        keys = cert["keys"]
        plain = quagmire_iii_decrypt(
            cert["ciphertext"],
            keyword=keys["keyword"],
            indicator=keys["indicator"],
            indicator_under=keys["indicator_under"],
        )
        self.assertEqual(cert["cipher_name"], "quagmire-iii")
        self.assertEqual(cert["name"], "quagmire-iii")
        self.assertEqual(plain, cert["plaintext"])
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(hashlib.sha256(plain.encode("utf-8")).hexdigest(), cert["plaintext_sha256"])
        self.assertEqual(quagmire_iii_encrypt(cert["message"], **_args()), cert["ciphertext"])
        self.assertEqual(cert["source_url"], ACA_URL)
        self.assertEqual(cert["key"], quagmire_iii_key(**_args()))
        self.assertEqual(keys["key"], cert["key"])
        self.assertEqual(keys["plaintext_alphabet"], ACA_ALPHABET)
        self.assertEqual(keys["ciphertext_alphabet"], ACA_ALPHABET)
        self.assertEqual(keys["period"], 7)
        self.assertEqual(len(cert["source_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
