---
name: where-was-i
description: Pause work cleanly, or resume and recall earlier sessions. Use for "pause", "I'm logging off", "where did I leave off", "recall my work on X", "continue that branch".
---

# Where was I

Three modes. Pick one from the request. Read `ground-rules` first.

## Pause

Only on an explicit "pause", "stopping", "going offline". "Keep going" is not
a pause.

1. Stop at a safe boundary: finish or back out of the current step. Cancel
   running subagents.
2. Take no irreversible action: no push, branch or PR unless already agreed.
3. Make the work durable: one clear `wip:` commit on the current branch, only
   with his agreement (commits are ask-first). If he declines, list the dirty
   files instead. Say in one line if the tree is broken.
4. Write a resume note to `/tmp/<slug>-resume.md`, or the `what-were-you-thinking` log if one
   exists: intent, progress and what is verified, current state, next steps,
   key files, gotchas.

Reply: where you stopped, what is on disk versus in your head, whether the
tree is clean, and the first action on resume.

## Pick up

Resume a previous session or branch. The prior trail is authoritative: read
it, do not redo it.

1. Find the trail: resume note, `what-were-you-thinking` log, the branch (`git log`,
   `git diff` against base), PR, and past sessions via `session_store_sql`
   (this repo only; scope by `cwd`/`repository`).
2. Rebuild state: branch, what landed, open todos, decisions made. Parse long
   transcripts in a subagent and keep only the timeline in the main thread.
3. Diff done against planned. Name the resume point. Do not re-run the old
   repro or redo finished work.
4. Hand the rest to the matching skill (`bug-hunt`, `ticket-quest`,
   `figure-it-out`).
5. Verify inherited claims on the real artifact before building on them.

## Recall

"Where did I leave off on X?" Rebuild context before acting.

1. Pin the scope: window (default 7 days), topic, repository. Say it back.
2. Query `session_store_sql` (cloud, time-bound, `LIMIT`) for sessions, turns,
   refs and files on the topic. Fan out to subagents only if many sessions.
3. Add the shared record when the topic is a feature or bug: open PRs, recent
   commits, Jira (read-only), plus `who-did-this` for what was tried.
4. Read the `skill-journal` entries on the topic if relevant.
5. Return a tight brief: current state, what was tried and did not hold, open
   threads, artifacts (PRs, tickets, branches), and the next action.

Never read other projects' sessions unless asked.
