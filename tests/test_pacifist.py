"""Pacifist preference among Caesar candidate plaintexts.

Given a peaceful sentence and a violent sentence as candidates for one
known Caesar ciphertext, the solver must pick the peaceful plaintext.
That plaintext must match the certificate SHA-256.

This is a preference among candidates, not a decipherment of army
message Nr. 86, Kryptos K4, or an unknown script.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.pacifist import (
    CAESAR_SHIFT,
    CANDIDATE_PLAINTEXTS,
    METHOD_NAME,
    PEACE_WORDS,
    PEACEFUL_PLAINTEXT,
    VIOLENCE_WORDS,
    VIOLENT_PLAINTEXT,
    caesar_encrypt,
    choose_pacifist,
    known_caesar_ciphertext,
    pacifist_score,
    solve_pacifist,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "pacifist_certificate.json"
)


class PacifistScopeTest(unittest.TestCase):
    def test_module_documents_preference_not_decipherment(self) -> None:
        import engine.solvers.pacifist as pacifist_mod

        doc = pacifist_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("preference among", lowered)
        self.assertIn("candidates", lowered)
        self.assertIn("not a decipherment", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("k4", lowered)
        self.assertIn("unknown script", lowered)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class PacifistWordListTest(unittest.TestCase):
    def test_word_lists_contain_required_terms(self) -> None:
        self.assertEqual(PEACE_WORDS, frozenset({"peace", "calm", "garden"}))
        self.assertEqual(VIOLENCE_WORDS, frozenset({"attack", "war", "kill"}))

    def test_peaceful_scores_higher_than_violent(self) -> None:
        self.assertGreater(
            pacifist_score(PEACEFUL_PLAINTEXT),
            pacifist_score(VIOLENT_PLAINTEXT),
        )
        self.assertGreater(pacifist_score(PEACEFUL_PLAINTEXT), 0)
        self.assertLess(pacifist_score(VIOLENT_PLAINTEXT), 0)


class PacifistChoiceTest(unittest.TestCase):
    def test_selects_peaceful_plaintext(self) -> None:
        chosen = choose_pacifist(CANDIDATE_PLAINTEXTS)
        self.assertEqual(chosen, PEACEFUL_PLAINTEXT)
        self.assertEqual(
            chosen,
            "The calm garden keeps peace under soft light.",
        )

    def test_solver_returns_peaceful_plaintext(self) -> None:
        cipher = known_caesar_ciphertext()
        result = solve_pacifist(CANDIDATE_PLAINTEXTS, ciphertext=cipher)
        self.assertEqual(result.method, METHOD_NAME)
        self.assertEqual(result.plaintext, PEACEFUL_PLAINTEXT)
        self.assertEqual(result.details["mode"], "preference_among_candidates")
        scope = result.details["scope"].lower()
        self.assertIn("preference among candidate", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("k4", scope)
        self.assertIn("unknown script", scope)
        self.assertNotIn("\u2014", result.details["scope"])
        self.assertNotIn("\u2013", result.details["scope"])

    def test_peaceful_plaintext_matches_known_caesar_ciphertext(self) -> None:
        cipher = known_caesar_ciphertext()
        self.assertEqual(cipher, caesar_encrypt(PEACEFUL_PLAINTEXT, CAESAR_SHIFT))
        self.assertEqual(cipher, "Aol jhst nhyklu rllwz wlhjl bukly zvma spnoa.")

    def test_empty_candidates_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            choose_pacifist([])
        with self.assertRaises(ValueError):
            choose_pacifist(["  ", ""])


class PacifistCertificateTest(unittest.TestCase):
    """Certificate checks the chosen peaceful plaintext SHA-256."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_selects_peaceful_plaintext_matching_hash(self) -> None:
        self.assertEqual(self.cert["method"], METHOD_NAME)
        self.assertEqual(self.cert["cipher_name"], "caesar")
        plaintext = self.cert["plaintext"]
        self.assertEqual(plaintext, PEACEFUL_PLAINTEXT)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            digest,
            "b06bcda857f543144a9f463bfe9c1b8d7aed2c5a87482880663633487cfe3b82",
        )
        chosen = choose_pacifist(self.cert["candidates"])
        self.assertEqual(chosen, plaintext)
        self.assertEqual(chosen, self.cert["chosen"])
        result = solve_pacifist(
            self.cert["candidates"],
            ciphertext=self.cert["ciphertext"],
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(
            caesar_encrypt(plaintext, self.cert["keys"]["shift"]),
            self.cert["ciphertext"],
        )
        note = self.cert["note"].lower()
        self.assertIn("preference among candidate", note)
        self.assertIn("nr. 86", note)
        self.assertIn("k4", note)
        self.assertIn("unknown script", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)


if __name__ == "__main__":
    unittest.main()
