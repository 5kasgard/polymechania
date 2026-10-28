# Pre-registration: T2c, effort and capped thinking on Haiku

Written 2026-10-29, before any run. Follows T2b (`bench/boot/T2B_RESULTS.md`),
whose arm E could not run: Claude Haiku 5.5 refuses a fixed thinking
budget and is steered instead by `output_config.effort` with adaptive
thinking. Haiku 5.5's defaults are adaptive thinking at `medium` effort,
with thinking counted against `max_tokens`
([effort docs](https://platform.claude.com/docs/en/build-with-claude/effort)),
which is what T2's arm B ran. Needs the door change that allows `effort`
low, medium or high. Exploratory: one attempt per task.

## Question

Is there a setting that keeps Haiku's thinking but avoids the empty
answers, and does it beat thinking off (T2b arm D) on these tasks?

## Design

- **Tasks, model, form:** as T2b: the pilot's 12 hard tasks, Claude Haiku
  5.5, arm B form (same `self.md` and `packet.txt`, both cached,
  `max_tokens` 4,096), graded after all calls of an arm.
- **Arms (new):**
  - **L:** `thinking: {"type": "adaptive"}`, `output_config: {"effort": "low"}`.
  - **DL:** `thinking: {"type": "disabled"}`, `output_config: {"effort": "low"}`.
- **Compared with (already run, not repeated):** T2 arm B (adaptive,
  medium by default: 10/12, 2 empty, $0.0126) and T2b arm D (disabled,
  medium: 12/12, 0 empty, $0.0060).
- **Logged:** as T2b (thinking tokens, block types, stop reason).

## Decisions, fixed now

- **Low effort avoids the empties** if arm L has no empty answer.
- **Setting for resident runs on Haiku (direction, not result):** among
  L, DL and D, the most passes; ties go to the cheapest in dollars. With
  12 tasks and one attempt, a gap of one or two passes is a direction to
  taste, as in T2b.

## Cost bound

24 calls on Haiku at most 4,096 output tokens each: under $0.06.
