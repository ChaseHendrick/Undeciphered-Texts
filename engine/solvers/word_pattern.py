"""Bounded word-pattern constraint search for monoalphabetic substitution.

Requires word divisions and a supplied lexicon, but never a supplied key.
Domains contain dictionary words with the same repeated-letter pattern.
Minimum remaining values chooses a word; a shared injective cipher-to-plain
map forward-checks every other domain after each tentative assignment.

Algorithm reference: AIMA Python's CSP backtracking, MRV and forward checking:
https://github.com/aimacode/aima-python/blob/master/aima/csp.py

This implementation uses word constraints, not an n-gram score or beam search.
Uniqueness is only within the supplied lexicon and the substitution model.
It does not decipher an unknown writing system or claim an unsolved text.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from engine.alphabet import ALPHABET
from engine.result import SolveResult


SOURCE_URL = "https://github.com/aimacode/aima-python/blob/master/aima/csp.py"
SCOPE = (
    "Word-separated A-Z monoalphabetic substitution with a supplied lexicon. "
    "A unique candidate is unique only within that lexicon and model; "
    "not an unknown-script reading or a solution of Kryptos K4, Zodiac, "
    "Beale, McCormick, Voynich, or army message Nr. 86."
)
_WORD = re.compile(r"[A-Za-z]+")
_ASCII = frozenset(ALPHABET + ALPHABET.lower())


def _normalize_word(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("lexicon entries and pattern inputs must be strings")
    if _WORD.fullmatch(value) is None:
        raise ValueError("lexicon entries and pattern inputs must be single A-Z words")
    return value.upper()


def word_pattern(word: str) -> tuple[int, ...]:
    """Number distinct letters by first occurrence: NOON and DEED are 0,1,1,0."""
    normalized = _normalize_word(word)
    seen: dict[str, int] = {}
    return tuple(seen.setdefault(letter, len(seen)) for letter in normalized)


@dataclass(frozen=True)
class WordPatternCandidate:
    """One consistent plaintext and cipher-to-plain key, in ciphertext A-Z order.

Question marks mark unobserved cipher letters. Their assignments are not
invented; even a unique plaintext need not determine a complete 26-letter key.
    """

    plaintext: str
    decrypt_key: str

    @property
    def key_complete(self) -> bool:
        return "?" not in self.decrypt_key


@dataclass(frozen=True)
class WordPatternSearchResult:
    """Candidates plus exact search limits and lexicon-relative certainty."""

    candidates: tuple[WordPatternCandidate, ...]
    nodes: int
    pruned_values: int
    solutions_found: int
    search_complete: bool
    stop_reason: str
    dictionary_size: int
    unique_words: int
    first_selected_word: str

    @property
    def ambiguous(self) -> bool | None:
        """True if multiple answers were found; None if ambiguity remains unknown."""
        if self.solutions_found > 1:
            return True
        return False if self.search_complete else None

    @property
    def unique_within_lexicon(self) -> bool:
        return self.search_complete and self.solutions_found == 1


@dataclass
class _Frame:
    word: str
    remaining: tuple[str, ...]
    domains: dict[str, tuple[str, ...]]
    cipher_to_plain: dict[str, str]
    plain_to_cipher: dict[str, str]
    choices: Iterator[str]


def _frame(
    remaining: tuple[str, ...],
    domains: dict[str, tuple[str, ...]],
    cipher_to_plain: dict[str, str],
    plain_to_cipher: dict[str, str],
) -> _Frame:
    # MRV first, then more distinct letters and longer words for stable ties.
    word = min(remaining, key=lambda item: (
        len(domains[item]), -len(set(item)), -len(item), item,
    ))
    return _Frame(word, tuple(item for item in remaining if item != word), domains,
                  cipher_to_plain, plain_to_cipher, iter(domains[word]))


def _compatible(
    cipher_word: str,
    plain_word: str,
    cipher_to_plain: dict[str, str],
    plain_to_cipher: dict[str, str],
) -> bool:
    # Matching word patterns already enforce the constraints within a word.
    # These maps enforce consistency and injectivity across different words.
    return all(
        cipher_to_plain.get(cipher, plain) == plain
        and plain_to_cipher.get(plain, cipher) == cipher
        for cipher, plain in zip(cipher_word, plain_word)
    )


def _candidate(text: str, mapping: dict[str, str]) -> WordPatternCandidate:
    plaintext = "".join(
        mapping[ch.upper()].lower() if "a" <= ch <= "z"
        else mapping[ch] if "A" <= ch <= "Z" else ch
        for ch in text
    )
    return WordPatternCandidate(plaintext, "".join(mapping.get(ch, "?") for ch in ALPHABET))


def search_word_pattern(
    ciphertext: str,
    words: Iterable[str],
    *,
    max_nodes: int = 10000,
    max_candidates: int = 20,
) -> WordPatternSearchResult:
    """Enumerate lexicon-consistent decryptions without being given a key.

