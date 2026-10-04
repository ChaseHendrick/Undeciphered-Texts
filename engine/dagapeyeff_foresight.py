"""Choose the next D'Agapeyeff job, then stop if it fails its own goal.

Each member has one goal and refuses a job that misses it. A job runs
only when every member lets it through. The job they allow is a fixed
digit dropped from each printed group of five. It has to land on the
book's square before a word score is worth running. No letter string
is stored.
"""

from __future__ import annotations

from engine.dagapeyeff_infer import infer
from engine.dagapeyeff_swarm import CHALLENGE

_ROW = set("67890")
_COLUMN = set("12345")

_MEMBERS = (
    {"id": "class-guard", "goal": "Refuse a job inside a closed class."},
    {"id": "closer", "goal": "Accept only a word score on cells the rule changes. The bar is prose at -2.5185."},
    {"id": "null-keeper", "goal": "Refuse a job with no shuffled control."},
    {"id": "budget", "goal": "Refuse a finished family, and a larger copy of one that already failed."},
    {"id": "square", "goal": "A digit rule has to land on the book square before a word score is worth running."},
)

_JOBS = (
    {"id": "period-5", "family": "short-shift", "changes_cells": True, "score": "word", "has_null": True, "budget": "large"},
    {"id": "column-order", "family": "reorder", "changes_cells": False, "score": "pattern", "has_null": True, "budget": "done"},
    {"id": "group-digit", "family": "group-digit", "changes_cells": True, "score": "word", "has_null": True, "budget": "small"},
)

_FAMILY = {
    "counts": ("counts",),
    "same-cells": ("reorder",),
    "short-keys": ("short-shift", "bifid", "running-text"),
}


def _closed_families(drawn: dict) -> set[str]:
    families = set()
    for item in drawn["classes"]:
        if item["status"] != "closed":
            continue
        families.update(_FAMILY[item["id"]])
    return families


def _rejections(job: dict, closed: set[str]) -> list[dict]:
    reasons = []
    if job["family"] in closed:
        reasons.append({"member": "class-guard", "reason": "This job is inside a closed class."})
    if job["score"] != "word" or not job["changes_cells"]:
        reasons.append({"member": "closer", "reason": "The goal is a word score on cells this rule changes."})
    if not job["has_null"]:
        reasons.append({"member": "null-keeper", "reason": "A job with no shuffled control cannot be a goal."})
    if job["budget"] != "small":
        reasons.append({"member": "budget", "reason": "This family is already finished, or it is a larger copy of one that failed."})
    return reasons


def _group_digits() -> list[dict]:
    groups = CHALLENGE.split()
    phases = []
    for phase in range(5):
        digits = "".join(group[:phase] + group[phase + 1:] for group in groups)
        off_square = 0
        pairs = len(digits) // 2
        for index in range(0, len(digits) - 1, 2):
            pair = digits[index:index + 2]
            if pair[0] not in _ROW or pair[1] not in _COLUMN:
                off_square += 1
        phases.append({"phase": phase, "pairs": pairs, "off_square": off_square})
    return phases


def foresight(records: list[dict] | None = None) -> dict:
    drawn = infer(records)
    closed = _closed_families(drawn)
    rejected = []
    accepted = []
    for job in _JOBS:
        reasons = _rejections(job, closed)
        if reasons:
            rejected.append({"id": job["id"], "by": reasons})
        else:
            accepted.append(job["id"])
    phases = _group_digits()
    fewest = min(phase["off_square"] for phase in phases)
    on_square = sum(1 for phase in phases if phase["off_square"] == 0)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "members": [dict(member) for member in _MEMBERS],
        "accepted": accepted,
        "rejected": rejected,
        "groups": len(CHALLENGE.split()),
        "phases": phases,
        "phases_on_square": on_square,
        "fewest_off_square": fewest,
        "verdict": "refuse",
        "do_not": "Do not drop one fixed digit from each printed group of five.",
        "learned": (
            "The members let through one job: drop one fixed digit from each printed group of five. "
            "That changes the cells, so it is not a closed class. "
            "None of the five positions stays on the book square. "
            "The fewest pairs off the square is 79 of 158. "
            "A word score was not run. Refuse it."
        ),
    }
