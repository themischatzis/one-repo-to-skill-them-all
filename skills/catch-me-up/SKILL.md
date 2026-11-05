---
name: catch-me-up
description: Plain-words catch-up on what changed this session and every call waiting on Themis. Use for "catch me up", "palantir", "what happened", "what's waiting on me", "explain that simply", or after a long autopilot run.
---

# Catch me up

Report what is there, in plain words. Read-only: change no code, start no
job, post nothing. Read `ground-rules` for reply style.

Assume he remembers his last message and nothing after it. Notifications and
subagent results are not his messages.

## Gather

- Your own work, subagent reports and anything others said in this session
  since his last message.
- Re-check live state for every PR, CI run, branch or agent touched. Never
  report remembered state. Verify each number against its source and say when
  you corrected one.
- Action items: calls or steps only he can take (product choice, approval,
  irreversible action, access you lack). Include ones still open from earlier.
  Work you can still do yourself is not an action item. Never invent a call to
  fill the reply.

## Write

Plain words, short sentences, no jargon, like one person catching up another.
Say what changed for him, not how you did it: "the tests pass", not "CI is
green". Leave out hashes, paths, commands and counts unless he needs one to act.
Name PRs and branches the way he would, with the link.

1. One sentence: what waits on him (or "nothing waits on you").
2. What happened: under 100 words, only what changed something for him.
3. Each waiting call: about 30 words. What it changes for users, the evidence,
   the risk, your pick. Write "unknown" for a fact you lack. Never cut an item
   to save words and never replace an item with a link.
4. If he only asked "explain that simply": restate your last message in plain
   words and stop. Skip the rest.

A small table or ASCII sketch is fine when it shows a change faster than prose.
