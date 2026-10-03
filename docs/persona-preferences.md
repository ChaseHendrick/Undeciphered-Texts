# Persona preferences among candidates

Three small solvers each see two candidate sentences and keep the one that
matches a fixed word list. The kept sentence is a sentence written for this
repository. The other sentence is a plain alternative that does not use those
words.

These are preferences among candidates, not decipherments of Nr. 86, K4, or an
unknown script. Nothing here reads an unread historical text.

| Persona | Word list | Module |
| --- | --- | --- |
| Hallucinogens | color, dream, melting | `engine/solvers/persona_hallucinogens.py` |
| Inheritance | fortune, heir, estate | `engine/solvers/persona_inheritance.py` |
| Court notice | empire, decree, throne | `engine/solvers/persona_court_notice.py` |

Inheritance is the same preference once called a dying aristocrat, said in
plain voice. Court notice is the same preference once called a world emperor,
said in plain voice. Hallucinogens keeps that spelling.

Each certificate under `engine/data/persona_*_certificate.json` stores the
chosen sentence and the SHA-256 of that sentence. `tests/test_persona_preferences.py`
checks that the solver picks the certificate sentence over a plain alternative
and that the hash matches.
