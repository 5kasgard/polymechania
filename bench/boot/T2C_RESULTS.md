# T2c results: effort and capped thinking on Haiku

Independently audited: `T2C_AUDIT.md` (numbers reproduce; wording corrected below).

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
  Thinking at low effort had a median of about 580 tokens per task; there
  is no baseline to say it was a cut, because T2 did not log thinking.
- **Setting for resident runs on Haiku (a direction, not a result):**
  **D, thinking disabled at the default (medium) effort**, with the most
  passes. DL is a hair cheaper ($0.0058 against $0.0060) and one pass
  behind; with 12 tasks and one attempt that gap is a direction to taste,
  as fixed in advance. D also ran in another session (T2b), so a one-pass
  difference cannot be told apart from run-to-run variation.

## The failures

- **L, regex:** empty; 4,096 thinking tokens, no text block.
- **DL, approx:** a real wrong answer (2,711 bytes of code that raised
  `ZeroDivisionError` under the grader), not an empty one. Thinking off removed the empty answers in both
  T2b and T2c; the one remaining failure is the model's work.

## What it means

- Across T2, T2b and T2c, all six empty answers (T2 arm A: three; T2
  arm B: two; T2c L: one) came with thinking on, by default or at low
  effort; in T2 "on" is inferred from the default, supported by T11's
  1,721 thinking tokens. None of the 24 calls with thinking off (T2b D and
  T2c DL) was empty.
- With a 4,096-token cap, adaptive thinking is a gamble on hard tasks: it
  usually fits, and when it does not, the run returns nothing. A resident's
  run on Haiku should turn thinking off, or, if it needs thinking, have a
  much larger `max_tokens` than the door allows today.
- Thinking on roughly doubled output and cost (L $0.0110 against DL
  $0.0058; 2.07 times even leaving out regex) for no gain in passes here.
