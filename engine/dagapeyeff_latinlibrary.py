"""Every 196-letter window of The Latin Library against the cells' letter counts. Not a reading.

engine.dagapeyeff_latinlib screened 8.9 million letters of Latin and found no
window within 2 errors of the cells' counts. The Latin Library
(https://www.thelatinlibrary.com/) holds far more: classical, Christian,
medieval and neo-Latin texts. This screen crawled its author and text pages,
one request at a time, into the ignored work/ folder, and counts every window
of every page the same way: the fewest single-cell errors that turn the
window into the cells' counts, under any one-to-one key and any order.

The crawl was stopped after 1,777 fetched pages to give the time to searches; the
frozen result covers those pages, whose sorted list is hashed in the report. Course and
teaching folders, which mix in English, are skipped, and only
paragraphs led by Latin function words are kept. For the closest windows only
a page and a letter offset are stored, never the letters.

No letter string is stored.
"""

from __future__ import annotations

import hashlib
import html
import re
import time
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_latinlib import _KEEP, _LETTERS, errors_per_window, is_latin
from engine.dagapeyeff_screen import fold

ROOT = "https://www.thelatinlibrary.com/"
_WORK = Path(__file__).resolve().parents[1] / "work" / "external" / "latinlibrary"
_DEPTH = 4
_PAUSE = 0.5
# The frozen run stopped crawling after the pages already fetched; a page not fetched by then is skipped.
_FETCH = False
_SKIP = ("ll1/", "ll2/", "courses/", "imperialism/", "law/", "historians/", "satire/", "caes/", "catullus/",
         "livius/", "sallust/", "virgil/", "epubs", "about.html", "cred.html", "indices.html", "technical.html")


def _local(url: str) -> Path:
    path = urllib.parse.urlparse(url).path.strip("/") or "index.html"
    return _WORK / (path.replace("/", "__") + ".page")


def _get(url: str) -> str:
    path = _local(url)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    if not _FETCH:
        return ""
    time.sleep(_PAUSE)
    request = urllib.request.Request(url, headers={"User-Agent": "Undeciphered-Texts letter-count screen"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except Exception:  # A missing page is left out; the crawl list records what was read.
        raw = b""
    _WORK.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw.decode("latin-1" if b"charset=iso-8859-1" in raw.lower() else "utf-8", errors="replace")


def _links(url: str, page: str) -> list[str]:
    out = []
    for href in re.findall(r'href="([^"#]+)"', page, re.I):
        target = urllib.parse.urljoin(url, href.strip())
        parsed = urllib.parse.urlparse(target)
        if parsed.netloc not in ("www.thelatinlibrary.com", "thelatinlibrary.com"):
            continue
        rel = parsed.path.lstrip("/")
        if any(rel.startswith(skip) for skip in _SKIP):
            continue
        if rel and not re.search(r"(\.s?html?|/)$", rel) and "." in rel.rsplit("/", 1)[-1]:
            continue
        path = parsed.path or "/"
        if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
            path += "/"  # An author folder: its page links relative to the folder.
        out.append(urllib.parse.urlunparse(("https", "www.thelatinlibrary.com", path, "", "", "")))
    return out


def crawl() -> list[str]:
    seen, queue = {ROOT}, deque([(ROOT, 0)])
    order = []
    while queue:
        url, depth = queue.popleft()
        page = _get(url)
        if not page:
            continue
        order.append(url)
        if depth < _DEPTH:
            for link in _links(url, page):
                if link not in seen:
                    seen.add(link)
                    queue.append((link, depth + 1))
    return sorted(order)


def letters(page: str) -> str:
    body = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", " ", page)
    body = re.sub(r"(?i)<(p|br|div|tr|h\d)\b[^>]*>", "\n\n", body)
    body = html.unescape(re.sub(r"<[^>]+>", " ", body))
    return fold(" ".join(paragraph for paragraph in re.split(r"\n\s*\n", body) if is_latin(paragraph)))


@frozen("dagapeyeff-latinlibrary")
def latinlibrary_report() -> dict:
    target = sorted_counts(_cells()).astype(np.int32)
    urls = crawl()
    pages = total_letters = total_windows = within_2 = within_4 = within_8 = 0
    fewest = None
    closest = []
    medians = []
    for url in urls:
        text = letters(_get(url))
        if len(text) < _LETTERS:
            continue
        errors = errors_per_window(text, target)
        pages += 1
        total_letters += len(text)
        total_windows += len(errors)
        within_2 += int((errors <= 2).sum())
        within_4 += int((errors <= 4).sum())
        within_8 += int((errors <= 8).sum())
        medians.append(float(np.median(errors)))
        low = int(errors.min())
        fewest = low if fewest is None else min(fewest, low)
        at = int(np.argmin(errors))
        closest.append({"page": urllib.parse.urlparse(url).path, "offset": at, "errors": low})
    closest.sort(key=lambda item: (item["errors"], item["page"], item["offset"]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": ROOT,
        "pages_crawled": len(urls),
        "crawl_sha256": hashlib.sha256("\n".join(urls).encode()).hexdigest(),
        "pages_screened": pages,
        "letters": total_letters,
        "windows": total_windows,
        "fewest_errors": fewest,
        "median_of_page_medians": float(np.median(medians)) if medians else None,
        "within_2": within_2,
        "within_4": within_4,
        "within_8": within_8,
        "closest": closest[:_KEEP],
    }
