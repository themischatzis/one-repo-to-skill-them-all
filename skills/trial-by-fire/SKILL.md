---
name: trial-by-fire
description: Blind-test a skill, prompt or instruction change to see if it really changes agent behaviour. Use for "test this skill change", "did the skill help", "trial by fire", or before adopting a borrowed skill.
---

# Trial by fire

A skill edit affects every future session, so treat it as an experiment.
Reuse `divide-and-conquer` and `compare-designs` mechanics. Read `ground-rules`.

## Blinding rules

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `benchmark`,
  `candidate` or `arena` in any file, directory or prompt a candidate sees.
- The candidate prompt reads like an ordinary request from him: goal, not meta.
- Do not ask which skills or files it used. Grade from the files it actually
  opened (tool calls) and the shape of the result, not its self-report.
- Plain, project-shaped directory names. Do not tell candidates others exist.
- The judge sees outputs by anonymous label, never by model or variant name.

## Steps

1. **Frame.** Name the variant (old skill vs edited skill, or none vs new) and
   the behaviour that counts as success. Write a 3-6 point rubric for the
   judge only.
2. **Set up** a sanitized directory per candidate with its variant in place and
   whatever context an ordinary task would have.
3. **Author one organic prompt** and give the same one to every candidate.
4. **Run** each variant at least twice in parallel through `divide-and-conquer`;
   one run is an anecdote.
5. **Judge** with one blind judge scoring all outputs on one scale.
6. **Read every output yourself** and compare it to the judge. Disagreement
   means a biased judge or an ambiguous rubric.

## Reply

Variant, rubric, per-run notes, verdict, and a recommendation: keep, change or
drop the edit. Log the result in the journal through `skill-retro`.
