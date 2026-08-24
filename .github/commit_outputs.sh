#!/usr/bin/env bash
# Commit step for releases.yml and facilities.yml. Replaces the `git add -A`
# block in BOTH; they must match, because the bug is a collision between them.
#
# ---------------------------------------------------------------------------
# WHAT WENT WRONG ON 2026-08-24
#
# facilities checked out main at 05:56 and ran for 55 minutes. harvest ran
# 06:23-06:33 and pushed 1507cc5. At 06:52 facilities' push was rejected, and
# the rebuild did what it was written to do:
#
#     git fetch origin main
#     git reset --mixed origin/main
#     git add -A --ignore-errors harvest/ projects.json projects.json.gz ...
#
# reset --mixed moves the branch pointer and leaves the working tree alone.
# That is correct and deliberate - it is what lets a generated file be
# re-committed on top of whatever arrived. But it means the index now describes
# harvest's commit while the working tree is from 05:56, and `git add -A` reads
# every difference between them as this job's change:
#
#   - harvest/ogtr_trials.json existed on origin and NOT on this disk, because
#     harvest created it after this job's checkout. -A staged that as a
#     deletion. The commit carries `delete mode 100644 harvest/ogtr_trials.json`.
#   - bch_organisms, cfia_records, consultations, industry_points,
#     ippc_contacts, isaaa_approvals, latam_approvals, open_registers,
#     resources, treaties.geojson, trials.geojson and projects.json.gz all
#     showed as M: this job's 05:56 copies staged over harvest's 06:33 ones.
#
# So it was not only OGTR. harvest's entire run was reverted, and its 34 trial
# records left projects.json.gz - 43730 release records became 43695, which is
# those 34 plus one OSM row, exactly.
#
# `git add -A` cannot tell "I deleted this" from "somebody else added this".
# Nothing about the pathspec list fixes that; the failure is in -A.
#
# THE FIX: stage what this run actually wrote, found by modification time
# against a stamp taken at the start of the step. A file another job added is
# not newer than the stamp, so it is never staged - not as a modification, not
# as a deletion. New harvesters are picked up without editing a list, which the
# explicit-list version of this could not do.
# ---------------------------------------------------------------------------

set -e

JOB="${1:?usage: commit_outputs.sh <job-name>}"   # "releases" or "facilities"
STAMP="${RUNNER_TEMP:-/tmp}/step-start"

# Call ONCE, immediately before the harvesters run:
#     bash .github/commit_outputs.sh --stamp
if [ "$JOB" = "--stamp" ]; then
  touch "$STAMP"
  echo "stamped $STAMP"
  exit 0
fi

if [ ! -e "$STAMP" ]; then
  echo "!! no start stamp - run 'commit_outputs.sh --stamp' before the"
  echo "   harvesters. Refusing to stage: without it this step cannot tell"
  echo "   this run's output from another job's, which is the bug it exists"
  echo "   to prevent."
  exit 1
fi

git config user.name  "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

stage_outputs() {
  # Written or rewritten since the stamp, excluding source and git internals.
  # -newer, not -mmin: a step that runs for 55 minutes cannot use a fixed
  # window, and india_nartsr alone is allowed 30.
  local n=0
  while IFS= read -r f; do
    case "$f" in
      *.py|*.sh|*.yml|*.yaml|./.git/*) continue ;;
    esac
    [ -f "$f" ] || continue
    if git check-ignore -q "$f"; then
      echo "    !! ${f#./} IS GITIGNORED - written but never committed"
      continue
    fi
    git add "${f#./}"
    n=$((n + 1))
  done < <(find ./harvest ./overlays . -maxdepth 3 -type f -newer "$STAMP" \
             -not -path './.git/*' 2>/dev/null | sort -u)
  echo "  staged $n file(s) written by this run"
}

stage_outputs
echo "staged this run:"
git diff --cached --name-only | sed 's/^/    /'

# A run that harvested nothing is a real outcome, not a failure.
if git diff --cached --quiet; then
  echo "nothing changed"
  exit 0
fi

git commit -m "$JOB: refresh $(date -u +%Y-%m-%d)"

for i in 1 2 3 4 5; do
  git push && exit 0
  echo "push rejected; rebuilding the commit on top of origin (attempt $i)"
  # Rebasing cannot work here. Every file these jobs write is a generated
  # artefact and projects.json.gz is a BINARY one - git has no way to merge two
  # gzips and stops with a conflict it cannot be taught to resolve. A whole
  # successful run was lost to that once. For generated files the newest run is
  # right, so the commit is rebuilt on top of whatever arrived.
  git fetch origin main || true
  git reset --mixed origin/main
  # And THIS is why the re-add is the same mtime-filtered function rather than
  # `git add -A`: after the reset the working tree is older than origin for
  # every file another job just wrote.
  stage_outputs
  if git diff --cached --quiet; then
    echo "nothing left to commit after fetching"
    exit 0
  fi
  git commit -m "$JOB: refresh $(date -u +%Y-%m-%d)"
  sleep 5
done

echo "push failed after 5 attempts"
exit 1

# ---------------------------------------------------------------------------
# ALSO ADD, at the top level of BOTH workflow files, so the collision cannot
# start in the first place. The mtime fix makes an overlap survivable; this
# makes it rare, and the two are worth having together because a manual
# workflow_dispatch can collide with a schedule at any time.
#
#     concurrency:
#       group: gmo-map-commit
#       cancel-in-progress: false
#
# One shared group name across both files. cancel-in-progress MUST be false -
# true would kill a 55-minute facilities run partway through.
#
# And in each job, before the harvesters:
#
#     - name: mark step start
#       run: bash .github/commit_outputs.sh --stamp
#
# and in place of the old commit block:
#
#     - name: commit
#       run: bash .github/commit_outputs.sh facilities   # or: releases
# ---------------------------------------------------------------------------
