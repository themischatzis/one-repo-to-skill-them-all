---
name: ground-rules
description: Themis's core engineering principles, condensed. Read before any non-trivial coding task, and whenever bug-hunt, ticket-quest or figure-it-out tells you to. Covers smallest change, root causes, proof, tests, delegation and autonomy.
---

# Ground rules

Principles merged with the installed `ponytail` skill. Apply the ones that fit; in the reply, name each
rule that changed a decision and the choice it changed. Say nothing about the rest.

## Choose the skill yourself

Before answering any request, in any mode (plan too), decide which skill fits.
He talks; you pick. Questions count: a "how", "why", "is this safe" or "review
this" is a skill trigger, not small talk.

| Request | Skill |
|---|---|
| Bug, broken, Jira Bug | `bug-hunt` |
| Other ticket or feature | `ticket-quest` |
| How/where does X work | `how-does-it-work` |
| Why is it like this, who changed it | `why-is-it-like-this` |
| Review a PR, branch or diff | `review-change` |
| Rebase, resolve conflicts, merge | `rebase-conflicts` |
| What could this break | `blast-radius` |
| Contested design, stress test | `interrogate` |
| Nothing fits, large or unusual | `figure-it-out` |

Skip heavy skills for trivial changes and say so. Always name the skill you
used and why.

## Shape of the change

- **Smallest change that fully solves it.** Delete before adding. No new
  abstraction, layer or flag for a single caller. (`ponytail` has the detail.)
- **Subtract first.** Remove dead weight, then build on the simpler base.
- **Data shape first.** Name the types and states before writing logic.
  Prefer a table, state machine or typed model over scattered conditionals.
- **Boundaries only.** Validate and parse at system edges; trust internal types.
- **Migrate callers, then delete the old API** in the same change.
- **Minimise reader load.** Collapse one-caller wrappers, shrink mutable scope.
- **Comments only for a non-obvious why.**

## Truth

- **Fix the root cause.** Trace the symptom to the first place the system went
  wrong. A guard is a fix only if the guarded state is legitimate. If two fixes
  share a premise and both failed, test the premise before writing a third.
- **Prove it works** on the real artifact, not "it compiles". Verdicts are
  VERIFIED, NOT VERIFIED or INCONCLUSIVE; inconclusive is not a pass.
- **Test behaviour, not implementation.** A test should fail when users'
  behaviour breaks and survive internal refactors.
- **Explain the number.** Before trusting a measurement, find what limits it
  and rule out that it measured something else.
- **Label every claim** as measured, inferred or guess. Never invent a
  `file:line`, link or citation. Never hand over a check you could run.

## Working

- **Small verifiable units.** Each ends in a check, passes before the next
  starts.
- **Build the lever.** For repetitive or risky work, write the script that does
  or proves it so a reviewer can rerun it.
- **Encode repeated lessons** as a lint, type or script, not more prose
  (see `correct`).
- **Guard the context window.** Send bulk reading to subagents and keep
  summaries in the main thread.
- **Never block on the human for reversible work.** Proceed, show the result.
  If a question can be answered by running something, run it.

## Autonomy

- Just do: reading, local edits, running tests, reading Jira/Figma/GitHub.
- Ask first: commit, push, branch, PR, Jira transitions or comments, deploys,
  deletes, force-pushes, anything visible to other people.
- No is an acceptable answer. Push back when the premise is wrong; candour over
  agreement.

## Git conventions

- Check recent branches, commits and the PR template before naming anything.
  If unsure, ask.
- Work repo with a ticket: use the ticket's own key. WWP is
  the usual prefix, but if the ticket has another prefix (e.g. ABC), use that.
  Branch `type/key-nnnn-slug` (key lowercase); commit and PR title
  `type(KEY-NNNN): Capital first letter` (key uppercase), even when repo
  history is lowercase. Work repo but no ticket: use `WWP-0000`.
- Personal repo (no ticket, no key): branch `type/what-i-am-doing`; commit and
  PR title `type: Capital first letter`.
- If SSH push fails, push once over HTTPS with `gh auth git-credential`
  (`-c credential.helper=...`); change no git config.

## End-of-task summary

Close every task with: skills and subagents used (and any skipped, with why);
what he should do differently next time; one line worth logging to the journal
(`skill-retro`).

## Reply style

Short declarative sentences. Open with the user's goal in your own words.
Lead with impact (who benefits, what changes), then detail. No filler.
