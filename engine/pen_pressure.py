"""Pen pressure as a second channel. The ink letters are not the secret.

A heavy stroke and a light stroke are the two forms Bacon used. A pinprick
is a hole through a chosen letter of an ordinary page. Neither one is
recoverable from the letter identities alone. This module reads only a
channel the caller supplies. It does not look at a scan and invent one.
"""

from __future__ import annotations

from collections.abc import Sequence

from engine.solvers.baconian import baconian_decode

# Light is Bacon's a-form. Heavy is the b-form. The choice is declared here.
_LIGHT = "L"
_HEAVY = "H"


def read_pressure(marks: str, *, variant: str = "24") -> dict:
    """Decode an explicit string of L and H. Anything else is not a pressure mark."""
    if not isinstance(marks, str) or not marks.strip():
        raise ValueError("pressure marks are required; ink letters are not a substitute")
    units = []
    for char in marks:
        if char.isspace():
            continue
        upper = char.upper()
        if upper == _LIGHT:
            units.append("a")
        elif upper == _HEAVY:
            units.append("b")
        else:
            raise ValueError("pressure marks must be L or H; a letter of ink is not a pressure")
    text = baconian_decode("".join(units), variant=variant)
    return {
        "text": text,
        "channel": "explicit heavy and light strokes",
        "variant": variant,
        "claimed_plaintext": None,
        "solved": False,
    }


def read_pinpricks(cover: str, indexes: Sequence[int]) -> dict:
    """Read the letters a caller says were pricked. The other letters stay cover text."""
    if not isinstance(cover, str):
        raise TypeError("cover text must be a string")
    letters = [(index, char.upper()) for index, char in enumerate(cover) if char.isalpha()]
    if not letters:
        raise ValueError("cover text has no letters")
    if isinstance(indexes, (str, bytes)) or not isinstance(indexes, Sequence):
        raise TypeError("pinprick indexes must be a sequence of positions in the cover")
    if not indexes:
        raise ValueError("no pinpricks were supplied")
    seen: set[int] = set()
    picked = []
    for index in indexes:
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("each pinprick index must be an integer")
        if index < 0 or index >= len(cover) or not cover[index].isalpha():
            raise ValueError("a pinprick must fall on a letter of the cover")
        if index in seen:
            raise ValueError("the same letter was pricked twice")
        seen.add(index)
        picked.append(cover[index].upper())
    return {
        "text": "".join(picked),
        "cover_letters": len(letters),
        "pricks": len(picked),
        "channel": "explicit pinprick positions",
        "claimed_plaintext": None,
        "solved": False,
    }


def ink_alone(text: str) -> dict:
    """The page as a transcription of letters. No pressure and no pinpricks were recorded."""
    if not isinstance(text, str) or not any(char.isalpha() for char in text):
        raise ValueError("ink text must contain a letter")
    return {
        "text": None,
        "pressure_recorded": False,
        "pinpricks_recorded": False,
        "claimed_plaintext": None,
        "solved": False,
        "reason": "A transcription of the ink does not contain the pressure channel.",
    }
