"""Rewrite generated doc indexes from the research notes and the logs.

Hand-written prose outside the marked regions is left alone. A push to
main runs this script and commits the result when the indexes moved.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "research-notes"
LOGS = ROOT / "docs" / "logs"
README = NOTES / "README.md"
ROOT_README = ROOT / "README.md"
DAGAPEYEFF = NOTES / "dagapeyeff-2026-10-05.md"
STATUS = NOTES / "dagapeyeff-status.json"

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
_ORDER = ("open", "tested-without-power", "excluded-by-count", "closed-with-power")
_LABEL = {
    "closed-with-power": "Closed with shown power",
    "excluded-by-count": "Excluded by a count",
    "tested-without-power": "Tested without shown power",
    "open": "Open",
}

_FIELD = re.compile(r"^index-(id|title|problem|data|next): (.*)$", re.M)


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


_DATE = re.compile(r"(20\d\d-\d\d-\d\d)")


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


def ledger() -> dict:
    return json.loads(STATUS.read_text(encoding="utf-8"))


def tally(data: dict) -> dict[str, int]:
    counts = {status: 0 for status in _ORDER}
    for family in data["families"]:
        counts[family["status"]] += 1
    return counts


def _percent(part: int, whole: int) -> int:
    return round(100 * part / whole) if whole else 0


def status_summary(data: dict) -> str:
    counts = tally(data)
    total = sum(counts.values())
    shut = counts["closed-with-power"] + counts["excluded-by-count"]
    return (
        f"Unsolved. Plaintext recovered: {data['plaintext_recovered_percent']} percent. "
        f"{shut} of {total} hypothesis families listed ({_percent(shut, total)} percent) are closed with shown power "
        f"or excluded by a count; {counts['open']} are open. Reviewed through {data['reviewed_through']}."
    )


def status_block(data: dict) -> str:
    counts = tally(data)
    total = sum(counts.values())
    lines = [
        "## How close is this to solved?",
        "",
        f"**{status_summary(data)}**",
        "",
        "Progress here means ruling hypotheses out, not reading part of a message. The percentage is a share of "
        "the families listed below, which is not every possible cipher, and a hand construction with no message "
        "fits every statistic measured so far. It is not a measure of distance to a reading.",
        "",
        "| Status | Families | Share |",
        "| --- | --- | --- |",
    ]
    for status in _ORDER:
        lines.append(f"| {_LABEL[status]} | {counts[status]} | {_percent(counts[status], total)} percent |")
    for status in _ORDER:
        families = sorted((f for f in data["families"] if f["status"] == status), key=lambda f: f.get("priority", 0))
        if not families:
            continue
        lines += ["", f"### {_LABEL[status]} ({len(families)})", "", "| Family | Evidence |", "| --- | --- |"]
        for family in families:
            links = ", ".join(f"[log](../logs/{name})" for name in family["logs"])
            lines.append(f"| {family['family']} | {family['evidence']} {links} |")
    lines += ["", "Generated from [`dagapeyeff-status.json`](dagapeyeff-status.json) by `tools/refresh_docs.py`."]
    return "\n".join(lines)


def _open(data: dict) -> list[dict]:
    return sorted((f for f in data["families"] if f["status"] == "open"), key=lambda f: f["priority"])


def next_block(data: dict) -> str:
    lines = ["Open families, in the order they are planned:", ""]
    for rank, family in enumerate(_open(data), start=1):
        lines.append(f"{rank}. **{family['family']}.** {family['next']}")
    lines += ["", "Generated from [`dagapeyeff-status.json`](dagapeyeff-status.json) by `tools/refresh_docs.py`."]
    return "\n".join(lines)


def _replace(text: str, start: str, end: str, body: str) -> str:
    if start not in text or end not in text:
        raise SystemExit(f"missing markers {start}")
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    match = pattern.search(text)
    if match is None:
        raise SystemExit(f"missing markers {start}")
    replacement = f"{start}{body}{end}" if "\n" not in match.group(0) else f"{start}\n{body}\n{end}"
    return text[:match.start()] + replacement + text[match.end():]


def render() -> dict[str, str]:
    notes = [_block(path) for path in _notes()]
    count = str(len(notes))
    updated = {
        str(README.relative_to(ROOT)): _replace(README.read_text(), CASE_START, CASE_END, case_table(notes)),
        str(ROOT_README.relative_to(ROOT)): _replace(
            ROOT_README.read_text(),
            COUNT_START,
            COUNT_END,
            f"{count} dated primary-source case notes",
        ),
    }
    if DAGAPEYEFF.exists():
        note = _replace(DAGAPEYEFF.read_text(), LOG_START, LOG_END, log_index())
        if STATUS.exists():
            data = ledger()
            note = _replace(note, STATUS_START, STATUS_END, status_block(data))
            note = _replace(note, NEXT_START, NEXT_END, next_block(data))
            note = re.sub(r"^index-next: .*$", "index-next: " + _open(data)[0]["next"].rstrip("."), note, count=1, flags=re.M)
            readme = updated[str(ROOT_README.relative_to(ROOT))]
            updated[str(ROOT_README.relative_to(ROOT))] = _replace(
                readme, README_STATUS_START, README_STATUS_END, status_summary(data)
            )
        updated[str(DAGAPEYEFF.relative_to(ROOT))] = note
        updated[str(README.relative_to(ROOT))] = _replace(
            README.read_text(), CASE_START, CASE_END, case_table([
                _block_text(path, note if path == DAGAPEYEFF else path.read_text()) for path in _notes()
            ])
        )
    return updated


def write(updated: dict[str, str]) -> list[str]:
    changed = []
    for relative, text in updated.items():
        path = ROOT / relative
        if path.read_text() != text:
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
