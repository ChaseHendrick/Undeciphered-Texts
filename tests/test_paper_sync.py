"""The companion publisher stages each paper as GENChase does, and refuses the mistakes it should."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("paper_sync", _ROOT / "tools" / "paper_sync.py")
paper_sync = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(paper_sync)

_ABSTRACT = "# T\n\nPreprint, release 0.9.0.\n\n## Abstract\n\nWe show that 5 > 3 & 2 < 4.\n\nA second paragraph.\n\n## Files\n"


def _registry(**fields) -> dict:
    entry = {"id": "t", "title": "T", "status": "ready", "companion": "o/t", "pdf": "papers/t/paper/t.pdf",
             "latex": "papers/t/paper/t.tex", "textLicense": "all-rights-reserved"}
    entry.update(fields)
    return {"author": {"name": "A B", "given-names": "A", "family-names": "B", "affiliation": "Independent Researcher",
                       "email": "ab@real-domain.org", "orcid": "0000-0000-0000-0000"},
            "papers": [entry, {"id": "u", "title": "U", "status": "draft", "companion": "o/u"}]}


class PaperSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.files = {
            "README.md": _ABSTRACT, "RELEASES.md": "# Releases\n\n## 1.0.0 (2026-10-06)\n\nFirst.\n\n## 0.9.0\n\nOld.\n",
            "paper/t.tex": "\\author{A B \\texttt{ab@real-domain.org}}\n", "paper/t.pdf": "%PDF-1.5\n%%EOF\n",
            "code/run.py": "print(1)\n", "notes/QUALITY.md": "private\n",
        }
        for name, text in self.files.items():
            path = self.root / "papers" / "t" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        (self.root / "licenses").mkdir()
        (self.root / "licenses" / "Apache-2.0.txt").write_text("Apache License\n", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def stage(self, reg: dict | None = None) -> tuple[Path, list[str]]:
        out = self.root / "out"
        found = paper_sync.stage(self.root, "t", out, reg=reg or _registry(), year=2026, files=list(self.files))
        return out, found

    def test_a_clean_paper_stages_without_its_notes(self) -> None:
        out, found = self.stage()
        self.assertEqual(found, [])
        staged = sorted(path.relative_to(out).as_posix() for path in out.rglob("*") if path.is_file())
        self.assertEqual(staged, [".zenodo.json", "CITATION.cff", "LICENSE", "README.md", "RELEASES.md",
                                  "code/run.py", "paper/t.pdf", "paper/t.tex"])

    def test_metadata_matches_genchase(self) -> None:
        out, _ = self.stage()
        record = json.loads((out / ".zenodo.json").read_text(encoding="utf-8"))
        self.assertEqual((record["upload_type"], record["publication_type"], record["license"]),
                         ("publication", "preprint", "other-closed"))
        self.assertTrue(record["description"].startswith("<p>We show that 5 &gt; 3 &amp; 2 &lt; 4.</p><p>A second paragraph.</p>"))
        self.assertIn("all rights reserved", record["description"])
        self.assertEqual(record["creators"], [{"name": "B, A", "affiliation": "Independent Researcher",
                                               "orcid": "0000-0000-0000-0000"}])
        self.assertRegex((out / "LICENSE").read_text(encoding="utf-8"), r"^The manuscript in paper/.*All rights reserved\.")
        citation = (out / "CITATION.cff").read_text(encoding="utf-8")
        self.assertIn('repository-code: "https://github.com/o/t"', citation)
        self.assertNotIn("doi:", citation)

    def test_a_verified_archive_updates_the_readme_and_citation(self) -> None:
        self.files["README.md"] = _ABSTRACT.replace(
            "release 0.9.0.", "release 0.9.0, [doi:10.5281/zenodo.111](https://doi.org/10.5281/zenodo.111).")
        (self.root / "papers" / "t" / "README.md").write_text(self.files["README.md"], encoding="utf-8")
        out, found = self.stage(_registry(archiveVersion="1.0.0", codeDoi="10.5281/zenodo.222"))
        self.assertEqual(found, [])
        readme = (out / "README.md").read_text(encoding="utf-8")
        self.assertIn("release 1.0.0, [doi:10.5281/zenodo.222](https://doi.org/10.5281/zenodo.222).", readme)
        self.assertIn('doi: "10.5281/zenodo.222"', (out / "CITATION.cff").read_text(encoding="utf-8"))

    def test_planted_mistakes_are_refused(self) -> None:
        cases = {
            "an email outside the manuscript": ("code/run.py", "# mail ab@real-domain.org\n"),
            "a link out of the paper folder": ("README.md", _ABSTRACT + "[x](../../engine)\n"),
            "TeX left in the abstract": ("README.md", _ABSTRACT.replace("5 > 3", "$5 \\times 3$")),
            "no abstract": ("README.md", "# T\n\n## Files\n"),
        }
        for what, (name, text) in cases.items():
            with self.subTest(what):
                (self.root / "papers" / "t" / name).write_text(text, encoding="utf-8")
                _, found = self.stage()
                self.assertTrue(found, what)
                (self.root / "papers" / "t" / name).write_text(self.files[name], encoding="utf-8")
                shutil.rmtree(self.root / "out")
        with self.assertRaises(paper_sync.Refused):
            self.stage(_registry(archiveVersion="v1.0.0", codeDoi="10.5281/zenodo.222"))
        with self.assertRaises(paper_sync.Refused):
            paper_sync.ready(_registry(), "u")
        self.assertEqual([entry["id"] for entry in paper_sync.ready(_registry())], ["t"])

    def test_release_notes_are_read_by_version(self) -> None:
        self.assertEqual(paper_sync.notes(self.root, "t", "1.0.0"), "First.\n")
        self.assertEqual(paper_sync.notes(self.root, "t", "v0.9.0"), "Old.\n")
        self.assertEqual(paper_sync.notes(self.root, "t", "2.0.0"), "")

    def test_the_quality_record_gates_a_release(self) -> None:
        quality = self.root / "papers" / "t" / "notes" / "QUALITY.md"
        lines = [f"- [x] **U{i}. Item.** Evidence that is long enough to count as evidence here." for i in range(1, 8)]
        quality.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertEqual(paper_sync.quality_open(self.root, "t"), [])
        quality.write_text("\n".join(lines).replace("- [x] **U4", "- [ ] **U4") + "\n", encoding="utf-8")
        self.assertEqual(paper_sync.quality_open(self.root, "t"), ["U4: open"])
        quality.write_text("\n".join(lines[:6]) + "\n- [x] **U7. Item.** ok\n", encoding="utf-8")
        self.assertEqual(paper_sync.quality_open(self.root, "t"), ["U7: checked without evidence"])

    def test_the_registered_papers_stage_and_check_themselves(self) -> None:
        for entry in paper_sync.registry()["papers"]:
            with self.subTest(entry["id"]):
                self.assertEqual(paper_sync.check(_ROOT, entry["id"]), [])


if __name__ == "__main__":
    unittest.main()
