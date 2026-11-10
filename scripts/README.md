# Scripts

Small helpers you read and run yourself. Nothing here runs automatically, and
no agent can run them: the [guard](../guard/README.md) blocks the roles from
creating worktrees.

| Script | What it does |
|---|---|
| `new-worktree.sh <new-branch> [base-ref]` | Creates a sibling worktree on a new branch and prints its path. Refuses an existing branch or directory. |

Run it from inside the repo:

```sh
scripts/new-worktree.sh feat/my-change
```

Each extra branch gets its own worktree on its own new branch.
[Gandalf](../agents/gandalf/README.md) runs this script himself, then starts
roles that write in the new worktree. When done, remove a worktree with
`git worktree remove <path>`.
