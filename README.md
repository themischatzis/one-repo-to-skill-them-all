# One Repo to Skill Them All

One developer. Several AI assistants. A suspicious number of repetitive tasks.

Welcome to Themis's personal collection of AI skills: reusable instructions that
turn "please do the thing" into something slightly more reliable than a wizard
arriving precisely when production goes down.

No rings, no prophecies, no framework. Just Markdown with a purpose.

## The fellowship

| Skill | Its quest |
|---|---|
| [create-jira-bug](skills/create-jira-bug/README.md) | Turn "it's broken" into a useful Jira bug, with context, impact, reproduction steps, and expected behaviour. |
| [external-skills](skills/external-skills/README.md) | Remember which skills were borrowed, where they came from, and how to invite them back. |
| [mcp-servers](skills/mcp-servers/README.md) | Reconnect the palantirs: MCP servers, authentication, and setup instructions. |
| [ground-rules](skills/ground-rules/README.md) | The shared principles every playbook reads first. |
| [bug-hunt](skills/bug-hunt/README.md) | Reproduce, root-cause, test-first fix and verify a bug. |
| [ticket-quest](skills/ticket-quest/README.md) | Deliver a Jira ticket in small verified units. |
| [how-does-it-work](skills/how-does-it-work/README.md) | Cited explanations of how code works. |
| [why-is-it-like-this](skills/why-is-it-like-this/README.md) | History and intent behind the code. |
| [review-change](skills/review-change/README.md) | Review a PR, branch or diff against its intent, with proven findings. |
| [rebase-conflicts](skills/rebase-conflicts/README.md) | Rebase a branch and resolve conflicts safely and repeatably. |
| [interrogate](skills/interrogate/README.md) | Adversarial review where only run-proven findings survive. |
| [figure-it-out](skills/figure-it-out/README.md) | Design a playbook for large or unusual work. |
| [tdd-bug-fix](skills/tdd-bug-fix/README.md) | Fix bugs test-first when the test is cheap. |
| [blast-radius](skills/blast-radius/README.md) | Find what a change breaks elsewhere and prove the key safety fact. |
| [correct](skills/correct/README.md) | Turn repeated corrections into guards. |
| [skill-retro](skills/skill-retro/README.md) | Journal how you work and review the skills against it. |

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
