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

Folded in on the cleanup pass (2026-10-29), verbatim from the review file named under each heading (git history, commit `fa517d6`); only the heading level of the review's own headings is lowered to nest here.

### Review of t12c-claude.md by @cf/google/gemma-4-26b-a4b-it (Workers AI, free; not Claude), 2026-10-29

Handling: amendment 1 (temperature 0 for Haiku; concurrent calls kept, with the reason given there) and amendment 2 (the API refused `temperature`, so Haiku ran at its sampling default).

Kept as received.

1. **Confounds:** The primary confound is the change in **temperature**. T12b used temperature 0 (deterministic), while T12c uses the Claude API default (stochastic). This introduces variance in the resident's behavior that was absent in the original test, potentially masking the effect of the "start-packet" or the pressure orders. Additionally, the **parallel execution** of R and R+ calls may introduce subtle timing or rate-limiting differences compared to the sequential nature of T12b.

2. **Rule Broken:** **Rule 5 (Same conditions for every vendor)** is violated. While the rule allows for different defaults if tuned identically, the transition from a fixed temperature (0) in the baseline to a variable default in the repeat changes the fundamental "settings" of the experiment. This makes it a different test rather than a direct replication.

3. **Exact changes before running:**
*   **Fix Temperature:** Explicitly set the temperature for the Claude Haiku resident to 0 (if the API allows) or document the specific default value used to ensure it is applied identically across all arms (S, R, R+).
*   **Standardize Execution:** Run the R and R+ arms sequentially rather than in parallel to match the T12b execution pattern and eliminate concurrency as a variable.

### Review of t12c-claude.md by @cf/meta/llama-3.3-70b-instruct-fp8-fast (Workers AI, free; not Claude), 2026-10-29

Handling: amendment 1 says "Llama's review found no rule broken; it is kept as received."

Kept as received.

Here's a review of the pre-registered experiment:
1. Confounds or differences from the earlier test that could explain a different result: The resident model has changed from Gemma 4 26B to Claude Haiku 5.5, and the temperature setting is different (default for Claude instead of 0). The `thinking` setting is also disabled for Claude, which may affect the results.
2. Any testing rule broken: No rules appear to be broken, as the pre-registration follows the required format and includes all necessary details, such as authorship, budget, and audit plans.
3. Exact changes before running: The changes made before running the experiment include using a different resident model (Claude Haiku 5.5), disabling the `thinking` setting, and using default effort and temperature settings. The judges and prompts remain the same as in the earlier test.
