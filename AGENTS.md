# Repository instructions

- This is a personal collection of AI skills. Keep changes small and readable.
- Put each skill in `skills/<lowercase-hyphenated-name>/SKILL.md`, with matching
  `name` and a description explaining when to use it.
- Put human-facing usage and skill-specific setup in that skill's `README.md`.
  Keep the top-level README generic and link to each skill's README.
- Keep every `SKILL.md` and agent file plain and token-light, descriptions
  included. Put the LOTR humour and theme in that folder's `README.md` only.
- Custom agents go in `agents/<name>/<name>.agent.md` with a `README.md` beside
  them, like skills. Keep the `description` short and plain; jokes and theme
  belong in the README only.
- Agents you start yourself go in `agents/`. Roles that Gandalf starts as his
  team go in `roles/<name>/<name>.agent.md` with a `README.md`. Every agent and
  role needs a guard hook and its name in `ROLES` in `guard/guard.py`. Do not
  add a `tools:` line; agents get every tool, MCP included.
- Role files keep one fixed layout: Specialization, Work style, Rules. The guard
  and report rules live inside Rules.
- Every new, renamed or removed skill or agent needs a row change in the
  routing table in `copilot-instructions.md`; that file is how plain requests
  reach the right skill.
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

| Rule | Enforcer |
|---|---|
| Agents omit tool allowlists and keep matching guard hooks | `scripts/install-agents.py`; `scripts/test_install_agents.py` |
| Only Gandalf spawns workers, with explicit agent types and no recursive orchestration | `guard/guard.py`; `guard/test_guard.py` |
| Specialist selection, peer collaboration and built-in supervision | Advisory: Gandalf's briefs and oversight; built-ins do not have role hooks |
| Branch changes cannot revert installed agents, guard or routing | `scripts/install-agents.py`; `scripts/test_install_agents.py` |
