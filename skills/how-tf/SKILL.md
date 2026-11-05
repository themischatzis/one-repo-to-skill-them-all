---
name: how-tf
description: Explain how a subsystem, feature or code path works, or where something should live, before changing it. Use for "how does X work", walkthroughs, onboarding, and placement/ownership questions. Read-only.
---

# How tf

Produce the explanation a senior engineer would give to someone onboarding:
enough for a working mental model, not annotated source. Read-only.

## 1. Size it

State your interpretation of the question and go; the user can redirect.

- **Simple** (one module or function): read it yourself and explain.
- **Complex** (a subsystem, cross-cutting feature, several services): split
  into 2-4 distinct angles and launch one `explore` subagent per angle in
  parallel, each with its angle, the goal, and a request for cited
  `file:line` findings. Then synthesise yourself.

When in doubt, take the simple path.

## 2. Explain

Use only the sections that apply:

- **Overview**: what it is and why it exists, two or three sentences.
- **Key concepts**: the vocabulary and core types.
- **How it works**: runtime flow, in order.
- **Where things live**: files and owners, each with a path.
- **Gotchas**: surprises, hidden coupling, things that break when you change it.

Every claim cites a real `file:line`. Never invent a caller or API. If an
explorer's claim looks off, check it before repeating it.

## Hand back

The explanation. If it precedes a change, name the likely owner and place for
the change, then hand over to `bug-hunt` or `ticket-quest`.
