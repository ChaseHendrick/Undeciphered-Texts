"""Preference for candidate sentences that use fortune, heir, and estate.

Persona: inheritance. Reworded from a dying-aristocrat label into plain
speech about a household and what was left. The word list is a preference
among candidates. These are preferences among candidates, not decipherments
of Nr. 86, K4, or an unknown script.

The separate investigate_inheritance API performs real bounded classical
cipher searches using caller clues. Its hypotheses are never verified
historical readings; the preference word list supplies no search evidence.
"""

from __future__ import annotations

import re
from collections import deque
from collections.abc import Sequence

from engine.language import get_model
from engine.persona_solver_common import make_report, validate_inputs
from engine.solvers.autokey import autokey_decrypt, autokey_encrypt
from engine.solvers.condi import condi_decrypt, condi_encrypt

# Word list for the inheritance preference: fortune, heir, estate.
WORD_LIST = ("fortune", "heir", "estate")

DISCLAIMER = (
    "These are preferences among candidates, not decipherments of "
    "Nr. 86, K4, or an unknown script."
)


def covers(text: str) -> bool:
    """True when every inheritance word appears as its own word."""
    lowered = text.lower()
    return all(re.search(rf"\b{re.escape(word)}\b", lowered) for word in WORD_LIST)


def choose(left: str, right: str) -> str:
    """Pick the candidate that matches the inheritance word list.

    Exactly one of the two sentences must contain fortune, heir, and estate.
    The other is a plain alternative. This does not decipher anything.
    """
    left_ok = covers(left)
    right_ok = covers(right)
    if left_ok == right_ok:
        raise ValueError("need exactly one candidate that matches the word list")
    return left if left_ok else right


def _hints(value, name, maximum):
    if value is None:
        return ()
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence of words")
    if len(value) > maximum:
        raise ValueError(f"{name} supports at most {maximum} entries")
    words = []
    total = 0
    for word in value:
        if not isinstance(word, str):
            raise TypeError(f"{name} entries must be strings")
        if not 1 <= len(word) <= 64 or not all(c.isascii() and c.isalpha() for c in word):
            raise ValueError(f"{name} entries require 1..64 ASCII letters")
        total += len(word)
        if total > 16384:
            raise ValueError(f"{name} supports at most 16384 supplied letters")
        cleaned = word.upper()
        if cleaned not in words:
            words.append(cleaned)
    return tuple(words)


