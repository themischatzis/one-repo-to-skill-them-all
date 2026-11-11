# Roles

The fellowship's hands. These are the team [Gandalf](../agents/gandalf/README.md)
plans for and starts as subagents, each with a narrow job and its own
[guard](../guard/README.md) hook.

| Role | Job |
|---|---|
| [adversary](adversary/README.md) | Last pass: finds reasons not to ship. Read-only. |
| [analyst](analyst/README.md) | Judges proposals and researches. Read-only plus web. |
| [architect](architect/README.md) | Structure and tradeoffs. Read-only. |
| [backend](backend/README.md) | Server code: WordPress/PHP (`wp*`), Node, Java. |
| [ci-fixer](ci-fixer/README.md) | Fixes a failing CI job. |
| [devops](devops/README.md) | Build, CI and infra files; never deploys. |
| [docs](docs/README.md) | Documentation; edits Markdown and `docs/` only. |
| [frontend](frontend/README.md) | React and TypeScript. |
| [manager](manager/README.md) | Splits a goal into ordered tasks. Read-only. |
| [ml-engineer](ml-engineer/README.md) | ML and data code. |
| [prompt-engineer](prompt-engineer/README.md) | Prompts, skills and agent instructions. |
| [qa](qa/README.md) | Tests; edits test files only. |
| [resolver](resolver/README.md) | Merge-conflict hunks, by hand. |
| [retrieval](retrieval/README.md) | Finds and cites relevant context. Read-only. |
| [reviewer](reviewer/README.md) | Reviews a change; never edits. |
| [security](security/README.md) | Vulnerabilities and secret leaks; never edits. |
| [visionary](visionary/README.md) | Where the product could go next. Read-only plus web. |
| [vp](vp/README.md) | Cross-piece coordination; approve, reject or escalate. Read-only. |

Each role is `roles/<name>/<name>.agent.md` plus a README. They are ordinary
user-level agents, so `/agent` lists them, but they are meant to be started by
Gandalf. A new role also needs its name in `ROLES` in `guard/guard.py`.

Install with the [repository setup guide](../README.md#equip-your-skills).
