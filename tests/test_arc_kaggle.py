"""Competition adapter controls use only constructed grids, never ARC holdouts."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "papers/arc-prize-2026/kaggle"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = load_module("arc_submission_adapter_test", PACKAGE / "adapter.py")
builder = load_module("arc_notebook_builder_test", PACKAGE / "build_notebook.py")


def fixture():
    return {"synthetic": {"train": [{"input": [[1, 0]], "output": [[0, 1]]}],
                          "test": [{"input": [[2, 0]]}, {"input": [[3], [0]]}]}}


def receipt(predictions):
    return {"policies": {"group_vote": predictions},
            "search": {"search_complete": False, "stop_reason": "candidate_budget"},
            "test_ambiguity": []}


class AdapterTests(unittest.TestCase):
    def test_test_labels_and_other_fields_never_reach_solver(self):
        tasks = fixture()
        tasks["synthetic"]["test"][0]["output"] = [[9]]
        tasks["synthetic"]["secret"] = "not a feature"
        original = copy.deepcopy(tasks)
        seen = []

        def solve(task, max_candidates):
            seen.append(copy.deepcopy(task))
            task["test"][0]["input"][0][0] = 9
            return receipt([{"attempt_1": None, "attempt_2": [[0, 2]]},
                            {"attempt_1": [[0], [3]], "attempt_2": None}])

        output, audit = adapter.make_submission(tasks, solve=solve, max_candidates=7)
        self.assertEqual(tasks, original)
        self.assertEqual(set(seen[0]), {"train", "test"})
        self.assertEqual(set(seen[0]["test"][0]), {"input"})
        self.assertEqual(output["synthetic"][0]["attempt_1"], [[2, 0]])
        self.assertEqual(output["synthetic"][1]["attempt_1"], [[0], [3]])
        self.assertEqual(audit["fallback_attempt_count"], 2)
        self.assertEqual(audit["max_candidates_per_task"], 7)
        self.assertFalse(audit["tasks"]["synthetic"]["search"]["search_complete"])
        self.assertEqual(audit["submission_sha256"], adapter.canonical_hash(output))

    def test_all_unavailable_predictions_are_tagged_legal_fallbacks(self):
        output, audit = adapter.make_submission(
            fixture(), solve=lambda *args, **kwargs: receipt(
                [{"attempt_1": None, "attempt_2": None}] * 2))
        self.assertEqual(audit["fallback_attempt_count"], 4)
        adapter.validate_submission(fixture(), output)
        self.assertEqual(output["synthetic"][1]["attempt_2"], [[3], [0]])

    def test_predictions_preserve_test_order_and_do_not_alias(self):
        grid = [[4]]
        output, audit = adapter.make_submission(
            fixture(), solve=lambda *args, **kwargs: receipt(
                [{"attempt_1": grid, "attempt_2": grid},
                 {"attempt_1": [[5]], "attempt_2": [[6]]}]))
        self.assertEqual(audit["fallback_attempt_count"], 0)
        output["synthetic"][0]["attempt_1"][0][0] = 8
        self.assertEqual(grid, [[4]])
        self.assertEqual(output["synthetic"][0]["attempt_2"], [[4]])
        self.assertEqual(output["synthetic"][1]["attempt_1"], [[5]])

    def test_malformed_predictions_fail_instead_of_becoming_fallbacks(self):
        bad = [[], [{"attempt_1": None}],
               [{"attempt_1": [[True]], "attempt_2": [[1]]}] * 2,
               [{"attempt_1": [[10]], "attempt_2": [[1]]}] * 2,
               [{"attempt_1": [[1], [2, 3]], "attempt_2": [[1]]}] * 2]
        for predictions in bad:
            with self.subTest(predictions=predictions), self.assertRaises(ValueError):
                adapter.make_submission(fixture(), solve=lambda *a, **kw: receipt(predictions))

    def test_submission_requires_exact_ids_attempt_names_and_test_count(self):
        good, _ = adapter.make_submission(fixture(), solve=lambda *a, **kw: receipt(
            [{"attempt_1": None, "attempt_2": None}] * 2))
        bad = [{}, dict(good, extra=[]), {"synthetic": good["synthetic"][:1]},
               {"synthetic": [{"attempt_1": [[1]], "attempt_2": [[1]], "extra": 2}] * 2}]
        for output in bad:
            with self.subTest(output=output), self.assertRaises(ValueError):
                adapter.validate_submission(fixture(), output)

    def test_grid_validation_enforces_all_bounds(self):
        for bad in ([], [[]], [[0]] * 31, [[0] * 31], [[-1]], [[1.0]], [[False]], "1"):
            with self.subTest(grid=bad), self.assertRaises(ValueError):
                adapter.validate_grid(bad, "control")
        adapter.validate_grid([[0] * 30 for _ in range(30)], "maximum")

    def test_bad_budget_policy_and_tasks_rejected(self):
        for budget in (-1, True, 1.0):
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                adapter.make_submission(fixture(), max_candidates=budget)
        with self.assertRaises(ValueError):
            adapter.make_submission(fixture(), policy="invented")
        for bad in ({}, [], {"task": {"train": [], "test": []}}):
            with self.subTest(task=bad), self.assertRaises(ValueError):
                adapter.make_submission(bad)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.json"
            path.write_text('{"same":1,"same":2}')
            with self.assertRaises(ValueError):
                adapter.load_json(path)

    def test_input_cannot_be_overwritten_as_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.json"
            path.write_text(json.dumps(fixture()))
            with self.assertRaises(ValueError):
                adapter.run_file(path, path, Path(temporary) / "audit.json")

    def test_failed_rerun_removes_stale_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path, output_path, audit_path = [root / name for name in
                                                  ("input.json", "submission.json", "audit.json")]
            input_path.write_text("not JSON")
            output_path.write_text("old output")
            audit_path.write_text("old audit")
            with self.assertRaises(ValueError):
                adapter.run_file(input_path, output_path, audit_path)
            self.assertFalse(output_path.exists())
            self.assertFalse(audit_path.exists())

    def test_documented_cli_imports_checkout_without_pythonpath(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            input_path.write_text(json.dumps(fixture()))
            proc = subprocess.run([sys.executable, "-I", str(PACKAGE / "adapter.py"),
                                   "--input", str(input_path), "--output", str(root / "submission.json"),
                                   "--audit", str(root / "audit.json"), "--max-candidates", "0"],
                                  cwd=root, capture_output=True, text=True, timeout=30,
                                  env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["fallback_attempt_count"], 4)


class NotebookTests(unittest.TestCase):
    def synthetic_repo(self, root):
        package = root / "engine/arc"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text('''def solve_task(task, max_candidates=4096):
    assert all(set(pair) == {"input"} for pair in task["test"])
    return {"policies": {"group_vote": [{"attempt_1": None, "attempt_2": None}
            for pair in task["test"]]}, "search": {"candidate_checks": 0}, "test_ambiguity": []}
''')
        destination = root / "papers/arc-prize-2026/kaggle"
        destination.mkdir(parents=True)
        (destination / "adapter.py").write_bytes((PACKAGE / "adapter.py").read_bytes())

    def test_private_cpu_offline_metadata_and_deterministic_notebook(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.synthetic_repo(root)
            first, manifest = builder.build_notebook(repo_root=root)
            second, _ = builder.build_notebook(repo_root=root)
            self.assertEqual(first, second)
            self.assertIn("engine/arc/__init__.py", manifest["embedded_source_sha256"])
            builder.write_bundle(root / "bundle", kernel_id="synthetic-owner/synthetic-notebook", repo_root=root)
            metadata = json.loads((root / "bundle/kernel-metadata.json").read_text())
            self.assertTrue(metadata["is_private"])
            self.assertFalse(metadata["enable_gpu"])
            self.assertFalse(metadata["enable_internet"])
            self.assertEqual(metadata["competition_sources"], [builder.COMPETITION])
            self.assertEqual(metadata["dataset_sources"], [])
            self.assertTrue(all(not cell.get("outputs") for cell in first["cells"]))

    def test_notebook_executes_embedded_source_in_clean_offline_process(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.synthetic_repo(root)
            notebook, _ = builder.build_notebook(repo_root=root, max_candidates=0)
            tasks = fixture()
            tasks["synthetic"]["test"][0]["output"] = [[9]]
            input_path = root / "input.json"
            input_path.write_text(json.dumps(tasks))
            code = "\n".join("".join(cell["source"]) for cell in notebook["cells"]
                             if cell["cell_type"] == "code")
            # Python's audit hook prevents network operations, including DNS.
            blocker = "import sys\ndef deny(event, args):\n    if event.startswith('socket.'):\n        raise RuntimeError('network forbidden')\nsys.addaudithook(deny)\n"
            script = root / "run.py"
            script.write_text(blocker + code)
            env = dict(os.environ, ARC_INPUT_PATH=str(input_path), ARC_WORK_DIR=str(root / "run"),
                       PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run([sys.executable, "-I", str(script)], env=env, cwd=root,
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            output = json.loads((root / "run/submission.json").read_text())
            adapter.validate_submission(tasks, output)
            audit = json.loads((root / "run/submission-audit.json").read_text())
            self.assertEqual(audit["fallback_attempt_count"], 4)
            self.assertEqual(audit["max_candidates_per_task"], 0)
            self.assertTrue((root / "run/source-manifest.json").is_file())
            manifest = json.loads((root / "run/source-manifest.json").read_text())
            self.assertEqual(audit["source_manifest_sha256"], adapter.canonical_hash(manifest))

    def test_missing_sources_and_invalid_kernel_ids_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                builder.build_notebook(repo_root=Path(temporary))
            for kernel_id in ("", "../name", "user/name/extra", "user/space name"):
                with self.subTest(kernel_id=kernel_id), self.assertRaises(ValueError):
                    builder.write_bundle(Path(temporary), kernel_id=kernel_id)

    def test_source_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.synthetic_repo(root)
            (root / "engine/arc/linked.py").symlink_to(root / "engine/arc/__init__.py")
            with self.assertRaises(ValueError):
                builder.build_notebook(repo_root=root)

    def test_real_embedded_solver_recovers_constructed_rotation_offline(self):
        notebook, manifest = builder.build_notebook(repo_root=ROOT, max_candidates=8)
        tasks = {"constructed_rotation": {
            "train": [{"input": [[1, 2, 3], [4, 5, 6]],
                       "output": [[4, 1], [5, 2], [6, 3]]}],
            "test": [{"input": [[1, 2], [3, 4], [5, 6]]}]}}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            input_path.write_text(json.dumps(tasks))
            code = "\n".join("".join(cell["source"]) for cell in notebook["cells"]
                             if cell["cell_type"] == "code")
            blocker = "import sys\ndef deny(event, args):\n    if event.startswith('socket.'):\n        raise RuntimeError('network forbidden')\nsys.addaudithook(deny)\n"
            script = root / "run.py"
            script.write_text(blocker + code)
            proc = subprocess.run([sys.executable, "-I", str(script)], cwd=root,
                                  env=dict(os.environ, ARC_INPUT_PATH=str(input_path),
                                           ARC_WORK_DIR=str(root / "output"), PYTHONDONTWRITEBYTECODE="1"),
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            output = json.loads((root / "output/submission.json").read_text())
            self.assertEqual(output["constructed_rotation"][0]["attempt_1"],
                             [[5, 3, 1], [6, 4, 2]])
            audit = json.loads((root / "output/submission-audit.json").read_text())
            self.assertEqual(audit["source_manifest_sha256"], adapter.canonical_hash(manifest))
            self.assertEqual(audit["tasks"]["constructed_rotation"]["search"]["candidate_checks"], 8)
            self.assertFalse(audit["tasks"]["constructed_rotation"]["search"]["search_complete"])


if __name__ == "__main__":
    unittest.main()
