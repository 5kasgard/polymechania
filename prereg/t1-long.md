# Pre-registration (DRAFT, not yet reviewed or approved): T1, run shapes on long work

Written 2026-10-29, before any T1 run and before any model has seen the
long tasks. **Draft:** to be reviewed by Gemma 4 26B and Llama 3.3 70B (free,
not Claude) and seen by the owner before it is committed as final.

**Question** (docs/architecture.md, T1). On work that runs over several
dependent rounds with changing requirements, does starting each round in a
fresh run help, and does it help only when an independent check sits on the
boundary between runs ("a run boundary is worth its cost only where an
independent check sits on it")?

**Outside prior.** EvoCode-Bench (arXiv 2605.24110): for most agents,
single-round scores from a reference prior state beat persistent multi-round
scores by 22-40 points, and pass rates fall below half of round 1 by round
5. Ord (arXiv 2505.05115): cutting a task into pieces does not change its
chance of success unless something catches errors between the pieces.

**Authorship:** Claude Opus 5.5 (the session), who wrote the tasks too.
**Budget:** API bound **$0** (free models only); neurons are spread across
days by `bench/neurons.py`, after E-ext finishes (E-ext was registered first).

## Tasks

The six long tasks in `bench/long` (5 rounds each, 30 rounds; 67 cumulative
hidden tests with retirements), unchanged after this draft except for fixes
from the spec review, which must be committed before any run.

## Arms (every round asks for the complete module)

- **C, one session:** one conversation; each round's change is a new user
  turn after the model's previous reply (shape (c) without compaction; five
  rounds fit easily).
- **B, fresh runs:** each round is a fresh call holding only the model's own
  previous module, a two-line note it wrote at the end of its previous reply
  ("Notes for next time:"), and this round's change (shapes (a)/(b)).
- **BV, fresh runs with a check on the boundary:** as B, plus the failure
  messages of the *earlier rounds'* still-active tests on its previous
  module (never this round's new tests): the regression check a gate could
  run between runs.
- **SR, single-round control:** each round starts from the *reference*
  module of the round before, plus this round's change (EvoCode's SR).

Every arm sees round 1's full spec; later rounds give the change text, and
B, BV and SR also get a one-line list of the earlier changes' titles.

## Workers and conditions (the same for every arm)

Gemma 4 26B, Llama 3.3 70B and Qwen 3.8 27B on Workers AI through the door
(three families, free), temperature 0, `max_tokens` 4,096, each model's own
default thinking (as E-ext amendment 1). One attempt per round. Rounds run in
order within a task; tasks and models in parallel within the allowance.

## Measures

- **Round pass rate:** rounds whose module passes every active hidden test
  (30 per arm per model).
- **MT:** for C, B and BV, rounds passed before a task's first failure
  (EvoCode's fail-stop), averaged over tasks.
- Also reported: neurons and output tokens per round; how often B and BV
  rewrite earlier behaviour that had passed (a regression).

## Decisions, fixed now (pooled over the three models; gaps under 15 points are directions)

1. **A fresh start alone helps** if B's round pass rate is at least 15 points
   above C's.
2. **A check on the boundary helps** if BV is at least 15 points above B.
3. **The outside prior holds here** if SR minus C is between 15 and 45
   points (EvoCode's 22-40, widened for 30 rounds a model); below 15, our
   tasks are too easy to show it; above 45, too hard.
4. If C, B and BV all pass at least 90% of rounds, report that the tasks did
   not separate the shapes, rather than that shape does not matter.

## Audit

Grades, passes and MT recomputed by `bench/verify.py` (extended to T1) from
the saved modules; the write-up's wording audited by a non-Claude model.
