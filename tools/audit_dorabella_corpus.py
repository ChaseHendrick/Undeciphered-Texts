"""Replay the larger-corpus campaign independently and score its true controls."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.language import LanguageModel
from tools.dorabella_corpus_campaign import CONTROL_PROSE, KEYS, load_book


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encrypt(plain, key):
    if len(key) != 26 or set(key) != set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        raise ValueError('invalid encryption permutation')
    return ''.join(key[ord(letter) - 65] for letter in plain)


def full_score(plain, table):
    seq = [ord(letter) - 65 for letter in plain]
    return sum(table[sum(seq[i + j] * (26 ** (3 - j)) for j in range(4))]
               for i in range(len(seq) - 3))


def run(args):
    report_raw = args.report.read_bytes()
    report = json.loads(report_raw)
    bodies = []
    for index, (path, ebook, title) in enumerate(((args.austen, 1342, 'Pride and Prejudice'),
                                               (args.bronte, 1260, 'Jane Eyre'))):
        body, metadata = load_book(path, ebook, title)
        if metadata != report['training_sources'][index]:
            raise AssertionError('training corpus snapshot changed')
        bodies.append(body)
    model = LanguageModel('\n'.join(bodies), alpha=report['model']['alpha'])
    table_digest = digest(struct.pack('<' + 'd' * len(model.logp), *model.logp))
    if table_digest != report['model']['logp_little_endian_float64_sha256']:
        raise AssertionError('reconstructed model disagrees')
    audit = {'schema_version': 1, 'campaign_report_sha256': digest(report_raw),
        'reconstructed_score_table_sha256': table_digest, 'score_table_exact_match': True,
        'all_forward_replays_match': True, 'all_scores_match': True,
        'control_objective_audit': [], 'runs_replayed': 0, 'retained_candidates_replayed': 0,
        'historical_correctness_verified': False, 'claimed_plaintext': None}
    for group in ('controls', 'null_runs', 'target_runs'):
        for index, record in enumerate(report[group]):
            input_stream = record['input']
            for candidate in ({'plaintext': record['candidate_plaintext'],
                               'key': record['encrypt_key_AZ_to_cipher_labels'], 'score': record['score']},
                              *record['details']['candidates']):
                if encrypt(candidate['plaintext'], candidate['key']) != input_stream:
                    raise AssertionError('independent candidate forward replay failed')
                score = full_score(candidate['plaintext'], model.logp)
                if not math.isclose(score, candidate['score'], rel_tol=1e-12, abs_tol=1e-8):
                    raise AssertionError('independent score replay failed')
                audit['retained_candidates_replayed'] += 1
            audit['runs_replayed'] += 1
            if group == 'controls':
                reference = ''.join(c.upper() for c in CONTROL_PROSE[index] if c.isascii() and c.isalpha())[:87]
                if encrypt(reference, KEYS[index]) != input_stream:
                    raise AssertionError('independent control construction failed')
                comparison = record['reference_comparison']
                if reference != comparison['reference_plaintext'] or digest(reference.encode('ascii')) != comparison['expected_sha256']:
                    raise AssertionError('control reference certificate changed')
                reference_score = full_score(reference, model.logp)
                audit['control_objective_audit'].append({'name': record['name'],
                    'reference_score': reference_score, 'recovered_score': record['score'],
                    'candidate_minus_reference': record['score'] - reference_score,
                    'exact_recovery': record['candidate_plaintext'] == reference,
                    'matching_positions': comparison['matching_positions'],
                    'wrong_candidate_outscores_reference': record['candidate_plaintext'] != reference and record['score'] > reference_score + 1e-8})
    args.output.write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--austen', type=Path, required=True)
    parser.add_argument('--bronte', type=Path, required=True)
    parser.add_argument('--report', type=Path, default=Path(__file__).resolve().parents[1] / 'docs/logs/dorabella-corpus-2026-10-03.json')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'docs/logs/dorabella-corpus-audit-2026-10-03.json')
    run(parser.parse_args())
