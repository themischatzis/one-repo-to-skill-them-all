---
name: ticket-quest
description: End-to-end playbook for delivering a Jira ticket or feature request - understand, design small, build in verifiable units, review and prove. Use for "work on this ticket", "implement PROJ-123", "build this", or any non-bug change.
---

# Ticket quest

You own the design: plan, delegate, review, verify.
Read `ground-rules` first.
Use `bug-hunt` instead for defects, `figure-it-out` for large or
multi-day work.

## Steps

1. **Intake.** Read the ticket with the Atlassian MCP (description,
   acceptance criteria, linked issues, comments, Figma links; open Figma
   with the Figma MCP when design matters). Restate the goal, the problem
   being solved, and the smallest change you expect. List acceptance criteria
   as a checklist; ask only about genuine product calls, not facts you can
   observe.
2. **Understand the area** with `how-does-it-work`, and
   `why-is-it-like-this` if you plan to change existing behaviour.
3. **Name the data shape** and pick its structure (table, state machine,
   typed model). For a decision that is hard to reverse, get two competing
   designs from parallel subagents and choose; say why.
4. **Decompose** into small units, riskiest first, each ending in a check.
   Note which can run in parallel (disjoint files) and which share state.
5. **Build** each unit with the smallest change. Write the test with the
   behaviour (`ground-rules`: test behaviour, not implementation). Delegate
   self-contained units to `general-purpose` subagents with exact scope and
   success criteria; review their diffs.
6. **Verify** each unit, then the whole against the acceptance checklist on the
   real surface (run it, hit the endpoint, open the page).
7. **Review.** `blast-radius` on the change; `code-review` on the diff;
   `interrogate` if the design was contested.
8. **Hand off.** Draft a short PR description (why first, then what, then how
   it was verified) and a Jira comment, and offer them. Do not post.

## Do not

Commit, push, branch, open a PR, comment on or transition the ticket unless asked.
Don't add scope the ticket didn't ask for; note it as a follow-up.

**Reply:** goal, what you built, choices and why, acceptance checklist with
evidence for each item, open decisions. Tables for design alternatives.
