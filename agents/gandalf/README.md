# Gandalf

"A wizard is never late." He plans, you approve, and only then do the
fellowship set off.

Talk to Gandalf and he drafts a plan: who does what, in what order, and
how each step is proved. He asks you to approve it, starts the workers,
follows their collaboration and escalates blockers or unsafe decisions.
Ordinary coordination stays within the team. Commits, pushes and PRs go back to you via
[pr-forge](../../skills/pr-forge/README.md).

He has every tool: read, search, edit, shell, ask you and start subagents. He
picks from all available custom and built-in agents, preferring specialist
roles, with `sam` and `gollum` for small helper tasks. Each brief carries the
context, owned paths, safety boundaries and collaborators the worker needs.
Workers can exchange findings and questions through available messaging tools;
Gandalf relays when those tools are unavailable. Only Gandalf starts workers
and owns assignments, scope and decisions. The [guard](../../guard/README.md)
still rejects recursive Gandalf runs.
Gandalf reads connected MCP data himself and passes it to roles; task-launched
subagents may not have MCP tools.

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
using `python3 scripts/install-agents.py`. It copies the agents, guard and
routing into `~/.copilot`, so changing branches cannot revert the installation.
Rerun it to publish intentional changes, then restart Copilot CLI.

Built-ins do not have the custom role hooks. Gandalf gives them the same safety
rules and supervises them; that is advisory, not hook enforcement.

Gandalf can start as many workers as a task needs in one worktree, as long as
builders own different files. He cannot kill an agent; see
[stopping agents](../../guard/README.md#stopping-agents). For a second branch,
he runs `scripts/new-worktree.sh <new-branch> [base]` himself and starts roles
that write in that worktree. He also runs `git` and `gh` himself.
`git merge`, `gh pr merge` and merge calls through
`gh api` ask you first, and `sudo` is denied. Other sensitive commands (curl,
wget, ssh, cloud CLIs, deploys, publishing) ask you too. In autopilot the
prompt cannot show, so those calls are denied.
Commits and pushes still hit Copilot's normal permission prompt.
