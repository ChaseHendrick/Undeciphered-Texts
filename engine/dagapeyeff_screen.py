"""Which languages could give the cells' letter counts? A key-free screen. Not a reading.

A one-to-one letter key, with or without any transposition, keeps letter
counts. For each language, every 196-letter window of real text is given the
fewest single-cell errors that would turn its sorted counts into the cells'
(engine.dagapeyeff_errors). A language whose windows need few errors is worth
a search with its own model; one whose closest window needs many is excluded
for any one-to-one key, whatever the order.

The texts are the sentences of Universal Dependencies treebanks
(https://github.com/UniversalDependencies), fetched into the ignored work/
folder; only counts are stored here. Accents are removed, a few letters are
spelled out (for example ß as SS and þ as TH), Russian is transliterated, and
J is folded into I as in the book's square. Treebank sentences are mixed
genres, so a window can span two sentences.

No letter string is stored.
"""

from __future__ import annotations

import subprocess
import unicodedata
from pathlib import Path

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_foursquare import PLAIN

_WORK = Path(__file__).resolve().parents[1] / "work" / "external" / "ud"
_LETTERS = 196
_MIN_LETTERS = 20_000
_MAX_WINDOWS = 250_000
TREEBANKS = (
    "Afrikaans-AfriBooms", "Albanian-TSA", "Basque-BDT", "Breton-KEB", "Catalan-AnCora", "Croatian-SET",
    "Czech-FicTree", "Danish-DDT", "Dutch-Alpino", "Estonian-EWT", "Faroese-FarPaHC", "Finnish-TDT",
    "French-GSD", "Galician-CTG", "German-GSD", "Hausa-NorthernAutogramm", "Hungarian-Szeged", "Icelandic-Modern",
    "Indonesian-GSD", "Irish-IDT", "Latin-ITTB", "Latin-Perseus", "Latvian-LVTB", "Lithuanian-ALKSNIS",
    "Maltese-MUDT", "Naija-NSC", "Norwegian-Bokmaal", "Polish-LFG", "Portuguese-Bosque", "Romanian-RRT",
    "Russian-GSD", "Scottish_Gaelic-ARCOSG", "Slovenian-SSJ", "Spanish-GSD", "Swedish-Talbanken",
    "Tagalog-TRG", "Turkish-IMST", "Vietnamese-VTB", "Welsh-CCG", "Wolof-WTB", "Yoruba-YTB",
)
_SPELLED = {"ß": "SS", "Æ": "AE", "Œ": "OE", "Ø": "O", "Ð": "D", "Þ": "TH", "Ł": "L", "Đ": "D", "Ħ": "H",
            "İ": "I", "ı": "I", "Ŋ": "N", "Ə": "E", "Ɓ": "B", "Ɗ": "D", "Ƙ": "K", "Ƴ": "Y"}
# A plain British-style transliteration, the kind an English reader of 1939 would meet.
_RUSSIAN = {
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "E", "Ж": "ZH", "З": "Z", "И": "I",
    "Й": "I", "К": "K", "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T",
    "У": "U", "Ф": "F", "Х": "KH", "Ц": "TS", "Ч": "CH", "Ш": "SH", "Щ": "SHCH", "Ъ": "", "Ы": "Y", "Ь": "",
    "Э": "E", "Ю": "YU", "Я": "YA",
}


def fold(text: str) -> str:
    """Letters A to Z, J folded into I."""
    out = []
    for ch in text.upper():
        if ch in _RUSSIAN:
            out.append(_RUSSIAN[ch])
            continue
        if ch in _SPELLED:
            out.append(_SPELLED[ch])
            continue
        for part in unicodedata.normalize("NFD", ch):
            if "A" <= part <= "Z":
                out.append(part)
    return "".join(out).replace("J", "I")


def _fetch(name: str) -> Path:
    folder = _WORK / f"UD_{name}"
    if not (folder / ".git").exists():
        _WORK.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        f"https://github.com/UniversalDependencies/UD_{name}", str(folder)], check=True)
    return folder


def text_of(name: str) -> str:
    sentences = []
    for path in sorted(_fetch(name).glob("*.conllu")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# text = "):
                sentences.append(line[len("# text = "):])
    return fold(" ".join(sentences))


def screen(letters: str, target: np.ndarray) -> dict:
    ints = np.asarray([PLAIN.index(ch) for ch in letters])
    stride = max(1, (len(ints) - _LETTERS) // _MAX_WINDOWS + 1)
    starts = np.arange(0, len(ints) - _LETTERS + 1, stride)
    counts = np.zeros((len(starts), 25), dtype=np.int64)
    for letter in range(25):
        running = np.concatenate([[0], np.cumsum(ints == letter)])
        counts[:, letter] = running[starts + _LETTERS] - running[starts]
    fewest = np.abs(-np.sort(-counts, axis=1) - target).sum(axis=1) // 2
    distinct = (counts > 0).sum(axis=1)
    largest = counts.max(axis=1)
    return {
        "letters": len(letters),
        "windows": int(len(starts)),
        "stride": int(stride),
        "fewest_errors": int(fewest.min()),
        "median_errors": float(np.median(fewest)),
        "within_4": int((fewest <= 4).sum()),
        "within_8": int((fewest <= 8).sum()),
        "distinct_at_most_18": int((distinct <= 18).sum()),
        "largest_at_most_20": int((largest <= 20).sum()),
    }


@frozen("dagapeyeff-screen")
def screen_report() -> dict:
    target = sorted_counts(_cells())
    rows = {}
    small = []
    for name in TREEBANKS:
        letters = text_of(name)
        if len(letters) < _MIN_LETTERS:
            small.append({"treebank": name, "letters": len(letters)})
            continue
        rows[name] = screen(letters, target)
    ranked = sorted(rows, key=lambda name: (rows[name]["fewest_errors"], rows[name]["median_errors"]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": "https://github.com/UniversalDependencies, sentences of each treebank's .conllu files",
        "languages": rows,
        "too_small": small,
        "ranked": ranked,
        "closest": {"treebank": ranked[0], **rows[ranked[0]]},
    }
