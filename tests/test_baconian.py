"""Both independently printed ACA Baconian carriers and explicit variants."""
import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.baconian import ACA_CARRIER_INITIALS, ACA_CARRIER_LETTERS, baconian_decode, baconian_encode, baconian_extract, solve_baconian


class BaconianTest(unittest.TestCase):
    def test_published_word_initials_carrier_recovers_success(self):
        units = baconian_extract(ACA_CARRIER_INITIALS, extraction="word_initials")
        self.assertEqual(units, "baaab baabb aaaba aaaba aabaa baaab baaab".replace(" ", ""))
        self.assertEqual(baconian_decode(units, variant="24"), "SUCCESS")
        result = solve_baconian(ACA_CARRIER_INITIALS, extraction="word_initials", variant="24")
        self.assertEqual(result.plaintext, "SUCCESS")

    def test_published_every_letter_carrier_matches_printed11_letter_answer(self):
        result = solve_baconian(ACA_CARRIER_LETTERS, extraction="every_letter", variant="24")
        self.assertEqual(result.plaintext, "NOWISAGOODT")
        self.assertEqual(result.details["unit_count"], 55)
        self.assertEqual(result.details["merged_letter_choices"], [{"offset": 3, "choices": ["I", "J"]}])

    def test_all_codes_and_merged_letter_loss_are_explicit(self):
        alphabet24 = "ABCDEFGHIKLMNOPQRSTUWXYZ"
        for variant, alphabet in (("24", alphabet24), ("26", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")):
            units = baconian_encode(alphabet, variant=variant)
            self.assertEqual(baconian_decode(units, variant=variant), alphabet)
        self.assertEqual(baconian_encode("J V", variant="24"), baconian_encode("I U", variant="24"))
        self.assertEqual(baconian_decode(baconian_encode("J V", variant="24"), variant="24"), "IU")
        self.assertEqual(baconian_decode(baconian_encode("J V", variant="26"), variant="26"), "JV")
        self.assertEqual(baconian_decode("babbb", variant="24"), "Z")
        self.assertEqual(baconian_decode("bbaab", variant="26"), "Z")

    def test_extraction_is_explicit_and_word_tokenization_is_documented(self):
        self.assertEqual(baconian_extract("*Now, is a good time!", extraction="word_initials"), "baaab")
        self.assertEqual(baconian_extract("N-O A'M", extraction="every_letter"), "bbaa")
        self.assertEqual(baconian_extract("ALPHA-BETA CAN'T DOG", extraction="word_initials"), "aaa")
        with self.assertRaises(TypeError):
            solve_baconian(ACA_CARRIER_INITIALS)
        with self.assertRaises(ValueError):
            solve_baconian(ACA_CARRIER_INITIALS, extraction="font_style", variant="24")

    def test_direct_grouping_trailing_units_and_unused_codes_are_rejected(self):
        self.assertEqual(baconian_decode("AAAAA aaaab\nAAABA", variant="24"), "ABC")
        for units in ("", "aaaa", "aaaaaa", "a aaab", "aabaa ab", "01010", "aaaac", "bbbbb", "bbaaa"):
            with self.subTest(units=units), self.assertRaises(ValueError):
                baconian_decode(units, variant="24")
        with self.assertRaises(ValueError):
            baconian_decode("bbaba", variant="26")
        result = solve_baconian("aaaba aaaaa baaba", extraction="direct", variant="24")
        self.assertEqual(result.plaintext, "CAT")

    def test_carrier_counts_finite_bounds_unicode_and_variants(self):
        for text in ("", "1234", "caf\u00e9", "\u03b1\u03b2"):
            with self.assertRaises(ValueError):
                baconian_extract(text, extraction="every_letter")
        with self.assertRaises(ValueError):
            solve_baconian("ABCD", extraction="every_letter", variant="24")
        with self.assertRaises(ValueError):
            baconian_extract("A" * 10001, extraction="every_letter")
        with self.assertRaises(ValueError):
            baconian_extract(" " * 100001, extraction="word_initials")
        for variant in ("25", 24, None, True):
            with self.assertRaises((ValueError, TypeError)):
                baconian_decode("aaaaa", variant=variant)

    def test_both_certificate_answers_hash_recovered_output(self):
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/baconian_certificate.json").read_text())
        for vector in certificate["vectors"]:
            result = solve_baconian(vector["ciphertext"], extraction=vector["extraction"], variant=vector["variant"])
            self.assertEqual(result.plaintext, vector["plaintext"])
            self.assertEqual(hashlib.sha256(result.plaintext.encode("ascii")).hexdigest(), vector["plaintext_sha256"])
            self.assertTrue(result.details["plaintext_spacing_lost"])
            self.assertEqual(result.details["mode"], "specified_extraction")


if __name__ == "__main__":
    unittest.main()
