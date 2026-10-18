"""K4 running keys from other texts: exact scan, English-key check, no claim.

No network: fixtures are texts already in the repo.
"""

from __future__ import annotations

import random
import tempfile
import unittest

from engine.k4_running_key_texts import (
    FROZEN_SOURCES,
    decrypt,
    encrypt,
    english_fragment_check,
    english_fragment_control,
    english_null,
    fragment_score,
    key_fragments,
    key_letter,
    keyed_alphabet,
    load_sources,
    normalize_letters,
    repo_sources,
    required_key,
    scan_text,
    search_k4_running_key_texts,
    tableaux,
    threshold_from,
)
from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.solvers.k4_attempt import K4_CIPHERTEXT


def _german_plain() -> str:
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "engine" / "data" / "neural_heldout_grimm_wolf.txt"
    raw = path.read_text(encoding="utf-8")
    return normalize_letters("\n".join(l for l in raw.splitlines() if not l.startswith("#")))


def _plant(rule: str, alphabet: str, key_text: str, offset: int, plain: str):
    key = key_text[offset : offset + 97]
    cipher = encrypt(rule, alphabet, plain[:97], key)
    spans = tuple((start, plain[start : start + len(word)]) for start, word in CRIB_SPANS)
    return cipher, required_key(rule, alphabet, cipher, spans)


class TableauTest(unittest.TestCase):
    def test_keyed_alphabets(self) -> None:
        self.assertEqual(keyed_alphabet("KRYPTOS"), "KRYPTOSABCDEFGHIJLMNQUVWXZ")
        self.assertEqual(keyed_alphabet("PALIMPSEST"), "PALIMSETBCDFGHJKNOQRUVWXYZ")
        self.assertEqual(keyed_alphabet("ABSCISSA"), "ABSCIDEFGHJKLMNOPQRTUVWXYZ")
        self.assertEqual(len(tableaux()), 12)

    def test_published_k1_k2_vectors_under_keyed_vigenere(self) -> None:
        # Supplied-key check against the published K1 and K2 certificates.
        import json
        from pathlib import Path

        data = Path(__file__).resolve().parent.parent / "engine" / "data"
        alpha = keyed_alphabet("KRYPTOS")
        for name, key in (("k1", "PALIMPSEST"), ("k2", "ABSCISSA")):
            cert = json.loads((data / f"kryptos_{name}_certificate.json").read_text())
            plain = normalize_letters(cert["plaintext"])
            cipher = normalize_letters(cert["ciphertext"])
            running = (key * (len(plain) // len(key) + 1))[: len(plain)]
            self.assertEqual(encrypt("vigenere", alpha, plain, running), cipher)
            self.assertEqual(decrypt("vigenere", alpha, cipher, running), plain)

    def test_key_letter_inverts_every_tableau(self) -> None:
        rng = random.Random(7)
        for _, rule, alpha in tableaux():
            for _ in range(200):
                p, k = rng.choice(alpha), rng.choice(alpha)
                c = encrypt(rule, alpha, p, k)
                self.assertEqual(key_letter(rule, alpha, c, p), k)
                self.assertEqual(decrypt(rule, alpha, c, k), p)

    def test_k4_required_key_places_the_clues(self) -> None:
        for _, rule, alpha in tableaux():
            req = required_key(rule, alpha)
            self.assertEqual(len(req), 24)
            for start, word in CRIB_SPANS:
                for j, ch in enumerate(word):
                    k = dict(req)[start + j]
                    self.assertEqual(decrypt(rule, alpha, K4_CIPHERTEXT[start + j], k), ch)


class ExactScanTest(unittest.TestCase):
    def test_planted_key_in_doyle_is_found_at_its_offset(self) -> None:
        doyle = repo_sources()["neural_heldout_doyle"]
        plain = _german_plain()  # the scan is language-agnostic
        self.assertGreater(len(doyle), 5000)
        for name, rule, alpha in tableaux():
            cipher, req = _plant(rule, alpha, doyle, 2345, plain)
            res = scan_text(doyle, req)
            self.assertIn({"direction": "forward", "offset": 2345}, res["full_matches"], name)
            self.assertEqual(res["best_partial"], 24)
            self.assertLess(res["shuffle_best"], 24)
            self.assertLess(res["chance"]["expected_max"], 12)

    def test_planted_key_read_backwards_is_found(self) -> None:
        doyle = repo_sources()["neural_heldout_doyle"]
        plain = _german_plain()
        _, rule, alpha = tableaux()[5]
        _, req = _plant(rule, alpha, doyle[::-1], 1000, plain)
        res = scan_text(doyle, req)
        self.assertIn({"direction": "backward", "offset": 1000}, res["full_matches"])

    def test_planted_key_in_k3_plaintext_is_found(self) -> None:
        k3 = repo_sources()["kryptos_k3_plaintext"]
        plain = _german_plain()
        _, rule, alpha = tableaux()[1]
        _, req = _plant(rule, alpha, k3, 100, plain)
        res = scan_text(k3, req, backwards=False)
        self.assertEqual(res["full_matches"], [{"direction": "forward", "offset": 100}])


class EnglishFragmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.null = english_null()
        cls.threshold = threshold_from(cls.null)

    def test_planted_english_key_scores_at_english_levels(self) -> None:
        doyle = repo_sources()["neural_heldout_doyle"]
        plain = _german_plain()
        ctl = english_fragment_control(doyle, plain, self.threshold, stride=25)
        for row in ctl["rows"]:
            self.assertTrue(row["roundtrip_ok"])
            self.assertGreater(row["trials"], 200)
            # Held-out English: a few percent fall under the 1st percentile
            # of the in-sample null. Well under 10 percent here.
            self.assertLess(row["below_rate"], 0.10)

    def test_random_keys_mostly_fall_below_threshold(self) -> None:
        rng = random.Random(3)
        below = 0
        for _ in range(300):
            frags = tuple("".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n)) for n in (13, 11))
            below += fragment_score(frags) < self.threshold
        self.assertGreater(below, 280)

    def test_k4_check_reports_statistical_exclusion_only(self) -> None:
        check = english_fragment_check(self.threshold)
        self.assertEqual(len(check["rows"]), 12)
        self.assertIn("not an exact exclusion", check["note"])
        vig = check["rows"][0]
        self.assertEqual(vig["tableau"], "vigenere/AZ")
        self.assertEqual(vig["fragments"], key_fragments(required_key("vigenere", keyed_alphabet("AZ"))))


