"""Coptic letter reader for the Unicode Coptic alphabet, plus a tiny cited lexicon.

This reads letters that Unicode already encodes as Coptic. It looks those
spellings up in a three-word lexicon copied from public dictionary pages.
It does not decipher Linear A, the Voynich manuscript, Rongorongo, Indus,
or any other undeciphered script. A character outside the Coptic letter
ranges is reported as unread. It is not given a sound or a meaning.

Letter names come from the Unicode character names (Coptic block and the
Coptic letters that still sit in the Greek and Coptic block):

- https://www.unicode.org/charts/PDF/U2C80.pdf
- https://www.unicode.org/charts/PDF/U0370.pdf

Lexicon rows are Sahidic (or shared-dialect) headwords. Romanization and
English gloss are taken from the cited page, not invented here. Crum page
links are the bibliography those Wiktionary entries give; this file does
not transcribe the scan.

Spellings are written with Unicode escapes so the code points stay obvious:
the tested noun is U+2CA3 U+2CB1 U+2C99 U+2C89 (RO, OOU, MI, EIE).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

# Coptic letters in the Greek and Coptic block, then the Coptic block.
_COPTIC_RANGES = ((0x03E2, 0x03EF), (0x2C80, 0x2CFF))

UNICODE_COPTIC_CHART = "https://www.unicode.org/charts/PDF/U2C80.pdf"
UNICODE_GREEK_AND_COPTIC_CHART = "https://www.unicode.org/charts/PDF/U0370.pdf"

# Wiktionary headwords. Escapes are the real letters, not a private cipher.
ROME = "\u2ca3\u2cb1\u2c99\u2c89"  # ro oou mi eie
ANOK = "\u2c81\u2c9b\u2c9f\u2c95"
SNAU = "\u2ca5\u2c9b\u2c81\u2ca9"
ROME_CAPITAL = "\u2ca2\u2cb0\u2c98\u2c88"


@dataclass(frozen=True)
class CopticLetter:
    """One Unicode Coptic letter."""

    char: str
    name: str
    codepoint: str

    @property
    def known(self) -> bool:
        return True


@dataclass(frozen=True)
class UnreadSign:
    """A character this reader refuses to interpret."""

    char: str
    reason: str

    @property
    def known(self) -> bool:
        return False


@dataclass(frozen=True)
class Lexeme:
    """One dictionary headword. Gloss and romanization are from source_url."""

    word: str
    romanization: str
    gloss: str
    pos: str
    source_url: str
    bibliography: str


@dataclass(frozen=True)
class WordReading:
    """Letters of one token, and a lexicon hit only when the spelling is listed."""

    letters: tuple[CopticLetter | UnreadSign, ...]
    lexeme: Lexeme | None

    @property
    def all_letters_known(self) -> bool:
        return bool(self.letters) and all(item.known for item in self.letters)


# Romanization and gloss checked against the live Wiktionary pages on 2026-10-02.
# ROME noun "human, person": https://en.wiktionary.org/wiki/ + ROME
#   Crum 1939 p. 294: http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=294
# ANOK pronoun "I": Crum 1939 p. 11
#   http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=11
# SNAU numeral "two"
LEXICON: tuple[Lexeme, ...] = (
    Lexeme(
        word=ROME,
        romanization="r\u014dme",
        gloss="human, person",
        pos="noun",
        source_url="https://en.wiktionary.org/wiki/" + ROME,
        bibliography="http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=294",
    ),
    Lexeme(
        word=ANOK,
        romanization="anok",
        gloss="I",
        pos="pronoun",
        source_url="https://en.wiktionary.org/wiki/" + ANOK,
        bibliography="http://coptot.manuscriptroom.com/crum-coptic-dictionary/?pageID=11",
    ),
    Lexeme(
        word=SNAU,
        romanization="snau",
        gloss="two",
        pos="numeral",
        source_url="https://en.wiktionary.org/wiki/" + SNAU,
        bibliography="",
    ),
)

_BY_WORD = {item.word: item for item in LEXICON}


def is_coptic_letter(char: str) -> bool:
    """True when Unicode names this one character as a Coptic letter."""
    if len(char) != 1:
        return False
    code = ord(char)
    if not any(start <= code <= end for start, end in _COPTIC_RANGES):
        return False
    name = unicodedata.name(char, "")
    return name.startswith("COPTIC ") and "LETTER" in name


def coptic_small(char: str) -> str:
    """Map a Coptic capital to the following small letter. Others pass through.

    In both Coptic ranges, Unicode encodes each capital immediately before
    its small partner. The name of that next character is checked so a
    non-pair is not rewritten.
    """
    if len(char) != 1 or not is_coptic_letter(char):
        return char
    name = unicodedata.name(char)
    if "CAPITAL LETTER" not in name:
        return char
    nxt = chr(ord(char) + 1)
    small_name = unicodedata.name(nxt, "")
    if small_name.startswith("COPTIC ") and "SMALL LETTER" in small_name:
        return nxt
    return char


def fold_word(text: str) -> str:
    """NFC, drop whitespace, and lowercase Coptic capitals."""
    folded = unicodedata.normalize("NFC", text)
    return "".join(coptic_small(ch) for ch in folded if not ch.isspace())


def read_letters(text: str) -> tuple[CopticLetter | UnreadSign, ...]:
    """Identify each Coptic letter. Anything else stays unread.

    Whitespace is skipped. Combining marks and non-Coptic signs are returned
    as UnreadSign so a caller cannot mistake them for a transliteration.
    """
    found: list[CopticLetter | UnreadSign] = []
    for char in unicodedata.normalize("NFC", text):
        if char.isspace():
            continue
        if is_coptic_letter(char):
            found.append(
                CopticLetter(
                    char=char,
                    name=unicodedata.name(char),
                    codepoint=f"U+{ord(char):04X}",
                )
            )
            continue
        if unicodedata.combining(char):
            found.append(UnreadSign(char=char, reason="combining_mark"))
        else:
            found.append(UnreadSign(char=char, reason="not_coptic_letter"))
    return tuple(found)


def lookup(word: str) -> Lexeme | None:
    """Return the lexicon row for this spelling, or None. Not a decipherment."""
    return _BY_WORD.get(fold_word(word))


def read_word(word: str) -> WordReading:
    """Read letters and attach a lexicon hit only for a listed headword."""
    return WordReading(letters=read_letters(word), lexeme=lookup(word))


def format_reading(reading: WordReading) -> str:
    """One plain-text line. Unknown signs are marked unread, not guessed."""
    parts: list[str] = []
    for item in reading.letters:
        if isinstance(item, CopticLetter):
            parts.append(f"{item.char} {item.codepoint} {item.name}")
        else:
            parts.append(f"{item.char!r} unread:{item.reason}")
    letter_text = " | ".join(parts) if parts else "(no letters)"
    if reading.lexeme is None:
        return f"{letter_text}\nlexicon: no entry (not a reading of an unknown script)"
    lex = reading.lexeme
    bib = f" bibliography: {lex.bibliography}" if lex.bibliography else ""
    return (
        f"{letter_text}\n"
        f"lexicon: {lex.word} ({lex.romanization}) {lex.pos} '{lex.gloss}' "
        f"source: {lex.source_url}{bib}"
    )
