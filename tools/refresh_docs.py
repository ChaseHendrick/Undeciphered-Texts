"""Rewrite generated doc indexes from the research notes and the logs.

Hand-written prose outside the marked regions is left alone. A push to
main runs this script and commits the result when the indexes moved.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "research-notes"
LOGS = ROOT / "docs" / "logs"
README = NOTES / "README.md"
ROOT_README = ROOT / "README.md"
DAGAPEYEFF = NOTES / "dagapeyeff-2026-10-05.md"

CASE_START = "<!-- case-index:start -->"
CASE_END = "<!-- case-index:end -->"
COUNT_START = "<!-- research-note-count:start -->"
COUNT_END = "<!-- research-note-count:end -->"
LOG_START = "<!-- generated-logs:start -->"
LOG_END = "<!-- generated-logs:end -->"

_FIELD = re.compile(r"^index-(id|title|problem|data|next): (.*)$", re.M)


def _notes() -> list[Path]:
    return sorted(path for path in NOTES.glob("*.md") if path.name != "README.md")


def _block(path: Path) -> dict[str, str]:
    text = path.read_text()
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
        updated[str(DAGAPEYEFF.relative_to(ROOT))] = _replace(
            DAGAPEYEFF.read_text(), LOG_START, LOG_END, log_index()
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
