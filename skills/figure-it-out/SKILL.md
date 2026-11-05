---
name: figure-it-out
description: Design an auditable playbook when no narrower skill fits, such as a large migration, an ambitious multi-part change, or work Themis reviews after stepping away. Scales rigour to the task, runs a hypothesis loop and logs decisions. Use for "figure it out" or when bug-hunt and ticket-quest don't fit.
---

# Figure it out

When no playbook fits, design one. The first deliverable is the workflow
itself, then you run it. Read
`ground-rules` first.

## A. Frame

Before any code, state:
- **Done** as a falsifiable predicate ("X returns Y for Z", not "works").
- **Scope**, quantified: rough units, effort, blockers found by looking.
- **Rigour**, biased high for one-way doors and wide blast radius, lower for
  reversible small steps. Rigour means gates and artifacts, not trying harder.

Show the framing before a long run. Reversible work proceeds without asking;
a multi-hour run earns one checkpoint.

## B. Design the workflow

- Split into atomic, independently landable units; riskiest unknown first.
- Build the verification harness before the work, with a baseline captured from
  the pre-change state ("old value vs new value").
- One-way-door decisions: get competing designs from parallel subagents and
  have a `rubber-duck` pick holes. Skip for mechanical work.
- Fan out only across seams (different files, services or layers). Give each
  worker its own git worktree. Do not over-fan.
- Write the phase list down; that list is what Themis reviews.

## C. Run the loop

Each unit is an experiment: hypothesis, smallest change, measure on the real
artifact, keep if it advanced, revert if not. Verify each unit before the
next. Inspect the artifact, never a self-report; if something passes too
easily, suspect the check first. Pair delegated work with an independent
`code-review` or `rubber-duck` judge. Never hide a negative result.

## D. Keep the trail

Keep a short decision log in the session `files/` folder: one row per step with
hypothesis, action, result, verdict. Only commit it if asked.

## E. Verify and hand back

Before any branch, commit or PR name, re-read the `ground-rules` section 'Git conventions' (view from that heading; don't rely on a truncated read) and the repo's CONTRIBUTING. The personal rule wins; mention any conflict.

Check the whole against the Phase A predicate on the real product. Turn any
recurring correction into a guard (`correct`).

**Reply:** the playbook, rigour and why, path to the trail, what is verified
against the predicate, what is still open.
