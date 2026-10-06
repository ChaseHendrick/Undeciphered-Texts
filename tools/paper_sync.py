#!/usr/bin/env python3
"""Publish a finished paper as a public repository of its own, its "companion" in papers/papers.json.

    python3 tools/paper_sync.py --list [--paper <id>]   "<id> <owner/repo>" for each paper ready to publish
    python3 tools/paper_sync.py --stage <id> <dir>      write the companion's files into an empty <dir>
    python3 tools/paper_sync.py --check <id>            stage into a scratch folder and report problems
    python3 tools/paper_sync.py --companion <id>        the paper's companion repository, owner/name
    python3 tools/paper_sync.py --notes <id> <version>  the release notes under "## <version>" of RELEASES.md
    python3 tools/paper_sync.py --release-check <id>    refuse a release while the quality record has open items

This is the GENChase publisher (tools/paper-sync.js there) for this repository, so every paper of the
owner's reaches its companion and Zenodo the same way. The companion holds papers/<id>/ without notes/
and submission/, which stay here, plus the frozen inputs its numbers program names (companionData), and a
LICENSE, a CITATION.cff and a .zenodo.json written from papers.json. Zenodo archives each release as a
preprint (Publication / Preprint); its description is the "## Abstract" section of the README.
.github/workflows/papers.yml runs tools/paper-publish.sh, which calls this; docs/PUBLISHING-PAPERS.md
is the runbook.
"""

from __future__ import annotations

import datetime
import html
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["draft", "preparing", "ready", "on-arxiv", "submitted", "accepted", "published"]
PRIVATE_DIRS = ("notes/", "submission/")
GENERATED = ("LICENSE", "CITATION.cff", ".zenodo.json")
BINARY = re.compile(r"\.(pdf|png|jpe?g|gif|zip|npz|gz)$", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
SEMVER = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
ZENODO_DOI = re.compile(r"10\.5281/zenodo\.[1-9][0-9]{0,20}")
TEXT_LICENSES = {
    "all-rights-reserved": "The manuscript in paper/, its figures included, is Copyright (c) {year} {name}. All rights reserved.",
    "CC-BY-4.0": ("The manuscript in paper/, its figures included, is Copyright (c) {year} {name}, licensed under the "
                  "Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/)."),
}
QUALITY_ITEMS = ("U1", "U2", "U3", "U4", "U5", "U6", "U7")


class Refused(Exception):
    pass


def registry(root: Path = ROOT) -> dict:
    return json.loads((root / "papers" / "papers.json").read_text(encoding="utf-8"))


def paper(reg: dict, paper_id: str) -> dict:
    for entry in reg["papers"]:
        if entry["id"] == paper_id:
            return entry
    raise Refused(f"no paper {paper_id} in papers/papers.json")


def ready(reg: dict, only: str | None = None) -> list[dict]:
    out = []
    for entry in reg["papers"]:
        if only and entry["id"] != only:
            continue
        why = None
        if not entry.get("companion"):
            why = "has no companion repository"
        elif ORDER.index(entry["status"]) < ORDER.index("ready"):
            why = f"is {entry['status']}, not ready"
        if why:
            if only:
                raise Refused(f"paper {only} {why}")
            continue
        if not re.fullmatch(r"[a-z0-9-]+", entry["id"]) or not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+", entry["companion"]):
            raise Refused(f"bad id or companion for {entry['id']}")
        out.append(entry)
    if only and not out:
        raise Refused(f"no paper {only} in papers/papers.json")
    return out


def tracked_files(root: Path, paper_id: str) -> list[str]:
    prefix = f"papers/{paper_id}/"
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", prefix], check=True,
                            stdout=subprocess.PIPE).stdout.decode("utf-8")
    return [name[len(prefix):] for name in listed.split("\0") if name]


def archive_citation(entry: dict) -> dict | None:
    if "archiveVersion" not in entry or entry.get("archiveVersion") is None:
        return None
    version, doi = entry["archiveVersion"], entry.get("codeDoi")
    if not isinstance(version, str) or not SEMVER.fullmatch(version) or not isinstance(doi, str) or not ZENODO_DOI.fullmatch(doi):
        raise Refused(f"archiveVersion of {entry['id']} needs a plain release version and its registered Zenodo DOI")
    return {"version": version, "doi": doi}


