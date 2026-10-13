# SPDX-License-Identifier: MIT-0
"""Bounded demonstration-consistent grid synthesis and auditable selection.

A compatible program is a hypothesis. Search-prefix agreement is not a proof;
conditional uniqueness requires complete enumeration and defined predictions
for every demonstration-consistent program on that test input.
"""
from __future__ import annotations

from collections import OrderedDict
from functools import lru_cache
import hashlib
import itertools
import json
from time import perf_counter

from . import dsl
from .grid import as_grid, shape, to_lists

POLICIES = ('first_programs', 'first_distinct', 'group_vote')


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _read_task(task):
    if not isinstance(task, dict):
        raise ValueError('task must be a dictionary')
    train, test = task.get('train'), task.get('test')
    if not isinstance(train, list) or not 1 <= len(train) <= 100:
        raise ValueError('task needs 1..100 demonstration pairs')
    if not isinstance(test, list) or not 1 <= len(test) <= 100:
        raise ValueError('task needs 1..100 test inputs')
    examples, queries = [], []
    for pair in train:
        if not isinstance(pair, dict) or 'input' not in pair or 'output' not in pair:
            raise ValueError('every demonstration needs input and output')
        examples.append((as_grid(pair['input']), as_grid(pair['output'])))
    for pair in test:
        if not isinstance(pair, dict) or 'input' not in pair:
            raise ValueError('every test pair needs input')
        queries.append(as_grid(pair['input']))
    # Test answers are intentionally neither validated, hashed nor consulted.
    return tuple(examples), tuple(queries)


def _witness(query, first, second):
    a, b = first['output'], second['output']
    mismatch = {'kind': 'shape', 'left': list(shape(a)), 'right': list(shape(b))}
    if shape(a) == shape(b):
        mismatch = next({'kind': 'cell', 'row': r, 'col': c, 'left': x, 'right': y}
                        for r, (ra, rb) in enumerate(zip(a, b))
                        for c, (x, y) in enumerate(zip(ra, rb)) if x != y)
    return {'input': to_lists(query), 'left_program': first['representative_program'],
            'right_program': second['representative_program'],
            'left_output': to_lists(a), 'right_output': to_lists(b), 'difference': mismatch,
            'meaning': 'Both programs match every demonstration but disagree on this test input.'}


