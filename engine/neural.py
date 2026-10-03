"""Learned English letter fitness: a small trigram neural language model.

The two previous letters are one-hot encoded, passed through a tanh hidden
layer, and scored with a 26-way softmax. Weights are fit by momentum gradient descent
on next-letter cross-entropy. The training prose is Jane Austen, Pride and Prejudice, chapters I-III
(Project Gutenberg eBook 1342), not the held-out Doyle passage and not the
demo or test plaintext. Held-out numbers are in docs/neural-grade.md.

The substitution solver still searches with the quadgram model. This network
is a second opinion on a candidate decipherment. A higher score means the
Latin-letter string looks more like that English sample. It is not a reading
of Linear A, the Voynich manuscript, or the Vesuvius scrolls.

Numpy is used for the matrix updates when it is installed. The same model
trains with the standard library otherwise.
"""

from __future__ import annotations

import math
import random
from functools import lru_cache
from pathlib import Path

from engine.alphabet import letters_only

_DATA = Path(__file__).resolve().parent / "data" / "neural_train_austen.txt"

HIDDEN = 32
NUMPY_EPOCHS = 60
PURE_EPOCHS = 24
MOMENTUM = 0.8
SEED = 20261002


def load_training_prose(path: Path | None = None) -> str:
    """Return the training prose, skipping leading '#' attribution lines."""
    raw = (path or _DATA).read_text(encoding="utf-8")
    lines = [line for line in raw.splitlines() if not line.startswith("#")]
    return "\n".join(lines).strip()


