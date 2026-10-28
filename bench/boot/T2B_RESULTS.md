# T2b results: thinking and Haiku's empty answers

Independently audited: `T2B_AUDIT.md` (data, grades and costs hold; two claims corrected below).

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
- **Default for resident runs on Haiku:** disabled, as a direction to
  taste, not a pre-registered decision (12/12 against 10/12 is two passes,
  which the pre-registration itself says is not evidence).
  The rule was to choose between D and E, and E could not run (below), so
  the choice here is D against T2's default, outside the pre-registered
  rule.
- As fixed in advance, 12 tasks with one attempt each show a direction,
  not a result. 12/12 against 10/12 is consistent with T2's failures
  being output spent on thinking rather than wrong code, but does not
  prove it.

## Deviation: arm E could not run

The API refused `thinking: {"type": "enabled", "budget_tokens": 2048}`
for Claude Haiku 5.5: "not supported for this model. Use
`thinking.type.adaptive` and `output_config.effort`." The door allows
`thinking` but not `output_config`, so adaptive thinking with an effort
level cannot pass it today. The one arm-E request was refused and not charged; its refusal text is
recorded here, not in the raw data. Testing it
needs a door change (allow `output_config.effort`, still capped).

## What it means for the architecture

- A resident's run should set its thinking explicitly. Leaving it to the
  model's default spent the whole output budget on thinking on hard tasks
  and returned nothing.
- With thinking off, Haiku passed all 12 hard tasks at about **$0.0005**
  per task. The 12 easy tasks also passed in T2 arm B, but with the
  model's default thinking, not with thinking off. *(Corrected after the
  audit: the first draft claimed all 24 with thinking off, and $0.0006.)*
- The mechanism (output spent on thinking) is inferred from T11 and the D
  contrast; T2 did not log thinking tokens, and one attempt per task cannot
  rule out chance.
- *Hypothesis, not tested here:* the cascade in T2 escalated mostly
  because of these empties, so with thinking off Haiku alone may be enough
  for work of this kind, with Sonnet the exception rather than the
  backstop.
