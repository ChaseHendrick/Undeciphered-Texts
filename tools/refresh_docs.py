"""Rewrite generated doc indexes from the research notes, their status ledgers and the logs.

Hand-written prose outside the marked regions is left alone. A push to
main runs this script and commits the result when the indexes moved.

Each `docs/research-notes/<case>-status.json` ledger writes the status block
and next steps of its note, that note's `index-next` line, one row of the
status table in the root README, and its entry in `research-feed.json`, the
file hendrickresearch.com reads to build its research pages.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTES = DOCS / "research-notes"
LOGS = DOCS / "logs"
CACHE = ROOT / "engine" / "data" / "swarm_cache"
README = NOTES / "README.md"
ROOT_README = ROOT / "README.md"
DAGAPEYEFF = NOTES / "dagapeyeff-2026-10-05.md"
STATUS = NOTES / "dagapeyeff-status.json"
FEED = NOTES / "research-feed.json"
REPOSITORY = "https://github.com/ChaseHendrick/Undeciphered-Texts"
BLOB = REPOSITORY + "/blob/main/"

CASE_START = "<!-- case-index:start -->"
CASE_END = "<!-- case-index:end -->"
COUNT_START = "<!-- research-note-count:start -->"
COUNT_END = "<!-- research-note-count:end -->"
LOG_START = "<!-- generated-logs:start -->"
LOG_END = "<!-- generated-logs:end -->"
STATUS_START = "<!-- generated-status:start -->"
STATUS_END = "<!-- generated-status:end -->"
NEXT_START = "<!-- generated-next:start -->"
NEXT_END = "<!-- generated-next:end -->"
README_STATUS_START = "<!-- dagapeyeff-status:start -->"
README_STATUS_END = "<!-- dagapeyeff-status:end -->"
TABLE_START = "<!-- research-status:start -->"
TABLE_END = "<!-- research-status:end -->"
_ORDER = ("open", "tested-without-power", "excluded-by-constraint", "excluded-by-count", "closed-with-power")
_SHUT = ("closed-with-power", "excluded-by-count", "excluded-by-constraint")
_LABEL = {
    "closed-with-power": "Closed with shown power",
    "excluded-by-count": "Excluded by a count",
    "excluded-by-constraint": "Excluded by the clues",
    "tested-without-power": "Tested without shown power",
    "open": "Open",
}

_FIELD = re.compile(r"^index-(id|title|problem|data|next): (.*)$", re.M)
_DATE = re.compile(r"(20\d\d-\d\d-\d\d)")
_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def _notes() -> list[Path]:
    return sorted(path for path in NOTES.glob("*.md") if path.name != "README.md")


def _block(path: Path) -> dict[str, str]:
    return _block_text(path, path.read_text())


def _block_text(path: Path, text: str) -> dict[str, str]:
    found = dict(_FIELD.findall(text))
    return {
        "id": found.get("id", path.stem),
        "title": found.get("title", path.stem),
        "problem": found.get("problem", "Add an index block to this note."),
        "data": found.get("data", "See the note."),
        "next": found.get("next", "Add an index block to this note."),
        "file": path.name,
    }


def _ordered(notes: list[dict[str, str]]) -> list[dict[str, str]]:
    current = README.read_text() if README.exists() else ""
    rank = {name: index for index, name in enumerate(re.findall(r"\]\(([^)]+\.md)\)", current))}
    return sorted(notes, key=lambda note: (rank.get(note["file"], 10_000), note["file"]))


def case_table(notes: list[dict[str, str]]) -> str:
    rows = [
        "| Case | Problem represented here | Data entry point | Next measurable task |",
        "| --- | --- | --- | --- |",
    ]
    for note in _ordered(notes):
        rows.append(
            f"| [{note['title']}]({note['file']}) | {note['problem']} | {note['data']} | {note['next']} |"
        )
    return "\n".join(rows)


def _log_key(path: Path) -> tuple[str, str]:
    found = _DATE.findall(path.name)
    return (found[-1] if found else "", path.name)


def log_index() -> str:
    rows = []
    for path in sorted(LOGS.glob("dagapeyeff*.md"), key=_log_key):
        title = path.stem
        for line in path.read_text().splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        rows.append(f"- [{title}](../logs/{path.name})")
    return "\n".join(rows)


def ledgers() -> list[dict]:
    """Every status ledger, in the order of the case index."""
    found = [json.loads(path.read_text(encoding="utf-8")) | {"_file": path.name}
             for path in sorted(NOTES.glob("*-status.json"))]
    rank = {note["file"]: index for index, note in enumerate(_ordered([_block(path) for path in _notes()]))}
    return sorted(found, key=lambda data: (rank.get(data["note"], 10_000), data["case"]))


def ledger() -> dict:
    return json.loads(STATUS.read_text(encoding="utf-8")) | {"_file": STATUS.name}


def log_path(name: str) -> str:
    """A cited log, relative to docs/: a bare name in docs/logs, or a path under docs/."""
    return f"logs/{name}" if (LOGS / name).exists() else name


def _statuses(data: dict) -> list[str]:
    return [status for status in _ORDER if status in data["statuses"]]


def label(data: dict, status: str) -> str:
    return data.get("labels", {}).get(status, _LABEL[status])


def tally(data: dict) -> dict[str, int]:
    counts = {status: 0 for status in _statuses(data)}
    for family in data["families"]:
        counts[family["status"]] += 1
    return counts


def _percent(part: int, whole: int) -> int:
    return round(100 * part / whole) if whole else 0


def status_summary(data: dict) -> str:
    counts = tally(data)
    total = sum(counts.values())
    shut_statuses = [status for status in _SHUT if status in counts]
    shut = sum(counts[status] for status in shut_statuses)
    phrase = " or ".join(label(data, status)[0].lower() + label(data, status)[1:] for status in shut_statuses)
    script = data.get("kind") == "script"
    opening = "Undeciphered. Reading recovered" if script else "Unsolved. Plaintext recovered"
    unit = data.get("unit", "hypothesis families")
    verb = "is" if shut == 1 else "are"
    return (
        f"{opening}: {data['plaintext_recovered_percent']} percent. "
        f"{shut} of {total} {unit} listed ({_percent(shut, total)} percent) {verb} {phrase}; "
        f"{counts.get('open', 0)} {'is' if counts.get('open', 0) == 1 else 'are'} open. "
        f"Reviewed through {data['reviewed_through']}."
    )


def _links(data: dict, family: dict, prefix: str) -> str:
    return ", ".join(f"[log]({prefix}{log_path(name)})" for name in family["logs"])


def status_block(data: dict) -> str:
    counts = tally(data)
    total = sum(counts.values())
    lines = ["## How close is this to solved?", "", f"**{status_summary(data)}**", ""]
    if data.get("lay", {}).get("summary"):
        lines += [f"**In plain words.** {data['lay']['summary']}", ""]
    column = "Questions" if data.get("kind") == "script" else "Families"
    lines += [data["caveat"], "", f"| Status | {column} | Share |",
              "| --- | --- | --- |"]
    for status in _statuses(data):
        lines.append(f"| {label(data, status)} | {counts[status]} | {_percent(counts[status], total)} percent |")
    column = "Question" if data.get("kind") == "script" else "Family"
    for status in _statuses(data):
        families = sorted((f for f in data["families"] if f["status"] == status), key=lambda f: f.get("priority", 0))
        if not families:
            continue
        lines += ["", f"### {label(data, status)} ({len(families)})", "", f"| {column} | Evidence |", "| --- | --- |"]
        for family in families:
            links = _links(data, family, "../")
            lines.append(f"| {family['family']} | {family['evidence']}{' ' + links if links else ''} |")
    lines += ["", f"Generated from [`{data['_file']}`]({data['_file']}) by `tools/refresh_docs.py`."]
    return "\n".join(lines)


def _open(data: dict) -> list[dict]:
    return sorted((f for f in data["families"] if f["status"] == "open"), key=lambda f: f["priority"])


def next_block(data: dict) -> str:
    column = "Open questions" if data.get("kind") == "script" else "Open families"
    lines = [f"{column}, in the order they are planned:", ""]
    for rank, family in enumerate(_open(data), start=1):
        lines.append(f"{rank}. **{family['family'].rstrip('?.')}.** {family['next']}")
    lines += ["", f"Generated from [`{data['_file']}`]({data['_file']}) by `tools/refresh_docs.py`."]
    return "\n".join(lines)


def status_table(cases: list[dict]) -> str:
    rows = ["| Case | Status |", "| --- | --- |"]
    for data in cases:
        rows.append(f"| [{data['title']}](docs/research-notes/{data['note']}) | {status_summary(data)} |")
    return "\n".join(rows)


def _replace(text: str, start: str, end: str, body: str) -> str:
    if start not in text or end not in text:
        raise SystemExit(f"missing markers {start}")
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    match = pattern.search(text)
    if match is None:
        raise SystemExit(f"missing markers {start}")
    replacement = f"{start}{body}{end}" if "\n" not in match.group(0) else f"{start}\n{body}\n{end}"
    return text[:match.start()] + replacement + text[match.end():]


def _cache(name: str) -> dict:
    return json.loads((CACHE / f"{name}.json").read_text(encoding="utf-8"))


def _language(treebank: str) -> str:
    """Latin-ITTB is shown as Latin (ITTB)."""
    language, _, corpus = treebank.replace("_", " ").partition("-")
    return f"{language} ({corpus})" if corpus else language


def _language_screen(chart: dict) -> dict:
    """Rows from the frozen screens. English's fewest errors are half its sorted-count distance."""
    screen = _cache("dagapeyeff-screen")
    rows = [{"label": _language(name), "value": row["fewest_errors"], "median": row["median_errors"], "within_8": row["within_8"]}
            for name, row in ((name, screen["languages"][name]) for name in screen["ranked"])]
    corpus = _cache("dagapeyeff-corpus")
    rows.append({"label": "English (prose corpus)", "value": corpus["closest_sorted_distance"] // 2,
                 "median": corpus["median_sorted_distance"] / 2, "within_8": None})
    for name, pick in (("dagapeyeff-russian", lambda r: min(r["rows"].values(), key=lambda x: x["fewest_errors"])),
                       ("dagapeyeff-esperanto", lambda r: r["esperanto"])):
        if (CACHE / f"{name}.json").exists():
            row = pick(_cache(name))
            title = "Russian (best of four spellings)" if "russian" in name else "Esperanto (10 books)"
            rows.append({"label": title, "value": row["fewest_errors"], "median": row["median_errors"],
                         "within_8": row["within_8"]})
    rows.sort(key=lambda row: (row["value"], row["median"]))
    return {key: value for key, value in chart.items() if key != "from_cache"} | {
        "kind": "bar", "unit": "fewest errors", "rows": rows}


