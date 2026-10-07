"""Every research note has a well-formed status ledger that drives its page, the README and the site feed."""

from __future__ import annotations

import fnmatch
import json
import re
import unittest

from tools.refresh_docs import DOCS, FEED, NOTES, ROOT, _ORDER, ledgers, log_path, render, status_summary, tally

_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})\.md$")


class ResearchStatusTest(unittest.TestCase):
    def test_every_note_has_a_ledger(self) -> None:
        notes = {path.name for path in NOTES.glob("*.md") if path.name != "README.md"}
        self.assertEqual({data["note"] for data in ledgers()}, notes)

    def test_every_ledger_is_well_formed(self) -> None:
        for data in ledgers():
            with self.subTest(case=data["case"]):
                self.assertEqual(data["schema"], "research-status-1")
                self.assertEqual(data["plaintext_recovered_percent"], 0)
                self.assertIn(data["kind"], ("cipher", "script"))
                self.assertIn(data["stage"], ("proposed", "ongoing", "preprint"))
                self.assertTrue(set(data["statuses"]) <= set(_ORDER))
                self.assertTrue(data["caveat"])
                for field in ("tagline", "summary", "what_it_is", "what_we_found", "whats_next", "faq", "background"):
                    self.assertTrue(data["lay"][field], field)
                self.assertTrue(data["researcher"]["summary"])
                priorities = []
                for family in data["families"]:
                    self.assertIn(family["status"], data["statuses"])
                    if family["status"] == "open":
                        self.assertTrue(family["next"])
                        priorities.append(family["priority"])
                    else:
                        self.assertTrue(family["logs"], family["family"])
                    for name in family["logs"]:
                        self.assertTrue((DOCS / log_path(name)).exists(), name)
                self.assertEqual(sorted(priorities), list(range(1, len(priorities) + 1)))
                text = json.dumps(data, ensure_ascii=False)
                self.assertNotIn("—", text)
                self.assertNotIn("–", text)

    def test_no_ledger_is_behind_its_logs(self) -> None:
        for data in ledgers():
            if "log_glob" not in data:
                continue
            with self.subTest(case=data["case"]):
                folder, pattern = data["log_glob"].rsplit("/", 1)
                dated = [path for path in (DOCS / folder).glob("*.md") if fnmatch.fnmatch(path.name, pattern)]
                newest = max(_DATE.findall(path.name)[0] for path in dated)
                self.assertGreaterEqual(data["reviewed_through"], newest)
                cited = {log_path(name) for family in data["families"] for name in family["logs"]}
                uncited = sorted(path.name for path in dated if _DATE.findall(path.name)[0] >= data["cite_every_log_from"]
                                 and f"{folder}/{path.name}" not in cited)
                self.assertEqual(uncited, [], f"cite these in docs/research-notes/{data['_file']}")

    def test_the_status_reaches_every_page_and_the_feed(self) -> None:
        pages = render()
        feed = json.loads(pages[str(FEED.relative_to(ROOT))])
        self.assertEqual(feed["schema"], "research-feed-1")
        by_id = {case["id"]: case for case in feed["cases"]}
        for data in ledgers():
            with self.subTest(case=data["case"]):
                summary = status_summary(data)
                self.assertIn(summary, pages["README.md"])
                self.assertIn(summary, pages[f"docs/research-notes/{data['note']}"])
                case = by_id[data["case"]]
                self.assertEqual(case["summary"], summary)
                self.assertEqual(sum(row["count"] for row in case["statuses"]), sum(tally(data).values()))
                self.assertNotIn("claimed_plaintext", json.dumps(case))


if __name__ == "__main__":
    unittest.main()
