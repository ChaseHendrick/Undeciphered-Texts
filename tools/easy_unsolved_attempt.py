"""Bounded Dorabella experiment on a frozen primary research transcription.

This script does not edit engine sources, fit neural weights, or submit an
answer. Reference plaintext is used only to evaluate constructed controls.
The two stochastic attacks use the existing repository implementations.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from contextlib import ExitStack
import datetime
import hashlib
import json
import math
from pathlib import Path
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch
import urllib.request

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from engine.alphabet import letters_only, to_ints
from engine.language import get_model
from engine import fixtures
from engine.solvers import substitution as sub
from engine.solvers import homophonic_fixed_temperature as homo

RAW = 'abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod'
CT = RAW.upper()
SHORT_REFERENCE = 'THECOURIERPLACEDTHEPARCELBESIDETHEGATEANDWAITEDUNDERTHEPORCHUNTILTHEHEAVYRAINHADSTOPPED'
SEEDS = (1729, 2718, 3141)
MAX_WORK_CALLS = 1000000
MAX_SEARCH_SECONDS = 120
WORK = Counter()


class SearchLimit(RuntimeError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def count(kind):
    if sum(WORK.values()) >= MAX_WORK_CALLS:
        raise SearchLimit('objective_operation_limit')
    WORK[kind] += 1


def wrap(fn, kind):
    def measured(*args, **kwargs):
        count(kind)
        return fn(*args, **kwargs)
    return measured


def independent_sub_encrypt(plain, key):
    assert len(key) == 26 and len(set(key)) == 26
    return ''.join(key[ord(ch) - 65] for ch in plain)


def independent_homo_encrypt(plain, table, selectors=None):
    cursors = defaultdict(int)
    out = []
    for i, letter in enumerate(plain):
        options = table[letter]
        choice = cursors[letter] % len(options) if selectors is None else selectors[i]
        if not 0 <= choice < len(options):
            raise ValueError('invalid homophone selector')
        out.append(options[choice])
        cursors[letter] += 1
    return out


def accuracy(actual, expected):
    return {'expected_length': len(expected), 'actual_length': len(actual),
            'matching_positions': sum(a == e for a, e in zip(actual, expected)),
            'exact_reference_match': actual == expected,
            'expected_sha256': sha(expected.encode('ascii')), 'recovered_sha256': sha(actual.encode('ascii'))}


def bijective_record(cipher, result):
    plain = letters_only(result.plaintext)
    replay = independent_sub_encrypt(plain, result.key)
    assert replay == cipher
    return {'technique': 'bijective_cooled_annealing', 'candidate_plaintext': plain,
            'encrypt_key_AZ_to_cipher_labels': result.key, 'score': result.score,
            'score_kind': 'repository English quadgram log fitness, not correctness probability',
            'normalized_forward_sha256': sha(replay.encode('ascii')),
            'exact_forward_match': True, 'historical_verification': 'unavailable',
            'claimed_plaintext': None,
            'settings': {k: result.details[k] for k in ('seed', 'restarts', 'anneal_steps')},
            'neural_second_opinion': 'disabled after search; not needed by optimization; no neural fitting'}


def homophonic_record(tokens, result, glyph_inventory=None):
    mapping = dict(piece.split('=') for piece in result.key.split())
    plain = result.plaintext
    assert ''.join(mapping[t] for t in tokens) == plain
    table = defaultdict(list)
    for token, letter in sorted(mapping.items()):
        table[letter].append(token)
    # A homophonic decoder does not determine which of several homophones
    # an encoder chooses. Observed selectors provide a conditional witness,
    # and are never presented as independently sourced historical choices.
    selectors = [table[letter].index(token) for letter, token in zip(plain, tokens)]
    replay = independent_homo_encrypt(plain, table, selectors)
    assert replay == tokens
    canonical = independent_homo_encrypt(plain, table)
    record = {'technique': 'relaxed_homophonic_fixed_temperature', 'candidate_plaintext': plain,
              'cipher_token_to_plain_letter': mapping, 'score': result.score,
              'score_kind': 'same English quadgram fitness; larger model has more freedom',
              'decoder_consistent_at_all_positions': True,
              'exact_forward_match_given_observed_selectors': True,
              'encoder_homophone_selectors': selectors,
              'selector_provenance': 'Ciphertext-derived choices, not a source-backed historical encoder rule',
              'round_robin_encoder_matches_without_selectors': canonical == tokens,
              'historical_verification': 'unavailable', 'claimed_plaintext': None,
              'settings': {k: result.details[k] for k in ('seed', 'steps', 'temperature')},
              'merged_cipher_symbols': len(mapping) - len(set(mapping.values()))}
    if glyph_inventory is not None:
        glyphs = ''.join(glyph_inventory[int(token)] for token in replay)
        assert glyphs == CT
        record['lossless_glyph_replay_sha256'] = sha(glyphs.encode('ascii'))
    return record


def timed_run(name, fn, destination):
    before = WORK.copy()
    start = time.perf_counter()
    record = fn()
    record['run_name'] = name
    record['elapsed_seconds'] = time.perf_counter() - start
    record['actual_objective_operations'] = dict(WORK - before)
    record['stop_reason'] = 'configured_heuristic_work_completed'
    record['exhaustive_key_search'] = False
    destination.append(record)
    print(json.dumps({'run': name, 'elapsed_seconds': record['elapsed_seconds'],
                      'operations': record['actual_objective_operations'],
                      'exact_control_match': record.get('reference_comparison', {}).get('exact_reference_match')}), flush=True)


def source_snapshot(url):
    with urllib.request.urlopen(url, timeout=18) as response:
        raw = response.read(2000000)
        return {'url': url, 'sha256': sha(raw), 'bytes': len(raw),
                'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'http_last_modified': response.headers.get('Last-Modified')}, raw


def run():
    assert len(CT) == 87 and len(set(CT)) == 20 and len(SHORT_REFERENCE) == 87
    source_records = []
    metadata_snapshot, metadata_raw = source_snapshot('https://zenodo.org/api/records/4819086')
    metadata = json.loads(metadata_raw)
    metadata_snapshot.update({'role': 'Author-deposited HistoCrypt code/data archive metadata',
                              'title': metadata['metadata']['title'], 'doi': metadata['doi'],
                              'published': metadata['metadata']['publication_date'],
                              'data_license': metadata['metadata']['license']['id'],
                              'archive_publisher_md5': metadata['files'][0]['checksum'],
                              'archive_md5_computed_here': False})
    source_records.append(metadata_snapshot)
    page_snapshot, page_raw = source_snapshot('https://decipher.nu/challenges/elgars-dorabella-cipher/workbench')
    page_text = page_raw.decode('utf-8')
    assert 'No systematic decipherment has been accepted.' in page_text
    source_records.append({**page_snapshot, 'role': 'Live community challenge status and display transcription',
                           'status_scope': 'Listed as having no accepted systematic decipherment, not proof about every private proposal'})
    paths = [REPO/'engine/solvers/substitution.py', REPO/'engine/solvers/homophonic_fixed_temperature.py',
             REPO/'engine/language.py', REPO/'engine/data/english.txt', Path(__file__)]
    code_before = {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in paths}
    report = {'schema_version': 1, 'date': '2026-10-03', 'target': 'Elgar Dorabella cipher',
              'status': 'not_solved', 'new_verified_plaintext': False, 'claimed_plaintext': None,
              'source_status_scope': 'Live primary community challenge remains open; Hauer author research/data remains no accepted systematic reading. No global authority over unpublished proposals claimed.',
              'source_records': source_records,
              'primary_archive': {'url': 'https://doi.org/10.5281/zenodo.4819086',
                  'member': 'dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt',
                  'member_bytes': 87, 'member_raw_utf8': RAW, 'member_sha256': sha(RAW.encode('ascii')),
                  'extraction': 'Previously read directly by streamed tarfile from normal-TLS archive response; same87 characters shown by live challenge.',
                  'archive_limit': 'Streaming archive inspection stopped after31.857 seconds; entire archive checksum was not recomputed. No third-party code, model or corpus vendored.'},
              'paper_url': 'https://softwareprocess.es/pubs/hauer2021HistoCrypt-dorabella.pdf',
              'transcription': CT, 'normalized_sha256': sha(CT.encode('ascii')), 'symbols': 20, 'length': 87,
              'normalization': 'Lowercase neutral glyph labels uppercased bijectively; no punctuation, word boundaries, gaps or letters inserted. Original author file already flattened.',
              'older_transcription_audit': {'source_url': 'https://raw.githubusercontent.com/doranchak/zodiac-killer-ciphers/master/src/main/java/com/zodiackillerciphers/ciphers/Ciphers.java',
                  'canonical_repeated_symbol_disagreement_offsets': [33,77], 'used_for_search': False,
                  'scope': 'Lossless canonical equality-pattern comparison, not an original-autograph adjudication.'},
              'assumptions': ['One glyph decodes to one English letter in the selected models.',
                  'Bijective model requires different glyphs to decode differently; homophonic model relaxes that restriction.',
                  'No target cribs, artist-name dictionary, phonetic spelling rules, music mapping or target-adaptive tuning.',
                  'Glyph-label ordering has no claimed phonetic meaning.',
                  'All target candidates use the same fixed existing quadgram corpus; score is not independent evidence.'],
              'bounds': {'search_wall_limit_seconds': MAX_SEARCH_SECONDS, 'objective_operation_limit': MAX_WORK_CALLS,
                  'target_seeds': list(SEEDS), 'target_bijective_restarts': 5,'target_bijective_steps_per_restart': 3000,
                  'target_bijective_shake_runs': 4,'target_bijective_shake_steps': 1500,
                  'bijective_polish_pass_limit_per_call': 16,'bijective_polish_call_count': 5,
                  'target_homophonic_steps': 10000,'homophonic_polish_pass_limit': 30,
                  'homophonic_temperature': 2.0,'witness_limit': 20,
                  'operation_definition': 'Count full quadgram score calls and incremental homophone assignment score updates separately; skipped/no-change proposals and repeated states are not distinct keys.'},
              'sources_and_code_before': code_before,
              'python': sys.version,'git_head_at_start': subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
              'controls': [],'target_runs': [],'target_heldout_verification': {'available':False,
                  'reason':'No independently sourced historical plaintext or key acquired; no guessed plaintext treated as reference.'}}
    start = time.perf_counter()
    def timeout(signum, frame):
        raise SearchLimit('search_wall_limit')
    original_handler = signal.signal(signal.SIGALRM, timeout)
    signal.alarm(MAX_SEARCH_SECONDS)
    error = None
    with ExitStack() as stack:
        stack.enter_context(patch.object(sub, '_score', wrap(sub._score, 'bijective_full_quadgram_scores')))
        stack.enter_context(patch.object(homo, '_score', wrap(homo._score, 'homophonic_full_quadgram_scores')))
        stack.enter_context(patch.object(homo, '_assign', wrap(homo._assign, 'homophonic_incremental_score_updates')))
        # Neural scoring is strictly post-search in this existing solver.
        # Disable it so this experiment does not train a neural model merely
        # to add an unused second-opinion number to the heuristic result.
        stack.enter_context(patch.object(sub, 'get_neural_model', lambda: SimpleNamespace(score=lambda seq: None, backend='disabled')))
        try:
            def sub_control(plain, key, settings):
                cipher = independent_sub_encrypt(plain, key)
                result = sub.solve_substitution(cipher, **settings)
                record = bijective_record(cipher, result)
                inverse = {c: chr(65+i) for i,c in enumerate(key)}
                assert ''.join(inverse[c] for c in cipher) == plain
                record.update({'fixture_kind':'Constructed known plaintext and fixed substitution; no supplied key in search',
                               'reference_ciphertext':cipher,'independent_known_key_replay':True,
                               'reference_comparison':accuracy(record['candidate_plaintext'],plain)})
                return record
            timed_run('long-bijective-health-control',lambda:sub_control(letters_only(fixtures.SUBSTITUTION_PLAIN),
                       fixtures.SUBSTITUTION_KEY,{'restarts':10,'steps':4000,'seed':20261002}),report['controls'])
            timed_run('matched87-bijective-control',lambda:sub_control(SHORT_REFERENCE,
                       'PHQGIUMEAYLNOFDXJKRCVSTZWB',{'restarts':5,'steps':3000,'seed':SEEDS[0]}),report['controls'])
            def homo_control(plain, settings):
                table = homo.homophone_table(plain)
                tokens = independent_homo_encrypt(plain,table)
                inverse = {token:letter for letter,choices in table.items() for token in choices}
                assert ''.join(inverse[t] for t in tokens) == plain
                result = homo.solve_homophonic_fixed_temperature(' '.join(tokens), **settings)
                record = homophonic_record(tokens,result)
                record.update({'fixture_kind':'Constructed known plaintext with two E homophones, other letters single; no map supplied in search',
                               'reference_tokens':tokens,'independent_known_key_replay':True,
                               'reference_comparison':accuracy(record['candidate_plaintext'],plain)})
                return record
            timed_run('long-homophonic-health-control',lambda:homo_control(homo.fixture_plaintext(),
                       {'seed':3,'steps':20000,'temperature':2.0}),report['controls'])
            timed_run('matched87-homophonic-control',lambda:homo_control(SHORT_REFERENCE,
                       {'seed':SEEDS[0],'steps':10000,'temperature':2.0}),report['controls'])
            def frequency_baseline():
                seq=to_ints(CT); key=sub.frequency_decrypt_key(seq)
                plain=''.join(chr(65+key[i]) for i in seq)
                encrypt=['?']*26
                for cipher_i,plain_i in enumerate(key):encrypt[plain_i]=chr(65+cipher_i)
                record=bijective_record(CT,SimpleNamespace(plaintext=plain,key=''.join(encrypt),
                      score=sub._score(seq,key,get_model().logp),details={'seed':None,'restarts':0,'anneal_steps':0}))
                record['technique']='deterministic_frequency_rank_baseline'
                record['search_objective']='English unigram rank; quadgram score computed only afterward'
                return record
            timed_run('target-frequency-baseline',frequency_baseline,report['target_runs'])
            inventory=sorted(set(CT));token_map={ch:f'{i:02d}' for i,ch in enumerate(inventory)}
            tokens=[token_map[ch] for ch in CT]
            report['lossless_homophone_inventory']=inventory
            for seed in SEEDS:
                timed_run(f'target-bijective-seed-{seed}',lambda seed=seed:bijective_record(CT,
                           sub.solve_substitution(CT,restarts=5,steps=3000,seed=seed)),report['target_runs'])
                timed_run(f'target-homophonic-seed-{seed}',lambda seed=seed:homophonic_record(tokens,
                           homo.solve_homophonic_fixed_temperature(' '.join(tokens),seed=seed,steps=10000,temperature=2.0),inventory),report['target_runs'])
        except SearchLimit as exc:
            error=str(exc)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM,original_handler)
    report['elapsed_search_seconds']=time.perf_counter()-start
    report['actual_objective_operations']=dict(WORK)
    report['total_objective_operations']=sum(WORK.values())
    report['stop_reason']=error or 'all_declared_heuristic_runs_completed'
    report['exhaustive_key_search']=False
    report['no_neural_model_training']=True
    report['sources_unchanged_during_search']=code_before=={str(p.relative_to(REPO)):sha(p.read_bytes()) for p in paths}
    assert report['sources_unchanged_during_search']
    report['target_model_spaces']={'bijective_observed_maps':math.factorial(26)//math.factorial(6),
                                   'homophonic_observed_maps':26**20,
                                   'note':'Unconstrained20-glyph mapping spaces; heuristic operation counts are not unique-map coverage.'}
    summary={}
    for method in sorted({r['technique'] for r in report['target_runs']}):
        runs=[r for r in report['target_runs'] if r['technique']==method]
        best=max(runs,key=lambda r:r['score'])
        distances=[sum(a!=b for a,b in zip(left['candidate_plaintext'],right['candidate_plaintext']))
                   for i,left in enumerate(runs) for right in runs[i+1:]]
        summary[method]={'runs':len(runs),'distinct_plaintexts':len({r['candidate_plaintext'] for r in runs}),
                         'highest_score':best['score'],'highest_scoring_candidate':best['candidate_plaintext'],
                         'seed_pair_hamming_distances':distances,'historically_verified_candidates':0}
    report['target_summary']=summary
    report['completed_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    report['reproduction_command']='.venv/bin/python tools/easy_unsolved_attempt.py'
    report['verification_scope']='Bijective forward replay is exact but not independent truth. Relaxed homophonic replay requires explicitly ciphertext-derived selectors. No sourced historical heldout reference exists.'
    out=REPO/'docs/easy-unsolved-attempt-2026-10-03.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'elapsed_search_seconds':report['elapsed_search_seconds'],
                      'total_objective_operations':report['total_objective_operations'],
                      'stop_reason':report['stop_reason'],'target_summary':summary},indent=2),flush=True)


if __name__ == '__main__':
    run()
