"""Algebra and recurrence composition with independently constructed controls."""
from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.persona_mechanic import _autokey_trial, investigate_mechanic

PLAIN = "THECLOCKSTRUCKMIDNIGHTANDTHEKEEPEROPENEDTHEGATEFORTHELASTTRAIN"
PROGRESSIVE = "FBWGFATJPCQLYOOWHJJPOMJOJHTCYKPIVUHAULALRXZJBGHAOZZZMLFFEQEFSF"
AUTOKEY = "FBWGFAVRWVCIEUEBUHKQTBDALZOXKRHILVYTICIUHWITEWXMSXTAIQOJMAVLIF"
HILL = "DRPAHAQIGCJIPJWBGHQVDBBIUIPG"
HILL_PLAIN = "HELPTHESMALLBOATSLEFTATDAWNX"
CERT = Path(__file__).resolve().parents[1] / "engine/data/persona_mechanic_solver_certificate.json"


class MechanicSolverTest(unittest.TestCase):
    def test_literal_controls_predict_unprovided_suffix_without_selected_keys(self):
        for cipher, crib, plain, family in (
            (PROGRESSIVE, "THECLOCKSTRU", PLAIN, "progressive-key"),
            (AUTOKEY, "THECLO", PLAIN, "autokey"),
            (HILL, "HELP", HILL_PLAIN, "hill")):
            report = investigate_mechanic(cipher, cribs=(Crib(0, crib),))
            hit = next(c for c in report["candidates"] if c["family"] == family and c["plaintext"] == plain)
            self.assertTrue(hit["forward_consistent"])
            self.assertTrue(hit["crib_match"])
            self.assertFalse(report["correctness_known"])
            self.assertIsNone(report["claimed_plaintext"])
            self.assertEqual(report["checks"], sum(a["checks"] for a in report["actions"]))
            self.assertLessEqual(report["checks"], 5000)
            json.dumps(report, allow_nan=False)

    def test_partial_models_keep_unknown_letters_and_are_not_complete_candidates(self):
        report = investigate_mechanic(AUTOKEY, cribs=(Crib(0, "T"),), max_candidates=100)
        self.assertTrue(report["hypotheses"])
        self.assertTrue(any("?" in h["predicted_plaintext"] for h in report["hypotheses"]))
        self.assertTrue(all("?" not in c["plaintext"] for c in report["candidates"]))
        autokey = report["branch_reports"]["autokey"]
        period6 = next(h for h in autokey["hypotheses"] if h["period"] == 6)
        self.assertIn("?", period6["predicted_plaintext"])
        for position, letter in enumerate(period6["predicted_plaintext"]):
            if position % 6:
                self.assertEqual(letter, "?")
            else:
                self.assertEqual(letter, PLAIN[position])

    def test_autokey_forced_letters_match_exhaustive_primer_oracle(self):
        cipher = "QWER"
        for known in ({1: "L"}, {1: "L", 3: "A"}):
            compatible = []
            for primer in product(range(26), repeat=2):
                plain = []
                for index, letter in enumerate(cipher):
                    shift = primer[index] if index < 2 else plain[index - 2]
                    plain.append((ord(letter) - 65 - shift) % 26)
                text = "".join(chr(65 + value) for value in plain)
                if all(text[index] == letter for index, letter in known.items()):
                    compatible.append(text)
            actual = _autokey_trial(cipher, known, 2)
            if not compatible:
                self.assertIsNone(actual)
            else:
                expected = "".join(compatible[0][i] if all(p[i] == compatible[0][i] for p in compatible)
                                   else "?" for i in range(len(cipher)))
                self.assertEqual(actual["predicted_plaintext"], expected)
                self.assertEqual(actual["compatible_primers"], len(compatible))

    def test_shared_budgets_zero_checks_and_no_evidence(self):
        for budget in (0, 1, 5, 31, 32, 100, 1000):
            report = investigate_mechanic(HILL, cribs=(Crib(0, "HELP"),), max_checks=budget, max_candidates=2)
            self.assertLessEqual(report["checks"], budget)
            self.assertEqual(report["checks"], sum(a["checks"] for a in report["actions"]))
            self.assertLessEqual(len(report["candidates"]), 2)
            if budget == 0:
                self.assertEqual(report["candidates"], [])
                self.assertFalse(report["search_complete"])
        empty = investigate_mechanic(HILL)
        self.assertEqual(empty["checks"], 0)
        self.assertEqual(empty["candidates"], [])
        self.assertFalse(empty["search_complete"])
        self.assertEqual(empty["stop_reason"], "requires_aligned_cribs")

    def test_odd_length_skips_hill_without_adding_padding(self):
        report = investigate_mechanic(AUTOKEY[:-1], cribs=(Crib(0, "THECLO"),))
        self.assertEqual(report["branch_reports"]["hill"]["status"], "not_applicable")
        self.assertTrue(all(len(c["plaintext"]) == len(AUTOKEY) - 1 for c in report["candidates"]))

    def test_standard_library_without_optional_dependencies(self):
        with patch.dict("sys.modules", {"numpy": None, "z3": None}):
            report = investigate_mechanic(AUTOKEY, cribs=(Crib(0, "THECLO"),))
        self.assertTrue(any(c["plaintext"] == PLAIN and c["family"] == "autokey" for c in report["candidates"]))
        self.assertEqual(report["neural_advice"]["status"], "not_used")

    def test_invalid_inputs_and_cribs(self):
        for text in (None, "ABC", "A" * 513, "AB12CD", "α" * 30):
            with self.assertRaises((TypeError, ValueError)):
                investigate_mechanic(text)
        for options in ({"cribs": "HELP"}, {"cribs": (Crib(27, "TOO"),)},
                        {"cribs": (Crib(0, "HELP"), Crib(1, "XX"))},
                        {"max_checks": True}, {"max_checks": -1}, {"max_checks": 100001},
                        {"max_candidates": 0}, {"max_candidates": 101}):
            with self.assertRaises((TypeError, ValueError)):
                investigate_mechanic(HILL, **options)

    def test_certificate_hashes_actual_recovered_plaintexts(self):
        certificate = json.loads(CERT.read_text())
        for vector in certificate["vectors"]:
            report = investigate_mechanic(vector["ciphertext"],
                                         cribs=tuple(Crib(**c) for c in vector["cribs"]))
            recovered = next(c["plaintext"] for c in report["candidates"]
                             if c["plaintext"] == vector["expected_plaintext"] and c["family"] == vector["family"])
            self.assertEqual(sha256(recovered.encode("ascii")).hexdigest(), vector["plaintext_sha256"])
            self.assertFalse(vector["key_supplied_to_solver"])


if __name__ == "__main__":
    unittest.main()
