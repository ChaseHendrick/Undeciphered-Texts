"""Ogham character lookup from the Unicode Standard names list.

This is a lookup of published character identities (code point and Unicode
name). It is not a decipherment of Ogham inscriptions, Primitive Irish, or
any undeciphered text. It does not assign a reading to a monument.

Source fetched 2026-10-02 (Unicode 18.0.0 Ogham names list):
https://unicode.org/Public/18.0.0/charts/nameslist/1680/
"""

from __future__ import annotations

from dataclasses import dataclass

SOURCE_URL = "https://unicode.org/Public/18.0.0/charts/nameslist/1680/"
SOURCE_NOTE = (
    "Unicode 18.0.0 Ogham names list (U+1680..U+169C). "
    "Character identity only; not a decipherment."
)

# (code point, Unicode name, group) as printed on the names list above.
# The character is the Unicode scalar for that code point.
_ROWS: tuple[tuple[int, str, str], ...] = (
    (0x1680, "OGHAM SPACE MARK", "space"),
    (0x1681, "OGHAM LETTER BEITH", "traditional"),
    (0x1682, "OGHAM LETTER LUIS", "traditional"),
    (0x1683, "OGHAM LETTER FEARN", "traditional"),
    (0x1684, "OGHAM LETTER SAIL", "traditional"),
    (0x1685, "OGHAM LETTER NION", "traditional"),
    (0x1686, "OGHAM LETTER UATH", "traditional"),
    (0x1687, "OGHAM LETTER DAIR", "traditional"),
    (0x1688, "OGHAM LETTER TINNE", "traditional"),
    (0x1689, "OGHAM LETTER COLL", "traditional"),
    (0x168A, "OGHAM LETTER CEIRT", "traditional"),
    (0x168B, "OGHAM LETTER MUIN", "traditional"),
    (0x168C, "OGHAM LETTER GORT", "traditional"),
    (0x168D, "OGHAM LETTER NGEADAL", "traditional"),
    (0x168E, "OGHAM LETTER STRAIF", "traditional"),
    (0x168F, "OGHAM LETTER RUIS", "traditional"),
    (0x1690, "OGHAM LETTER AILM", "traditional"),
    (0x1691, "OGHAM LETTER ONN", "traditional"),
    (0x1692, "OGHAM LETTER UR", "traditional"),
    (0x1693, "OGHAM LETTER EADHADH", "traditional"),
    (0x1694, "OGHAM LETTER IODHADH", "traditional"),
    (0x1695, "OGHAM LETTER EABHADH", "forfeda"),
    (0x1696, "OGHAM LETTER OR", "forfeda"),
    (0x1697, "OGHAM LETTER UILLEANN", "forfeda"),
    (0x1698, "OGHAM LETTER IFIN", "forfeda"),
    (0x1699, "OGHAM LETTER EAMHANCHOLL", "forfeda"),
    (0x169A, "OGHAM LETTER PEITH", "forfeda"),
    (0x169B, "OGHAM FEATHER MARK", "punctuation"),
    (0x169C, "OGHAM REVERSED FEATHER MARK", "punctuation"),
)


@dataclass(frozen=True)
class OghamEntry:
    """One row from the Unicode Ogham names list."""

    codepoint: int
    name: str
    group: str

    @property
    def character(self) -> str:
        return chr(self.codepoint)

    @property
    def code(self) -> str:
        return f"U+{self.codepoint:04X}"


_BY_CP: dict[int, OghamEntry] = {
    cp: OghamEntry(cp, name, group) for cp, name, group in _ROWS
}
_BY_CHAR: dict[str, OghamEntry] = {chr(cp): entry for cp, entry in _BY_CP.items()}
_BY_NAME: dict[str, OghamEntry] = {entry.name: entry for entry in _BY_CP.values()}


def entries() -> tuple[OghamEntry, ...]:
    """Every names-list row, in code-point order."""
    return tuple(_BY_CP[cp] for cp, _, _ in _ROWS)


def lookup(query: str | int) -> OghamEntry:
    """Look up a code point, U+hex, character, or exact Unicode name.

    Raises KeyError when the query is not on the sourced names list.
    """
    if isinstance(query, int):
        return _BY_CP[query]
    text = query.strip()
    if text in _BY_CHAR:
        return _BY_CHAR[text]
    if text in _BY_NAME:
        return _BY_NAME[text]
    folded = text.upper().replace(" ", "")
    if folded.startswith("U+"):
        return _BY_CP[int(folded[2:], 16)]
    if folded.startswith("0X"):
        return _BY_CP[int(folded, 16)]
    if all(ch in "0123456789ABCDEF" for ch in folded) and folded:
        return _BY_CP[int(folded, 16)]
    raise KeyError(query)
