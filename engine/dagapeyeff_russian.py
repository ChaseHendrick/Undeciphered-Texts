"""Does Russian come closer under another transliteration? A key-free screen. Not a reading.

engine.dagapeyeff_screen transliterated Russian one way, in a plain British
style, and found it needs 13 errors at its closest window. D'Agapeyeff was
born in Russia, so the choice matters: a writer putting Russian on a 25-letter
square has to pick a spelling, and digraphs such as ZH, KH and SHCH move the
letter counts. This screen repeats the count for four spellings and three
treebanks: the British style, one Latin letter for each Cyrillic letter (ISO 9
with its accents removed), a German style and a French style.

The texts are the sentences of Universal Dependencies treebanks, fetched into
the ignored work/ folder by engine.dagapeyeff_screen; only counts are stored.

No letter string is stored.
"""

from __future__ import annotations

import unicodedata

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_screen import _RUSSIAN, _SPELLED, _fetch, screen

TREEBANKS = ("Russian-GSD", "Russian-SynTagRus", "Russian-Taiga")

_ONE_LETTER = {
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "E", "Ж": "Z", "З": "Z", "И": "I",
    "Й": "I", "К": "K", "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T",
    "У": "U", "Ф": "F", "Х": "H", "Ц": "C", "Ч": "C", "Ш": "S", "Щ": "S", "Ъ": "", "Ы": "Y", "Ь": "",
    "Э": "E", "Ю": "U", "Я": "A",
}
_GERMAN = {
    **_RUSSIAN, "В": "W", "Ж": "SCH", "З": "S", "Й": "J", "Х": "CH", "Ц": "Z", "Ч": "TSCH", "Ш": "SCH",
    "Щ": "SCHTSCH", "Ю": "JU", "Я": "JA",
}
_FRENCH = {
    **_RUSSIAN, "Ж": "J", "Ц": "TS", "Ч": "TCH", "Ш": "CH", "Щ": "CHTCH", "У": "OU", "Ю": "IOU", "Я": "IA",
}
SCHEMES = {"british": _RUSSIAN, "one-letter": _ONE_LETTER, "german": _GERMAN, "french": _FRENCH}


def fold(text: str, scheme: str) -> str:
    """Letters A to Z under one Russian spelling, J folded into I."""
    table = SCHEMES[scheme]
    out = []
    for ch in text.upper():
        if ch in table:
            out.append(table[ch])
            continue
        if ch in _SPELLED:
            out.append(_SPELLED[ch])
            continue
        for part in unicodedata.normalize("NFD", ch):
            if "A" <= part <= "Z":
                out.append(part)
    return "".join(out).replace("J", "I")


def _sentences(name: str) -> str:
    sentences = []
    for path in sorted(_fetch(name).glob("*.conllu")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# text = "):
                sentences.append(line[len("# text = "):])
    return " ".join(sentences)


@frozen("dagapeyeff-russian")
def russian_report() -> dict:
    target = sorted_counts(_cells())
    rows = {}
    for name in TREEBANKS:
        raw = _sentences(name)
        for scheme in SCHEMES:
            rows[f"{name} {scheme}"] = {"treebank": name, "scheme": scheme, **screen(fold(raw, scheme), target)}
    closest = min(rows, key=lambda key: (rows[key]["fewest_errors"], rows[key]["median_errors"]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": "https://github.com/UniversalDependencies, sentences of each treebank's .conllu files",
        "rows": rows,
        "closest": {"row": closest, **rows[closest]},
        "fewest_errors": rows[closest]["fewest_errors"],
        "windows_within_8": sum(row["within_8"] for row in rows.values()),
    }
