#!/bin/sh
# Usage: new-worktree.sh <new-branch> [base-ref]
# Creates a sibling worktree on a NEW branch, so each worktree has its own
# branch. Fails if the branch already exists. Prints the worktree path.
set -eu

branch=${1:?usage: new-worktree.sh <new-branch> [base-ref]}
base=${2:-HEAD}

git check-ref-format --branch "$branch" >/dev/null
top=$(git rev-parse --show-toplevel)
dir="$(dirname "$top")/$(basename "$top")-$(printf %s "$branch" | tr '/' '-')"

if [ -e "$dir" ]; then
  echo "already exists: $dir" >&2
  exit 1
fi

git worktree add -b "$branch" "$dir" "$base" >&2
echo "$dir"
