"""Hash the cells and the scores that depend on them. Not a reading.

The encoding is part of the result. Tuples become lists. Floats become the
17-digit general format. Object keys are sorted. SHA-256 of that JSON is the
content hash. Each step's chain hash is SHA-256 of the previous chain hash,
a newline, and the new content hash. The first step's chain hash is its
content hash. No letter string is stored.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from engine.dagapeyeff_balls import ball_report
from engine.dagapeyeff_convert import convert_report
from engine.dagapeyeff_record import record_report
from engine.dagapeyeff_swarm import challenge_pairs
from engine.dagapeyeff_yardstick import yardstick_report


def freeze(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("a provenance hash cannot cover a non-finite float")
        return format(value, ".17g")
    if isinstance(value, (list, tuple)):
        return [freeze(item) for item in value]
    if isinstance(value, dict):
        return {str(key): freeze(value[key]) for key in sorted(value, key=str)}
    raise TypeError(f"no provenance encoding for {type(value).__name__}")


def content_hash(value: Any) -> str:
    payload = json.dumps(freeze(value), separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def chain_hash(previous: str | None, content: str) -> str:
    if previous is None:
        return content
    return hashlib.sha256(f"{previous}\n{content}".encode("utf-8")).hexdigest()


def provenance_report() -> dict:
    steps = (
        ("cells", list(challenge_pairs())),
        ("yardstick", yardstick_report()),
        ("balls", ball_report()),
        ("record", record_report()),
        ("convert", convert_report()),
    )
    entries = []
    previous = None
    for name, value in steps:
        content = content_hash(value)
        previous = chain_hash(previous, content)
        entries.append({"name": name, "content_sha256": content, "chain_sha256": previous})
    return {
        "solved": False,
        "claimed_plaintext": None,
        "entries": entries,
        "chain_sha256": previous,
        "scope": (
            "A matching hash means the cells and these scores were recomputed, not that they were read. "
            "No letter string is stored."
        ),
    }