def companion_readme(readme: str, entry: dict) -> str:
    """Point the README's current release and DOI, before its first section, at the verified archive."""
    archive = archive_citation(entry)
    if not archive:
        return readme
    at = readme.find("\n## ")
    at = len(readme) if at < 0 else at
    head, rest = readme[:at], readme[at:]
    release = re.search(r"\b[Rr]elease\s+(" + SEMVER.pattern + r")\b", head)
    locator = re.search(r"\[doi:(10\.5281/zenodo\.\d+)\]\(https://doi\.org/\1\)", head)
    if not release or not locator or release.start() > locator.start():
        raise Refused(f"README of {entry['id']} needs its release version and its Zenodo DOI link before the first section")
    doi = archive["doi"]
    head = head[:locator.start()] + f"[doi:{doi}](https://doi.org/{doi})" + head[locator.end():]
    head = head[:release.start(1)] + archive["version"] + head[release.end(1):]
    return head + rest


def abstract_of(readme: str) -> tuple[list[str], list[str]]:
    """The "## Abstract" section as paragraphs of plain text, and what keeps it from being one."""
    match = re.search(r"^## Abstract\b[^\n]*\n(.*?)(?=^## |\Z)", readme, flags=re.S | re.M)
    if not match:
        return [], ['README.md: no "## Abstract" section, which the Zenodo description is made from']
    paragraphs = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n\s*\n", match.group(1))]
    paragraphs = [part for part in paragraphs if part]
    if not paragraphs:
        return [], ['README.md: the "## Abstract" section is empty']
    left = sorted(set(re.findall(r"\\[A-Za-z]+|\$|\\.", " ".join(paragraphs))))
    if left:
        return paragraphs, ["README.md: the abstract keeps TeX that has no plain-text form for the Zenodo description: " + " ".join(left)]
    if any(part.startswith("(written by") for part in paragraphs):
        return paragraphs, ["README.md: the abstract is still a placeholder; run the paper's numbers program"]
    return paragraphs, []


def _person(author: dict, indent: str) -> list[str]:
    lines = [f'{indent}- given-names: {json.dumps(author["given-names"])}',
             f'{indent}  family-names: {json.dumps(author["family-names"])}',
             f'{indent}  affiliation: {json.dumps(author["affiliation"])}']
    if author.get("orcid"):
        lines.append(f'{indent}  orcid: {json.dumps("https://orcid.org/" + author["orcid"])}')
    return lines


def citation(reg: dict, entry: dict, year: int) -> str:
    archive = archive_citation(entry)
    arxiv = (entry.get("arxiv") or {}).get("id")
    arxiv_doi = "10.48550/arXiv." + re.sub(r"v\d+$", "", arxiv) if arxiv else None
    journal_doi = (entry.get("journal") or {}).get("doi")
    preferred_doi = journal_doi or arxiv_doi or entry.get("codeDoi")
    preferred_url = f"https://arxiv.org/abs/{arxiv}" if arxiv else f"https://github.com/{entry['companion']}"
    lines = ["cff-version: 1.2.0", 'message: "If you use these programs or data, please cite the paper."',
             f"title: {json.dumps(entry['title'])}", "type: software", "authors:", *_person(reg["author"], "  "),
             "license: Apache-2.0", f"repository-code: {json.dumps('https://github.com/' + entry['companion'])}"]
    if archive:
        lines.append(f"version: {json.dumps(archive['version'])}")
    if entry.get("codeDoi"):
        lines.append(f"doi: {json.dumps(entry['codeDoi'])}")
    lines += ["preferred-citation:", "  type: article", f"  title: {json.dumps(entry['title'])}", "  authors:",
              *_person(reg["author"], "    "), f"  year: {year}", f"  url: {json.dumps(preferred_url)}"]
    if preferred_doi:
        lines.append(f"  doi: {json.dumps(preferred_doi)}")
    return "\n".join(lines) + "\n"


