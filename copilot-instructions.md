# Themis's routing

Applies in every repo and mode. He talks, you pick the skill or agent.
Questions ("how", "why", "is this safe", "review this") are triggers too.
Read `ground-rules` before any non-trivial coding task.

Open the reply with one line: skill or agent picked and why. Skip heavy skills
for trivial changes and say so. If two fit, first match wins: Jira key or URL,
PR number or URL, explicit words, then topic.

| Request | Use |
|---|---|
| Bug, broken, Jira Bug | `bug-hunt` (test-first: `tdd-bug-fix`) |
| Other ticket or feature | `ticket-quest` |
| File a Jira bug | `create-jira-bug` |
| How or where does X work | `how-tf` |
| Why is it like this, who changed it | `who-did-this` |
| Review a PR, branch or diff | `review-change` |
| Rebase, conflicts, update my branch | `untangle-this` |
| Open PR: green CI, review comments | `babysit-pr` |
| What could this break | `what-could-go-wrong` |
| Stress-test a design or change | `tear-it-apart` |
| Commit, open or write a PR | `pr-forge` |
| Large, unusual or unattended work | `figure-it-out` (log: `what-were-you-thinking`) |
| Same mistake again | `never-again` |
| Catch me up, explain simply | `catch-me-up` |
| Pause, resume, where did I leave off | `where-was-i` |
| Write or tidy prose | `unslop` |
| Vague or shallow task | `try-harder` |
| Note this, reflect, retro | `skill-retro` |
| Did a skill change help | `trial-by-fire` |
| My skills, plugins or MCP setup | `external-skills`, `mcp-servers` |
| Many independent slices (only if asked or clearly wide) | `divide-and-conquer` |
| Competing designs (only if asked) | `compare-designs` |

Agents: edits to `sam`; comment cleanup on a diff to `gollum`. Multi-role work
(plan, then run BE/FE/QA and others under guard) to `gandalf`, who asks before
acting and starts the role agents (adversary, analyst, architect, backend,
ci-fixer, devops, docs, frontend, manager, ml-engineer, prompt-engineer, qa,
resolver, retrieval, reviewer, security, visionary, vp).

Build skills end by offering `pr-forge`. Never merge a PR unless he says so
for that PR. Commits, pushes, PRs and Jira writes are ask-first. Close tasks per `ground-rules`.
