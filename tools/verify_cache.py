"""Rerun frozen searches and compare them with engine/data/swarm_cache.

The unit tests read the frozen files, so a code change that would move a
score does not fail them. This script reruns each search, one process per
file, and reports a match, a mismatch, a timeout, or an error. It never
rewrites a frozen file. A match is a recomputation, not a reading.

    python3 tools/verify_cache.py                 # every frozen file
    python3 tools/verify_cache.py widths heavy    # only these names
    python3 tools/verify_cache.py --list          # names and modules
    python3 tools/verify_cache.py --timeout 600 --jobs 4
"""

from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "engine" / "data" / "swarm_cache"
sys.path.insert(0, str(ROOT))


def frozen_reports() -> dict[str, tuple[str, str]]:
    """Map each frozen name to (module, function)."""
    from engine.dagapeyeff_cache import frozen_registry

    return frozen_registry()


def _normal(value):
    return json.loads(json.dumps(value, sort_keys=True))


def differences(stored, fresh, path: str = "") -> list[str]:
    """List the paths where two JSON values differ."""
    if isinstance(stored, dict) and isinstance(fresh, dict):
        out = []
        for key in sorted(set(stored) | set(fresh)):
            where = f"{path}.{key}" if path else str(key)
            if key not in stored:
                out.append(f"{where}: missing from file, fresh {fresh[key]!r}")
            elif key not in fresh:
                out.append(f"{where}: missing from rerun, file {stored[key]!r}")
            else:
                out.extend(differences(stored[key], fresh[key], where))
        return out
    if isinstance(stored, list) and isinstance(fresh, list):
        if len(stored) != len(fresh):
            return [f"{path}: length {len(stored)} in file, {len(fresh)} in rerun"]
        out = []
        for index, (left, right) in enumerate(zip(stored, fresh)):
            out.extend(differences(left, right, f"{path}[{index}]"))
        return out
    if stored == fresh and type(stored) is type(fresh):
        return []
    return [f"{path}: file {stored!r}, rerun {fresh!r}"]


def _child(name: str, module_name: str, attr: str) -> int:
    module = importlib.import_module(module_name)
    fresh = _normal(getattr(module, attr).compute())
    stored = json.loads((CACHE / f"{name}.json").read_text(encoding="utf-8"))
    diff = differences(stored, fresh)
    print(json.dumps({"name": name, "diff": diff}))
    return 0


def _run_one(name: str, module_name: str, attr: str, timeout: float) -> dict:
    started = time.monotonic()
    try:
        done = subprocess.run(
            [sys.executable, __file__, "--child", name, module_name, attr],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "timeout", "seconds": round(time.monotonic() - started, 1)}
    seconds = round(time.monotonic() - started, 1)
    if done.returncode != 0:
        tail = (done.stderr or done.stdout).strip().splitlines()[-3:]
        return {"name": name, "status": "error", "seconds": seconds, "detail": tail}
    result = json.loads(done.stdout.strip().splitlines()[-1])
    status = "match" if not result["diff"] else "mismatch"
    return {"name": name, "status": status, "seconds": seconds, "detail": result["diff"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--child", nargs=3, metavar=("NAME", "MODULE", "ATTR"), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.child:
        return _child(*args.child)
    reports = frozen_reports()
    stored_names = {path.stem for path in CACHE.glob("*.json")}
    if args.list:
        for name in sorted(reports):
            print(f"{name}\t{reports[name][0]}.{reports[name][1]}")
        orphans = sorted(stored_names - set(reports))
        if orphans:
            print("files without a frozen function:", ", ".join(orphans))
        return 0
    wanted = args.names or sorted(reports)
    unknown = [name for name in wanted if name not in reports]
    if unknown:
        parser.error("unknown frozen name: " + ", ".join(unknown))
    missing_files = [name for name in wanted if name not in stored_names]
    if missing_files:
        parser.error("no frozen file for: " + ", ".join(missing_files))
    failed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(_run_one, name, *reports[name], args.timeout) for name in wanted]
        for future in futures:
            result = future.result()
            print(f"{result['status']:8} {result['seconds']:8.1f}s  {result['name']}", flush=True)
            for line in result.get("detail") or []:
                print(f"           {line}", flush=True)
            if result["status"] != "match":
                failed += 1
    print(f"{len(wanted) - failed} of {len(wanted)} frozen files reproduced")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
