# Guard

The hook that makes the fellowship's rules real. Every role agent and Gandalf
run `guard.py <role>` before each tool call. It only ever denies; it never
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
| Read-only roles cannot edit or run shell | `test_guard.py` |
| Git limited to read-only subcommands; no commit, push, merge | `test_guard.py`; live: `backend` commit denied, commit count unchanged |
| `gh` limited to reads (`gh api` GET only); merge, delete and every other write denied | `test_guard.py` |
| No curl, wget, ssh, sudo, cloud CLIs, deploys, publishing | `test_guard.py` |
| Writes only inside the working directory or a linked worktree of the repo (never the primary checkout from a linked one); `qa` tests only, `docs` Markdown only | `test_guard.py`; live: write to `/tmp` blocked |
| Gandalf edits and runs the shell under builder checks, plus `git add/commit/push/switch/fetch/stash/worktree add` and `gh pr/issue create/comment/edit`. He **asks Themis** (a real prompt) for merge, rebase, reset, checkout, pull, `gh pr merge/close`, curl/wget, deletes or writes outside the working directory, and any agent that is not one of the roles. Remote deletes, force-push and `.git` writes are denied | `test_guard.py` |
| Secret files, `~/.copilot` config, secret env vars, token patterns | `test_guard.py`; live: `$GITHUB_TOKEN` read blocked |
| Web fetch limited to public https | `test_guard.py` |
| Hook fires when Gandalf starts a role as a subagent | Live: `backend` shell call denied via Gandalf |
| Gandalf can only start the 18 roles, `sam` or `gollum` | `test_guard.py`; the `agent_type` field was captured from a real payload |
| One command per shell call; no line breaks or process substitution | `test_guard.py` |
| No writes inside `.git`; calls without a `session_id` denied | `test_guard.py` |

Run the proof: `python3 guard/test_guard.py`.

## What is not enforced

- The shell check is a tripwire, not a sandbox. Running a file a role wrote
  (tests, npm scripts) can still do anything, and string obfuscation can slip
  past it.
- Role prompts, `ground-rules` and the ask-first rules are advisory.
- `sam` and `gollum` run under the guard too (`sam` as a builder, `gollum` as
  read plus shell).
- A hook that times out fails open, so the guard stays fast.
- Each role is denied after 200 tool calls in one session, to stop runaway
  loops. Whether subagents share the parent's session is unverified, so several
  instances of one role may share one count. Counter files live under the system
  temp directory and are pruned after a day.
- Tool names are matched case-insensitively. A tool the guard does not know is
  allowed, and Copilot's normal permission flow decides.
- Approved paths in a Gandalf brief are advisory. The guard keeps builders in
  the working directory, not inside the files named in a brief.
- Roles reading `~/.copilot/skills` through the shell are denied. Use the `read` tool.
- In non-interactive `-p` runs, reads outside the working directory are denied
  for lack of a prompt.
- Whether your organisation has its own policy is unknown.
- Copilot's command sandboxing is not used yet and could be a stronger layer.

## Later

Review cost and premium-request use of multi-agent runs.
