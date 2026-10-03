"""Preference for candidate sentences that use fortune, heir, and estate.

Persona: inheritance. Reworded from a dying-aristocrat label into plain
speech about a household and what was left. The word list is a preference
among candidates. These are preferences among candidates, not decipherments
of Nr. 86, K4, or an unknown script.
"""

from __future__ import annotations

import re

# Word list for the inheritance preference: fortune, heir, estate.
WORD_LIST = ("fortune", "heir", "estate")

DISCLAIMER = (
    "These are preferences among candidates, not decipherments of "
    "Nr. 86, K4, or an unknown script."
)


def covers(text: str) -> bool:
    """True when every inheritance word appears as its own word."""
    lowered = text.lower()
    return all(re.search(rf"\b{re.escape(word)}\b", lowered) for word in WORD_LIST)


def choose(left: str, right: str) -> str:
    """Pick the candidate that matches the inheritance word list.

    Exactly one of the two sentences must contain fortune, heir, and estate.
    The other is a plain alternative. This does not decipher anything.
    """
    left_ok = covers(left)
    right_ok = covers(right)
    if left_ok == right_ok:
        raise ValueError("need exactly one candidate that matches the word list")
    return left if left_ok else right
