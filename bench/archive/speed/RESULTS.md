# S1 results: speed by where a job runs

Run 2026-10-29 under `bench/archive/prereg/s1-speed.md` (committed before running).
API spend $0. Raw: `s1-here.json`, `s1-actions.json`, `s1-calls.json`.

## J1, grading the 96 saved T2 solutions (median of three)

| Where | CPUs | One at a time | All CPUs at once | Queue + set-up |
|---|---|---|---|---|
| This session's container | 2 | 20.1 s | 10.6 s (1.9x) | none |
| GitHub Actions `ubuntu-latest` (public repo) | **4** | 22.9 s | 9.8 s (2.3x) | 4 s queue, about 3 s set-up |
| Codespaces | not reachable | | | this session's GitHub access does not cover the Codespaces API |

All arms passed the same 90 of 96, as recorded. The runner's 4 CPUs settle
the conflicting published specs.

## J2, 24 short Gemma 4 26B calls through the door (one pass)

| | Wall time | Median call | Neurons |
|---|---|---|---|
| One at a time | 174.9 s | 5.6 s | 189 |
| 8 at once | **19.6 s (8.9x)** | 6.0 s | 188 |

The script used all 24 pilot task specs (the pre-registration said "the
easy task specs", of which there are only 12).

## Decisions, as pre-registered

- **Doing things at once pays (at least 2x):** holds for model calls
  (8.9x, and each call barely slowed, so Workers AI did not throttle at
  8); holds on Actions for grading (2.3x); just short here (1.9x on 2
  CPUs).
- **Route to Actions** only if at least 2x faster including queue and
  set-up, or if it frees the session for over a minute at no loss of
  speed: **not** for this 10-second job (about 17 s there against 10.6 s
  here). Long jobs (minutes) are where Actions pays, by freeing the session.

## What it means

- The biggest speed lever measured is **concurrency of model calls**:
  nearly 9x for free. T2 and T12b ran their calls one at a time; the next
  runners should send calls at once (after the first, cache-writing call
  for Claude).
- Machines matter less than waiting: for exact jobs under a minute, the
  session's own container is fastest; for long ones, Actions frees it.
- One day, one pass for J2: a direction for routing, not a constant.
