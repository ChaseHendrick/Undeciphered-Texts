"""ACA Condi printed answer and general feedback controls."""
import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.condi import ACA_CIPHER, ACA_MESSAGE, ACA_PLAIN, condi_alphabet, condi_decrypt, condi_encrypt, solve_condi


class CondiTest(unittest.TestCase):
    def test_printed_alphabet_and_complete_formatted_known_answer(self):
        self.assertEqual(condi_alphabet("STRANGE", shift=21), "VWXYZSTRANGEBCDFHIJKLMOPQU")
        settings = {"keyword": "STRANGE", "initial_offset": 25, "alphabet_shift": 21}
        self.assertEqual(condi_decrypt(ACA_CIPHER, **settings), ACA_MESSAGE)
        self.assertEqual(condi_encrypt(ACA_MESSAGE, **settings), ACA_CIPHER)
        self.assertEqual(condi_encrypt("OUR", **settings), "MOR")

    def test_one_based_feedback_including_position26_and_separators(self):
        self.assertEqual(condi_encrypt("AZ A!", keyword="ABCDEFGHIJKLMNOPQRSTUVWXYZ", initial_offset=0), "AA A!")
        self.assertEqual(condi_decrypt("AA A!", keyword="ABCDEFGHIJKLMNOPQRSTUVWXYZ", initial_offset=0), "AZ A!")
        self.assertEqual(condi_encrypt("*Ours, is!", keyword="STRANGE", initial_offset=25, alphabet_shift=21), "*MORC, PP!")

    def test_general_keywords_offsets_and_shifts_roundtrip(self):
        plain = "THE QUICK, BROWN FOX! *ALICE'S 2 BOOKS."
        for keyword in ("ALPHABET", "REPEATED", "Z", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            for shift in (0, 1, 13, 25):
                for offset in (0, 1, 25, 26):
                    cipher = condi_encrypt(plain, keyword=keyword, initial_offset=offset, alphabet_shift=shift)
                    self.assertEqual(condi_decrypt(cipher, keyword=keyword, initial_offset=offset, alphabet_shift=shift), plain)

    def test_wrapper_records_supplied_key_and_certificate_hash(self):
        result = solve_condi(ACA_CIPHER, keyword="STRANGE", initial_offset=25, alphabet_shift=21)
        self.assertEqual(result.plaintext, ACA_MESSAGE)
        self.assertEqual(result.method, "condi")
        self.assertEqual(result.details["mode"], "known_key")
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/condi_certificate.json").read_text())
        self.assertEqual(certificate["plaintext"], ACA_PLAIN)
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(ACA_PLAIN.encode("ascii")).hexdigest())

    def test_invalid_inputs_fail_without_unicode_conversion(self):
        for text in ("", "123!", "caf\u00e9"):
            with self.assertRaises(ValueError):
                condi_encrypt(text, keyword="KEY", initial_offset=1)
        with self.assertRaises(TypeError):
            condi_encrypt(None, keyword="KEY", initial_offset=1)
        for keyword in ("", "123", "\u03b1"):
            with self.assertRaises(ValueError):
                condi_alphabet(keyword)
        for name, value in (("initial_offset", -1), ("initial_offset", 27), ("initial_offset", True), ("alphabet_shift", 26), ("alphabet_shift", 1.5)):
            settings = {"keyword": "KEY", "initial_offset": 1, name: value}
            with self.subTest(name=name, value=value), self.assertRaises((ValueError, TypeError)):
                condi_encrypt("TEXT", **settings)

    def test_bounded_supplied_dictionary_search_recovers_synthetic_settings(self):
        from engine.reverse_engineer import Crib
        from engine.solvers.condi import infer_condi
        plain = "MEETINGATDAWNUSETHEWESTGATETOMORROWBRINGONLYTHESEALEDLETTER"
        cipher = "YHWZGVQFRABVBTLVZFAOOVYDFRZZMSSLSLDWRFVQUEYBWFAVVSKGCMGZCZY"
        report = infer_condi(cipher, keywords=("PLANET", "SECRET", "CIPHER"), cribs=[Crib(0, plain[:15])], max_checks=3000)
        self.assertTrue(report.search_complete)
        self.assertIsNone(report.claimed_plaintext)
        hits = [candidate for candidate in report.candidates if candidate.keyword == "SECRT" and candidate.alphabet_shift == 7 and candidate.initial_offset == 9]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].predicted_plaintext, plain)

    def test_condi_candidate_search_caps_cribs_and_invalid_settings(self):
        from engine.reverse_engineer import Crib
        from engine.solvers.condi import infer_condi
        for cap in (0, 1):
            report = infer_condi("ABC", keywords=("KEY",), cribs=[Crib(0, "A")], max_checks=cap)
            self.assertFalse(report.search_complete)
            self.assertLessEqual(report.checks, cap)
        for changes in ({"keywords": ()}, {"keywords": "KEY"}, {"alphabet_shifts": (26,)}, {"initial_offsets": (-1,)}, {"max_checks": True}, {"max_candidates": 0}):
            settings = {"keywords": ("KEY",), "cribs": [Crib(0, "A")], **changes}
            with self.subTest(changes=changes), self.assertRaises((ValueError, TypeError)):
                infer_condi("ABC", **settings)
        with self.assertRaises(ValueError):
            infer_condi("ABC", keywords=("KEY",), cribs=[Crib(0, "A"), Crib(0, "B")])


if __name__ == "__main__":
    unittest.main()
