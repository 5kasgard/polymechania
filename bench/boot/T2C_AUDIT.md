# T2c audit

Independent audit by a separate agent, 2026-10-29. No network calls; `t2c.py report` and the pilot graders only.

## Order and numbers

- Pre-registration `a919e10` (05:13:04) comes before the results `f27c56a` (05:19:23). Between those commits nothing changed in `prereg/`, `t2c.py`, `run.py`, `self.md` or `packet.txt`.
- Regrading all 24 matches `t2c_results.json`. L: 11/12, with regex failing (0 bytes, 4,096 thinking tokens, `max_tokens`). DL: 11/12, with approx failing (`ZeroDivisionError`, 2,711 bytes of code). Empty answers: L 1, DL 0.
- Dollars: L $0.011046, DL $0.005763, total $0.0168. Thinking tokens: L 14,169, DL 0. Output tokens: L 20,867, DL 10,306. All confirmed.
- The L median is 582, across 12 values from 0 to 4,096 (window did not think at all). "About 580" holds.

## Decisions

- "Low effort avoids the empties: does not hold" is correct.
- D wins under the pre-registered rule: most passes, ties to the cheaper arm.
- The results call the one-pass gap "noise". The pre-registration says only "a direction to taste", so "noise" goes a little past it.

## The thinking-off claim

- Exactly 24 calls had thinking off: T2b D (12) and T2c DL (12). All 24 logged `thinking_tokens` 0 and returned text only, with no empty answer.
- There are 6 empty answers in total, all from Haiku: T2 arm A (regex, sudoku, approx), T2 arm B (regex, approx) and T2c L (regex).
- T2 never set `thinking`, so in T2 "thinking on" is inferred from the default. T2's t11 call logged 1,721 thinking tokens, which supports that. The claim holds.

## Overclaims and missing caveats

1. "Low effort cut thinking on most tasks" has no baseline. T2 arm B did not log thinking tokens, so nothing measured shows a cut.
2. The results never say that T2 arm A also produced 3 empty answers, which strengthens the thinking-on pattern.
3. D was run in a different session (T2b) from L and DL. With one attempt per task, an arm-to-arm difference of one pass cannot be told apart from run-to-run variation.
4. "Doubled output and cost" holds even without regex: L costs 2.07 times DL on the other 11 tasks.
5. "On a hidden test" (DL approx) is not checked here.
6. The `t2c.py` docstring is stale. It says results go to `t2b_results.json` and that "only the `thinking` field changes", but `output_config` changes too.
