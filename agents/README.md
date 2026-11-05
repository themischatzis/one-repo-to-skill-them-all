# The companions

Skills are instructions. Agents are the ones who actually carry the bags.

| Agent | Who they are | Reach for them when |
|---|---|---|
| `sam` | Loyal, sensible, reads [ground-rules](../skills/ground-rules/README.md) before every task, and never wanders off with a commit. | You delegate an edit or helper task to a subagent and want it done small, proven and reported honestly. |
| `gollum` | Read-only, deranged, and passionate about deleting comments. My precious. | You want a diff or file set checked for narrating, apologetic or commented-out clutter before review. He flags; he never edits. |

## Equip your companions

Link them into Copilot's personal agents directory. Edits in the repo reach the
linked agent immediately.

```sh
mkdir -p "$HOME/.copilot/agents"
for a in agents/*.agent.md; do
  n=$(basename "$a")
  [ -e "$HOME/.copilot/agents/$n" ] || ln -s "$PWD/$a" "$HOME/.copilot/agents/$n"
done
```

Run it from the repo root, then use `/agent` to confirm they are listed.

## Adding a companion

Create `agents/<name>.agent.md` with `name` and `description` frontmatter and a
short body. Keep each agent to one job and say what it must never do.
