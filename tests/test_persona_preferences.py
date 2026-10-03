"""Persona solvers prefer one written sentence over a plain alternative.

Each solver is given two candidates and must pick the sentence that matches
its word list. The certificate stores that known sentence and its SHA-256.
These are preferences among candidates, not decipherments of Nr. 86, K4,
or an unknown script.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.persona_court_notice import choose as choose_court
from engine.solvers.persona_court_notice import covers as court_covers
from engine.solvers.persona_hallucinogens import choose as choose_hallucinogens
from engine.solvers.persona_hallucinogens import covers as hallucinogens_covers
from engine.solvers.persona_inheritance import choose as choose_inheritance
from engine.solvers.persona_inheritance import covers as inheritance_covers


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "engine" / "data"

PLAIN = "The clerk filed the receipt and locked the drawer before leaving."

MODULES = (
    ROOT / "engine" / "solvers" / "persona_hallucinogens.py",
    ROOT / "engine" / "solvers" / "persona_inheritance.py",
    ROOT / "engine" / "solvers" / "persona_court_notice.py",
    ROOT / "docs" / "persona-preferences.md",
    DATA / "persona_hallucinogens_certificate.json",
    DATA / "persona_inheritance_certificate.json",
    DATA / "persona_court_notice_certificate.json",
)


def _load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class PersonaScopeTest(unittest.TestCase):
    def test_docs_and_sources_state_preference_not_decipherment(self) -> None:
        import engine.solvers.persona_court_notice as court
        import engine.solvers.persona_hallucinogens as hallucinogens
        import engine.solvers.persona_inheritance as inheritance

        for mod in (hallucinogens, inheritance, court):
            doc = (mod.__doc__ or "").lower()
            self.assertIn("preferences among candidates", doc)
            self.assertIn("not decipherments", doc)
            self.assertIn("nr. 86", doc)
            self.assertIn("k4", doc)
            self.assertIn("unknown script", doc)
            note = mod.DISCLAIMER.lower()
            self.assertIn("preferences among candidates", note)
            self.assertIn("not decipherments", note)
            self.assertIn("nr. 86", note)
            self.assertIn("k4", note)
            self.assertIn("unknown script", note)
        self.assertIn("hallucinogens", (hallucinogens.__doc__ or "").lower())

        page = (ROOT / "docs" / "persona-preferences.md").read_text(encoding="utf-8")
        lowered = page.lower()
        self.assertIn("hallucinogens", lowered)
        self.assertNotIn("hallinogens", lowered)
        self.assertIn("preferences among candidates, not decipherments", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("k4", lowered)
        self.assertIn("unknown script", lowered)

        for path in MODULES:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\u2014", text, path.name)
            self.assertNotIn("\u2013", text, path.name)
            self.assertNotIn("hallinogens", text.lower(), path.name)


class HallucinogensPreferenceTest(unittest.TestCase):
    def test_picks_certificate_sentence_and_sha256(self) -> None:
        cert = _load("persona_hallucinogens_certificate.json")
        chosen = cert["chosen_sentence"]
        self.assertEqual(cert["persona"], "hallucinogens")
        self.assertEqual(cert["word_list"], ["color", "dream", "melting"])
        self.assertTrue(hallucinogens_covers(chosen))
        self.assertFalse(hallucinogens_covers(PLAIN))
        self.assertEqual(choose_hallucinogens(chosen, PLAIN), chosen)
        self.assertEqual(choose_hallucinogens(PLAIN, chosen), chosen)
        self.assertEqual(_sha256(chosen), cert["sentence_sha256"])
        self.assertIn("not a decipherment", cert["note"].lower())
        self.assertIn("nr. 86", cert["note"].lower())
        self.assertIn("k4", cert["note"].lower())
        self.assertIn("unknown script", cert["note"].lower())

        other = "A color from the dream was melting across the page."
        self.assertEqual(choose_hallucinogens(PLAIN, other), other)
        self.assertNotEqual(other, chosen)


class InheritancePreferenceTest(unittest.TestCase):
    def test_picks_certificate_sentence_and_sha256(self) -> None:
        cert = _load("persona_inheritance_certificate.json")
        chosen = cert["chosen_sentence"]
        self.assertEqual(cert["persona"], "inheritance")
        self.assertEqual(cert["word_list"], ["fortune", "heir", "estate"])
        self.assertEqual(cert["reworded_from"], "dying aristocrat")
        self.assertTrue(inheritance_covers(chosen))
        self.assertFalse(inheritance_covers(PLAIN))
        self.assertEqual(choose_inheritance(chosen, PLAIN), chosen)
        self.assertEqual(choose_inheritance(PLAIN, chosen), chosen)
        self.assertEqual(_sha256(chosen), cert["sentence_sha256"])
        self.assertIn("not a decipherment", cert["note"].lower())

        other = "No fortune passed to the heir when the estate was sold."
        self.assertEqual(choose_inheritance(other, PLAIN), other)
        self.assertNotEqual(other, chosen)


class CourtNoticePreferenceTest(unittest.TestCase):
    def test_picks_certificate_sentence_and_sha256(self) -> None:
        cert = _load("persona_court_notice_certificate.json")
        chosen = cert["chosen_sentence"]
        self.assertEqual(cert["persona"], "court notice")
        self.assertEqual(cert["word_list"], ["empire", "decree", "throne"])
        self.assertEqual(cert["reworded_from"], "world emperor")
        self.assertTrue(court_covers(chosen))
        self.assertFalse(court_covers(PLAIN))
        self.assertEqual(choose_court(chosen, PLAIN), chosen)
        self.assertEqual(choose_court(PLAIN, chosen), chosen)
        self.assertEqual(_sha256(chosen), cert["sentence_sha256"])
        self.assertIn("not a decipherment", cert["note"].lower())

        other = "One decree set the throne at the center of the empire."
        self.assertEqual(choose_court(PLAIN, other), other)
        self.assertNotEqual(other, chosen)


if __name__ == "__main__":
    unittest.main()
