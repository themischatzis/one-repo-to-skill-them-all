# One Repo to Skill Them All

One developer. Several AI assistants. A suspicious number of repetitive tasks.

Welcome to Themis's personal collection of AI skills: reusable instructions that
turn "please do the thing" into something slightly more reliable than a wizard
arriving precisely when production goes down.

No rings, no prophecies, no framework. Just Markdown with a purpose.

## The fellowship

| Skill | Its quest |
|---|---|
| [babysit-pr](skills/babysit-pr/README.md) | Watch a PR through conflicts, reviews and CI until merge-ready. |
| [bug-hunt](skills/bug-hunt/README.md) | Reproduce, root-cause, test-first fix and verify a bug. |
| [catch-me-up](skills/catch-me-up/README.md) | Plain-words catch-up: what changed and what waits on you. |
| [compare-designs](skills/compare-designs/README.md) | Competing attempts, judged blind, best parts merged (opt-in). |
| [create-jira-bug](skills/create-jira-bug/README.md) | Turn "it's broken" into a useful Jira bug, with context, impact, reproduction steps, and expected behaviour. |
| [divide-and-conquer](skills/divide-and-conquer/README.md) | Parallel subagents over independent slices (opt-in). |
| [external-skills](skills/external-skills/README.md) | Remember which skills were borrowed, where they came from, and how to invite them back. |
| [figure-it-out](skills/figure-it-out/README.md) | Design a playbook for large or unusual work. |
| [ground-rules](skills/ground-rules/README.md) | The shared principles every playbook reads first. |
| [how-tf](skills/how-tf/README.md) | Cited explanations of how code works. |
| [mcp-servers](skills/mcp-servers/README.md) | Reconnect the palantirs: MCP servers, authentication, and setup instructions. |
| [never-again](skills/never-again/README.md) | Turn repeated corrections into guards. |
| [pr-forge](skills/pr-forge/README.md) | Small ordered commits and a briefing-style PR, with your naming rules. |
| [review-change](skills/review-change/README.md) | Review a PR, branch or diff against its intent, with proven findings. |
| [skill-retro](skills/skill-retro/README.md) | Journal how you work, reflect on sessions and review the skills against it. |
| [tdd-bug-fix](skills/tdd-bug-fix/README.md) | Fix bugs test-first when the test is cheap. |
| [tear-it-apart](skills/tear-it-apart/README.md) | Adversarial review where only run-proven findings survive. |
| [ticket-quest](skills/ticket-quest/README.md) | Deliver a Jira ticket in small verified units. |
| [trial-by-fire](skills/trial-by-fire/README.md) | Blind test of a skill change. |
| [try-harder](skills/try-harder/README.md) | Make a vague task deeper before work starts. |
| [unslop](skills/unslop/README.md) | Plain prose for PRs, Jira, READMEs and skills, minus AI tells. |
| [untangle-this](skills/untangle-this/README.md) | Rebase a branch and resolve conflicts safely and repeatably. |
| [what-could-go-wrong](skills/what-could-go-wrong/README.md) | Find what a change breaks elsewhere and prove the key safety fact. |
| [what-were-you-thinking](skills/what-were-you-thinking/README.md) | A decision log for long or unattended runs. |
| [where-was-i](skills/where-was-i/README.md) | Pause cleanly, pick up a session, recall where you left off. |
| [who-did-this](skills/who-did-this/README.md) | History and intent behind the code. |

### Agents

| Agent | Its quest |
|---|---|
| [gandalf](agents/gandalf/README.md) | The orchestrator: plans, asks, then runs the roles under guard. |
| [gollum](agents/gollum/README.md) | Hates unnecessary comments with his whole heart. |
| [sam](agents/sam/README.md) | A loyal delegate that carries the edits. |

