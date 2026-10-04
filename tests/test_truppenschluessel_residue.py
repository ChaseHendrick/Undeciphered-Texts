"""Residue ledger: count the public Truppenschlüssel page, do not attack it."""

from __future__ import annotations

import unittest

from engine.truppenschluessel_residue import load_residue, summarize, unmarked


class TruppenschluesselResidueTest(unittest.TestCase):
    def test_page_count_separates_later_breaks(self) -> None:
        payload = load_residue()
        self.assertEqual(payload["page_updated"], "2026-07-27")
        self.assertEqual(payload["checked"], "2026-10-04")
        self.assertEqual(payload["page_meta_count"], 41)
        stats = summarize(payload)
        self.assertEqual(stats["listed"], 41)
        self.assertEqual(stats["broken"], 11)
        self.assertEqual(stats["unmarked"], 30)
        self.assertEqual(stats["broken_dates"], {"2022-01-22": 10, "2022-01-26": 1})

    def test_ledger_has_no_message_text(self) -> None:
        payload = load_residue()
        self.assertNotIn("ciphertext", payload)
        self.assertNotIn("plaintext", payload)
        for row in payload["messages"]:
            self.assertNotIn("ciphertext", row)
            self.assertNotIn("plaintext", row)
            self.assertEqual(len(row["designator"]), 5)

    def test_live_relations_and_short_message_are_explicit(self) -> None:
        payload = load_residue()
        live = unmarked(payload)
        by_indicator = {}
        for row in live:
            by_indicator.setdefault(row["designator"], []).append(row)
        self.assertEqual(len(by_indicator["IASRZ"]), 2)
        self.assertEqual(
            [row["form_length"] for row in by_indicator["IASRZ"]],
            [90, 52],
        )
        stats = summarize(payload)
        self.assertEqual(stats["relation_counts"]["same_reception_minute:1941-07-04T1010"], 2)
        self.assertEqual(stats["relation_counts"]["same_form_time:1941-07-04T1735"], 2)
        self.assertEqual(stats["relation_counts"]["same_final_group:TIYIZ"], 2)
        afuvo = next(row for row in live if row["designator"] == "AFUVO")
        self.assertEqual(afuvo["form_length"], 14)
        self.assertEqual(afuvo["nr"], 26)
        self.assertIsNone(afuvo["broken_on"])
        hfeyy = next(row for row in live if row["designator"] == "HFEYY")
        self.assertIn("five-dash gap", hfeyy["transcription_note"])
        self.assertEqual(stats["unmarked_with_j_note"], 2)
        self.assertEqual(stats["unmarked_form_length_under_20"], 1)


if __name__ == "__main__":
    unittest.main()
