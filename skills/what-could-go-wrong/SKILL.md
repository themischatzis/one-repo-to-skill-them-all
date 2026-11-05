---
name: what-could-go-wrong
description: Find what a change could break elsewhere before it ships, and prove the one fact it is safe because of by running code. Use for "blast radius of X", "what could this break", or reviewing a small diff you don't trust.
---

# What could go wrong

Find the breakage grep won't show you. Listing callers is not the job.
Read-only: report, don't fix.

## Don't trust your own writeup

A convincing writeup proves nothing. Find the one or two facts the change's
safety depends on and get each as far down this ladder as is cheap:

1. Asserted. Worthless alone.
2. Cited at a real `file:line` or library source.
3. Walked step by step to show the bad case can't happen.
4. Ran it: a script or test calling the real code that fails loudly if wrong.
5. Reproduced in the running app.

## Steps

1. Read the full change, including what the diff doesn't spell out.
2. Name the one fact it is safe because of.
3. Look past grep: library source and pinned version, timing/teardown order,
   API payloads, DB columns, feature flags, other services or languages
   reading the same data, code several hops downstream.
4. For each risk give likelihood, cost and a real `file:line`. Never invent a
   caller or API. "Searched, found nothing" is a valid answer.
5. Run a small script or test against the real code to prove the key fact.

## Reply

- **What it does** (including the non-obvious part)
- **The one safety fact**: ladder step reached and proof, or "unproven"
- **Risks**: how it breaks, `file:line`, likelihood, cost, how to check
- **Cleared**: what you checked and why it's fine
- **Before you merge**: the cheapest test or repro that catches the real bug
