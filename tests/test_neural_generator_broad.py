"""Broadened generator checks. The shipped weight file must stay unchanged."""

from __future__ import annotations

import hashlib
import random
import unittest
from pathlib import Path

from engine.neural_generator_broad import (
    evaluate_incumbent,
    sample_enigma,
    sample_m209,
    sample_restricted_enigma,
    sample_restricted_m209,
)
from engine.neural_grade import encrypt_family
from engine.solvers.enigma import enigma_decrypt
from engine.solvers.m209 import (
    BOUCHAUDY_LUGS,
    BOUCHAUDY_PINS,
    WHEEL_ALPHABETS,
    WHEEL_SIZES,
    lugs_from_specs,
    m209_decrypt,
)

_OLD_ROTORS = (
    ("I", "II", "III"),
    ("II", "I", "III"),
    ("III", "II", "I"),
    ("I", "III", "II"),
)
_PLAIN = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
_WEIGHTS = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "neural_router_v2_weights.json"
)


class BroadNeuralGeneratorTest(unittest.TestCase):
    def test_broad_enigma_can_draw_outer_rotor_and_nonempty_plugboard(self):
        rng = random.Random(20261004)
        saw_outer = False
        saw_plug = False
        for _ in range(32):
            settings, ciphertext = sample_enigma(rng, _PLAIN)
            self.assertEqual(enigma_decrypt(ciphertext, **settings), _PLAIN)
            rotors = settings["rotors"]
            self.assertEqual(len(set(rotors)), 3)
            for name in rotors:
                self.assertIn(name, {"I", "II", "III", "IV", "V"})
            self.assertIn(settings["reflector"], {"B", "C"})
            self.assertLessEqual(len(settings["plugboard"]), 6)
            if any(name in {"IV", "V"} for name in rotors):
                saw_outer = True
            if settings["plugboard"]:
                saw_plug = True
        self.assertTrue(saw_outer, "32 draws never used rotor IV or V")
        self.assertTrue(saw_plug, "32 draws never used a nonempty plugboard")

    def test_restricted_enigma_matches_old_empty_plugboard_generator(self):
        for seed in (0, 1, 20261004):
            old = random.Random(seed)
            new = random.Random(seed)
            expected = encrypt_family("enigma", _PLAIN, old)
            settings, ciphertext = sample_restricted_enigma(new, _PLAIN)
            self.assertEqual(ciphertext, expected)
            self.assertEqual(settings["plugboard"], [])
            self.assertEqual(settings["reflector"], "B")
            self.assertIn(settings["rotors"], _OLD_ROTORS)
            self.assertEqual(len(settings["rings"]), 3)
            self.assertEqual(len(settings["positions"]), 3)
            self.assertEqual(enigma_decrypt(ciphertext, **settings), _PLAIN)

    def test_restricted_m209_matches_old_fixed_pins_and_lugs(self):
        for seed in (0, 1, 20261004):
            old = random.Random(seed)
            new = random.Random(seed)
            expected = encrypt_family("m209", _PLAIN, old)
            settings, ciphertext = sample_restricted_m209(new, _PLAIN)
            self.assertEqual(ciphertext, expected)
            self.assertEqual(settings["pin_patterns"], BOUCHAUDY_PINS)
            self.assertEqual(settings["lug_specs"], BOUCHAUDY_LUGS)
            self.assertEqual(
                m209_decrypt(ciphertext, **settings),
                _PLAIN,
            )

    def test_broad_m209_roundtrip_and_pins_are_not_bouchaudy(self):
        rng = random.Random(20261004)
        settings, ciphertext = sample_m209(rng, _PLAIN)
        self.assertEqual(m209_decrypt(ciphertext, **settings), _PLAIN)
        pins = settings["pin_patterns"]
        self.assertNotEqual(tuple(pins), tuple(BOUCHAUDY_PINS))
        self.assertEqual(len(pins), len(WHEEL_SIZES))
        for pattern, alphabet, size in zip(pins, WHEEL_ALPHABETS, WHEEL_SIZES):
            self.assertEqual(len(pattern), size)
            self.assertEqual(len(pattern), len(alphabet))
            self.assertTrue(any(mark != "_" for mark in pattern))
            for index, mark in enumerate(pattern):
                self.assertIn(mark, {alphabet[index], "_"})
        lugs = settings["lug_specs"]
        self.assertEqual(len(lugs), 27)
        self.assertNotEqual(tuple(lugs), tuple(BOUCHAUDY_LUGS))
        self.assertTrue(any(spec != "0-0" for spec in lugs))
        lugs_from_specs(lugs)
        external = settings["external_key"]
        self.assertEqual(len(external), 6)
        for letter, alphabet in zip(external, WHEEL_ALPHABETS):
            self.assertIn(letter, alphabet)

    def test_evaluate_incumbent_counts_and_does_not_change_weights(self):
        before = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
        report = evaluate_incumbent("A" * 180, seed=20261004, per_family=1)
        after = hashlib.sha256(_WEIGHTS.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(report["weights_sha256"], before)
        self.assertFalse(report["incumbent_replaced"])
        self.assertEqual(report["seed"], 20261004)
        self.assertEqual(report["per_family"], 1)
        for side in ("restricted", "broad"):
            block = report[side]
            self.assertEqual(block["total"], 2)
            self.assertLessEqual(block["top1_correct"], block["total"])
            self.assertLessEqual(block["top3_correct"], block["total"])
            self.assertGreaterEqual(block["top3_correct"], block["top1_correct"])
            for family in ("enigma", "m209"):
                counts = block["per_family"][family]
                self.assertEqual(counts["total"], 1)
                self.assertLessEqual(counts["top1_correct"], 1)
                self.assertLessEqual(counts["top3_correct"], 1)
        broad = report["broad"]
        self.assertIn("enigma_nonempty_plugboard", broad)
        self.assertIn("enigma_rotor_outside_i_ii_iii", broad)
        self.assertIn("m209_pins_differ_from_bouchaudy", broad)
        self.assertEqual(broad["m209_pins_differ_from_bouchaudy"], 1)


if __name__ == "__main__":
    unittest.main()