Gandalf's roles live in [roles/](roles/README.md) and are the team he starts (each guarded
by the [guard](guard/README.md)):
[adversary](roles/adversary/README.md), [analyst](roles/analyst/README.md),
[architect](roles/architect/README.md), [backend](roles/backend/README.md),
[ci-fixer](roles/ci-fixer/README.md), [devops](roles/devops/README.md),
[docs](roles/docs/README.md), [frontend](roles/frontend/README.md),
[manager](roles/manager/README.md), [ml-engineer](roles/ml-engineer/README.md),
[prompt-engineer](roles/prompt-engineer/README.md), [qa](roles/qa/README.md),
[resolver](roles/resolver/README.md), [retrieval](roles/retrieval/README.md),
[reviewer](roles/reviewer/README.md), [security](roles/security/README.md),
[visionary](roles/visionary/README.md), [vp](roles/vp/README.md).

Run `/agent` to confirm they are listed.

Rebuilding the laptop? Start with the
[external skills guide](skills/external-skills/README.md) and
[MCP setup guide](skills/mcp-servers/README.md). These record the observed setup,
not a bag of credentials or a promise to install anything automatically.

## Equip your skills

Clone this repo somewhere permanent, then link the skill into Copilot's personal
skills directory. Edits in the repo will immediately reach the linked skill.

```sh
git clone https://github.com/themischatzis/one-repo-to-skill-them-all.git
cd one-repo-to-skill-them-all
mkdir -p "$HOME/.copilot/skills"
for s in skills/*/; do
  n=$(basename "$s")
  [ -e "$HOME/.copilot/skills/$n" ] || ln -s "$PWD/skills/$n" "$HOME/.copilot/skills/$n"
done

mkdir -p "$HOME/.copilot/agents"
for a in agents/*/*.agent.md roles/*/*.agent.md; do
  n=$(basename "$a")
  [ -e "$HOME/.copilot/agents/$n" ] || ln -s "$PWD/$a" "$HOME/.copilot/agents/$n"
done
```

Gandalf, his roles, `sam` and `gollum` all need the [guard](guard/README.md). Read
`guard/guard.py`, then link it:

```sh
[ -e "$HOME/.copilot/guard" ] || ln -s "$PWD/guard" "$HOME/.copilot/guard"
```

For parallel work, [scripts](scripts/README.md) has a worktree helper.

Then link the always-on routing file, so Copilot picks the right skill or agent
from a plain request in every repo. It only links if none exists yet; if you
already have a `~/.copilot/copilot-instructions.md`, merge by hand.

```sh
[ -e "$HOME/.copilot/copilot-instructions.md" ] || \
  ln -s "$PWD/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
```

If that destination already exists, inspect it first; don't overwrite your
existing fellowship. Repeat the link step for any future skills you want to use.

In Copilot CLI, run `/skills reload`, then `/skills info create-jira-bug`.
Personal skills are shared across your projects, not copied into each repo.

## Send it on a quest

Choose your companion from [the fellowship](#the-fellowship), then read its
`skills/<skill-name>/README.md`. That is the map for humans: what it does,
what it needs, and how to get it moving. The neighbouring `SKILL.md` is the
wizard's instruction manual. Please do not swap them; the wizard is confused
enough already.

Ask Copilot to use the skill by name and describe your quest. Skills can load
when your request matches their description; an explicit name saves everyone
a meeting at Rivendell.

Some companions need local configuration, a connected service, or answers
before setting off. Their own READMEs explain the particulars. Keep secrets
on your laptop, read permission prompts, and remember: installing a skill is
not the same as authenticating a service. Even Gandalf needs to sign in.

## Contributing to the fellowship

Add a folder under `skills/` containing a `SKILL.md` with `name` and `description`
frontmatter, plus a `README.md` for usage and skill-specific setup. Link that
README from the fellowship table. Keep it small, useful, and free of private
information.

Commit and PR titles use `feat: Capitalized title`, for example
`feat: Add Jira bug reporting skill`. No ticket prefixes: this is a personal
repo, not the Council of Mandatory Tracking Numbers.

## Inspired by

[Bernstein](https://github.com/sipyourdrink-ltd/bernstein) and [pstack](https://github.com/cursor/plugins/tree/main/pstack).
