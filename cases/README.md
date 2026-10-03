# Local cipher cases

Follow [the case workflow](../docs/WORKFLOW.md) to create an intake from a UTF-8 transcription with provenance, declared assumptions, bounded hypothesis reports, and candidate comparisons. Use `python3 -m engine.case_workflow init SLUG --ciphertext-file PATH --source-url URL` from the repository root, or choose an external directory with `--root`.

Each case preserves copied source bytes and an intake hash anchor. Edit `case.json` for annotations and evidence. Confirmed training cribs and independent heldout cribs remain separate. Reports and their immutable snapshots live under the case's `runs/` directory. A case remains `unsolved` throughout this workflow.

No personal unknown ciphertext is included here. Review source permissions and privacy before adding a case to Git. Temporary test cases never become repository examples.
