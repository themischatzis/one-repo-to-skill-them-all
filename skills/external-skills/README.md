# The borrowed fellowship

Not every member of the company was forged here. Some wandered in from
elsewhere with a ponytail and strong opinions about your abstraction layer.

## Recorded external collection

Observed on 2026-11-03 through Copilot's plugin and skill lists.

**Plugin:** `ponytail@ponytail` from
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail).

| Skill | Why it is here |
|---|---|
| `ponytail` | Keep implementation small and focused on what was actually asked. |
| `ponytail-review` | Review a particular change for meaningful problems. |
| `ponytail-audit` | Inspect a whole repository without changing it. |
| `ponytail-debt` | Find the shortcuts deliberately left for later. |
| `ponytail-gain` | Show the plugin's benchmark savings report. |
| `ponytail-help` | Explain the plugin's modes and commands. |

These are installed and available, not a claim that every skill is used daily.
The installed collection is documented, not vendored: upstream owns its code,
instructions, and licensing.

## Install on another laptop

Prerequisite: an installed, signed-in GitHub Copilot CLI. Review the upstream
[installation guide](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md)
and plugin hooks before granting trust. Hooks may require Node.js on `PATH`.

Run these in your terminal:

```sh
copilot plugin marketplace add DietrichGebert/ponytail
copilot plugin install ponytail@ponytail
```

Check `copilot plugin marketplace list` and `copilot plugin list` first; skip
steps already completed. Do not add a second copy of the same skills manually.
The marketplace is named `ponytail`; it is not the built-in `awesome-copilot`
marketplace.

## Check and update

```sh
copilot plugin list
copilot skill list
```

Inside an interactive Copilot session, run `/skills reload`. The upstream
Copilot guide documents namespaced commands such as
`/ponytail:ponytail-review`; use the command shown by your installed version.

When you actually want an upstream update, check
`copilot plugin update --help`, then run:

```sh
copilot plugin update ponytail@ponytail
```

Review upstream changes before updating; this guide does not pin a version.

## Not external installs (forged in this repository)

`create-jira-bug`, `external-skills`, and `mcp-servers` are this repository's
personal skills. Their installation is covered in the
[top-level README](../../README.md#equip-your-skills).

`customize-cloud-agent` and `github-pr-media` were supplied by Copilot itself
in the observed setup; there is no separate plugin to install for them.
Built-in availability can change between Copilot versions.

Source for CLI commands:
[Copilot plugin installation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing).
