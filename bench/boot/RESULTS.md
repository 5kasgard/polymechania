# T2 results: a thin boot through the door

Run 2026-10-28 under `prereg/t2-thin-boot.md` with amendment 1 (after
`prereg/t2-review-1.md`). Raw data: `results.json`; code given by each run:
`solutions/`; the start packet: `self.md` and `packet.txt` (hashes checked
before running). 98 calls in all (2 calibration, 96 task calls) plus 2 for
T11; total cost **$0.70**.

## The decisions, as pre-registered

| Decision | Rule | Result | Holds? |
|---|---|---|---|
| Thin boot | boot <= 4,000 tokens and <= 5% of the pilot's ~79,000 | **1,486 tokens, 1.9%** (both models) | yes |
| Caching | each of calls 2-24 in arm B reads >= 90% of the boot from cache | 1,480 of 1,486 read on **23/23** calls, both models; largest gap between calls 28 s | yes |
| Quality | pooled A+B on Haiku below 40/48 means a thin boot costs quality | **43/48** (Sonnet 47/48) | no quality loss by the rule |
| Headline | dollars per pass, arm B, against the pilot's bracket | see below | |

## Numbers

| | Pass | $ per pass | Boot share (median, descriptive) |
|---|---|---|---|
| Haiku, door, A (cold) | 21/24 | $0.00125 | 46% |
| Haiku, door, B (cached) | 22/24 | **$0.00100** | 44% |
| Haiku, pilot harness | 24/24 | $0.00133 to $0.00884 | about 97% |
| Sonnet, door, A (cold) | 23/24 | $0.01580 | 56% |
| Sonnet, door, B (cached) | 24/24 | **$0.01211** | 56% |
| Sonnet, pilot harness | 24/24 | $0.01797 to $0.16936 | about 97% |

The pilot's range is API-equivalent (it ran on a subscription): all input
priced as cache reads at the low end, all as uncached input at the high
end, output fixed at 1,000 tokens per run before running. The door's arm B
costs **0.75x to 0.11x** the pilot per pass on Haiku and **0.67x to
0.07x** on Sonnet: cheaper at either end of the bracket.

Median time per call: about 8 s on both models (the pilot's sub-agents:
median about 15 s).

## What the failures were

All six failures (Haiku: regex, sudoku and approx in A; regex and approx
in B. Sonnet: regex in A) stopped at the door's **4,096-token output cap**
mid-answer, so the code was cut off. No call that finished its answer
failed a grader. That cap was set for E1, not for this; a run budget is a
separate dial (spec section 7), and the same calls with a higher cap, or a
retry on `max_tokens`, would be the next measurement.

## T11, the runaway check

- `max_tokens` 5,000: refused by the door itself, 400, "max_tokens must be
  1-4096". Holds.
- A request for a 10,000-word essay with `max_tokens` 4,096: stopped with
  `stop_reason` `max_tokens` at exactly 4,096 output tokens (of which
  1,721 were thinking). Holds: the worst case of one call is 4,096 output
  tokens plus its input, about $0.0022 on Haiku and $0.045 on Sonnet.

## What this does and does not show

- **Shows:** a run can start for about 1,500 tokens instead of about
  80,000, the whole start packet caches after the first call, and on these
  24 tasks one-shot runs with no tools passed nearly as often as tool-using
  sub-agents, at lower cost per pass.
- **Does not show:** long, vague, multi-step work (T1), where losing tools
  could matter more; a self grown by a resident (this one was written for
  the test, by someone who knew the tasks, which may raise pass rates);
  more than two attempts per task; caching across the gaps of a real
  schedule (calls here were seconds apart).
