# T2 results: a thin boot through the door

Run 2026-10-28 under `prereg/t2-thin-boot.md` with amendment 1 (after
`prereg/t2-thin-boot.md`, Reviews). Raw data: `results.json`; code given by each run:
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
0.07x** on Sonnet: cheaper at either end of the bracket. The low end (pilot
input read from cache) is the realistic one, so the honest headline is
**about 25 to 33% cheaper per pass**, not 9 to 14 times. That margin rests
on the assumed 1,000 output tokens per pilot run: below about 320 (Haiku)
or 410 (Sonnet) it would vanish (`AUDIT.md`).

Median time per call: about 8 s on both models (the pilot's sub-agents:
median 20.4 s on Haiku, 11.5 s on Sonnet).

## What the failures were (corrected after `AUDIT.md`)

All six failures stopped at the door's **4,096-token output cap**, and no
call that finished its answer failed a grader. But they are two kinds:

- **Haiku, five of them** (regex and approx in both arms; sudoku in A):
  the saved code is **empty**. Haiku never began its answer; the likely
  cause is extended thinking it was not asked for. T11 shows 1,721
  thinking tokens on a request that set no `thinking` field, and the
  runner did not log thinking per call, so this is the likely cause,
  not a measured one.
- **Sonnet, one** (regex, arm A): 3.6 KB of real code cut off mid-answer.

So the first draft of this file was wrong to call them all truncated
answers. The 4,096 cap is the door's hard limit (set for E1); raising it
means changing the door.

## The cascade, priced from these same calls

Haiku first; Sonnet only where Haiku's answer failed its exact check
(A paired with A, B with B, as pre-registered):

| | Pass | $ total | $ per pass |
|---|---|---|---|
| Cascade, A | 23/24 | $0.1121 | $0.00488 |
| Cascade, B (cached) | **24/24** | $0.0818 | **$0.00341** |
| Sonnet alone, B | 24/24 | $0.2908 | $0.01211 |

The cached cascade matched Sonnet alone on these 24 tasks at about a
quarter of the price. This is the planner's escalation (spec section 2)
measured for the first time; the pilot had no task that needed it.
Caveat: it escalated on the *hidden* grader, which a real run would not
have; with only the worker's visible checks (the spec's examples, a
`max_tokens` stop, an empty answer) some failures would slip through.
Five of the six here would still have been caught, because the answer was
empty or cut off; that is a property of these failures, not a general
result. Priced after the run, by the pairing rule fixed in amendment 1.

## T11, the runaway check

- `max_tokens` 5,000: refused by the door itself, 400, "max_tokens must be
  1-4096". Holds.
- A request for a 10,000-word essay with `max_tokens` 4,096: stopped with
  `stop_reason` `max_tokens` at exactly 4,096 output tokens (of which
  1,721 were thinking). Holds: the worst case of one call is 4,096 output
  tokens plus its input, about $0.0022 on Haiku (tested) and $0.044 on Sonnet (arithmetic, not tested).

## What this does and does not show

Independently audited: `AUDIT.md` (every number and grade reproduced).

- **Shows:** a run can start for about 1,500 tokens instead of about
  80,000; the whole start packet caches after the first call; one-shot
  runs with no tools passed 43/48 (Haiku) and 47/48 (Sonnet), and a cached
  Haiku-then-Sonnet cascade passed 24/24 at about a quarter of Sonnet's
  price.
- **Weaker than it looks:** arms A and B send the same prompt, so this is
  about 24 independent tasks, not 48; Haiku failed regex and approx in
  both arms, a consistent gap on hard tasks rather than chance; the self
  was written knowing the tasks; thinking appears to have been on by
  default.
- **Does not show:** long, vague, multi-step work (T1), where losing tools
  could matter more; a self grown by a resident (this one was written for
  the test, by someone who knew the tasks, which may raise pass rates);
  more than two attempts per task; caching across the gaps of a real
  schedule (calls here were seconds apart).

## Addendum (2026-10-29, exploratory): the pilot's output, bounded

The pilot logged one token total per run, so its output cannot be
recovered exactly. A lower bound can: each sub-agent had to write its
solution file as output. Using the highest characters-per-output-token
seen on the door's own code replies (3.32, from T2b), the pilot's mean
output was at least **593 tokens per run on Haiku and 398 on Sonnet**.
The audit's break-even (recomputed: 317 and 408) then gives, at the
pilot's low end (its start-up read from a warm cache):

| | Pilot low end, per pass | Door, arm B, per pass | Door / pilot |
|---|---|---|---|
| Haiku | at most $0.00113 | $0.00100 | at least 12% cheaper |
| Sonnet | at most $0.01201 | $0.01211 | about even |

So **with a warm cache, the thin boot saves little per call**; the
harness's 80,000-token start-up costs little when it is read from cache
at 0.1x or 0.05x. The large saving (the high end, 9 to 14 times) is when
that start-up is *not* cached, which is the case for runs more than five
minutes apart (or an hour, with the long-lived cache): exactly the runs a
schedule makes. So the thin boot matters most for spaced-out, scheduled
work, and for the share of a plan's usage window each run consumes, not
for back-to-back calls. The script for these numbers is not kept; they
follow from `bench/pilot/results.json`, the pilot's solution files and
`t2b_results.json`.