class K4ReportTest(unittest.TestCase):
    def test_report_claims_nothing_and_repo_hashes_hold(self) -> None:
        names = (
            "kryptos_k1_plaintext",
            "kryptos_k2_plaintext",
            "kryptos_k3_plaintext",
            "kryptos_k1k2k3_plaintext",
            "neural_heldout_doyle",
            "king_james_bible",
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = search_k4_running_key_texts(tmp, names=names, with_fragment_check=False)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        rows = {row["name"]: row for row in report["scan"]}
        self.assertEqual(rows["king_james_bible"]["status"], "missing")
        self.assertIn("skipped", rows["kryptos_k1_plaintext"])
        for item in report["unverified"]:
            self.assertEqual(item["status"], "unverified")
        for name in names[1:5]:
            self.assertEqual(rows[name]["status"], "repo")
            for t in rows[name]["tableaux"]:
                self.assertEqual(t["full_matches"], [])

    def test_frozen_repo_entries_match(self) -> None:
        frozen = {e["name"]: e for e in FROZEN_SOURCES}
        for row in load_sources("/nonexistent-work-dir"):
            if row["origin"] == "repo":
                self.assertEqual(row["letters_sha256_seen"], frozen[row["name"]]["letters_sha256"])
                self.assertEqual(row["letters_seen"], frozen[row["name"]]["letters"])


class DocTest(unittest.TestCase):
    def test_log_states_the_negative_and_the_frozen_hashes(self) -> None:
        from pathlib import Path

        doc = Path(__file__).resolve().parent.parent / "docs" / "k4-focus" / "running-key-texts-2026-10-18.md"
        text = doc.read_text(encoding="utf-8")
        self.assertNotIn("—", text)
        self.assertNotIn("–", text)
        self.assertIn("Not solved. No plaintext claimed.", text)
        self.assertIn("statistical exclusion, not an exact one", text)
        for entry in FROZEN_SOURCES:
            self.assertIn(entry["letters_sha256"], text)
            self.assertIn(entry["url"], text)


if __name__ == "__main__":
    unittest.main()
