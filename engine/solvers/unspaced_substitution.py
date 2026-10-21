"""Exact bounded dictionary constraints with unknown word boundaries.

An iterative trie search jointly assigns a global injective cipher-to-plain
map and word breaks. It does not require given spaces, a key or target cribs.
Alphabetical traversal is reproducible, not a probability or quality ranking.
Completion and uniqueness apply only to the supplied finite vocabulary and
declared word-length interval. No historical plaintext is claimed.

General backtracking reference, without copying its implementation:
https://github.com/aimacode/aima-python/blob/master/aima/csp.py
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
import hashlib
import math
import re
import time


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_RAW_CHARACTERS = 4096
MAX_LEXICON_CHARACTERS = 1_000_000
MAX_TRIE_NODES = 250_000


@dataclass(slots=True)
class _TrieNode:
    children: dict[int, int] = field(default_factory=dict)
    terminal: bool = False


@dataclass(frozen=True, slots=True)
class _State:
    position: int
    trie_node: int
    mapping: tuple[int, ...]
    used_letters: int
    boundaries: tuple[int, ...]


def _integer(value, name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ValueError(f'{name} must be an integer between 1 and {maximum}')
    return value


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode('ascii')).hexdigest()


def _lexicon(words: Iterable[str], maximum: int) -> tuple[list[str], int]:
    if isinstance(words, (str, bytes, Mapping)):
        raise TypeError('lexicon must be an iterable of single A-Z words')
    try:
        iterator = iter(words)
    except TypeError as exc:
        raise TypeError('lexicon must be an iterable of single A-Z words') from exc
    unique, characters, count = set(), 0, 0
    for count, word in enumerate(iterator, 1):
        if count > maximum:
            raise ValueError('lexicon entries exceed max_lexicon_entries')
        if not isinstance(word, str):
            raise TypeError('each lexicon entry must be a string')
        if not 1 <= len(word) <= 64 or re.fullmatch(r'[A-Za-z]+', word) is None:
            raise ValueError('lexicon entries must be single ASCII words of 1 through 64 letters')
        characters += len(word)
        if characters > MAX_LEXICON_CHARACTERS:
            raise ValueError('lexicon characters exceed the preparation bound')
        unique.add(word.upper())
    if not unique:
        raise ValueError('lexicon must contain at least one word')
    return sorted(unique), count


def _trie(words: list[str]) -> list[_TrieNode]:
    nodes = [_TrieNode()]
    for word in words:
        current = 0
        for letter in word:
            code = ord(letter) - 65
            child = nodes[current].children.get(code)
            if child is None:
                if len(nodes) >= MAX_TRIE_NODES:
                    raise ValueError('lexicon trie exceeds the preparation node bound')
                child = len(nodes)
                nodes[current].children[code] = child
                nodes.append(_TrieNode())
            current = child
        nodes[current].terminal = True
    return nodes


def _candidate(ciphertext: str, state: _State) -> dict:
    plaintext = ''.join(ALPHABET[state.mapping[ord(letter) - 65]] for letter in ciphertext)
    boundaries = state.boundaries + (len(ciphertext),)
    starts = (0,) + boundaries[:-1]
    words = [plaintext[start:end] for start, end in zip(starts, boundaries)]
    mapping = {letter: ALPHABET[state.mapping[ord(letter) - 65]] for letter in sorted(set(ciphertext))}
    inverse = {plain: cipher for cipher, plain in mapping.items()}
    replay = ''.join(inverse[letter] for letter in plaintext)
    assert len(mapping) == len(inverse) and replay == ciphertext
    return {'plaintext': ' '.join(words), 'plaintext_letters': plaintext, 'words': words,
            'word_boundaries': list(boundaries), 'cipher_to_plain': mapping,
            'decrypt_key': ''.join('?' if code < 0 else ALPHABET[code] for code in state.mapping),
            'key_complete': all(code >= 0 for code in state.mapping),
            'family': 'substitution', 'forward_consistent': True, 'dictionary_consistent': True,
            'plaintext_sha256': _digest(plaintext),
            'evidence': ['Global observed-symbol bijection', 'Complete supplied-lexicon segmentation',
                         'Exact ciphertext forward replay; historical correctness unknown']}


def infer_unspaced_substitution(
    text: str, *, lexicon: Iterable[str], max_nodes: int = 100000,
    max_states: int = 4096, max_candidates: int = 20,
    min_word_length: int = 1, max_word_length: int = 32,
    max_lexicon_entries: int = 20000, timeout_seconds: float = 30.,
) -> dict:
    """Enumerate dictionary-consistent plaintexts and unknown word boundaries.

    One popped state consumes one search node, including boundary transitions.
    max_states bounds the pending DFS frontier; overflow stops without silently
    dropping branches. One additional solution can establish candidate-limit
    ambiguity. An exact final permitted node can still prove completion.
    Input preparation has separate finite entry/character/trie bounds.
    """
    started = time.monotonic()
    if not isinstance(text, str):
        raise TypeError('text must be a string')
    if len(text) > MAX_RAW_CHARACTERS:
        raise ValueError('raw ciphertext exceeds the formatting-character bound')
    if any(letter not in ALPHABET + ALPHABET.lower() + ' \t\r\n\f\v' for letter in text):
        raise ValueError('ciphertext must contain ASCII A-Z letters and formatting whitespace only')
    ciphertext = ''.join(letter for letter in text.upper() if letter in ALPHABET)
    if not 4 <= len(ciphertext) <= 512:
        raise ValueError('ciphertext must contain 4 through 512 normalized letters')
    _integer(max_nodes, 'max_nodes', 1_000_000)
    _integer(max_states, 'max_states', 16384)
    _integer(max_candidates, 'max_candidates', 100)
    _integer(min_word_length, 'min_word_length', 64)
    _integer(max_word_length, 'max_word_length', 64)
    _integer(max_lexicon_entries, 'max_lexicon_entries', 50000)
    if min_word_length > max_word_length:
        raise ValueError('min_word_length cannot exceed max_word_length')
    if (isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float))
            or not .001 <= timeout_seconds <= 120 or not math.isfinite(timeout_seconds)):
        raise ValueError('timeout_seconds must be finite between 0.001 and 120')
    vocabulary, entries = _lexicon(lexicon, max_lexicon_entries)
    effective = [word for word in vocabulary if min_word_length <= len(word) <= max_word_length]
    trie = _trie(effective)
    root = _State(0, 0, (-1,) * 26, 0, ())
    stack = [root] if effective else []
    nodes, peak, solutions = 0, len(stack), 0
    candidates, plaintexts, boundary_patterns = [], set(), set()
    reason, pending = 'complete', 0
    deadline = started + timeout_seconds
    while stack:
        if time.monotonic() >= deadline:
            reason = 'timeout'
            break
        if nodes >= max_nodes:
            reason = 'node_limit'
            break
        state = stack.pop()
        nodes += 1
        node = trie[state.trie_node]
        if state.position == len(ciphertext):
            if node.terminal:
                candidate = _candidate(ciphertext, state)
                solutions += 1
                plaintexts.add(candidate['plaintext_letters'])
                boundary_patterns.add(tuple(candidate['word_boundaries']))
                if solutions <= max_candidates:
                    candidates.append(candidate)
                elif stack:
                    reason = 'candidate_limit'
                    break
            continue
        successors = []
        if node.terminal:
            successors.append(_State(state.position, 0, state.mapping, state.used_letters,
                                     state.boundaries + (state.position,)))
        cipher = ord(ciphertext[state.position]) - 65
        assigned = state.mapping[cipher]
        choices = ((assigned, node.children[assigned]),) if assigned in node.children else ()
        if assigned < 0:
            choices = sorted(node.children.items())
        for plain, child in choices:
            if assigned < 0:
                if state.used_letters & (1 << plain):
                    continue
                mapping = state.mapping[:cipher] + (plain,) + state.mapping[cipher + 1:]
                used = state.used_letters | (1 << plain)
            else:
                mapping, used = state.mapping, state.used_letters
            successors.append(_State(state.position + 1, child, mapping, used, state.boundaries))
        if len(stack) + len(successors) > max_states:
            pending = len(stack) + len(successors)
            reason = 'state_limit'
            break
        stack.extend(reversed(successors))
        peak = max(peak, len(stack))
    complete = reason == 'complete'
    pending = pending or len(stack)
    distinct = len(plaintexts)
    distinct_boundaries = len(boundary_patterns)
    forced = '?' * len(ciphertext)
    if complete and plaintexts:
        forced = ''.join(next(iter(values)) if len(values) == 1 else '?'
                         for values in (set(column) for column in zip(*sorted(plaintexts))))
    return {
        'method': 'unspaced-substitution', 'status': 'complete' if complete else 'incomplete',
        'model_status': 'sat' if solutions else ('unsat' if complete else 'unknown'),
        'claimed_plaintext': None, 'correctness_known': False, 'historical_solution_verified': False,
        'normalized_ciphertext': ciphertext, 'raw_input_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
        'ciphertext_sha256': _digest(ciphertext), 'distinct_symbols': len(set(ciphertext)),
        'lexicon_sha256': _digest('\n'.join(vocabulary)),
        'effective_lexicon_sha256': _digest('\n'.join(effective)),
        'dictionary_size': len(vocabulary), 'effective_dictionary_size': len(effective),
        'lexicon_entries_consumed': entries, 'trie_nodes': len(trie),
        'nodes': nodes, 'peak_states': peak, 'pending_states': pending,
        'solutions_found': solutions, 'segmentations_found': distinct_boundaries, 'plaintexts_found': distinct,
        'candidates': candidates, 'search_complete': complete, 'stop_reason': reason,
        'unique_plaintext_within_lexicon': complete and distinct == 1,
        'unique_segmentation_within_lexicon': complete and distinct_boundaries == 1,
        'ambiguous_plaintext': True if distinct > 1 else (False if complete else None),
        'ambiguous_boundaries': True if distinct_boundaries > 1 else (False if complete else None),
        'forced_plaintext': forced, 'elapsed_seconds': time.monotonic() - started,
        'bounds': {'max_nodes': max_nodes, 'max_states': max_states, 'max_candidates': max_candidates,
                   'min_word_length': min_word_length, 'max_word_length': max_word_length,
                   'max_lexicon_entries': max_lexicon_entries, 'timeout_seconds': timeout_seconds,
                   'max_lexicon_characters': MAX_LEXICON_CHARACTERS, 'max_trie_nodes': MAX_TRIE_NODES,
                   'max_raw_characters': MAX_RAW_CHARACTERS, 'max_normalized_letters': 512},
        'scope': 'Supplied-lexicon, declared-word-length, bijective A-Z substitution only. '
                 'Word boundaries are inferred. Completeness is not a historical verification or an exclusion of English. '
                 'Missing vocabulary, transcription errors and other cipher models remain untested.',
        'candidate_order': 'Deterministic alphabetical DFS, without a language score or answer-word bias',
    }