def zenodo(reg: dict, entry: dict, paragraphs: list[str]) -> str:
    related = []
    arxiv = (entry.get("arxiv") or {}).get("id")
    if arxiv:
        related.append({"identifier": "arXiv:" + re.sub(r"v\d+$", "", arxiv), "relation": "isSupplementTo",
                        "scheme": "arxiv", "resource_type": "publication-preprint"})
    if (entry.get("journal") or {}).get("doi"):
        related.append({"identifier": entry["journal"]["doi"], "relation": "isSupplementTo", "scheme": "doi",
                        "resource_type": "publication-article"})
    if entry.get("developmentRepository"):
        related.append({"identifier": "https://github.com/" + entry["developmentRepository"], "relation": "isSupplementedBy",
                        "scheme": "url", "resource_type": "software"})
    author = reg["author"]
    creator = {"name": f"{author['family-names']}, {author['given-names']}", "affiliation": author["affiliation"]}
    if author.get("orcid"):
        creator["orcid"] = author["orcid"]
    holds = ("This record holds the manuscript, a preprint that has not been peer reviewed, with the programs that check "
             "its results and their output. README.md describes each program and how to run it.")
    manuscript = ("The manuscript in paper/, including its figures, is licensed under Creative Commons Attribution 4.0 "
                  "International (CC BY 4.0)." if entry.get("textLicense") == "CC-BY-4.0"
                  else "The manuscript in paper/, including its figures, is all rights reserved.")
    components = (manuscript + " The programs in code/ and the data in data/ are licensed under the Apache License 2.0; "
                  "that license does not apply to the manuscript or its figures. Specific component notices and directory "
                  "licenses govern any exceptions; see LICENSE and NOTICE.")
    record = {
        "title": entry["title"], "upload_type": "publication", "publication_type": "preprint",
        "description": "".join(f"<p>{html.escape(part, quote=False)}</p>" for part in [*paragraphs, holds, components]),
        "creators": [creator],
        "license": "other-open" if entry.get("textLicense") == "CC-BY-4.0" else "other-closed",
    }
    if related:
        record["related_identifiers"] = related
    return json.dumps(record, indent=2, ensure_ascii=False) + "\n"


def license_text(root: Path, reg: dict, entry: dict, year: int) -> str:
    template = TEXT_LICENSES.get(entry.get("textLicense") or "all-rights-reserved")
    if not template:
        raise Refused(f"textLicense of {entry['id']} must be one of {', '.join(TEXT_LICENSES)}")
    return (template.format(year=year, name=reg["author"]["name"]) + "\n\nThe programs in code/ and the data in data/ are "
            "licensed under the Apache License, Version 2.0, whose text follows.\n\n"
            + (root / "licenses" / "Apache-2.0.txt").read_text(encoding="utf-8"))


def companion_data(root: Path, entry: dict) -> dict[str, bytes]:
    """The files the paper's numbers program says the companion needs from outside the paper folder."""
    program = entry.get("companionData")
    if not program:
        return {}
    path = root / "papers" / entry["id"] / program
    spec = importlib.util.spec_from_file_location(f"companion_data_{entry['id'].replace('-', '_')}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files = module.companion_data()
    for name in files:
        if name.startswith("/") or ".." in name.split("/") or not name.startswith("data/"):
            raise Refused(f"companionData of {entry['id']} gave a path outside data/: {name}")
    return files


def problems(directory: Path, reg: dict) -> list[str]:
    """Email addresses outside the manuscript, and Markdown links out of the paper folder."""
    allowed = {str(reg["author"].get("email", "")).lower()}
    out = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        name = path.relative_to(directory).as_posix()
        if BINARY.search(name) or name == "LICENSE":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\]\(\.\./", text):
            out.append(f"{name}: a Markdown link out of the paper folder")
        stray = {address for address in EMAIL.findall(text)
                 if not (name.startswith("paper/") and address.lower() in allowed)
                 and not re.search(r"@example\.(com|org|net)$", address, re.I)}
        if stray:
            out.append(f"{name}: email address {', '.join(sorted(stray))}")
    return out


def stage(root: Path, paper_id: str, directory: Path, *, reg: dict | None = None, year: int | None = None,
          files: list[str] | None = None) -> list[str]:
    reg = reg or registry(root)
    entry = paper(reg, paper_id)
    if not entry.get("companion"):
        raise Refused(f"paper {paper_id} has no companion repository in papers/papers.json")
    if directory.exists() and any(directory.iterdir()):
        raise Refused(f"{directory} is not empty")
    year = year or datetime.datetime.now(datetime.timezone.utc).year
    files = files if files is not None else tracked_files(root, paper_id)
    exclude = entry.get("companionExclude") or []
    required = ["README.md", "RELEASES.md", *[entry[key].removeprefix(f"papers/{paper_id}/")
                                              for key in ("pdf", "latex", "markdown") if entry.get(key)]]
    if any(name not in files or name in required for name in exclude):
        raise Refused(f"companionExclude must list tracked, non-manuscript files relative to papers/{paper_id}/")
    out = []
    for name in required:
        if name not in files:
            out.append(f"{name}: missing from papers/{paper_id}/ (or not committed)")
    for name in files:
        if name.startswith(PRIVATE_DIRS) or name in exclude or name in GENERATED:
            continue
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / "papers" / paper_id / name, target)
    for name, data in companion_data(root, entry).items():
        if (directory / name).exists():
            raise Refused(f"companionData {name} would overwrite a file of papers/{paper_id}/")
        (directory / name).parent.mkdir(parents=True, exist_ok=True)
        (directory / name).write_bytes(data)
    readme_path = directory / "README.md"
    if not readme_path.exists():
        raise Refused(f"papers/{paper_id}/README.md is missing")
    readme = companion_readme(readme_path.read_text(encoding="utf-8"), entry)
    readme_path.write_text(readme, encoding="utf-8")
    (directory / "LICENSE").write_text(license_text(root, reg, entry, year), encoding="utf-8")
    (directory / "CITATION.cff").write_text(citation(reg, entry, year), encoding="utf-8")
    paragraphs, abstract_problems = abstract_of(readme)
    (directory / ".zenodo.json").write_text(zenodo(reg, entry, paragraphs), encoding="utf-8")
    return out + abstract_problems + problems(directory, reg)


