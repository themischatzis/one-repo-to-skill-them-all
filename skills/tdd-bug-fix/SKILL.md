---
name: tdd-bug-fix
description: Fix a bug test-first when there is a cheap, obvious test target. Use when asked for TDD, a regression test, or a failing test first, or when fixing a bug (e.g. from a Jira ticket) that a small unit test can reproduce. Skip when the test path is expensive or unclear.
---

# TDD bug fix

Make the broken behaviour executable before touching production code.
Adapted from Cursor's pstack `tdd` skill.

## When not to

If a test needs broad harness setup, brittle mocks, slow end-to-end infra,
production-only state, or vague repro steps, don't build one. Use the closest
cheap check instead (script, repro command, log assertion) and say so.
No new test beats a bad test.

## Steps

1. State intended vs current behaviour and the smallest repro. If the bug comes
   from a Jira ticket, use its Steps to reproduce / Expected Result.
2. Find the narrowest existing test style for that code path and follow it.
3. Write the smallest failing test that encodes intended behaviour, not the
   current implementation.
4. Run it. Confirm it fails for the right reason before fixing.
5. Make the smallest production fix.
6. Rerun the test and the neighbouring tests.

## Guardrails

- Never edit a test to match a wrong implementation or weaken assertions
  without a stated reason.
- No fixture churn or unrelated coverage.
- Make flaky repros deterministic.

## Reply

Name the test, its failure before the fix, and its pass after. If you couldn't
show failing-before, say why and what you used instead.
