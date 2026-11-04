---
name: skill-retro
description: Keep a private journal of how Themis works and review the personal skills against it. Use to log a working-style observation ("note that...", "log this") or for a skill retro, such as "review my skills", "weekly retro", "what should change in the skills".
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