def check(root: Path, paper_id: str) -> list[str]:
    """Stage into a scratch folder, report problems, and run the paper's own check there, as a reader would."""
    with tempfile.TemporaryDirectory(prefix="companion-") as scratch:
        directory = Path(scratch) / "c"
        found = stage(root, paper_id, directory)
        entry = paper(registry(root), paper_id)
        if entry.get("companionData"):
            run = subprocess.run([sys.executable, "-I", entry["companionData"], "--check"], cwd=directory,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if run.returncode:
                found.append(f"{entry['companionData']} --check fails in the staged companion: {run.stdout.strip()}")
        return found


def notes(root: Path, paper_id: str, version: str) -> str:
    """The section of RELEASES.md headed "## <version>", the version without a leading v."""
    path = root / "papers" / paper_id / "RELEASES.md"
    if not path.exists():
        return ""
    want, found, out = version.removeprefix("v"), False, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if found:
                break
            found = line.split()[1] == want
            continue
        if found:
            out.append(line)
    return "\n".join(out).strip("\n") + ("\n" if out else "")


def quality_open(root: Path, paper_id: str) -> list[str]:
    """The quality items of notes/QUALITY.md that are open, missing, or checked without evidence."""
    path = root / "papers" / paper_id / "notes" / "QUALITY.md"
    if not path.exists():
        return ["notes/QUALITY.md is missing"]
    text = path.read_text(encoding="utf-8")
    out = []
    for item in QUALITY_ITEMS:
        match = re.search(r"^- \[( |x)\] \*\*" + item + r"\.[^*]*\*\*(.*)$", text, flags=re.M)
        if not match:
            out.append(f"{item}: missing from notes/QUALITY.md")
        elif match.group(1) != "x":
            out.append(f"{item}: open")
        elif len(match.group(2).strip()) < 40:
            out.append(f"{item}: checked without evidence")
    return out


def release_check(root: Path, paper_id: str) -> list[str]:
    entry = paper(registry(root), paper_id)
    found = [f"quality {line}" for line in quality_open(root, paper_id)]
    if ORDER.index(entry["status"]) < ORDER.index("ready"):
        found.append(f"status is {entry['status']}, not ready")
    return found + check(root, paper_id)


def main(argv: list[str]) -> int:
    try:
        if argv[:1] == ["--list"]:
            only = argv[2] if argv[1:2] == ["--paper"] and len(argv) > 2 else None
            for entry in ready(registry(), only or None):
                print(entry["id"], entry["companion"])
            return 0
        if argv[:1] == ["--stage"] and len(argv) == 3:
            found = stage(ROOT, argv[1], Path(argv[2]))
        elif argv[:1] == ["--check"] and len(argv) == 2:
            found = check(ROOT, argv[1])
        elif argv[:1] == ["--release-check"] and len(argv) == 2:
            found = release_check(ROOT, argv[1])
        elif argv[:1] == ["--companion"] and len(argv) == 2:
            print(paper(registry(), argv[1])["companion"])
            return 0
        elif argv[:1] == ["--notes"] and len(argv) == 3:
            sys.stdout.write(notes(ROOT, argv[1], argv[2]))
            return 0
        else:
            print(__doc__.strip(), file=sys.stderr)
            return 2
    except Refused as exc:
        print(f"paper_sync: {exc}", file=sys.stderr)
        return 1
    for line in found:
        print(line)
    if found:
        return 1
    if argv[0] != "--stage":
        print(f"{argv[1]}: no problems found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
