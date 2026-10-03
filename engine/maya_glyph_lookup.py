"""Lookup of published Classic Maya sign readings.

This module only returns rows copied from a cited catalog. It does not
decipher undeciphered Maya passages, inscriptions, or codices.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Kept as a constant so callers and tests can see the limit without reading prose.
DOES_NOT_DECIPHER_UNDECIPHERED_MAYA_PASSAGES = True

_DATA = Path(__file__).resolve().parent / "data" / "maya_glyph_lookup.json"
_APOSTROPHES = str.maketrans({
    "\u2019": "'",  # RIGHT SINGLE QUOTATION MARK, as in the CMGG gloss "k’in"
    "\u02bc": "'",  # MODIFIER LETTER APOSTROPHE
    "\u2018": "'",
    "`": "'",
})


@dataclass(frozen=True)
class GlyphReading:
    thompson: str
    also_listed_as: tuple[str, ...]
    reading: str
    part_of_speech: str
    gloss: str
    source_url: str

    def as_dict(self) -> dict[str, object]:
        return {
            "thompson": self.thompson,
            "also_listed_as": list(self.also_listed_as),
            "reading": self.reading,
            "part_of_speech": self.part_of_speech,
            "gloss": self.gloss,
            "source_url": self.source_url,
        }


def _load() -> list[GlyphReading]:
    payload = json.loads(_DATA.read_text(encoding="utf-8"))
    rows: list[GlyphReading] = []
    for item in payload["glyphs"]:
        rows.append(
            GlyphReading(
                thompson=item["thompson"],
                also_listed_as=tuple(item.get("also_listed_as", ())),
                reading=item["reading"],
                part_of_speech=item["part_of_speech"],
                gloss=item["gloss"],
                source_url=item["source_url"],
            )
        )
    return rows


def _norm(value: str) -> str:
    return " ".join(value.strip().translate(_APOSTROPHES).upper().split())


def lookup(sign: str) -> GlyphReading | None:
    """Return the catalog row for one known sign id or reading.

    ``sign`` must be a single catalog key such as ``T544`` or ``K'IN``.
    A longer string is not segmented and is not a decipherment: the result
    is ``None``.
    """
    if not isinstance(sign, str):
        raise TypeError("sign must be a string")
    key = _norm(sign)
    if not key or " " in key:
        return None
    for row in _load():
        names = [row.thompson, row.reading, *row.also_listed_as]
        if key in {_norm(name) for name in names}:
            return row
    return None
