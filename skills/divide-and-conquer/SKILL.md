---
name: divide-and-conquer
description: Fan out parallel subagents over independent slices, return one consolidated report. Use only when asked ("divide and conquer", "swarm this", "fan out", "great eagles") or for clearly independent slices.
---

# Divide and conquer

The eagles arrive when the work is wide, not when it is hard. Parallel subagents cost
credits and context: use only on independent slices. Never for one continuous
trace. Read `ground-rules` (guard the context window, separate shared state).

## Frame

1. State the done predicate and the report each worker returns.
2. Pick a shape: **slices** (partition the work), **race** (N workers, same
   brief, declare `first pass`, `rank all` or `best-of` up front), or both.
3. Give each writing worker its own output location, a git worktree where
   possible. Workers that measure or verify get the exact commit SHAs and the
   method (what one sample is, how many).

## Fan out

Launch all workers in one message through the `task` tool, in background mode,
`general-purpose` for work that needs edits and `explore` for read-only
research. Leave `model` to the harness defaults. Each brief stands alone: goal,
scope, exact slice, how to verify, what to report. Reports are `PASS`,
`ISSUES` or `BLOCKED` with evidence; a worker that proves a defect lists every
defect it can prove.

## Aggregate

While they run, do independent work and do not poll. Read each result once.
Drop one that omits the SHAs or method its brief named and respawn it once;
after a second miss record a gap (a gap is not a pass). If a worker drops out,
continue with N-1 and say so. Never paste raw worker dumps.

## Report

One table (slice, verdict, evidence), issue one-liners, gaps, and the race rule
if used. Log it in the `what-were-you-thinking` log for long runs.