_FROM_CACHE = {"dagapeyeff-screen": _language_screen}


def _chart(chart: dict) -> dict:
    out = _FROM_CACHE[chart["from_cache"]](chart) if "from_cache" in chart else dict(chart)
    if "log" in out:
        out["log"] = BLOB + "docs/" + log_path(out["log"])
    return out


def _sources(note: str) -> list[dict]:
    seen, out = set(), []
    for text, url in _LINK.findall(note):
        if url not in seen and "github.com/ChaseHendrick" not in url:
            seen.add(url)
            out.append({"title": text, "url": url})
    return out


def feed_case(data: dict, note: str) -> dict:
    counts = tally(data)
    families = []
    for family in sorted(data["families"], key=lambda f: (_ORDER.index(f["status"]), f.get("priority", 0))):
        families.append({
            "family": family["family"], "status": family["status"], "status_label": label(data, family["status"]),
            "evidence": family["evidence"], "next": family.get("next"), "priority": family.get("priority"),
            "logs": [BLOB + "docs/" + log_path(name) for name in family["logs"]],
        })
    return {
        "id": data["case"],
        "title": data["title"],
        "kind": data.get("kind", "cipher"),
        "stage": data.get("stage", "ongoing"),
        "unit": data.get("unit", "hypothesis families"),
        "reviewed_through": data["reviewed_through"],
        "plaintext_recovered_percent": data["plaintext_recovered_percent"],
        "summary": status_summary(data),
        "caveat": data["caveat"],
        "note_url": BLOB + "docs/research-notes/" + data["note"],
        "ledger_url": BLOB + "docs/research-notes/" + data["_file"],
        "problem": _block_text(NOTES / data["note"], note)["problem"],
        "statuses": [{"status": status, "label": label(data, status), "definition": data["statuses"][status],
                      "count": counts[status], "percent": _percent(counts[status], sum(counts.values()))}
                     for status in _statuses(data)],
        "families": families,
        "next": [{"family": f["family"], "next": f["next"]} for f in _open(data)],
        "lay": data.get("lay", {}),
        "researcher": data.get("researcher", {}),
        "manuscript": data.get("manuscript"),
        "charts": [_chart(chart) for chart in data.get("charts", [])],
        "data": data.get("data", {}),
        "sources": _sources(note),
    }


