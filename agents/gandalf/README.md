# Gandalf

"A wizard is never late." He plans, you approve, and only then do the
fellowship set off.

Talk to Gandalf and he drafts a plan: which role does what, in what order, and
how each step is proved. He asks you to approve it, starts the agents the task
needs as subagents, reports after every step, and stops at anything shady. He asks at
every decision and never assumes. Commits, pushes and PRs go back to you via
[pr-forge](../../skills/pr-forge/README.md).

He has every tool: read, search, edit, shell, ask you and start subagents. He
picks the agents a task needs himself, from the roles below, `sam` and `gollum`,
or a built-in such as `explore`, and passes each one the context it needs in
its brief. A [guard](../../guard/README.md) hook still applies.

The [agent instructions](gandalf.agent.md) have the detail. Roles he can call
(in [roles/](../../roles)):
[adversary](../../roles/adversary/README.md), [analyst](../../roles/analyst/README.md),
[architect](../../roles/architect/README.md), [backend](../../roles/backend/README.md),
[ci-fixer](../../roles/ci-fixer/README.md), [devops](../../roles/devops/README.md),
[docs](../../roles/docs/README.md), [frontend](../../roles/frontend/README.md),
[manager](../../roles/manager/README.md), [ml-engineer](../../roles/ml-engineer/README.md),
[prompt-engineer](../../roles/prompt-engineer/README.md), [qa](../../roles/qa/README.md),
[resolver](../../roles/resolver/README.md), [retrieval](../../roles/retrieval/README.md),
[reviewer](../../roles/reviewer/README.md), [security](../../roles/security/README.md),
[visionary](../../roles/visionary/README.md), [vp](../../roles/vp/README.md).

Install with the [repository setup guide](../../README.md#equip-your-skills),
including the guard link. Install the guard first: a hook pointing at a missing
script is untested, so do not rely on it failing closed.

Gandalf can start as many roles as a task needs in one worktree, as long as
builders own different files. He cannot kill an agent; see
[stopping agents](../../guard/README.md#stopping-agents). For a second branch,
he runs `scripts/new-worktree.sh <new-branch> [base]` himself and starts roles
that write in that worktree. He also runs `git` and `gh` himself. Merging is
the one thing he cannot do: `git merge`, `gh pr merge` and merge calls through
`gh api` ask you first, and `sudo` is denied. Other sensitive commands (curl,
wget, ssh, cloud CLIs, deploys, publishing) ask you too. In autopilot the
prompt cannot show, so those calls are denied.
Commits and pushes still hit Copilot's normal permission prompt.
