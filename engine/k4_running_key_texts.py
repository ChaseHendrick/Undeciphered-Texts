"""K4 running keys from texts other than K3: exact clue scan plus an English-key check.

A running key never repeats, so a key text either places the two public clues
or it does not. For each of twelve tableaux (Vigenere c = p + k, Beaufort
c = k - p, variant Beaufort c = p - k, each on A-Z and on the KRYPTOS,
PALIMPSEST and ABSCISSA keyed alphabets in the K1/K2 sense
c = A[(A^-1 p + A^-1 k) mod 26]) the clues EASTNORTHEAST at 21 and
BERLINCLOCK at 63 fix 24 key letters at positions 21..33 and 63..73.

``scan_text`` looks for every offset o where a key text, read forwards or
backwards, has exactly those 24 letters at o+21..o+33 and o+63..o+73. Only the
clue letters are used, so the scan holds whatever language K4's plaintext is
in. It also reports the best partial match and the maximum expected by chance
(Poisson binomial with the text's own letter rates, plus one seeded shuffle).

``english_fragment_check`` asks a source-agnostic question: if the key is
English prose from any source, the 13-letter and 11-letter key fragments,
42 letters apart, must score like English. The null is every aligned pair at
that separation in engine/data/neural_train_public.txt. The threshold is the
1st percentile of that null, fixed in ``THRESHOLD_PERCENTILE`` before K4 is
scored. A planted English running key on held-out text is the power control.
An exclusion at that threshold is statistical, not exact.

Key texts are frozen in ``FROZEN_SOURCES`` by URL and SHA-256 of the
letters-only text. Large texts are fetched into the git-ignored work/ folder
and are not vendored. Downloaded files are read as text only.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import bisect
import hashlib
import json
import math
import random
import time
import unicodedata
from functools import lru_cache
from pathlib import Path

from engine.alphabet import ALPHABET
from engine.k4_gromark_obstruction import CRIB_SPANS, KEYWORDS
from engine.solvers.columnar import KRYPTOS_K3_CIPHERTEXT, KRYPTOS_K3_PLAINTEXT
from engine.solvers.k4_attempt import K4_CIPHERTEXT

_ROOT = Path(__file__).resolve().parent.parent
_DATA = Path(__file__).resolve().parent / "data"
DEFAULT_WORK_DIR = _ROOT / "work" / "k4_running_key_texts"

RULES = ("vigenere", "beaufort", "variant_beaufort")
ALPHABET_KEYWORDS = ("AZ",) + KEYWORDS
WINDOW = 97
# Highest clue position plus one: a key text needs this many letters past o.
SPAN_END = max(start + len(word) for start, word in CRIB_SPANS)
THRESHOLD_PERCENTILE = 1.0
SHUFFLE_SEED = 20261018
_FULL_MATCH_CAP = 20

# German letters are spelled out before accents are dropped.
_TRANSLIT = {"Ä": "AE", "Ö": "OE", "Ü": "UE", "ß": "SS", "ẞ": "SS"}


def normalize_letters(text: str) -> str:
    """Uppercase A-Z only. AE OE UE SS for German letters, accents dropped."""
    out: list[str] = []
    for ch in text.upper():
        if ch in _TRANSLIT:
            out.append(_TRANSLIT[ch])
            continue
        if "A" <= ch <= "Z":
            out.append(ch)
            continue
        if ch.isalpha():
            base = unicodedata.normalize("NFKD", ch)
            out.extend(b for b in base if "A" <= b <= "Z")
    return "".join(out)


def sha256_letters(letters: str) -> str:
    return hashlib.sha256(letters.encode("ascii")).hexdigest()


# --------------------------------------------------------------------------
# Tableaux


def keyed_alphabet(keyword: str) -> str:
    """Keyword letters first, then the unused letters in A-Z order."""
    if keyword == "AZ":
        return ALPHABET
    seen: list[str] = []
    for ch in normalize_letters(keyword) + ALPHABET:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def tableaux() -> tuple[tuple[str, str, str], ...]:
    """(name, rule, alphabet) for the twelve tableaux, in a fixed order."""
    rows = []
    for rule in RULES:
        for word in ALPHABET_KEYWORDS:
            rows.append((f"{rule}/{word}", rule, keyed_alphabet(word)))
    return tuple(rows)


def _index(alphabet: str) -> dict[str, int]:
    return {ch: i for i, ch in enumerate(alphabet)}


def encrypt_letter(rule: str, alphabet: str, p: str, k: str) -> str:
    inv = _index(alphabet)
    if rule == "vigenere":
        return alphabet[(inv[p] + inv[k]) % 26]
    if rule == "beaufort":
        return alphabet[(inv[k] - inv[p]) % 26]
    if rule == "variant_beaufort":
        return alphabet[(inv[p] - inv[k]) % 26]
    raise ValueError(f"unknown rule {rule}")


def decrypt_letter(rule: str, alphabet: str, c: str, k: str) -> str:
    inv = _index(alphabet)
    if rule == "vigenere":
        return alphabet[(inv[c] - inv[k]) % 26]
    if rule == "beaufort":
        return alphabet[(inv[k] - inv[c]) % 26]
    if rule == "variant_beaufort":
        return alphabet[(inv[c] + inv[k]) % 26]
    raise ValueError(f"unknown rule {rule}")


def key_letter(rule: str, alphabet: str, c: str, p: str) -> str:
    """The one key letter that sends plaintext p to ciphertext c."""
    inv = _index(alphabet)
    if rule == "vigenere":
        return alphabet[(inv[c] - inv[p]) % 26]
    if rule == "beaufort":
        return alphabet[(inv[c] + inv[p]) % 26]
    if rule == "variant_beaufort":
        return alphabet[(inv[p] - inv[c]) % 26]
    raise ValueError(f"unknown rule {rule}")


def encrypt(rule: str, alphabet: str, plain: str, key: str) -> str:
    if len(key) < len(plain):
        raise ValueError("a running key is not repeated")
    return "".join(encrypt_letter(rule, alphabet, p, k) for p, k in zip(plain, key))


def decrypt(rule: str, alphabet: str, cipher: str, key: str) -> str:
    """Decrypt; a '?' key letter (past the end of a key text) gives '?'."""
    out = []
    for c, k in zip(cipher, key):
        out.append("?" if k == "?" else decrypt_letter(rule, alphabet, c, k))
    return "".join(out)


def required_key(
    rule: str, alphabet: str, ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS
) -> tuple[tuple[int, str], ...]:
    """(position, key letter) fixed by each clue letter."""
    out = []
    for start, word in spans:
        for j, p in enumerate(word):
            pos = start + j
            out.append((pos, key_letter(rule, alphabet, ciphertext[pos], p)))
    return tuple(out)


def key_fragments(required: tuple[tuple[int, str], ...], spans=CRIB_SPANS) -> tuple[str, ...]:
    """The key letters grouped by clue span."""
    lookup = dict(required)
    return tuple(
        "".join(lookup[start + j] for j in range(len(word))) for start, word in spans
    )


# --------------------------------------------------------------------------
# Exact scan


def _indicator_ints(letters: str, needed: set[str]) -> dict[str, int]:
    """One byte per text letter: 1 where it equals the letter, else 0.

    Stored as a little-endian integer so a right shift by 8*pos lines text
    position o+pos up with o. Sums of 24 such bytes stay below 256.
    """
    raw = letters.encode("ascii")
    out = {}
    for letter in needed:
        table = bytes(1 if i == ord(letter) else 0 for i in range(256))
        out[letter] = int.from_bytes(raw.translate(table), "little")
    return out


def _match_counts(
    length: int, indicators: dict[str, int], required: tuple[tuple[int, str], ...]
) -> bytes:
    """Byte o is the number of required key letters matched at offset o."""
    offsets = length - SPAN_END + 1
    if offsets <= 0:
        return b""
    total = 0
    for pos, letter in required:
        total += indicators[letter] >> (8 * pos)
    return total.to_bytes(length, "little")[:offsets]


def _poisson_binomial(probs: list[float]) -> list[float]:
    dist = [1.0]
    for p in probs:
        nxt = [0.0] * (len(dist) + 1)
        for m, q in enumerate(dist):
            nxt[m] += q * (1.0 - p)
            nxt[m + 1] += q * p
        dist = nxt
    return dist


def chance_max(probs: list[float], trials: int) -> dict:
    """Expected maximum of ``trials`` independent Poisson-binomial counts."""
    dist = _poisson_binomial(probs)
    tails = [sum(dist[m:]) for m in range(len(dist))]

    def p_max_at_least(m: int) -> float:
        tail = min(max(tails[m], 0.0), 1.0)
        if tail >= 1.0:
            return 1.0
        return -math.expm1(trials * math.log1p(-tail))

    expected = sum(p_max_at_least(m) for m in range(1, len(dist)))
    return {"expected_max": expected, "p_max_at_least": p_max_at_least, "tails": tails}


def scan_text(
    letters: str,
    required: tuple[tuple[int, str], ...],
    *,
    backwards: bool = True,
    shuffle_seed: int | None = SHUFFLE_SEED,
    indicator_cache: dict | None = None,
) -> dict:
    """Every offset where the key text holds all required key letters.

    Offsets are counted in the direction read. For a backwards read, the key
    letter at position i is letters[forward_start - i] with
    forward_start = len(letters) - 1 - offset.
    """
    n = len(letters)
    needed = {letter for _, letter in required}
    cache = indicator_cache if indicator_cache is not None else {}
    directions = [("forward", letters)]
    if backwards:
        directions.append(("backward", letters[::-1]))
    full: list[dict] = []
    best = -1
    best_at: list[dict] = []
    offsets_total = 0
    for name, text in directions:
        key = (name, "text")
        have = cache.setdefault(key, {})
        missing = needed - set(have)
        if missing:
            have.update(_indicator_ints(text, missing))
        counts = _match_counts(n, have, required)
        offsets_total += len(counts)
        if not counts:
            continue
        top = max(counts)
        if top > best:
            best = top
            best_at = []
        if top == best:
            start = 0
            while len(best_at) < 5:
                o = counts.find(bytes([top]), start)
                if o < 0:
                    break
                best_at.append({"direction": name, "offset": o})
                start = o + 1
        start = 0
        target = bytes([len(required)])
        while True:
            o = counts.find(target, start)
            if o < 0:
                break
            full.append({"direction": name, "offset": o})
            start = o + 1
    probs_rate = _letter_rates(letters)
    chance = None
    if offsets_total:
        stats = chance_max([probs_rate[letter] for _, letter in required], offsets_total)
        chance = {
            "expected_max": round(stats["expected_max"], 3),
            "p_max_at_least_best": (
                stats["p_max_at_least"](best) if best >= 0 else None
            ),
        }
    shuffle_best = None
    if shuffle_seed is not None and offsets_total:
        key = ("shuffle", shuffle_seed)
        if key not in cache:
            chars = list(letters)
            random.Random(shuffle_seed).shuffle(chars)
            shuffled = "".join(chars)
            cache[key] = {"text": shuffled, "fwd": {}, "bwd": {}}
        entry = cache[key]
        shuffle_best = 0
        for slot, text in (("fwd", entry["text"]), ("bwd", entry["text"][::-1]))[
            : 2 if backwards else 1
        ]:
            have = entry[slot]
            missing = needed - set(have)
            if missing:
                have.update(_indicator_ints(text, missing))
            counts = _match_counts(n, have, required)
            if counts:
                shuffle_best = max(shuffle_best, max(counts))
    return {
        "letters": n,
        "offsets_scanned": offsets_total,
        "full_matches": full,
        "best_partial": best if best >= 0 else None,
        "best_partial_at": best_at,
        "chance": chance,
        "shuffle_best": shuffle_best,
    }


def _letter_rates(letters: str) -> dict[str, float]:
    n = max(len(letters), 1)
    return {ch: letters.count(ch) / n for ch in ALPHABET}


def key_window(letters: str, direction: str, offset: int, length: int = WINDOW) -> str:
    """Key letters from a scan hit, padded with '?' past the end of the text."""
    text = letters if direction == "forward" else letters[::-1]
    seg = text[offset : offset + length]
    return seg + "?" * (length - len(seg))


# --------------------------------------------------------------------------
# Frozen sources

_KRYPTOS_URL = "https://en.wikipedia.org/wiki/Kryptos"


def _certificate(name: str) -> dict:
    return json.loads((_DATA / name).read_text(encoding="utf-8"))


def _repo_text(name: str) -> str:
    """A repo data file without its '#' provenance header lines."""
    raw = (_DATA / name).read_text(encoding="utf-8")
    return "\n".join(line for line in raw.splitlines() if not line.startswith("#"))


def repo_sources() -> dict[str, str]:
    """Key texts already in the repo, letters only. No network needed."""
    k1 = _certificate("kryptos_k1_certificate.json")
    k2 = _certificate("kryptos_k2_certificate.json")
    k1p = normalize_letters(k1["plaintext"])
    k2p = normalize_letters(k2["plaintext"])
    k3p = normalize_letters(KRYPTOS_K3_PLAINTEXT)
    k1c = normalize_letters(k1["ciphertext"])
    k2c = normalize_letters(k2["ciphertext"])
    k3c = normalize_letters(KRYPTOS_K3_CIPHERTEXT)
    return {
        "kryptos_k1_plaintext": k1p,
        "kryptos_k2_plaintext": k2p,
        "kryptos_k3_plaintext": k3p,
        "kryptos_k1k2k3_plaintext": k1p + k2p + k3p,
        "kryptos_k1k2k3_ciphertext": k1c + k2c + k3c,
        "neural_heldout_doyle": normalize_letters(_repo_text("neural_heldout_doyle.txt")),
        "neural_train_public": normalize_letters(
            (_DATA / "neural_train_public.txt").read_text(encoding="utf-8")
        ),
    }


_GB = "https://www.gutenberg.org/cache/epub/{0}/pg{0}.txt"
_IA = "https://archive.org/download/{0}/{0}_djvu.txt"

# Frozen 2026-10-18. letters_sha256 is over normalize_letters() of the
# extracted text. raw_sha256 is over the downloaded bytes. "gutenberg"
# extraction keeps the lines between the *** START OF and *** END OF markers.
FROZEN_SOURCES: tuple[dict, ...] = (
    # Repo texts. URL is the cited source of the published plaintext.
    {"name": "kryptos_k1_plaintext", "origin": "repo", "language": "en",
     "url": _KRYPTOS_URL, "where": "engine/data/kryptos_k1_certificate.json",
     "letters": 63, "letters_sha256":
     "a4a581f02185ae92d52bbf55113cb59e73a2914f24af2634ffdb33c1d4988c15"},
    {"name": "kryptos_k2_plaintext", "origin": "repo", "language": "en",
     "url": _KRYPTOS_URL, "where": "engine/data/kryptos_k2_certificate.json",
     "letters": 370, "letters_sha256":
     "cb5420f5cd5e8def287353d8522a79bb066a76c083746d56f4fed85e23a5a165"},
    {"name": "kryptos_k3_plaintext", "origin": "repo", "language": "en",
     "url": _KRYPTOS_URL, "where": "engine.solvers.columnar.KRYPTOS_K3_PLAINTEXT",
     "letters": 336, "letters_sha256":
     "ea07f4ff5bc4ffcf6cd2a3e33263d25543ea81d1089ed9a413021d75db46aafc"},
    {"name": "kryptos_k1k2k3_plaintext", "origin": "repo", "language": "en",
     "url": _KRYPTOS_URL, "where": "K1 + K2 + K3 plaintexts in sculpture order",
     "letters": 769, "letters_sha256":
     "d6867c975d1150ebe529abf3027da24353fda20bff4a310e51f3e51f2044008c"},
    {"name": "kryptos_k1k2k3_ciphertext", "origin": "repo", "language": "none",
     "url": _KRYPTOS_URL, "where": "K1 + K2 + K3 ciphertexts in sculpture order",
     "letters": 769, "letters_sha256":
     "df59b0c4d29a0493e2ff39061e006128700e2fb0c83cfa331676431ab675e16b"},
    {"name": "neural_heldout_doyle", "origin": "repo", "language": "en",
     "url": _GB.format(1661), "where": "engine/data/neural_heldout_doyle.txt",
     "letters": 7314, "letters_sha256":
     "cbee687d0c9465488180c158b20542777681e2b1900ca4015caa9d25aaba162a"},
    {"name": "neural_train_public", "origin": "repo", "language": "en",
     "url": "engine/data/neural_train_public.txt (public-domain training prose)",
     "where": "engine/data/neural_train_public.txt",
     "letters": 1916398, "letters_sha256":
     "8ec4db841fced52b112282e6fbe0f9aee89e38af3d371b9b43b1b620203326fb"},
    # Fetched texts, stored under work/k4_running_key_texts/raw/.
    {"name": "carter_tomb_vol1_1923_ocr", "origin": "fetch", "language": "en",
     "url": _IA.format("tomboftutankhame00cart_1"), "file": "carter_v1_ocr.txt",
     "extraction": "whole", "letters": 284914, "letters_sha256":
     "2e398a0b57f6ce5f0d16710e968fd4da7fa5662981474212a345376b7d996865",
     "raw_sha256":
     "05e90d80a0e4469f523156381764c219b571c656d83360fed2dfabbbdaf12f46"},
    {"name": "carter_tomb_vol2_1927_ocr", "origin": "fetch", "language": "en",
     "url": _IA.format("tomboftutankhame02cart"), "file": "carter_v2_ocr.txt",
     "extraction": "whole", "letters": 351185, "letters_sha256":
     "4bbcb5dacadb6e6575409e15bb26188f5307ed3d2676fb83b20fc26abb731a75",
     "raw_sha256":
     "c5862e1086add937f2359936d60415c8ca13d94ede918190129db2d2f7d3f755"},
    {"name": "declaration_of_independence", "origin": "fetch", "language": "en",
     "url": _GB.format(1), "file": "pg1.txt", "extraction": "gutenberg",
     "letters": 8448, "letters_sha256":
     "6cb6c0a224a7f53c90be6b724bd7f120603a98b0ba44d7a0ca7ce64cb0a4a872", "raw_sha256":
     "8fc7483413518ecf182d982a2e61289894e7fa3ccb1fa3d1db4c1be55debb1f0"},
    {"name": "us_constitution", "origin": "fetch", "language": "en",
     "url": _GB.format(5), "file": "pg5.txt", "extraction": "gutenberg",
     "letters": 22328, "letters_sha256":
     "a392b34ff2b774d97baf04997fc7c360ca56d2ef952e22c0554dea83c0e8c37a", "raw_sha256":
     "d177168e3f4898213dced30fbbe60d74ad08e884ed5dd86bff94a1b8836b5982"},
    {"name": "king_james_bible", "origin": "fetch", "language": "en",
     "url": _GB.format(10), "file": "pg10.txt", "extraction": "gutenberg",
     "letters": 3225906, "letters_sha256":
     "b6c30fd38555f0b6be949eef7ceacfdd8fe96309b60d3a4563071649f886f049", "raw_sha256":
     "0204adaed1f25700aa854218cae63c7172228c41088f335e99167a071eed83c0"},
    {"name": "pride_and_prejudice", "origin": "fetch", "language": "en",
     "url": _GB.format(1342), "file": "pg1342.txt", "extraction": "gutenberg",
     "letters": 563939, "letters_sha256":
     "47619b437e5e71f4b126ff803f4be493903e2aca6fe1b1440d14b99d89f8c03c", "raw_sha256":
     "3f6bb9d6f78e0293b56acd4714dd68cb7d6d1d293402031ce9d5a216bcaf9d75"},
    {"name": "moby_dick", "origin": "fetch", "language": "en",
     "url": _GB.format(2701), "file": "pg2701.txt", "extraction": "gutenberg",
     "letters": 955178, "letters_sha256":
     "e2140a13eb2a68c575e21428a0b6d3773c05e4c0f6f9f93d7de1af7ea320c1be", "raw_sha256":
     "b5e88b71a1cda068e9ab1d94344c9d932338ba6da1a66def97a1aecd9cfcc87d"},
    {"name": "tale_of_two_cities", "origin": "fetch", "language": "en",
     "url": _GB.format(98), "file": "pg98.txt", "extraction": "gutenberg",
     "letters": 584912, "letters_sha256":
     "4a97885eb286ce2d1d5de60c975fb8f6a7130101187ae7e267f6cdb553b35f98", "raw_sha256":
     "d54c2b80d40a40b982cd88852c6180bb944d95acdb028af3d0e01a1750681784"},
    {"name": "war_and_peace", "origin": "fetch", "language": "en",
     "url": _GB.format(2600), "file": "pg2600.txt", "extraction": "gutenberg",
     "letters": 2517012, "letters_sha256":
     "66fad2084a5b2646de1e1f3bdb17d545020c6116a2c169a70fdba45af60bab94", "raw_sha256":
     "2d5bb2ad5f422765e714617e21fa31bbaf8958aa79682c86fca6660fcc5d1b2b"},
    {"name": "goethe_faust_1", "origin": "fetch", "language": "de",
     "url": _GB.format(2229), "file": "pg2229.txt", "extraction": "gutenberg",
     "letters": 150796, "letters_sha256":
     "d92c0b35e48b63f25f5183f686f02f362efce9597aa4b3d51ec8ab023047e727", "raw_sha256":
     "fed2a58edd6910ee96d27ada614d34bcc41f03750d86541c41246bb74c564ff7"},
    {"name": "kafka_verwandlung", "origin": "fetch", "language": "de",
     "url": _GB.format(22367), "file": "pg22367.txt", "extraction": "gutenberg",
     "letters": 100976, "letters_sha256":
     "76fff2217254107492dd8377235b863fac35f8256b9fa4328dc002e36f28ca7d", "raw_sha256":
     "359d3f5983c812393f4bd7ee49a350ffffc7d476015e58d6b84b6c848dd2b0e9"},
    {"name": "fontane_effi_briest", "origin": "fetch", "language": "de",
     "url": _GB.format(5323), "file": "pg5323.txt", "extraction": "gutenberg",
     "letters": 477712, "letters_sha256":
     "8bcdc1d122968881ba8a2e422086eb5be9ccdd515fa0c56b8acb50ef8f39a4fb", "raw_sha256":
     "15a93db448403b07093042b6aa251ab22474ad9c05918e69f7ead5c62c0b2e8e"},
    {"name": "fontane_frau_jenny_treibel_berlin", "origin": "fetch", "language": "de",
     "url": _GB.format(46184), "file": "pg46184.txt", "extraction": "gutenberg",
     "letters": 311569, "letters_sha256":
     "d2087dcc8d9a658f7a90c5adda0d8b92c46e9217e6de822897a74ce93573c348", "raw_sha256":
     "db31e96fe927a24744501b9f8d210de06faf1196b29626492e38e1e1a53f40d9"},
)

# Tried and not used. Recorded so the list is not mistaken for complete.
NOT_FETCHED: tuple[dict, ...] = (
    {"name": "carter_tomb_vol1_gutenberg",
     "url": "https://www.gutenberg.org/ebooks/search/?query=tut-ankh-amen",
     "reason": "Project Gutenberg search returned no record for the 1923 volume; "
               "the archive.org OCR of the 1923 printing was used instead."},
    {"name": "cia_kryptos_texts", "url": "https://www.cia.gov/legacy/museum/artifact/kryptos/",
     "reason": "No public full-text CIA key text; skipped as instructed."},
)


def extract_text(raw: str, extraction: str) -> str:
    if extraction == "whole":
        return raw
    if extraction != "gutenberg":
        raise ValueError(f"unknown extraction {extraction}")
    lines = raw.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("*** START OF"))
    end = next(i for i, line in enumerate(lines) if line.startswith("*** END OF"))
    return "\n".join(lines[start + 1 : end])


def load_sources(work_dir: Path | str | None = None, verify: bool = True) -> list[dict]:
    """Every frozen source as {name, letters, status}. Missing files are recorded."""
    work = Path(work_dir) if work_dir is not None else DEFAULT_WORK_DIR
    repo = repo_sources()
    out = []
    for entry in FROZEN_SOURCES:
        row = dict(entry)
        if entry["origin"] == "repo":
            letters = repo[entry["name"]]
            row["status"] = "repo"
        else:
            path = work / "raw" / entry["file"]
            if not path.is_file():
                row.update(status="missing", text="")
                out.append(row)
                continue
            data = path.read_bytes()
            row["raw_sha256_seen"] = hashlib.sha256(data).hexdigest()
            letters = normalize_letters(extract_text(data.decode("utf-8", "replace"), entry["extraction"]))
            row["status"] = "fetched"
        row["letters_seen"] = len(letters)
        row["letters_sha256_seen"] = sha256_letters(letters)
        if verify and row["letters_sha256"] != "PENDING" and row["letters_sha256_seen"] != row["letters_sha256"]:
            row["status"] = "hash_mismatch"
            letters = ""
        row["text"] = letters
        out.append(row)
    return out


def fetch_sources(work_dir: Path | str | None = None, tries: int = 6) -> list[dict]:
    """Download the fetched sources into work_dir/raw. Network use only here."""
    import urllib.request

    raw_dir = (Path(work_dir) if work_dir is not None else DEFAULT_WORK_DIR) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    log = []
    for entry in FROZEN_SOURCES:
        if entry["origin"] != "fetch":
            continue
        target = raw_dir / entry["file"]
        status = "present" if target.is_file() else "failed"
        for _ in range(tries if status == "failed" else 0):
            try:
                with urllib.request.urlopen(entry["url"], timeout=60) as resp:
                    target.write_bytes(resp.read())
                status = "fetched"
                break
            except OSError as exc:  # recorded and continued
                status = f"failed: {exc}"
                time.sleep(3)
        log.append({"name": entry["name"], "url": entry["url"], "status": status})
    return log


# --------------------------------------------------------------------------
# English-key fragment check


def _text_ints(letters: str) -> list[int]:
    return [ord(ch) - 65 for ch in letters]


def fragment_score(fragments: tuple[str, ...]) -> float:
    """Sum of DiscountedLanguageModel.full_score over the key fragments (nats)."""
    from engine.language import get_model

    model = get_model()
    return sum(model.full_score(_text_ints(f)) for f in fragments)


def aligned_pair_scores(letters: str, spans=CRIB_SPANS) -> list[float]:
    """full_score of every aligned fragment pair in an English text, sorted.

    Pair o takes the text letters at the clue positions shifted by o.
    """
    from engine.language import get_model

    model = get_model()
    one, two, three = model.prefix
    logp = model.logp
    t = _text_ints(letters)
    n = len(t)
    pre = [0.0] * n
    for s in range(n - 2):
        a, b, c = t[s], t[s + 1], t[s + 2]
        pre[s] = one[a] + two[a * 26 + b] + three[(a * 26 + b) * 26 + c]
    cum = [0.0] * (n + 1)
    acc = 0.0
    for i in range(n):
        if i >= 3:
            acc += logp[((t[i - 3] * 26 + t[i - 2]) * 26 + t[i - 1]) * 26 + t[i]]
        cum[i + 1] = acc
    span_end = max(start + len(word) for start, word in spans)
    parts = [(start, len(word)) for start, word in spans]
    scores = []
    for o in range(n - span_end + 1):
        total = 0.0
        for start, length in parts:
            s = o + start
            total += pre[s] + cum[s + length] - cum[s + 3]
        scores.append(total)
    scores.sort()
    return scores


@lru_cache(maxsize=1)
def english_null() -> tuple[float, ...]:
    letters = normalize_letters((_DATA / "neural_train_public.txt").read_text(encoding="utf-8"))
    return tuple(aligned_pair_scores(letters))


def percentile(sorted_scores, value: float) -> float:
    """Percent of null pairs scoring at or below value."""
    return 100.0 * bisect.bisect_right(sorted_scores, value) / len(sorted_scores)


def threshold_from(sorted_scores, pct: float = THRESHOLD_PERCENTILE) -> float:
    idx = max(0, min(len(sorted_scores) - 1, int(len(sorted_scores) * pct / 100.0)))
    return sorted_scores[idx]


def english_fragment_control(
    key_letters: str,
    plain_letters: str,
    threshold: float,
    *,
    stride: int = 9,
    reference: float | None = None,
) -> dict:
    """Plant an English running key, recover fragments from the clue spans.

    For each tableau and each key offset (every ``stride`` letters), a
    97-letter plaintext window is encrypted with the key window. The clue
    spans of that planted plaintext then give the key letters exactly as K4's
    clues do. Returns how often the planted fragments fall below threshold,
    and, when ``reference`` is given, how often they score at or below it.
    """
    rows = []
    limit_k = len(key_letters) - WINDOW
    limit_p = len(plain_letters) - WINDOW
    if limit_k < 0 or limit_p < 0:
        raise ValueError("control texts need at least 97 letters")
    for name, rule, alphabet in tableaux():
        below = 0
        trials = 0
        lowest = math.inf
        at_or_below_reference = 0
        roundtrip_ok = True
        for o in range(0, limit_k + 1, stride):
            key = key_letters[o : o + WINDOW]
            p0 = (o * 7) % (limit_p + 1)
            plain = plain_letters[p0 : p0 + WINDOW]
            cipher = encrypt(rule, alphabet, plain, key)
            spans = tuple((start, plain[start : start + len(word)]) for start, word in CRIB_SPANS)
            frags = key_fragments(required_key(rule, alphabet, cipher, spans), spans)
            expect = tuple(key[start : start + len(word)] for start, word in CRIB_SPANS)
            if frags != expect or decrypt(rule, alphabet, cipher, key) != plain:
                roundtrip_ok = False
            trials += 1
            score = fragment_score(frags)
            lowest = min(lowest, score)
            if score < threshold:
                below += 1
            if reference is not None and score <= reference:
                at_or_below_reference += 1
        rows.append(
            {
                "tableau": name,
                "trials": trials,
                "below_threshold": below,
                "below_rate": below / trials if trials else None,
                "lowest_score": lowest,
                "at_or_below_reference": at_or_below_reference if reference is not None else None,
                "roundtrip_ok": roundtrip_ok,
            }
        )
    return {"threshold": threshold, "rows": rows}


def english_fragment_check(threshold: float | None = None) -> dict:
    """K4 key fragments per tableau, scored against the English null."""
    null = english_null()
    thr = threshold_from(null) if threshold is None else threshold
    rows = []
    for name, rule, alphabet in tableaux():
        frags = key_fragments(required_key(rule, alphabet))
        score = fragment_score(frags)
        # An English key read backwards gives reversed fragments.
        score_rev = fragment_score(tuple(f[::-1] for f in frags))
        rows.append(
            {
                "tableau": name,
                "fragments": frags,
                "score": score,
                "percentile": percentile(null, score),
                "excluded_for_english_key": score < thr,
                "score_reversed": score_rev,
                "percentile_reversed": percentile(null, score_rev),
                "excluded_for_reversed_english_key": score_rev < thr,
            }
        )
    return {
        "null_pairs": len(null),
        "null_min": null[0],
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "threshold": thr,
        "rows": rows,
        "note": "Statistical exclusion at the stated percentile, not an exact exclusion.",
    }


# --------------------------------------------------------------------------
# K4 report

# Held-out English key texts for the power control in the logged run. None of
# them is in neural_train_public.txt, which fits the quadgram model.
REPORT_CONTROLS = (
    "neural_heldout_doyle",
    "pride_and_prejudice",
    "war_and_peace",
    "declaration_of_independence",
    "king_james_bible",
    "carter_tomb_vol1_1923_ocr",
)


def search_k4_running_key_texts(
    work_dir: Path | str | None = None,
    *,
    names: tuple[str, ...] | None = None,
    with_fragment_check: bool = True,
    control_names: tuple[str, ...] = ("neural_heldout_doyle",),
) -> dict:
    """Exact clue scan over the frozen texts plus the English-key check."""
    t0 = time.perf_counter()
    sources = load_sources(work_dir)
    if names is not None:
        sources = [s for s in sources if s["name"] in names]
    tabs = tableaux()
    required = {name: required_key(rule, alpha) for name, rule, alpha in tabs}
    scan_rows = []
    unverified = []
    for src in sources:
        letters = src["text"]
        meta = {k: src[k] for k in ("name", "url", "language", "status")}
        meta["letters"] = len(letters)
        meta["letters_sha256"] = src.get("letters_sha256_seen")
        if len(letters) < SPAN_END:
            scan_rows.append({**meta, "skipped": f"fewer than {SPAN_END} letters"})
            continue
        cache: dict = {}
        t1 = time.perf_counter()
        per_tab = []
        for name, rule, alpha in tabs:
            res = scan_text(letters, required[name], indicator_cache=cache)
            per_tab.append({"tableau": name, **res})
            for hit in res["full_matches"]:
                if len(unverified) >= _FULL_MATCH_CAP:
                    break
                key = key_window(letters, hit["direction"], hit["offset"])
                unverified.append(
                    {
                        "status": "unverified",
                        "text": src["name"],
                        "tableau": name,
                        **hit,
                        "key": key,
                        "decryption": decrypt(rule, alpha, K4_CIPHERTEXT, key),
                    }
                )
        scan_rows.append({**meta, "tableaux": per_tab, "seconds": time.perf_counter() - t1})
    report = {
        "claimed_plaintext": None,
        "solved": False,
        "ciphertext_sha256": hashlib.sha256(K4_CIPHERTEXT.encode()).hexdigest(),
        "required_keys": {
            name: "".join(letter for _, letter in req) for name, req in required.items()
        },
        "scan": scan_rows,
        "unverified": unverified,
        "unverified_cap": _FULL_MATCH_CAP,
        "not_fetched": list(NOT_FETCHED),
    }
    if with_fragment_check:
        t2 = time.perf_counter()
        check = english_fragment_check()
        controls = []
        by_name = {s["name"]: s["text"] for s in sources}
        repo = repo_sources()
        plain = repo["kryptos_k2_plaintext"] + repo["kryptos_k3_plaintext"]
        # Highest K4 fragment score over the twelve tableaux, either reading.
        k4_best = max(max(row["score"], row["score_reversed"]) for row in check["rows"])
        check["k4_best_score"] = k4_best
        for cname in control_names:
            key_text = by_name.get(cname) or repo.get(cname, "")
            if len(key_text) < WINDOW:
                controls.append({"key_text": cname, "skipped": "not available"})
                continue
            stride = max(1, len(key_text) // 1500)
            ctl = english_fragment_control(
                key_text, plain, check["threshold"], stride=stride, reference=k4_best
            )
            controls.append({"key_text": cname, "stride": stride, **ctl})
        check["controls"] = controls
        check["seconds"] = time.perf_counter() - t2
        report["english_key_check"] = check
    report["seconds"] = time.perf_counter() - t0
    return report


def _print_summary(report: dict) -> None:
    print("required key letters (positions 21..33 | 63..73):")
    for name, req in report["required_keys"].items():
        print(f"  {name:28s} {req[:13]} {req[13:]}")
    for row in report["scan"]:
        if "skipped" in row:
            print(f"{row['name']}: {row['letters']} letters, skipped ({row['skipped']})")
            continue
        print(f"{row['name']}: {row['letters']} letters, {row['seconds']:.2f} s")
        for t in row["tableaux"]:
            ch = t["chance"]
            print(
                f"  {t['tableau']:28s} full={len(t['full_matches'])} best={t['best_partial']}"
                f" expected_max={ch['expected_max']} p={ch['p_max_at_least_best']:.3g}"
                f" shuffle_best={t['shuffle_best']}"
            )
    print("unverified full matches:", report["unverified"])
    check = report.get("english_key_check")
    if check:
        print(
            f"threshold {check['threshold']:.3f} at {check['threshold_percentile']} pct"
            f" of {check['null_pairs']} pairs; null min {check['null_min']:.3f}"
        )
        for r in check["rows"]:
            print(
                f"  {r['tableau']:28s} {r['fragments'][0]} {r['fragments'][1]}"
                f" score={r['score']:.2f} pct={r['percentile']:.4f} excluded={r['excluded_for_english_key']}"
                f" reversed={r['score_reversed']:.2f} excluded_rev={r['excluded_for_reversed_english_key']}"
            )
        for c in check["controls"]:
            print("control", c.get("key_text"), c.get("stride"), c.get("skipped", ""))
            for r in c.get("rows", []):
                print(
                    f"  {r['tableau']:28s} below {r['below_threshold']}/{r['trials']}"
                    f" lowest={r['lowest_score']:.2f} at_or_below_k4_best={r['at_or_below_reference']}"
                    f" roundtrip={r['roundtrip_ok']}"
                )
    print(f"total {report['seconds']:.1f} s; solved={report['solved']} claimed_plaintext={report['claimed_plaintext']}")


if __name__ == "__main__":  # pragma: no cover
    import sys

    if "--fetch" in sys.argv:
        for line in fetch_sources():
            print(line)
    _print_summary(
        search_k4_running_key_texts(
            control_names=REPORT_CONTROLS
        )
    )


__all__ = [
    "FROZEN_SOURCES",
    "NOT_FETCHED",
    "THRESHOLD_PERCENTILE",
    "aligned_pair_scores",
    "decrypt",
    "encrypt",
    "english_fragment_check",
    "english_fragment_control",
    "english_null",
    "fetch_sources",
    "key_fragments",
    "key_letter",
    "keyed_alphabet",
    "load_sources",
    "normalize_letters",
    "repo_sources",
    "required_key",
    "scan_text",
    "search_k4_running_key_texts",
    "tableaux",
]
