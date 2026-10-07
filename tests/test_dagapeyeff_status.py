"""The D'Agapeyeff status ledger is well formed, cites real logs, and cannot fall behind the logs."""

from __future__ import annotations

import re
import unittest

from tools.refresh_docs import ROOT, STATUS, ledger, render, status_summary, tally

_STATUSES = {"closed-with-power", "excluded-by-count", "tested-without-power", "open"}

_LOGS = ROOT / "docs" / "logs"


def _date(name: str) -> str:
    found = re.findall(r"(\d{4}-\d{2}-\d{2})\.md$", name)
    return found[0] if found else ""


class DagapeyeffStatusTest(unittest.TestCase):
    def test_every_family_is_well_formed_and_cites_a_real_log(self) -> None:
        data = ledger()
        self.assertEqual(data["schema"], "research-status-1")
        self.assertEqual(data["case"], "dagapeyeff")
        self.assertEqual(data["plaintext_recovered_percent"], 0)
        self.assertEqual(set(data["statuses"]), _STATUSES)
        priorities = []
        for family in data["families"]:
            self.assertIn(family["status"], _STATUSES)
            self.assertTrue(family["logs"])
            for name in family["logs"]:
                self.assertTrue((_LOGS / name).exists(), name)
            if family["status"] == "open":
                self.assertTrue(family["next"])
                priorities.append(family["priority"])
            text = " ".join(str(value) for value in family.values())
            self.assertNotIn("—", text)
            self.assertNotIn("–", text)
        self.assertEqual(sorted(priorities), list(range(1, len(priorities) + 1)))

    def test_the_ledger_is_not_behind_the_logs(self) -> None:
        data = ledger()
        dated = [path.name for path in _LOGS.glob("dagapeyeff*-????-??-??.md")]
        self.assertGreaterEqual(data["reviewed_through"], max(_date(name) for name in dated))
        cited = {name for family in data["families"] for name in family["logs"]}
        uncited = sorted(name for name in dated if _date(name) >= data["cite_every_log_from"] and name not in cited)
        self.assertEqual(uncited, [], "add these logs to docs/research-notes/dagapeyeff-status.json")

    def test_the_status_is_generated_into_the_page_and_the_readme(self) -> None:
        data = ledger()
        summary = status_summary(data)
        self.assertTrue(summary.startswith("Unsolved. Plaintext recovered: 0 percent."))
        self.assertEqual(sum(tally(data).values()), len(data["families"]))
        pages = render()
        self.assertIn(summary, pages["README.md"])
        note = pages["docs/research-notes/dagapeyeff-2026-10-05.md"]
        self.assertIn(summary, note)
        self.assertIn("<!-- generated-next:start -->", note)
        self.assertNotIn("Proposed next comparison", note)
        self.assertTrue(STATUS.exists())


if __name__ == "__main__":
    unittest.main()
