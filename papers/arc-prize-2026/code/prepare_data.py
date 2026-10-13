#!/usr/bin/env python3
# SPDX-License-Identifier: MIT-0
"""Separate public ARC challenges from scoring answers without displaying grids."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PIN = 'f3283f727488ad98fe575ea6a5ac981e4a188e49'
SALT = 'arc-prize-2026-v1:'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')

def prepare(source, destination):
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != PIN:
        raise ValueError('official dataset commit does not match the protocol')
    if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip():
        raise ValueError('official dataset checkout has local modifications')
    if destination.exists():
        raise ValueError('refusing to overwrite a prepared dataset')
    train = sorted((source / 'data/training').glob('*.json'))
    evaluation = sorted((source / 'data/evaluation').glob('*.json'))
    if len(train) != 1000 or len(evaluation) != 120:
        raise ValueError('unexpected dataset task counts')
    ranked = sorted(train, key=lambda p: hashlib.sha256((SALT + p.stem).encode()).hexdigest())
    partitions = {'development': ranked[:800], 'validation': ranked[800:], 'evaluation': evaluation}
    destination.mkdir(parents=True)
    manifest = {'schema': 'arc-data-v1', 'source_url': 'https://github.com/arcprize/ARC-AGI-2',
                'source_commit': commit, 'license': 'Apache-2.0', 'split_salt': SALT,
                'license_sha256': sha(source / 'LICENSE'), 'partitions': {}, 'incidental_exposure': {}}
    for split, paths in partitions.items():
        challenges, solutions, original = {}, {}, {}
        for path in sorted(paths):
            task = json.loads(path.read_text())
            task_id = path.stem
            challenges[task_id] = {'train': task['train'], 'test': [{'input': p['input']} for p in task['test']]}
            solutions[task_id] = [p['output'] for p in task['test']]
            original[task_id] = sha(path)
        cp, sp = destination / f'{split}_challenges.json', destination / f'{split}_solutions.json'
        dump(cp, challenges)
        dump(sp, solutions)
        manifest['partitions'][split] = {'ids': sorted(challenges), 'tasks': len(challenges),
            'test_inputs': sum(map(len, solutions.values())), 'task_sha256': original,
            'challenges_sha256': sha(cp), 'solutions_sha256': sha(sp)}
        if '4cd1b7b2' in challenges:
            manifest['incidental_exposure'] = {'task_id': '4cd1b7b2', 'partition': split,
                'scope': 'Earlier web lookup exposed a public training task before the protocol; no split reassignment.'}
    dump(destination / 'manifest.json', manifest)
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = prepare(args.source, args.output)
    print(json.dumps({k: {x: v[x] for x in ('tasks', 'test_inputs')} for k, v in result['partitions'].items()}))
    print(json.dumps(result['incidental_exposure']))
