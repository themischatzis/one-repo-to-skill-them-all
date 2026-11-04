---
name: ground-rules
description: Themis's core engineering principles, condensed. Read before any non-trivial coding task, and whenever bug-hunt, ticket-quest or figure-it-out tells you to. Covers smallest change, root causes, proof, tests, delegation and autonomy.
---

# Ground rules

Adapted from Cursor's pstack `poteto-mode` principles, merged with the
installed `ponytail` skill. Apply the ones that fit; in the reply, name each
rule that changed a decision and the choice it changed. Say nothing about the rest.

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

## Reply style

Short declarative sentences. Open with the user's goal in your own words.
Lead with impact (who benefits, what changes), then detail. No filler.
