"""Exact conditional composition tests, with independent literal controls."""
import itertools
import random
import unittest

from engine.k4_models import search_k4_models, reencrypt_k4_model
from engine.reverse_engineer import Crib

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MIXED = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
PLAIN = "THEHARBORBELLRANGTWICEBEFOREDAWNANDTHESMALLBOATSLEFTTHEQUAYWITHNETSFOLDEDONTHEDECKATHINMISTHIDTHE"
REPEATING_CIPHER = "FOPQDIXEJZDTTHHGZBPTBUMETPIXTNGTIEDFYIPECPTEIRNHMTLEORYTAAIOPYTWUFCWIWGXIGZAHQTDFAHQNRRQDAXQWXHIF"
AUTOKEY_CIPHER = "UFXBIECICBVTHPUYDWBAIMMIJHVUHJHQBUVUVMRZWHMJEWPDXIMZIQSMUMJGHSFKVWTDTPFZYFJMEISCHMZUVFGWPWXXEWNGV"
BEAUFORT_CIPHER = "TMPIXWBWVZXLFTIVNOMTOHALIXHEWOGWTIMWOHMINMFWWHNXMHTUMNAHPBEBMOWFSKZQHFJEEJCMILTMWMILLJNIXEBKIBTWT"
CIPHER_AUTOKEY = "FVMMWVIOKLAPEWHBMFCLRJQSYNHXTOWLRQMMVGRZXMMZFRJNIHGDORQPHMITCXKQYXLXPEKZECEQEQOUKZPQNQHVMYTXNOVKJ"


def oracle(plain, family, key, alphabet, width, order, direction="left-to-right"):
    columns = range(width) if direction == "left-to-right" else range(width - 1, -1, -1)
    positions = [i for c in columns for i in range(c, len(plain), width)]
    work = plain if order == "substitute-then-transpose" else "".join(plain[i] for i in positions)
    values = [alphabet.index(ch) for ch in work]
    cipher = []
    for i, value in enumerate(values):
        if family in ("repeating", "beaufort") or i < len(key):
            shift = key[i % len(key)]
        elif family == "plaintext-autokey":
            shift = values[i - len(key)]
        else:
            shift = cipher[i - len(key)]
        cipher.append((shift - value if family == "beaufort" else value + shift) % 26)
    rendered = "".join(alphabet[v] for v in cipher)
    return "".join(rendered[i] for i in positions) if order == "substitute-then-transpose" else rendered


