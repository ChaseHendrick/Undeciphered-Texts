"""Residual ensemble for bounded, calibrated cipher-family ranking.

NumPy is optional for core solvers but required for this router. Fresh-key
samples, training-only statistics, a separate calibration split, and an
unchanged legacy benchmark keep family ranking distinct from decipherment.
Modern optimizer and calibration references:
https://arxiv.org/abs/1711.05101
https://proceedings.mlr.press/v70/guo17a.html
Optional frozen-teacher distillation: https://arxiv.org/abs/1503.02531
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import time
import os
import tempfile
from pathlib import Path

import numpy as np

from engine.neural_grade import (TRAIN_PATH, HELD_EN_PATH, FAMILIES, ROUTER_SEED,
    _english_unigram, _router_samples, assert_split, assert_certificate_plaintexts_excluded,
    encrypt_family, letters_az, load_training_prose, discover_solver_labels, label_is_unsolved)
from engine.neural_features import feature_tables, router_features
from engine.neural_training import classification_objective, curriculum_weights, correctness_speed_reward

DATA = Path(__file__).resolve().parent / "data"
WEIGHTS_PATH = DATA / "neural_router_v2_weights.json"
METRICS_PATH = DATA / "neural_router_v2_metrics.json"
FEATURE_VERSION = "cipher_statistics_v8"
FEATURE_WIDTHS = {f"cipher_statistics_v{version}": width for version, width in
                  ((2, 58), (3, 82), (4, 126), (5, 142), (6, 222), (7, 228), (8, 148), (9, 154), (10, 145))}
MODEL_NAME = "Bob the Neural Net"
EXTRA_FAMILIES = ("rail-fence", "affine", "autokey", "condi", "progressive-key", "redefence")


def _softmax(logits):
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    probabilities = np.exp(shifted)
    return probabilities / np.sum(probabilities, axis=1, keepdims=True)


def calibrated_probabilities(logits, temperature):
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)) or not .05 <= temperature <= 100 or not math.isfinite(temperature):
        raise ValueError("temperature must be finite and between0.05 and100")
    logits = np.asarray(logits, dtype=np.float64)
    if logits.ndim != 2 or not np.all(np.isfinite(logits)):
        raise ValueError("logits must be a finite matrix")
    # Center before division, allowing underflow to zero for extreme finite gaps.
    with np.errstate(over="ignore", under="ignore"):
        centered = logits - np.max(logits, axis=1, keepdims=True)
        return _softmax(centered / temperature)


def residual_parameters(width, hidden, classes, *, seed):
    rng = np.random.default_rng(seed)
    return {"w0": rng.normal(0, math.sqrt(2 / (width + hidden)), (width, hidden)),
            "b0": np.zeros(hidden),
            "w1": rng.normal(0, math.sqrt(1 / hidden), (hidden, hidden)),
            "b1": np.zeros(hidden),
            "w2": rng.normal(0, math.sqrt(2 / (hidden + classes)), (hidden, classes)),
            "b2": np.zeros(classes)}


def residual_gradients(parameters, x, labels, *, smoothing=.03, dropout=0., rng=None,
                       sample_weights=None, paired_rows=(), consistency_weight=0.,
                       teacher_probabilities=None, distillation_strength=0., distillation_temperature=2.):
    """Cross-entropy and exact backpropagation, before optimizer weight decay."""
    _validate_distillation(distillation_strength, distillation_temperature)
    x = np.asarray(x, dtype=np.float64)
    labels = np.asarray(labels)
    p = parameters
    h0 = np.tanh(x @ p["w0"] + p["b0"])
    mask = np.ones_like(h0) if dropout == 0 else (rng.random(h0.shape) >= dropout) / (1 - dropout)
    a0 = h0 * mask
    h1 = np.tanh(a0 @ p["w1"] + p["b1"])
    a1 = h1 + a0
    logits = a1 @ p["w2"] + p["b2"]
    loss, delta, _ = classification_objective(logits, labels, smoothing=smoothing,
        sample_weights=sample_weights, paired_rows=paired_rows, consistency_weight=consistency_weight)
    if distillation_strength:
        teacher_loss, teacher_delta = teacher_kl_objective(logits, teacher_probabilities,
            strength=distillation_strength, temperature=distillation_temperature)
        loss += teacher_loss
        delta += teacher_delta
    da1 = delta @ p["w2"].T
    dz1 = da1 * (1 - h1 * h1)
    dz0 = (da1 + dz1 @ p["w1"].T) * mask * (1 - h0 * h0)
    return loss, {"w2": a1.T @ delta, "b2": delta.sum(axis=0),
                  "w1": a0.T @ dz1, "b1": dz1.sum(axis=0),
                  "w0": x.T @ dz0, "b0": dz0.sum(axis=0)}


def network_logits(x, model):
    x = np.asarray(x, dtype=np.float64)
    normalized = (x - np.asarray(model["mean"])) / np.asarray(model["scale"])
    p = {name: np.asarray(value, dtype=np.float64) for name, value in model["parameters"].items()}
    a0 = np.tanh(normalized @ p["w0"] + p["b0"])
    a1 = np.tanh(a0 @ p["w1"] + p["b1"]) + a0
    return a1 @ p["w2"] + p["b2"]


def warm_start_model(model, mean, scale):
    """Rebase a residual model and append zero-weight inputs without changing logits.

    Old features must be the exact prefix of the new feature vector. Converting
    normalization changes only the first layer: Wnew = scaleNew / scaleOld * Wold
    and bnew = bold + (meanNew - meanOld) / scaleOld @ Wold. Extra inputs initially
    have zero weights. Optimizer state is deliberately not transferred.
    """
    try:
        if not isinstance(model, dict) or not isinstance(model["parameters"], dict):
            raise ValueError("warm start requires a residual model dictionary")
        old_mean, old_scale = np.asarray(model["mean"], dtype=float), np.asarray(model["scale"], dtype=float)
        new_mean, new_scale = np.asarray(mean, dtype=float), np.asarray(scale, dtype=float)
        if (old_mean.ndim != 1 or new_mean.ndim != 1 or old_scale.shape != old_mean.shape
                or new_scale.shape != new_mean.shape or not 1 <= len(old_mean) <= len(new_mean) <= 1024
                or any(not np.all(np.isfinite(a)) for a in (old_mean, old_scale, new_mean, new_scale))
                or np.any(old_scale <= 0) or np.any(new_scale <= 0)):
            raise ValueError("warm start needs finite equal-width means and positive scales without removing inputs")
        parameters = {name: np.asarray(value, dtype=float) for name, value in model["parameters"].items()}
        if set(parameters) != {"w0", "b0", "w1", "b1", "w2", "b2"}:
            raise ValueError("invalid warm-start residual parameters")
        if parameters["b0"].ndim != 1 or parameters["b2"].ndim != 1:
            raise ValueError("invalid warm-start residual parameters")
        hidden, classes = len(parameters["b0"]), len(parameters["b2"])
        shapes = {"w0": (len(old_mean), hidden), "b0": (hidden,), "w1": (hidden, hidden),
                  "b1": (hidden,), "w2": (hidden, classes), "b2": (classes,)}
        if (not 2 <= hidden <= 256 or not 2 <= classes <= 128
                or any(parameters[name].shape != shape or not np.all(np.isfinite(parameters[name]))
                       for name, shape in shapes.items())):
            raise ValueError("invalid warm-start residual parameters")
        converted = {name: value.copy() for name, value in parameters.items()}
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            first = np.zeros((len(new_mean), hidden))
            first[:len(old_mean)] = (new_scale[:len(old_mean)] / old_scale)[:, None] * parameters["w0"]
            converted["b0"] += ((new_mean[:len(old_mean)] - old_mean) / old_scale) @ parameters["w0"]
        converted["w0"] = first
        if any(not np.all(np.isfinite(value)) for value in converted.values()):
            raise ValueError("warm-start normalization conversion is not finite")
        return {**model, "mean": new_mean.tolist(), "scale": new_scale.tolist(),
                "parameters": {name: value.tolist() for name, value in converted.items()}}
    except (KeyError, TypeError, IndexError, OverflowError) as exc:
        raise ValueError("malformed warm-start residual model") from exc


def _nll(probabilities, labels):
    return -float(np.log(np.maximum(probabilities[np.arange(len(labels)), labels], 1e-300)).mean())


def _validate_learning_rate(learning_rate):
    if (isinstance(learning_rate, bool) or not isinstance(learning_rate, (int, float))
            or not 0 < learning_rate <= .1 or not math.isfinite(learning_rate)):
        raise ValueError("learning_rate must be finite, positive and at most0.1")


def _validate_distillation(strength, temperature):
    if (isinstance(strength, bool) or not isinstance(strength, (int, float))
            or not 0 <= strength <= 1 or not math.isfinite(strength)):
        raise ValueError("distillation_strength must be finite and between 0 and 1")
    if (isinstance(temperature, bool) or not isinstance(temperature, (int, float))
            or not .5 <= temperature <= 10 or not math.isfinite(temperature)):
        raise ValueError("distillation_temperature must be finite and between 0.5 and 10")


def teacher_kl_objective(logits, teacher_probabilities, *, strength=.1, temperature=2.):
    """Return strength*T**2*mean KL(q || softmax(logits/T)) and its logit gradient.

    Teacher targets are fixed distributions, not updated by backpropagation.
    The exact derivative is strength*T*(p*sum(q)-q)/rows. Supplied rows must
    already sum to one within roundoff; normalization removes that roundoff.
    No logarithm of a zero teacher probability is evaluated.
    """
    _validate_distillation(strength, temperature)
    try:
        student, teacher = np.asarray(logits), np.asarray(teacher_probabilities)
        if (student.ndim != 2 or not 1 <= len(student) <= 20_000
                or not 2 <= student.shape[1] <= 128 or student.dtype.kind not in "fiu"
                or teacher.shape != student.shape or teacher.dtype.kind not in "fiu"):
            raise ValueError("teacher and student must be bounded equal-shape numeric matrices")
        student, teacher = student.astype(np.float64), teacher.astype(np.float64)
        if (not np.all(np.isfinite(student)) or not np.all(np.isfinite(teacher))
                or np.any(teacher < 0) or np.any(teacher > 1)
                or not np.allclose(teacher.sum(axis=1), 1., rtol=0., atol=1e-10)):
            raise ValueError("teacher targets must be finite probability distributions and logits finite")
        if strength == 0:
            return 0., np.zeros_like(student)
        with np.errstate(over="raise", invalid="raise", divide="raise", under="ignore"):
            teacher = teacher / teacher.sum(axis=1, keepdims=True)
            shifted = (student - student.max(axis=1, keepdims=True)) / temperature
            exponentials = np.exp(shifted)
            totals = exponentials.sum(axis=1, keepdims=True)
            probabilities = exponentials / totals
            log_probabilities = shifted - np.log(totals)
            log_teacher = np.zeros_like(teacher)
            np.log(teacher, out=log_teacher, where=teacher > 0)
            loss = strength * temperature**2 * float(np.sum(teacher * (log_teacher - log_probabilities)) / len(student))
            gradient = strength * temperature * (
                probabilities * teacher.sum(axis=1, keepdims=True) - teacher) / len(student)
        if not math.isfinite(loss) or not np.all(np.isfinite(gradient)):
            raise ValueError("teacher objective exceeds representable float64 arithmetic")
        return loss, gradient
    except (TypeError, OverflowError, FloatingPointError) as exc:
        raise ValueError("teacher objective requires representable finite numeric inputs") from exc


def _frozen_teacher_probabilities(train_x, models, *, input_width, hidden, classes, temperature):
    """Evaluate frozen incumbent models on training features only, with no labels."""
    if not isinstance(models, (list, tuple)) or not 1 <= len(models) <= 5:
        raise ValueError("teacher must contain between 1 and 5 incumbent models")
    checked, width = [], None
    for model in models:
        try:
            validated = warm_start_model(model, model["mean"], model["scale"])
        except (KeyError, TypeError) as exc:
            raise ValueError("teacher requires valid incumbent residual models") from exc
        current_width = len(validated["mean"])
        if (current_width != input_width or current_width > train_x.shape[1]
                or (width is not None and current_width != width)
                or len(validated["parameters"]["b0"]) != hidden
                or len(validated["parameters"]["b2"]) != classes):
            raise ValueError("teacher must preserve incumbent input width, hidden width and output classes")
        width = current_width
        checked.append(validated)
    logits = np.mean([network_logits(train_x[:, :width], model) for model in checked], axis=0)
    if not np.all(np.isfinite(logits)):
        raise ValueError("teacher logits must remain finite")
    probabilities = calibrated_probabilities(logits, temperature)
    probabilities.setflags(write=False)
    return probabilities


def fit_residual_network(train_x, train_y, validation_x, validation_y, *, hidden=64, epochs=160, seed=20261003,
                         initial_model=None, learning_rate=.01, teacher_models=None,
                         distillation_strength=0., distillation_temperature=2., cost_sensitive=False):
    """Supervised, curriculum and paired-dropout training with validation checkpoints."""
    _validate_learning_rate(learning_rate)
    _validate_distillation(distillation_strength, distillation_temperature)
    if distillation_strength and initial_model is None:
        raise ValueError("positive distillation requires an incumbent warm start")
    x, v = np.asarray(train_x, dtype=np.float64), np.asarray(validation_x, dtype=np.float64)
    y, vy = np.asarray(train_y), np.asarray(validation_y)
    if y.ndim != 1 or vy.ndim != 1 or y.dtype.kind not in "iu" or vy.dtype.kind not in "iu":
        raise ValueError("training labels must be integer vectors")
    if x.ndim != 2 or v.ndim != 2 or x.shape[1] != v.shape[1] or not len(x) or not len(v):
        raise ValueError("training and validation must be nonempty equal-width matrices")
    if x.size + v.size > 2_000_000 or len(x) > 10_000 or x.shape[1] > 1024:
        raise ValueError("training matrices exceed bounded dimensions")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(v)) or len(y) != len(x) or len(vy) != len(v):
        raise ValueError("invalid finite features or label lengths")
    if not isinstance(epochs, int) or isinstance(epochs, bool) or not 1 <= epochs <= 1000:
        raise ValueError("epochs must be between1 and1000")
    if not isinstance(hidden, int) or isinstance(hidden, bool) or not 2 <= hidden <= 256:
        raise ValueError("hidden must be between2 and256")
    classes = int(y.max()) + 1
    if not 2 <= classes <= 128 or set(y.tolist()) != set(range(classes)) or np.any(vy < 0) or np.any(vy >= classes):
        raise ValueError("class labels must cover consecutive classes")
    mean, scale = x.mean(axis=0), x.std(axis=0) + 1e-6
    normalized = (x - mean) / scale
    initial = warm_start_model(initial_model, mean, scale) if initial_model is not None else None
    if initial is not None:
        if len(initial["parameters"]["b0"]) != hidden or len(initial["parameters"]["b2"]) != classes:
            raise ValueError("warm start must preserve hidden width and output classes")
        parameters = {name: np.asarray(value, dtype=float) for name, value in initial["parameters"].items()}
    else:
        parameters = residual_parameters(x.shape[1], hidden, classes, seed=seed)
    moments = {k: np.zeros_like(value) for k, value in parameters.items()}
    velocities = {k: np.zeros_like(value) for k, value in parameters.items()}
    rng = np.random.default_rng(seed + 1)
    best_loss, best_correct, best, best_epoch = float("inf"), -1, None, 0
    if initial is not None:
        # The incumbent is checkpoint0, so validation cannot force a worse model.
        probabilities = _softmax(network_logits(v, initial))
        best_loss = _nll(probabilities, vy)
        best_correct = int((probabilities.argmax(axis=1) == vy).sum())
        best = initial
    if not isinstance(cost_sensitive, bool):
        raise ValueError("cost_sensitive must be an explicit boolean")
    factors = np.ones(classes, dtype=float)
    if cost_sensitive:
        if initial is None:
            raise ValueError("cost-sensitive weights need the incumbent's validation errors")
        predicted = _softmax(network_logits(v, initial)).argmax(axis=1)
        for label in range(classes):
            mask = vy == label
            if not int(mask.sum()):
                raise ValueError("cost-sensitive weights need every class in validation")
            errors = 1.0 - float((predicted[mask] == label).mean())
            factors[label] = 1.0 + errors
    views = np.concatenate((normalized, normalized))
    view_labels = np.concatenate((y, y))
    pairs = [(i, i + len(x)) for i in range(len(x))]
    teacher_options = {}
    if distillation_strength:
        teacher_models = [initial_model] if teacher_models is None else teacher_models
        teacher = _frozen_teacher_probabilities(x, teacher_models, input_width=len(initial_model["mean"]), hidden=hidden,
            classes=classes, temperature=distillation_temperature)
        teacher_options = {"teacher_probabilities": np.concatenate((teacher, teacher)),
            "distillation_strength": distillation_strength, "distillation_temperature": distillation_temperature}
    for epoch in range(1, epochs + 1):
        a0 = np.tanh(normalized @ parameters["w0"] + parameters["b0"])
        clean_logits = (np.tanh(a0 @ parameters["w1"] + parameters["b1"]) + a0) @ parameters["w2"] + parameters["b2"]
        weights = curriculum_weights(y, clean_logits, epoch=epoch, total_epochs=epochs) * factors[y]
        _, gradients = residual_gradients(parameters, views, view_labels, dropout=.05, rng=rng,
            sample_weights=np.concatenate((weights, weights)), paired_rows=pairs, consistency_weight=.15,
            **teacher_options)
        rate = (learning_rate / .01) * (.001 + .009 * .5 * (1 + math.cos(math.pi * (epoch - 1) / epochs)))
        for name, parameter in parameters.items():
            moments[name] = .9 * moments[name] + .1 * gradients[name]
            velocities[name] = .999 * velocities[name] + .001 * gradients[name] ** 2
            if name.startswith("w"):
                parameter *= 1 - rate * .01
            parameter -= rate * (moments[name] / (1 - .9**epoch)) / (np.sqrt(velocities[name] / (1 - .999**epoch)) + 1e-8)
        if epoch % 5 == 0 or epoch == epochs:
            model = {"mean": mean.tolist(), "scale": scale.tolist(), "parameters": {k: value.tolist() for k, value in parameters.items()}}
            probabilities = _softmax(network_logits(v, model))
            loss = _nll(probabilities, vy)
            correct = int((probabilities.argmax(axis=1) == vy).sum())
            if (correct, -loss) > (best_correct, -best_loss):
                best_loss, best_correct, best, best_epoch = loss, correct, model, epoch
    result = {**best, "optimizer": "adamw", "hidden": hidden, "epochs": epochs,
            "checkpoint_epoch": best_epoch, "validation_nll": best_loss,
            "validation_correct": best_correct, "validation_total": len(vy),
            "checkpoint_policy": "maximize correct validation labels, then minimize NLL; earliest exact tie",
            "training_types": ["supervised_label_smoothing", "curriculum_hard_examples", "paired_dropout_consistency"],
            "consistency_weight": .15, "label_smoothing": .03, "dropout": .05, "seed": seed,
            "warm_start": initial is not None, "optimizer_state": "fresh", "learning_rate": learning_rate}
    if distillation_strength:
        result["training_types"] = result["training_types"] + ["frozen_incumbent_teacher_kl"]
        result.update(distillation_strength=distillation_strength, distillation_temperature=distillation_temperature,
            teacher_scope="generated training rows only", teacher_ensemble_size=len(teacher_models))
    return result


def cryptanalytic_features(text, tables):
    """Fitness of unknown-key trials fitted with training-only language tables.

    The 44 scalars contain no retained keys or plaintext strings. These are
    advisory family features, not independent validation of a decipherment.
    """
    from engine.solvers.rail_fence import rail_fence_decrypt
    values = np.array([ord(ch) - 65 for ch in text.upper() if "A" <= ch <= "Z"])
    if not 16 <= len(values) <= 8192:
        raise ValueError("cryptanalytic features require 16..8192 A-Z letters")
    english = np.maximum(tables["english"], 1e-300)
    logenglish, logdig = np.log(english), tables["logdig"]
    vig_log = np.array([[logenglish[(j - k) % 26] for k in range(26)] for j in range(26)])
    beau_log = np.array([[logenglish[(k - j) % 26] for k in range(26)] for j in range(26)])
    score = lambda rows: np.mean(logdig[rows[..., :-1], rows[..., 1:]], axis=-1)
    row = []
    for period in range(1, 13):
        positions = np.arange(len(values)) % period
        counts = np.bincount(positions * 26 + values, minlength=period * 26).reshape(period, 26)
        vig = (values - (counts @ vig_log).argmax(axis=1)[positions]) % 26
        beau = ((counts @ beau_log).argmax(axis=1)[positions] - values) % 26
        keys = np.arange(13)[:, None]
        letters = np.arange(26)[None, :]
        porta_map = np.where(letters >= 13, (letters - 13 - keys) % 13, 13 + (letters + keys) % 13)
        porta_keys = (counts @ logenglish[porta_map].T).argmax(axis=1)
        porta = porta_map[porta_keys[positions], values]
        row.extend(float(score(trial)) for trial in (vig, beau, porta))
    offsets = np.arange(26)[:, None]
    affine_scores = []
    for multiplier in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        trial = (pow(multiplier, -1, 26) * (values[None, :] - offsets)) % 26
        affine_scores.append(float(score(trial).max()))
    row.extend((affine_scores[0], max(affine_scores)))
    normalized = "".join(chr(65 + int(value)) for value in values)
    for rails in range(2, 8):
        recovered = rail_fence_decrypt(normalized, rails)
        trial = np.array([ord(ch) - 65 for ch in recovered])
        row.append(float(score(trial)))
    return row


def _features(text, english, tables, *, version="cipher_statistics_v2"):
    if version not in FEATURE_WIDTHS:
        raise ValueError("unsupported cipher feature version")
    row = router_features(text, english, tables)
    values = np.array([ord(ch) - 65 for ch in text.upper() if "A" <= ch <= "Z"])
    # Additional long-period IC and best Vigenere column agreement. No trial text survives.
    for period in range(9, 17):
        columns = [values[i::period] for i in range(period)]
        ics = []
        for column in columns:
            counts = np.bincount(column, minlength=26)
            n = len(column)
            ics.append(float((counts * (counts - 1)).sum() / (n * (n - 1))) if n > 1 else 0.)
        row.append(float(np.mean(ics)))
    for period in range(1, 13):
        agreements = []
        for offset in range(period):
            counts = np.bincount(values[offset::period], minlength=26).astype(float)
            agreements.append(float((counts @ tables["mvig"]).max() / (np.linalg.norm(counts) * tables["norm"] + 1e-12)))
        row.append(float(np.mean(agreements)))
    if version in tuple(f"cipher_statistics_v{i}" for i in range(3, 11)):
        for width in (2, 3, 4):
            grams = [tuple(values[i:i + width]) for i in range(len(values) - width + 1)]
            frequencies = {}
            for gram in grams:
                frequencies[gram] = frequencies.get(gram, 0) + 1
            counts = np.asarray(list(frequencies.values()), dtype=float)
            p = counts / counts.sum()
            row.extend((len(counts) / len(grams), float(-(p * np.log(p)).sum()),
                        float(p.max()), float(counts[counts > 1].sum() / len(grams))))
        row.extend(float(np.mean(values[lag:] == values[:-lag])) if len(values) > lag else 0. for lag in range(6, 18))
    if version in tuple(f"cipher_statistics_v{i}" for i in range(4, 11)):
        row.extend(cryptanalytic_features(text, tables))
    if version in ("cipher_statistics_v5", "cipher_statistics_v6", "cipher_statistics_v7", "cipher_statistics_v9",
                   "cipher_statistics_v10", FEATURE_VERSION):
        from engine.solvers.autokey_inference import autokey_feature_scores
        row.extend(autokey_feature_scores(text, tables))
    if version in ("cipher_statistics_v6", "cipher_statistics_v7"):
        row.extend(float(value) for value in np.bincount(values, minlength=26) / len(values))
        row.extend(float(np.mean(values[lag:] == values[:-lag])) if len(values) > lag else 0.
                   for lag in range(18, 70))
        for offset in (0, 1):
            pairs = values[offset:len(values) - (len(values) - offset) % 2].reshape(-1, 2)
            row.append(float(tables["logdig"][pairs[:, 0], pairs[:, 1]].mean()))
    if version in ("cipher_statistics_v7", "cipher_statistics_v9", FEATURE_VERSION):
        from engine.neural_m209_features import m209_pair_features
        row.extend(m209_pair_features(text, tables))
    if version == "cipher_statistics_v9":
        from engine.neural_features import wheel_lag_features
        row.extend(wheel_lag_features(values))
    if version == "cipher_statistics_v10":
        # The format 5 prefix, then a bounded no-plugboard Enigma trial. No setting survives.
        from engine.neural_enigma_features import enigma_features
        row.extend(enigma_features(text, tables))
    return row


def _encrypt(family, text, draw):
    if family == "condi":
        from engine.solvers.condi import condi_encrypt
        keyword = "".join(draw.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(draw.randint(4, 9)))
        return condi_encrypt(text, keyword=keyword, initial_offset=draw.randrange(26), alphabet_shift=draw.randrange(26))
    if family == "progressive-key":
        from engine.solvers.progressive_key import progressive_key_encrypt
        keyword = "".join(draw.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(draw.randint(4, 9)))
        return progressive_key_encrypt(text, keyword=keyword, progression=draw.randrange(1, 26))
    if family == "redefence":
        from engine.solvers.redefence import redefence_encrypt
        rails = draw.randint(3, 5)
        ranks = list(range(1, rails + 1))
        draw.shuffle(ranks)
        return redefence_encrypt(text, ranks, offset=draw.randrange(2 * (rails - 1)))
    if family == "rail-fence":
        from engine.solvers.rail_fence import rail_fence_encrypt
        return rail_fence_encrypt(text, draw.randint(2, 7))
    if family == "affine":
        from engine.solvers.affine import affine_encrypt
        return affine_encrypt(text, draw.choice((3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)), draw.randrange(26))
    if family == "autokey":
        from engine.solvers.autokey import autokey_encrypt
        return autokey_encrypt(text, "".join(draw.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(draw.randint(4, 9))))
    return encrypt_family(family, text, draw)


def _samples(letters, families, count, seed, english, tables, *, version=FEATURE_VERSION):
    draw = random.Random(seed)
    if len(letters) < 360:
        raise ValueError("sample prose needs at least360 letters")
    x, y = [], []
    for label, family in enumerate(families):
        for _ in range(count):
            length = draw.choice((120, 180, 240))
            start = draw.randrange(len(letters) - length + 1)
            ciphertext = _encrypt(family, letters[start:start + length], draw)
            x.append(_features(ciphertext, english, tables, version=version))
            y.append(label)
    return np.asarray(x), np.asarray(y)


def promotion_allowed(benchmark_accuracy, baseline_accuracy, overall_accuracy, previous_overall,
                      previous_benchmark=None):
    return (benchmark_accuracy + 1e-12 >= baseline_accuracy
            and (previous_benchmark is None or benchmark_accuracy + 1e-12 >= previous_benchmark)
            and (previous_overall is None or overall_accuracy + 1e-12 >= previous_overall))


def train_router(*, epochs=200, train_per_class=128, write=True, weights_path=WEIGHTS_PATH,
                 expanded_families=False, hidden=64, ensemble_size=3, warm_start=False, learning_rate=.01,
                 distillation_strength=0., distillation_temperature=2., feature_version=None,
                 more_prose=False, cost_sensitive=False):
    """One local pass. Hyperparameters and calibration never use Doyle scores."""
    started = time.perf_counter()
    _validate_learning_rate(learning_rate)
    _validate_distillation(distillation_strength, distillation_temperature)
    version = FEATURE_VERSION if feature_version is None else feature_version
    if version not in FEATURE_WIDTHS:
        raise ValueError("feature_version must be a known cipher statistics version")
    if not isinstance(warm_start, bool):
        raise ValueError("warm_start must be an explicit boolean")
    if distillation_strength and not warm_start:
        raise ValueError("positive distillation requires warm_start=True")
    if not isinstance(epochs, int) or isinstance(epochs, bool) or not 1 <= epochs <= 1000:
        raise ValueError("epochs must be between 1 and 1000")
    if not isinstance(hidden, int) or isinstance(hidden, bool) or not 2 <= hidden <= 256:
        raise ValueError("hidden must be between 2 and 256")
    if not isinstance(ensemble_size, int) or isinstance(ensemble_size, bool) or not 1 <= ensemble_size <= 5:
        raise ValueError("ensemble_size must be between 1 and 5")
    if not isinstance(train_per_class, int) or isinstance(train_per_class, bool) or not 8 <= train_per_class <= 256:
        raise ValueError("train_per_class must be between8 and256")
    if not isinstance(cost_sensitive, bool):
        raise ValueError("cost_sensitive must be an explicit boolean")
    if cost_sensitive and not warm_start:
        raise ValueError("cost-sensitive weights require warm_start=True")
    if not isinstance(more_prose, bool):
        raise ValueError("more_prose must be an explicit boolean")
    full = letters_az(load_training_prose(TRAIN_PATH))
    if more_prose:
        extra_path = DATA / "neural_train_public.txt"
        extra = letters_az(extra_path.read_text(encoding="utf-8"))
        if len(extra) < 10000:
            raise ValueError("the extra training prose is too short")
        full += extra
    held = letters_az(load_training_prose(HELD_EN_PATH))
    cut, calibration_cut = int(len(full) * .6), int(len(full) * .8)
    training, validation, calibration = full[:cut], full[cut:calibration_cut], full[calibration_cut:]
    for left, right in ((training, validation), (training, calibration), (validation, calibration), (full, held)):
        assert_split(left, right)
    assert_certificate_plaintexts_excluded(full, held)
    if more_prose:
        wells = letters_az((DATA / "neural_audit_wells.txt").read_text(encoding="utf-8"))
        grimm = letters_az((DATA / "neural_heldout_grimm_wolf.txt").read_text(encoding="utf-8"))
        assert_split(full, wells)
        assert_split(full, grimm)
    english = _english_unigram(training)
    tables = feature_tables(training, english)
    certified = set(discover_solver_labels())
    extra = EXTRA_FAMILIES if expanded_families else EXTRA_FAMILIES[:3]
    families = [name for name in (*FAMILIES, *extra) if name in certified]
    destination = Path(weights_path)
    incumbent_bytes = None
    if distillation_strength and destination.is_file():
        if destination.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("incumbent artifact exceeds the 4 MiB bound")
        incumbent_bytes = destination.read_bytes()
    previous = load_router(destination) if destination.is_file() else None
    teacher_sha256 = None
    if incumbent_bytes is not None:
        if destination.read_bytes() != incumbent_bytes:
            raise ValueError("incumbent changed while loading the frozen teacher")
        teacher_sha256 = hashlib.sha256(incumbent_bytes).hexdigest()
    if previous is not None and previous["families"] != families[:len(previous["families"])]:
        raise ValueError("incumbent families must be a prefix of candidate families; use matching expanded settings or a separate artifact path")
    if warm_start:
        if previous is None:
            raise ValueError("warm start requires an existing incumbent artifact")
        if previous["families"] != families:
            raise ValueError("warm start must preserve the exact family list and order")
        if previous["training_letters"] != training:
            raise ValueError("warm start must preserve training-only language tables; use a cold fit for changed training prose")
        if previous["feature_version"] not in ("cipher_statistics_v2", "cipher_statistics_v3",
                                               "cipher_statistics_v4", "cipher_statistics_v5",
                                               "cipher_statistics_v9", "cipher_statistics_v10", FEATURE_VERSION):
            raise ValueError("warm start requires prefix-compatible features; V6/V7 replay is supported but their inputs cannot be discarded")
        if len(previous["models"]) != ensemble_size:
            raise ValueError("warm start must preserve ensemble size")
        if any(len(model["parameters"]["b0"]) != hidden for model in previous["models"]):
            raise ValueError("warm start must preserve hidden width")
    x, y = _samples(training, families, train_per_class, ROUTER_SEED, english, tables, version=version)
    vx, vy = _samples(validation, families, 24, ROUTER_SEED + 101, english, tables, version=version)
    teacher_options = {}
    if distillation_strength:
        teacher_options = {"teacher_models": previous["models"], "distillation_strength": distillation_strength,
            "distillation_temperature": distillation_temperature}
    models = [fit_residual_network(x, y, vx, vy, hidden=hidden, epochs=epochs, seed=ROUTER_SEED + i * 997,
                                  initial_model=previous["models"][i] if warm_start else None,
                                  learning_rate=learning_rate, cost_sensitive=cost_sensitive, **teacher_options)
              for i in range(ensemble_size)]
    cx, cy = _samples(calibration, families, 24, ROUTER_SEED + 303, english, tables, version=version)
    c_logits = np.mean([network_logits(cx, model) for model in models], axis=0)
    temperature = min((.75, 1., 1.25, 1.5, 2., 3.), key=lambda t: _nll(calibrated_probabilities(c_logits, t), cy))
    hx, hy = _samples(held, families, 24, ROUTER_SEED + 202, english, tables, version=version)
    h_logits = np.mean([network_logits(hx, model) for model in models], axis=0)
    probs = calibrated_probabilities(h_logits, temperature)
    correct = int((probs.argmax(axis=1) == hy).sum())
    per_family = {name: {"correct": int((probs[hy == i].argmax(axis=1) == i).sum()), "total": int((hy == i).sum())} for i, name in enumerate(families)}
    # Replay exactly the fixed original17-family,204-example benchmark, with each model's own training tables.
    original_english = _english_unigram(full)
    original_tables = feature_tables(full, original_english)
    benchmark_x, benchmark_y = _router_samples(held, original_english, 12, ROUTER_SEED + 1, FAMILIES, original_tables)
    old = json.loads((DATA / "neural_router_weights.json").read_text())
    z = (np.asarray(benchmark_x) - np.asarray(old["mean"])) / np.asarray(old["scale"])
    old_logits = np.tanh(z @ np.asarray(old["w1"]) + np.asarray(old["b1"])) @ np.asarray(old["w2"]) + np.asarray(old["b2"])
    baseline_correct = sum(old["families"][int(index)] == FAMILIES[label] for index, label in zip(old_logits.argmax(axis=1), benchmark_y))
    draw = random.Random(ROUTER_SEED + 1)
    windows = [held[i:i + 180] for i in range(0, len(held) - 179, 180)]
    candidate_x, benchmark_ciphertexts = [], []
    for label, family in enumerate(FAMILIES):
        for sample in range(12):
            window = windows[(sample * 5 + label * 2) % len(windows)]
            offset = (sample * 17) % 40
            ciphertext = encrypt_family(family, window[offset:] + window[:offset], draw)
            benchmark_ciphertexts.append(ciphertext)
            candidate_x.append(_features(ciphertext, english, tables, version=version))
    candidate_logits = np.mean([network_logits(candidate_x, model) for model in models], axis=0)
    benchmark_correct = sum(families[int(index)] == FAMILIES[label] for index, label in zip(candidate_logits.argmax(axis=1), benchmark_y))
    previous_overall = previous.get("heldout_accuracy") if previous is not None and previous["families"] == families else None
    predecessor_comparison = None
    predecessor_ok = True
    previous_benchmark = None
    if previous is not None:
        previous_english = _english_unigram(previous["training_letters"])
        previous_tables = feature_tables(previous["training_letters"], previous_english)
        px, py = _samples(held, previous["families"], 24, ROUTER_SEED + 202,
                          previous_english, previous_tables, version=previous["feature_version"])
        predecessor_logits = np.mean([network_logits(px, model) for model in previous["models"]], axis=0)
        before = int((predecessor_logits.argmax(axis=1) == py).sum())
        previous_benchmark_x = [_features(ct, previous_english, previous_tables, version=previous["feature_version"])
                                for ct in benchmark_ciphertexts]
        previous_benchmark_logits = np.mean([network_logits(previous_benchmark_x, model) for model in previous["models"]], axis=0)
        before_benchmark = sum(previous["families"][int(index)] == FAMILIES[label]
            for index, label in zip(previous_benchmark_logits.argmax(axis=1), benchmark_y))
        previous_benchmark = before_benchmark / len(benchmark_y)
        # Appended families preserve RNG order and the identical earlier-family test ciphertexts.
        after = int((probs[:len(py)].argmax(axis=1) == py).sum())
        predecessor_comparison = {"correct_before": before, "correct_after": after, "total": len(py),
                                  "families_before": previous["families"], "families_after": families,
                                  "output_class_counts": [len(previous["families"]), len(families)]}
        predecessor_comparison.update(benchmark_correct_before=before_benchmark,
            benchmark_correct_after=benchmark_correct, benchmark_total=len(benchmark_y))
        predecessor_ok = after >= before
    accuracy = correct / len(hy)
    promoted = predecessor_ok and promotion_allowed(benchmark_correct / len(benchmark_y), baseline_correct / len(benchmark_y), accuracy, previous_overall, previous_benchmark)
    payload = {"format_version": int(version.removeprefix("cipher_statistics_v")), "feature_version": version, "families": families,
               "models": models, "mean": models[0]["mean"], "scale": models[0]["scale"],
               "temperature": temperature, "heldout_accuracy": accuracy,
               "training_letters": training, "train_sha256": hashlib.sha256(training.encode()).hexdigest(),
               "validation_sha256": hashlib.sha256(validation.encode()).hexdigest(),
               "calibration_sha256": hashlib.sha256(calibration.encode()).hexdigest(),
               "heldout_sha256": hashlib.sha256(held.encode()).hexdigest(),
               "note": "Family ranking only; no plaintext claim. Disjoint Austen slices train, select checkpoints and calibrate. Reused Doyle comparisons are development benchmarks."}
    metrics = {"model_name": MODEL_NAME, "format_version": payload["format_version"], "feature_version": version,
               "warm_start": warm_start, "learning_rate": learning_rate,
               "checkpoint_epochs": [model.get("checkpoint_epoch") for model in models],
               "families": families, "correct": correct, "total": len(hy),
               "accuracy": accuracy, "top3_correct": int(np.any(np.argsort(probs, axis=1)[:, -3:] == hy[:, None], axis=1).sum()),
               "per_family": per_family, "temperature": temperature, "calibration_nll": _nll(calibrated_probabilities(c_logits, temperature), cy),
               "heldout_nll": _nll(probs, hy), "benchmark_correct": benchmark_correct,
               "baseline_correct": baseline_correct, "benchmark_total": len(benchmark_y),
               "promoted": promoted, "predecessor_comparison": predecessor_comparison, "train_per_class": train_per_class, "epochs": epochs,
               "hidden":hidden, "ensemble_size":ensemble_size, "more_prose": more_prose,
               "cost_sensitive": cost_sensitive,
               "calibration_sha256": payload["calibration_sha256"],
               "train_sha256": payload["train_sha256"], "validation_sha256": payload["validation_sha256"], "heldout_sha256": payload["heldout_sha256"]}
    metrics["training_types"] = models[0]["training_types"]
    if distillation_strength:
        teacher_record = {"strength": distillation_strength, "temperature": distillation_temperature,
            "source_model_sha256": teacher_sha256,
            "feature_version": previous["feature_version"], "ensemble_size": len(previous["models"]),
            "scope": "generated training rows only", "objective": "T^2 KL(teacher || student)",
            "teacher": "frozen mean-logit incumbent ensemble", "synthetic_labels": "retained at full supervised weight"}
        payload["distillation"] = teacher_record
        metrics["distillation"] = teacher_record
    metrics["elapsed_seconds"] = time.perf_counter() - started
    metrics["reward"] = float(np.mean([correctness_speed_reward(bool(ok), metrics["elapsed_seconds"] / len(hy))
        for ok in (probs.argmax(axis=1) == hy)]))
    metrics["reward_scope"] = "Synthetic family-label ground truth only; wrong labels receive -1 regardless of speed. Reward never overrides promotion."
    metrics["model_policy"] = {"status": "promoted" if promoted else "rejected",
        "action": "replace incumbent" if promoted else "retain incumbent; candidate gets the axe",
        "criterion": "zero additional errors on both fixed benchmarks; speed cannot compensate for incorrect labels"}
    artifact = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode() + b"\n"
    metrics["artifact_bytes"] = len(artifact)
    metrics["model_sha256"] = hashlib.sha256(artifact).hexdigest()
    if len(artifact) > 4 * 1024 * 1024:
        metrics["promoted"] = False
        metrics["model_policy"].update(status="rejected", action="retain incumbent; candidate exceeds artifact size bound")
    if write and metrics["promoted"]:
        if distillation_strength and hashlib.sha256(destination.read_bytes()).hexdigest() != teacher_sha256:
            raise ValueError("incumbent changed during training; refusing to replace a newer artifact")
        _atomic_json(destination, payload, compact=True)
        metrics_stem = (destination.stem.replace("weights", "metrics")
                        if "weights" in destination.stem else destination.stem + ".metrics")
        _atomic_json(destination.with_name(metrics_stem + ".json"), metrics)
    return metrics


def _atomic_json(path, payload, *, compact=False):
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            json.dump(payload, temporary, indent=None if compact else 2,
                      separators=(",", ":") if compact else None, allow_nan=False)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise
    try:
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


def evaluate_router(corpus, *, samples_per_class=24, seed=20262003, weights_path=None):
    """Evaluate new ciphertexts on a separate declared ASCII prose corpus.

    No weights, checkpoints or calibration values are changed. All sliding
    48-letter overlaps with Austen and development Doyle are rejected.
    """
    if not isinstance(corpus, str) or not 1000 <= len(corpus) <= 100000 or any(ch.isalpha() and not ch.isascii() for ch in corpus):
        raise ValueError("audit corpus requires 1000..100000 ASCII prose characters")
    if not isinstance(samples_per_class, int) or isinstance(samples_per_class, bool) or not 1 <= samples_per_class <= 64:
        raise ValueError("samples_per_class must be between 1 and 64")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be a 32-bit nonnegative integer")
    letters = letters_az(corpus)
    if len(letters) < 1000:
        raise ValueError("audit corpus needs at least 1000 letters")
    for path in (TRAIN_PATH, HELD_EN_PATH):
        earlier = letters_az(load_training_prose(path))
        windows = {earlier[i:i + 48] for i in range(len(earlier) - 47)}
        if any(letters[i:i + 48] in windows for i in range(len(letters) - 47)):
            raise ValueError("audit corpus overlaps training, selection, calibration or development prose")
    assert_certificate_plaintexts_excluded(letters)
    destination = WEIGHTS_PATH if weights_path is None else Path(weights_path)
    p = load_router(destination)
    english = _english_unigram(p["training_letters"])
    tables = feature_tables(p["training_letters"], english)
    started = time.perf_counter()
    x, labels = _samples(letters, p["families"], samples_per_class, seed, english, tables,
                         version=p["feature_version"])
    logits = np.mean([network_logits(x, model) for model in p["models"]], axis=0)
    probabilities = calibrated_probabilities(logits, p["temperature"])
    correct = probabilities.argmax(axis=1) == labels
    return {"kind":"independent_corpus_family_audit", "model_name":MODEL_NAME, "claimed_plaintext":None,
            "correct":int(correct.sum()), "total":len(labels), "accuracy":float(correct.mean()),
            "top3_correct":int(np.any(np.argsort(probabilities, axis=1)[:, -3:] == labels[:, None],axis=1).sum()),
            "nll":_nll(probabilities, labels), "seed":seed, "samples_per_class":samples_per_class,
            "corpus_sha256":hashlib.sha256(letters.encode()).hexdigest(),
            "model_sha256":hashlib.sha256(destination.read_bytes()).hexdigest(),
            "elapsed_seconds":time.perf_counter() - started,
            "per_family":{name:{"correct":int(correct[labels == i].sum()), "total":int((labels == i).sum())}
                          for i,name in enumerate(p["families"])},
            "scope":"One fixed model on previously unused prose and fresh synthetic keys; conditional on the disclosed family generators."}


def load_router(path=None):
    destination = WEIGHTS_PATH if path is None else Path(path)
    if destination.stat().st_size > 4 * 1024 * 1024:
        raise ValueError("router artifact exceeds 4 MiB")
    p = json.loads(destination.read_text())
    try:
        families = p["families"]
        widths = {(version, f"cipher_statistics_v{version}"): width for version, width in
                  ((2, 58), (3, 82), (4, 126), (5, 142), (6, 222), (7, 228), (8, 148), (9, 154), (10, 145))}
        width = widths.get((p["format_version"], p["feature_version"]))
        if width is None or not isinstance(families, list) or not 2 <= len(families) <= 128 or any(not isinstance(f, str) for f in families):
            raise ValueError("unsupported router format")
        if len(set(families)) != len(families) or any(not isinstance(f, str) or label_is_unsolved(f) or f not in set(FAMILIES) | set(EXTRA_FAMILIES) for f in families):
            raise ValueError("router contains unsupported family")
        calibrated_probabilities(np.zeros((1, len(families))), p["temperature"])
        if not isinstance(p["models"], list) or not 1 <= len(p["models"]) <= 5 or any(not isinstance(model, dict) for model in p["models"]):
            raise ValueError("invalid ensemble size")
        for model in p["models"]:
            mean, scale = np.asarray(model["mean"]), np.asarray(model["scale"])
            if mean.shape != (width,) or scale.shape != mean.shape or not np.all(np.isfinite(mean)) or not np.all(np.isfinite(scale)) or np.any(scale <= 0):
                raise ValueError("invalid feature normalization")
            if not isinstance(model["parameters"], dict):
                raise ValueError("invalid residual parameters")
            params = {k: np.asarray(v, dtype=float) for k, v in model["parameters"].items()}
            hidden = len(params["b0"])
            shapes = {"w0": (width, hidden), "b0": (hidden,), "w1": (hidden, hidden), "b1": (hidden,), "w2": (hidden, len(families)), "b2": (len(families),)}
            if not 2 <= hidden <= 256 or set(params) != set(shapes) or any(params[k].shape != shape or not np.all(np.isfinite(params[k])) for k, shape in shapes.items()):
                raise ValueError("invalid residual parameters")
        if p["mean"] != p["models"][0]["mean"] or p["scale"] != p["models"][0]["scale"]:
            raise ValueError("inconsistent feature normalization")
        training = p["training_letters"]
        if not isinstance(training, str) or not 360 <= len(training) <= 2_000_000 or any(not "A" <= ch <= "Z" for ch in training) or hashlib.sha256(training.encode()).hexdigest() != p["train_sha256"]:
            raise ValueError("invalid training provenance")
        if not isinstance(p["heldout_accuracy"], (int, float)) or isinstance(p["heldout_accuracy"], bool) or not 0 <= p["heldout_accuracy"] <= 1 or not math.isfinite(p["heldout_accuracy"]):
            raise ValueError("invalid heldout accuracy")
    except (KeyError, TypeError, IndexError, OverflowError) as exc:
        raise ValueError("malformed router artifact") from exc
    return p


def route_probabilities(text, *, weights_path=None):
    """Rank all trained families; score is an estimate conditional on this corpus."""
    if not isinstance(text, str):
        raise TypeError("ciphertext must be text")
    if len(text) > 8192 or sum(ch.isascii() and ch.isalpha() for ch in text) < 16 or any(ch.isalpha() and not ch.isascii() for ch in text):
        raise ValueError("router requires16 or more A-Z letters and at most8192 characters")
    p = load_router(weights_path)
    english = _english_unigram(p["training_letters"])
    tables = feature_tables(p["training_letters"], english)
    x = [_features(text.upper(), english, tables, version=p["feature_version"])]
    logits = np.mean([network_logits(x, model) for model in p["models"]], axis=0)
    probabilities = calibrated_probabilities(logits, p["temperature"])[0]
    candidates = sorted(({"family": family, "probability": float(probabilities[i])} for i, family in enumerate(p["families"])), key=lambda c: (-c["probability"], c["family"]))
    return {"kind": "family_ranking", "model_name": MODEL_NAME, "claimed_plaintext": None, "candidates": candidates,
            "uncertain": candidates[0]["probability"] < .5 or candidates[0]["probability"] - candidates[1]["probability"] < .15,
            "uncertainty_policy": "fixed probability and margin heuristics, not an OOD detector",
            "model_sha256": hashlib.sha256((WEIGHTS_PATH if weights_path is None else Path(weights_path)).read_bytes()).hexdigest(),
            "scope": "Ranks trained known cipher families only. A family probability does not validate a plaintext."}
