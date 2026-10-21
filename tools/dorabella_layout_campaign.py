#!/usr/bin/env python3
"""Frozen, bounded Dorabella reading-order experiments, never a solve claim.

The labels and physical line boundaries come from two cited primary papers.
All layouts are index permutations. A bijective substitution search receives
only the ordered ciphertext, not control plaintexts or keys. Reference control
text is consulted after inference. No historical plaintext is available.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.language import get_model
from engine.solvers import substitution

HAUER_ROWS = (
    'ABCDEFGDHIJKLMKNKKFBBKMOIOPJQ',
    'GKGFODHRDCKKCFPLGKJKFSQLMOHHOJQ',
    'CQFSQCMSTPQCKFSLQPDBPQFDMOD',
)
SCHMEH_ROWS = (
    'ABCDEFGDHAIJKLJMJJFBBJNGOGNIP',
    'GJGFQDHRSCJJCFNKGJIJFTPKLQHHQIP',
    'CPFUPCLUUNPCJFUKPNDBNPFDLED',
)
ROW_LENGTHS = (29, 31, 27)
SEEDS = (202610031, 202610032, 202610033)
SEARCH = dict(restarts=5, steps=6000, temperature=30.0, cooling=0.997)
SOURCE_RECORDS = (
    dict(id='hauer2021', url='https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf',
         pdf_sha256='fe3fb6ff15f8c9d685b298c94b5a0d8417cf462b41a408ae0fbf3d8d2d18a97b',
         inspected_pages=[2], transcription_source='author Zenodo archive member',
         archive_url='https://doi.org/10.5281/zenodo.4819086',
         archive_member='dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt',
         raw_member_sha256='36d5211d9beb72c0fe99fad1fa1c268c7519d2cb82f294d53237cff4eded6730',
         row_count_evidence='Page 2 Figure 1 inspected directly; a second reader counted 29, 31, 27.'),
    dict(id='schmeh2018', url='https://ep.liu.se/ecp/149/026/ecp18149026.pdf',
         landing_url='https://ep.liu.se/en/conference-article.aspx?Article_No=26&issue=149&series=ecp',
         pdf_sha256='637005bdedc93c32cf6183bd031df44d205ce12a595e490124efe09b215a8533',
         inspected_pages=[2, 3], transcription_source='literal printed transcription on page 146',
         row_count_evidence='Page 146 printed lines separately counted 29, 31, 27; page 147 Figure 1 inspected.'),
)

# New prose controls, deliberately unrelated to an asserted Dorabella reading.
# First 87 normalized letters are a declared matched-length test design.
CONTROL_PROSE = (
    'THE CHILDREN WALKED ALONG THE RIVER UNTIL THEY FOUND THE OLD BRIDGE AND THEN RETURNED HOME BEFORE THE RAIN BEGAN.',
    'AFTER THE MEETING THE DOCTOR WROTE A LETTER TO THE FAMILY AND EXPLAINED WHY THE PATIENT WOULD NEED ANOTHER WEEK OF REST.',
    'THE FARMER OPENED THE WOODEN GATE AND WATCHED THE HORSES CROSS THE FIELD WHILE HIS BROTHER CARRIED WATER FROM THE WELL.',
    'WHEN THE TRAIN ARRIVED AT THE STATION THE TRAVELERS COLLECTED THEIR BAGS AND ASKED A PORTER TO SHOW THEM THE WAY OUT.',
)
CONTROL_KEY = 'MNBVCXZLKJHGFDSAPOIUYTREWQ'


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode('ascii')).hexdigest()


def layouts():
    """Top/bottom row direction times independent reversal of each physical row."""
    rows = (tuple(range(0, 29)), tuple(range(29, 60)), tuple(range(60, 87)))
    out = []
    for order in ((0, 1, 2), (2, 1, 0)):
        for mask in range(8):
            perm = tuple(i for row in order for i in (rows[row][::-1] if mask & (1 << row) else rows[row]))
            out.append(dict(id=f'{"top" if order[0] == 0 else "bottom"}-mask-{mask}',
                            row_order=list(order), reversed_physical_rows=[i for i in range(3) if mask & (1 << i)],
                            ordered_to_original=list(perm)))
    return out


def order(text, permutation):
    return ''.join(text[i] for i in permutation)


def restore(text, permutation):
    original = [''] * len(text)
    for stream_index, original_index in enumerate(permutation):
        original[original_index] = text[stream_index]
    return ''.join(original)


def oracle_encrypt(plain, key):
    # Independent literal character lookup, not the solver's key inversion.
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(key[alphabet.index(ch)] for ch in plain)


def layout_checks(frozen):
    source = ''.join(chr(65 + i % 26) for i in range(87))
    checks = []
    for layout in frozen:
        permutation = layout['ordered_to_original']
        assert sorted(permutation) == list(range(87))
        stream = order(source, permutation)
        assert restore(stream, permutation) == source
        # A second inverse implementation by the position of each original index.
        independent = ''.join(stream[permutation.index(i)] for i in range(87))
        assert independent == source
        checks.append(dict(layout=layout['id'], permutation_bijective=True, inverse_roundtrip=True,
                           independent_inverse_matches=True))
    return checks


class StopSearch(Exception):
    pass


def run(output, max_seconds, max_objective_calls):
    frozen = layouts()
    report = dict(schema_version=1, experiment_date='2026-10-03',
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  claimed_plaintext=None, correctness_known=False, historical_status='no_verified_reading',
                  objective='existing repository English conditional quadgram score, natural log sum',
                  no_cribs=True, no_target_reference_plaintext=True, neural_scoring_disabled=True,
                  source_records=list(SOURCE_RECORDS), layouts=frozen,
                  layout_controls=layout_checks(frozen), search_parameters=SEARCH,
                  bounds=dict(max_seconds=max_seconds, max_objective_calls=max_objective_calls,
                              planned_target_runs=96, seeds=list(SEEDS), control_runs=8),
                  controls=[], targets=[], interrupted_run=None)
    inputs = dict(hauer2021=''.join(HAUER_ROWS), schmeh2018=''.join(SCHMEH_ROWS))
    for rows in (HAUER_ROWS, SCHMEH_ROWS):
        assert tuple(map(len, rows)) == ROW_LENGTHS
    report['inputs'] = [dict(id=name, literal=raw, sha256=sha(raw), letters=len(raw),
                             distinct_labels=len(set(raw)), row_lengths=list(ROW_LENGTHS), row_offsets=[0, 29, 60])
                        for name, raw in inputs.items()]
    a, b = inputs.values()
    differences = [[i, j] for i in range(87) for j in range(i)
                   if (a[i] == a[j]) != (b[i] == b[j])]
    report['transcription_comparison'] = dict(method='pairwise label equality, independent of label names',
                                             disagreeing_pairs=differences, count=len(differences),
                                             adjudicated=False)
    report['geometry_scope'] = dict(physical_rows_verified=True, label_to_arc_orientation_verified=False,
                                    music_or_numeric_geometry_search_executed=False,
                                    reason='Neither checked paper supplies a verified neutral-label-to-geometry table.')
    report['runtime'] = dict(python=sys.version.split()[0])
    try:
        report['source_git_commit'] = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, timeout=5).strip()
        report['source_git_dirty'] = bool(subprocess.check_output(
            ['git', 'status', '--porcelain'], cwd=ROOT, text=True, timeout=5).strip())
    except (OSError, subprocess.SubprocessError):
        report['source_git_commit'] = None
        report['source_git_dirty'] = None
    report['source_hashes'] = {p: sha((ROOT / p).read_bytes()) for p in (
        'engine/solvers/substitution.py', 'engine/language.py', 'engine/data/english.txt',
        'tools/dorabella_layout_campaign.py')}
    model = get_model()
    report['language_model'] = dict(sample_letters=model.sample_letters,
                                   source='engine/data/english.txt', corpus_read_only=True,
                                   no_additional_dictionary=True)
    corpus = ''.join(c for c in (ROOT / 'engine/data/english.txt').read_text().upper() if 'A' <= c <= 'Z')
    control_plaintexts = [''.join(c for c in text if 'A' <= c <= 'Z')[:87] for text in CONTROL_PROSE]
    assert len(set(CONTROL_KEY)) == 26
    assert all(len(p) == 87 and p not in corpus for p in control_plaintexts)
    report['controls_design'] = dict(source='new literal constructed prose, not a historical claim',
                                    known_answer_not_in_search_arguments=True,
                                    no_exact_control_plaintext_in_model_corpus=True,
                                    distinct_reference_plaintexts=4,
                                    repeated_ordered_inference_inputs=True,
                                    interpretation='Two inverse layouts per reference give the same ordered cipher; they test layout replay, not independent recovery trials.',
                                    selection='first 87 ASCII letters of four declared sentences',
                                    original_prose=list(CONTROL_PROSE), encryption_key=CONTROL_KEY)
    calls = 0
    verification_score_calls = 0
    original_score = substitution._score
    started = time.perf_counter()
    current = None

    def counted_score(seq, key, logp):
        nonlocal calls
        if calls + verification_score_calls >= max_objective_calls:
            raise StopSearch('objective_call_limit')
        if time.perf_counter() - started >= max_seconds:
            raise StopSearch('time_limit')
        calls += 1
        return original_score(seq, key, logp)

    def alarm(_signum, _frame):
        raise StopSearch('time_limit')

    def verification_score(plain):
        nonlocal verification_score_calls
        if calls + verification_score_calls >= max_objective_calls:
            raise StopSearch('objective_call_limit')
        verification_score_calls += 1
        return model.score([ord(c) - 65 for c in plain])

    def infer(cipher, permutation, seed, label):
        nonlocal current
        stream = order(cipher, permutation)
        before = calls
        current = dict(label=label, seed=seed, ordered_ciphertext_sha256=sha(stream),
                       objective_calls_before=before)
        result = substitution.solve_substitution(stream, seed=seed, **SEARCH)
        plain = result.plaintext.upper()
        original_plain = restore(plain, permutation)
        encoded_stream = oracle_encrypt(plain, result.key)
        encoded_original = restore(encoded_stream, permutation)
        assert encoded_stream == stream and encoded_original == cipher
        score = verification_score(plain)
        assert abs(score - result.score) < 1e-8
        row = dict(seed=seed, ordered_ciphertext=stream, ordered_ciphertext_sha256=sha(stream),
                   reading_order_plaintext_candidate=plain, original_position_plaintext_candidate=original_plain,
                   plaintext_candidate_sha256=sha(plain), encryption_key=result.key,
                   decrypt_map=result.details['decrypt_map'], score=score,
                   objective_calls=calls - before, exact_stream_forward_replay=True,
                   exact_original_stream_forward_replay=True, original_ciphertext_replay=encoded_original,
                   original_ciphertext_replay_sha256=sha(encoded_original),
                   status='unverified_fitness_candidate', claimed_plaintext=None,
                   exhaustive_key_search=False)
        current = None
        return row

    old_handler = signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, max_seconds)
    stop_reason = 'configured_runs_completed'
    try:
        with patch.object(substitution, '_score', counted_score), patch.object(
            substitution, 'get_neural_model', lambda: SimpleNamespace(score=lambda seq: None, backend='disabled')
        ):
            for index, expected in enumerate(control_plaintexts):
                for layout in (frozen[0], frozen[13]):
                    permutation = layout['ordered_to_original']
                    cipher = restore(oracle_encrypt(expected, CONTROL_KEY), permutation)
                    row = infer(cipher, permutation, SEEDS[0] + index, f'control-{index}-{layout["id"]}')
                    recovered = row['reading_order_plaintext_candidate']
                    row.update(control=index, layout=layout['id'], ciphertext=cipher,
                               reference_plaintext=expected, reference_plaintext_sha256=sha(expected),
                               exact_reference_match=recovered == expected,
                               matching_reference_positions=sum(x == y for x, y in zip(recovered, expected)),
                               reference_score=verification_score(expected))
                    report['controls'].append(row)
                    print(json.dumps(dict(kind='control', control=index, layout=layout['id'],
                                          matching=row['matching_reference_positions'], calls=calls)), flush=True)
            # Breadth first: both inventories and every layout before another seed.
            for seed in SEEDS:
                for name, cipher in inputs.items():
                    for layout in frozen:
                        row = infer(cipher, layout['ordered_to_original'], seed, f'{name}-{layout["id"]}')
                        row.update(transcription=name, layout=layout['id'])
                        report['targets'].append(row)
                    print(json.dumps(dict(kind='target_checkpoint', seed=seed, transcription=name,
                                          target_runs=len(report['targets']), calls=calls)), flush=True)
    except StopSearch as exc:
        stop_reason = str(exc)
        report['interrupted_run'] = current
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
    report['actual'] = dict(objective_calls=calls, elapsed_seconds=time.perf_counter() - started,
                            verification_full_score_calls=verification_score_calls,
                            completed_control_runs=len(report['controls']),
                            completed_target_runs=len(report['targets']), stop_reason=stop_reason,
                            configured_search_complete=stop_reason == 'configured_runs_completed',
                            exhaustive_key_search=False, historical_correctness_known=False)
    report['summary'] = dict(exact_control_recoveries=sum(r['exact_reference_match'] for r in report['controls']),
                             control_runs=len(report['controls']),
                             distinct_control_plaintexts=len({r['reference_plaintext'] for r in report['controls']}),
                             exact_distinct_control_plaintexts=len({r['reference_plaintext'] for r in report['controls'] if r['exact_reference_match']}),
                             target_unique_candidate_plaintexts=len({r['reading_order_plaintext_candidate'] for r in report['targets']}),
                             all_retained_replays_exact=all(r['exact_original_stream_forward_replay'] for r in report['targets']),
                             target_reference_available=False, statistical_significance_estimated=False)
    report['ranked_candidates'] = sorted(report['targets'], key=lambda r: (-r['score'], r['transcription'], r['layout'], r['seed']))[:10]
    report['limitations'] = [
        'Heuristic configured completion is not exhaustive substitution key coverage.',
        'English fitness cannot verify a reading or choose a disputed glyph transcription.',
        'The fixed row layouts are hypotheses, not established reading directions.',
        'A bijection allows 20 or 21 observed glyph labels to map into 26 English letters; homophonic and polyalphabetic models are outside this campaign.',
        'No music, orientation arithmetic, null-calibrated significance, historical plaintext or source-backed heldout crib was supplied.',
        'Repeated trials on one 87-symbol target do not create independent evidence.',
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.name + '.tmp')
    temp.write_text(json.dumps(report, indent=2) + '\n')
    temp.replace(output)
    print(json.dumps(report['actual'], indent=2))
    return report


def extend_tempering(output):
    """Declared post-baseline extension over every non-identity ordered stream."""
    from engine.solvers.substitution_parallel_tempering import solve_substitution_parallel_tempering
    report = json.loads(output.read_text())
    if report.get('tempering_extension'):
        raise ValueError('a supplemental extension already exists')
    if not report['actual']['configured_search_complete']:
        raise ValueError('the baseline must finish before the supplemental extension')
    max_seconds = report['bounds']['max_seconds']
    max_evaluations = report['bounds']['max_objective_calls']
    baseline_calls = report['actual']['objective_calls']
    verification_calls = report['actual'].get('verification_full_score_calls', 0)
    baseline_seconds = report['actual']['elapsed_seconds']
    frozen = report['layouts']
    inputs = {r['id']: r['literal'] for r in report['inputs']}
    parameters = dict(seed=202610034, restarts=1, sweeps=5000, max_proposals=45000,
                      polish_passes=6, exchange_interval=25, max_candidates=3)
    extension = dict(protocol='Declared after the completed baseline, before supplemental target search',
                     selection='All ordered input streams except Hauer identity, with no fitness selection',
                     excluded=dict(transcription='hauer2021', layout='top-mask-0',
                                   reason='The independent main campaign owns original-stream tempering.'),
                     planned_runs=31, parameters=parameters, runs=[], source_hashes={p: sha((ROOT / p).read_bytes()) for p in (
                         'engine/solvers/substitution_parallel_tempering.py', 'tools/dorabella_layout_campaign.py')},
                     objective='same frozen repository English quadgram table', no_cribs=True,
                     target_reference_available=False, claimed_plaintext=None, exhaustive_key_search=False)
    started = time.perf_counter()
    stop_reason = 'configured_streams_completed'
    proposals = full_scores = exchanges = 0
    for name, cipher in inputs.items():
        for layout in frozen:
            if name == 'hauer2021' and layout['id'] == 'top-mask-0':
                continue
            remaining_seconds = max_seconds - baseline_seconds - (time.perf_counter() - started)
            remaining_evaluations = max_evaluations - baseline_calls - verification_calls - proposals - full_scores
            if remaining_seconds <= 0 or remaining_evaluations < 50:
                stop_reason = 'combined_time_limit' if remaining_seconds <= 0 else 'combined_evaluation_limit'
                break
            permutation = layout['ordered_to_original']
            stream = order(cipher, permutation)
            # Forty full-score calls safely exceed this one-restart API's fixed
            # initialization/retention overhead. Actual values remain separate.
            bounds = dict(parameters, max_proposals=min(45000, remaining_evaluations - 40),
                          timeout_seconds=min(remaining_seconds, 10.0))
            result = solve_substitution_parallel_tempering(stream, **bounds)
            details = result.details
            proposals += details['proposals']
            full_scores += details['full_score_calls']
            exchanges += details['exchange_attempts']
            witnesses = []
            for candidate in details['candidates']:
                plain = candidate['plaintext']
                replay = restore(oracle_encrypt(plain, candidate['key']), permutation)
                assert replay == cipher
                witnesses.append(dict(reading_order_plaintext_candidate=plain,
                                      original_position_plaintext_candidate=restore(plain, permutation),
                                      plaintext_candidate_sha256=sha(plain), encryption_key=candidate['key'],
                                      decrypt_map=candidate['decrypt_map'], score=candidate['score'],
                                      original_ciphertext_replay=replay, original_ciphertext_replay_sha256=sha(replay),
                                      exact_original_stream_forward_replay=True,
                                      claimed_plaintext=None, status='unverified_fitness_candidate'))
            row = dict(transcription=name, layout=layout['id'], ordered_ciphertext=stream,
                       ordered_ciphertext_sha256=sha(stream), bounds=bounds,
                       proposals=details['proposals'], full_score_calls=details['full_score_calls'],
                       exchange_attempts=details['exchange_attempts'], exchange_accepted=details['exchange_accepted'],
                       affected_quadgram_windows_evaluated=details['affected_quadgram_windows_evaluated'],
                       maximum_cached_score_drift=details['maximum_cached_score_drift'],
                       configured_search_complete=details['configured_search_complete'],
                       stop_reason=details['stop_reason'], elapsed_seconds=details['elapsed_seconds'],
                       candidates=witnesses)
            extension['runs'].append(row)
        else:
            print(json.dumps(dict(kind='extension_checkpoint', transcription=name,
                                  completed_runs=len(extension['runs']), proposals=proposals)), flush=True)
            continue
        break
    elapsed = time.perf_counter() - started
    extension['actual'] = dict(completed_runs=len(extension['runs']),
                               configured_streams_visited=len(extension['runs']) == 31,
                               fully_completed_inner_searches=sum(r['configured_search_complete'] for r in extension['runs']),
                               stop_reason=stop_reason, delta_proposals=proposals,
                               full_score_calls=full_scores, exchange_attempts=exchanges,
                               elapsed_seconds=elapsed, exhaustive_key_search=False)
    report['tempering_extension'] = extension
    report['combined_actual'] = dict(baseline_full_score_calls=baseline_calls,
                                     independent_verification_full_score_calls=verification_calls,
                                     supplemental_full_score_calls=full_scores,
                                     supplemental_delta_proposals=proposals,
                                     supplemental_exchange_attempts=exchanges,
                                     counted_evaluations=baseline_calls + verification_calls + proposals + full_scores,
                                     count_definition='Sum of full-score calls and delta proposals, not distinct keys; exchanges counted separately',
                                     total_search_seconds=baseline_seconds + elapsed,
                                     baseline_target_runs=len(report['targets']), supplemental_target_runs=len(extension['runs']),
                                     historical_correctness_known=False, exhaustive_key_search=False)
    report['bounds']['supplemental_counting'] = 'The same 6000000 ceiling now bounds full-score calls plus delta proposals; no distinct-key claim.'
    report['runner_hash_at_release'] = sha(Path(__file__).read_bytes())
    assert report['combined_actual']['counted_evaluations'] <= max_evaluations
    # Cooperative final assembly adds small overhead if the search times out;
    # preserve measured elapsed time even if serialization crosses the deadline.
    temp = output.with_name(output.name + '.tmp')
    temp.write_text(json.dumps(report, indent=2) + '\n')
    temp.replace(output)
    print(json.dumps(report['combined_actual'], indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/logs/dorabella-layouts-2026-10-03.json')
    parser.add_argument('--max-seconds', type=float, default=180)
    parser.add_argument('--max-objective-calls', type=int, default=6_000_000)
    parser.add_argument('--extend-tempering', action='store_true',
                        help='append the fixed post-baseline extension to an existing completed report')
    args = parser.parse_args()
    if not 0 < args.max_seconds <= 180 or not 1 <= args.max_objective_calls <= 6_000_000:
        parser.error('bounds must be positive and at most 180 seconds and 6000000 objective calls')
    if args.extend_tempering:
        if not args.output.exists():
            parser.error('the supplemental extension needs an existing baseline report')
        extend_tempering(args.output)
        return
    if args.output.exists():
        parser.error('output already exists; choose a new path to preserve the previous experiment')
    run(args.output, args.max_seconds, args.max_objective_calls)


if __name__ == '__main__':
    main()
