"""Preference for candidate sentences that use color, dream, and melting.

Persona: hallucinogens. The word list is a preference among candidates.
These are preferences among candidates, not decipherments of Nr. 86, K4,
or an unknown script.
"""

from __future__ import annotations

import re

# Word list for the hallucinogens preference: color, dream, melting.
WORD_LIST = ("color", "dream", "melting")

DISCLAIMER = (
    "These are preferences among candidates, not decipherments of "
    "Nr. 86, K4, or an unknown script."
)


def covers(text: str) -> bool:
    """True when every hallucinogens word appears as its own word."""
    lowered = text.lower()
    return all(re.search(rf"\b{re.escape(word)}\b", lowered) for word in WORD_LIST)


def choose(left: str, right: str) -> str:
    """Pick the candidate that matches the hallucinogens word list.

    Exactly one of the two sentences must contain color, dream, and melting.
    The other is a plain alternative. This does not decipher anything.
    """
    left_ok = covers(left)
    right_ok = covers(right)
    if left_ok == right_ok:
        raise ValueError("need exactly one candidate that matches the word list")
    return left if left_ok else right
