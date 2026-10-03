"""Periodic Gromark's published keyed alphabet, chain, and complete answer."""
import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.periodic_gromark import ACA_CIPHER, ACA_PLAIN, ACA_PRINTED_CIPHER, periodic_gromark_alphabet, periodic_gromark_decrypt, periodic_gromark_encrypt, periodic_gromark_frame, periodic_gromark_keyword, periodic_gromark_primer, periodic_gromark_running_key, periodic_gromark_unframe, solve_periodic_gromark


class PeriodicGromarkTest(unittest.TestCase):
    def test_printed_key_transposition_alphabet_and_chain(self):
        self.assertEqual(periodic_gromark_primer("ENIGMA"), "264351")
        self.assertEqual(periodic_gromark_alphabet("ENIGMA"), "AJRXEBKSYGFPVIDOUMHQWNCLTZ")
        self.assertEqual(periodic_gromark_running_key("ENIGMA", 64), "2643518078698754575299227181498995377848045228497402361425975674")
        self.assertEqual(periodic_gromark_keyword("REPEATED"), "REPATD")
        self.assertEqual(periodic_gromark_primer("REPEATED"), "534162")

    def test_complete_printed_plaintext_and_ciphertext(self):
        self.assertEqual(periodic_gromark_encrypt(ACA_PLAIN, keyword="ENIGMA"), ACA_CIPHER)
        self.assertEqual(periodic_gromark_decrypt(ACA_CIPHER, keyword="ENIGMA"), ACA_PLAIN)
        self.assertEqual(periodic_gromark_encrypt("WINTRY", keyword="ENIGMA"), "RHNAAX")

    def test_framing_primer_and_check_digit_are_explicit_and_verified(self):
        self.assertEqual(periodic_gromark_frame(ACA_CIPHER, keyword="ENIGMA"), ACA_PRINTED_CIPHER)
        self.assertEqual(periodic_gromark_unframe(ACA_PRINTED_CIPHER, keyword="ENIGMA"), ACA_CIPHER)
        self.assertEqual(periodic_gromark_decrypt(ACA_PRINTED_CIPHER, keyword="ENIGMA", framed=True), ACA_PLAIN)
        for text in (ACA_PRINTED_CIPHER.replace("264351", "264352"), ACA_PRINTED_CIPHER[:-2] + "5."):
            with self.assertRaises(ValueError):
                periodic_gromark_unframe(text, keyword="ENIGMA")
        with self.assertRaises(ValueError):
            periodic_gromark_decrypt(ACA_PRINTED_CIPHER, keyword="ENIGMA")

    def test_general_repeated_keywords_periods_and_short_groups(self):
        plain = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        for keyword in ("AB", "CAB", "REPEATED", "SECRET", "ABCDEFGHI"):
            cipher = periodic_gromark_encrypt(plain, keyword=keyword)
            self.assertEqual(periodic_gromark_decrypt(cipher, keyword=keyword), plain.replace(" ", ""))
            framed = periodic_gromark_frame(cipher, keyword=keyword)
            self.assertEqual(periodic_gromark_decrypt(framed, keyword=keyword, framed=True), plain.replace(" ", ""))

    def test_large_valid_frames_remain_readable_after_grouping_expansion(self):
        body = "A" * 700000
        framed = periodic_gromark_frame(body, keyword="AB")
        self.assertGreater(len(framed), 1000000)
        self.assertEqual(periodic_gromark_unframe(framed, keyword="AB"), body)

    def test_wrapper_and_certificate_hash(self):
        result = solve_periodic_gromark(ACA_PRINTED_CIPHER, keyword="ENIGMA", framed=True)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.details["period"], 6)
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/periodic_gromark_certificate.json").read_text())
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(ACA_PLAIN.encode("ascii")).hexdigest())

    def test_invalid_types_alphabets_keyword_widths_and_lengths(self):
        for keyword in ("", "A", "ABCDEFGHIJ", "\u03b1\u03b2", "123"):
            with self.assertRaises(ValueError):
                periodic_gromark_keyword(keyword)
        for text in ("", "123", "caf\u00e9"):
            with self.assertRaises(ValueError):
                periodic_gromark_encrypt(text, keyword="KEY")
        for length in (-1, 1000001, True, 1.5):
            with self.assertRaises((ValueError, TypeError)):
                periodic_gromark_running_key("KEY", length)
        self.assertEqual(periodic_gromark_running_key("KEY", 0), "")


if __name__ == "__main__":
    unittest.main()
