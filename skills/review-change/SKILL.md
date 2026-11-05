---
name: review-change
description: Review a PR, branch or diff properly, against the intent of the change, not just the lines. Use for "review this PR/branch/changes", "any concerns", "is this ready to merge". Reports findings; does not fix or post.
---

# Review change

Read-only. Never post comments, approve or push unless asked.

1. **Intent.** Read the PR description, ticket (Jira via MCP if a key exists)
   and linked discussion. State in two lines what the change should do and
   its acceptance criteria. If there is no stated intent, say so.
2. **Scope.** `gh pr view`/`gh pr diff` or `git diff base...HEAD`. List files
   and group them. Flag anything not explained by the intent.
3. **Context.** Read the surrounding code of each change, not just hunks:
   callers, siblings, existing tests, repo conventions (CONTRIBUTING, PR
   template). Check CI status and open review comments.
4. **Judge.** Correctness against the intent; missing acceptance items;
   edge cases; security; tests that would fail without the change; leftover
   or unrelated changes; naming against `pr-forge` Git conventions.
5. **Prove.** Run the tests or reproduce the claim for anything you will call
   a bug. Mark unproven concerns as "unverified". For risky changes, run
   `what-could-go-wrong`; for contested designs, `tear-it-apart`. Use a `code-review`
   subagent as a second pair of eyes on large diffs.
6. **Report.** Verdict first (ready / needs changes / blocked). Then findings
   ranked by severity, each with `file:line`, why it matters, evidence, and a
   suggested fix. Then acceptance checklist, then nits. Offer to draft
   review comments; do not post.
