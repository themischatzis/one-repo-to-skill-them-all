# One failing test to rule them all

Fixes a bug test-first, but only when the test is cheap. If it would need a
Mordor-sized harness, it falls back to the closest quick check and says so.
See it fail for the right reason, make the smallest fix, then watch it pass.
Works well after [create-jira-bug](../create-jira-bug/README.md), whose repro
steps become the failing test, and inside [bug-hunt](../bug-hunt/README.md).
The [skill instructions](SKILL.md) have the detail.

Install with the [repository setup guide](../../README.md#equip-your-skills).
