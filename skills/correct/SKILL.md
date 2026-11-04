---
name: correct
description: Turn repeated agent or reviewer corrections in a repo into structural guards. Use when told the same mistake keeps happening, after being corrected twice for the same thing, or when asked to make a mistake impossible.
---

# Correct

Change the repo so the next contributor can't repeat the mistake.

Assume every contributor only sees the files it opened and copies the nearest
example. Make a change that looks right from one file right for the whole repo.

## Find the classes

Read recent commits, reverts, review comments, agent instruction files and
workaround comments. Group mistakes; a class counts once it happened twice.

## Fix at the highest level that works

1. **Architecture**: one owner per piece of state, hide internals so the wrong
   import fails, delete old paths an agent would copy.
2. **Types**, then a lint/CI check whose error names the thing to use instead.
3. **Tests** of behaviour, not internals.
4. **Docs or agent rules last**, only for judgment calls. Nothing fails when
   they are skipped.

## Prove it

Show each new check fails on a real past mistake. Run the same command locally
and in CI. Ask before landing any fix; keep one small change per class.

## Rule table

Keep a table in `AGENTS.md` pairing each rule with what enforces it. A rule
with no enforcer is a repeat: fix it at a higher level.

## Reply

Each class with evidence, the level chosen, and why a higher one didn't work.
