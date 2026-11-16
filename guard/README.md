<!-- # Guard

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
A bad payload or unknown role is printed as a deny. A guard bug (crash) denies
everything except reads (read, view, grep, glob) that touch no secret.

## Denial log

Every deny, ask and crash appends one redacted line (time, role, tool, rule
code, short session id; never the command, path or token) to
`~/.copilot/guard-logs/denials.log`. It rotates at 1 MB, keeps one backup, and
agents can read it. Set `GUARD_LOG` to move it. Count denials by rule with
`jq -r .code ~/.copilot/guard-logs/denials.log | sort | uniq -c | sort -rn`.

## Stopping agents

- Open `/tasks`, select a worker and press `x` to stop it.
- `touch "${TMPDIR:-/tmp}/gandalf-guard/STOP"` denies every call from every
  guarded agent until you delete the file. It does not cancel in-flight work
  or stop unhooked built-ins. Gandalf asks you to use `/tasks` when he has no
  runtime cancellation tool.
- A role is halted for the rest of its session after 10 policy denials (secrets, sudo, merge, force-push, spawn). Guard crashes and asks do not count.

## What is enforced

| Rule | Proof |
|---|---|
| **Merge**: `git merge`, `gh pr merge` and merge calls through `gh api` are denied for roles. Gandalf **asks Themis** (a real prompt) | `test_guard.py`; live: `backend` `gh pr merge` denied |
| `sudo`, plain force-push (`--force`, `-f`, `+ref`, `:ref`, `--delete`) and `gh api -X DELETE` are denied (Gandalf asks for the API delete). `--force-with-lease` is allowed only right after a finished rebase (last reflog entry). Publishing, deploys, ssh and cloud CLIs, `curl | sh` and `curl` uploads **ask Themis** for every agent | `test_guard.py` |
| Secret files, secret env vars, env dumps, `gh auth token`, token patterns. Under `~/.copilot` agents may read everything except `config.json`, `mcp-config.json`, `settings.json` and files named oauth, token, credential or secret; every write is denied. Shell reads there work with read-only commands (`ls`, `cat`, `grep`, `rg` without `--pre`, `find` without `-delete`/`-exec`); globs on hidden names are denied | `test_guard.py`; live: `$GITHUB_TOKEN` read blocked |
| Any hooked role can research public https; private URLs and credentials are denied | `test_guard.py` |
| Only Gandalf starts workers, with an explicit custom or built-in `agent_type`. Missing types and recursive Gandalf runs are denied | `test_guard.py` |
| Freeform patches check every file and move target for secrets and protected configuration | `test_guard.py`; `../scripts/test_install_agents.py` |
| Installation copies stay unchanged when the source checkout changes | `../scripts/test_install_agents.py` |
| Line breaks, backticks, `$(...)` and process substitution are split into parts and each part is checked; heredocs fall back to a word check | `test_guard.py` |
| Calls without a `session_id` denied | `test_guard.py` |

Run the proof: `python3 guard/test_guard.py` and
`python3 scripts/test_install_agents.py`.

## What is not enforced

- Roles can edit anywhere, run any git or `gh` command except merge, and use the
  shell. Plan-first roles (plan mode) are a prompt convention, not enforced.
- The shell check is a tripwire, not a sandbox. `bash -c`, `eval` and `xargs`
  are unwrapped, but variables (`F=--force; git push $F`), interpreters
  (`python3 -c`), a file a role wrote and string obfuscation can still slip
  past it. The state files in the system temp directory can be removed with a
  broad glob such as `rm -rf /tmp/g*`; move them out of reach if that matters.
- Role prompts, `ground-rules` and the ask-first rules are advisory.
- Built-ins lack custom role hooks. Gandalf supplies their safety brief and
  supervises them; the guard does not enforce their calls.
- Workers may exchange task-relevant messages. Assigned collaborators, reporting
  to Gandalf and staying within the approved plan are brief rules, not hook checks.
- A hook that times out fails open, so the guard stays fast.
- Each role is denied after 500 tool calls in one session, to stop runaway
  loops. When Themis says to raise it, Gandalf runs
  `python3 ~/.copilot/guard/guard.py --set-limit 2000` (3 to 6 digits, never
  below 500, at most 100000). That command is a real approval prompt for Gandalf and
  denied for roles, as is any other touch of `gandalf-guard/`. The raise lasts
  until the state files are a day old. Whether subagents share the parent's session is unverified, so several
  instances of one role may share one count. Counter files live under the system
  temp directory and are pruned after a day.
- Tool names are matched case-insensitively. A tool the guard does not know,
  including every MCP tool, is allowed, and Copilot's normal permission flow decides.
- Roles reading Copilot's token and settings files are denied by design.
- In non-interactive `-p` runs, an `ask` has no one to answer it.
- Whether your organisation has its own policy is unknown.
- Copilot's command sandboxing is not used yet and could be a stronger layer.

## Later

Review cost and premium-request use of multi-agent runs. -->
