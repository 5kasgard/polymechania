# Pre-registration: E-ext, do public benchmarks predict our own results?

Written 2026-10-29, before any E-ext run. First test of
`docs/evidence-model.md` (queue q03). **Authorship:** Claude Opus 5.5 (the
session). Reviewed before running by Gemma 4 26B and Llama 3.3 70B (free,
not Claude). **Budget:** API $0; Workers AI free allowance only, at most
9,000 neurons a day by the runner's own count, spread over as many days
as needed.

## The external numbers, frozen now (before our data)

Artificial Analysis Coding Index, as mirrored on vitna.ai's "Coding
Index" board (read 2026-10-29 via Exa search; AA's own pages are scripts):

| Workers AI model | Index entry | AA Coding Index |
|---|---|---|
| `@cf/qwen/qwen3.8-27b` | Qwen3.8 27B | 68.1 |
| `@cf/google/gemma-4-26b-a4b-it` | Gemma 4 26B A4B | 39.3 |
| `@cf/nvidia/nemotron-3-120b-a12b` | Nemotron 3 Super (120B-A12B) | 37.7 |
| `@cf/openai/gpt-oss-120b` | gpt-oss-120b | 30.4 |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | Llama 3.3 70B Instruct | 11.9 |
| `@cf/meta/llama-4-scout-17b-16e-instruct` | Llama 4 Scout | 8.2 |
| `@cf/meta/llama-3.1-8b-instruct-fp8-fast` | Llama 3.1 8B Instruct | 5.4 |

Not usable for the primary test (no Coding Index entry for these exact
models): Claude Haiku 5.5 and Sonnet 5.5 (AA Intelligence Index 43 and 56,
at max effort), gpt-oss-20b, Granite 4.0 H Micro, Mistral Small 3.1.

## Known mismatches (stated, not fixed)

- AA runs each model at its own chosen settings (often maximum reasoning);
  Workers AI serves some as fp8 quantisations; the door fixes temperature 0
  and turns thinking off for Gemma only, others at their defaults. So this
  tests whether the *public number as published* predicts *our use as we
  run it*, which is the practical question.
- Seven models, below the 10 that agreement checks want (BenchBench);
  the result is a direction, whatever it is.

## Design

- **Tasks:** the pilot's 24 tasks and hidden graders, unchanged.
- **Prompt (same for every model):** "Write the Python module described
  below. Reply with exactly one fenced Python code block containing the
  complete module, and nothing else." followed by the specification. No
  self, no packet.
- **Settings:** `max_tokens` 4,096 (the door's cap), one attempt per task
  per model; the door's fixed settings as above.
- **Runner:** calls 8 at once; counts neurons from each response; stops
  for the day at 9,000; resumes the next day where it stopped.

## Measures and decisions, fixed now

- **Primary:** Spearman rank correlation, across the seven models, between
  the AA Coding Index and our pass count out of 24. **Public benchmarks
  predict our results** if it is at least **0.714** (the one-tailed 5%
  critical value for 7 items). Ties in pass counts take average ranks.
- **Secondary:** the same on the 12 hard tasks only (less ceiling);
  Kendall's tau; how many of the 21 model pairs the index orders the same
  way we do; and cost per pass in neurons per model.
- **Also reported, not decided on:** where Haiku 5.5 and Sonnet 5.5 (T2's
  results, other settings) would sit against their Intelligence Index.
- If the index predicts our order, external evidence can carry more
  weight in cards for this kind of work; if not, internal tests on our own
  work get the budget (evidence model, point 7).

## Amendment 1 (2026-10-29, after the two reviews, before any run)

From Gemma's review (rule 5): **every model at its own Workers AI default
for thinking**, including Gemma (the door's Gemma-only "thinking off" is
skipped for this test by a new opt-in field, `default_thinking: true`, on
`/ai`), and **temperature 0 and `max_tokens` 4,096 for all** (fixed by the
door). The fp8 and settings mismatches with AA's runs remain and are the
point of the test (the public number against our use). Llama's review: the
Haiku and Sonnet comparison is reported only, as already stated; no more
models have Coding Index entries.

## Reviews

Folded in on the cleanup pass (2026-10-29), verbatim from the review file named under each heading (git history, commit `fa517d6`); only the heading level of the review's own headings is lowered to nest here.

### Review of eext-benchmarks.md by @cf/google/gemma-4-26b-a4b-it (Workers AI, free; not Claude), 2026-10-29

Handling: amendment 1 (above), which set temperature 0 and `max_tokens` 4,096 for all models and left thinking at each model's own default (the door's Gemma-only thinking-off is skipped for this test); the fp8 and settings mismatches with AA's runs are kept as the point of the test.

Kept as received.

1. **Confounds:**
* **Inconsistent Settings:** The "door" applies different settings (temperature 0/no thinking for Gemma vs. defaults for others). This violates Rule 5, as settings are not uniform across vendors, making it impossible to tell if results reflect model capability or the specific configuration mismatch.
* **Quantization/Hardware:** Comparing fp8 quantizations to AA's "maximum reasoning" settings introduces noise regarding whether the index predicts the *model* or the *specific deployment*.
* **Sample Size:** With only 7 models, the statistical power is low, increasing the risk of a Type II error.

2. **Testing Rules Broken:**
* **Rule 5 (Same conditions):** Settings are not fixed/identical across all arms; they vary by model.
* **Rule 4 (Blind/Shuffled):** While the prompt is identical, the lack of uniform settings means the "arms" are not being tested under the same conditions.

3. **Exact Changes Before Running:**
* **Standardize Settings:** Force all models to use the same temperature and "thinking" settings (either all at defaults or all at the "door's" fixed settings) to satisfy Rule 5.
* **Document Settings:** Explicitly list the fixed temperature and reasoning parameters in the "Settings" section.

### Review of eext-benchmarks.md by @cf/meta/llama-3.3-70b-instruct-fp8-fast (Workers AI, free; not Claude), 2026-10-29

Handling: amendment 1 (above): the Haiku and Sonnet comparison is reported only, and no more models have Coding Index entries.

Kept as received.

Here's a review of the pre-registered experiment:
1. Confounds include differences in model settings and quantisations between AA and Workers AI, which may affect the results. The small number of models (7) may also lead to less reliable conclusions.
2. No testing rule appears to be broken, as the pre-registration follows the guidelines outlined in the testing rules section.
3. Exact changes to consider before running include:
 * Consider adding more models to increase the reliability of the results.
 * Clarify how the Intelligence Index for Haiku 5.5 and Sonnet 5.5 will be used, as it is not directly comparable to the Coding Index.
 * Double-check that the settings for each model are correctly specified and consistent with the pre-registration.
