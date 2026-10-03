"""Lookup of one Greek letter and one published Classical Greek gloss.

This module returns rows copied from cited pages. It does not decipher
Linear B, and it does not decipher unknown Greek (Linear A, Cypro-Minoan,
or any other unread script). It does not assign values to undeciphered signs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Kept as a constant so callers and tests can see the limit without reading prose.
DOES_NOT_DECIPHER_LINEAR_B_OR_UNKNOWN_GREEK = True

_DATA = Path(__file__).resolve().parent / "data" / "ancient_greek_lookup.json"

LETTER_SOURCE_URL = "https://unicode.org/Public/18.0.0/charts/nameslist/0370/"
WORD_SOURCE_URL = (
    "https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)/nqrwpos"
)


@dataclass(frozen=True)
class GreekLetter:
    codepoint: str
    character: str
    unicode_name: str
    ancient_name: str
    source_url: str
    ancient_name_source_url: str

    def as_dict(self) -> dict[str, str]:
        return {
            "codepoint": self.codepoint,
            "character": self.character,
            "unicode_name": self.unicode_name,
            "ancient_name": self.ancient_name,
            "source_url": self.source_url,
            "ancient_name_source_url": self.ancient_name_source_url,
        }


@dataclass(frozen=True)
class GreekWord:
    lemma: str
    gloss: str
    sense: str
    source_url: str

    def as_dict(self) -> dict[str, str]:
        return {
            "lemma": self.lemma,
            "gloss": self.gloss,
            "sense": self.sense,
            "source_url": self.source_url,
        }


def _payload() -> dict:
    return json.loads(_DATA.read_text(encoding="utf-8"))


def letters() -> tuple[GreekLetter, ...]:
    return tuple(GreekLetter(**row) for row in _payload()["letters"])


def words() -> tuple[GreekWord, ...]:
    return tuple(GreekWord(**row) for row in _payload()["words"])


def _single_token(value: str) -> str | None:
    if not isinstance(value, str):
        raise TypeError("query must be a string")
    key = " ".join(value.strip().split())
    if not key or " " in key:
        return None
    return key


def lookup_letter(query: str) -> GreekLetter | None:
    """Return the catalog row for one fetched Greek letter.

    ``query`` must be a single character, ``U+`` code, or exact Unicode name.
    A longer string is not a decipherment: the result is ``None``.
    """
    key = _single_token(query)
    if key is None:
        return None
    folded = key.upper().replace(" ", "")
    for row in letters():
        names = {row.character, row.codepoint, row.codepoint.upper(), row.unicode_name}
        if key in names or folded == row.codepoint.upper().replace(" ", ""):
            return row
        if key.upper() == row.unicode_name:
            return row
    return None


def lookup_word(lemma: str) -> GreekWord | None:
    """Return the catalog row for one fetched lemma.

    ``lemma`` must be a single dictionary headword already in the file.
    A passage, a Linear B transcription, or any other string returns ``None``.
    """
    key = _single_token(lemma)
    if key is None:
        return None
    for row in words():
        if key == row.lemma:
            return row
    return None
