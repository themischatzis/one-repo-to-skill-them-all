# Scripts

Small helpers you read and run yourself. Nothing here runs automatically.

| Script | What it does |
|---|---|
| `python3 scripts/install-agents.py` | Copies custom agents, guard and routing into `~/.copilot`. Replaces this repo's symlinks and managed copies; refuses foreign symlinks. |
| `new-worktree.sh <new-branch> [base-ref]` | Creates a sibling worktree on a new branch and prints its path. Refuses an existing branch or directory. |

Agent installation is independent of branch changes. Rerun the installer to
publish edits, then restart Copilot CLI. Skills and MCP configuration are not
changed. Check it with `python3 scripts/test_install_agents.py`.

Run the worktree helper from inside the repo:

```sh
scripts/new-worktree.sh feat/my-change
```

Each extra branch gets its own worktree on its own new branch.
[Gandalf](../agents/gandalf/README.md) runs this script himself, then starts
roles that write in the new worktree. When done, remove a worktree with
`git worktree remove <path>`.
