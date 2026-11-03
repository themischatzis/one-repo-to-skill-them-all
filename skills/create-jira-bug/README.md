# A bug's unexpected journey

Turn "it's broken" into a useful Jira **Bug**, not an epic saga.
The [skill instructions](SKILL.md) keep the report structured and stop the
assistant from inventing facts to fill the parchment.

## Before setting off

Install this personal skill using the
[repository setup guide](../../README.md#equip-your-skills), then connect and
authenticate [Atlassian MCP](../mcp-servers/README.md). Local configuration
selects the board; it does not grant Jira access.

## Keep Mordor's address private

The skill uses `JIRA_BOARD`. The real board URL belongs on your laptop,
not in this public repo.

From the repository root, on first setup:

```sh
mkdir -p "$HOME/.config/one-repo-to-skill-them-all"
cp .env.example "$HOME/.config/one-repo-to-skill-them-all/env"
chmod 600 "$HOME/.config/one-repo-to-skill-them-all/env"
```

Skip the copy if that local file already exists; don't overwrite your settings.
Edit it to set your board URL. Load it before starting Copilot:

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

## Send the bug on its quest

Ask Copilot:

> Use create-jira-bug: this page returns 200 when it should redirect. Here are the reproduction steps...

Or invoke `/create-jira-bug` without arguments. It asks for missing information
before creating anything:

- Actual behaviour: what happens.
- Expected behaviour: what should happen.
- Brand.
- Affected browsers/devices.
- Epic/parent issue key or URL.
- Environment, if Jira requires it and the report does not establish it.

Already supplied answers are not requested again. Missing or unclear actual or
expected behaviour blocks creation, even when every Jira field is known.
No answering on your behalf if you are unavailable, and no guessing browser
coverage, customer impact, or the correct URL.

An explicit "N/A" for browsers/devices or "No parent" is accepted only when Jira
allows it. Some workflows require an Epic Link even if field metadata doesn't
say so; the skill asks rather than borrowing an unrelated epic.

## What lands in Jira

The description uses these sections, in order: **Background**, **Impact**,
**Steps to reproduce**, **Actual Result**, **Expected Result**, and
**Screenshots / Videos**. Background includes the affected link, OS, and browser.

WordPress bugs use `WP: <Title>`; nb-phoenix or talkSPORT bugs use `TS: <Title>`,
unless you supply an exact title or another prefix.

After creation, the skill reads the issue back and returns its key and link.
It reports any unverified board membership rather than promising a ticket is
visible on a filtered board. It never creates a real issue merely to test
connectivity.
