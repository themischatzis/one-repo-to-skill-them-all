# One failing test to rule them all

Fix a bug test-first, but only when the test is cheap. If it would need a
Mordor-sized harness, the skill falls back to the closest quick check.
The [skill instructions](SKILL.md) work well after
[create-jira-bug](../create-jira-bug/README.md): the ticket's repro steps become
the failing test.

Install it with the [repository setup guide](../../README.md#equip-your-skills).
