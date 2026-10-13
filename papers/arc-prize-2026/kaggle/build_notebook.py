"""Build a source-sealed, self-contained CPU Kaggle notebook. Does not upload."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COMPETITION = "arc-prize-2026-arc-agi-2"
# Verified 13 October 2026 from a live competition notebook. The directory is
# competitions/<slug>, not the slug alone.
COMPETITION_CHALLENGES = (
    "/kaggle/input/competitions/arc-prize-2026-arc-agi-2/arc-agi_test_challenges.json"
)
POLICIES = ("first_programs", "first_distinct", "group_vote")


def _cell(kind: str, source: str) -> dict:
    result = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def build_notebook(*, repo_root: Path = ROOT, max_candidates: int = 4096,
                   policy: str = "group_vote") -> tuple[dict, dict]:
    if type(max_candidates) is not int or max_candidates < 0:
        raise ValueError("max_candidates must be a nonnegative integer")
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    root = Path(repo_root).resolve()
    package = root / "engine/arc"
    if not (package / "__init__.py").is_file():
        raise ValueError("engine/arc/__init__.py is required")
    # Only the isolated ARC package is embedded, never repository data or secrets.
    sources = {"engine/__init__.py": "# Isolated namespace for the embedded ARC package.\n"}
    for path in sorted(package.rglob("*.py")):
        if path.is_symlink() or not path.resolve().is_relative_to(package.resolve()):
            raise ValueError("ARC source must not contain symlinks")
        sources[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    adapter = root / "papers/arc-prize-2026/kaggle/adapter.py"
    sources["arc_kaggle_adapter.py"] = adapter.read_text(encoding="utf-8")
    for path, source in sources.items():
        compile(source, path, "exec")
    hashes = {name: hashlib.sha256(source.encode("utf-8")).hexdigest()
              for name, source in sources.items()}
    manifest = {
        "schema_version": 1,
        "competition": COMPETITION,
        "policy": policy,
        "max_candidates_per_task": max_candidates,
        "embedded_source_sha256": hashes,
        "namespace_note": "engine/__init__.py is a minimal generated namespace, not the cipher engine initializer",
        "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    setup = """import hashlib, json, os, sys
from pathlib import Path

""" + "SOURCES = " + repr(sources) + "\n" + "SOURCE_MANIFEST = " + repr(manifest) + "\n" + """
# Test overrides are used only by local fixtures. Kaggle uses /kaggle/working.
WORK = Path(os.environ.get("ARC_WORK_DIR", "/kaggle/working"))
WORK.mkdir(parents=True, exist_ok=True)
SOURCE_ROOT = WORK / "_arc_source"
for relative, source in SOURCES.items():
    expected = SOURCE_MANIFEST["embedded_source_sha256"][relative]
    if hashlib.sha256(source.encode("utf-8")).hexdigest() != expected:
        raise ValueError("embedded source hash mismatch: " + relative)
    target = SOURCE_ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
for name in list(sys.modules):
    if name == "engine" or name.startswith("engine.") or name == "arc_kaggle_adapter":
        del sys.modules[name]
sys.path.insert(0, str(SOURCE_ROOT))
from arc_kaggle_adapter import run_file
(WORK / "source-manifest.json").write_text(json.dumps(SOURCE_MANIFEST, sort_keys=True, indent=2) + "\\n")
"""
    run = (
        "# The competition supplies the test challenge file at rerun time.\n"
        "INPUT = Path(os.environ.get(\"ARC_INPUT_PATH\",\n"
        f"    \"{COMPETITION_CHALLENGES}\"))\n"
        "audit = run_file(INPUT, WORK / \"submission.json\", WORK / \"submission-audit.json\",\n"
        "    max_candidates=SOURCE_MANIFEST[\"max_candidates_per_task\"],\n"
        "    policy=SOURCE_MANIFEST[\"policy\"], source_manifest=SOURCE_MANIFEST)\n"
        "print(json.dumps({key: audit[key] for key in\n"
        "    (\"status\", \"task_count\", \"test_input_count\", \"fallback_attempt_count\", \"submission_sha256\")},\n"
        "    sort_keys=True, indent=2))\n"
    )
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
        },
        "cells": [
            _cell("markdown", "# Bounded Ambiguity in ARC Program Search\n\nOffline, CPU-only inference from the embedded source manifest. "
                  "This notebook writes two legal attempts per test input. Unavailable solver predictions use "
                  "an explicitly audited input-copy fallback. A successful run establishes an output format check, "
                  "not a leaderboard score or a paper acceptance.\n"),
            _cell("code", setup),
            _cell("code", run),
        ],
    }
    for i, cell in enumerate(notebook["cells"]):
        cell["id"] = f"arc-{i:02d}"
    return notebook, manifest


def write_bundle(output_dir: Path, *, kernel_id: str, repo_root: Path = ROOT,
                 max_candidates: int = 4096, policy: str = "group_vote") -> dict:
    if not re.fullmatch(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", kernel_id):
        raise ValueError("kernel_id must be the actual username/notebook-slug")
    notebook, manifest = build_notebook(repo_root=repo_root, max_candidates=max_candidates, policy=policy)
    metadata = {
        "id": kernel_id,
        "title": "Bounded Ambiguity in ARC Program Search",
        "code_file": "arc-prize-2026.ipynb",
        "language": "python", "kernel_type": "notebook",
        "is_private": True, "enable_gpu": False, "enable_internet": False,
        "dataset_sources": [], "competition_sources": [COMPETITION],
        "kernel_sources": [], "model_sources": [],
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in (("arc-prize-2026.ipynb", notebook),
                        ("kernel-metadata.json", metadata), ("source-manifest.json", manifest)):
        path = output_dir / name
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n",
                             encoding="utf-8")
        temporary.replace(path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--kernel-id", required=True)
    parser.add_argument("--max-candidates", type=int, default=4096)
    parser.add_argument("--policy", choices=POLICIES, default="group_vote")
    args = parser.parse_args()
    manifest = write_bundle(args.output_dir, kernel_id=args.kernel_id,
                            max_candidates=args.max_candidates, policy=args.policy)
    print(json.dumps({"status": "built_locally_not_uploaded", "source_files": len(manifest["embedded_source_sha256"]),
                      "output_dir": str(args.output_dir)}, sort_keys=True))


if __name__ == "__main__":
    main()
