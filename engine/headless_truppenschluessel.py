"""Headless Truppenschlüssel. Two squares, no invented letter.

The cipher is the repo's two-square. A dash or a J occupies one slot and
stays a hole, so the pair grid does not slide sideways. An odd leftover
letter is a hole too. Nothing is padded with X. solved stays false.
"""

from __future__ import annotations

from engine.ciphers import square_from_keyword, two_square_decrypt, two_square_encrypt
from engine.ts_close_pairs import (
    DEZPS_KNOWN,
    DSZPZ,
    HOHOX,
    IASRZ_129,
    IASRZ_130,
    SSKFV,
)

_RESIDUE = (
    ("IASRZ_129", IASRZ_129),
    ("IASRZ_130", IASRZ_130),
    ("DSZPZ", DSZPZ),
    ("DEZPS", DEZPS_KNOWN),
    ("SSKFV", SSKFV),
    ("HOHOX", HOHOX),
)


class HeadlessTruppenschluessel:
    """One pair of 5×5 squares. It enciphers known letters. It does not pick a key."""

    def __init__(self, left: str, right: str) -> None:
        # square_from_keyword accepts an already-built square and rejects a bad one.
        self.left = square_from_keyword(left)
        self.right = square_from_keyword(right)

    def seal(self, text: str) -> str:
        """Encrypt a complete even letter string. J, dashes, and odd length are refused."""
        letters = "".join(char.upper() for char in text if char.isalpha())
        if "J" in letters:
            raise ValueError("J is not in this square; pass II as I, or do not invent a substitute")
        if len(letters) % 2 or not letters:
            raise ValueError("will not invent a padding letter")
        return two_square_encrypt(letters, self.left, self.right)

    def feed(self, text: str) -> str:
        """Decrypt. Spaces are ignored. A dash or J spoils that one pair and does not slide the rest."""
        slots = []
        for char in text:
            if char.isspace():
                continue
            upper = char.upper()
            if upper == "-" or upper == "J":
                slots.append("-")
            elif upper.isalpha():
                slots.append(upper)
            else:
                raise ValueError("feed accepts letters, spaces, dashes, and J as a hole")
        out: list[str] = []
        for index in range(0, len(slots) - 1, 2):
            pair = slots[index] + slots[index + 1]
            if "-" in pair:
                out.append("??")
            else:
                out.append(two_square_decrypt(pair, self.left, self.right))
        if len(slots) % 2:
            out.append("?")
        if not out:
            raise ValueError("text has no slots")
        return "".join(out)


def residue_without_squares() -> dict:
    """The unsolved messages have no printed squares. Do not open them."""
    blocked = tuple(
        {"name": name, "letters": len(text), "squares_published": False, "opened": False}
        for name, text in _RESIDUE
    )
    return {
        "claimed_plaintext": None,
        "solved": False,
        "blocked": blocked,
        "scope": "No Truppenschlüssel square was printed for these six messages. None were opened.",
    }