class K4ModelsTest(unittest.TestCase):
    def find_control(self, cipher, family, alphabet=AZ, order="substitute-then-transpose"):
        result = search_k4_models(cipher, cribs=(Crib(0, PLAIN[:21]),),
                                 max_period=3, max_width=7, max_checks=1000,
                                 max_candidates=1000, alphabets=(alphabet,),
                                 families=(family,), orders=(order,))
        self.assertTrue(result["search_complete"])
        self.assertIsNone(result["claimed_plaintext"])
        hit = next(c for c in result["candidates"] if c["layout"] ==
                   {"kind": "ragged-columnar", "width": 7, "direction": "left-to-right"}
                   and c["period"] == 3)
        self.assertEqual(hit["predicted_plaintext"], PLAIN)
        self.assertTrue(hit["key_complete"])
        self.assertTrue(hit["re_encryption_matches"])
        self.assertEqual(reencrypt_k4_model(PLAIN, family=family,
                         key_shift_indices=hit["key_shift_indices"], alphabet=alphabet,
                         layout=hit["layout"], order=order), cipher)
        return hit

    def test_literal_ragged_periodic_recovery_without_key(self):
        self.assertEqual(oracle(PLAIN, "repeating", (12, 0, 15), AZ, 7,
                                "substitute-then-transpose"), REPEATING_CIPHER)
        hit = self.find_control(REPEATING_CIPHER, "repeating")
        self.assertEqual(hit["key_shift_indices"], [12, 0, 15])

    def test_literal_keyed_alphabet_autokey_without_primer(self):
        hit = self.find_control(AUTOKEY_CIPHER, "plaintext-autokey", MIXED)
        self.assertEqual(hit["key_shift_indices"], [17, 7, 3])
        self.assertEqual(oracle(PLAIN, "plaintext-autokey", (17, 7, 3), MIXED, 7,
                                "substitute-then-transpose"), AUTOKEY_CIPHER)

    def test_before_substitution_order_keeps_original_crib_coordinates(self):
        self.find_control(BEAUFORT_CIPHER, "beaufort", order="transpose-then-substitute")
        self.assertEqual(oracle(PLAIN, "beaufort", (12, 0, 15), AZ, 7,
                                "transpose-then-substitute"), BEAUFORT_CIPHER)

    def test_ciphertext_autokey_literal_and_independent_oracle(self):
        self.find_control(CIPHER_AUTOKEY, "ciphertext-autokey")
        self.assertEqual(oracle(PLAIN, "ciphertext-autokey", (12, 0, 15), AZ, 7,
                                "substitute-then-transpose"), CIPHER_AUTOKEY)

    def test_primary_autokey_vector_propagates_both_directions(self):
        r = search_k4_models("EHPFSFEBHMHPF", cribs=(Crib(4, "O"),),
                             families=("plaintext-autokey",), alphabets=(AZ,),
                             orders=("substitute-then-transpose",), max_period=1)
        hit = next(c for c in r["candidates"] if c["layout"]["kind"] == "identity")
        self.assertEqual(hit["predicted_plaintext"], "TOBEORNOTTOBE")
        self.assertEqual(hit["key_shift_indices"], [11])

    def test_partial_key_does_not_fill_letters_or_claim_consistency(self):
        r = search_k4_models("BCDEFGHI", cribs=(Crib(0, "A"),), max_period=4,
                             max_candidates=1000, families=("repeating",), alphabets=(AZ,))
        c = next(c for c in r["candidates"] if c["layout"]["kind"] == "identity" and c["period"] == 4)
        self.assertEqual(c["predicted_plaintext"], "A???E???")
        self.assertEqual(c["key_shift_indices"], [1, None, None, None])
        self.assertEqual(c["compatible_key_completions"], 26 ** 3)
        self.assertIsNone(c["re_encryption_matches"])
        self.assertTrue(c["forced_equations_verified"])

    def test_exact_budget_and_fair_family_alphabet_order_coverage(self):
        r = search_k4_models("A" * 97, cribs=(Crib(0, "A"),), max_checks=17,
                             max_candidates=1)
        self.assertEqual(r["checks"], 17)
        self.assertEqual(r["stop_reason"], "check_limit")
        self.assertFalse(r["search_complete"])
        counts = [g["checks"] for g in r["coverage"]]
        self.assertLessEqual(max(counts) - min(counts), 1)
        self.assertTrue(r["candidates_truncated"])
        self.assertGreater(r["compatible_models"], len(r["candidates"]))

    def test_zero_budget_and_retained_cap_do_not_imply_completed_search(self):
        zero = search_k4_models("ABCD", cribs=(Crib(0, "A"),), max_checks=0)
        self.assertEqual(zero["checks"], 0)
        self.assertEqual(zero["candidates"], [])
        self.assertFalse(zero["search_complete"])
        a = search_k4_models("AAAAAAAA", cribs=(Crib(0, "A"),), max_candidates=1,
                             max_period=2, max_width=2, max_checks=1000)
        self.assertTrue(a["search_complete"])
        self.assertTrue(a["candidates_truncated"])
        self.assertIsNone(a["claimed_plaintext"])

    def test_conflicting_constraints_reject_identity_setting(self):
        r = search_k4_models("AAAA", cribs=(Crib(0, "AB"),), max_period=1,
                             families=("repeating",), alphabets=(AZ,), max_candidates=1000)
        self.assertFalse(any(c["layout"]["kind"] == "identity" for c in r["candidates"]))
        self.assertEqual(r["checks"], r["rejected_models"] + r["compatible_models"])

    def test_random_models_match_oracle_for_both_orders_and_column_directions(self):
        draw = random.Random(730)
        for family, order, alphabet, direction in itertools.product(
                ("repeating", "beaufort", "plaintext-autokey", "ciphertext-autokey"),
                ("substitute-then-transpose", "transpose-then-substitute"),
                (AZ, MIXED), ("left-to-right", "right-to-left")):
            plain = "".join(draw.choice(AZ) for _ in range(37))
            key = tuple(draw.randrange(26) for _ in range(3))
            cipher = oracle(plain, family, key, alphabet, 4, order, direction)
            r = search_k4_models(cipher, cribs=(Crib(0, plain[:19]),), max_period=3,
                                 max_width=4, max_checks=1000, max_candidates=1000,
                                 families=(family,), orders=(order,), alphabets=(alphabet,))
            hit = next(c for c in r["candidates"] if c["layout"] ==
                       {"kind": "ragged-columnar", "width": 4, "direction": direction} and c["period"] == 3)
            self.assertEqual(hit["predicted_plaintext"], plain)
            self.assertEqual(hit["key_shift_indices"], list(key))

    def test_invalid_inputs_and_duplicate_models_are_rejected(self):
        for text, options in [(None, {}), ("AB?CD", {}), ("ABéCD", {}), ("A" * 513, {}),
                ("ABCD", {"cribs": ()}), ("ABCD", {"max_checks": True}),
                ("ABCD", {"max_checks": 10001}), ("ABCD", {"max_width": 33}),
                ("ABCD", {"max_period": 0}), ("ABCD", {"max_candidates": 0}),
                ("ABCD", {"families": ("repeating", "repeating")}),
                ("ABCD", {"families": ("unknown",)}), ("ABCD", {"alphabets": ("A" * 26,)}),
                ("ABCD", {"orders": ("bad",)}), ("ABCD", {"cribs": iter((Crib(0, "A"),))}),
                ("ABCD", {"cribs": (Crib(True, "A"),)}),
                ("ABCD", {"cribs": (Crib(4, "A"),)}),
                ("ABCD", {"cribs": (Crib(0, "A"), Crib(0, "B"))})]:
            opts = {"cribs": (Crib(0, "A"),), **options}
            with self.subTest(text=text, opts=opts), self.assertRaises((ValueError, TypeError)):
                search_k4_models(text, **opts)

