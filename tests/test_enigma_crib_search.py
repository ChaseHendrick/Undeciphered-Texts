"""Unknown starts with fixed settings, missing slots, and independent controls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from engine.reverse_engineer import Crib
from engine.solvers.enigma_crib_search import search_enigma_starts


# Independent arithmetic oracle: literal rotor tables, no engine machine calls.
_WIRES = {"I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
          "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
          "V": "VZBRGITYUPSDNHLXAWMJQOFECK"}
_NOTCH = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z"}
_REFLECT = {"B": "YRUHQSLDPXNGOKMIEBFZCWVJAT", "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}


def _oracle(plain, positions, *, rotors=("I", "II", "III"), rings="AAA", reflector="B", plugs=()):
    windows = [ord(ch) - 65 for ch in positions]
    offsets = [ord(ch) - 65 for ch in rings]
    patch = {ch: ch for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for a, b in plugs:
        patch[a], patch[b] = b, a
    output = []
    for letter in plain:
        middle_carry = chr(65 + windows[1]) == _NOTCH[rotors[1]]
        right_carry = chr(65 + windows[2]) == _NOTCH[rotors[2]]
        windows = [(windows[0] + middle_carry) % 26,
                   (windows[1] + (middle_carry or right_carry)) % 26, (windows[2] + 1) % 26]
        contact = ord(patch[letter]) - 65
        for rotor in (2, 1, 0):
            shift = windows[rotor] - offsets[rotor]
            contact = (ord(_WIRES[rotors[rotor]][(contact + shift) % 26]) - 65 - shift) % 26
        contact = ord(_REFLECT[reflector][contact]) - 65
        for rotor in (0, 1, 2):
            shift = windows[rotor] - offsets[rotor]
            contact = (_WIRES[rotors[rotor]].index(chr(65 + (contact + shift) % 26)) - shift) % 26
        output.append(patch[chr(65 + contact)])
    return "".join(output)


class EnigmaCribSearchTest(unittest.TestCase):
    def test_existing_published_vector_without_start_input(self):
        report = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),))
        self.assertTrue(report.search_complete)
        self.assertEqual(report.checks, 26**3)
        self.assertEqual(report.checked_starts, report.checks)
        hit = next(candidate for candidate in report.candidates if candidate.positions == "AAA")
        self.assertEqual(hit.plaintext, "AAAAA")
        self.assertTrue(hit.re_encryption_matches)
        self.assertIsNone(report.claimed_plaintext)
        self.assertTrue(report.unique_plaintext_within_settings)
        self.assertEqual(report.unique_start_within_settings, report.accepted_start_count == 1)
        self.assertEqual(report.supplied_settings["rings"], "AAA")
        json.dumps(report.to_dict())

    def test_missing_cipher_slots_advance_and_remain_unknown(self):
        reports = [search_enigma_starts(cipher, cribs=(Crib(0, "AA"), Crib(3, "AA"))) for cipher in ("BD?GO", "BD-GO")]
        for report in reports:
            hit = next(candidate for candidate in report.candidates if candidate.positions == "AAA")
            self.assertEqual(hit.plaintext, "AA?AA")
            self.assertEqual(report.gap_positions, (2,))
            self.assertEqual(report.ciphertext_length, 5)
            self.assertEqual(report.known_positions, 4)
            self.assertTrue(hit.re_encryption_matches)
        self.assertEqual(reports[0].candidates, reports[1].candidates)
        # Removing the gap changes later machine steps and cannot replay this crib.
        removed = search_enigma_starts("BDGO", cribs=(Crib(0, "AAAA"),), max_checks=1)
        self.assertEqual(removed.candidates, ())

    def test_crib_touching_missing_requires_explicit_skip_and_never_fills_it(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            search_enigma_starts("BD?GO", cribs=(Crib(0, "AAAAA"),))
        report = search_enigma_starts("BD?GO", cribs=(Crib(0, "AAAAA"),), skip_missing=True, max_checks=1)
        self.assertEqual(report.candidates[0].plaintext, "AA?AA")
        self.assertEqual(report.skipped_crib_positions, 1)
        self.assertEqual(report.known_positions, 4)
        self.assertFalse(report.unique_start_within_settings)

    def test_independent_oracle_nondefault_settings_and_gap_at_double_step(self):
        self.assertEqual(_oracle("AAAAA", "AAA"), "BDZGO")
        plain = "THEHARBORBELLRANGTWICEBEFOREDAWN"
        settings = {"rotors": ("V", "I", "III"), "rings": "BDF", "reflector": "C", "plugboard": ("AB", "CD", "EH")}
        literal = _oracle(plain, "MCK", rotors=settings["rotors"], rings=settings["rings"],
                          reflector="C", plugs=("AB", "CD", "EH"))
        report = search_enigma_starts(literal[:4] + "-" + literal[5:], cribs=(Crib(0, "THEH"), Crib(5, "RBOR")), **settings)
        hit = next(candidate for candidate in report.candidates if candidate.positions == "MCK")
        self.assertEqual(hit.plaintext, plain[:4] + "?" + plain[5:])
        self.assertTrue(report.search_complete)
        self.assertLessEqual(report.letter_steps, 1000000)
        # III/II/I at ADQ goes AER then BFS. The missing first press must
        # participate in both the right-notch carry and middle double-step.
        cipher = _oracle(plain, "ADQ", rotors=("III", "II", "I"))
        report = search_enigma_starts("?" + cipher[1:], rotors=("III", "II", "I"),
                                     cribs=(Crib(1, "HEHARBOR"),))
        hit = next(candidate for candidate in report.candidates if candidate.positions == "ADQ")
        self.assertEqual(hit.plaintext, "?" + plain[1:])
        self.assertTrue(hit.re_encryption_matches)

    def test_retention_limit_and_incomplete_single_witness_do_not_establish_uniqueness(self):
        incomplete = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),), max_checks=1)
        self.assertEqual(incomplete.accepted_start_count, 1)
        self.assertFalse(incomplete.search_complete)
        self.assertFalse(incomplete.unique_start_within_settings)
        self.assertIsNone(incomplete.start_ambiguity)
        ambiguous = search_enigma_starts("BDZGO", cribs=(Crib(0, "A"),), max_candidates=1)
        self.assertTrue(ambiguous.search_complete)
        self.assertGreater(ambiguous.accepted_start_count, 1)
        self.assertTrue(ambiguous.start_ambiguity)
        self.assertTrue(ambiguous.plaintext_ambiguity)
        self.assertTrue(ambiguous.candidates_truncated)
        self.assertEqual(len(ambiguous.candidates), 1)
        self.assertFalse(ambiguous.unique_start_within_settings)

    def test_start_budget_and_machine_slot_work_budget(self):
        for limit in (0, 1, 10):
            report = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),), max_checks=limit)
            self.assertEqual(report.checks, limit)
            self.assertFalse(report.search_complete)
            self.assertLessEqual(report.letter_steps, 1000000)
        report = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),), max_letter_steps=4)
        self.assertEqual(report.checks, 1)
        self.assertEqual(report.checked_starts, 0)
        self.assertEqual(report.letter_steps, 4)
        self.assertEqual(report.stop_reason, "work_limit")
        self.assertEqual(report.incomplete_start, "AAA")
        self.assertFalse(report.search_complete)
        self.assertEqual(report.candidates, ())
        late = search_enigma_starts("A" * 512, cribs=(Crib(511, "B"),), max_letter_steps=100)
        self.assertEqual(late.letter_steps, 100)
        self.assertEqual(late.checked_starts, 0)
        self.assertFalse(late.search_complete)

    def test_impossible_self_encryption_is_a_scoped_rejection(self):
        report = search_enigma_starts("BDZGO", cribs=(Crib(0, "B"),))
        self.assertEqual(report.checks, 0)
        self.assertEqual(report.accepted_start_count, 0)
        self.assertTrue(report.search_complete)
        self.assertEqual(report.stop_reason, "structural_rejection")
        self.assertEqual(report.contradictions[0]["kind"], "self_encryption")
        self.assertFalse(report.unique_start_within_settings)

    def test_forward_mismatch_is_rejected(self):
        with patch("engine.solvers.enigma_crib_search._process_slots", return_value="AAAAA"):
            report = search_enigma_starts("BDZGO", cribs=(Crib(0, "AAAAA"),), max_checks=1)
        self.assertEqual(report.re_encryption_mismatches, 1)
        self.assertEqual(report.accepted_start_count, 0)
        self.assertEqual(report.candidates, ())

    def test_strict_settings_input_and_crib_validation(self):
        for values in ({"max_checks": -1}, {"max_checks": 17577}, {"max_checks": True},
                       {"max_candidates": 0}, {"max_candidates": 101},
                       {"max_letter_steps": -1}, {"max_letter_steps": 1000001}, {"skip_missing": 1},
                       {"rotors": "III"}, {"rotors": ("I", "I", "III")}, {"rotors": ("I", "II", 3)},
                       {"reflector": "A"}, {"rings": "AA1A"}, {"rings": "ÅAA"},
                       {"plugboard": "AB AC"}, {"plugboard": "A1B"}, {"plugboard": (("A",),)},
                       {"cribs": ()}, {"cribs": iter(())}, {"cribs": ((0, "A"),)},
                       {"cribs": (Crib(True, "A"),)}, {"cribs": (Crib(5, "A"),)},
                       {"cribs": (Crib(0, "A"), Crib(0, "C"))}, {"cribs": (Crib(0, "Å"),)}):
            params = {"cribs": (Crib(0, "AAAAA"),), **values}
            with self.subTest(values=values), self.assertRaises((ValueError, TypeError)):
                search_enigma_starts("BDZGO", **params)
        for text in (None, "", "?--", "BDZGO.", "BD3GO", "BDŽGO", "A" * 513):
            with self.assertRaises((ValueError, TypeError)):
                search_enigma_starts(text, cribs=(Crib(0, "A"),))

    def test_certificate_hashes_actual_unknown_start_recovery(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/enigma_crib_search_certificate.json").read_text())
        report = search_enigma_starts(cert["ciphertext"], cribs=tuple(Crib(**crib) for crib in cert["cribs"]),
                                     **cert["supplied_settings"], **cert["search_limits"])
        self.assertTrue(any(hashlib.sha256(candidate.plaintext.encode("ascii")).hexdigest() == cert["plaintext_sha256"] for candidate in report.candidates))
        self.assertEqual(cert["tool_name"], "enigma-crib-search")
        self.assertNotIn("positions", cert["supplied_settings"])
        self.assertEqual(report.checks, cert["checks"])
        self.assertEqual(report.letter_steps, cert["letter_steps"])
        self.assertEqual(report.accepted_start_count, cert["accepted_start_count"])
        self.assertEqual(report.search_complete, cert["search_complete"])
        self.assertIsNone(report.claimed_plaintext)


if __name__ == "__main__":
    unittest.main()
