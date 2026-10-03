"""Unknown-key composition controls and bounded persona report semantics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.affine import affine_decrypt
from engine.solvers.persona_hallucinogens import investigate_hallucinogens, choose, covers


PLAIN = "THEHARBORBELLRANGTWICEBEFOREDAWNANDTHESMALLBOATSLEFTTHEQUAYWITHNETSFOLDEDONTHEDECKATHINMISTHIDTHEFARSHOREBUTTHECREWKNEWTHECHANNELBYTHESOUNDOFWATERAGAINSTSTONE"
# Literal ciphertexts constructed by an independent x -> 7*x+3 map, then
# reversal or right rotation by three. The solver receives neither key nor PT.
REVERSED_AFFINE = "FQXGZGZQHDTDSFGDBMXYQNXZFAGPKCFQQDARFAGBFQVBFSRFAGGNKFSXAZSDMFAGYHAGZHJQHAGDVRFYFAGQXYFYCXMZGFQAGHBPDNLFAGGMFCZGDXKCCDJZFAGYQDQBDYFSXMFKFRHBGTQDSCCFKSXKSDAFAG"
ROTATED_AFFINE = "XQFGAFADSKXSKFCCSDQTGBHRFKFMXSFYDBQDQYGAFZJDCCKXDGZCFMGGAFLNDPBHGAQFGZMXCYFYXQGAFYFRVDGAHQJHZGAHYGAFMDSZAXSFKNGGAFRSFBVQFBGAFRADQQFCKPGAFZXNQYXMBDGFSDTDHQZGZG"
UNITS = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)


def _independent_forward(candidate):
    key = candidate["key"]
    affine = key["affine"]
    mapped = "".join(chr(65 + (affine["a"] * (ord(ch) - 65) + affine["b"]) % 26)
                     for ch in candidate["plaintext"])
    transform = key["transform"]
    if transform["kind"] == "reverse":
        return mapped[::-1]
    if transform["kind"] == "rotate_left":
        offset = transform["offset"]
        return mapped[-offset:] + mapped[:-offset]
    return mapped


class HallucinogensSolverTest(unittest.TestCase):
    def test_blind_reversed_affine_recovery_and_uncomposed_control(self):
        report = investigate_hallucinogens(REVERSED_AFFINE, max_rotations=0)
        self.assertEqual(report["candidates"][0]["plaintext"], PLAIN)
        hit = report["candidates"][0]
        self.assertEqual(hit["key"]["transform"], {"kind": "reverse", "offset": 0})
        self.assertEqual(hit["key"]["affine"], {"a": 7, "b": 3})
        self.assertEqual(_independent_forward(hit), REVERSED_AFFINE)
        self.assertTrue(hit["forward_consistent"])
        self.assertTrue(hit["crib_match"])
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["checks"], 2 * 312)
        # Every plain affine key fails to recover this unreversed fixture.
        self.assertFalse(any(affine_decrypt(REVERSED_AFFINE, a, b) == PLAIN
                             for a in UNITS for b in range(26)))
        self.assertFalse(report["correctness_known"])
        self.assertIsNone(report["happiness"])
        self.assertIsNone(report["claimed_plaintext"])
        json.dumps(report)

    def test_rotation_composition_and_original_plaintext_crib_coordinates(self):
        report = investigate_hallucinogens(ROTATED_AFFINE,
            cribs=(Crib(0, "THEHARBOR"), Crib(20, PLAIN[20:30])), max_rotations=3)
        hit = next(c for c in report["candidates"] if c["plaintext"] == PLAIN)
        self.assertEqual(hit["key"]["transform"], {"kind": "rotate_left", "offset": 3})
        self.assertEqual(_independent_forward(hit), ROTATED_AFFINE)
        self.assertEqual(report["known_positions"], 19)
        self.assertTrue(all(c["plaintext"].startswith("THEHARBOR") for c in report["candidates"]))
        no_rotation = investigate_hallucinogens(ROTATED_AFFINE,
            cribs=(Crib(0, "THEHARBOR"),), max_rotations=0)
        self.assertEqual(no_rotation["candidates"], [])
        self.assertTrue(no_rotation["search_complete"])

    def test_budget_is_global_and_transformations_are_interleaved(self):
        for budget in (0, 1, 2, 7, 31, 100):
            report = investigate_hallucinogens(REVERSED_AFFINE, max_checks=budget,
                                               max_candidates=3, max_rotations=3)
            self.assertEqual(report["checks"], budget)
            self.assertFalse(report["search_complete"])
            self.assertEqual(sum(t["checks"] for t in report["transform_checks"]), budget)
            counts = [t["checks"] for t in report["transform_checks"]]
            self.assertLessEqual(max(counts) - min(counts), 1)
            self.assertLessEqual(len(report["candidates"]), 3)
            if budget == 0:
                self.assertEqual(report["candidates"], [])
        complete = investigate_hallucinogens("TEST", max_checks=10000, max_rotations=64)
        self.assertEqual(complete["checks"], 5 * 312)
        self.assertTrue(complete["search_complete"])
        self.assertEqual(complete["bounds"]["effective_rotation_offsets"], [1, 2, 3])

    def test_all_candidates_independently_reencrypt_and_scores_are_sorted(self):
        report = investigate_hallucinogens(REVERSED_AFFINE, max_rotations=2)
        self.assertEqual(len({c["plaintext"] for c in report["candidates"]}), len(report["candidates"]))
        scores = [c["score"] for c in report["candidates"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for candidate in report["candidates"]:
            self.assertEqual(_independent_forward(candidate), REVERSED_AFFINE)
            self.assertEqual(len(candidate["plaintext"]), len(REVERSED_AFFINE))
            self.assertIn("transform", candidate["evidence"])

    def test_duplicate_plaintexts_retain_bounded_equivalent_witnesses(self):
        report = investigate_hallucinogens("AAAA", max_rotations=64, max_candidates=1)
        self.assertGreater(report["duplicate_candidates"], 0)
        self.assertTrue(report["candidates_truncated"])
        witness = report["candidates"][0]
        self.assertEqual(witness["equivalent_compositions_seen"], 60)
        self.assertEqual(len(witness["equivalent_compositions"]), 4)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertFalse(report["unique_plaintext_established"])

    def test_bad_inverse_is_rejected_by_forward_replay(self):
        with patch("engine.solvers.persona_hallucinogens.affine_decrypt", return_value="AAAA"):
            report = investigate_hallucinogens("TEST", max_checks=1, max_rotations=0)
        self.assertEqual(report["candidates"], [])
        self.assertEqual(report["forward_mismatches"], 1)
        self.assertTrue(any(c["kind"] == "forward_mismatch" for c in report["contradictions"]))

    def test_bound_input_and_constraint_validation(self):
        for params in ({"max_rotations": -1}, {"max_rotations": 65}, {"max_rotations": True},
                       {"max_checks": -1}, {"max_checks": True}, {"max_candidates": 0},
                       {"cribs": (Crib(0, "AB"), Crib(1, "C"))}, {"cribs": (Crib(4, "A"),)},
                       {"cribs": iter(())}):
            with self.subTest(params=params), self.assertRaises((ValueError, TypeError)):
                investigate_hallucinogens("TEST", **params)
        for text in (None, "", "ABC", "1234", "ÅBCD", "A" * 513):
            with self.assertRaises((ValueError, TypeError)):
                investigate_hallucinogens(text)

    def test_legacy_word_preferences_are_unchanged(self):
        preferred = "A color from the dream was melting across the page."
        self.assertTrue(covers(preferred))
        self.assertEqual(choose(preferred, "Plain text."), preferred)
        with self.assertRaises(ValueError):
            choose(preferred, preferred)

    def test_certificate_is_actual_blind_recovery(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/persona_hallucinogens_solver_certificate.json").read_text())
        report = investigate_hallucinogens(cert["ciphertext"], **cert["search_limits"])
        hit = report["candidates"][0]
        self.assertEqual(hashlib.sha256(hit["plaintext"].encode()).hexdigest(), cert["plaintext_sha256"])
        self.assertEqual(report["checks"], cert["checks"])
        self.assertEqual(_independent_forward(hit), cert["ciphertext"])
        self.assertNotIn("key", cert["search_limits"])
        self.assertEqual(cert["tool_name"], "persona-hallucinogens")
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
