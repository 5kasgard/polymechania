# Long tasks: five rounds, changing requirements, cumulative tests (q15)

Six single-file Python tasks (`tasks/`), each with five rounds. Each round adds
a requirement or **changes an earlier one** (every task has at least one
round that overturns an earlier rule: a new signature, a new rounding rule, a
sliding window instead of a fixed one, duplicates refused instead of the
later one winning, backorders allowed). Tests stay active across rounds
unless the round that changes the rule retires them; a round passes only if
every active test passes. 67 tests in all.

| Task | What changes along the way |
|---|---|
| ratelimit | fixed window, then per key, then sliding, retry_after, forgetting idle keys |
| config | pairs, sections (new return shape), comments, `${...}` interpolation, duplicates become errors |
| invoice | Decimal totals, tax, discounts, round per line instead of at the end, banker's rounding |
| words | top words, stop words and apostrophes, n-grams, ties by first appearance, Unicode and casefold |
| inventory | add and remove, history and undo, reservations, backorders allowed, snapshot and restore |
| booking | bookings, cancel and list, repeating series with a horizon, free slots, tentative bookings |

## Where the design comes from (download the method, build the instance)

EvoCode-Bench (arXiv 2605.24110, May 2026: 26 tasks, 5-15 rounds, cumulative
executable tests, Docker workspaces) and LoopsBench (arXiv 2608.00267: dependency
DAGs, completed units kept as regression obligations) measure this kind of work,
but need an agent harness and containers the door cannot run. These tasks keep
their method at a size the door can (text in, one module out, under 4,096
output tokens) so cheap and free models can be arms. Their published result is
the outside prior for T1: single-round scores from a reference prior state
beat persistent multi-round scores by 22-40 points for most agents, and pass
rates fall below half of round 1 by round 5.

Each round also has a reference module, so a run can be scored both ways, as
EvoCode does: **persistent** (each round starts from the worker's own code) and
**single-round** (each round starts from the reference of the round before).

## Checks on the graders (exact, before any model sees a task)

`python bench/long/grade.py --validate` (in CI) confirms for every round that the
reference passes every active test; the previous round's reference fails at
least one new test (an empty module for round 1); every retired test existed
and the retiring round's reference fails it. It caught four mistakes of mine
while building: a wrong expected n-gram order, a fixed-window test a sliding
window also passed, a reference crash on an unknown sku, and two tests that
could not tell rounding rules apart.

## Limits

Written by Claude, who will also be one of the workers tested on them; the
specs have not yet had an independent review for ambiguity (a test needing
something the spec does not say). That review is queued for the free judges
(Gemma, Llama) when the Workers AI allowance returns.
