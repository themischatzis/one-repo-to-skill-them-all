# The palantir connections

Skills tell the assistant how to do a quest. MCP servers let it reach the
outside world. Neither is permission to summon tickets without asking.

## Recorded setup

Observed on 2026-11-03 using Copilot's MCP list and this session's available
integrations. Endpoints below are public provider addresses, not account URLs.

| Name | Source | Purpose | Setup |
|---|---|---|---|
| `atlassian` | Personal HTTP server | Jira and Confluence tools | Configure the remote endpoint and authenticate. |
| `figma` | Personal HTTP server | Design context and Figma tools | Configure the remote endpoint and authenticate. |
| `github-mcp-server` | Built into Copilot CLI | GitHub context and operations | No separate MCP installation. |
| `ide` | VS Code connection in this session | Editor selection and diagnostics | Connect the editor with `/ide`; not a personal MCP entry. |

Only Atlassian and Figma are manually configured in the recorded personal
setup. This inventory does not imply access to every service or tool on a new
machine. Organisation policy, account permissions, and subscriptions still apply.

## Install the two remote servers

Prerequisite: an installed, signed-in GitHub Copilot CLI.

First check for existing entries:

```sh
copilot mcp list
```

On a new setup, run:

```sh
copilot mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
copilot mcp add --transport http figma https://mcp.figma.com/mcp
```

These commands recreate the recorded endpoints in
`~/.copilot/mcp-config.json`. Skip existing entries; do not overwrite the whole
file. No Docker container, npm server, or copied access token is needed for
this remote setup.

**Atlassian version note:** the recorded setup uses `/v1/mcp`. Atlassian's
current [official setup guide](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)
now recommends `/v2/mcp`. For a new installation, review that guide and choose
the desired version explicitly; use `https://mcp.atlassian.com/v2/mcp` in the
command if choosing v2. Do not silently migrate an existing v1 connection.

## Authenticate and verify

1. Start Copilot and open `/mcp`.
2. Select the server and follow its authentication prompts in the browser.
   Sign in to the intended Atlassian or Figma account and review access.
3. Check `/mcp` again for connection status and available tools.

`copilot mcp list` confirms configuration, not successful authentication.
Do not create a real Jira issue or Figma document as a connection test.

Figma's remote server does not require the desktop app. Client support and
account/tool limits are controlled by Figma; see the
[official remote setup guide](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/).
If your client or organisation is blocked, adding the URL alone won't fix it.

## GitHub and the editor

The GitHub MCP server comes with Copilot CLI. Use the normal Copilot sign-in
flow and confirm availability in `/mcp`; don't install a second GitHub server
or generate a PAT just to reproduce this setup. GitHub CLI (`gh`) is a separate
tool, not this MCP server.

For editor tools, open the intended workspace in VS Code and use `/ide` in
Copilot CLI to connect. This is a session integration, not another remote URL
to put in `mcp-config.json`.

## Keep the secrets out of the Shire

Never commit a copy of your real MCP configuration or OAuth cache.
Authentication headers, tokens, private endpoints, tenant URLs, and
organisation-specific settings stay local. `JIRA_BOARD` is separate local
configuration for the bug skill; it does not install or authenticate MCP.

Official CLI reference:
[Adding MCP servers](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).