def solve_task(task, max_candidates=4096, *, candidate_programs=None):
    """Return all three policies from one deterministic bounded candidate stream.

    `candidate_programs` optionally supplies a finite, explicit grammar for
    independent oracle tests. Literal duplicates are removed before counting.
    Missing attempts remain null; a competition adapter may add a clearly
    recorded fallback but must not call it a synthesized or forced answer.
    """
    started = perf_counter()
    if type(max_candidates) is not int or not 0 <= max_candidates <= 100000:
        raise ValueError('max_candidates must be an integer in 0..100000')
    training, queries = _read_task(task)
    atoms = dsl.primitives(training)
    if candidate_programs is None:
        total = dsl.grammar_size(atoms)
        stream = dsl.programs(atoms)
        grammar_hash = dsl.grammar_sha256(atoms)
        grammar_name = 'arc-dsl-v1'
    else:
        if not isinstance(candidate_programs, (list, tuple)) or len(candidate_programs) > 100000:
            raise ValueError('candidate_programs must be an explicit finite list with at most 100000 entries')
        if any(not isinstance(p, dsl.Program) or p.cost > 2 for p in candidate_programs):
            raise ValueError('explicit candidates must be Program objects of depth at most 2')
        pool = tuple(dict.fromkeys(candidate_programs))
        total, stream = len(pool), iter(pool)
        grammar_hash = _digest([p.to_dict() for p in pool])
        grammar_name = 'explicit-finite-grammar'
    groups = [OrderedDict() for _ in queries]
    first_predictions = [[] for _ in queries]
    undefined = [0 for _ in queries]
    candidates, checks, train_checks, fully_defined = [], 0, 0, 0
    applications = 0
    trace = hashlib.sha256()

    @lru_cache(maxsize=8192)
    def execute_atom(atom, grid):
        nonlocal applications
        applications += 1
        return dsl.apply_atom(atom, grid)

    def execute(program, grid):
        for atom in program.steps:
            grid = execute_atom(atom, grid)
            if grid is None:
                return None
        return grid

    for program in itertools.islice(stream, max_candidates):
        checks += 1
        trace.update((program.key + '\n').encode())
        for source, target in training:
            train_checks += 1
            if execute(program, source) != target:
                break
        else:
            group_ids, all_defined = [], True
            for idx, query in enumerate(queries):
                output = execute(program, query)
                if output is None:
                    undefined[idx] += 1
                    all_defined = False
                    group_ids.append(None)
                    continue
                if len(first_predictions[idx]) < 2:
                    first_predictions[idx].append(output)
                if output not in groups[idx]:
                    groups[idx][output] = {'group_id': len(groups[idx]), 'output': output,
                                          'program_votes': 0, 'representative_program': program.to_dict(),
                                          'representative_cost': program.cost, 'representative_key': program.key,
                                          'first_candidate_index': checks - 1}
                group = groups[idx][output]
                group['program_votes'] += 1
                if (program.cost, program.key) < (group['representative_cost'], group['representative_key']):
                    group.update(representative_cost=program.cost, representative_key=program.key,
                                 representative_program=program.to_dict())
                group_ids.append(group['group_id'])
            fully_defined += all_defined
            candidates.append({'program': program.to_dict(), 'cost': program.cost, 'output_group_ids': group_ids})
    complete = checks == total
    policies = {name: [] for name in POLICIES}
    ambiguity = []
    for idx, by_output in enumerate(groups):
        ordered = list(by_output.values())
        voted = sorted(ordered, key=lambda g: (-g['program_votes'], g['representative_cost'], g['representative_key']))
        choices = {'first_programs': first_predictions[idx],
                   'first_distinct': [g['output'] for g in ordered[:2]],
                   'group_vote': [g['output'] for g in voted[:2]]}
        for policy, outputs in choices.items():
            policies[policy].append({f'attempt_{j + 1}': to_lists(outputs[j]) if j < len(outputs) else None
                                    for j in range(2)})
        if len(ordered) > 1:
            status = 'ambiguous'
        elif not ordered:
            status = 'undefined_test' if candidates else ('no_solution_within_declared_grammar' if complete else 'unknown')
        elif complete and undefined[idx] == 0:
            status = 'unique_within_declared_grammar'
        else:
            status = 'incomplete_agreement' if not complete else 'agreement_with_undefined_hypotheses'
        public_groups = [{k: to_lists(v) if k == 'output' else v
                          for k, v in group.items() if k != 'representative_key'} for group in ordered]
        ambiguity.append({'test_index': idx, 'status': status, 'distinct_output_groups': len(ordered),
                          'undefined_consistent_programs': undefined[idx], 'groups': public_groups,
                          'witness': _witness(queries[idx], ordered[0], ordered[1]) if len(ordered) > 1 else None})
    info = execute_atom.cache_info()
    return {'schema': 'arc-synthesis-receipt-v1', 'policies': policies, 'test_ambiguity': ambiguity,
            'candidates': candidates,
            'input_sha256': _digest({'train': training, 'test_inputs': queries}),
            'search': {'candidate_checks': checks, 'candidate_budget': max_candidates,
                       'grammar_size': total, 'grammar_sha256': grammar_hash, 'grammar': grammar_name,
                       'maximum_depth': 2, 'search_complete': complete,
                       'stop_reason': 'grammar_exhausted' if complete else 'candidate_budget',
                       'train_consistent': len(candidates), 'fully_defined_candidates': fully_defined,
                       'primitive_count': len(atoms), 'training_pair_checks': train_checks,
                       'primitive_applications': applications, 'primitive_cache_hits': info.hits,
                       'candidate_trace_sha256': trace.hexdigest(), 'elapsed_seconds': perf_counter() - started},
            'scope': 'Predictions are hypotheses within a finite grid grammar. Votes are program counts, not probabilities. '
                     'Test answers are not used. Search exhaustion does not establish general ARC correctness.'}
