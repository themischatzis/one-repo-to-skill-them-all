---
name: what-were-you-thinking
description: Keep a TSV decision log for long, autopilot or multi-phase work Themis reviews later. Use for "what were you thinking", "red book", "keep a decision log", "I'm going to bed".
---

# What were you thinking?

Bilbo wrote down what happened so others could read it later. Keep one log per
run, one row per decision, so he can audit the run without replaying it.

## Format

TSV, single-line cells, evidence is a pointer not prose. Columns:
`ts, phase, decision, why, evidence, result`.

- **decision**: what was chosen or done, one line.
- **why**: plain words, as you would tell a teammate.
- **evidence**: commit SHA, PR number, `file:line` or artifact path.
- **result**: `tests green`, `reverted`, `INCONCLUSIVE`, `open`.

Log forks chosen, units finished with their verification, pivots and reverts
with their trigger, blockers, and gates fixed. In a loop, one row per
iteration. Skip the trivial.

## Use

- Start the log with `scripts/log.sh <logfile> <phase> <decision> <why>
  <evidence> <result>`. It stamps the time, writes the header on first use and
  strips tabs and newlines. Default file: `/tmp/<task-slug>-decisions.tsv`.
- Keep it outside the repo. Commit it only if he asks.
- Rows are honest: never hide a negative result, never log a guess as a fact.
- `figure-it-out` points here for its decision log. `where-was-i` points at
  it from the resume note instead of duplicating it.
- At the end, summarise the log in the reply: decisions, reverts, open items.
  He reads that, then the TSV only if something looks off.
