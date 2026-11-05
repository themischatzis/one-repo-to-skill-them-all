---
name: figure-it-out
description: Design an auditable playbook for large, unusual or unattended work (migration, multi-part change) when no narrower skill fits. Use for "figure it out".
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

Keep the decision log with `what-were-you-thinking` (one row per step: hypothesis, action,
result, verdict). Only commit it if asked. For an unattended run, write the
finish condition and an escape hatch first (stop and write up why if stuck),
and use `where-was-i` to pause or resume.

## E. Verify and hand back

Use `pr-forge` for branch, commit and PR work (its Git conventions and the repo's CONTRIBUTING apply; the personal rule wins).

Check the whole against the Phase A predicate on the real product. Turn any
recurring correction into a guard (`never-again`).

**Reply:** the playbook, rigour and why, path to the trail, what is verified
against the predicate, what is still open.
