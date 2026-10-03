"""Exact affine constraint controls with no persona or language ranking."""
from __future__ import annotations

import hashlib
import json
from math import gcd
from pathlib import Path
from random import Random
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.pacifist import investigate_pacifist

ROOT = Path(__file__).resolve().parents[1]
LONG_CIPHER = "DZIUIUDZYHILUDOHHIBYGITZYLSYUUOQYDZODEYEIJJPYGLWTDIDEOUYBGITZYLYPEIDZOAYWKHBIBYHKLDZYSMJDITJIYLOBPHKMLDYYBHKLDZYUZIHDUIBGYIDIUOSKBKOJTZOXYDIGEYGOBODDOGAIDEIDZXOUIGHLYCMYBGWOBOJWUIUXMDEYGOBOJUKMUYDZODOBOJWUIUDKLYGKVYLDZYKLIQIBOJAYWUKDZODEYGOBPYGITZYLDZYSYUUOQY"
LONG_PLAIN = "THISISTHEFIRSTAFFINECIPHERMESSAGETHATWEWILLDECRYPTITWASENCIPHEREDWITHAKEYOFNINEFORTHEMULTIPLIERANDFOURTEENFORTHESHIFTSINCEITISAMONOALPHABETICWECANATTACKITWITHBASICFREQUENCYANALYSISBUTWECANALSOUSETHATANALYSISTORECOVERTHEORIGINALKEYSOTHATWECANDECIPHERTHEMESSAGE"
CRIBS = (Crib(0, "T"), Crib(3, "S"))


