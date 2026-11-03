# Repository instructions

- This is a personal collection of AI skills. Keep changes small and readable.
- Put each skill in `skills/<lowercase-hyphenated-name>/SKILL.md`, with matching
  `name` and a description explaining when to use it.
- Put human-facing usage and skill-specific setup in that skill's `README.md`.
  Keep the top-level README generic and link to each skill's README.
- Use commit and PR titles in the form `feat: Capitalized title`. Do not add
  Jira keys or other ticket prefixes.
- Never publish real Jira board URLs, organisation-specific IDs, customer data,
  credentials, or local configuration. Refer to `JIRA_BOARD` instead.
- Keep personal configuration outside the repo; `.env.example` contains only
  placeholders.
- Keep external skill and MCP inventories in their respective skill READMEs.
  Distinguish observed installs from built-ins and session integrations.
- Verify installation commands against CLI help or official upstream docs.
  Never vendor third-party skills or publish real MCP configuration/auth data.
