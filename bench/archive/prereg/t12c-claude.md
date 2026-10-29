# Pre-registration: T12c, does T12b hold with a Claude resident?

Written 2026-10-29, before any T12c run. Repeats T12b
(`bench/archive/prereg/t12b-self.md`, results `bench/archive/self/RESULTS_B.md`) with the
resident changed from Gemma 4 26B to **Claude Haiku 5.5**, to test whether
the start-packet finding holds on Claude.

**Authorship (rule 7):** written by Claude Opus 5.5 (the session), which
also wrote T12b and knows its result; reviewed before running by two
non-Claude models (Gemma 4 26B and Llama 3.3 70B, Workers AI, free).
**Budget (rule 9):** API cost bound **$0.10** (under a tenth of the about
$4.25 left); judges free (Workers AI), run after the daily allowance
resets if today's is short.

## Everything as T12b, except

- **Resident:** `claude-haiku-5-5` through the door, `thinking:
  {"type": "disabled"}` (the setting T2b/T2c chose for Haiku), default
  effort, `max_tokens` 4,096, **temperature 0** (as T12b's Gemma; see
  amendment 1).
- **The self is the system block with `cache_control`**, as in T2 arm B.
- **Calls run at once** (`bench/parallel.py`): the three S sessions in
  parallel (each turn in order), and all R and R+ calls 8 at once after
  the first.
- **Judges:** Llama 3.3 70B and Gemma 4 26B, both not Claude, blind,
  shuffled (seed 12), same prompt as T12b; no Claude judge (rule 3: the
  worker is Claude).

Arms S, R, R+; the same 12 easy tasks, three sequences of 8, pressure on
orders 3, 5, 7, texts unchanged; the same `ast` checks; 72 replies.

## Decisions, fixed now (same rules as T12b)

- **Carrying instructions costs the self** if R keeps at least 15 points
  more of the rules (orders 3-8, 72 checks per arm) than R+. If it holds,
  T12b's finding holds on Claude Haiku.
- **Fresh context helps** if R+ keeps at least 15 points more than S.
- Gaps under 15 points are directions. Judges' means are reported beside
  mean length, per judge.
- If Haiku keeps nearly every rule in every arm (at least 90% in S and
  R+), report that Claude resisted the pressure itself and the test could
  not separate the arms, rather than that the rule does not matter.

## Audit

Numbers by `bench/verify.py` (extended to T12c); wording by a non-Claude
model.

## Amendment 1 (2026-10-29, after the two reviews, before any run)

- **Temperature 0** for Haiku (Gemma's review): the door does pass
  `temperature`, so the first draft was wrong to say it could not.
- **Calls stay concurrent** (declining Gemma's second point, with the
  reason): every call is independent and its content does not depend on
  when it runs, so concurrency can change speed, not answers. Rate-limit
  errors would surface as failed calls, which `bench/parallel.py`
  re-raises rather than drops.
- Llama's review found no rule broken; it is kept as received.

## Amendment 2 (2026-10-29, before any data)

The API refused `temperature` for Claude Haiku 5.5 ("`temperature` is
deprecated for this model"; three calls refused, nothing charged, no
replies). So amendment 1's fix is impossible: Haiku runs at its own
sampling default, while T12b's Gemma ran at temperature 0. This is a
**known difference from T12b** that could explain a different result
(run-to-run variation, which one attempt per order cannot measure), and
is reported with the results. Everything else stands.

## Reviews

Folded in on the cleanup pass (2026-10-29), condensed to the points made; the full text of each review file is in git history at `fa517d6`.

**Gemma 4 26B (Workers AI, free; not Claude).**
- Confound: temperature. T12b ran Gemma at 0; T12c uses Haiku's default, so rule 5 is changed against the baseline. Applied in amendment 1 (set temperature 0). Amendment 2 then found the API refuses `temperature` for Claude Haiku 5.5, so Haiku ran at its default and the difference from T12b is reported with the results.
- Confound: R and R+ calls run in parallel, where T12b ran sequentially. Declined in amendment 1 with a reason: calls are independent, so concurrency can change speed, not answers; rate-limit errors would surface as failed calls, which `bench/parallel.py` re-raises.

**Llama 3.3 70B (Workers AI, free).** Listed the known differences from T12b (resident Gemma to Haiku, temperature, thinking off); found no rule broken; suggested no change.
