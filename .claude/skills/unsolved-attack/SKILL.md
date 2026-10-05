---
name: unsolved-attack
description: >
  Solve a ciphertext someone brings by running this repo's solvers.
  Use when the user pastes a cipher, a crib, or a key and wants it read.
  Do not use it to declare a catalogued unread cipher solved, and do not
  invent a plaintext the solvers did not return.
---

# Solve someone's cipher

Run this from the repository root. The ciphertext is the text the user just gave you. Do not replace it with D'Agapeyeff, K4, or any sample in the repo.

## Run the solvers

Keep their letters, digits, and spaces as they wrote them. Then:

```sh
python3 -m engine analyze -- "THEIR CIPHERTEXT"
python3 -m engine route -- "THEIR CIPHERTEXT"
python3 -m engine solve caesar -- "THEIR CIPHERTEXT"
python3 -m engine solve vigenere -- "THEIR CIPHERTEXT"
python3 -m engine solve substitution -- "THEIR CIPHERTEXT"
```

`route` and the letter solvers expect A-Z text. If the text is not letters, skip those and use `python3 -m engine tools` to find a tool whose input matches. Run it with `python3 -m engine run TOOL TEXT --params '{}'`. The parameter object has to be the one `tools` lists. Do not invent parameter names.

If they know a stretch of plaintext, fit it. The offset is the zero-based position in the A-Z letters:

```sh
python3 -m engine reverse-engineer -- "THEIR CIPHERTEXT" --crib 0:KNOWN
python3 -m engine investigate -- "THEIR CIPHERTEXT" --crib 0:KNOWN
```

If they already know the method and the key, use that tool's supplied-key command and say the key was given. `solve keyed-vigenere` needs `--key` and `--alphabet`.

`run` accepts at most 8,192 characters of text. A longer message has to be split only if they say the parts are separate. Do not drop letters to make it fit.

## What counts as solved

Report a plaintext only when a command printed it. Name the command, the method, and the key or period it printed. If the tool also printed a check that the plaintext encrypts back to their ciphertext, say that. If it did not check, say the solver returned the text and it has not been re-encrypted here.

If every command fails to recover readable text, say the solvers did not recover it. Do not invent a plaintext the solvers did not return. Do not write a guessed reading. Do not fill unknown letters with a story.

## What this is not

A catalogued unread cipher is not someone's message. D'Agapeyeff, K4, and the other targets in `docs/CATALOG.md` stay unsolved unless a solver returns a plaintext that checks. Do not paste those ciphertexts into this procedure and call the result a solution.

The rules in `docs/AI-AGENTS.md` still apply. An unknown-key search has to recover a fixture without being handed the key. A known-key helper has to say the key was supplied.
