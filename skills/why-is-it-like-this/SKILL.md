---
name: why-is-it-like-this
description: Find out why code is shaped the way it is, using git history, PRs and Jira. Use for "why was this built this way", "who changed this and why", regression history, and before removing something that looks pointless.
---

# Why is it like this

Recover intent from history, not from guessing. Read-only.
Companion to `how-does-it-work`.

## Steps

1. Pin the target: the exact lines, symbol or behaviour.
2. `git log -L`, `git log -S`, and `git blame` to find the commits that
   introduced and last reshaped it. Follow renames (`--follow`).
3. For each relevant commit, read the message and the PR
   (`gh pr view <n> --comments`). If a Jira key appears in the branch, commit
   or PR, read the ticket with the Atlassian MCP for the original problem.
4. Check whether the reason still holds: has the constraint it worked around
   gone away? Is the same thing done differently elsewhere?
5. Look for the regression point when the question is "when did this break":
   the last known good commit, and the change that broke it.

## Rules

- Quote real commits, PRs and tickets. If history is silent, say "no recorded
  reason" and give your inference labelled as inference.
- Strip private details before anything goes into public text.

## Hand back

- **Intent**: why it exists, with sources.
- **Timeline**: the few commits that matter (hash, date, one line each).
- **Still valid?** Whether the reason still applies.
- **Safe to change?** What you'd check next; point to `blast-radius` if
  the answer is "maybe".
