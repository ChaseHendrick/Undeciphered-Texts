"""Known-language reader router.

Dispatch a short phrase to a reader for a language that is already known.
English and German use the small cited lexicons in this file. Latin is
delegated to engine.latin_reader. Egyptian Gardiner sign codes are delegated
to engine.egyptian when that module imports; otherwise Egyptian is skipped.

This does NOT decipher unknown languages or scripts. Linear A, the Indus
script, the Voynich manuscript, and rongorongo are refused. A gloss is a
dictionary or sign-table hit with a citation. Tokens that are not in the
lexicon stay unglossed. They are not guessed.

German headwords in this file keep their umlauts (König, jüngste, schön,
Töchter). The file is UTF-8.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

NOT_A_DECIPHERMENT = (
    "This reader glosses a few known languages from cited dictionaries. "
    "It does not decipher unknown languages or scripts, including Linear A, "
    "the Indus script, the Voynich manuscript, and rongorongo."
)

_REFUSED_SCRIPTS = {
    "linear a": "Linear A",
    "linear-a": "Linear A",
    "lineara": "Linear A",
    "indus": "the Indus script",
    "indus script": "the Indus script",
    "indus valley": "the Indus script",
    "indus valley script": "the Indus script",
    "voynich": "the Voynich manuscript",
    "voynich manuscript": "the Voynich manuscript",
    "rongorongo": "rongorongo",
}

_TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)

_WIKT_EN = "Wiktionary (CC BY-SA), English"
_WIKT_DE = "Wiktionary (CC BY-SA), German"


class UnknownScriptError(ValueError):
    """The caller asked for an undeciphered script. No gloss is returned."""


class UnknownLanguageError(ValueError):
    """The language is not one of the known-language readers."""


@dataclass(frozen=True)
class Gloss:
    """One lexicon or sign-table hit."""

    token: str
    lemma: str
    part_of_speech: str
    gloss: str
    citation: str
    source_url: str


@dataclass(frozen=True)
class GlossReport:
    """Glosses for one phrase. Unglossed tokens are listed, not guessed."""

    language: str
    phrase: str
    phrase_citation: str
    entries: tuple[Gloss, ...]
    unglossed: tuple[str, ...]
    reading: str = ""
    disclaimer: str = NOT_A_DECIPHERMENT


@dataclass(frozen=True)
class _Sense:
    lemma: str
    part_of_speech: str
    gloss: str
    citation: str
    source_url: str


def _sense(
    lemma: str,
    part_of_speech: str,
    gloss: str,
    citation: str,
    source_url: str,
) -> _Sense:
    return _Sense(lemma, part_of_speech, gloss, citation, source_url)


# Surface form (casefold) -> sense. Checked against the cited page on 2026-10-02.
_ENGLISH: dict[str, _Sense] = {
    "tired": _sense(
        "tired",
        "adjective",
        "in need of some rest or sleep",
        _WIKT_EN + ', s.v. "tired"',
        "https://en.wiktionary.org/wiki/tired",
    ),
    "sister": _sense(
        "sister",
        "noun",
        "a daughter of the same parents as another person; a female sibling",
        _WIKT_EN + ', s.v. "sister"',
        "https://en.wiktionary.org/wiki/sister",
    ),
}

_GERMAN: dict[str, _Sense] = {
    "könig": _sense(
        "König",
        "noun",
        "king",
        _WIKT_DE + ', s.v. "König"',
        "https://en.wiktionary.org/wiki/K%C3%B6nig",
    ),
    "töchter": _sense(
        "Tochter",
        "noun",
        "daughters",
        _WIKT_DE + ', s.v. "Tochter" (form Töchter is the plural)',
        "https://en.wiktionary.org/wiki/Tochter",
    ),
    "tochter": _sense(
        "Tochter",
        "noun",
        "daughter",
        _WIKT_DE + ', s.v. "Tochter"',
        "https://en.wiktionary.org/wiki/Tochter",
    ),
    "schön": _sense(
        "schön",
        "adjective",
        "beautiful, lovely, pretty",
        _WIKT_DE + ', s.v. "schön"',
        "https://en.wiktionary.org/wiki/sch%C3%B6n",
    ),
    "jüngste": _sense(
        "jung",
        "adjective",
        "youngest; feminine superlative of jung",
        _WIKT_DE + ', s.v. "jung" / "jüngste" (superlative)',
        "https://en.wiktionary.org/wiki/j%C3%BCngste",
    ),
}

_LEXICONS = {
    "english": _ENGLISH,
    "german": _GERMAN,
}


def normalize_language(name: str) -> str:
    """Casefold a language name and collapse spaces."""
    folded = name.strip().casefold().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", folded)


def _refused_label(name: str) -> str | None:
    spaced = normalize_language(name)
    if spaced in _REFUSED_SCRIPTS:
        return _REFUSED_SCRIPTS[spaced]
    compact = spaced.replace(" ", "")
    return {
        "lineara": "Linear A",
        "indusscript": "the Indus script",
        "voynichmanuscript": "the Voynich manuscript",
        "rongorongo": "rongorongo",
    }.get(compact)


def latin_reader_module():
    """Return engine.latin_reader, or None if it cannot be imported."""
    try:
        from engine import latin_reader
    except ImportError:
        return None
    if not callable(getattr(latin_reader, "read_latin", None)):
        return None
    return latin_reader


def egyptian_sign_module():
    """Return engine.egyptian when Gardiner sign codes can be glossed, else None."""
    try:
        from engine import egyptian
    except ImportError:
        return None
    if not callable(getattr(egyptian, "read_hieroglyphs", None)):
        return None
    if not callable(getattr(egyptian, "get_reader", None)):
        return None
    return egyptian


def available_languages() -> tuple[str, ...]:
    """Languages this router will gloss. Egyptian is omitted when its module is absent."""
    names = ["english"]
    if latin_reader_module() is not None:
        names.append("latin")
    names.append("german")
    if egyptian_sign_module() is not None:
        names.append("egyptian")
    return tuple(names)


def tokenize(phrase: str) -> list[str]:
    """Letter tokens, keeping Unicode letters such as ä, ö, ü, and ß."""
    return _TOKEN.findall(phrase)


def gloss_phrase(
    language: str,
    phrase: str,
    *,
    phrase_citation: str = "",
) -> GlossReport:
    """Gloss ``phrase`` in a known language.

    Raises UnknownScriptError for Linear A, Indus, Voynich, and rongorongo.
    Raises UnknownLanguageError for any other name that is not registered.
    Does not guess a meaning for a token that is not in the lexicon.
    """
    if not isinstance(phrase, str):
        raise TypeError("phrase must be a str")
    refused = _refused_label(language)
    if refused is not None:
        raise UnknownScriptError(
            f"{refused} is not a known language this reader can gloss. "
            + NOT_A_DECIPHERMENT
        )
    key = normalize_language(language)
    if key == "latin":
        return _gloss_latin(phrase, phrase_citation)
    if key == "egyptian":
        return _gloss_egyptian(phrase, phrase_citation)
    lexicon = _LEXICONS.get(key)
    if lexicon is None:
        known = ", ".join(available_languages())
        raise UnknownLanguageError(
            f"No known-language reader for {language!r}. Registered: {known}. "
            + NOT_A_DECIPHERMENT
        )
    return _gloss_lexicon(key, phrase, phrase_citation, lexicon)


def _gloss_lexicon(
    language: str,
    phrase: str,
    phrase_citation: str,
    lexicon: dict[str, _Sense],
) -> GlossReport:
    entries: list[Gloss] = []
    unglossed: list[str] = []
    for token in tokenize(phrase):
        sense = lexicon.get(token.casefold())
        if sense is None:
            unglossed.append(token)
            continue
        entries.append(
            Gloss(
                token=token,
                lemma=sense.lemma,
                part_of_speech=sense.part_of_speech,
                gloss=sense.gloss,
                citation=sense.citation,
                source_url=sense.source_url,
            )
        )
    return GlossReport(
        language=language,
        phrase=phrase,
        phrase_citation=phrase_citation,
        entries=tuple(entries),
        unglossed=tuple(unglossed),
    )


def _gloss_latin(phrase: str, phrase_citation: str) -> GlossReport:
    module = latin_reader_module()
    if module is None:
        raise UnknownLanguageError(
            "Latin is not registered: engine.latin_reader could not be imported. "
            + NOT_A_DECIPHERMENT
        )
    reading = module.read_latin(phrase)
    entries: list[Gloss] = []
    unglossed: list[str] = []
    for item in reading.glosses:
        if not item.known or not item.gloss or not item.source_url:
            unglossed.append(item.form)
            continue
        headword = item.headword or item.lemma or item.form
        entries.append(
            Gloss(
                token=item.form,
                lemma=item.lemma or item.form,
                part_of_speech="",
                gloss=item.gloss,
                citation="Dickinson College Commentaries, " + headword,
                source_url=item.source_url,
            )
        )
    return GlossReport(
        language="latin",
        phrase=phrase,
        phrase_citation=phrase_citation,
        entries=tuple(entries),
        unglossed=tuple(unglossed),
        reading=reading.classical,
    )


def _gloss_egyptian(phrase: str, phrase_citation: str) -> GlossReport:
    module = egyptian_sign_module()
    if module is None:
        raise UnknownLanguageError(
            "Egyptian sign codes are not registered: engine.egyptian is absent. "
            + NOT_A_DECIPHERMENT
        )
    reader = module.get_reader()
    reading = module.read_hieroglyphs(phrase)
    entries = tuple(
        Gloss(
            token=sign.input,
            lemma=sign.code,
            part_of_speech="Gardiner sign",
            gloss=(
                f"{sign.transliteration}: {sign.gloss}"
                if sign.transliteration
                else sign.gloss
            ),
            citation=(
                "Gardiner sign "
                + sign.code
                + ", sourced subset of the Wikipedia list of Egyptian hieroglyphs"
            ),
            source_url=reader.source_url,
        )
        for sign in reading.signs
    )
    return GlossReport(
        language="egyptian",
        phrase=phrase,
        phrase_citation=phrase_citation,
        entries=entries,
        unglossed=(),
        reading=reading.transliteration,
    )
