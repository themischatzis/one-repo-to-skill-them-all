---
name: untangle-this
description: Rebase a branch or PR onto its base and resolve merge conflicts safely. Use for "rebase", "resolve conflicts", "update my branch", "PR has conflicts".
---

# Untangle this

1. **Prepare.** `git status` must be clean (stash or ask). Identify branch
   and base (`gh pr view` if a PR). `git fetch`. Note the current tip SHA as
   a rollback point; never rebase a shared branch without asking.
2. **Understand both sides.** For each conflicted file, read what the base
   changed (`git log base..` for that file) and what the branch intended
   (PR description, commits). Resolve by intent, not by picking a side.
3. **Resolve.** Keep both intents where they are compatible. Never leave
   markers. Lockfiles and generated files: regenerate with the package
   manager, don't hand-merge. If intent is unclear, ask.
4. **Verify.** Build, lint and run the tests that cover touched files. Compare
   `git diff <old-tip>..HEAD` to confirm only the intended changes remain.
5. **Hand back.** List each conflict and how it was resolved. Pushing needs
   `--force-with-lease`; ask first, and use the `ground-rules` push fallback
   if SSH fails.
