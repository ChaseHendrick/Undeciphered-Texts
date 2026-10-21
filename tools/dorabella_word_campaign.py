"""Frozen, bounded dictionary campaign; target has no expected answer or key."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work/dorabella-words'
sys.path.insert(0, str(ROOT))
from engine.solvers.unspaced_substitution import infer_unspaced_substitution

TARGET = 'abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod'
CONTROL_WORDS = 'THE COURIER SLOWLY CARRIED SEALED LETTERS THROUGH THE VILLAGE BEFORE SUNRISE AND RETURNED BY THE RIVER'.split()
DISTRACTORS = 'CIPHER CONSISTENT READERS SECRET QUIET SIGNAL SILENT AFTER BOATS FRIENDS CLEAR PAPER EVENING EARLY'.split()
TOKEN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def words(body):
    return sorted({re.sub("['’]", '', m.group()).upper() for m in TOKEN.finditer(body)
                   if len(re.sub("['’]", '', m.group())) <= 64})


def corpus(path, *, gutenberg=False, training_prefix=False):
    with path.open('rb') as handle:
        raw = handle.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError('corpus exceeds the 2 MB source-file bound')
    text = raw.decode('utf-8-sig')
    record = {'path': str(path), 'file_bytes': len(raw), 'file_sha256': sha(raw)}
    if gutenberg:
        start = re.search(r'^\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*\s*$', text, re.M)
        end = re.search(r'^\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*\s*$', text, re.M)
        if not start or not end or start.end() >= end.start():
            raise ValueError('corpus requires ordered Project Gutenberg START/END marker lines')
        text = text[start.end():end.start()]
        record['body_policy'] = 'UTF-8-sig decode; characters strictly between START/END marker lines'
    else:
        text = '\n'.join(line for line in text.splitlines() if not line.startswith('#'))
        record['body_policy'] = 'UTF-8-sig decode; omit comment lines starting #; join retained lines with LF'
    if training_prefix:
        matches = list(re.finditer(r'[A-Za-z]', text))
        cut = len(matches) * 3 // 5
        end_position = matches[cut].start() if cut < len(matches) else len(text)
        # Drop the crossing token, rather than inventing a truncated word type.
        last = [m.end() for m in TOKEN.finditer(text) if m.end() <= end_position]
        record['prefix_letter_cut'] = cut
        record['body_policy'] += '; first 60% of ASCII letter positions, truncated to last complete token'
        text = text[:last[-1]] if last else ''
    body = text.encode('utf-8')
    record.update(body_bytes=len(body), body_sha256=sha(body), word_types=len(words(text)))
    return words(text), record


def frozen_protocol(broader_austen, broader_eyre):
    small_austen, a = corpus(ROOT / 'engine/data/neural_train_austen.txt', training_prefix=True)
    original, b = corpus(ROOT / 'engine/data/english.txt')
    broad_a, c = corpus(broader_austen, gutenberg=True)
    broad_b, d = corpus(broader_eyre, gutenberg=True)
    dictionaries = {'training-prose': sorted(set(small_austen + original)),
                    'broader-prose': sorted(set(broad_a + broad_b))}
    for name, vocabulary in dictionaries.items():
        (WORK / (name + '.txt')).write_text('\n'.join(vocabulary), encoding='ascii')
    control = ''.join(CONTROL_WORDS)
    assert len(control) == 87
    # Independent affine permutation used only for the synthetic control encoder.
    control_cipher = ''.join(chr(65 + (5 * (ord(c) - 65) + 8) % 26) for c in control)
    protocol = {
        'declared_before_target_search': True,
        'target': TARGET, 'target_bytes': len(TARGET), 'raw_input_sha256': sha(TARGET.encode()),
        'normalized_input_sha256': sha(TARGET.upper().encode()),
        'module_sha256': sha((ROOT / 'engine/solvers/unspaced_substitution.py').read_bytes()),
        'lexicon_policy': "Unique ASCII word types, including proper names and foreign ASCII words; internal straight/curly apostrophes removed; hyphens split tokens; no target or control text added",
        'corpora': [a, b, c, d],
        'lexicons': {name: {'size': len(v), 'sha256': sha('\n'.join(v).encode())} for name, v in dictionaries.items()},
        'run_bounds': {'max_nodes': 250000, 'max_states': 4096, 'max_candidates': 20,
                       'max_lexicon_entries': 20000, 'timeout_seconds': 30.},
        'length_models': [{'name': 'ordinary-finite', 'min_word_length': 1, 'max_word_length': 32},
                          {'name': 'strict-finite', 'min_word_length': 2, 'max_word_length': 16}],
        'target_run_count': 4, 'target_total_node_bound': 1000000, 'target_total_timeout_bound_seconds': 120,
        'control': {'plaintext': control, 'words': CONTROL_WORDS, 'ciphertext': control_cipher,
                    'lexicon': sorted(set(CONTROL_WORDS + DISTRACTORS)),
                    'control_only_key': 'E(p)=(5*p+8) mod26',
                    'key_supplied_to_inference': False, 'expected_plaintext_supplied_to_inference': False,
                    'plaintext_sha256': sha(control.encode())},
        'control_bounds': {'max_nodes': 100000, 'max_states': 4096, 'max_candidates': 100, 'timeout_seconds': 10.},
    }
    (WORK / 'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
    return protocol, dictionaries


def main():
    global WORK
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--austen', '--broader-austen', dest='broader_austen', type=Path,
                        required=True, help='Project Gutenberg eBook 1342 UTF-8 text')
    parser.add_argument('--bronte', '--broader-eyre', dest='broader_eyre', type=Path,
                        required=True, help='Project Gutenberg eBook 1260 UTF-8 text')
    parser.add_argument('--output', type=Path, required=True, help='New or empty output directory; existing content is refused')
    parser.add_argument('--ordinary-singletons', action='store_true', help='Separately declared A/I-only singleton supplemental model using any remainder of the one-million-node budget')
    args = parser.parse_args()
    WORK = args.output
    if WORK.is_symlink() or (WORK.exists() and (not WORK.is_dir() or any(WORK.iterdir()))):
        parser.error('--output must be a new or empty directory without a symlink at that path')
    WORK.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    protocol, dictionaries = frozen_protocol(args.broader_austen, args.broader_eyre)
    print('Protocol frozen', protocol['lexicons'], flush=True)
    control = protocol['control']
    control_report = infer_unspaced_substitution(control['ciphertext'], lexicon=control['lexicon'], **protocol['control_bounds'])
    recovered = [c for c in control_report['candidates'] if c['plaintext_letters'] == control['plaintext']]
    control_record = {'kind': '87-letter constructed control with separate vocabulary', 'report': control_report,
                      'known_answer_recovered': bool(recovered), 'exact_reference_boundaries_recovered': any(c['words'] == control['words'] for c in recovered)}
    print('Separate control', control_report['nodes'], control_report['stop_reason'], bool(recovered), flush=True)
    coverage = []
    for name, vocabulary in dictionaries.items():
        for lengths in protocol['length_models']:
            eligible = {word for word in vocabulary if lengths['min_word_length'] <= len(word) <= lengths['max_word_length']}
            missing = sorted(set(control['words']) - eligible)
            coverage.append({'lexicon': name, 'length_model': lengths['name'],
                             'control_reference_segmentation_in_model': not missing,
                             'reference_words_missing_or_excluded': missing,
                             'note': 'Coverage audit only; reference plaintext not added to target vocabulary'})
    runs = []
    for name, vocabulary in dictionaries.items():
        for lengths in protocol['length_models']:
            options = {key: value for key, value in lengths.items() if key != 'name'}
            report = infer_unspaced_substitution(TARGET, lexicon=vocabulary, **protocol['run_bounds'], **options)
            runs.append({'lexicon': name, 'length_model': lengths['name'], 'report': report})
            print('Target', name, lengths['name'], report['nodes'], report['stop_reason'], report['solutions_found'], round(report['elapsed_seconds'], 3), flush=True)
    missing_control = infer_unspaced_substitution('ZRCSWFRCPGCCFULCZZCPUSAVUWUZCVZ',
        lexicon=['THE', 'CIPHER', 'KEEPS', 'LETTERS'], max_nodes=100000, timeout_seconds=10.)
    results = {'protocol': protocol, 'matched_length_control': control_record,
               'corpus_dictionary_coverage_controls': coverage,
               'missing_vocabulary_control': {'plaintext': 'THECIPHERKEEPSLETTERSCONSISTENT',
                   'missing_word': 'CONSISTENT', 'report': missing_control,
                   'note': 'Valid constructed English is not recoverable from this declared incomplete lexicon; no English exclusion follows'},
               'target_runs': runs, 'total_target_nodes': sum(run['report']['nodes'] for run in runs),
               'target_elapsed_seconds_sum': sum(run['report']['elapsed_seconds'] for run in runs),
               'campaign_elapsed_seconds': time.monotonic() - started,
               'claimed_plaintext': None, 'historical_solution_verified': False}
    if args.ordinary_singletons:
        vocabulary = [word for word in dictionaries['broader-prose'] if len(word) > 1 or word in ('A', 'I')]
        remaining = protocol['target_total_node_bound'] - results['total_target_nodes']
        declaration = {'declared_before_supplemental_search': True,
                       'reason': 'Separate optional A/I singleton model; original four runs retained',
                       'lexicon_policy': 'Preserve all longer broader-prose entries; singleton words only A and I',
                       'dictionary_size': len(vocabulary), 'lexicon_sha256': sha('\n'.join(vocabulary).encode()),
                       'max_nodes': remaining, 'timeout_seconds': 30., 'min_word_length': 1, 'max_word_length': 32}
        results['supplemental_declaration'] = declaration
        (WORK / 'supplemental-protocol.json').write_text(json.dumps(declaration, indent=2) + '\n')
        if remaining:
            options = dict(protocol['run_bounds'], max_nodes=remaining)
            report = infer_unspaced_substitution(TARGET, lexicon=vocabulary, **options)
            results['target_runs'].append({'lexicon': 'broader-prose-ordinary-singletons', 'length_model': 'ordinary-finite', 'report': report})
            results['total_target_nodes'] += report['nodes']
            results['target_elapsed_seconds_sum'] += report['elapsed_seconds']
            print('Supplement', report['nodes'], report['stop_reason'], report['solutions_found'], flush=True)
        else:
            results['supplemental_not_run'] = 'One-million-node total target budget already exhausted'
        results['campaign_elapsed_seconds_including_supplemental_search'] = time.monotonic() - started
    (WORK / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Results saved', WORK / 'results.json', flush=True)


if __name__ == '__main__':
    main()