def _pattern(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def _vigenere(text, keyword, decrypt=False):
    sign = -1 if decrypt else 1
    return "".join(chr(65 + (ord(c) - 65 + sign * (ord(keyword[i % len(keyword)]) - 65)) % 26)
                   for i, c in enumerate(text))


def _word_tasks(text, cipher, lexicon, known, action):
    """Each yielded callable tests exactly one word assignment, without lookahead work."""
    words = tuple(dict.fromkeys(w.upper() for w in re.findall(r"[A-Za-z]+", text)))
    domains = {word: tuple(w for w in sorted(lexicon) if _pattern(w) == _pattern(word)) for word in words}
    action["word_divisions_assumed"] = True
    action["unique_ciphertext_words"] = len(words)
    missing = [word for word in words if not domains[word]]
    if missing:
        action["missing_pattern_word_count"] = len(missing)
        return
    c2p, p2c = {}, {}
    for index, plain in known.items():
        encrypted = cipher[index]
        if (encrypted in c2p and c2p[encrypted] != plain) or (plain in p2c and p2c[plain] != encrypted):
            action["crib_mapping_contradiction"] = True
            return
        c2p[encrypted] = plain
        p2c[plain] = encrypted
    ordered = sorted(words, key=lambda w: (len(domains[w]), -len(w), w))
    stack = [[0, 0, c2p, p2c]]
    while stack:
        depth, cursor, old_c2p, old_p2c = stack[-1]
        word = ordered[depth]
        if cursor == len(domains[word]):
            stack.pop()
            continue
        plain_word = domains[word][cursor]
        stack[-1][1] += 1
        next_maps = []

        def trial(word=word, plain_word=plain_word, depth=depth,
                  old_c2p=old_c2p, old_p2c=old_p2c, next_maps=next_maps):
            new_c2p, new_p2c = dict(old_c2p), dict(old_p2c)
            for encrypted, plain in zip(word, plain_word):
                if ((encrypted in new_c2p and new_c2p[encrypted] != plain)
                        or (plain in new_p2c and new_p2c[plain] != encrypted)):
                    return None
                new_c2p[encrypted] = plain
                new_p2c[plain] = encrypted
            if depth + 1 < len(ordered):
                next_maps.append((new_c2p, new_p2c))
                return None
            plaintext = "".join(new_c2p[c] for c in cipher)
            key = "".join(new_p2c.get(chr(65 + i), "?") for i in range(26))
            forward = "".join(key[ord(c) - 65] for c in plaintext)
            return {"plaintext": plaintext, "family": "substitution", "key": {"plaintext_to_ciphertext": key},
                    "forward": forward, "evidence": {"method": "supplied lexicon word-pattern bijection",
                    "assumed_preserved_word_divisions": True, "unseen_plaintext_key_slots": key.count("?")}}

        yield trial
        if next_maps:
            new_c2p, new_p2c = next_maps[0]
            stack.append([depth + 1, 0, new_c2p, new_p2c])


def _keyword_tasks(cipher, keywords, family):
    for keyword in keywords:
        def trial(keyword=keyword):
            if family == "vigenere":
                plain = _vigenere(cipher, keyword, True)
                forward = _vigenere(plain, keyword)
            else:
                plain = autokey_decrypt(cipher, keyword)
                forward = autokey_encrypt(plain, keyword)
            return {"plaintext": plain, "family": family, "key": {"keyword": keyword}, "forward": forward,
                    "evidence": {"method": "caller-supplied keyword guess", "selected_key_supplied": False}}
        yield trial


def _condi_tasks(cipher, keywords):
    for keyword in keywords:
        for shift in range(26):
            for offset in range(26):
                def trial(keyword=keyword, shift=shift, offset=offset):
                    params = {"keyword": keyword, "alphabet_shift": shift, "initial_offset": offset}
                    plain = condi_decrypt(cipher, **params)
                    return {"plaintext": plain, "family": "condi", "key": params,
                            "forward": condi_encrypt(plain, **params), "evidence": {
                            "method": "caller-supplied keyword guess with tested alphabet shift and offset",
                            "selected_key_supplied": False}}
                yield trial


def _crib_autokey_tasks(cipher, known, action):
    for period in range(1, min(32, len(cipher)) + 1):
        def trial(period=period):
            forced = {i: ord(c) - 65 for i, c in known.items()}
            queue = deque(forced)
            while queue:
                index = queue.popleft()
                neighbors = []
                if index >= period:
                    neighbors.append((index - period, (ord(cipher[index]) - 65 - forced[index]) % 26))
                if index + period < len(cipher):
                    after = index + period
                    neighbors.append((after, (ord(cipher[after]) - 65 - forced[index]) % 26))
                for neighbor, value in neighbors:
                    if neighbor in forced:
                        if forced[neighbor] != value:
                            action["inconsistent_periods"] += 1
                            return None
                    else:
                        forced[neighbor] = value
                        queue.append(neighbor)
            if len(forced) < len(cipher):
                action["partial_periods"] += 1
                action["maximum_forced_letters_in_partial_period"] = max(
                    action["maximum_forced_letters_in_partial_period"], len(forced))
                return None
            plain = "".join(chr(65 + forced[i]) for i in range(len(cipher)))
            keyword = "".join(chr(65 + (ord(cipher[i]) - 65 - forced[i]) % 26) for i in range(period))
            return {"plaintext": plain, "family": "autokey", "key": {"keyword": keyword, "period": period},
                    "forward": autokey_encrypt(plain, keyword), "evidence": {
                    "method": "exact bidirectional plaintext-autokey crib propagation",
                    "all_plaintext_letters_forced_within_period": True,
                    "primer_supplied": False, "period": period}}
        yield trial


def investigate_inheritance(text, *, cribs=(), lexicon=None, keywords=None,
                           max_checks=5000, max_candidates=20):
    """Investigate explicit caller clues with one round-robin bounded budget.

    A check tests one supplied word assignment, keyword/setting, or complete
    bounded-period crib propagation. Candidate storage keeps ranked examples
    without stopping search. Partial autokey columns are not filled by scores.
    """
    cipher, _, known = validate_inputs(text, cribs, max_checks, max_candidates)
    words = _hints(lexicon, "lexicon", 512)
    guesses = _hints(keywords, "keywords", 128)
    condi_guesses = tuple(dict.fromkeys("".join(dict.fromkeys(word)) for word in guesses))
    actions = []
    branches = deque()
    retained = {}
    checks = compatible = 0
    model = None

    def add(name, tasks, **metadata):
        action = {"branch": name, "checks": 0, "search_complete": False, **metadata}
        actions.append(action)
        iterator = iter(tasks(action))
        task = next(iterator, None)
        if task is None:
            action["search_complete"] = True
        else:
            branches.append((action, iterator, task))

    if words:
        add("substitution", lambda action: _word_tasks(text, cipher, words, known, action), supplied_words=len(words))
    if guesses:
        add("vigenere", lambda action: _keyword_tasks(cipher, guesses, "vigenere"), declared_trials=len(guesses))
        add("keyword_autokey", lambda action: _keyword_tasks(cipher, guesses, "autokey"), declared_trials=len(guesses))
        add("condi", lambda action: _condi_tasks(cipher, condi_guesses),
            declared_trials=676 * len(condi_guesses), alphabet_shifts=list(range(26)), initial_offsets=list(range(26)))
    if known:
        add("crib_autokey", lambda action: _crib_autokey_tasks(cipher, known, action),
            maximum_period=min(32, len(cipher)), partial_periods=0, inconsistent_periods=0,
            maximum_forced_letters_in_partial_period=0)

    while branches and checks < max_checks:
        action, iterator, task = branches.popleft()
        trial = task()
        checks += 1
        action["checks"] += 1
        if trial is not None:
            plain = trial["plaintext"]
            if trial.pop("forward") != cipher:
                raise RuntimeError("Inheritance trial failed forward verification")
            if all(plain[i] == letter for i, letter in known.items()):
                compatible += 1
                if model is None:
                    model = get_model()
                trial["score"] = model.score([ord(c) - 65 for c in plain]) / max(1, len(plain) - 3)
                trial["forward_consistent"] = True
                trial["crib_match"] = True
                trial["evidence"].update({"known_positions": len(known),
                    "predicted_letters_beyond_crib": len(cipher) - len(known),
                    "score_is_correctness": False, "independently_verified": False})
                identity = (trial["family"], plain)
                previous = retained.get(identity)
                if previous is None or _candidate_order(trial) < _candidate_order(previous):
                    retained[identity] = trial
                ordered = sorted(retained.values(), key=_candidate_order)[:max_candidates]
                retained = {(c["family"], c["plaintext"]): c for c in ordered}
        upcoming = next(iterator, None)
        if upcoming is None:
            action["search_complete"] = True
        else:
            branches.append((action, iterator, upcoming))

    no_clues = not words and not guesses and not known
    complete = not branches and not no_clues
    reason = "no_clues" if no_clues else "completed" if complete else "check_budget"
    candidates = sorted(retained.values(), key=_candidate_order)
    report = make_report("inheritance", "caller-clue word patterns, keyword guesses and exact autokey propagation",
        candidates, checks, max_checks, complete, reason, actions, [
        "Only caller-supplied lexicon, keyword guesses and cribs provide clues; preference words are unused.",
        "Word-pattern substitution assumes supplied source word divisions survived encryption.",
        "Ordinary Vigenere, plaintext autokey and Condi are conditional family assumptions.",
        "Crib-only autokey periods are bounded at 32; unforced columns never produce a full candidate.",
        "One check is a word assignment, key/setting trial or bounded-period propagation, not a CPU instruction.",
        "Quadgram ranking from engine/data/english.txt is English fitness, not verified correctness.",
        "Completion covers declared branches, not all ciphers or all keyword/lexicon possibilities."])
    report["known_positions"] = len(known)
    report["compatible_trials"] = compatible
    report["retention"] = {"max_candidates": max_candidates,
        "deduplication": "same family and full plaintext among retained examples",
        "ranking_exhaustive_over_all_keys": False, "candidate_limit_stops_search": False}
    return report


def _candidate_order(candidate):
    return (-candidate["score"], candidate["family"], candidate["plaintext"], repr(candidate["key"]))
