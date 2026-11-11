# Guard

The hook that makes the fellowship's rules real. Every role agent and Gandalf
run `guard.py <role>` before each tool call. It can deny or ask; it never
approves, so Copilot's normal permission prompts stay in charge.

## Install

User-level only. Repo-level hooks are skipped in untrusted folders, which would
silently drop the guard. Read `guard.py` first, then:

```sh
ln -s "$PWD/guard" "$HOME/.copilot/guard"
```

The agents then find it at `~/.copilot/guard/guard.py`. Any error, bad payload
or unknown role is printed as a deny.

## Stopping agents

- Esc twice stops what is running.
- `touch "${TMPDIR:-/tmp}/gandalf-guard/STOP"` denies every call from every
  guarded agent until you delete the file. Gandalf himself cannot kill agents.
- A role is halted for the rest of its session after 10 blocked attempts.

## What is enforced

| Rule | Proof |
|---|---|
| **Merge**: `git merge`, `gh pr merge` and merge calls through `gh api` are denied for roles. Gandalf **asks Themis** (a real prompt) | `test_guard.py`; live: `backend` `gh pr merge` denied |
| `sudo` is denied. Other sensitive commands (curl, wget, ssh, cloud CLIs, deploys, publishing, `xargs`, `eval`) **ask Themis** for every agent | `test_guard.py` |
| Secret files, `~/.copilot` config, secret env vars, env dumps, token patterns | `test_guard.py`; live: `$GITHUB_TOKEN` read blocked |
| Web fetch only for `analyst` and `visionary`, public https only | `test_guard.py` |
| Only Gandalf starts agents. He may pick any, built-in or custom | `test_guard.py` |
| One command per shell call; no backticks, heredocs, line breaks or process substitution | `test_guard.py` |
| Calls without a `session_id` denied | `test_guard.py` |

Run the proof: `python3 guard/test_guard.py`.

## What is not enforced

- Roles can edit anywhere, run any git or `gh` command except merge, and use the
  shell. Read-only roles are read-only by prompt only.
- The shell check is a tripwire, not a sandbox. Running a file a role wrote
  (tests, npm scripts) can still do anything, and string obfuscation can slip
  past it.
- Role prompts, `ground-rules` and the ask-first rules are advisory.
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
