"""Quagmire IV known-key recovery against the ACA sheet worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/QuagmireIV.pdf

Plaintext keyword SENSORY. Ciphertext keyword PERC(EP)TION. Indicator
EXTRA under plaintext S, period 5. Printed plaintext "This one employs
three keywords". Printed ciphertext VBMRF CYISP MPBRR HEICX RREIG DX.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.alphabet import letters_only
from engine.solvers import SOLVERS
from engine.solvers.quagmire_iv import (
    ACA_CIPHER,
    ACA_CIPHERTEXT_ALPHABET,
    ACA_CIPHERTEXT_KEYWORD,
    ACA_INDICATOR,
    ACA_INDICATOR_UNDER,
    ACA_KEY,
    ACA_MESSAGE,
    ACA_PLAIN,
    ACA_PLAINTEXT_ALPHABET,
    ACA_PLAINTEXT_KEYWORD,
    ACA_PRINTED_CIPHER,
    ACA_URL,
    quagmire_iv_alphabet,
    quagmire_iv_decrypt,
    quagmire_iv_encrypt,
    quagmire_iv_row,
    solve_quagmire_iv,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "quagmire_iv_certificate.json"
)

_SHEET_ROWS = (
    "ERCTIONABDFGHJKLMQSUVWXYZP",
    "XYZPERCTIONABDFGHJKLMQSUVW",
    "TIONABDFGHJKLMQSUVWXYZPERC",
    "RCTIONABDFGHJKLMQSUVWXYZPE",
    "ABDFGHJKLMQSUVWXYZPERCTION",
)


def _decrypt(text: str, **overrides: str) -> str:
    args = {
        "plaintext_keyword": ACA_PLAINTEXT_KEYWORD,
        "ciphertext_keyword": ACA_CIPHERTEXT_KEYWORD,
        "indicator": ACA_INDICATOR,
        "indicator_under": ACA_INDICATOR_UNDER,
    }
    args.update(overrides)
    return quagmire_iv_decrypt(text, **args)


def _encrypt(text: str, **overrides: str) -> str:
    args = {
        "plaintext_keyword": ACA_PLAINTEXT_KEYWORD,
        "ciphertext_keyword": ACA_CIPHERTEXT_KEYWORD,
        "indicator": ACA_INDICATOR,
        "indicator_under": ACA_INDICATOR_UNDER,
    }
    args.update(overrides)
    return quagmire_iv_encrypt(text, **args)


class QuagmireIvScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.quagmire_iv as quagmire_mod

        doc = (quagmire_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("ciphers/QuagmireIV.pdf", ACA_URL)
        self.assertNotIn("quagmire-iv", SOLVERS)
        self.assertNotIn("quagmire_iv", SOLVERS)


class QuagmireIvPublishedExampleTest(unittest.TestCase):
    """ACA sheet: SENSORY, PERCEPTION, EXTRA under S."""

    def test_keyed_alphabets_match_the_published_block(self) -> None:
        self.assertEqual(quagmire_iv_alphabet("SENSORY"), ACA_PLAINTEXT_ALPHABET)
        self.assertEqual(quagmire_iv_alphabet("PERCEPTION"), ACA_CIPHERTEXT_ALPHABET)
        self.assertEqual(quagmire_iv_alphabet("PERC(EP)TION"), ACA_CIPHERTEXT_ALPHABET)
        self.assertEqual(len(ACA_PLAINTEXT_ALPHABET), 26)
        self.assertEqual(len(ACA_CIPHERTEXT_ALPHABET), 26)
        under = ACA_PLAINTEXT_ALPHABET.index("S")
        for letter, expected in zip("EXTRA", _SHEET_ROWS):
            self.assertEqual(
                quagmire_iv_row(ACA_CIPHERTEXT_ALPHABET, letter, under),
                expected,
            )

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = _encrypt(ACA_MESSAGE)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(_encrypt(ACA_PLAIN, ciphertext_keyword="PERC(EP)TION"), ACA_CIPHER)
        self.assertEqual(_encrypt(ACA_MESSAGE, plaintext_keyword="sensory", indicator="extra", indicator_under="s"), ACA_CIPHER)
        self.assertEqual(ACA_CIPHER, ACA_PRINTED_CIPHER.replace(" ", ""))

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = _decrypt(ACA_PRINTED_CIPHER)
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(_decrypt(ACA_CIPHER, ciphertext_keyword="PERC(EP)TION"), ACA_PLAIN)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_quagmire_iv(
            ACA_CIPHER,
            plaintext_keyword=ACA_PLAINTEXT_KEYWORD,
            ciphertext_keyword=ACA_CIPHERTEXT_KEYWORD,
            indicator=ACA_INDICATOR,
            indicator_under=ACA_INDICATOR_UNDER,
        )
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "quagmire-iv")
        self.assertEqual(result.key, ACA_KEY)
        self.assertEqual(result.details["source_url"], ACA_URL)
        self.assertEqual(result.details["period"], 5)
        self.assertEqual(result.details["plaintext_alphabet"], ACA_PLAINTEXT_ALPHABET)
        self.assertEqual(result.details["ciphertext_alphabet"], ACA_CIPHERTEXT_ALPHABET)
        self.assertEqual(result.details["indicator"], "EXTRA")
        self.assertEqual(result.details["indicator_under"], "S")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)

    def test_indicator_column_changes_ciphertext_and_roundtrips(self) -> None:
        shifted = _encrypt(ACA_MESSAGE, indicator_under="A")
        self.assertNotEqual(shifted, ACA_CIPHER)
        self.assertEqual(
            _decrypt(shifted, indicator_under="A"),
            ACA_PLAIN,
        )
        other = _encrypt("the early bird", indicator="EEL", indicator_under="Y")
        self.assertEqual(
            _decrypt(other, indicator="EEL", indicator_under="Y"),
            letters_only("the early bird"),
        )
        self.assertEqual(len("EEL"), 3)
        self.assertNotEqual(
            other,
            _encrypt("the early bird", indicator="EEL", indicator_under="A"),
        )


class QuagmireIvCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "quagmire-iv")
        self.assertEqual(self.cert["name"], "quagmire-iv")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        keys = self.cert["keys"]
        self.assertEqual(plaintext, ACA_PLAIN)
        self.assertEqual(ciphertext, ACA_CIPHER)
        self.assertEqual(keys["key"], key)
        self.assertEqual(key, ACA_KEY)
        self.assertEqual(keys["plaintext_keyword"], ACA_PLAINTEXT_KEYWORD)
        self.assertEqual(keys["ciphertext_keyword"], ACA_CIPHERTEXT_KEYWORD)
        self.assertEqual(keys["indicator"], ACA_INDICATOR)
        self.assertEqual(keys["indicator_under"], ACA_INDICATOR_UNDER)
        self.assertEqual(keys["plaintext_alphabet"], ACA_PLAINTEXT_ALPHABET)
        self.assertEqual(keys["ciphertext_alphabet"], ACA_CIPHERTEXT_ALPHABET)
        self.assertEqual(keys["period"], 5)
        self.assertEqual(self.cert["message"], ACA_MESSAGE)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            quagmire_iv_decrypt(
                ciphertext,
                plaintext_keyword=keys["plaintext_keyword"],
                ciphertext_keyword=keys["ciphertext_keyword"],
                indicator=keys["indicator"],
                indicator_under=keys["indicator_under"],
            ),
            plaintext,
        )
        self.assertEqual(
            quagmire_iv_encrypt(
                ACA_MESSAGE,
                plaintext_keyword=keys["plaintext_keyword"],
                ciphertext_keyword=keys["ciphertext_keyword"],
                indicator=keys["indicator"],
                indicator_under=keys["indicator_under"],
            ),
            ciphertext,
        )
        self.assertEqual(
            quagmire_iv_encrypt(
                plaintext,
                plaintext_keyword=keys["plaintext_keyword"],
                ciphertext_keyword="PERC(EP)TION",
                indicator=keys["indicator"],
                indicator_under=keys["indicator_under"],
            ),
            ciphertext,
        )
        result = solve_quagmire_iv(
            ciphertext,
            plaintext_keyword=keys["plaintext_keyword"],
            ciphertext_keyword=keys["ciphertext_keyword"],
            indicator=keys["indicator"],
            indicator_under=keys["indicator_under"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(result.key, key)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        self.assertNotIn("\u2014", self.cert["note"])
        self.assertNotIn("\u2013", self.cert["note"])
        self.assertNotIn("\u2014", plaintext)
        self.assertNotIn("\u2013", plaintext)


if __name__ == "__main__":
    unittest.main()
