"""Bounded bijective substitution with sparse quadgram deltas and replica exchange.

Replicas are logical chains in one process, not threads. Scores maximize the
existing English quadgram objective. A fitted candidate is not a historical
decipherment, a correctness probability, or an exhaustive key search.
"""
from __future__ import annotations

import math
import random
import time

from engine.alphabet import letters_only, reinject
from engine.language import get_model
from engine.result import SolveResult
from engine.solvers.substitution import frequency_decrypt_key

DEFAULT_TEMPERATURES = (0.25, 0.5, 0.9, 1.5, 2.5, 4.0, 7.0, 12.0)


def exchange_log_ratio(score_i: float, score_j: float, temperature_i: float, temperature_j: float) -> float:
    """log(pi(swapped)/pi(current)) for weights exp(score/temperature)."""
    return (1.0 / temperature_i - 1.0 / temperature_j) * (score_j - score_i)


def _integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{name} must be an integer in {low}..{high}')


def _validate_table(logp):
    if not isinstance(logp, (list, tuple)) or len(logp) != 26 ** 4 or any(
        isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or abs(v) > 1e100 for v in logp
    ):
        raise ValueError('quadgram table must contain 26**4 finite numeric scores with absolute value at most 1e100')


class _Topology:
    def __init__(self, seq):
        self.seq = seq
        self.windows = [tuple(seq[i:i + 4]) for i in range(len(seq) - 3)]
        coefficients = [[0] * len(self.windows) for _ in range(26)]
        for index, window in enumerate(self.windows):
            for symbol, weight in zip(window, (17576, 676, 26, 1)):
                coefficients[symbol][index] += weight
        # A swap changes index by (key[b]-key[a]) * (coeff[a]-coeff[b]).
        # Repeated symbols inside one window contribute their full weight.
        self.pairs = {}
        observed = set(seq)
        self.active_pairs = []
        for a in range(25):
            for b in range(a + 1, 26):
                self.pairs[a, b] = tuple((i, x - y) for i, (x, y) in enumerate(
                    zip(coefficients[a], coefficients[b])) if x != y)
                if a in observed or b in observed:
                    self.active_pairs.append((a, b))


class QuadgramSwapState:
    """A bijective key plus cached quadgram indices; useful for exact delta tests.

    delta does not mutate. commit consumes a delta for the current state.
    Caller-provided tables must have 26**4 finite log-score entries. The solver
    uses the existing repository table; public construction validates a table.
    """
    def __init__(self, seq, key, logp, *, _topology=None):
        if not isinstance(seq, (list, tuple)) or not 4 <= len(seq) <= 4096 or any(
            type(c) is not int or not 0 <= c < 26 for c in seq
        ):
            raise ValueError('sequence must contain 4..4096 A-Z integer symbols')
        if not isinstance(key, (list, tuple)) or len(key) != 26 or any(
            type(c) is not int for c in key
        ) or set(key) != set(range(26)):
            raise ValueError('key must be a permutation of the 26 integer letters')
        if _topology is None:
            _validate_table(logp)
        self.topology = _topology or _Topology(seq)
        self.key = list(key)
        self.logp = logp
        self.indices = [sum(key[c] * w for c, w in zip(window, (17576, 676, 26, 1)))
                        for window in self.topology.windows]
        self.score = sum(logp[index] for index in self.indices)

    def _pair(self, a, b):
        if type(a) is not int or type(b) is not int or not 0 <= a < 26 or not 0 <= b < 26 or a == b:
            raise ValueError('swap symbols must be distinct integer letters in 0..25')
        return (a, b) if a < b else (b, a)

    def delta(self, a, b):
        a, b = self._pair(a, b)
        change = self.key[b] - self.key[a]
        logp, indices = self.logp, self.indices
        total = 0.0
        for index, coefficient in self.topology.pairs[a, b]:
            old = indices[index]
            total += logp[old + change * coefficient] - logp[old]
        return total

    def commit(self, a, b, delta):
        a, b = self._pair(a, b)
        change = self.key[b] - self.key[a]
        for index, coefficient in self.topology.pairs[a, b]:
            self.indices[index] += change * coefficient
        self.key[a], self.key[b] = self.key[b], self.key[a]
        self.score += delta


