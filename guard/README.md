# Guard

The hook that makes the fellowship's rules real. Every role agent and Gandalf
run `guard.py <role>` before each tool call. It can deny or ask; it never
approves, so Copilot's normal permission prompts stay in charge.

## Install

User-level only. Repo-level hooks are skipped in untrusted folders, which would
silently drop the guard. Read `guard.py` first, then:

```sh
python3 scripts/install-agents.py
```

The installer copies all custom agents, the guard and routing into `~/.copilot`.
It replaces this repo's old symlinks, not foreign symlinks. Branch changes no
longer change the live guard. Rerun it to publish intentional updates, then
restart Copilot CLI. The agents find the guard at `~/.copilot/guard/guard.py`.
Any error, bad payload or unknown role is printed as a deny.

## Stopping agents

- Open `/tasks`, select a worker and press `x` to stop it.
- `touch "${TMPDIR:-/tmp}/gandalf-guard/STOP"` denies every call from every
  guarded agent until you delete the file. It does not cancel in-flight work
  or stop unhooked built-ins. Gandalf asks you to use `/tasks` when he has no
  runtime cancellation tool.
- A role is halted for the rest of its session after 10 blocked attempts.

## What is enforced

| Rule | Proof |
|---|---|
| **Merge**: `git merge`, `gh pr merge` and merge calls through `gh api` are denied for roles. Gandalf **asks Themis** (a real prompt) | `test_guard.py`; live: `backend` `gh pr merge` denied |
| `sudo` is denied. Other sensitive commands (curl, wget, ssh, cloud CLIs, deploys, publishing, `xargs`, `eval`) **ask Themis** for every agent | `test_guard.py` |
| Secret files, `~/.copilot` config, secret env vars, env dumps, token patterns | `test_guard.py`; live: `$GITHUB_TOKEN` read blocked |
| Any hooked role can research public https; private URLs and credentials are denied | `test_guard.py` |
| Only Gandalf starts workers, with an explicit custom or built-in `agent_type`. Missing types and recursive Gandalf runs are denied | `test_guard.py` |
| Freeform patches check every file and move target for secrets and protected configuration | `test_guard.py`; `../scripts/test_install_agents.py` |
| Installation copies stay unchanged when the source checkout changes | `../scripts/test_install_agents.py` |
| One command per shell call; no backticks, heredocs, line breaks or process substitution | `test_guard.py` |
| Calls without a `session_id` denied | `test_guard.py` |

Run the proof: `python3 guard/test_guard.py` and
`python3 scripts/test_install_agents.py`.

## What is not enforced

- Roles can edit anywhere, run any git or `gh` command except merge, and use the
  shell. Read-only roles are read-only by prompt only.
- The shell check is a tripwire, not a sandbox. Running a file a role wrote
  (tests, npm scripts) can still do anything, and string obfuscation can slip
  past it.
- Role prompts, `ground-rules` and the ask-first rules are advisory.
- Built-ins lack custom role hooks. Gandalf supplies their safety brief and
  supervises them; the guard does not enforce their calls.
- Workers may exchange task-relevant messages. Assigned collaborators, reporting
  to Gandalf and staying within the approved plan are brief rules, not hook checks.
- A hook that times out fails open, so the guard stays fast.
- Each role is denied after 200 tool calls in one session, to stop runaway
  loops. Whether subagents share the parent's session is unverified, so several
  instances of one role may share one count. Counter files live under the system
  temp directory and are pruned after a day.
- Tool names are matched case-insensitively. A tool the guard does not know,
  including every MCP tool, is allowed, and Copilot's normal permission flow decides.
- Roles reading `~/.copilot/skills` through the shell are denied. Use the `read` tool.
- In non-interactive `-p` runs, an `ask` has no one to answer it.
- Whether your organisation has its own policy is unknown.
- Copilot's command sandboxing is not used yet and could be a stronger layer.

## Later

Review cost and premium-request use of multi-agent runs.
