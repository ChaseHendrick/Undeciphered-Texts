"""Known-key three-rotor Enigma recovery against a published worked example.

Source (fetched 2026-10-02): https://en.wikipedia.org/wiki/Enigma_rotor_details

This is a known-key historical machine test. It does not claim a break of
an unsolved intercept, and it is not a claim about army message Nr. 86
or Kryptos K4.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.enigma import (
    WIKIPEDIA_CIPHER,
    WIKIPEDIA_PLAIN,
    WIKIPEDIA_PLUGBOARD,
    WIKIPEDIA_POSITIONS,
    WIKIPEDIA_REFLECTOR,
    WIKIPEDIA_RING_B,
    WIKIPEDIA_RING_B_CIPHER,
    WIKIPEDIA_RINGS,
    WIKIPEDIA_ROTORS,
    WIKIPEDIA_ROTOR_DETAILS_URL,
    enigma_decrypt,
    enigma_encrypt,
    solve_enigma,
    windows_after_steps,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "enigma_certificate.json"


class EnigmaScopeTest(unittest.TestCase):
    def test_module_documents_known_key_not_unsolved_intercept_or_nr86_or_k4(self) -> None:
        import engine.solvers.enigma as enigma_mod

        doc = (enigma_mod.__doc__ or "").lower()
        self.assertIn("known-key historical machine", doc)
        self.assertIn("not", doc)
        self.assertIn("unsolved intercept", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("enigma_rotor_details", WIKIPEDIA_ROTOR_DETAILS_URL.lower())


class EnigmaPublishedExampleTest(unittest.TestCase):
    """Wikipedia: rotors I II III, reflector B, rings AAA, start AAA, AAAAA → BDZGO."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = enigma_encrypt(
            WIKIPEDIA_PLAIN,
            rotors=WIKIPEDIA_ROTORS,
            reflector=WIKIPEDIA_REFLECTOR,
            rings=WIKIPEDIA_RINGS,
            positions=WIKIPEDIA_POSITIONS,
            plugboard=WIKIPEDIA_PLUGBOARD,
        )
        self.assertEqual(cipher, WIKIPEDIA_CIPHER)
        self.assertEqual(cipher, "BDZGO")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_enigma(
            WIKIPEDIA_CIPHER,
            rotors=WIKIPEDIA_ROTORS,
            reflector=WIKIPEDIA_REFLECTOR,
            rings=WIKIPEDIA_RINGS,
            positions=WIKIPEDIA_POSITIONS,
            plugboard=WIKIPEDIA_PLUGBOARD,
        )
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAIN)
        self.assertEqual(result.plaintext, "AAAAA")
        self.assertEqual(result.method, "enigma")
        self.assertEqual(result.details["rotors"], ["I", "II", "III"])
        self.assertEqual(result.details["reflector"], "B")
        self.assertEqual(result.details["rings"], "AAA")
        self.assertEqual(result.details["positions"], "AAA")
        self.assertEqual(result.details["plugboard"], [])
        self.assertEqual(result.details["source_url"], WIKIPEDIA_ROTOR_DETAILS_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known-key historical", scope)
        self.assertIn("not a break of an unsolved intercept", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)

    def test_reciprocal_machine_roundtrips_the_published_example(self) -> None:
        again = enigma_decrypt(
            enigma_encrypt(WIKIPEDIA_PLAIN),
            rotors=("i", "ii", "iii"),
            reflector="b",
            rings="aaa",
            positions="aaa",
            plugboard=[],
        )
        self.assertEqual(again, WIKIPEDIA_PLAIN)

    def test_ring_b_example_on_the_same_page(self) -> None:
        # Same rotors, reflector, and start; every ring set to B.
        cipher = enigma_encrypt(WIKIPEDIA_PLAIN, rings=WIKIPEDIA_RING_B)
        self.assertEqual(cipher, WIKIPEDIA_RING_B_CIPHER)
        self.assertEqual(enigma_decrypt(cipher, rings=WIKIPEDIA_RING_B), WIKIPEDIA_PLAIN)

    def test_wikipedia_step_sequence_including_double_step(self) -> None:
        # Normal sequence and double-step sequence, rotors I II III.
        self.assertEqual(windows_after_steps(3, positions="AAU"), ["AAV", "ABW", "ABX"])
        self.assertEqual(
            windows_after_steps(4, positions="ADU"),
            ["ADV", "AEW", "BFX", "BFY"],
        )


class EnigmaCertificateTest(unittest.TestCase):
    """Certificate checks the published Wikipedia example, not an unsolved intercept."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "enigma")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        settings = self.cert["key_settings"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            enigma_decrypt(
                ciphertext,
                rotors=tuple(settings["rotors"]),
                reflector=settings["reflector"],
                rings=settings["rings"],
                positions=settings["positions"],
                plugboard=settings["plugboard"],
            ),
            plaintext,
        )
        result = solve_enigma(
            ciphertext,
            rotors=tuple(settings["rotors"]),
            reflector=settings["reflector"],
            rings=settings["rings"],
            positions=settings["positions"],
            plugboard=settings["plugboard"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], WIKIPEDIA_ROTOR_DETAILS_URL)
        note = self.cert["note"].lower()
        self.assertIn("known-key historical", note)
        self.assertIn("not a break of an unsolved intercept", note)
        self.assertIn("nr. 86", note)
        self.assertIn("k4", note)
        self.assertNotIn("solved nr. 86", note)
        self.assertNotIn("kryptos k4 is", note)


if __name__ == "__main__":
    unittest.main()
