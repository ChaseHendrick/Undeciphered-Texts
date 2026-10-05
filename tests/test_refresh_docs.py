"""Generated doc indexes match the notes and the D'Agapeyeff logs."""

from __future__ import annotations

import unittest

from tools.refresh_docs import ROOT, render


class RefreshDocsTest(unittest.TestCase):
    def test_the_committed_indexes_match_the_generator(self) -> None:
        updated = render()
        stale = [
            relative
            for relative, text in updated.items()
            if (ROOT / relative).read_text(encoding="utf-8") != text
        ]
        self.assertEqual(stale, [])

    def test_every_note_is_in_the_case_table(self) -> None:
        table = render()["docs/research-notes/README.md"]
        self.assertIn("dagapeyeff-2026-10-05.md", table)
        self.assertIn("kryptos-k4-2026-10-03.md", table)
        self.assertIn("9 dated primary-source case notes", render()["README.md"])


if __name__ == "__main__":
    unittest.main()