Each tentative word assignment consumes one node. The node budget bounds
search, after the finite lexicon and initial domains are prepared. Iterative
DFS avoids a recursion-depth limit on long texts. At most max_candidates
answers are stored. Finding one further answer stops with candidate_limit.

If a budget ends search, an empty candidate list does not prove no solution,
and a single found candidate does not prove uniqueness. Completion proves
only that all words in the supplied lexicon were considered under this model.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a string")
    if any(ch.isalpha() and ch not in _ASCII for ch in ciphertext):
        raise ValueError("ciphertext letters must use A-Z")
    for name, value in (("max_nodes", max_nodes), ("max_candidates", max_candidates)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    cipher_words = tuple(dict.fromkeys(word.upper() for word in _WORD.findall(ciphertext)))
    if not cipher_words:
        raise ValueError("ciphertext must contain at least one A-Z word")
    if isinstance(words, (str, bytes)):
        raise TypeError("words must be an iterable of dictionary words, not a string")
    lexicon = sorted({_normalize_word(word) for word in words})
    if not lexicon:
        raise ValueError("words must contain at least one dictionary word")
    index: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in lexicon:
        index[word_pattern(word)].append(word)
    domains = {word: tuple(index[word_pattern(word)]) for word in cipher_words}
    candidates: list[WordPatternCandidate] = []
    nodes = pruned_values = solutions_found = 0
    stop_reason = "complete"
    first_selected_word = ""
    stack: list[_Frame] = []
    if all(domains.values()):
        stack.append(_frame(cipher_words, domains, {}, {}))
        first_selected_word = stack[0].word
    while stack:
        frame = stack[-1]
        try:
            plain_word = next(frame.choices)
        except StopIteration:
            stack.pop()
            continue
        # Exhausted iterators are removed before this check, so an exact last
        # allowed node can still end with a complete proof of dictionary search.
        if nodes >= max_nodes:
            stop_reason = "node_limit"
            break
        nodes += 1
        forward = dict(frame.cipher_to_plain)
        reverse = dict(frame.plain_to_cipher)
        for cipher, plain in zip(frame.word, plain_word):
            forward[cipher] = plain
            reverse[plain] = cipher
        if not frame.remaining:
            solutions_found += 1
            if solutions_found > max_candidates:
                stop_reason = "candidate_limit"
                break
            candidates.append(_candidate(ciphertext, forward))
            continue
        filtered: dict[str, tuple[str, ...]] = {}
        for word in frame.remaining:
            options = tuple(plain for plain in frame.domains[word]
                            if _compatible(word, plain, forward, reverse))
            pruned_values += len(frame.domains[word]) - len(options)
            if not options:
                break
            filtered[word] = options
        else:
            stack.append(_frame(frame.remaining, filtered, forward, reverse))
    return WordPatternSearchResult(
        candidates=tuple(candidates), nodes=nodes, pruned_values=pruned_values,
        solutions_found=solutions_found, search_complete=stop_reason == "complete",
        stop_reason=stop_reason, dictionary_size=len(lexicon),
        unique_words=len(cipher_words), first_selected_word=first_selected_word,
    )


def solve_word_pattern(
    ciphertext: str,
    words: Iterable[str],
    *,
    max_nodes: int = 10000,
    max_candidates: int = 20,
) -> SolveResult:
    """Return plaintext only when exhaustive search finds one lexicon answer.

All retained candidates remain in details for ambiguous or bounded searches.
An empty top-level plaintext then means no unique answer was established.
    """
    search = search_word_pattern(ciphertext, words, max_nodes=max_nodes,
                                 max_candidates=max_candidates)
    selected = search.candidates[0] if search.unique_within_lexicon else None
    return SolveResult(
        method="word-pattern-substitution",
        plaintext=selected.plaintext if selected else "",
        key=selected.decrypt_key if selected else "",
        score=float(search.unique_words) if selected else 0.0,
        details={
            "mode": "key_search",
            "algorithm": "word-pattern MRV backtracking with forward checking",
            "search_complete": search.search_complete,
            "stop_reason": search.stop_reason,
            "unique_within_lexicon": search.unique_within_lexicon,
            "ambiguous": search.ambiguous,
            "solutions_found": search.solutions_found,
            "solution_count_exact": search.search_complete,
            "nodes": search.nodes,
            "max_nodes": max_nodes,
            "max_candidates": max_candidates,
            "pruned_values": search.pruned_values,
            "dictionary_size": search.dictionary_size,
            "unique_words": search.unique_words,
            "first_selected_word": search.first_selected_word,
            "key_complete": selected.key_complete if selected else False,
            "key_direction": "ciphertext A-Z to plaintext, ? for unobserved letters",
            "candidates": [{"plaintext": candidate.plaintext,
                            "decrypt_key": candidate.decrypt_key,
                            "key_complete": candidate.key_complete}
                           for candidate in search.candidates],
            "source_url": SOURCE_URL,
            "scope": SCOPE,
        },
    )


__all__ = [
    "SOURCE_URL", "SCOPE", "WordPatternCandidate", "WordPatternSearchResult",
    "word_pattern", "search_word_pattern", "solve_word_pattern",
]
