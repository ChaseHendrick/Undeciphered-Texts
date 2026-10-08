#!/bin/sh
# Brings edits made directly in a paper's companion repository back into papers/<id>/, so this
# repository's copy matches the public one. Run it after you edit the companion on GitHub, and when
# the publish papers workflow reports a conflict.
#
#   sh tools/paper-pull.sh dagapeyeff-exclusions
#
# Every file on the companion's main branch, the record, is copied into papers/<id>/, except LICENSE,
# CITATION.cff and .zenodo.json, which the workflow writes from papers/papers.json, and data/, which
# it copies from engine/data. notes/ and
# submission/ are never touched. A file that exists here but no longer in the companion is listed,
# not deleted. Then review with git diff, run python3 tools/paper_sync.py --check <id>, and commit.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
ID=${1:?usage: sh tools/paper-pull.sh <paper-id>}
REMOTE=${PAPERS_REMOTE:-https://github.com}
repo=$(python3 "$ROOT/tools/paper_sync.py" --companion "$ID")
DEST="$ROOT/papers/$ID"
[ -d "$DEST" ] || { echo "No folder papers/$ID"; exit 2; }
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
git clone -q --depth 1 --branch main "$REMOTE/$repo.git" "$tmp/c" || { echo "Cannot clone $repo."; exit 1; }
(cd "$tmp/c" && git ls-files) > "$tmp/files"
n=0
while IFS= read -r f; do
  case "$f" in LICENSE|CITATION.cff|.zenodo.json|data/*|notes/*|submission/*) continue ;; esac
  if ! cmp -s "$tmp/c/$f" "$DEST/$f" 2>/dev/null; then
    mkdir -p "$DEST/$(dirname "$f")"
    cp "$tmp/c/$f" "$DEST/$f"
    echo "updated papers/$ID/$f"
    n=$((n + 1))
  fi
done < "$tmp/files"
git -C "$ROOT" ls-files -- "papers/$ID" | sed "s#^papers/$ID/##" | while IFS= read -r f; do
  case "$f" in notes/*|submission/*) continue ;; esac
  grep -qxF "$f" "$tmp/files" || echo "only here, not in the companion: papers/$ID/$f (delete it if that removal was intended)"
done
echo "$n file(s) brought in from $repo. Review with git diff, then run python3 tools/paper_sync.py --check $ID."
