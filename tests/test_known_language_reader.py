"""Gloss one fetched, cited phrase per language the router includes.

Each phrase is downloaded in this test. A hit must carry a citation URL.
Linear A, Indus, Voynich, and rongorongo are refused. Egyptian sign codes
run only when engine.egyptian imports.
"""

from __future__ import annotations

import http.client
import re
import time
import unittest
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

from engine.known_language_reader import (
    NOT_A_DECIPHERMENT,
    UnknownScriptError,
    available_languages,
    egyptian_sign_module,
    gloss_phrase,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "known-language-reader.md"
_SPACE = re.compile(r"\s+")
_TAGS = re.compile(r"<[^>]+>")
_HIERO = re.compile(r"hiero_([A-Za-z]+\d+[A-Za-z]?)\.png")


def _collapse(text: str) -> str:
    return _SPACE.sub(" ", text)


def _fetch(url: str, attempts: int = 3) -> str:
    """Download a cited page. A transfer cut off midway is tried again, at most three times in all."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "undeciphered-texts-known-language-reader/1.0"},
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8")
        except (http.client.IncompleteRead, ConnectionError, urllib.error.URLError):
            if attempt == attempts - 1:
                raise
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def _visible(html: str) -> str:
    return _collapse(_TAGS.sub(" ", html))


# Prose languages. Egyptian is fetched separately because the phrase is
# Gardiner codes taken from the cited page, not a Latin-letter sentence.
CITED = (
    {
        "language": "english",
        "url": "https://www.gutenberg.org/cache/epub/11/pg11.txt",
        "citation": (
            "Lewis Carroll, Alice's Adventures in Wonderland, "
            "Project Gutenberg eBook 11, "
            "https://www.gutenberg.org/cache/epub/11/pg11.txt"
        ),
        "phrase": (
            "Alice was beginning to get very tired of sitting by her sister on the bank"
        ),
        "lemma": "tired",
        "gloss_has": "rest",
    },
    {
        "language": "latin",
        "url": (
            "https://www.perseus.tufts.edu/hopper/text?doc="
            "Perseus:text:1999.02.0002:book=1:chapter=1"
        ),
        "citation": (
            "Caesar, De bello Gallico 1.1, T. Rice Holmes (Oxford, 1914) "
            "on Perseus, "
            "https://www.perseus.tufts.edu/hopper/text?doc="
            "Perseus:text:1999.02.0002:book=1:chapter=1"
        ),
        "phrase": "Gallia est omnis divisa in partes tres",
        "lemma": "gallia",
        "gloss_has": "Gaul",
        "strip_tags": True,
    },
    {
        "language": "german",
        "url": "https://www.gutenberg.org/cache/epub/77905/pg77905.txt",
        "citation": (
            "Jacob and Wilhelm Grimm, Der Froschkönig oder der eiserne Heinrich, "
            "Project Gutenberg eBook 77905, "
            "https://www.gutenberg.org/cache/epub/77905/pg77905.txt"
        ),
        "phrase": (
            "lebte ein König, dessen Töchter waren alle schön, aber die jüngste war so schön"
        ),
        "lemma": "König",
        "gloss_has": "king",
    },
)

AMUN_URL = "https://en.wikipedia.org/wiki/Amun"
AMUN_CODES = ("M17", "Y5", "N35")


class KnownLanguageReaderTest(unittest.TestCase):
    def test_doc_and_module_refuse_undeciphered_scripts(self) -> None:
        doc = DOC.read_text(encoding="utf-8")
        self.assertIn(NOT_A_DECIPHERMENT, doc)
        for name in ("Linear A", "Indus", "Voynich", "rongorongo"):
            self.assertIn(name, doc)
            self.assertIn(name, NOT_A_DECIPHERMENT)
        self.assertIn("does not decipher", doc.casefold())
        self.assertIn("König", doc)
        self.assertNotIn("\ufffd", doc)

    def test_refuses_unknown_scripts_without_a_gloss(self) -> None:
        for name in ("Linear A", "Indus", "Voynich", "rongorongo", "linear-a"):
            with self.assertRaises(UnknownScriptError) as caught:
                gloss_phrase(name, "Gallia est omnis divisa in partes tres")
            message = str(caught.exception)
            self.assertIn("does not decipher", message)
            self.assertIn("rongorongo", message)

    def test_each_included_language_glosses_one_fetched_cited_phrase(self) -> None:
        included = set(available_languages())
        covered = {case["language"] for case in CITED}
        if egyptian_sign_module() is not None:
            covered.add("egyptian")
            self.assertIn("egyptian", included)
        else:
            self.assertNotIn("egyptian", included)
        self.assertTrue(covered <= included)
        self.assertEqual(included - covered, set())
        for case in CITED:
            with self.subTest(language=case["language"]):
                raw = _fetch(case["url"])
                body = _visible(raw) if case.get("strip_tags") else _collapse(raw)
                phrase = case["phrase"]
                self.assertIn(phrase, body)
                report = gloss_phrase(
                    case["language"],
                    phrase,
                    phrase_citation=case["citation"],
                )
                self.assertEqual(report.language, case["language"])
                self.assertEqual(report.phrase_citation, case["citation"])
                self.assertIn("does not decipher", report.disclaimer)
                match = [
                    entry
                    for entry in report.entries
                    if entry.lemma.casefold() == case["lemma"].casefold()
                ]
                self.assertEqual(len(match), 1, report.entries)
                entry = match[0]
                self.assertIn(case["gloss_has"].casefold(), entry.gloss.casefold())
                self.assertTrue(entry.citation)
                self.assertTrue(entry.source_url.startswith("https://"))
                for other in report.entries:
                    self.assertTrue(other.source_url.startswith("https://"))
                    self.assertNotIn("\ufffd", other.lemma)
        if egyptian_sign_module() is not None:
            self._gloss_fetched_amun_signs()
        german = gloss_phrase("german", CITED[2]["phrase"])
        by_lemma = {entry.lemma: entry for entry in german.entries}
        self.assertEqual(by_lemma["König"].token, "König")
        self.assertIn("ö", by_lemma["König"].token)
        self.assertEqual(by_lemma["jung"].token, "jüngste")
        self.assertIn("ü", by_lemma["jung"].token)
        self.assertEqual(by_lemma["schön"].token, "schön")
        self.assertIn("ö", by_lemma["schön"].lemma)

    def _gloss_fetched_amun_signs(self) -> None:
        page = _fetch(AMUN_URL)
        codes = [code.upper() for code in _HIERO.findall(page)]
        found = None
        width = len(AMUN_CODES)
        for index in range(len(codes) - width + 1):
            window = tuple(codes[index : index + width])
            if window == AMUN_CODES:
                found = window
                break
        self.assertEqual(found, AMUN_CODES)
        visible = _visible(page).casefold()
        self.assertIn("jmn", visible)
        phrase = " ".join(AMUN_CODES)
        report = gloss_phrase(
            "egyptian",
            phrase,
            phrase_citation=(
                "Wikipedia, Amun (Egyptian jmn; wikihiero M17 Y5 N35), " + AMUN_URL
            ),
        )
        self.assertEqual(report.language, "egyptian")
        self.assertEqual(report.reading, "jmn")
        self.assertIn(report.reading, visible)
        self.assertEqual(tuple(entry.lemma for entry in report.entries), AMUN_CODES)
        n35 = report.entries[2]
        self.assertIn("water", n35.gloss.casefold())
        self.assertIn("List_of_Egyptian_hieroglyphs", n35.source_url)
        self.assertTrue(n35.source_url.startswith("https://"))



KL_CERT_PATH = ROOT / "engine" / "data" / "known_language_reader_certificate.json"


class KnownLanguageReaderCertificateTest(unittest.TestCase):
    """Certificate checks a cited known-language phrase, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(KL_CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "known-language-reader")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        self.assertEqual(cert["input"], known)
        report = gloss_phrase(
            cert["language"],
            cert["input"],
            phrase_citation=cert["source_url"],
        )
        self.assertEqual(report.language, "latin")
        self.assertTrue(any("Gaul" in (e.gloss or "") for e in report.entries))
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
