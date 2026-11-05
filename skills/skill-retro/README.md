# The palantír log

Journals how you work and, a week later, reviews every skill against it plus
your past Copilot sessions: keep, change, delete, add. Unlike the real
palantíri, it only shows true things and does not lure you to Mordor.
The [skill instructions](SKILL.md) have the detail.

## Reflect, Mirror and Trial

- **Reflect**: say "reflect" after a session that taught something. Three
  read-only reviewers (judgment, tooling, divergent) via
  [divide-and-conquer](../divide-and-conquer/README.md) feed an Accepted,
  Rejected and Backlog list, and nothing is edited until you approve. Backlog
  items go to [never-again](../never-again/README.md).
- **Mirror**: say "what are my patterns" for a monthly look in the water. It
  mines the journal and sessions, asks which patterns are really you, and only
  then proposes edits to [ground-rules](../ground-rules/README.md).
- **Trial**: after a big skill edit or an adopted skill, it offers
  [trial-by-fire](../trial-by-fire/README.md) before you keep it.

## Setup

Notes live in a separate **private** repo so they follow you across laptops
and stay out of this public one. The journal is split so a review stays cheap:
`inbox.md` (unreviewed, the only file read by default), `ideas.md` (undecided),
`rejected.md` (decided no, searched before proposing), `reviewed/YYYY-MM.md`
(applied or kept) and `sessions/` (daily auto-log). After each review, inbox
lines are filed into the right place.

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
