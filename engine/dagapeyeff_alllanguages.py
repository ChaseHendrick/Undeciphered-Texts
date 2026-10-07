"""Every language in Universal Dependencies against the cells' letter counts. A key-free screen. Not a reading.

engine.dagapeyeff_screen screened 39 languages. This screen takes one treebank
for every language that Universal Dependencies lists with at least 5,000 tokens:
for each language the largest treebank of at most 1.5 million tokens, as listed
on https://universaldependencies.org/ on 6 October 2026 (TREEBANKS below). Each
is fetched into a temporary folder, counted and deleted, unless an earlier
probe already keeps it in the ignored work/ folder.

Texts in the Latin alphabet are folded as in the screen: accents removed, a few
letters spelled out, J folded into I. Texts in the Cyrillic, Greek, Armenian,
Georgian, Coptic and Gothic alphabets are romanized letter by letter with the
unidecode package (Russian then reads much as in the screen's British style).
Scripts without separate letters for vowels, or with signs for syllables or
words (Arabic, Hebrew, Indic scripts, Chinese, Japanese, Korean, Thai,
cuneiform, hieroglyphs), are not romanized: a romanization would invent the
letters that are counted, so they are listed as skipped. A text under 20,000
letters is skipped too.

The count is the screen's: the fewest single-cell errors that turn a 196-letter
window into the cells' counts, under any one-to-one key and any order. Only
counts are stored. No letter string is stored.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_screen import _MIN_LETTERS, _WORK, fold, screen

TREEBANKS = (
    "Abkhaz-AbNC", "Afrikaans-AfriBooms", "Akkadian-MCONG", "Alemannic-DIVITAL", "Amharic-ATT",
    "Ancient_Greek-PROIEL", "Ancient_Hebrew-PTNK", "Arabic-NYUAD", "Armenian-ArmTDP", "Bambara-CRB",
    "Basque-BDT", "Bavarian-MaiBaam", "Beja-Autogramm", "Belarusian-HSE", "Bhojpuri-BHTB",
    "Bororo-BDT", "Breton-KEB", "Bulgarian-BTB", "Buryat-BDT", "Cantonese-HK",
    "Catalan-AnCora", "Chinese-GSDSimp", "Chintang-CTNTB", "Chukchi-HSE", "Classical_Armenian-CAVaL",
    "Classical_Chinese-Kyoto", "Coptic-Scriptorium", "Croatian-SET", "Czech-CAC", "Danish-DDT",
    "Dutch-LassySmall", "Egyptian-PC", "English-CHILDES", "Erzya-JR", "Estonian-EDT",
    "Faroese-FarPaHC", "Finnish-TDT", "French-FTB", "Frisian-Frysk", "Galician-CTG",
    "Georgian-GLC", "German-GSD", "Gheg-GPS", "Gothic-PROIEL", "Greek-GDT",
    "Guajajara-TuDeT", "Haitian_Creole-Adolphe", "Hausa-NorthernAutogramm", "Hebrew-HTB", "Highland_Puebla_Nahuatl-ITML",
    "Hindi-HDTB", "Hindi_English-HIENCS", "Hungarian-Szeged", "Icelandic-IcePaHC", "Ika-ChibErgIS",
    "Indonesian-GSD", "Irish-IDT", "Italian-ISDT", "Japanese-BCCWJ", "Javanese-CSUI",
    "Kabyle-ADPT", "Kazakh-KTB", "Khoekhoe-KDT", "Kiche-IU", "Komi_Zyrian-Lattice",
    "Korean-Kaist", "Kyrgyz-KTMU", "Latin-ITTB", "Latvian-LVTB", "Ligurian-GLT",
    "Lithuanian-ALKSNIS", "Low_Saxon-LSDC", "Magahi-MGTB", "Maghrebi_Arabic_French-Arabizi", "Maltese-MUDT",
    "Manx-Cadhan", "Marathi-CMUPAN", "Mbya_Guarani-Dooley", "Middle_French-PROFITEROLE", "Naija-NSC",
    "Nheengatu-CompLin", "North_Sami-Giella", "Northern_Kurdish-Kurmanji", "Norwegian-Bokmaal", "Occitan-TTB",
    "Odia-ODTB", "Old_Church_Slavonic-PROIEL", "Old_East_Slavic-TOROT", "Old_English-OEDT", "Old_French-PROFITEROLE",
    "Old_Georgian-GLC", "Old_Occitan-CorAG", "Ottoman_Turkish-DUDU", "Pashto-Sikaram", "Persian-PerDT",
    "Polish-PDB", "Pomak-Philotis", "Portuguese-CINTIL", "Punjabi-PunTB", "Romanian-Nonstandard",
    "Russian-GSD", "Ruuli-RDT", "Sanskrit-Vedic", "Scottish_Gaelic-ARCOSG", "Serbian-SET",
    "Shanghainese-ShUD", "Sicilian-STB", "Sindhi-Isra", "Slovak-SNK", "Slovenian-SSJ",
    "Spanish-AnCora", "Swedish-LinES", "Tagalog-NewsCrawl", "Tamil-TTB", "Telugu-MTG",
    "Thai-TUD", "Turkish-Penn", "Turkish_German-SAGT", "Turkmen-TUD", "Ukrainian-IU",
    "Upper_Sorbian-UFAL", "Urdu-UDTB", "Uspanteko-MesoTree", "Uyghur-UDT", "Uzbek-UzUDT",
    "Vietnamese-VTB", "Welsh-CCG", "Western_Armenian-ArmTDP", "Western_Sierra_Puebla_Nahuatl-MesoTree", "Wolof-WTB",
    "Xibe-XDT", "Yiddish-YiTB", "Yoruba-YTB", "Zaar-Autogramm",
)
_ALPHABETS = ("LATIN", "CYRILLIC", "GREEK", "ARMENIAN", "GEORGIAN", "COPTIC", "GOTHIC")


def _sentences(folder: Path) -> str:
    out = []
    for path in sorted(folder.glob("*.conllu")):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# text = "):
                out.append(line[len("# text = "):])
    return " ".join(out)


def _text(name: str) -> str:
    kept = _WORK / f"UD_{name}"
    if (kept / ".git").exists():
        return _sentences(kept)
    temporary = Path(tempfile.mkdtemp(prefix="ud-"))
    try:
        subprocess.run(["git", "clone", "--quiet", "--depth", "1",
                        f"https://github.com/UniversalDependencies/UD_{name}", str(temporary / "tb")], check=True)
        return _sentences(temporary / "tb")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def script(text: str) -> str:
    """The script of most letters: the first word of their Unicode names."""
    counts: dict[str, int] = {}
    for ch in text[:200_000]:
        if ch.isalpha():
            name = unicodedata.name(ch, "UNKNOWN").split(" ")[0]
            counts[name] = counts.get(name, 0) + 1
    return max(counts, key=counts.get) if counts else "NONE"


def letters(text: str, kind: str) -> str:
    if kind == "LATIN":
        return fold(text)
    from unidecode import unidecode

    return fold(unidecode(text))


@frozen("dagapeyeff-alllanguages")
def alllanguages_report() -> dict:
    target = sorted_counts(_cells())
    rows, skipped = {}, []
    for name in TREEBANKS:
        text = _text(name)
        kind = script(text)
        if kind == "NONE":
            skipped.append({"treebank": name, "reason": "no sentence text in the treebank"})
            continue
        if kind not in _ALPHABETS:
            skipped.append({"treebank": name, "reason": f"script {kind.lower()} is not romanized"})
            continue
        folded = letters(text, kind)
        if len(folded) < _MIN_LETTERS:
            skipped.append({"treebank": name, "reason": f"{len(folded)} letters"})
            continue
        row = screen(folded, target)
        rows[name] = {"script": kind.lower(), **row,
                      "within_8_per_million_windows": round(1e6 * row["within_8"] / row["windows"], 1)}
    ranked = sorted(rows, key=lambda name: (rows[name]["fewest_errors"], rows[name]["median_errors"]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": "https://universaldependencies.org/ treebanks, sentences of each .conllu file",
        "languages": rows,
        "skipped": skipped,
        "ranked": ranked,
        "closest": {"treebank": ranked[0], **rows[ranked[0]]},
    }
