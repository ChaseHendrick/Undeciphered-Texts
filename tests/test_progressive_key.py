"""Printed ACA prefix and bounded inference without a supplied keyword."""
import hashlib
import json
import unittest
from pathlib import Path

from engine.reverse_engineer import Crib
from engine.solvers.progressive_key import ACA_CIPHER, ACA_PLAIN, infer_progressive_key, progressive_key_decrypt, progressive_key_encrypt, solve_progressive_key

SYNTHETIC_PLAIN = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGPACKMYBOXWITHFIVEDOZENLIQUORJUGS"
SYNTHETIC_CIPHER = "ELQEHANDWLNONHPDIBVXFUJUGNUZIWASFSJXBLVWNJEPNEIEEGYAHUEOQWVCLYJDNEJ"


class ProgressiveKeyTest(unittest.TestCase):
    def test_independently_printed30_letter_example(self):
        self.assertEqual(len(ACA_PLAIN), 30)
        self.assertEqual(progressive_key_encrypt(ACA_PLAIN, keyword="GRAPEFRUIT", progression=1), ACA_CIPHER)
        self.assertEqual(progressive_key_decrypt(ACA_CIPHER, keyword="GRAPEFRUIT", progression=1), ACA_PLAIN)

    def test_keyword_repeats_progression_zero_and_short_final_group(self):
        for keyword in ("REPEATED", "Z", "ABCABC"):
            for progression in (0, 1, 7, 25):
                plain = "SEPARATORS ARE IGNORED AND NO PADDING IS ADDED"
                cipher = progressive_key_encrypt(plain, keyword=keyword, progression=progression)
                self.assertEqual(progressive_key_decrypt(cipher, keyword=keyword, progression=progression), plain.replace(" ", ""))
        self.assertEqual(progressive_key_encrypt("AAAAAAA", keyword="ABC", progression=2), "ABCCDEE")

    def test_synthetic_unknown_keyword_period_and_progression_are_inferred(self):
        report = infer_progressive_key(SYNTHETIC_CIPHER, cribs=[Crib(0, SYNTHETIC_PLAIN[:15])], max_period=8)
        self.assertTrue(report.search_complete)
        self.assertEqual(report.checks, 8 * 26)
        self.assertIsNone(report.claimed_plaintext)
        hits = [candidate for candidate in report.candidates if candidate.key == "LEMON" and candidate.progression == 7]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].predicted_plaintext, SYNTHETIC_PLAIN)
        self.assertEqual(hits[0].period, 5)
        self.assertTrue(hits[0].key_complete)
        self.assertEqual(len(report.candidates), 1)

    def test_missing_slots_remain_unknown_and_duplicate_cribs_add_no_evidence(self):
        report = infer_progressive_key("BCDABC", cribs=[Crib(0, "A"), Crib(0, "A")], max_period=3, progressions=(0,))
        candidate = next(row for row in report.candidates if row.period == 3)
        self.assertEqual(candidate.key, "B??")
        self.assertEqual(candidate.predicted_plaintext, "A??Z??")
        self.assertFalse(candidate.key_complete)
        self.assertEqual(report.known_positions, 1)

    def test_check_and_candidate_caps_are_explicitly_incomplete(self):
        for cap in (0, 1):
            report = infer_progressive_key(SYNTHETIC_CIPHER, cribs=[Crib(0, "T")], max_period=8, max_checks=cap)
            self.assertFalse(report.search_complete)
            self.assertTrue(report.exhausted)
            self.assertLessEqual(report.checks, cap)
        report = infer_progressive_key("BCDABC", cribs=[Crib(0, "A")], max_period=3, max_candidates=1)
        self.assertEqual(len(report.candidates), 1)
        self.assertFalse(report.search_complete)
        self.assertEqual(report.exhaustion_reason, "candidate_limit")

    def test_wrapper_and_published_and_synthetic_certificate_hashes(self):
        result = solve_progressive_key(ACA_CIPHER, keyword="GRAPEFRUIT", progression=1)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.details["mode"], "known_key")
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/progressive_key_certificate.json").read_text())
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(ACA_PLAIN.encode("ascii")).hexdigest())
        fixture = certificate["unknown_key_fixture"]
        self.assertEqual(fixture["ciphertext"], SYNTHETIC_CIPHER)
        report = infer_progressive_key(fixture["ciphertext"], cribs=[Crib(**crib) for crib in fixture["cribs"]], max_period=fixture["max_period"])
        self.assertEqual(hashlib.sha256(report.candidates[0].predicted_plaintext.encode("ascii")).hexdigest(), fixture["plaintext_sha256"])

    def test_invalid_known_keys_cribs_and_finite_bounds(self):
        for keyword in ("", "123", "caf\u00e9"):
            with self.assertRaises(ValueError):
                progressive_key_encrypt("ABC", keyword=keyword, progression=1)
        for value in (-1, 26, True, 1.5):
            with self.assertRaises((ValueError, TypeError)):
                progressive_key_encrypt("ABC", keyword="A", progression=value)
        for changes in ({"max_period": 0}, {"max_period": 129}, {"progressions": ()}, {"progressions": (26,)}, {"progressions": "1"}, {"max_checks": -1}, {"max_checks": True}, {"max_candidates": 0}):
            with self.subTest(changes=changes), self.assertRaises((ValueError, TypeError)):
                infer_progressive_key("ABC", cribs=[Crib(0, "A")], **changes)
        for cribs in ([], [Crib(3, "A")], [Crib(0, "A"), Crib(0, "B")], [Crib(True, "A")], [Crib(0, "\u03b1")]):
            with self.assertRaises((ValueError, TypeError)):
                infer_progressive_key("ABC", cribs=cribs)


if __name__ == "__main__":
    unittest.main()
