"""The ACA four-row construction, exact homophones and bounded row inference."""
import hashlib
import json
from pathlib import Path
import unittest

from engine.reverse_engineer import Crib
from engine.solvers.homophonic import homophonic_table, homophonic_encrypt, homophonic_decrypt, solve_homophonic, infer_homophonic

PLAIN = "WORDDIVISIONSMAYBEKEPT"
CIPHER = "16 26 11 99 69 46 33 03 88 79 54 83 12 06 38 94 67 24 04 00 27 89."


class HomophonicTest(unittest.TestCase):
    def test_printed_four_numeric_rows(self):
        table = homophonic_table("GOLF")
        expected = (
            (20,21,22,23,24,25,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19),
            (38,39,40,41,42,43,44,45,46,47,48,49,50,26,27,28,29,30,31,32,33,34,35,36,37),
            (66,67,68,69,70,71,72,73,74,75,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65),
            (96,97,98,99,0,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95),
        )
        self.assertEqual(table, expected)
        self.assertEqual(len(set(sum(table, ()))), 100)

    def test_literal_vector_and_explicit_homophone_choices(self):
        codes = tuple(int(token) for token in CIPHER[:-1].split())
        rows = tuple(((code - 1) % 100) // 25 for code in codes)
        self.assertEqual(homophonic_encrypt(PLAIN, key="GOLF", rows=rows), CIPHER[:-1])
        self.assertEqual(homophonic_decrypt(CIPHER, key="GOLF", terminal_period=True), PLAIN)

    def test_every_row_independent_rotation_oracle_and_code_zero(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for key in ("AAAA", "ZEBR", "JAZZ", "GOLF"):
            merged_key = key.replace("J", "I")
            for row in range(4):
                expected = [((i - alphabet.index(merged_key[row])) % 25 + 1 + 25 * row) % 100 for i in range(25)]
                cipher = homophonic_encrypt(alphabet, key=key, rows=(row,) * 25)
                self.assertEqual(list(map(int, cipher.split())), expected)
                self.assertEqual(homophonic_decrypt(cipher, key=key), alphabet)
        self.assertEqual(homophonic_decrypt("00", key="GOLF"), "E")

    def test_case_spaces_and_i_j_loss_are_explicit(self):
        cipher = homophonic_encrypt("Jig saw", key="JAZZ")
        result = solve_homophonic(cipher, key="IAZZ")
        self.assertEqual(result.plaintext, "IIGSAW")
        self.assertEqual(result.details["letter_merges"], {"J": "I"})
        self.assertTrue(result.details["lost_word_spaces"])
        self.assertEqual(result.details["mode"], "supplied_key")

    def test_crib_inference_predicts_unseen_letters_without_key(self):
        report = infer_homophonic(CIPHER, cribs=(Crib(0, "WORDD"),), terminal_period=True)
        self.assertTrue(report.search_complete)
        self.assertEqual(report.checks, 100)
        self.assertEqual(report.key_pattern, "GOLF")
        self.assertEqual(report.predicted_plaintext, PLAIN)
        self.assertEqual(report.compatible_key_count, 1)
        self.assertEqual(report.known_positions, 5)
        self.assertIsNone(report.claimed_plaintext)

    def test_unobserved_rows_and_budget_exhaustion_remain_unresolved(self):
        partial_key = infer_homophonic(CIPHER, cribs=(Crib(0, "WOR"),), terminal_period=True)
        self.assertEqual(partial_key.key_pattern, "GO??")
        self.assertEqual(partial_key.compatible_key_count, 625)
        self.assertIn("?", partial_key.predicted_plaintext)
        for checks in (0, 1, 99):
            report = infer_homophonic(CIPHER, cribs=(Crib(0, "WORDD"),), max_checks=checks, terminal_period=True)
            self.assertFalse(report.search_complete)
            self.assertEqual(report.checks, checks)
            self.assertEqual(report.stop_reason, "check_limit")
            self.assertIsNone(report.compatible_key_count)
            self.assertIsNone(report.predicted_plaintext)

    def test_incompatible_and_overlapping_crib_controls(self):
        report = infer_homophonic("01 01", cribs=(Crib(0, "AB"),))
        self.assertTrue(report.search_complete)
        self.assertEqual(report.compatible_key_count, 0)
        self.assertIsNone(report.predicted_plaintext)
        duplicates = infer_homophonic(CIPHER, cribs=(Crib(0, "WOR"), Crib(1, "OR")), terminal_period=True)
        self.assertEqual(duplicates.known_positions, 3)
        self.assertEqual(duplicates.compatible_key_count, 625)
        merged = infer_homophonic("01", cribs=(Crib(0, "I"), Crib(0, "J")))
        self.assertEqual(merged.known_positions, 1)
        self.assertEqual(merged.key_pattern, "I???")
        for cribs in ((), (Crib(0, "A"), Crib(0, "B")), (Crib(2, "A"),), (Crib(True, "A"),)):
            with self.assertRaises((ValueError, TypeError)):
                infer_homophonic("01 01", cribs=cribs)

    def test_certificate_hashes_actual_published_output(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/homophonic_certificate.json").read_text())
        recovered = solve_homophonic(cert["ciphertext"], **cert["keys"]).plaintext
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(), cert["plaintext_sha256"])

    def test_invalid_codes_keys_choices_and_finite_bounds(self):
        for key in ("", "A", "ABCDE", "caf\u00e9", "AB1C"):
            with self.assertRaises(ValueError):
                homophonic_table(key)
        for cipher in ("", "1", "100", "01. 02", "01!", "\u0660\u0661", "00."):
            with self.assertRaises(ValueError):
                homophonic_decrypt(cipher, key="GOLF")
        for choices in ((True,), (4,), (), "0"):
            with self.assertRaises((ValueError, TypeError)):
                homophonic_encrypt("A", key="GOLF", rows=choices)
        for checks in (-1, 101, True, 1.5):
            with self.assertRaises((ValueError, TypeError)):
                infer_homophonic("01", cribs=(Crib(0, "A"),), max_checks=checks)
        with self.assertRaises(ValueError):
            homophonic_encrypt("A" * 4097, key="GOLF")
        with self.assertRaises(ValueError):
            homophonic_encrypt("A\x00", key="GOLF")
        with self.assertRaises(ValueError):
            infer_homophonic("01 " * 513, cribs=(Crib(0, "A"),))


if __name__ == "__main__":
    unittest.main()
