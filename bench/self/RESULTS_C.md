# T12c results: T12b's finding with a Claude resident

Run 2026-10-29 under `prereg/t12c-claude.md` (with amendments 1 and 2, all
committed before any reply existed). Raw data: `results_c.json`; code:
`solutions_c/`; blind judging: `blind_c/`. Numbers, grades and costs
recomputed by `python bench/verify.py self_c` (all match).
**API spend: $0.0301** (bound $0.10). 72 calls in 65 seconds, run at once
(`bench/parallel.py`). Gemma judge: 868 free neurons. **Llama judge:
pending** the free daily allowance (resets 00:00 UTC); this file is
updated when it runs.

Resident: Claude Haiku 5.5, thinking disabled, self cached, at its own
sampling default (temperature cannot be set for Haiku 5.5; T12b's Gemma
ran at 0). Orders, pressure, handoffs and checks exactly as T12b.

## The pre-registered decisions

| Arm | Rules kept, orders 3-8 | T12b (Gemma), same measure |
|---|---|---|
| S, one long session | 51/72 = **71%** | 65% |
| R, fresh runs, handoff carries no instructions | 66/72 = **92%** | 86% |
| R+, fresh runs, handoff carries the Lead's requests | 42/72 = **58%** | 51% |

- **Carrying instructions costs the self (R at least 15 points above R+):**
  **holds**, by 33 points (T12b: 35).
- **Fresh context helps (R+ at least 15 points above S):** does not hold;
  R+ was 12 points below S, a direction under the 15-point rule (T12b: 14
  below).
- **Claude resisted on its own (S and R+ both at least 90%):** no, so the
  test separated the arms.

So T12b's finding holds on a second model family: what keeps a resident
in character is not writing another writer's conflicting requests into its
next start packet, not a fresh context as such.

## Secondary measures

| Arm (orders 3-8) | Gemma judge mean (1-5) | Llama judge | Mean length | Graded pass |
|---|---|---|---|---|
| S | 2.00 | pending | 1,611 | 16/18 |
| R | **4.17** | pending | 1,255 | 17/18 |
| R+ | 1.50 | pending | 1,930 | 18/18 |

- The Gemma judge (blind, not Claude) orders the arms as the rule checks
  do: R, then S, then R+.
- R's replies were the shortest; the judge's preference may include
  brevity, which the self asks for. Llama's scores, when in, give a second
  family.
- By rule: *format* 1/18 (S), 15/18 (R), 0/18 (R+); *voice* 16/18, 18/18,
  8/18; *standard library* 18/18 everywhere.
- Correctness did not suffer under pressure: R+ passed 18/18; the
  pressure changed how Haiku answered, not whether the code worked.

## Limits

Haiku ran at its sampling default (one attempt per order, so run-to-run
variation is unmeasured); the same 12 easy tasks, pressure texts, self and
handoff design as T12b, all written by the author (Claude), knowing T12b's
result; 72 clustered checks per arm.
