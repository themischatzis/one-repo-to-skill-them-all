---
name: external-skills
description: List Themis's external AI skills and explain how to install or update them. Use when asked which third-party skills or plugins he uses, or how to recreate that setup.
---

# External skills

Read [README.md](README.md) in this directory for the recorded collection,
its upstream source, installation commands, and verification steps.

- For a list or installation question, explain the setup without changing it.
- If asked about the current laptop, run `copilot plugin list`,
  `copilot plugin marketplace list`, and `copilot skill list`. Distinguish the
  live inventory from the recorded snapshot.
- Separate external plugin skills, this repository's personal skills, and
  Copilot's built-in skills. An available skill is not evidence of frequent use.
- Before installing or updating, check `copilot plugin --help` and the
  upstream installation guide for current syntax. Review the source and any
  hooks or permissions; plugins can run code, not just supply Markdown.
- Install or update only when explicitly requested. Do not copy upstream
  skill contents into this repository or overwrite existing personal skills.
- Verify requested changes with the plugin and skill lists. If interactive
  reload or a new session is needed, say so. Do not claim a fresh installation
  was tested when only the documentation or existing setup was checked.
- Never publish local paths containing usernames, private repository sources,
  configuration dumps, credentials, or organisation-specific information.
