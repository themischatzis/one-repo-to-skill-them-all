# The palantír log

Journals how you work and, a week later, reviews every skill against it plus
your past Copilot sessions: keep, change, delete, add.
The [skill instructions](SKILL.md) have the detail.

## Setup

Notes live in a separate **private** repo so they follow you across laptops
and stay out of this public one:

```sh
gh repo clone themischatzis/skill-journal "$HOME/Projects/skill-journal"
```

## Daily auto-log

`log-sessions.sh` adds a line per Copilot session (CLI or VS Code, read from the
local session store, so closed tabs are fine) to the journal repo and pushes.
Run it by hand any time. To run it daily at 16:00 local time (UK time on a UK
laptop; a missed run fires on wake):

```sh
sed "s#__SCRIPT__#$PWD/log-sessions.sh#" com.themis.skill-journal.plist \
  > "$HOME/Library/LaunchAgents/com.themis.skill-journal.plist"
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.themis.skill-journal.plist"
```

Remove it with `launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.themis.skill-journal.plist"`.
Errors go to `/tmp/skill-journal.log`. The journal remote must authenticate
without prompts (HTTPS with `gh auth setup-git`).

Use another location by setting `SKILL_JOURNAL_DIR`. Try: "note that I prefer X"
or "run a skill retro". Install the skill with the
[repository setup guide](../../README.md#equip-your-skills).
