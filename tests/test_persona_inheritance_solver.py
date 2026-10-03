"""Independent literal controls for the bounded clue-driven investigator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from engine.reverse_engineer import Crib
from engine.solvers.persona_inheritance import investigate_inheritance

ROOT = Path(__file__).resolve().parents[1]
PLAIN = "THEHEIRREADTHESEALEDLETTERANDMOVEDTHEGOLDTOTHEESTATEBEFORESUNRISE"
VIGENERE = "XZXHXMVJXAWXLWLETPIVEEMXIJTNWQSNXDMLIYHLWXSLAEXWXSMEUIJGKELYRJBSX"
AUTOKEY = "XZXHXMKYIHHBYVWEDELHDITEIULRWFSMEQWTSBSOWASZVPHLHTAIFWYOKITYSFZWW"
CONDI = "OHGGGBONQCBDHGRRCFKTMKETEQLZEOXNUTDHGFRWMDOOHGNRSAAEAADQAQRDRPOPR"
GUESSES = ("FORTUNE", "CABINET", "ESTATE")


def matching(report, family):
    return [c for c in report["candidates"] if c["family"] == family and c["plaintext"] == PLAIN]


class InheritanceSolverTest(unittest.TestCase):
    def test_keyword_guesses_recover_vigenere_without_selected_key(self):
        result = investigate_inheritance(VIGENERE, keywords=GUESSES, cribs=(Crib(0, "THEHEIR"),))
        self.assertTrue(matching(result, "vigenere"))
        self.assertTrue(result["search_complete"])
        self.assertIsNone(result["claimed_plaintext"])
        self.assertFalse(result["correctness_known"])

    def test_keyword_guesses_recover_plaintext_autokey(self):
        result = investigate_inheritance(AUTOKEY, keywords=GUESSES, cribs=(Crib(0, "THEHEIR"),))
        self.assertTrue(matching(result, "autokey"))
        candidate = matching(result, "autokey")[0]
        self.assertTrue(candidate["forward_consistent"])
        self.assertTrue(candidate["crib_match"])

    def test_condi_keyword_setting_search_uses_all_declared_rotations(self):
        result = investigate_inheritance(CONDI, keywords=GUESSES, cribs=(Crib(0, "THEHEIRREAD"),))
        candidate = matching(result, "condi")[0]
        self.assertEqual(candidate["key"], {"keyword": "CABINET", "alphabet_shift": 7, "initial_offset": 9})
        self.assertEqual(result["checks"], 2066)
        self.assertTrue(result["search_complete"])

    def test_exact_autokey_crib_propagation_needs_no_keyword_list(self):
        result = investigate_inheritance(AUTOKEY, cribs=(Crib(0, "THEHEIR"),))
        candidate = matching(result, "autokey")[0]
        self.assertIn("crib propagation", candidate["evidence"]["method"])
        self.assertEqual(result["checks"], 32)
        self.assertEqual(candidate["evidence"]["predicted_letters_beyond_crib"], len(PLAIN) - 7)

    def test_supplied_lexicon_patterns_recover_a_substitution(self):
        result = investigate_inheritance("GSV SVRI SRW GSV WVVW", lexicon=("THE", "HEIR", "HID", "DEED", "CAT", "ROAD", "BIRD"))
        candidates = [c for c in result["candidates"] if c["plaintext"] == "THEHEIRHIDTHEDEED"]
        self.assertTrue(candidates)
        self.assertEqual(candidates[0]["family"], "substitution")
        self.assertTrue(result["search_complete"])
        key = candidates[0]["key"]["plaintext_to_ciphertext"]
        self.assertEqual("".join(key[ord(c) - 65] for c in candidates[0]["plaintext"]), "GSVSVRISRWGSVWVVW")

    def test_cribs_are_global_hard_constraints_and_duplicates_add_no_evidence(self):
        once = investigate_inheritance(VIGENERE, keywords=GUESSES, cribs=(Crib(0, "THEHEIR"),))
        twice = investigate_inheritance(VIGENERE, keywords=GUESSES, cribs=(Crib(0, "THEHEIR"), Crib(0, "theheir")))
        self.assertEqual(once["candidates"], twice["candidates"])
        with self.assertRaises(ValueError):
            investigate_inheritance(VIGENERE, cribs=(Crib(0, "THE"), Crib(1, "ZZ")))

    def test_strict_shared_budget_and_fair_trial_allocation(self):
        for budget in (0, 1, 2, 5, 7, 21):
            result = investigate_inheritance("GSV SVRI SRW GSV WVVW", keywords=GUESSES,
                lexicon=("THE", "HEIR", "HID", "DEED"), cribs=(Crib(0, "THE"),), max_checks=budget)
            self.assertLessEqual(result["checks"], budget)
            self.assertFalse(result["search_complete"])
            self.assertEqual(result["stop_reason"], "check_budget")
            if budget == 5:
                self.assertEqual({a["branch"] for a in result["actions"] if a["checks"]},
                    {"substitution", "vigenere", "keyword_autokey", "condi", "crib_autokey"})

    def test_no_clues_and_free_autokey_columns_never_pretend_recovery(self):
        empty = investigate_inheritance(AUTOKEY)
        self.assertEqual(empty["checks"], 0)
        self.assertEqual(empty["candidates"], [])
        self.assertFalse(empty["search_complete"])
        self.assertEqual(empty["stop_reason"], "no_clues")
        partial = investigate_inheritance(AUTOKEY, cribs=(Crib(0, "T"),))
        action = next(a for a in partial["actions"] if a["branch"] == "crib_autokey")
        self.assertGreater(action["partial_periods"], 0)
        self.assertFalse(partial["correctness_known"])

    def test_ranked_retention_is_deterministic_without_early_candidate_stop(self):
        one = investigate_inheritance(AUTOKEY, keywords=GUESSES, max_candidates=1)
        many = investigate_inheritance(AUTOKEY, keywords=GUESSES, max_candidates=20)
        self.assertEqual(one["checks"], many["checks"])
        self.assertTrue(one["search_complete"])
        self.assertEqual(one["candidates"], many["candidates"][:1])
        self.assertEqual(one, investigate_inheritance(AUTOKEY, keywords=GUESSES, max_candidates=1))

    def test_invalid_hints_types_unicode_and_limits(self):
        for value in ("ESTATE", ("",), ("café",), ("A B",), (1,), ("A" * 65,), tuple("A" for _ in range(129))):
            with self.assertRaises((TypeError, ValueError)):
                investigate_inheritance(AUTOKEY, keywords=value)
        for value in ("HEIR", ("",), ("HE1R",), ("café",), ("A" * 65,), tuple("A" for _ in range(513))):
            with self.assertRaises((TypeError, ValueError)):
                investigate_inheritance(AUTOKEY, lexicon=value)
        for text in ("ABC", "ABCD1", "ABCDα", "A" * 513):
            with self.assertRaises((TypeError, ValueError)):
                investigate_inheritance(text)
        for params in ({"max_checks": True}, {"max_checks": -1}, {"max_checks": 100001}, {"max_candidates": 0}):
            with self.assertRaises((TypeError, ValueError)):
                investigate_inheritance(AUTOKEY, **params)

    def test_word_pattern_bijection_and_inconsistent_crib_reject(self):
        result = investigate_inheritance("ABBA", lexicon=("DEED",), cribs=(Crib(0, "DA"),))
        self.assertFalse(any(c["family"] == "substitution" for c in result["candidates"]))
        self.assertTrue(result["search_complete"])
        result = investigate_inheritance("ABCD", lexicon=("DEED",))
        self.assertEqual(result["candidates"], [])

    def test_certificate_hashes_are_of_actual_recovered_candidates(self):
        cert = json.loads((ROOT / "engine/data/persona_inheritance_solver_certificate.json").read_text())
        for vector in cert["vectors"]:
            result = investigate_inheritance(vector["ciphertext"], lexicon=vector.get("lexicon"),
                keywords=vector.get("keywords"), cribs=tuple(Crib(**c) for c in vector.get("cribs", ())),
                max_checks=vector["max_checks"])
            candidates = [c for c in result["candidates"] if c["family"] == vector["family"]]
            self.assertTrue(any(hashlib.sha256(c["plaintext"].encode("ascii")).hexdigest() == vector["plaintext_sha256"] for c in candidates))
            self.assertIsNone(result["claimed_plaintext"])
            self.assertFalse(result["correctness_known"])


if __name__ == "__main__":
    unittest.main()
