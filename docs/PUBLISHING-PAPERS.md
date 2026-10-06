# When a paper is ready: publishing from this repository

The owner's papers are published one way. GENChase's runbook, `docs/PUBLISHING-PAPERS.md` in
ChaseHendrick/GENChase, is the full account, and its owner's decisions apply here unchanged: the quality bar,
the statuses, plain version tags without a leading v, the all-rights-reserved manuscript with Apache 2.0
programs and data, the `Use of AI` statement at body size, sources cited for what is known of them, and arXiv
deferred until an endorsement. This note covers only what differs for a paper kept in this repository.

## The pieces

| File | What it does |
|---|---|
| `papers/papers.json` | One entry a paper: its status, its companion repository, and its archive once verified |
| `papers/<id>/` | The paper folder. `notes/` stays here; everything else goes to the companion |
| `tools/paper_sync.py` | Stages the companion: the folder, the frozen inputs its numbers program names (`companionData`), and a LICENSE, CITATION.cff and .zenodo.json written from the registry. `--check` also runs the paper's own check inside the staged copy, so the companion stands on its own |
| `tools/paper-publish.sh` | GENChase's publisher: pushes the staged tree to the companion through the `undeciphered-sync` branch, keeps direct edits made there, locks the repository, and makes a release with a branded ZIP |
| `tools/paper-pull.sh` | Brings direct edits of a companion back into `papers/<id>/` |
| `tools/paper-archive-check.py`, `tools/paper-archive-build.py`, `tools/paper-zenodo-check.py` | Copied from GENChase unchanged: the PDF-in-archive check, the branded ZIP, and the Zenodo audit |
| `.github/workflows/papers.yml` | Runs the publisher on every merge that touches a paper, monthly, and on request |
| `.github/workflows/paper-archives.yml` | Audits every registered Zenodo archive weekly |

## The D'Agapeyeff paper

The paper's numbers are written by `code/make_numbers.py` from frozen results in `engine/data/`. Its
`companion_data()` lists those files, and the companion carries them under `data/`, so
`python3 code/make_numbers.py --check` works in the companion without this repository. The search programs
stay here; each release's notes name the commit of this repository it was published from.

Its companion is `ChaseHendrick/dagapeyeff`, with Zenodo's GitHub integration switched on.

## Setup, once

1. Give this repository the `PAPERS_TOKEN` secret (Settings, Secrets and variables, Actions): a fine-grained
   token with Contents and Administration read and write on the companion repositories. GENChase's token
   works if it covers all repositories. Until the secret exists the workflow does nothing.
2. On zenodo.org, under GitHub, switch the companion on (done for `dagapeyeff`).

## Each release

1. Close every item of `papers/<id>/notes/QUALITY.md` with its evidence, and set the status to `ready` in
   `papers/papers.json`. `python3 tools/paper_sync.py --release-check <id>` must report no problems.
2. Write the release notes in `papers/<id>/RELEASES.md` under `## 1.0.0`, and merge. The workflow pushes the
   folder to the companion on that merge.
3. Actions, **publish papers**, Run workflow: the paper id, the version (`1.0.0`), the archive mode and its
   confirmation.
   - `github-import` when Zenodo's GitHub integration is on for the companion. The GitHub release itself
     makes the Zenodo version, from GitHub's source ZIP; the branded `HendrickResearch_<id>_<version>.zip`
     is attached to the release with the same files.
   - `manual-zenodo` when the integration is off, as GENChase now does: upload the branded ZIP into a new,
     unpublished version draft yourself, as GENChase's `docs/PAPER-ARCHIVE-NAMING.md` describes.
4. When Zenodo shows the version, set `codeDoi` and `archiveVersion` in the registry (and `archiveFilename`
   and `archiveManuscript` for a branded deposit), put the DOI in the README's first lines and the
   manuscript's data availability paragraph, rebuild, and merge. `paper-archives.yml` then downloads the
   archive and compares its PDF with the repository's.