def solve_substitution_parallel_tempering(
    text: str, *, seed: int = 20261003, restarts: int = 4, sweeps: int = 5000,
    temperatures=DEFAULT_TEMPERATURES, exchange_interval: int = 25,
    max_proposals: int = 2_000_000, timeout_seconds: float = 30.0,
    max_candidates: int = 10, polish_passes: int = 8, logp=None,
) -> SolveResult:
    """Return the best English-fitness candidate and an honest bounded run record.

    Each sweep makes one random swap per replica. Adjacent replica exchanges
    alternate disjoint even/odd pairs at exchange_interval sweeps. Each restart
    initializes a fresh ladder. A final greedy neighborhood polish per restart
    shares max_proposals with tempering. No plaintext, key, crib or neural model
    is supplied to this search. Configured completion is not keyspace coverage.
    An optional frozen dense logp table replaces the default English objective;
    the caller must record corpus provenance and must not alter it during search.
    """
    if not isinstance(text, str) or len(text) > 16384 or any(ord(c) > 127 and c.isalpha() for c in text):
        raise ValueError('text must be at most 16384 characters with ASCII cipher letters')
    letters = letters_only(text)
    if not 40 <= len(letters) <= 4096:
        raise ValueError('substitution search requires 40..4096 ASCII letters')
    for name, value, low, high in (
        ('seed', seed, -2**63, 2**63 - 1), ('restarts', restarts, 1, 128),
        ('sweeps', sweeps, 1, 2_000_000), ('exchange_interval', exchange_interval, 1, 100000),
        ('max_proposals', max_proposals, 1, 50_000_000), ('max_candidates', max_candidates, 1, 100),
        ('polish_passes', polish_passes, 0, 32),
    ):
        _integer(value, name, low, high)
    if not isinstance(temperatures, (tuple, list)) or not 2 <= len(temperatures) <= 16 or any(
        isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or not 0.01 <= t <= 1000
        for t in temperatures
    ) or any(a >= b for a, b in zip(temperatures, temperatures[1:])):
        raise ValueError('temperatures must be 2..16 strictly increasing finite values in 0.01..1000')
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not math.isfinite(
        timeout_seconds
    ) or not 0 < timeout_seconds <= 180:
        raise ValueError('timeout_seconds must be finite and greater than zero, at most 180')
    started = time.perf_counter()
    deadline = started + timeout_seconds
    seq = [ord(c) - 65 for c in letters]
    supplied_table = logp is not None
    if supplied_table:
        _validate_table(logp)
    else:
        logp = get_model().logp
    topology = _Topology(seq)
    base = frequency_decrypt_key(seq)
    rng = random.Random(seed)
    pairs = topology.active_pairs
    proposals = accepted = exchanges = exchange_accepted = window_updates = 0
    full_scores = restarts_completed = sweeps_completed = 0
    maximum_score_drift = 0.0
    stop_reason = 'configured_work_completed'
    candidate_by_plain = {}
    best_key = base[:]
    best_score = float('-inf')

    def state_for(key):
        nonlocal full_scores
        full_scores += 1
        return QuadgramSwapState(seq, key, logp, _topology=topology)

    def retain(key, score):
        nonlocal best_key, best_score, full_scores, maximum_score_drift
        state = state_for(key)
        maximum_score_drift = max(maximum_score_drift, abs(state.score - score)) if math.isfinite(score) else maximum_score_drift
        plain = ''.join(chr(65 + state.key[c]) for c in seq)
        inverse = [''] * 26
        for cipher, plain_letter in enumerate(state.key):
            inverse[plain_letter] = chr(65 + cipher)
        candidate = {'plaintext': plain, 'key': ''.join(inverse), 'score': state.score,
                     'decrypt_map': ''.join(chr(65 + p) for p in state.key),
                     'claimed_plaintext': None, 'status': 'unverified_fitness_candidate'}
        if plain not in candidate_by_plain or state.score > candidate_by_plain[plain]['score']:
            candidate_by_plain[plain] = candidate
        if len(candidate_by_plain) > max_candidates:
            worst = min(candidate_by_plain, key=lambda p: (candidate_by_plain[p]['score'], p))
            del candidate_by_plain[worst]
        if state.score > best_score:
            best_score, best_key = state.score, key[:]

    def available():
        nonlocal stop_reason
        if proposals >= max_proposals:
            stop_reason = 'proposal_limit'
            return False
        if time.perf_counter() >= deadline:
            stop_reason = 'time_limit'
            return False
        return True

    def propose(state, a, b):
        nonlocal proposals, window_updates
        proposals += 1
        window_updates += len(topology.pairs[a, b])
        return state.delta(a, b)

    # Retain an initial consistent candidate even when initialization consumes
    # the time allowance. The wall bound is cooperative, checked in batches.
    initial = state_for(base)
    retain(base, initial.score)
    for restart in range(restarts):
        if not available():
            break
        states = []
        for replica in range(len(temperatures)):
            key = base[:]
            if restart == 0 and replica == 0:
                pass
            elif replica < 3:
                for _ in range(3 + 2 * replica + restart):
                    a, b = rng.choice(pairs)
                    key[a], key[b] = key[b], key[a]
            else:
                rng.shuffle(key)
            states.append(state_for(key))
        local_key = max(states, key=lambda state: state.score).key[:]
        local_score = max(state.score for state in states)
        completed_restart = True
        exchange_phase = 0
        for sweep in range(sweeps):
            if sweep % 32 == 0 and not available():
                completed_restart = False
                break
            for replica, temperature in enumerate(temperatures):
                if proposals >= max_proposals:
                    stop_reason = 'proposal_limit'
                    completed_restart = False
                    break
                state = states[replica]
                a, b = rng.choice(pairs)
                delta = propose(state, a, b)
                if delta >= 0 or rng.random() < math.exp(delta / temperature):
                    state.commit(a, b, delta)
                    accepted += 1
                    if state.score > local_score + 1e-9:
                        local_score, local_key = state.score, state.key[:]
            if not completed_restart:
                break
            sweeps_completed += 1
            if (sweep + 1) % exchange_interval == 0:
                for replica in range(exchange_phase, len(states) - 1, 2):
                    exchanges += 1
                    ratio = exchange_log_ratio(states[replica].score, states[replica + 1].score,
                                               temperatures[replica], temperatures[replica + 1])
                    if ratio >= 0 or rng.random() < math.exp(ratio):
                        states[replica], states[replica + 1] = states[replica + 1], states[replica]
                        exchange_accepted += 1
                exchange_phase = 1 - exchange_phase
        polished = state_for(local_key)
        for _ in range(polish_passes):
            if not available():
                completed_restart = False
                break
            improved = False
            for pair_index, (a, b) in enumerate(pairs):
                if proposals >= max_proposals or pair_index % 32 == 0 and not available():
                    if proposals >= max_proposals:
                        stop_reason = 'proposal_limit'
                    completed_restart = False
                    break
                delta = propose(polished, a, b)
                if delta > 1e-9:
                    polished.commit(a, b, delta)
                    accepted += 1
                    improved = True
            if not completed_restart or not improved:
                break
        retain(polished.key, polished.score)
        # Initialization or budget interruption can leave the original best
        # above the greedy result only by floating point noise; retain both.
        retain(local_key, local_score)
        if not completed_restart:
            break
        restarts_completed += 1
    candidates = sorted(candidate_by_plain.values(), key=lambda c: (-c['score'], c['plaintext']))
    inverse = [''] * 26
    for cipher, plain in enumerate(best_key):
        inverse[plain] = chr(65 + cipher)
    plain = ''.join(chr(65 + best_key[c]) for c in seq)
    return SolveResult(
        method='substitution_parallel_tempering', plaintext=reinject(text, plain),
        key=''.join(inverse), score=best_score,
        details={'seed': seed, 'letters': len(letters), 'restarts': restarts,
                 'sweeps_per_restart': sweeps, 'temperatures': list(temperatures),
                 'exchange_interval': exchange_interval, 'max_proposals': max_proposals,
                 'timeout_seconds': timeout_seconds, 'polish_passes': polish_passes,
                 'proposals': proposals, 'accepted_swaps': accepted,
                 'affected_quadgram_windows_evaluated': window_updates,
                 'exchange_attempts': exchanges, 'exchange_accepted': exchange_accepted,
                 'full_score_calls': full_scores, 'maximum_cached_score_drift': maximum_score_drift,
                 'restarts_completed': restarts_completed, 'sweeps_completed': sweeps_completed,
                 'configured_search_complete': restarts_completed == restarts,
                 'stop_reason': stop_reason, 'elapsed_seconds': time.perf_counter() - started,
                 'candidates': candidates, 'max_candidates': max_candidates,
                 'decrypt_map': ''.join(chr(65 + p) for p in best_key),
                 'fitness': 'supplied dense quadgram fitness, not correctness probability' if supplied_table else 'existing English quadgram log fitness, not correctness probability',
                 'supplied_score_table': supplied_table,
                 'operation_definition': 'One proposal evaluates one bijective key swap; repeated states allowed. Exchanges, full scores and affected windows counted separately.',
                 'wall_limit_scope': 'Cooperative batch checks; model/topology initialization and final result serialization can add overhead.',
                 'exhaustive_key_search': False, 'claimed_plaintext': None,
                 'status': 'unverified_fitness_candidate'},
    )
