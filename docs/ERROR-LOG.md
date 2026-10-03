# Error log

The append-only log is [`logs/errors.md`](logs/errors.md).

Format of each entry: **date**, **command**, **failure**, **retried**. The engine adds a row only when a demo recovery fails. It does not invent failures.
