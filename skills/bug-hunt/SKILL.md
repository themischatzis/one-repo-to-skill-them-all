---
name: bug-hunt
description: End-to-end playbook for fixing a bug: from a Jira ticket or a description to a reproduced, root-caused, test-first, verified fix. Use for "fix this bug", "investigate this defect", "this is broken", or a Jira bug key.
---

# Bug hunt

You own the outcome: plan, delegate the legwork, review, verify.
Read `ground-rules` first.

Every shipped line traces to evidence. A "might help" guard is a hypothesis,
not a fix; if evidence refutes it, revert what it motivated.

## Steps

1. **Intake.** If a Jira key or URL is given, read it with the Atlassian MCP:
   Background, Impact, Steps to reproduce, Actual and Expected. Restate the
   goal and the smallest change you expect, in your own words. If the evidence
   rules out the fix requested, say so and stop.
2. **Reproduce it yourself** on the same surface the user hit (test, CLI,
   browser, API call). Ask the human only with a specific reason you cannot
   reach it, after trying. If it won't fire, tighten conditions or add
   logging until it does.
3. **Find the cause by elimination.** List candidate hypotheses, then pick the
   check that cuts the most space, get runtime evidence, eliminate. Use
   `how-does-it-work` for the area and `why-is-it-like-this` for regression
   history. Send bulky reading to `explore` subagents. Confirm the surviving
   mechanism with an experiment, not by reading alone.
4. **Plan the smallest root-cause fix.** Crossing a function boundary or
   several callers: compare 2 designs first, and run `blast-radius`.
5. **Failing test first** via `tdd-bug-fix` when a cheap local test exists;
   otherwise keep the repro command as the check.
6. **Implement** the fix yourself, or hand a tightly scoped brief to a
   `general-purpose` subagent and review its diff line by line.
7. **Verify** on the original surface: the repro now passes, neighbouring tests
   pass. Wrong-surface or inconclusive is not a pass.
8. **Review.** Run `code-review` on the diff. For contested or risky fixes,
   run `interrogate`.
9. **Repeat check.** If this class of bug has happened before, suggest a guard
   via `correct`. Do not build it unasked.

## Do not

Commit, push, open a PR, comment on or transition the Jira ticket unless asked.
Offer them at the end.

**Reply:** goal, what was broken, root cause, fix, how verified. Paste the
failing-then-passing repro output verbatim. List rules from `ground-rules`
that changed a decision, and open questions.
