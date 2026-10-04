"""Checked metadata ledger for the public Truppenschlüssel residue.

The source page is Frode Weierud's CryptoCellar list of German Army
Truppenschlüssel messages the 2015 attack did not break. Later breaks are
printed on that same page. This module counts those marks. It does not store
ciphertext or plaintext, and it does not search keys.
"""

from __future__ import annotations

import json
from pathlib import Path

_LEDGER = Path(__file__).resolve().parent / "data" / "truppenschluessel_residue_2026-10-04.json"
_FORBIDDEN = {"ciphertext", "plaintext", "body", "groups", "key", "squares"}


def load_residue(path: Path | None = None) -> dict:
    """Load the dated residue ledger and reject stored message text."""
    source = path or _LEDGER
    payload = json.loads(source.read_text(encoding="utf-8"))
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("residue ledger has no messages")
    for row in messages:
        overlap = _FORBIDDEN.intersection(row)
        if overlap:
            raise ValueError(f"residue row stores forbidden fields: {sorted(overlap)}")
    return payload


def unmarked(payload: dict) -> list[dict]:
    """Rows with no Broken-on date on the checked page."""
    return [row for row in payload["messages"] if not row.get("broken_on")]


def summarize(payload: dict | None = None) -> dict:
    """Count the page without treating a broken row as live residue."""
    payload = payload or load_residue()
    rows = payload["messages"]
    live = unmarked(payload)
    broken_dates: dict[str, int] = {}
    for row in rows:
        mark = row.get("broken_on")
        if mark:
            broken_dates[mark] = broken_dates.get(mark, 0) + 1
    relations: dict[str, int] = {}
    for row in live:
        for link in row.get("relations") or []:
            relations[link] = relations.get(link, 0) + 1
    return {
        "checked": payload["checked"],
        "page_updated": payload["page_updated"],
        "listed": len(rows),
        "broken": len(rows) - len(live),
        "unmarked": len(live),
        "broken_dates": broken_dates,
        "unmarked_with_j_note": sum(1 for row in live if row.get("page_j_note")),
        "unmarked_form_length_under_20": sum(
            1 for row in live if isinstance(row.get("form_length"), int) and row["form_length"] < 20
        ),
        "relation_counts": relations,
    }
