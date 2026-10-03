"""AMSCO known-key recovery against a published worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac
Z13, Zodiac Z32, the Beale ciphers, the McCormick cipher, the Voynich
manuscript, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.amsco import (
    ACA_CIPHER,
    ACA_CIPHER_GROUPS,
    ACA_KEY,
    ACA_PLAIN,
    ACA_PRINTED,
    ACA_START,
    ACA_URL,
    amsco_decrypt,
    amsco_encrypt,
    amsco_letters,
    solve_amsco,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "amsco_certificate.json"
)


class AmscoScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.amsco as amsco_mod

        doc = (amsco_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/Amsco.pdf", ACA_URL)
        self.assertNotIn("amsco", SOLVERS)


class AmscoPublishedExampleTest(unittest.TestCase):
    """ACA sheet: key 41325, first cell a digraph, 57 plaintext letters."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = amsco_encrypt(ACA_PRINTED, ACA_KEY, start=ACA_START)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cipher, "CECRTEGLENPHPLUTNANTEIOMOWIRSITDDSINTNALINESAALEMHATGLRGR")
        self.assertEqual(len(cipher), 57)
        grouped = " ".join(cipher[i : i + 5] for i in range(0, len(cipher), 5))
        self.assertEqual(grouped, ACA_CIPHER_GROUPS)

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = amsco_decrypt(ACA_CIPHER_GROUPS, ACA_KEY, start="digraph")
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(
            plain,
            "INCOMPLETECOLUMNARWITHALTERNATINGSINGLELETTERSANDDIGRAPHS",
        )
        self.assertEqual(len(plain), 57)
        self.assertNotIn(" ", plain)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_amsco(ACA_CIPHER_GROUPS, key=ACA_KEY, start=ACA_START)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "amsco")
        self.assertEqual(result.key, "41325/digraph")
        self.assertEqual(result.details["numeric_key"], "41325")
        self.assertEqual(result.details["start"], "digraph")
        self.assertEqual(result.details["period"], 5)
        self.assertEqual(result.details["source_url"], ACA_URL)
        self.assertEqual(result.details["spaces"], "not_enciphered")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)

    def test_spaces_are_not_enciphered(self) -> None:
        self.assertEqual(amsco_letters(ACA_PRINTED), ACA_PLAIN)
        self.assertNotIn(" ", amsco_encrypt(ACA_PRINTED, ACA_KEY, start="digraph"))
        self.assertEqual(
            amsco_encrypt(ACA_PRINTED, ACA_KEY, start="digraph"),
            amsco_encrypt(ACA_PLAIN, ACA_KEY, start="digraph"),
        )

    def test_single_start_is_a_different_grid(self) -> None:
        other = amsco_encrypt(ACA_PLAIN, ACA_KEY, start="single")
        self.assertNotEqual(other, ACA_CIPHER)
        self.assertEqual(amsco_decrypt(other, ACA_KEY, start="single"), ACA_PLAIN)

    def test_even_period_alternates_the_first_column(self) -> None:
        # Period 4 is even. A continuous left-to-right wrap would repeat
        # the first-column size. The sheet says the first column alternates
        # for even periods too.
        plain = "ABCDEFGHIJ"
        cipher = amsco_encrypt(plain, "3142", start="digraph")
        self.assertEqual(cipher, "CHIFABGDEJ")
        self.assertEqual(amsco_decrypt(cipher, "3142", start="digraph"), plain)
        # Short final cell: 7 letters, period 4, first cell a single.
        short = "ABCDEFG"
        short_cipher = amsco_encrypt(short, "3142", start="single")
        self.assertEqual(amsco_decrypt(short_cipher, "3142", start="single"), short)
        self.assertEqual(len(short_cipher), 7)


class AmscoCertificateTest(unittest.TestCase):
    """Certificate checks the published example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "amsco")
        self.assertEqual(self.cert["name"], "amsco")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        numeric, start = key.split("/")
        self.assertEqual(self.cert["keys"]["numeric_key"], numeric)
        self.assertEqual(self.cert["keys"]["start"], start)
        self.assertEqual(numeric, ACA_KEY)
        self.assertEqual(start, "digraph")
        self.assertNotIn(" ", plaintext)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(amsco_decrypt(ciphertext, numeric, start=start), plaintext)
        result = solve_amsco(ciphertext, key=numeric, start=start)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(amsco_encrypt(plaintext, numeric, start=start), ciphertext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
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
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)


if __name__ == "__main__":
    unittest.main()
