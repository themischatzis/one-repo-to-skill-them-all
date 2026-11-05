---
name: skill-retro
description: Private journal of how Themis works, and review of his skills against it. Use for "note that...", "log this", "reflect", "review my skills", "weekly retro", "what are my patterns".
---

# Skill retro

The journal is `journal.md` in the private `skill-journal` repo, cloned at
`$SKILL_JOURNAL_DIR` (default `~/Projects/skill-journal`). If the clone is
missing, ask before cloning `themischatzis/skill-journal` with `gh`.
This skill is public: never copy journal contents, tickets, company names or
usernames into this repo.

## Log

When asked to note something, or when a skill from this repo was just used and
Themis corrected, rejected, overrode or praised something, append one line:
`- YYYY-MM-DD [skill] observation → keep | change | add | delete?`
Record observed behaviour and quoted preferences, not guesses about him.
Don't log every turn unprompted. Pull before writing. Commit the journal
(`feat: Capitalized title`) and push only when he agrees or asks. If a durable
cross-repo preference is stated, also offer to save it as a Copilot memory.

## Review

1. Pull the journal; read it plus `git log`/`git status` of the skills repo.
2. Query past sessions (`session_store_sql`, last 7-14 days) for sessions that
   used these skills: which ran, which never did, where he corrected course,
   what he asked for that no skill covered.
3. For each skill decide **keep**, **change** or **delete**, and list gaps to
   **add**. Back every call with a journal line or session evidence;
   "never used" is a finding, not proof it should go.
4. Present a table (skill, evidence, verdict, proposed change), then make the
   agreed edits uncommitted for review. Don't commit, branch or open a PR
   unless asked.
5. Append a dated retro line to the journal.

## Reflect (after one session)

Use when he says "reflect" or right after a task that taught something. One
weird session is an anecdote: skip trivial sessions and anything an existing
skill already covers.

1. Take this session's history (`session_store_sql`, this session only) or a
   tight digest of it.
2. Launch three read-only reviewers in parallel through the `task` tool
   (`divide-and-conquer`): **judgment** (where he corrected or overrode me),
   **tooling** (commands, tools and skills that failed or were skipped),
   **divergent** (what a different approach would have done better).
3. Synthesize into Accepted, Rejected and Backlog. Accept only a change that
   would alter a future decision. Anything a lint, script or check would
   enforce more reliably goes to Backlog via `never-again`.
4. Show all three lists and wait for approval. Then make the approved skill
   edits uncommitted in the skills repo, and log one journal line.

## Mirror (distil how he works)

Use for "what are my patterns" or a monthly check. Mine the journal and past
sessions for repeated preferences in replies, delegation, verification, code,
prose and process. Ask him which patterns are really him (`ask_user`); never
assume. Propose edits to `ground-rules` only for confirmed ones, keeping it
short, and for update runs mine only what is new since the last edit.

## Trial

When a skill edit is big or a borrowed skill is adopted, offer
`trial-by-fire` before keeping it.
