"""Search corrections this repo has had to make. Not a reading.

The file is engine/data/corrections.json. Each record is a claim that a
later measurement overturned. Search is a substring over the id, the tags,
the wrong claim, and the correction. A hit is not a plaintext.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_PATH = Path(__file__).resolve().parent / "data" / "corrections.json"
_REQUIRED = (
    "id",
    "date",
    "recorded_by",
    "wrong",
    "correction",
    "evidence",
    "supersedes",
    "tags",
    "solved",
    "claimed_plaintext",
)


@lru_cache(maxsize=1)
def load_corrections() -> dict:
    data = json.loads(_PATH.read_text(encoding="utf-8"))
    if data.get("schema") != "corrections-1":
        raise ValueError("corrections file has the wrong schema")
    seen = set()
    for record in data["records"]:
        missing = [key for key in _REQUIRED if key not in record]
        if missing:
            raise ValueError(f"record missing {missing}")
        if record["id"] in seen:
            raise ValueError(f"duplicate correction id {record['id']}")
        seen.add(record["id"])
        if record["solved"] is not False or record["claimed_plaintext"] is not None:
            raise ValueError(f"correction {record['id']} claims a reading")
    return data


def search_corrections(query: str) -> list[dict]:
    """Return records whose id, tags, wrong claim, or correction contain the query."""
    needle = query.casefold().strip()
    if not needle:
        return []
    hits = []
    for record in load_corrections()["records"]:
        haystack = " ".join(
            [
                record["id"],
                record["wrong"],
                record["correction"],
                " ".join(record["tags"]),
            ]
        ).casefold()
        if needle in haystack:
            hits.append(record)
    return hits
