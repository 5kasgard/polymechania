# T2c results: effort and capped thinking on Haiku

Run 2026-10-29 under `prereg/t2c-effort.md` (committed before running;
`self.md` and `packet.txt` hashes checked), after the door change of the
same day (`bench/cards/door/README.md`). Raw data: `t2c_results.json`;
code: `solutions/haiku/L/`, `solutions/haiku/DL/`. Cost: **$0.017**.

Claude Haiku 5.5, the pilot's 12 hard tasks, arm B form (`max_tokens`
4,096, start packet cached), one attempt per task:

| Arm | Thinking | Effort | Pass | Empty | $ | Thinking tokens | Output tokens |
|---|---|---|---|---|---|---|---|
| T2 arm B (default) | adaptive | medium (default) | 10/12 | 2 | $0.0126 | not logged | |
| **L** | adaptive | low | 11/12 | 1 | $0.0110 | 14,169 | 20,867 |
| **DL** | disabled | low | 11/12 | 0 | $0.0058 | 0 | 10,306 |
| T2b D | disabled | medium (default) | **12/12** | 0 | $0.0060 | 0 | |

## Decisions, as pre-registered

- **Low effort avoids the empties:** does not hold. In arm L, regex
  again spent all 4,096 output tokens thinking and returned nothing.
  Low effort cut thinking on most tasks (median about 580 tokens) but not
  on the hardest one.
- **Setting for resident runs on Haiku (a direction, not a result):**
  **D, thinking disabled at the default (medium) effort**, with the most
  passes. DL is a hair cheaper ($0.0058 against $0.0060) and one pass
  behind; with 12 tasks and one attempt that gap is noise, as fixed in
  advance.

## The failures

- **L, regex:** empty; 4,096 thinking tokens, no text block.
- **DL, approx:** a real wrong answer (`ZeroDivisionError` on a hidden
  test), not an empty one. Thinking off removed the empty answers in both
  T2b and T2c; the one remaining failure is the model's work.

## What it means

- Across T2, T2b and T2c, every empty answer came with thinking on
  (default or low effort). None came with thinking off (24 calls).
- With a 4,096-token cap, adaptive thinking is a gamble on hard tasks: it
  usually fits, and when it does not, the run returns nothing. A resident's
  run on Haiku should turn thinking off, or, if it needs thinking, have a
  much larger `max_tokens` than the door allows today.
- Thinking on roughly doubled output and cost (L $0.0110 against DL
  $0.0058) for no gain in passes here.