class PacifistExactSolverTest(unittest.TestCase):
    def test_published_long_vector_recovers_unknown_key_from_two_letters(self):
        report = investigate_pacifist(LONG_CIPHER, cribs=CRIBS)
        self.assertEqual(report["checks"], 312)
        self.assertTrue(report["search_complete"])
        self.assertEqual(report["compatible_key_count"], 1)
        self.assertTrue(report["unique_key_within_model"])
        self.assertEqual(report["consensus_plaintext"], LONG_PLAIN)
        self.assertEqual(report["known_positions"], 2)
        self.assertEqual(report["candidates"][0]["key"], {"a": 9, "b": 14})
        self.assertEqual(report["candidates"][0]["evidence"]["predicted_letters_beyond_crib"], 257)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["correctness_known"])

    def test_primary_short_published_vector_predicts_ten_noncrib_letters(self):
        report = investigate_pacifist("IHHWVC SWFRCP", cribs=(Crib(0, "AF"),))
        self.assertEqual(report["consensus_plaintext"], "AFFINECIPHER")
        self.assertEqual(report["candidates"][0]["key"], {"a": 5, "b": 8})
        self.assertEqual(report["known_positions"], 2)

    def test_no_crib_exhausts_all_keys_and_abstains_without_scoring(self):
        with patch("engine.language.get_model", side_effect=AssertionError("no language ranking")), \
             patch("engine.solvers.pacifist.pacifist_score", side_effect=AssertionError("no peaceful preference")):
            report = investigate_pacifist(LONG_CIPHER, max_candidates=2)
        self.assertEqual(report["checks"], 312)
        self.assertEqual(report["compatible_key_count"], 312)
        self.assertEqual(len(report["candidates"]), 2)
        self.assertTrue(report["abstained"])
        self.assertFalse(report["unique_key_within_model"])
        self.assertEqual(report["consensus_plaintext"], "?" * len(LONG_CIPHER))
        self.assertTrue(all(c["score"] == 0.0 for c in report["candidates"]))

    def test_partial_budgets_never_emit_forced_consensus_or_unique_key_claim(self):
        for limit in (0, 1, 118, 119, 311):
            report = investigate_pacifist(LONG_CIPHER, cribs=CRIBS, max_checks=limit)
            self.assertEqual(report["checks"], limit)
            self.assertFalse(report["search_complete"])
            self.assertEqual(report["stop_reason"], "check_budget")
            self.assertIsNone(report["compatible_key_count"])
            self.assertIsNone(report["unique_key_within_model"])
            self.assertEqual(report["consensus_plaintext"], "?" * len(LONG_CIPHER))
            self.assertTrue(report["abstained"])
        exact = investigate_pacifist(LONG_CIPHER, cribs=CRIBS, max_checks=312)
        self.assertTrue(exact["search_complete"])

    def test_retention_cap_does_not_omit_keys_from_consensus(self):
        report = investigate_pacifist("IHIH", cribs=(Crib(0, "A"),), max_candidates=1)
        self.assertEqual(report["compatible_key_count"], 12)
        self.assertEqual(report["consensus_plaintext"], "A?A?")
        self.assertFalse(report["unique_key_within_model"])
        self.assertEqual(len(report["candidates"]), 1)
        self.assertTrue(report["search_complete"])

    def test_impossible_model_never_vacuously_proves_plaintext(self):
        report = investigate_pacifist("ABCD", cribs=(Crib(0, "AA"),))
        self.assertEqual(report["compatible_key_count"], 0)
        self.assertEqual(report["candidates"], [])
        self.assertEqual(report["consensus_plaintext"], "????")
        self.assertFalse(report["unique_key_within_model"])
        self.assertTrue(report["abstained"])
        self.assertTrue(report["contradictions"])

    def test_duplicate_cribs_do_not_create_extra_evidence(self):
        once = investigate_pacifist(LONG_CIPHER, cribs=CRIBS)
        twice = investigate_pacifist(LONG_CIPHER, cribs=CRIBS + (Crib(0, "t"),))
        self.assertEqual(once, twice)

    def test_every_retained_witness_passes_independent_forward_formula(self):
        report = investigate_pacifist(LONG_CIPHER, max_candidates=100)
        for candidate in report["candidates"]:
            a, b = candidate["key"]["a"], candidate["key"]["b"]
            forward = "".join(chr(65 + (a * (ord(c) - 65) + b) % 26) for c in candidate["plaintext"])
            self.assertEqual(forward, LONG_CIPHER)
            self.assertTrue(candidate["forward_consistent"])
            self.assertTrue(candidate["crib_match"])

    def test_forward_check_failure_is_not_hidden(self):
        with patch("engine.solvers.pacifist.affine_decrypt", return_value="AAAA"):
            with self.assertRaises(RuntimeError):
                investigate_pacifist("BBBB", max_checks=1)

    def test_independent_random_modular_oracle_counts_and_consensus(self):
        rng = Random(7750)
        units = [i for i in range(26) if gcd(i, 26) == 1]
        for _ in range(30):
            plain = "".join(chr(65 + rng.randrange(26)) for _ in range(40))
            a, b = rng.choice(units), rng.randrange(26)
            cipher = "".join(chr(65 + (a * (ord(c) - 65) + b) % 26) for c in plain)
            offsets = rng.sample(range(len(plain)), rng.randrange(0, 5))
            cribs = tuple(Crib(i, plain[i]) for i in offsets)
            candidates = []
            for multiplier in units:
                inverse = next(v for v in range(26) if multiplier * v % 26 == 1)
                for shift in range(26):
                    candidate = "".join(chr(65 + inverse * (ord(c) - 65 - shift) % 26) for c in cipher)
                    if all(candidate[i] == plain[i] for i in offsets):
                        candidates.append(candidate)
            expected = "".join(chars[0] if all(c == chars[0] for c in chars) else "?" for chars in zip(*candidates))
            report = investigate_pacifist(cipher, cribs=cribs, max_candidates=1)
            self.assertEqual(report["compatible_key_count"], len(candidates))
            self.assertEqual(report["consensus_plaintext"], expected)
            self.assertEqual(report["unique_key_within_model"], len(candidates) == 1)

    def test_invalid_inputs_fail_before_any_search(self):
        for text in ("ABC", "ABCD1", "ABCDα", "A" * 513):
            with self.assertRaises((TypeError, ValueError)):
                investigate_pacifist(text)
        for params in ({"max_checks": True}, {"max_checks": -1}, {"max_checks": 100001}, {"max_candidates": 0}, {"max_candidates": 101}, {"cribs": (Crib(0, "A"), Crib(0, "B"))}):
            with self.assertRaises((TypeError, ValueError)):
                investigate_pacifist("ABCD", **params)

    def test_certificate_hashes_actual_consensus_and_does_not_supply_keys(self):
        certificate = json.loads((ROOT / "engine/data/persona_pacifist_solver_certificate.json").read_text())
        for vector in certificate["vectors"]:
            report = investigate_pacifist(vector["ciphertext"], cribs=tuple(Crib(**c) for c in vector["cribs"]))
            recovered = report["consensus_plaintext"]
            self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(), vector["plaintext_sha256"])
            self.assertEqual(report["compatible_key_count"], 1)
            self.assertEqual(recovered, vector["plaintext"])
            self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
