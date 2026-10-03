"""Word constraints recover a literal constructed fixture without a supplied key.

The fixture comes from engine.fixtures. Its ciphertext is frozen below rather
than generated in a test. The lexicon contains fixture words and decoys.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import unittest
from pathlib import Path

from engine.fixtures import SUBSTITUTION_PLAIN
from engine.solvers.word_pattern import (
    search_word_pattern,
    solve_word_pattern,
    word_pattern,
)


CIPHER = (
    "Utgsguolzl ygssgvtr zit ektta xhlzktqd xfzos zit ukqcts zxkftr ykgd ukqn koctk "
    "lzgft zg q wqfr gy ktr liqst. Zitn dtqlxktr zit roh gy tqei sqntk qfr vkgzt zit "
    "fxdwtkl of q yotsr wgga wtygkt zit kqof egxsr ldtqk zitd. Gft gxzekgh ligvtr "
    "kohhstl ziqz iqr iqkrtftr vitf zit vqztk vql liqssgv qfr vqkd. Qfgzitk itsr "
    "wkgatf litssl zit lomt gy q zixdwfqos. Zit hqkzn qzt sxfei gf q ysqz wgxsrtk "
    "qfr qkuxtr, vozigxz qfn itqz, qwgxz vitzitk zit korut iqr wttf q wtqei gk q "
    "rtszq. Wn sqzt qyztkfggf zitn iqr lqdhstl tfgxui zg pxlzoyn zit sgfu vqsa "
    "wqea zg zit vqugf. Q jxoea tbzkq wgb gy jxqkzm yobtr zit sqlz uqh of zit ltezogf."
)
EXPECTED_DECRYPT_KEY = "KXVMCNOPHQRSZYIJADLEGWBUFT"
LEXICON = tuple((
    "A ABOUT ABOVE AFTER AFTERNOON AGREE ALONE AND ANOTHER ANY ARGUED AS ASK ATE "
    "BACK BAND BEACH BEEN BEFORE BELL BELOW BLACK BOATS BOOK BOULDER BOX BREAD "
    "BROKEN BROWN BY CHILD CLEAR CLOUD COLD COULD CREEK DANCE DARK DEEP DELTA DIP "
    "DOWN EACH EARTH EMPTY ENOUGH EVERY EXTRA FIELD FIRST FISH FIXED FLAT FOG "
    "FOLLOWED FRESH FROM GAP GEOLOGISTS GLASS GRAVEL GRAY GREAT GREEN HAD HARBOR "
    "HARDENED HEAT HELD HOUSE IN JUSTIFY LAST LATE LAYER LIGHT LITTLE LONG LUNCH "
    "MEASURED MOON MORNING NEVER NIGHT NORTH NUMBERS OF ON ONE ONLY OR OTHER "
    "OUTCROP OVER PAPER PARTY PIER PLACE PRINT QUARTZ QUICK RAIN RED RIDGE RIPPLES "
    "RIVER ROUND SAFE SAMPLES SAND SEA SECTION SHALE SHALLOW SHELLS SHIP SHORE "
    "SHORT SHOWED SILVER SIZE SMALL SMEAR SOFT SOUTH STILL STONE STORM STORY "
    "STREET STRONG SUN SWEET TABLE THAT THE THEM THEN THESE THEY THOSE THREE "
    "THUMBNAIL TIDE TIME TO TODAY TREE TURNED UNDER UNTIL UPSTREAM VERY WAGON "
    "WALK WARM WAS WATER WERE WEST WHEN WHERE WHETHER WHITE WIND WITHOUT WORD "
    "WORLD WROTE YOUNG"
).split())
CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/word_pattern_certificate.json"
SOURCE_URL = "https://github.com/aimacode/aima-python/blob/master/aima/csp.py"


class WordPatternRecoveryTest(unittest.TestCase):
    def test_literal_fixture_recovers_without_plaintext_or_key_input(self):
        search = search_word_pattern(CIPHER, LEXICON, max_nodes=2000)
        self.assertTrue(search.search_complete)
        self.assertTrue(search.unique_within_lexicon)
        self.assertIs(search.ambiguous, False)
        self.assertEqual(len(search.candidates), 1)
        candidate = search.candidates[0]
        self.assertEqual(candidate.plaintext, SUBSTITUTION_PLAIN)
        self.assertEqual(candidate.decrypt_key, EXPECTED_DECRYPT_KEY)
        self.assertTrue(candidate.key_complete)
        self.assertGreater(search.pruned_values, 0)
        self.assertLessEqual(search.nodes, 2000)
        solved = solve_word_pattern(CIPHER, LEXICON, max_nodes=2000)
        self.assertEqual(solved.method, "word-pattern-substitution")
        self.assertEqual(solved.plaintext, SUBSTITUTION_PLAIN)
        self.assertEqual(solved.key, EXPECTED_DECRYPT_KEY)
        self.assertTrue(solved.details["unique_within_lexicon"])

    def test_missing_dictionary_word_has_no_solution_and_no_lookup(self):
        search = search_word_pattern(CIPHER, [word for word in LEXICON if word != "GEOLOGISTS"])
        self.assertTrue(search.search_complete)
        self.assertFalse(search.candidates)
        self.assertFalse(search.unique_within_lexicon)
        self.assertEqual(search.stop_reason, "complete")

    def test_case_and_punctuation_are_preserved(self):
        search = search_word_pattern("Ab, ab! 42", ["to", "TO"])
        self.assertEqual(search.candidates[0].plaintext, "To, to! 42")
        self.assertEqual(search.dictionary_size, 1)
        self.assertEqual(search.unique_words, 1)
        self.assertEqual(search.nodes, 1)
        self.assertEqual(search.candidates[0].decrypt_key, "TO" + "?" * 24)
        self.assertFalse(search.candidates[0].key_complete)

    def test_mrv_selects_smallest_domain_and_constraints_are_injective(self):
        search = search_word_pattern("ABBA XYZ", ["DEED", "NOON", "CAT"])
        self.assertEqual(search.first_selected_word, "XYZ")
        self.assertEqual({candidate.plaintext for candidate in search.candidates},
                         {"DEED CAT", "NOON CAT"})
        impossible = search_word_pattern("AB CD", ["TO"])
        self.assertTrue(impossible.search_complete)
        self.assertFalse(impossible.candidates)
        self.assertGreater(impossible.pruned_values, 0)

    def test_ambiguous_dictionary_solutions_are_returned_without_a_unique_claim(self):
        search = search_word_pattern("AB BA", ["AN", "NA", "AT", "TA"])
        self.assertTrue(search.search_complete)
        self.assertTrue(search.ambiguous)
        self.assertEqual(search.solutions_found, 4)
        self.assertEqual({candidate.plaintext for candidate in search.candidates},
                         {"AN NA", "NA AN", "AT TA", "TA AT"})
        solved = solve_word_pattern("AB BA", ["AN", "NA", "AT", "TA"])
        self.assertEqual(solved.plaintext, "")
        self.assertEqual(solved.key, "")
        self.assertFalse(solved.details["unique_within_lexicon"])
        self.assertTrue(solved.details["ambiguous"])
        self.assertEqual(len(solved.details["candidates"]), 4)

    def test_node_limit_never_claims_uniqueness_for_a_single_found_candidate(self):
        search = search_word_pattern("AB BA", ["AN", "NA", "AT", "TA"], max_nodes=2)
        self.assertFalse(search.search_complete)
        self.assertEqual(search.stop_reason, "node_limit")
        self.assertEqual(search.nodes, 2)
        self.assertEqual(len(search.candidates), 1)
        self.assertIsNone(search.ambiguous)
        self.assertFalse(search.unique_within_lexicon)
        solved = solve_word_pattern("AB BA", ["AN", "NA", "AT", "TA"], max_nodes=2)
        self.assertEqual(solved.plaintext, "")
        self.assertFalse(solved.details["search_complete"])

    def test_candidate_limit_keeps_storage_bounded_and_reports_known_ambiguity(self):
        search = search_word_pattern("AB BA", ["AN", "NA", "AT", "TA"], max_candidates=1)
        self.assertFalse(search.search_complete)
        self.assertEqual(search.stop_reason, "candidate_limit")
        self.assertEqual(len(search.candidates), 1)
        self.assertEqual(search.solutions_found, 2)
        self.assertTrue(search.ambiguous)
        self.assertFalse(search.unique_within_lexicon)

    def test_exact_final_limits_can_still_prove_dictionary_uniqueness(self):
        search = search_word_pattern("AB", ["TO"], max_nodes=1, max_candidates=1)
        self.assertTrue(search.search_complete)
        self.assertTrue(search.unique_within_lexicon)
        self.assertEqual(search.stop_reason, "complete")

    def test_word_pattern_preserves_repeated_letter_positions(self):
        self.assertEqual(word_pattern("noon"), (0, 1, 1, 0))
        self.assertEqual(word_pattern("DEED"), (0, 1, 1, 0))
        self.assertEqual(word_pattern("PEEL"), (0, 1, 1, 2))

    def test_candidates_match_exhaustive_small_alphabet_permutations(self):
        # An independent brute-force key oracle checks pruning and enumeration.
        rng = random.Random(20261003)
        possible_words = ["".join(pair) for pair in itertools.permutations("TONE", 2)]
        for trial in range(12):
            words = set(rng.sample(possible_words, rng.randint(3, len(possible_words))))
            expected = set()
            for values in itertools.permutations("TONE", 3):
                mapping = dict(zip("ABC", values))
                plaintext = "".join(mapping.get(ch, ch) for ch in "AB BA CA")
                if all(word in words for word in plaintext.split()):
                    expected.add(plaintext)
            search = search_word_pattern("AB BA CA", words, max_candidates=30)
            with self.subTest(trial=trial):
                self.assertTrue(search.search_complete)
                self.assertEqual({candidate.plaintext for candidate in search.candidates}, expected)


class WordPatternValidationTest(unittest.TestCase):
    def test_invalid_text_dictionary_and_budgets_are_rejected(self):
        for cipher in ("", "123 !", "caf\u00e9"):
            with self.subTest(cipher=cipher), self.assertRaises(ValueError):
                search_word_pattern(cipher, ["CAT"])
        for words in ([], ["TWO WORDS"], ["caf\u00e9"], ["ABC!"]):
            with self.subTest(words=words), self.assertRaises(ValueError):
                search_word_pattern("ABC", words)
        for words in ("CAT", [None]):
            with self.subTest(words=words), self.assertRaises(TypeError):
                search_word_pattern("ABC", words)
        for name in ("max_nodes", "max_candidates"):
            for value in (0, -1, True, 1.5):
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    search_word_pattern("ABC", ["CAT"], **{name: value})


class WordPatternCertificateTest(unittest.TestCase):
    def test_certificate_recovers_without_expected_key_and_matches_hash(self):
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["ciphertext"], CIPHER)
        self.assertEqual(cert["plaintext"], SUBSTITUTION_PLAIN)
        self.assertEqual(cert["fixture_kind"], "constructed_repository_fixture")
        self.assertEqual(cert["source_url"], SOURCE_URL)
        self.assertEqual(cert["keys"]["expected_decrypt_key"], EXPECTED_DECRYPT_KEY)
        solved = solve_word_pattern(cert["ciphertext"], cert["lexicon"],
                                    max_nodes=cert["limits"]["max_nodes"])
        self.assertTrue(solved.details["search_complete"])
        self.assertTrue(solved.details["unique_within_lexicon"])
        self.assertEqual(solved.plaintext, cert["plaintext"])
        self.assertEqual(solved.key, cert["keys"]["expected_decrypt_key"])
        self.assertEqual(hashlib.sha256(solved.plaintext.encode("utf-8")).hexdigest(),
                         cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
