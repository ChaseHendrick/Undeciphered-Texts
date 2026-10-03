"""Unknown digit maps with independent known answers and completion bounds."""

import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.solvers.morse_constraints import MorseCrib, search_morse_constraints, solve_morse_constraints

MORBIT_CIPHER = "27435 88151 28274 65679 378."
POLLUX_CIPHER = "08639 34257 02417 68596 30414 56234 90874 5360."
CERT = Path(__file__).parents[1] / "engine/data/morse_constraints_certificate.json"


class MorseConstraintsTest(unittest.TestCase):
    def test_unknown_morbit_map_recovers_the_independent_published_vector(self):
        result = search_morse_constraints(MORBIT_CIPHER, families=("morbit",), lexicon=("ONCE", "UPON", "A", "TIME"),
                                          max_maps=400000, timeout_seconds=60, terminal_period=True)
        self.assertTrue(result.search_complete)
        self.assertEqual(result.maps_examined, 362880)
        self.assertIn("ONCE UPON A TIME", [candidate.plaintext for candidate in result.candidates])
        self.assertIn("958427136", [candidate.key for candidate in result.candidates])
        certificate = json.loads(CERT.read_text())
        recovered = next(candidate.plaintext for candidate in result.candidates if candidate.plaintext == certificate["expected_plaintext"])
        self.assertEqual(certificate["expected_plaintext_sha256"], hashlib.sha256(recovered.encode("ascii")).hexdigest())
        self.assertNotIn("cipher_name", certificate)

    def test_unknown_pollux_map_uses_aligned_decoded_text_without_key_input(self):
        result = search_morse_constraints(POLLUX_CIPHER, families=("pollux",), cribs=(MorseCrib(0, "LUCK HELPS"),),
                                          max_maps=60000, timeout_seconds=60, terminal_period=True)
        self.assertTrue(result.search_complete)
        self.assertEqual(result.maps_examined, 59049)
        self.assertTrue(result.unique_plaintext_within_models)
        self.assertTrue(all(candidate.plaintext == "LUCK HELPS" for candidate in result.candidates))
        self.assertIn(".x-..x.--x", [candidate.key for candidate in result.candidates])

    def test_unobserved_digit_maps_do_not_prevent_conditional_plaintext_uniqueness(self):
        result = search_morse_constraints("0", families=("pollux",), lexicon=("E",), max_maps=60000, timeout_seconds=60)
        self.assertEqual(result.accepted_map_count, 18660)  # 3**9 - 2*2**9 + 1
        self.assertTrue(result.unique_plaintext_within_models)
        self.assertFalse(result.unique_map_within_models)
        self.assertTrue(result.map_ambiguity)
        self.assertFalse(result.plaintext_ambiguity)
        self.assertTrue(result.candidates_truncated)
        solved = solve_morse_constraints("0", families=("pollux",), lexicon=("E",), max_maps=60000, timeout_seconds=60)
        self.assertEqual(solved.plaintext, "E")
        self.assertEqual(solved.details["certainty_scope"], "completed supplied models and evidence only")

    def test_storage_limit_retains_bounded_examples_without_hiding_ambiguity(self):
        result = search_morse_constraints("0", families=("pollux",), lexicon=("E", "T"), max_maps=60000,
                                          max_candidates=1, timeout_seconds=60)
        self.assertTrue(result.search_complete)
        self.assertEqual(len(result.candidates), 1)
        self.assertTrue(result.plaintext_ambiguity)
        self.assertFalse(result.unique_plaintext_within_models)
        self.assertEqual(result.accepted_map_count, 37320)

    def test_one_found_candidate_at_map_limit_is_not_unique(self):
        result = search_morse_constraints("0", families=("pollux",), lexicon=("E",), max_maps=6)
        self.assertEqual(result.maps_examined, 6)
        self.assertEqual(result.accepted_map_count, 1)
        self.assertFalse(result.search_complete)
        self.assertFalse(result.unique_plaintext_within_models)
        self.assertIsNone(result.plaintext_ambiguity)
        self.assertIsNone(result.map_ambiguity)
        self.assertEqual(result.stop_reason, "map_limit")
        solved = solve_morse_constraints("0", families=("pollux",), lexicon=("E",), max_maps=6)
        self.assertEqual(solved.plaintext, "")

    def test_families_receive_round_robin_budget_and_known_bounds(self):
        result = search_morse_constraints("1", lexicon=("E", "I", "T"), max_maps=4)
        self.assertEqual([family.maps_examined for family in result.families], [2, 2])
        self.assertEqual([family.map_space for family in result.families], [362880, 59049])
        self.assertFalse(result.search_complete)
        zero = search_morse_constraints("0", families=("pollux",), lexicon=("E",), max_maps=0)
        self.assertEqual(zero.maps_examined, 0)
        self.assertEqual(zero.stop_reason, "map_limit")

    def test_exhaustive_contradictory_evidence_proves_no_candidate_within_model(self):
        result = search_morse_constraints("0", families=("pollux",), lexicon=("E",), cribs=(MorseCrib(0, "T"),),
                                          max_maps=59049, timeout_seconds=60)
        self.assertTrue(result.search_complete)  # Exact final budget still completes.
        self.assertEqual(result.accepted_map_count, 0)
        self.assertFalse(result.unique_plaintext_within_models)
        self.assertEqual(result.stop_reason, "complete")

    def test_global_deadline_is_explicit_incomplete_not_a_negative_proof(self):
        with patch("engine.solvers.morse_constraints._monotonic", side_effect=(0.0, 2.0, 2.0)):
            result = search_morse_constraints("0", families=("pollux",), lexicon=("E",), timeout_seconds=1)
        self.assertFalse(result.search_complete)
        self.assertEqual(result.maps_examined, 0)
        self.assertEqual(result.stop_reason, "time_limit")
        self.assertIsNone(result.plaintext_ambiguity)

    def test_input_and_evidence_bounds_fail_without_unbounded_search(self):
        for kwargs in ({}, {"lexicon": ()}, {"lexicon": "E"}, {"lexicon": ("\u00e9",)},
                       {"lexicon": ("E",), "families": ("unknown",)}, {"lexicon": ("E",), "families": "pollux"},
                       {"lexicon": ("E",), "max_maps": -1}, {"lexicon": ("E",), "max_maps": 500001},
                       {"lexicon": ("E",), "max_candidates": 0}, {"lexicon": ("E",), "max_maps": True},
                       {"lexicon": ("E",), "timeout_seconds": float("nan")}, {"lexicon": ("E",), "timeout_seconds": 61}):
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                search_morse_constraints("0", **kwargs)
        with self.assertRaises(ValueError):
            search_morse_constraints("0" * 513, families=("pollux",), lexicon=("E",))
        with self.assertRaises(ValueError):
            search_morse_constraints("0", families=("morbit",), lexicon=("E",))
        for cribs in ((MorseCrib(True, "E"),), (MorseCrib(0, "\u017f"),), (MorseCrib(0, "E"), MorseCrib(0, "T"))):
            with self.assertRaises((TypeError, ValueError)):
                search_morse_constraints("0", families=("pollux",), cribs=cribs)


if __name__ == "__main__":
    unittest.main()
