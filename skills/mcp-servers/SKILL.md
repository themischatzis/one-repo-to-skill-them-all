---
name: mcp-servers
description: List Themis's MCP servers and explain how to configure and authenticate them in Copilot CLI. Use when asked about his MCP setup, connected services, or recreating those connections.
---

# MCP servers

Read [README.md](README.md) in this directory for the recorded servers,
public endpoints, setup commands, authentication, and verification.

- Explain the setup without modifying it unless installation or changes are
  explicitly requested.
- For the live inventory, use `copilot mcp list`. Distinguish configured
  servers from built-in services and session-only IDE integration.
  Configuration does not prove a server is connected or authenticated.
- Check current `copilot mcp add --help` and official provider instructions
  before configuring a server. Do not silently migrate an existing endpoint
  or add a duplicate server.
- Keep existing local configuration intact. Use named server additions rather
  than replacing `~/.copilot/mcp-config.json` with an example file.
- Use the client's interactive authentication flow; never ask the user to
  paste OAuth tokens into chat, Markdown, commits, or shell history.
- Do not dump MCP config, HTTP headers, environment values, OAuth caches, or
  private endpoints into output. Inspect only the minimum metadata needed,
  and redact sensitive fields before displaying or publishing it.
- After an explicitly requested setup, verify status in `/mcp` and use a
  read-only tool only when authorized. Never create an issue, page, or design
  merely to test connectivity.
- Report authentication, client compatibility, or organisation-policy blockers
  plainly; do not claim a connection works just because configuration saved.
