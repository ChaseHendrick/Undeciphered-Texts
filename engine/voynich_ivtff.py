"""Parse IVTFF transliteration files for the Voynich MS.

The frozen corpus (engine/data/voynich) holds ZL 3b, GC 2a and IT 2a, three
nearly complete transliterations of the Voynich MS, all in IVTFF format 2.0,
fetched byte-exact from voynich.nu on 19 October 2026. This module parses the
file grammar exactly as documented there (R. Zandbergen, IVTFF Format
Definition 2.0.2, 08/07/2025, https://www.voynich.nu/software/ivtt/), and
normalises each locus into words for later comparison across transliterations.

Word counting convention, chosen to match the corpus source's own published
"long words" (words with uncertain spaces not counted): a word is the longest
run of glyphs between definite separators. The definite separators are the
full stop ".", the sequence "<->" and the sequence "<~>", which mark text
interrupted by a drawing element. A comma "," is an uncertain space and does
not count as a separator: it joins two half words into one word, with the
commas removed and the join recorded as a flag. Uncertain readings [a:b]
resolve to the first, most likely option. A high-ascii code @nnn; is one
glyph. One "?" is one unreadable glyph, and any longer run of question marks
counts as a single unknown glyph.

Under this convention the parser reproduces the corpus source's published
counts for all three frozen files exactly: loci 5,385 / 5,367 / 5,215,
paragraphs 740 / 775 / 772, and long words 36,278 / 38,242 / 37,919. GC and
IT each carry one locus marked invalid (f89v2.26, a label that shows through
from the other side of the leaf), which ZL removed.

This module does not propose readings of the manuscript. It reads published
transliteration data and reports what is in the frozen files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data" / "voynich"

FROZEN_FILES = {
    "ZL": "ZL3b-n.txt",
    "GC": "GC2a-n.txt",
    "IT": "IT2a-n.txt",
}

# Page names in the frozen files: f1r through f116v (recto or verso of folio
# number N, split folios 89 and 89-v carry a trailing digit), and the rosette
# fold-out fRos, which only ZL and GC cover.
_PAGE_NAME = r"(?:fRos|f\d+[rv]\d*)"
_PAGE_RE = re.compile(r"^<(%s)>\s*(<!.*>\s*)?$" % _PAGE_NAME)
_LOCUS_RE = re.compile(
    r"^<(%s)\.(\d+),([@+*=~!/&])([A-Z][a-z0-9])(?:;(\w+))?>\s*(.*)$" % _PAGE_NAME
)
_FILE_HEADER_RE = re.compile(r"^#=IVTFF ([A-Za-z0-9-]{4}) (\d+\.\d+) ([MDA])(?: (\S+))?\s*$")
_HIGH_ASCII_RE = re.compile(r"@\d{3};")
_ALT_READING_RE = re.compile(r"\[([^:\]]+)((?::[^:\]]+)+)\]")
_QUESTION_RUN_RE = re.compile(r"\?{3,}")


@dataclass(frozen=True)
class Locus:
    """One transliterated text item on one page."""

    folio: str
    num: int
    locator: str
    locus_type: str
    source_id: str | None
    line_no: int
    raw: str
    words: tuple[str, ...]
    paragraph_start: bool
    paragraph_end: bool
    uncertain_joins: int
    alt_readings: int
    unreadable: tuple[str, ...]
    drawing_gaps: int


@dataclass(frozen=True)
class Page:
    """One page header with its page variables and its loci."""

    name: str
    vars: dict[str, str]
    loci: tuple[Locus, ...]
    line_no: int


@dataclass(frozen=True)
class IVTFFFile:
    """A parsed IVTFF transliteration file."""

    path: str
    alphabet_code: str
    format_version: str
    origin: str
    serial: str
    pages: tuple[Page, ...]
    warnings: tuple[str, ...]

    @property
    def loci(self) -> tuple[Locus, ...]:
        return tuple(locus for page in self.pages for locus in page.loci)

    @property
    def locus_count(self) -> int:
        return sum(len(page.loci) for page in self.pages)

    @property
    def paragraph_count(self) -> int:
        return sum(1 for locus in self.loci if locus.paragraph_start)

    @property
    def long_word_count(self) -> int:
        return sum(len(locus.words) for locus in self.loci)

    @property
    def invalid_loci(self) -> tuple[Locus, ...]:
        """Loci marked as referring to text that does not really exist."""
        return tuple(locus for locus in self.loci if locus.locator == "!")

    def glyph_count(self) -> int:
        """Glyph counts under our own convention, not the corpus source's.

        Each high-ascii code is one glyph, each maximal run of question marks
        is one glyph, and every other character of the file's own alphabet is
        one glyph. The source publishes STA1-based counts instead, so these
        are internal numbers, frozen here for reproducibility.
        """
        total = 0
        for locus in self.loci:
            for word in locus.words:
                work = _HIGH_ASCII_RE.sub("G", word)
                work = _QUESTION_RUN_RE.sub("G", work)
                total += len(work)
        return total


def _resolve_reading(match: re.Match) -> str:
    """The first, most likely option of an uncertain reading."""
    return match.group(1)


def _split_text(raw: str) -> tuple[tuple[str, ...], dict]:
    """Normalise one locus text into words with per-locus flags."""
    flags = {
        "paragraph_start": raw.startswith("<%") or "<%>" in raw,
        "paragraph_end": raw.endswith("<$>") or "<$>" in raw,
        "drawing_gaps": raw.count("<->") + raw.count("<~>"),
        "alt_readings": len(re.findall(r"\[[^:\]]*:[^:\]]*\]", raw)),
        "uncertain_joins": 0,
        "words": (),
    }
    work = raw.replace("<->", ".").replace("<~>", ".")
    work = work.replace("<%>", "").replace("<$>", "")
    work = re.sub(r"<@[^>]*>", "", work)
    work = re.sub(r"<![^>]*>", "", work)
    work = _ALT_READING_RE.sub(_resolve_reading, work)
    flags["unreadable"] = tuple(re.findall(r"\?{3,}", work)) + tuple(
        match for match in re.findall(r"(?<!\?)\?(?!\?)", work)
    )
    words = []
    for token in re.split(r"[.]", work):
        joins = token.count(",")
        flags["uncertain_joins"] += joins
        token = token.replace(",", "")
        # Ligature braces are removed after counting the join flags, matching
        # the corpus source's extraction convention (ivtt ligature mode 1).
        token = token.replace("{", "").replace("}", "")
        if token:
            words.append(token)
    flags["words"] = tuple(words)
    return flags["words"], flags


def _page_vars(line: str) -> dict[str, str]:
    """Page variables $X=y from the page header's dedicated comment."""
    body = re.search(r"<!(.*?)>", line)
    if body is None:
        return {}
    found = {}
    for token in body.group(1).split():
        if token.startswith("$") and "=" in token:
            name, value = token[1:].split("=", 1)
            found[name] = value
    return found


