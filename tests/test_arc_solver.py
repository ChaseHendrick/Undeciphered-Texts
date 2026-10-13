# SPDX-License-Identifier: MIT-0
"""Known-answer, ambiguity and exhaustive finite-grammar controls for ARC."""
import copy
import itertools
import json
import unittest

from engine.arc import POLICIES, solve_task
from engine.arc.dsl import Atom, Program, apply_atom, apply_program, grammar_size, primitives, programs
from engine.arc.grid import as_grid, components


def program(*names):
    return Program(tuple(Atom(name) if isinstance(name, str) else Atom(*name) for name in names))


def task(source, target, query):
    return {'train': [{'input': source, 'output': target}], 'test': [{'input': query}]}


class GridDSLTests(unittest.TestCase):
    def test_grid_validation(self):
        for invalid in ([], [[]], [[1], [1, 2]], [[True]], [[1.0]], [[10]], [[-1]], [[0] * 31], [[0]] * 31, '1'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                as_grid(invalid)
        self.assertEqual(as_grid([[0, 9]]), ((0, 9),))

    def test_operation_validation(self):
        for name, args in [('exec', ()), ('rot90', (1,)), ('replace', (1, 20)), ('scale', (True,)),
                           ('component', (0, 1, 'largest')), ('crop_color', ('mode',)), ('color_map', (1,))]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                Atom(name, args)

    def test_rectangular_d4_literal_answers(self):
        source = as_grid([[1, 2, 3], [4, 5, 6]])
        expected = {'identity': [[1, 2, 3], [4, 5, 6]], 'rot90': [[4, 1], [5, 2], [6, 3]],
                    'rot180': [[6, 5, 4], [3, 2, 1]], 'rot270': [[3, 6], [2, 5], [1, 4]],
                    'flip_rows': [[4, 5, 6], [1, 2, 3]], 'flip_cols': [[3, 2, 1], [6, 5, 4]],
                    'transpose': [[1, 4], [2, 5], [3, 6]], 'anti_transpose': [[6, 3], [5, 2], [4, 1]]}
        for name, answer in expected.items():
            self.assertEqual(apply_atom(Atom(name), source), as_grid(answer), name)

    def test_color_crop_and_background_conventions(self):
        grid = as_grid([[0, 0, 0], [0, 2, 3], [0, 0, 0]])
        self.assertEqual(apply_atom(Atom('crop_background', (0,)), grid), ((2, 3),))
        self.assertEqual(apply_atom(Atom('crop_background', ('mode',)), grid), ((2, 3),))
        self.assertEqual(apply_atom(Atom('crop_color', (2,)), grid), ((2,),))
        self.assertIsNone(apply_atom(Atom('crop_color', (9,)), grid))
        self.assertEqual(apply_atom(Atom('swap', (2, 3)), ((2, 3, 0),)), ((3, 2, 0),))

    def test_objects_have_explicit_connectivity_and_ties(self):
        grid = as_grid([[1, 2, 0, 3], [0, 0, 0, 3], [4, 0, 5, 0]])
        self.assertEqual(len(components(grid, 0, True)), 5)
        self.assertEqual(len(components(grid, 0, False)), 4)
        self.assertEqual(apply_atom(Atom('component', (0, True, 'largest')), grid), ((3,), (3,)))
        self.assertEqual(apply_atom(Atom('component', (0, True, 'smallest')), grid), ((1,),))
        ring = as_grid([[2, 2, 2], [2, 3, 2], [2, 2, 2]])
        self.assertEqual(apply_atom(Atom('component', (0, True, 'largest')), ring),
                         ((2, 2, 2), (2, 0, 2), (2, 2, 2)))

    def test_scale_tile_repetition_and_compression(self):
        grid = ((1, 2),)
        self.assertEqual(apply_atom(Atom('scale', (2,)), grid), ((1, 1, 2, 2),) * 2)
        self.assertEqual(apply_atom(Atom('tile', (2,)), grid), ((1, 2, 1, 2),) * 2)
        self.assertEqual(apply_atom(Atom('repeat_rows', (3,)), grid), grid * 3)
        self.assertEqual(apply_atom(Atom('repeat_cols', (3,)), grid), ((1, 1, 1, 2, 2, 2),))
        self.assertEqual(apply_atom(Atom('compress', ('both',)), ((1, 1, 2), (1, 1, 2), (3, 3, 4))),
                         ((1, 2), (3, 4)))
        self.assertIsNone(apply_atom(Atom('scale', (2,)), ((1,) * 16,)))
        self.assertIsNone(apply_program(program(('scale', (3,)), ('compress', ('both',))), ((1,) * 11,)))

    def test_enumerator_exact_finite_size_and_no_literal_duplicates(self):
        atoms = (Atom('identity'), Atom('rot90'), Atom('flip_rows'))
        pool = tuple(programs(atoms))
        self.assertEqual(len(pool), grammar_size(atoms))
        self.assertEqual(len(pool), len(set(pool)))
        self.assertEqual([p.cost for p in pool], [1, 1, 1, 2, 2, 2, 2])


class SolverTests(unittest.TestCase):
    def test_known_rotation_recovery_without_program_supplied(self):
        data = task([[1, 2, 3], [4, 5, 6]], [[4, 1], [5, 2], [6, 3]], [[1, 2], [3, 4], [5, 6]])
        result = solve_task(data, 8)
        expected = [[5, 3, 1], [6, 4, 2]]
        for policy in POLICIES:
            self.assertEqual(result['policies'][policy][0]['attempt_1'], expected)
        self.assertEqual(result['search']['candidate_checks'], 8)
        self.assertFalse(result['search']['search_complete'])
        self.assertEqual(result['test_ambiguity'][0]['status'], 'incomplete_agreement')

    def test_learned_color_mapping_is_demonstration_only(self):
        data = task([[1, 2]], [[4, 5]], [[2, 1, 9]])
        result = solve_task(data, 30)
        outputs = [g['output'] for g in result['test_ambiguity'][0]['groups']]
        self.assertIn([[5, 4, 9]], outputs)
        data['test'][0]['output'] = {'invalid': 'must never be inspected'}
        other = solve_task(data, 30)
        for r in (result, other):
            r['search'].pop('elapsed_seconds')
        self.assertEqual(result, other)

    def test_actual_default_search_finds_composition(self):
        data = task([[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0]], [[3, 1], [4, 2]],
                    [[0, 5, 6, 0], [0, 7, 8, 0], [0, 0, 0, 0]])
        result = solve_task(data, 4096)
        self.assertIn([[7, 5], [8, 6]], [g['output'] for g in result['test_ambiguity'][0]['groups']])
        self.assertTrue(any(c['cost'] == 2 for c in result['candidates']))

    def test_ambiguity_witness_and_diversity_ablation(self):
        data = task([[1]], [[1]], [[1, 2], [3, 4]])
        pool = [program('identity'), program('rot180', 'rot180'), program('transpose'),
                program('flip_rows', 'rot90'), program('rot270', 'flip_rows')]
        result = solve_task(data, candidate_programs=pool)
        self.assertEqual(result['search']['candidate_checks'], 5)
        self.assertTrue(result['search']['search_complete'])
        self.assertEqual(result['test_ambiguity'][0]['status'], 'ambiguous')
        self.assertEqual(result['policies']['first_programs'][0]['attempt_1'],
                         result['policies']['first_programs'][0]['attempt_2'])
        self.assertNotEqual(result['policies']['first_distinct'][0]['attempt_1'],
                            result['policies']['first_distinct'][0]['attempt_2'])
        self.assertEqual(result['policies']['group_vote'][0]['attempt_1'], [[1, 3], [2, 4]])
        witness = result['test_ambiguity'][0]['witness']
        self.assertNotEqual(witness['left_output'], witness['right_output'])
        self.assertEqual(witness['difference']['kind'], 'cell')
        self.assertEqual(sum(g['program_votes'] for g in result['test_ambiguity'][0]['groups']), 5)

    def test_prefix_agreement_never_becomes_unique(self):
        data = task([[1]], [[1]], [[1, 2]])
        pool = [program('identity'), program('flip_cols')]
        prefix = solve_task(data, 1, candidate_programs=pool)
        complete = solve_task(data, 2, candidate_programs=pool)
        self.assertEqual(prefix['test_ambiguity'][0]['status'], 'incomplete_agreement')
        self.assertEqual(complete['test_ambiguity'][0]['status'], 'ambiguous')
        self.assertEqual(prefix['search']['stop_reason'], 'candidate_budget')

    def test_exhaustive_uniqueness_and_contradiction_are_scoped(self):
        pool = [program('identity'), program('flip_cols')]
        exact = solve_task(task([[1, 2]], [[2, 1]], [[3, 4]]), 2, candidate_programs=pool)
        self.assertEqual(exact['test_ambiguity'][0]['status'], 'unique_within_declared_grammar')
        impossible = solve_task(task([[1, 2]], [[3]], [[3, 4]]), 2, candidate_programs=pool)
        self.assertEqual(impossible['test_ambiguity'][0]['status'], 'no_solution_within_declared_grammar')
        self.assertIsNone(impossible['policies']['group_vote'][0]['attempt_1'])
        unknown = solve_task(task([[1, 2]], [[3]], [[3, 4]]), 0, candidate_programs=pool)
        self.assertEqual(unknown['test_ambiguity'][0]['status'], 'unknown')

    def test_undefined_consistent_hypothesis_prevents_unique_claim(self):
        data = task([[1]], [[1]], [[0]])
        result = solve_task(data, candidate_programs=[program('identity'), program(('crop_color', (1,)))])
        self.assertEqual(result['test_ambiguity'][0]['status'], 'agreement_with_undefined_hypotheses')
        self.assertEqual(result['test_ambiguity'][0]['undefined_consistent_programs'], 1)
        only = solve_task(data, candidate_programs=[program(('crop_color', (1,)))])
        self.assertEqual(only['test_ambiguity'][0]['status'], 'undefined_test')

    def test_duplicate_programs_do_not_manufacture_votes(self):
        p = program('identity')
        r = solve_task(task([[1]], [[1]], [[2]]), candidate_programs=[p, p, p])
        self.assertEqual(r['search']['grammar_size'], 1)
        self.assertEqual(r['search']['train_consistent'], 1)
        self.assertEqual(r['test_ambiguity'][0]['groups'][0]['program_votes'], 1)

    def test_two_test_inputs_have_independent_output_groups(self):
        data = task([[1]], [[1]], [[2]])
        data['test'].append({'input': [[2, 3]]})
        r = solve_task(data, candidate_programs=[program('identity'), program('transpose')])
        self.assertEqual(r['test_ambiguity'][0]['status'], 'unique_within_declared_grammar')
        self.assertEqual(r['test_ambiguity'][1]['status'], 'ambiguous')
        self.assertEqual(r['test_ambiguity'][1]['witness']['difference']['kind'], 'shape')

    def test_exhaustive_binary_grid_oracle(self):
        pool = [program('identity'), program('flip_cols'), program('flip_rows'), program('transpose')]
        grids = [((a, b), (c, d)) for a, b, c, d in itertools.product((0, 1), repeat=4)]
        # An independent literal oracle, not the implementation's transform helper.
        funcs = [lambda g: g, lambda g: (g[0][::-1], g[1][::-1]),
                 lambda g: (g[1], g[0]), lambda g: ((g[0][0], g[1][0]), (g[0][1], g[1][1]))]
        for src in grids:
            target = funcs[1](src)
            data = task([list(r) for r in src], [list(r) for r in target], [[0, 1], [1, 1]])
            result = solve_task(data, candidate_programs=pool)
            accepted = [i for i, fn in enumerate(funcs) if fn(src) == target]
            expected = {funcs[i](((0, 1), (1, 1))) for i in accepted}
            actual = {as_grid(g['output']) for g in result['test_ambiguity'][0]['groups']}
            self.assertEqual(actual, expected)
            self.assertEqual(result['search']['train_consistent'], len(accepted))

    def test_no_input_mutation_and_json_safe_receipt(self):
        data = task([[1, 2]], [[2, 1]], [[3, 4]])
        original = copy.deepcopy(data)
        result = solve_task(data, 20)
        self.assertEqual(data, original)
        json.dumps(result, allow_nan=False)

    def test_bad_task_and_budget_rejected(self):
        valid = task([[1]], [[1]], [[2]])
        for bad in (-1, True, 1.5, 100001):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                solve_task(valid, bad)
        for bad in ({}, {'train': [], 'test': []}, {'train': [{'input': [[1]]}], 'test': [{'input': [[2]]}]}):
            with self.assertRaises(ValueError):
                solve_task(bad)


if __name__ == '__main__':
    unittest.main()
