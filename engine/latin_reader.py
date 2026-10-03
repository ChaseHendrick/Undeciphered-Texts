"""Gloss known Latin after Roman inscription spelling is normalized.

Latin is a known language. This is a dictionary lookup over a small lexicon
copied from cited pages. It is not a decipherment of unknown texts, not a
morphological parser, and not a translation of a passage. A token is glossed
only when that exact classical form is listed, or when a listed -que clitic
can be split off a listed stem.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from engine.roman_text import to_classical, to_epigraphic

_LEXICON = Path(__file__).resolve().parent / "data" / "latin_lexicon.json"

NOT_A_DECIPHERMENT = (
    "Latin is a known language. This reader normalizes Roman inscription "
    "spelling and glosses words that are already in a small cited lexicon. "
    "It is not a decipherment of unknown texts."
)


@dataclass(frozen=True)
class Gloss:
    """One lexicon hit. known is False when the form is not in the list."""

    form: str
    lemma: str | None
    headword: str | None
    gloss: str | None
    source_url: str | None
    known: bool


@dataclass(frozen=True)
class LatinReading:
    original: str
    epigraphic: str
    classical: str
    glosses: tuple[Gloss, ...]
    note: str


@dataclass(frozen=True)
class _Entry:
    lemma: str
    headword: str
    gloss: str
    source_url: str
    forms: frozenset[str]


def _split_que(token: str, forms: dict[str, _Entry]) -> tuple[str, ...] | None:
    if len(token) <= 3 or not token.endswith("QUE"):
        return None
    stem = token[: -3]
    if stem in forms and "QUE" in forms:
        return (stem, "QUE")
    return None


class LatinLexicon:
    """In-memory copy of engine/data/latin_lexicon.json."""

    def __init__(self, entries: list[_Entry]) -> None:
        self.entries = tuple(entries)
        self.by_form: dict[str, _Entry] = {}
        for entry in entries:
            for form in entry.forms:
                self.by_form[form] = entry

    def lookup(self, token: str) -> tuple[Gloss, ...]:
        parts = _split_que(token, self.by_form) or (token,)
        found: list[Gloss] = []
        for part in parts:
            entry = self.by_form.get(part)
            if entry is None:
                found.append(
                    Gloss(
                        form=part,
                        lemma=None,
                        headword=None,
                        gloss=None,
                        source_url=None,
                        known=False,
                    )
                )
            else:
                found.append(
                    Gloss(
                        form=part,
                        lemma=entry.lemma,
                        headword=entry.headword,
                        gloss=entry.gloss,
                        source_url=entry.source_url,
                        known=True,
                    )
                )
        return tuple(found)


def load_lexicon(path: Path | None = None) -> LatinLexicon:
    raw = json.loads((path or _LEXICON).read_text(encoding="utf-8"))
    entries: list[_Entry] = []
    for row in raw["entries"]:
        forms = {str(form).upper() for form in row["forms"]}
        forms.add(str(row["lemma"]).upper())
        entries.append(
            _Entry(
                lemma=row["lemma"],
                headword=row["headword"],
                gloss=row["gloss"],
                source_url=row["source_url"],
                forms=frozenset(forms),
            )
        )
    return LatinLexicon(entries)


@lru_cache(maxsize=1)
def get_lexicon() -> LatinLexicon:
    return load_lexicon()


def read_latin(text: str, lexicon: LatinLexicon | None = None) -> LatinReading:
    """Normalize inscription spelling and gloss each known classical token."""
    book = lexicon or get_lexicon()
    classical = to_classical(text)
    glosses: list[Gloss] = []
    for token in classical.split():
        glosses.extend(book.lookup(token))
    return LatinReading(
        original=text,
        epigraphic=to_epigraphic(text),
        classical=classical,
        glosses=tuple(glosses),
        note=NOT_A_DECIPHERMENT,
    )
