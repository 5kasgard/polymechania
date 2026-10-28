# Audit of T2 results

Independent audit by a separate agent (Claude Opus 5.5), 2026-10-28. No
network calls. Nothing edited but this file.

## 1. Numbers: all reproduce

I recomputed everything from `results.json`, `bench/pilot/results.json` and
the `plan.py` prices, and found no mismatch that matters:
- Boot is 1,486 tokens on both models, 1.9% of 79,000.
- Pass counts: Haiku 21 and 22, Sonnet 23 and 24.
- Dollars per pass: $0.00125, $0.00100, $0.01580 and $0.01211.
- Median boot shares are 46/44% and 56/56%.
- Each per-call `usd` matches the token counts.
- In arm B, calls 2 to 24 each read 1,480 of 1,486 tokens from the cache on both models (99.6%). The largest gaps were 20.9 s (Haiku) and 28.2 s (Sonnet).
- The pilot bracket at a fixed 1,000 output tokens is $0.00133 to $0.00884 (Haiku) and $0.01797 to $0.16936 (Sonnet).
- The ratios are 0.75x to 0.11x and 0.67x to 0.07x.
- Task calls cost $0.702. With calibration and T11 the total is about $0.705.
- Median call times are 7 to 8 s. The pilot's pooled median is 15.1 s.

Two small points:
- The pilot's median of about 15 s hides a split between models: Haiku 20.4 s, Sonnet 11.5 s.
- T11's Sonnet worst case comes to $0.044, not $0.045. Sonnet was not tested directly; that figure is arithmetic.

## 2. Grades: confirmed

I regraded all 96 saved solutions with the pilot graders. All 96 match `results.json`. All six failures have `stop_reason` `max_tokens` at exactly 4,096 output tokens, and every call that ended `end_turn` passed.

**Correction to RESULTS.md.** It says the failures were "cut off mid-answer". That is true only for Sonnet's regex: 3.6 KB of unclosed code, which fails with a SyntaxError. **Haiku's five failing files are empty (0 bytes).** The reply held no text, so Haiku never began an answer. The likely cause is unrequested thinking. T11 shows the model thinking by default (1,721 thinking tokens), although the prereg says "no thinking". The runner does not log `thinking_tokens` per call, so this cannot be confirmed for the task runs. It affects both the cost per pass (thinking is billed as output) and why Haiku failed.

## 3. Pre-registration adherence: followed

- **Git history:**
  - Prereg at 22:29.
  - Amendment 1 at 22:35, which fixed the thresholds, the arms, the 1,000-token bracket, the second breakpoint and the hashes.
  - Results at 22:52.

  The only post-amendment diff to `run.py` is the user-agent header and the parsing of non-JSON error bodies. Neither touches the request body, the grading or the analysis, so the change is harmless. That it came before any model call succeeded cannot be verified from the files, because `results.json` has no timestamps. It is consistent with the commit order.
- **Hashes:** `self.md` and `packet.txt` match the amendment exactly.
- **Decisions:** all were applied as amended.
  - Thin boot: 1,486 ≤ 4,000 and ≤ 3,950.
  - Caching: each call ≥ 90% of the calibration boot.
  - Quality: pooled on Haiku, 43/48, not below 40.
  - Headline: arm B with arm A alongside, and the bracket at both ends.
  - Boot share is kept descriptive.

  No threshold or arm was changed after the data came in.

## 4. Interpretation

- **"No quality loss by the rule"** is correct as a rule outcome, but weaker than it sounds:
  - Arms A and B are the same prompt, so the effective sample is about 24 tasks, not 48. Haiku failed regex and approx in *both* arms, which is a systematic gap on hard tasks, not noise.
  - The pilot passed 24/24 with tools.
  - The disclosed task-aware self biases the door's pass rate upward.

  A better wording: "above the pre-registered floor; Haiku consistently fails 2 of 12 hard tasks under a 4,096 cap."
- **The A/B differences in passes and cost are not a caching effect.** Haiku B is cheaper per pass partly because one fewer call burned 4,096 tokens and failed. The caching saving itself is about 1,480 tokens per call.
- **The pilot bracket's low end, the realistic one for Claude Code with its cached prefix, decides the headline.** It depends on the assumed 1,000 output tokens. Holding the pilot's total tokens fixed, the door stays cheaper only while the pilot's runs averaged more than about 320 output tokens on Haiku, or about 410 on Sonnet. That is plausible (solutions plus tool calls), but it is an assumption. The low end also ignores the pilot's cache writes. "Cheaper at either end" is fair. The honest margin is "about 25 to 33% cheaper", not "up to 9 to 14x".
- **Missing caveats:**
  - Default thinking was on.
  - The 4,096 cap is the door's hard limit, so a "higher cap" retry needs a change to the door.
  - Sonnet's T11 worst case is computed, not measured.

## 5. Next measurement

1. Log `thinking_tokens` and the content-block types for every call.
2. Rerun the six failures, and ideally all of Haiku's hard tasks, with thinking explicitly disabled, then again with a capped `budget_tokens`. Report pass rate and $ per pass for each.
3. Price a Haiku-to-Sonnet cascade on `max_tokens` from the existing calls, pairing A with A and B with B as pre-registered. Sonnet B passed every task Haiku failed.
4. Recover the pilot's real output tokens, if the logs allow, to replace the bracket's assumption.
5. Then run T1, the long and vague work.
