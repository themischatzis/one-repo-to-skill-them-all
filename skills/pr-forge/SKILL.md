---
name: pr-forge
description: Turn finished work into small ordered commits and a ready PR with a briefing body, using Themis's naming conventions. Use for "open a PR", "commit this", "write the PR description", or at build hand-off.
---

# PR forge

Hand-off step for every build skill. Commits, pushes and PRs are ask-first
(`ground-rules` Autonomy). Once he says go, do the whole thing.

## Git conventions

Check the repo's `CONTRIBUTING`/PR template and recent branches and commits
before naming anything. If unsure, ask. Personal rule wins over repo docs when
both apply; mention the conflict.

- Work repo with a ticket: use the ticket's own key. WWP is the usual prefix,
  but if the ticket has another prefix (e.g. ABC), use that. Branch
  `type/key-nnnn-slug` (key lowercase); commit and PR title
  `type(KEY-NNNN): Capital first letter` (key uppercase), even when repo
  history is lowercase. Work repo but no ticket: use `WWP-0000`.
- Personal repo (no ticket, no key): branch `type/what-i-am-doing`; commit and
  PR title `type: Capital first letter`.
- If SSH push fails, push once over HTTPS with `gh auth git-credential`
  (`-c credential.helper=...`); change no git config.

## Steps

1. **Branch** per the conventions. A separate worktree is fine for parallel
   work; otherwise stay put.
2. **Clean the diff**: no debug leftovers, no narrating comments (run the
   `gollum` agent if the diff is comment-heavy), no unrelated changes.
3. **Commits**: small, ordered, each landable and telling the story. Amend a
   fix into the commit it belongs to; new commit when separable. Bodies do not
   restate the subject. No Co-authored-by trailer.
4. **Push**, with the SSH fallback above if needed.
5. **PR**: ready, not draft, unless he asks. Prefer several small PRs over one
   large one; a stack only when changes truly depend on each other. Use the
   repo's template if it has one, else the body below.
6. Pass the title and body through `unslop` before posting.

## Body

A one-minute briefing for a reviewer who has the diff. Short plain sentences,
`##` headings, drop a section with nothing to say.

- `## Why`: the problem and approach, 1-3 sentences.
- `## What changed`: 1-3 bullets; name a symbol only when it carries the change.
- `## Scope`: what it covers and deliberately leaves out.
- `## Tradeoffs`: only rejected alternatives a reviewer would ask about.
- `## Blast radius`: who or what it touches and why that is safe or risky
  (`what-could-go-wrong` output goes here).
- `## Verification`: 1-3 bullets, each a real run and its outcome. Screenshots
  or video where they prove a claim.

Keep SHAs, subagent recitals and file-by-file lists out of the body.

## After

Report the PR link and offer `babysit-pr` to watch it to merge-ready.
