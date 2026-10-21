"""Frozen, bounded original-stream Dorabella replica-exchange campaign.

Controls are evaluated before the main target campaign. Reference plaintext
never enters the optimizer. JSON is checkpointed after every finished seed.
No model fitting, neural training, third-party code or answer submission.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from engine.alphabet import letters_only
from engine.fixtures import SUBSTITUTION_KEY, SUBSTITUTION_PLAIN
from engine.language import get_model
from engine.solvers.substitution_parallel_tempering import solve_substitution_parallel_tempering
from tools.easy_unsolved_attempt import RAW, CT, SHORT_REFERENCE

SHORT_PLAIN = 'THEMANENTEREDTHEROOMANDTHENTHEOTHERMENCAMETOMEETHIMTHEREINTHEMORNINGTHEYWEREALLREADYAND'
SHORT_CIPHER = 'CEIOPFIFCIKIGCEIKDDOPFGCEIFCEIDCEIKOIFQPOICDOIICEAOCEIKIAFCEIODKFAFMCEIWTIKIPNNKIPGWPFG'
SEEDS = (1729, 2718, 3141, 5772, 8111, 104729, 130363, 20261003, 20261004, 20261005)
GLOBAL_SECONDS = 180.0
GLOBAL_PROPOSALS = 11_000_000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(plain, key):
    if len(key) != 26 or set(key) != set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        raise ValueError('independent forward encoder needs a full bijective key')
    return ''.join(key[ord(c) - 65] for c in plain)


def witness(cipher, candidate):
    plain = letters_only(candidate['plaintext'])
    replay = encode(plain, candidate['key'])
    if replay != cipher:
        raise AssertionError('independent full-stream forward replay failed')
    return {**candidate, 'plaintext_sha256': sha(plain.encode('ascii')),
            'forward_ciphertext': replay, 'forward_ciphertext_sha256': sha(replay.encode('ascii')),
            'exact_forward_match': True, 'historical_verification': 'unavailable',
            'claimed_plaintext': None}


def record(cipher, result):
    candidates = [witness(cipher, candidate) for candidate in result.details['candidates']]
    return {'best': witness(cipher, {'plaintext': result.plaintext, 'key': result.key,
                                    'score': result.score, 'decrypt_map': result.details['decrypt_map']}),
            'candidates': candidates,
            'run': {k: v for k, v in result.details.items() if k != 'candidates'}}


def run(output):
    prior_path = REPO / 'docs/easy-unsolved-attempt-2026-10-03.json'
    prior = json.loads(prior_path.read_text())
    if sha(CT.encode('ascii')) != 'ed1b7d3391cbe06bc52d023643860a0795624836cb7efe155d0af59e269d5a50':
        raise AssertionError('frozen input changed')
    model = get_model()  # Existing frozen repository objective; no target fitting.
    paths = [Path(__file__), REPO / 'engine/solvers/substitution_parallel_tempering.py',
             REPO / 'engine/solvers/substitution.py', REPO / 'engine/language.py',
             REPO / 'engine/data/english.txt', REPO / 'tools/easy_unsolved_attempt.py']
    start_hashes = {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in paths}
    report = {'schema_version': 1, 'tool_name': 'substitution-parallel-tempering',
              'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'target': 'Dorabella', 'status': 'not_solved', 'claimed_plaintext': None,
              'raw_neutral_labels': RAW, 'raw_sha256': sha(RAW.encode('ascii')),
              'normalized_ciphertext': CT, 'normalized_sha256': sha(CT.encode('ascii')),
              'length': len(CT), 'distinct_symbols': len(set(CT)),
              'source_records': prior['source_records'],
              'primary_archive': prior['primary_archive'], 'paper_url': prior['paper_url'],
              'source_record_scope': 'Reuse the prior acquired source snapshots and exact author member; not a new live status audit.',
              'algorithm_source': 'https://arxiv.org/abs/cond-mat/0407273',
              'algorithm_scope': 'Independent stdlib implementation of exact sparse quadgram key-swap deltas and single-process logical replica exchange; not new historical cryptanalysis.',
              'assumptions': ['Original author flattened stream, no rearrangement or inserted words.',
                  'One glyph maps to one English letter; distinct glyphs map to distinct letters.',
                  'Existing frozen English corpus and its quadgram table; no target phrases or neural fitting.',
                  'Full 26-letter permutations include arbitrary mappings for six unobserved glyph labels.',
                  'English fitness and exact forward replay do not establish historical correctness.'],
              'bounds': {'main_campaign_wall_seconds': GLOBAL_SECONDS, 'main_campaign_max_proposals': GLOBAL_PROPOSALS,
                         'target_seeds': list(SEEDS), 'target_restarts_per_seed': 5,
                         'target_sweeps_per_restart': 25000, 'target_max_proposals_per_seed': 1020000,
                         'target_timeout_seconds_per_seed': 30, 'candidate_cap_per_seed': 10,
                         'polish_passes_per_restart': 8,
                         'work_unit': 'One actual swap proposal including greedy polish; not a distinct key. Affected windows, exchange attempts and full rescoring are counted separately.',
                         'global_wall_scope': 'Search calls and checkpointing after corpus initialization; cooperative solver checks can add batch and result-finalization overhead.'},
              'source_code_sha256_at_start': start_hashes,
              'git_head_at_start': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
              'python': sys.version, 'controls': [], 'target_runs': [],
              'pre_campaign_performance_pilot': {'seed': 20261003, 'restarts': 1, 'sweeps': 10000,
                  'polish_passes': 4, 'proposals': 80310, 'affected_quadgram_windows_evaluated': 1878931,
                  'exchange_attempts': 1400, 'exchange_accepted': 327, 'elapsed_seconds': 0.6398183749988675,
                  'best_plaintext': 'XPNISTRICFMEDGEWEETPPEGOFOLMARERTOICKINEENTLDREMETHADGOCCOMANATHANGHULANETHDALIPLATIGOI',
                  'best_score': -222.27920918428364,
                  'scope': 'Performance pilot on an earlier draft with the same default objective, before this frozen main campaign. Full source byte hash and full key were not retained, so it is not a forward-verified frozen witness.'},
              'control_selection_note': 'The initial 87-letter courier exact-recovery test failed. A separate original prose prefix was then measured and retained as a passing regression; it has fewer distinct letters and is not an accuracy benchmark. An 88-letter harbor trial recovered 84 positions; a 146-letter courier extension recovered 138; a 120-letter meeting narrative recovered exactly. Those exploratory fixture runs had the same 180000-proposal upper cap, no target-specific score fitting, and were not part of this checkpointed campaign. Exact exploratory counts were not retained.',
              'prior_original_stream_bijective_target_scores': [r['score'] for r in prior['target_runs'] if r['technique'] == 'bijective_cooled_annealing'],
              'heldout_verification': {'available': False, 'reason': 'No independently sourced Dorabella plaintext or key acquired. Guessed words cannot serve as heldout truth.'},
              'exhaustive_key_search': False}
    started = time.perf_counter()
    totals = Counter()

    def save():
        report['actual_main_campaign_counts'] = dict(totals)
        report['elapsed_main_campaign_seconds'] = time.perf_counter() - started
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')

    def execute(cipher, kwargs):
        remaining_time = GLOBAL_SECONDS - (time.perf_counter() - started)
        remaining_proposals = GLOBAL_PROPOSALS - totals['proposals']
        if remaining_time <= 0 or remaining_proposals <= 0:
            return None
        result = solve_substitution_parallel_tempering(cipher, **{**kwargs,
            'max_proposals': min(kwargs['max_proposals'], remaining_proposals),
            'timeout_seconds': min(kwargs.get('timeout_seconds', 30), remaining_time)})
        for name in ('proposals', 'affected_quadgram_windows_evaluated', 'accepted_swaps',
                     'exchange_attempts', 'exchange_accepted', 'full_score_calls'):
            totals[name] += result.details[name]
        return record(cipher, result)

    short_kwargs = {'seed': 1729, 'restarts': 4, 'sweeps': 5000, 'max_proposals': 180000, 'timeout_seconds': 20}
    controls = [('independent87-meeting-prefix', SHORT_PLAIN, 'PHQGIUMEAYLNOFDXJKRCVSTZWB', short_kwargs),
                ('matched87-courier-negative-control', SHORT_REFERENCE, 'PHQGIUMEAYLNOFDXJKRCVSTZWB', short_kwargs),
                ('long-original-repository-control', letters_only(SUBSTITUTION_PLAIN), SUBSTITUTION_KEY,
                 {'seed': 20261003, 'restarts': 2, 'sweeps': 3500, 'max_proposals': 65000, 'timeout_seconds': 20})]
    for name, expected, hidden_key, kwargs in controls:
        cipher = encode(expected, hidden_key)
        if name == 'independent87-meeting-prefix' and cipher != SHORT_CIPHER:
            raise AssertionError('literal short fixture mismatch')
        run_record = execute(cipher, kwargs)
        if run_record is None:
            raise RuntimeError('global budget exhausted before controls completed')
        actual = run_record['best']['plaintext']
        run_record.update({'name': name, 'fixture_kind': 'Constructed original plaintext, independent encoder and hidden key; optimizer sees ciphertext only',
            'expected_plaintext': expected, 'expected_sha256': sha(expected.encode('ascii')),
            'ciphertext': cipher, 'ciphertext_sha256': sha(cipher.encode('ascii')),
            'reference_key_used_only_for_control_generation': hidden_key,
            'exact_reference_match': actual == expected,
            'matching_positions': sum(a == b for a, b in zip(actual, expected)),
            'length': len(expected), 'distinct_plain_letters': len(set(expected)),
            'reference_fitness': model.score([ord(c) - 65 for c in expected])})
        report['controls'].append(run_record)
        save()
        print(json.dumps({'control': name, 'exact': actual == expected, 'matching_positions': run_record['matching_positions'],
                          'proposals': run_record['run']['proposals'], 'elapsed': run_record['run']['elapsed_seconds']}), flush=True)
    if not report['controls'][0]['exact_reference_match'] or not report['controls'][2]['exact_reference_match']:
        report['stop_reason'] = 'positive_control_failed'
        save()
        return report
    for seed in SEEDS:
        run_record = execute(CT, {'seed': seed, 'restarts': 5, 'sweeps': 25000,
                                'max_proposals': 1020000, 'timeout_seconds': 30, 'max_candidates': 10})
        if run_record is None:
            break
        report['target_runs'].append(run_record)
        save()
        print(json.dumps({'target_seed': seed, 'score': run_record['best']['score'],
            'proposals': run_record['run']['proposals'], 'elapsed': run_record['run']['elapsed_seconds'],
            'stop': run_record['run']['stop_reason']}), flush=True)
    unique = {}
    for run_record in report['target_runs']:
        for candidate in run_record['candidates']:
            plain = candidate['plaintext']
            if plain not in unique:
                unique[plain] = {**candidate, 'supporting_seeds': []}
            unique[plain]['supporting_seeds'].append(run_record['run']['seed'])
    report['distinct_stored_target_candidates'] = len(unique)
    report['ranked_target_candidates'] = sorted(unique.values(), key=lambda c: (-c['score'], c['plaintext']))
    best_plains = [r['best']['plaintext'] for r in report['target_runs']]
    report['pairwise_best_candidate_hamming_distances'] = [sum(a != b for a, b in zip(x, y))
                                                         for x, y in itertools.combinations(best_plains, 2)]
    report['target_runs_completed'] = len(report['target_runs'])
    report['target_proposals'] = sum(r['run']['proposals'] for r in report['target_runs'])
    report['target_affected_windows'] = sum(r['run']['affected_quadgram_windows_evaluated'] for r in report['target_runs'])
    report['stop_reason'] = 'all_declared_seed_runs_completed' if len(report['target_runs']) == len(SEEDS) and all(
        r['run']['configured_search_complete'] for r in report['target_runs']) else 'bounded_incomplete_campaign'
    report['sources_unchanged_during_main_campaign'] = start_hashes == {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in paths}
    if not report['sources_unchanged_during_main_campaign']:
        raise AssertionError('campaign source changed during execution')
    save()
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/logs/dorabella-tempering-2026-10-03.json')
    arguments = parser.parse_args()
    final = run(arguments.output)
    print(json.dumps({'output': str(arguments.output), 'stop_reason': final['stop_reason'],
                      'target_runs': final.get('target_runs_completed', 0), 'counts': final['actual_main_campaign_counts'],
                      'elapsed': final['elapsed_main_campaign_seconds']}), flush=True)
