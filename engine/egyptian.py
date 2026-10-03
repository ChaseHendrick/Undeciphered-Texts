"""Egyptian hieroglyph lookup reader for a small Gardiner-sign subset.

Egyptian is a known (deciphered) script. This module maps Gardiner codes or
Unicode hieroglyphs to traditional Egyptological transliteration and a short
gloss from a sourced sign table. It is a dictionary lookup of known signs, not
a new decipherment, and it does not read damaged, incomplete, or unknown
inscriptions.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

_DATA_PATH = Path(__file__).resolve().parent / "data" / "gardiner_signs.json"
_HIEROGLYPH_START = 0x13000
_HIEROGLYPH_END = 0x1342F


@dataclass(frozen=True)
class SignEntry:
    """One Gardiner sign from the sourced subset table."""

    code: str
    unicode: str | None
    unicode_hex: str | None
    transliteration: str
    meaning: str

    @property
    def gloss(self) -> str:
        return self.meaning


@dataclass(frozen=True)
class SignReading:
    """Lookup result for one input token."""

    input: str
    code: str
    unicode: str | None
    transliteration: str
    gloss: str


@dataclass(frozen=True)
class Reading:
    """Transliteration plus gloss for a sequence of known signs."""

    signs: tuple[SignReading, ...]
    transliteration: str
    gloss: str

    def as_dict(self) -> dict:
        return {
            "transliteration": self.transliteration,
            "gloss": self.gloss,
            "signs": [
                {
                    "input": s.input,
                    "code": s.code,
                    "unicode": s.unicode,
                    "transliteration": s.transliteration,
                    "gloss": s.gloss,
                }
                for s in self.signs
            ],
        }


class UnknownSignError(KeyError):
    """Raised when a token is not in the loaded Gardiner subset."""


def _normalize_code(raw: str) -> str:
    text = raw.strip()
    if not text:
        raise UnknownSignError("empty sign token")
    # Accept AA1 / Aa1 / aa1; keep letter category + digits + optional letter.
    match = re.fullmatch(r"([A-Za-z]{1,2})(\d+)([A-Za-z]?)", text)
    if not match:
        return text.upper() if text.isascii() else text
    letters, digits, suffix = match.groups()
    if letters.upper() == "AA":
        head = "Aa"
    else:
        head = letters[0].upper() + letters[1:].lower() if len(letters) > 1 else letters.upper()
    return f"{head}{int(digits)}{suffix.upper()}"


def _is_hieroglyph_char(ch: str) -> bool:
    if len(ch) != 1:
        return False
    cp = ord(ch)
    return _HIEROGLYPH_START <= cp <= _HIEROGLYPH_END


def tokenize_input(sequence: str | Sequence[str]) -> list[str]:
    """Split Gardiner codes and/or Unicode hieroglyphs into tokens.

    Accepts a whitespace/comma/hyphen separated string of Gardiner codes, a
    string of contiguous Unicode hieroglyphs, a mixed string, or an iterable of
    tokens. Does not invent readings for damaged or unknown marks.
    """
    if isinstance(sequence, str):
        text = sequence.strip()
        if not text:
            return []
        # Prefer explicit separators when present.
        if re.search(r"[\s,;/|\-]+", text) and any(ch.isascii() and ch.isalpha() for ch in text):
            parts = re.split(r"[\s,;/|\-]+", text)
            return [p for p in parts if p]
        tokens: list[str] = []
        i = 0
        while i < len(text):
            ch = text[i]
            if ch.isspace() or ch in ",;/|-":
                i += 1
                continue
            if _is_hieroglyph_char(ch):
                tokens.append(ch)
                i += 1
                continue
            # Gardiner code: letters + digits (+ optional trailing letter)
            m = re.match(r"(?:AA|Aa|aa|[A-Za-z])\d+[A-Za-z]?", text[i:])
            if m:
                tokens.append(m.group(0))
                i += len(m.group(0))
                continue
            raise UnknownSignError(f"unrecognized token starting at {text[i:]!r}")
        return tokens
    return [str(item).strip() for item in sequence if str(item).strip()]


class EgyptianHieroglyphReader:
    """Lookup reader over a small sourced Gardiner-sign subset."""

    def __init__(self, signs: Sequence[SignEntry], *, source_url: str) -> None:
        self.source_url = source_url
        self._by_code: dict[str, SignEntry] = {}
        self._by_unicode: dict[str, SignEntry] = {}
        for entry in signs:
            code = _normalize_code(entry.code)
            self._by_code[code] = entry
            self._by_code[code.upper()] = entry
            if entry.unicode:
                self._by_unicode[entry.unicode] = entry
        self.signs = tuple(self._by_code[c] for c in sorted({_normalize_code(s.code) for s in signs}))

    @classmethod
    def from_json(cls, path: Path | str | None = None) -> "EgyptianHieroglyphReader":
        target = Path(path) if path is not None else _DATA_PATH
        payload = json.loads(target.read_text(encoding="utf-8"))
        entries = [
            SignEntry(
                code=row["code"],
                unicode=row.get("unicode") or None,
                unicode_hex=row.get("unicode_hex") or None,
                transliteration=row.get("transliteration") or "",
                meaning=row.get("meaning") or "",
            )
            for row in payload["signs"]
        ]
        return cls(entries, source_url=payload.get("source_url", ""))

    def lookup_sign(self, token: str) -> SignEntry:
        """Return the table row for one Gardiner code or Unicode hieroglyph."""
        raw = token.strip()
        if not raw:
            raise UnknownSignError("empty sign token")
        if raw in self._by_unicode:
            return self._by_unicode[raw]
        if _is_hieroglyph_char(raw):
            raise UnknownSignError(f"Unicode hieroglyph not in subset table: {raw!r}")
        code = _normalize_code(raw)
        entry = self._by_code.get(code) or self._by_code.get(code.upper())
        if entry is None:
            raise UnknownSignError(f"Gardiner code not in subset table: {raw!r}")
        return entry

    def read(self, sequence: str | Sequence[str]) -> Reading:
        """Map a sign sequence to concatenated transliteration and gloss list.

        Phonetic values are concatenated without separators. A following sign
        whose whole value is already a suffix of the reading so far is treated
        as a phonetic complement and is not repeated (so M17+Y5+N35 is j+mn+n
        → jmn, not jmnn). Per-sign rows still keep the table value. Gloss
        strings are joined with '; '. Empty transliterations (silent
        determinatives) are omitted from the reading but kept in per-sign rows.

        This complement rule is the textbook convention for redundant
        uniliterals. It can collapse a genuine repeated consonant. It does not
        resolve honorific transposition, damaged signs, or signs outside the
        table.
        """
        tokens = tokenize_input(sequence)
        if not tokens:
            return Reading(signs=(), transliteration="", gloss="")
        readings: list[SignReading] = []
        transliteration = ""
        gloss_parts: list[str] = []
        for token in tokens:
            entry = self.lookup_sign(token)
            code = _normalize_code(entry.code)
            readings.append(
                SignReading(
                    input=token,
                    code=code,
                    unicode=entry.unicode,
                    transliteration=entry.transliteration,
                    gloss=entry.gloss,
                )
            )
            value = entry.transliteration
            if value and not (transliteration.endswith(value)):
                transliteration += value
            if entry.gloss:
                gloss_parts.append(f"{code}: {entry.gloss}")
        return Reading(
            signs=tuple(readings),
            transliteration=transliteration,
            gloss="; ".join(gloss_parts),
        )


@lru_cache(maxsize=1)
def get_reader() -> EgyptianHieroglyphReader:
    """Load the default sourced Gardiner subset reader."""
    return EgyptianHieroglyphReader.from_json()


def read_hieroglyphs(sequence: str | Sequence[str]) -> Reading:
    """Convenience wrapper: Gardiner codes or Unicode → transliteration + gloss."""
    return get_reader().read(sequence)
