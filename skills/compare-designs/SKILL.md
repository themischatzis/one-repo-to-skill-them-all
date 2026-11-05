---
name: compare-designs
description: Run several independent attempts at one task, pick the best base, graft in the best parts of the rest. Use only when asked ("compare designs", "council", "arena this", "compare approaches") or for a contested design.
---

# Compare designs

Several independent attempts, one decision. Costs several subagents: skip it for mechanical or
obvious work. Read `ground-rules`; reuse `divide-and-conquer` for the fan-out.

## Steps

1. **Frame.** Same prompt for every candidate, so the prompt is the contract.
   State the artifact. Write a rubric of 3-6 gradeable criteria for this task;
   keep it from the candidates.
2. **Fan out** 2-4 candidates through `divide-and-conquer`, each in its own worktree
   or `/tmp/council-<slug>/candidate-<n>/`. Ask each for the artifact plus a short
   rationale naming the alternatives it rejected. Different models help when the
   task is judgment-sensitive; same model N times when it is generation-heavy.
   Use the harness's model choices.
3. **Judge.** One independent judge (a `rubber-duck`, ideally a different model
   family) scores the candidates by anonymous label against the rubric. He or
   she never sees which model produced what.
4. **Pick a base**, the best overall candidate.
5. **Graft** the strongest parts of the losers into it, one at a time, only
   where the rubric says they beat the base.
6. **Verify** the merged result on the real artifact, as in `ground-rules`.
7. Read every candidate yourself before trusting the judge. If you and the judge
   disagree, the rubric is ambiguous or someone is biased: say which.

## Reply

Rubric, per-candidate one-liners, the pick and why, what was grafted, the
verification, and the decision he still owns. Log it in the `what-were-you-thinking` log for
long runs.