class NeuralLetterModel:
    """Trainable character-level trigram network. Higher score is better."""

    def __init__(self, prose: str, seed: int = SEED) -> None:
        letters = "".join(ch for ch in letters_only(prose) if "A" <= ch <= "Z")
        if len(letters) < 8:
            raise ValueError("neural training sample is too short")
        self.training_letters = letters
        self.hidden = HIDDEN
        self.backend = "python"
        self.initial_loss = 0.0
        self.final_loss = 0.0
        self.train_events = 0
        self.W1: list[list[float]] = []
        self.b1: list[float] = []
        self.W2: list[list[float]] = []
        self.b2: list[float] = []
        self._fit(letters, seed)

    def _contexts(self, letters: str) -> list[tuple[int, int, list[int], int]]:
        ints = [ord(ch) - 65 for ch in letters]
        counts: dict[tuple[int, int], list[int]] = {}
        for i in range(2, len(ints)):
            key = (ints[i - 2], ints[i - 1])
            bucket = counts.get(key)
            if bucket is None:
                bucket = [0] * 26
                counts[key] = bucket
            bucket[ints[i]] += 1
        rows: list[tuple[int, int, list[int], int]] = []
        events = 0
        for (left, mid), bucket in counts.items():
            total = sum(bucket)
            events += total
            rows.append((left, mid, bucket, total))
        self.train_events = events
        return rows

    def _fit(self, letters: str, seed: int) -> None:
        rows = self._contexts(letters)
        try:
            import numpy as np
        except ImportError:
            np = None
        if np is not None:
            self.backend = "numpy"
            self._fit_numpy(rows, seed, np)
        else:
            self.backend = "python"
            self._fit_python(rows, seed)

    def _fit_numpy(self, rows: list[tuple[int, int, list[int], int]], seed: int, np) -> None:
        hidden = self.hidden
        n = len(rows)
        features = np.zeros((n, 52), dtype=np.float64)
        targets = np.zeros((n, 26), dtype=np.float64)
        weight = np.zeros(n, dtype=np.float64)
        for i, (left, mid, bucket, total) in enumerate(rows):
            features[i, left] = 1.0
            features[i, 26 + mid] = 1.0
            targets[i] = np.asarray(bucket, dtype=np.float64) / total
            weight[i] = total
        weight /= weight.sum()

        rng = np.random.default_rng(seed)
        w1 = rng.normal(0.0, 0.08, size=(52, hidden))
        b1 = np.zeros(hidden)
        w2 = rng.normal(0.0, 0.08, size=(hidden, 26))
        b2 = np.zeros(26)

        def loss_of(logits) -> float:
            shifted = logits - logits.max(axis=1, keepdims=True)
            log_probs = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
            return float(-np.sum(weight * np.sum(targets * log_probs, axis=1)))

        initial = None
        final = None
        vel_w1 = np.zeros_like(w1)
        vel_b1 = np.zeros_like(b1)
        vel_w2 = np.zeros_like(w2)
        vel_b2 = np.zeros_like(b2)
        for epoch in range(NUMPY_EPOCHS):
            rate = 1.2 if epoch < NUMPY_EPOCHS // 2 else 0.35
            hidden_pre = features @ w1 + b1
            activated = np.tanh(hidden_pre)
            logits = activated @ w2 + b2
            current = loss_of(logits)
            if initial is None:
                initial = current
            final = current
            shifted = logits - logits.max(axis=1, keepdims=True)
            probs = np.exp(shifted)
            probs /= probs.sum(axis=1, keepdims=True)
            grad_logits = (probs - targets) * weight[:, None]
            grad_w2 = activated.T @ grad_logits
            grad_b2 = grad_logits.sum(axis=0)
            grad_hidden = grad_logits @ w2.T
            grad_pre = grad_hidden * (1.0 - activated * activated)
            grad_w1 = features.T @ grad_pre
            grad_b1 = grad_pre.sum(axis=0)
            vel_w1 = MOMENTUM * vel_w1 + grad_w1
            vel_b1 = MOMENTUM * vel_b1 + grad_b1
            vel_w2 = MOMENTUM * vel_w2 + grad_w2
            vel_b2 = MOMENTUM * vel_b2 + grad_b2
            w1 -= rate * vel_w1
            b1 -= rate * vel_b1
            w2 -= rate * vel_w2
            b2 -= rate * vel_b2
        self.initial_loss = float(initial)
        self.final_loss = float(final)
        # W1 is 52 x hidden, W2 is hidden x 26, matching the pure-Python layout.
        self.W1 = w1.tolist()
        self.b1 = b1.tolist()
        self.W2 = w2.tolist()
        self.b2 = b2.tolist()

    def _fit_python(self, rows: list[tuple[int, int, list[int], int]], seed: int) -> None:
        hidden = self.hidden
        rng = random.Random(seed)
        w1 = [[rng.gauss(0.0, 0.08) for _ in range(hidden)] for _ in range(52)]
        b1 = [0.0] * hidden
        w2 = [[rng.gauss(0.0, 0.08) for _ in range(26)] for _ in range(hidden)]
        b2 = [0.0] * 26
        events = float(self.train_events)
        initial = None
        final = None
        for epoch in range(PURE_EPOCHS):
            rate = 0.9 if epoch < PURE_EPOCHS // 2 else 0.3
            grad_w1 = [[0.0] * hidden for _ in range(52)]
            grad_b1 = [0.0] * hidden
            grad_w2 = [[0.0] * 26 for _ in range(hidden)]
            grad_b2 = [0.0] * 26
            loss = 0.0
            for left, mid, bucket, total in rows:
                hidden_pre = [b1[j] + w1[left][j] + w1[26 + mid][j] for j in range(hidden)]
                activated = [math.tanh(value) for value in hidden_pre]
                logits = [
                    b2[k] + sum(activated[j] * w2[j][k] for j in range(hidden))
                    for k in range(26)
                ]
                peak = max(logits)
                exp_shift = [math.exp(value - peak) for value in logits]
                partition = sum(exp_shift)
                probs = [value / partition for value in exp_shift]
                log_partition = math.log(partition) + peak
                cross = 0.0
                for k in range(26):
                    if bucket[k]:
                        cross -= (bucket[k] / total) * (logits[k] - log_partition)
                loss += total * cross
                scale = total / events
                grad_logits = [(probs[k] - (bucket[k] / total)) * scale for k in range(26)]
                for j in range(hidden):
                    back = sum(grad_logits[k] * w2[j][k] for k in range(26))
                    back *= 1.0 - activated[j] * activated[j]
                    grad_b1[j] += back
                    grad_w1[left][j] += back
                    grad_w1[26 + mid][j] += back
                    activated_j = activated[j]
                    row = grad_w2[j]
                    for k in range(26):
                        row[k] += activated_j * grad_logits[k]
                for k in range(26):
                    grad_b2[k] += grad_logits[k]
            for i in range(52):
                for j in range(hidden):
                    w1[i][j] -= rate * grad_w1[i][j]
            for j in range(hidden):
                b1[j] -= rate * grad_b1[j]
                for k in range(26):
                    w2[j][k] -= rate * grad_w2[j][k]
            for k in range(26):
                b2[k] -= rate * grad_b2[k]
            mean_loss = loss / events
            if initial is None:
                initial = mean_loss
            final = mean_loss
        self.initial_loss = float(initial)
        self.final_loss = float(final)
        self.W1 = w1
        self.b1 = b1
        self.W2 = w2
        self.b2 = b2

    def _cache_numpy(self):
        import numpy as np

        self._np_w1 = np.asarray(self.W1, dtype=np.float64)
        self._np_b1 = np.asarray(self.b1, dtype=np.float64)
        self._np_w2 = np.asarray(self.W2, dtype=np.float64)
        self._np_b2 = np.asarray(self.b2, dtype=np.float64)

    def score(self, seq: list[int]) -> float:
        """Sum of log P(letter_t | letter_t-2, letter_t-1). Higher is better."""
        if len(seq) < 3:
            return 0.0
        try:
            import numpy as np
        except ImportError:
            return self._score_python(seq)
        if not hasattr(self, "_np_w1"):
            self._cache_numpy()
        arr = np.asarray(seq, dtype=np.int64)
        left = arr[:-2]
        mid = arr[1:-1]
        nxt = arr[2:]
        activated = np.tanh(self._np_b1 + self._np_w1[left] + self._np_w1[26 + mid])
        logits = activated @ self._np_w2 + self._np_b2
        peak = logits.max(axis=1)
        log_partition = peak + np.log(np.exp(logits - peak[:, None]).sum(axis=1))
        return float((logits[np.arange(nxt.shape[0]), nxt] - log_partition).sum())

    def _score_python(self, seq: list[int]) -> float:
        n = len(seq)
        hidden = self.hidden
        w1 = self.W1
        b1 = self.b1
        w2 = self.W2
        b2 = self.b2
        total = 0.0
        for index in range(2, n):
            left = seq[index - 2]
            mid = seq[index - 1]
            nxt = seq[index]
            activated = [
                math.tanh(b1[j] + w1[left][j] + w1[26 + mid][j]) for j in range(hidden)
            ]
            logits = [
                b2[k] + sum(activated[j] * w2[j][k] for j in range(hidden))
                for k in range(26)
            ]
            peak = max(logits)
            log_partition = peak + math.log(sum(math.exp(value - peak) for value in logits))
            total += logits[nxt] - log_partition
        return total

    def score_text(self, text: str) -> float:
        letters = "".join(ch for ch in letters_only(text) if "A" <= ch <= "Z")
        return self.score([ord(ch) - 65 for ch in letters])


@lru_cache(maxsize=1)
def get_neural_model() -> NeuralLetterModel:
    return NeuralLetterModel(load_training_prose())
