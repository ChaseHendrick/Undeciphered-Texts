"""Offline ARC-AGI-2 competition adapter, with explicit fallback accounting.

New project-authored code. This module does not score predictions, submit an
entry, accept rules, or turn an incomplete search into a correctness claim.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

POLICIES = ("first_programs", "first_distinct", "group_vote")
ATTEMPTS = ("attempt_1", "attempt_2")


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_grid(grid: Any, label: str) -> None:
    if not isinstance(grid, list) or not 1 <= len(grid) <= 30:
        raise ValueError(f"{label}: grid must have 1..30 rows")
    width = None
    for row in grid:
        if not isinstance(row, list) or not 1 <= len(row) <= 30:
            raise ValueError(f"{label}: row must have 1..30 cells")
        if width is None:
            width = len(row)
        if len(row) != width:
            raise ValueError(f"{label}: grid must be rectangular")
        if any(type(cell) is not int or not 0 <= cell <= 9 for cell in row):
            raise ValueError(f"{label}: cells must be integers 0..9")


def solver_task(task: Any, task_id: str) -> dict:
    """Copy only permitted fields; never forward test outputs to the solver."""
    if not isinstance(task, dict):
        raise ValueError(f"{task_id}: task must be an object")
    result = {}
    for split in ("train", "test"):
        pairs = task.get(split)
        if not isinstance(pairs, list) or not pairs:
            raise ValueError(f"{task_id}: {split} must be a nonempty list")
        clean = []
        for i, pair in enumerate(pairs):
            if not isinstance(pair, dict) or "input" not in pair:
                raise ValueError(f"{task_id}.{split}[{i}]: input required")
            validate_grid(pair["input"], f"{task_id}.{split}[{i}].input")
            item = {"input": copy.deepcopy(pair["input"])}
            if split == "train":
                if "output" not in pair:
                    raise ValueError(f"{task_id}.train[{i}]: output required")
                validate_grid(pair["output"], f"{task_id}.train[{i}].output")
                item["output"] = copy.deepcopy(pair["output"])
            clean.append(item)
        result[split] = clean
    return result


def validate_submission(challenges: dict, submission: Any) -> None:
    """Check IDs, test ordering/counts, attempt names, grid shape and colors."""
    if not isinstance(submission, dict) or set(submission) != set(challenges):
        raise ValueError("submission task IDs must exactly match challenge IDs")
    for task_id, task in challenges.items():
        answers = submission[task_id]
        if not isinstance(answers, list) or len(answers) != len(task["test"]):
            raise ValueError(f"{task_id}: one answer object required per test input")
        for i, answer in enumerate(answers):
            if not isinstance(answer, dict) or set(answer) != set(ATTEMPTS):
                raise ValueError(f"{task_id}[{i}]: exactly attempt_1 and attempt_2 required")
            for attempt in ATTEMPTS:
                validate_grid(answer[attempt], f"{task_id}[{i}].{attempt}")


def make_submission(
    challenges: Any,
    *,
    max_candidates: int = 4096,
    policy: str = "group_vote",
    solve: Callable | None = None,
) -> tuple[dict, dict]:
    if type(max_candidates) is not int or max_candidates < 0:
        raise ValueError("max_candidates must be a nonnegative integer")
    if policy not in POLICIES:
        raise ValueError(f"policy must be one of {POLICIES}")
    if not isinstance(challenges, dict) or not challenges:
        raise ValueError("challenges must be a nonempty task-ID mapping")
    if any(not isinstance(key, str) or not key for key in challenges):
        raise ValueError("challenge task IDs must be nonempty strings")
    clean_tasks = {key: solver_task(value, key) for key, value in challenges.items()}
    if solve is None:
        from engine.arc import solve_task

        solve = solve_task
    submission, tasks = {}, {}
    fallback_count = 0
    for task_id in sorted(clean_tasks):
        task = clean_tasks[task_id]
        # Defensive copy keeps a solver mutation from changing the fallback or seal.
        receipt = solve(copy.deepcopy(task), max_candidates=max_candidates)
        if not isinstance(receipt, dict):
            raise ValueError(f"{task_id}: solver receipt must be an object")
        predictions = receipt.get("policies", {}).get(policy)
        if not isinstance(predictions, list) or len(predictions) != len(task["test"]):
            raise ValueError(f"{task_id}: solver policy must cover every test input")
        answers, fallback = [], []
        for i, prediction in enumerate(predictions):
            if not isinstance(prediction, dict) or set(prediction) != set(ATTEMPTS):
                raise ValueError(f"{task_id}[{i}]: malformed solver attempt object")
            answer = {}
            for attempt in ATTEMPTS:
                grid = prediction[attempt]
                if grid is None:
                    grid = task["test"][i]["input"]
                    fallback.append({"test_index": i, "attempt": attempt,
                                     "reason": "solver_prediction_unavailable",
                                     "rule": "copy_test_input"})
                validate_grid(grid, f"{task_id}[{i}].{attempt}")
                answer[attempt] = copy.deepcopy(grid)
            answers.append(answer)
        submission[task_id] = answers
        fallback_count += len(fallback)
        tasks[task_id] = {
            "task_sha256": canonical_hash(task),
            "predictions_sha256": canonical_hash(answers),
            "search": receipt.get("search"),
            "test_ambiguity": receipt.get("test_ambiguity"),
            "solver_receipt_sha256": canonical_hash(receipt),
            "fallbacks": fallback,
        }
    validate_submission(clean_tasks, submission)
    audit = {
        "schema_version": 1,
        "status": "local_output_validated_not_submitted",
        "policy": policy,
        "max_candidates_per_task": max_candidates,
        "fallback_rule": "copy_test_input",
        "fallback_attempt_count": fallback_count,
        "task_count": len(submission),
        "test_input_count": sum(len(task["test"]) for task in clean_tasks.values()),
        "challenges_sha256": canonical_hash(clean_tasks),
        "submission_sha256": canonical_hash(submission),
        "tasks": tasks,
    }
    return submission, audit


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)


def run_file(input_path: str | Path, output_path: str | Path, audit_path: str | Path,
             *, max_candidates: int = 4096, policy: str = "group_vote",
             source_manifest: dict | None = None) -> dict:
    paths = [Path(path).resolve() for path in (input_path, output_path, audit_path)]
    if len(set(paths)) != 3:
        raise ValueError("input, submission and audit paths must be distinct")
    # A failed rerun must not leave an older submission looking current.
    for path in paths[1:]:
        path.unlink(missing_ok=True)
    submission, audit = make_submission(load_json(input_path),
                                        max_candidates=max_candidates, policy=policy)
    if source_manifest is not None:
        audit["source_manifest_sha256"] = canonical_hash(source_manifest)
    # An exception fails the run. It never silently replaces a broken solver.
    for path, value in ((Path(audit_path), audit), (Path(output_path), submission)):
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n",
                             encoding="utf-8")
        temporary.replace(path)
    return audit


def main() -> None:
    # Direct script execution puts this directory, not the checkout root, on
    # sys.path. The notebook imports this module and never uses this branch.
    import sys

    checkout = Path(__file__).resolve().parents[3]
    if (checkout / "engine/arc/__init__.py").is_file():
        sys.path.insert(0, str(checkout))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("submission.json"))
    parser.add_argument("--audit", type=Path, default=Path("submission-audit.json"))
    parser.add_argument("--max-candidates", type=int, default=4096)
    parser.add_argument("--policy", choices=POLICIES, default="group_vote")
    args = parser.parse_args()
    audit = run_file(args.input, args.output, args.audit,
                     max_candidates=args.max_candidates, policy=args.policy)
    print(json.dumps({key: audit[key] for key in
                      ("status", "task_count", "test_input_count", "fallback_attempt_count",
                       "submission_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
