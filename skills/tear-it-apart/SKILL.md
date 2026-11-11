---
name: tear-it-apart
description: >-
  Adversarial review: subagents try to break a change or design; only run-proven findings survive. Use for "tear it apart", "interrogate", "stress test this", "find blind spots". Reports, does not fix.
---

# Tear it apart

Adversaries try to break a change. A finding survives only if a run proves it.
Report; do not fix.

## Frame

Scope is what the user names, else the current branch diff against its merge
base plus the working tree. Restate the intent in your own words from the
request, commits and PR or Jira description. Ask if the intent is unclear.

## Fan out

Launch 3 subagents in parallel with the scope, the intent and this brief:
> Break this change. Prove each finding with a run against the real code: a
> failing test, repro script or command output showing wrong behaviour. Do
> not edit the repo; put repros in a scratch directory under /tmp. Report each
> finding with a title, the exact command, the output printed and the output
> the intent requires. Drop anything you could not run.

Give each a different angle so they don't duplicate: (1) correctness and edge
cases, (2) concurrency, failure, security and input handling, (3) what else in
the system depends on it (`what-could-go-wrong`). Use a `general-purpose` agent for
these; add a `rubber-duck` pass on the design itself if it is contested.

## Verify

Rerun each finding's command yourself. Keep it only if the output shows the
failure and the failure breaks the intent. Merge findings with the same root
cause. Drop the rest and count them.

## Hand back

- **Intent**: the restatement.
- **Findings**: command, output, how it breaks the intent, which angle found it.
  Say "no verified findings" when none survive.
- **Dropped**: count per adversary and why.
