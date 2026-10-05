"""Generated doc indexes match the notes and the D'Agapeyeff logs."""

from __future__ import annotations

import re
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

    def test_the_log_index_is_oldest_date_first(self) -> None:
        note = render()["docs/research-notes/dagapeyeff-2026-10-05.md"]
        block = note.split("<!-- generated-logs:start -->", 1)[1].split("<!-- generated-logs:end -->", 1)[0]
        dates = re.findall(r"\.\./logs/dagapeyeff[^)]*?(\d{4}-\d{2}-\d{2})\.md", block)
        self.assertEqual(dates, sorted(dates))
        self.assertGreater(len(dates), 1)
        self.assertEqual(dates[0], "2026-10-02")
        self.assertEqual(dates[-1], "2026-10-05")


if __name__ == "__main__":
    unittest.main()