def parse_ivtff_text(text: str) -> IVTFFFile:
    """Parse IVTFF text already in memory (tests and synthetic controls)."""
    file = _parse_lines(text.split("\n"))
    return IVTFFFile(
        path="",
        alphabet_code=file.alphabet_code,
        format_version=file.format_version,
        origin=file.origin,
        serial=file.serial,
        pages=file.pages,
        warnings=file.warnings,
    )


def parse_ivtff(path: str | Path) -> IVTFFFile:
    """Parse one IVTFF file into pages, loci and words."""
    path = Path(path)
    return _parse_lines(path.read_text(encoding="utf-8").split("\n"))


def _parse_lines(lines: list[str]) -> IVTFFFile:
    header_match = _FILE_HEADER_RE.match(lines[0])
    warnings: list[str] = []
    if header_match is None:
        warnings.append(f"unrecognised file header: {lines[0][:60]!r}")
        alphabet_code = version = origin = serial = ""
    else:
        alphabet_code, version, origin, serial = header_match.groups()
        serial = serial or ""
    pages: list[Page] = []
    loci: list[Locus] = []
    page: Page | None = None

    for line_no, line in enumerate(lines[1:], start=2):
        if line.startswith("#") or not line.strip():
            continue
        loci_match = _LOCUS_RE.match(line)
        if loci_match is not None:
            folio, num, locator, locus_type, source_id, body = loci_match.groups()
            words, flags = _split_text(body)
            locus = Locus(
                folio=folio,
                num=int(num),
                locator=locator,
                locus_type=locus_type,
                source_id=source_id,
                line_no=line_no,
                raw=body,
                words=words,
                paragraph_start=bool(flags["paragraph_start"]),
                paragraph_end=bool(flags["paragraph_end"]),
                uncertain_joins=flags["uncertain_joins"],
                alt_readings=flags["alt_readings"],
                unreadable=flags["unreadable"],
                drawing_gaps=flags["drawing_gaps"],
            )
            loci.append(locus)
            if page is None:
                warnings.append(f"line {line_no}: locus before any page header")
            continue
        page_match = _PAGE_RE.match(line)
        if page_match is not None:
            if page is not None and loci:
                pages.append(Page(page.name, page.vars, tuple(loci), page.line_no))
                loci = []
            elif page is not None and not loci:
                pages.append(Page(page.name, page.vars, (), page.line_no))
            page = Page(page_match.group(1), _page_vars(line), (), line_no)
            loci = []
            continue
        warnings.append(f"line {line_no}: unparsed line {line[:30]!r}")
    if page is not None:
        pages.append(Page(page.name, page.vars, tuple(loci), page.line_no))

    return IVTFFFile(
        path="synthetic",
        alphabet_code=alphabet_code,
        format_version=version,
        origin=origin,
        serial=serial,
        pages=tuple(pages),
        warnings=tuple(warnings),
    )


def load(code: str) -> IVTFFFile:
    """Parse one frozen corpus file by its two-letter code."""
    return parse_ivtff(DATA_DIR / FROZEN_FILES[code])


def statistics(file: IVTFFFile) -> dict:
    """The frozen-corpus counts this project computes for one file."""
    return {
        "loci": file.locus_count,
        "pages": len(file.pages),
        "paragraphs": file.paragraph_count,
        "long_words": file.long_word_count,
        "glyphs_our_convention": file.glyph_count(),
        "invalid_loci": len(file.invalid_loci),
        "warnings": len(file.warnings),
        "alphabet_code": file.alphabet_code,
        "format_version": file.format_version,
    }
