#!/usr/bin/env python3
# SPDX-License-Identifier: MIT-0
"""Research evaluator for frozen ARC v1 protocol.
Generates all three policies from one solve_task receipt per task,
seals predictions before scoring, reports exact two-attempt accuracy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root
from engine.arc.solver import solve_task

def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def load_json(p):
    return json.loads(Path(p).read_text())

def evaluate(challenges_path, solutions_path, max_candidates=4096, seed=20261013):
    challenges = load_json(challenges_path)
    solutions = load_json(solutions_path)
    ids = sorted(challenges)  # stable
    predictions = {}
    receipts = {}
    start = time.perf_counter()
    peak_rss = 0
    for tid in ids:
        task = challenges[tid]
        receipt = solve_task(task, max_candidates=max_candidates)
        receipts[tid] = receipt
        policies = receipt['policies']
        predictions[tid] = {
            'first_programs': policies['first_programs'],
            'first_distinct': policies['first_distinct'],
            'group_vote': policies['group_vote'],
        }
        # track rss
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_rss = max(peak_rss, rss)
    elapsed = time.perf_counter() - start
    # seal predictions
    pred_path = Path(challenges_path).with_suffix('.predictions.json')
    pred_path.write_text(json.dumps(predictions, sort_keys=True, separators=(',', ':')) + '\n')
    pred_sha = sha(predictions)
    # now score
    def score(policy_name):
        correct_outputs = 0
        total_outputs = 0
        correct_tasks = 0
        for tid in ids:
            sols = solutions[tid]
            preds = predictions[tid][policy_name]
            task_ok = True
            for i, sol in enumerate(sols):
                total_outputs += 1
                attempts = [preds[i].get('attempt_1'), preds[i].get('attempt_2')]
                if any(a == sol for a in attempts if a is not None):
                    correct_outputs += 1
                else:
                    task_ok = False
            if task_ok:
                correct_tasks += 1
        return correct_outputs / total_outputs if total_outputs else 0, correct_tasks / len(ids) if ids else 0
    scores = {p: score(p) for p in ('first_programs', 'first_distinct', 'group_vote')}
    # bootstrap placeholder (full impl later)
    return {
        'n_tasks': len(ids),
        'n_outputs': sum(len(solutions[t]) for t in ids),
        'scores': {k: {'output_acc': v[0], 'task_acc': v[1]} for k, v in scores.items()},
        'elapsed_seconds': elapsed,
        'peak_rss_kb': peak_rss,
        'predictions_sha256': pred_sha,
        'protocol': 'arc-prize-2026-v1',
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--challenges', required=True)
    ap.add_argument('--solutions', required=True)
    ap.add_argument('--max-candidates', type=int, default=4096)
    args = ap.parse_args()
    result = evaluate(args.challenges, args.solutions, args.max_candidates)
    print(json.dumps(result, indent=2))