def feed(cases: list[dict], notes: dict[str, str]) -> str:
    body = {
        "schema": "research-feed-1",
        "repository": REPOSITORY,
        "note": "Generated by tools/refresh_docs.py from the status ledgers. No case is solved; nothing here is a reading.",
        "cases": [feed_case(data, notes[data["note"]]) for data in cases],
    }
    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


def render() -> dict[str, str]:
    root_key = str(ROOT_README.relative_to(ROOT))
    readme = _replace(ROOT_README.read_text(), COUNT_START, COUNT_END, f"{len(_notes())} dated primary-source case notes")
    notes = {path.name: path.read_text() for path in _notes()}
    if DAGAPEYEFF.exists():
        notes[DAGAPEYEFF.name] = _replace(notes[DAGAPEYEFF.name], LOG_START, LOG_END, log_index())
    cases = ledgers()
    for data in cases:
        note = notes[data["note"]]
        note = _replace(note, STATUS_START, STATUS_END, status_block(data))
        note = _replace(note, NEXT_START, NEXT_END, next_block(data))
        if _open(data):
            note = re.sub(r"^index-next: .*$", "index-next: " + _open(data)[0]["next"].rstrip("."), note,
                          count=1, flags=re.M)
        notes[data["note"]] = note
        if data["case"] == "dagapeyeff":
            readme = _replace(readme, README_STATUS_START, README_STATUS_END, status_summary(data))
    if cases:
        readme = _replace(readme, TABLE_START, TABLE_END, status_table(cases))
    updated = {
        str(README.relative_to(ROOT)): _replace(
            README.read_text(), CASE_START, CASE_END,
            case_table([_block_text(path, notes[path.name]) for path in _notes()])),
        root_key: readme,
        str(FEED.relative_to(ROOT)): feed(cases, notes),
    }
    for name, text in notes.items():
        updated[str((NOTES / name).relative_to(ROOT))] = text
    return updated


def write(updated: dict[str, str]) -> list[str]:
    changed = []
    for relative, text in updated.items():
        path = ROOT / relative
        if not path.exists() or path.read_text() != text:
            path.write_text(text)
            changed.append(relative)
    return changed


def main() -> int:
    changed = write(render())
    if "--check" in sys.argv and changed:
        print("stale indexes:")
        for relative in changed:
            print(f"  {relative}")
        return 1
    for relative in changed:
        print(f"updated {relative}")
    if not changed:
        print("indexes already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
