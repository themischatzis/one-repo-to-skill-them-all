# One Repo to Skill Them All

One developer. Several AI assistants. A suspicious number of repetitive tasks.

Welcome to Themis's personal collection of AI skills: reusable instructions that
turn "please do the thing" into something slightly more reliable than a wizard
arriving precisely when production goes down.

No rings, no prophecies, no framework. Just Markdown with a purpose.

## The fellowship

| Skill | Its quest |
|---|---|
| [create-jira-bug](skills/create-jira-bug/SKILL.md) | Turn "it's broken" into a useful Jira bug, with context, impact, reproduction steps, and expected behaviour. |

## Equip your skills

Clone this repo somewhere permanent, then link the skill into Copilot's personal
skills directory. Edits in the repo will immediately reach the linked skill.

```sh
git clone https://github.com/themischatzis/one-repo-to-skill-them-all.git
cd one-repo-to-skill-them-all
mkdir -p "$HOME/.copilot/skills"
ln -s "$PWD/skills/create-jira-bug" "$HOME/.copilot/skills/create-jira-bug"
```

If that destination already exists, inspect it first; don't overwrite your
existing fellowship. Repeat the link step for any future skills you want to use.

In Copilot CLI, run `/skills reload`, then `/skills info create-jira-bug`.
Personal skills are shared across your projects, not copied into each repo.

## Keep Mordor's address private

The Jira skill uses `JIRA_BOARD`. The real board URL belongs on your laptop,
not in this public repo.

```sh
mkdir -p "$HOME/.config/one-repo-to-skill-them-all"
cp .env.example "$HOME/.config/one-repo-to-skill-them-all/env"
chmod 600 "$HOME/.config/one-repo-to-skill-them-all/env"
```

Edit that local file to set your board URL. Load it before starting Copilot:

```sh
source "$HOME/.config/one-repo-to-skill-them-all/env"
```

For future login shells, add this once to `~/.zprofile`:

```sh
if [ -f "$HOME/.config/one-repo-to-skill-them-all/env" ]; then
  . "$HOME/.config/one-repo-to-skill-them-all/env"
fi
```

The skill can also load that exact local file when `JIRA_BOARD` isn't inherited.
Jira access comes from your authenticated Atlassian tools; this file is not a
place for API tokens. Never commit real board URLs, credentials, or company data.

## Send it on a quest

Ask Copilot:

> Use create-jira-bug: this page returns 200 when it should redirect. Here are the reproduction steps...

The skill uses your bug-report format and creates a **Bug**, not an epic saga.
It won't invent browser coverage, customer impact, or the correct URL.

You can also invoke `/create-jira-bug` without arguments. It will ask for the
bug details, brand, affected browsers/devices, and epic/parent, plus the
environment if Jira requires it and the report doesn't establish it.
Nothing is created until you supply the missing answers. No answering on your
behalf, even if the wizard is temporarily unavailable.

## Contributing to the fellowship

Add a folder under `skills/` containing a `SKILL.md` with `name` and `description`
frontmatter. Keep it small, useful, and free of private information.

Commit and PR titles use `feat: Capitalized title`, for example
`feat: Add Jira bug reporting skill`. No ticket prefixes: this is a personal
repo, not the Council of Mandatory Tracking Numbers.
