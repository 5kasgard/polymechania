# T2b results: thinking and Haiku's empty answers

Run 2026-10-29 under `prereg/t2b-thinking.md` (committed before running;
`self.md` and `packet.txt` hashes checked). Raw data: `t2b_results.json`;
code: `solutions/haiku/D/`. Cost: **$0.006**.

| Haiku 5.5, 12 hard tasks, arm B form | Pass | Empty answers | $ | Thinking tokens |
|---|---|---|---|---|
| T2 arm B (no `thinking` field: the model's default) | 10/12 | 2 | $0.0126 | not logged |
| **D: thinking disabled** | **12/12** | **0** | **$0.0060** | 0 |
| E: thinking enabled, budget 2,048 | not run | | | |

## Decisions, as pre-registered

- **Thinking caused the empties:** holds. T2's default had two empty
  answers on these tasks (regex, approx); with thinking disabled there
  were none, and both passed.
- **Default for resident runs on Haiku:** **disabled**, on this evidence.
  The rule was to choose between D and E, and E could not run (below), so
  the choice here is D against T2's default, not against a capped budget.
- As fixed in advance, 12 tasks with one attempt each show a direction,
  not a result. Still, 12/12 against 10/12 is consistent with T2: Haiku's
  failures there were output spent on thinking, not wrong code.

## Deviation: arm E could not run

The API refused `thinking: {"type": "enabled", "budget_tokens": 2048}`
for Claude Haiku 5.5: "not supported for this model. Use
`thinking.type.adaptive` and `output_config.effort`." The door allows
`thinking` but not `output_config`, so adaptive thinking with an effort
level cannot pass it today. No arm-E call was made or charged. Testing it
needs a door change (allow `output_config.effort`, still capped).

## What it means for the architecture

- A resident's run should set its thinking explicitly. Leaving it to the
  model's default spent the whole output budget on thinking on hard tasks
  and returned nothing.
- With thinking off, the thin boot's Haiku runs passed every one of the
  pilot's 24 tasks across T2 (easy, arm B) and T2b (hard): one attempt
  each, at about $0.0006 per hard task.
- The cascade in T2 escalated mostly because of these empties; with
  thinking off, Haiku alone may be enough for work of this kind, and
  Sonnet would be the exception, not the backstop.
