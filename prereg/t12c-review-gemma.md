# Review of t12c-claude.md by @cf/google/gemma-4-26b-a4b-it (Workers AI, free; not Claude), 2026-10-29

Kept as received.

1. **Confounds:** The primary confound is the change in **temperature**. T12b used temperature 0 (deterministic), while T12c uses the Claude API default (stochastic). This introduces variance in the resident's behavior that was absent in the original test, potentially masking the effect of the "start-packet" or the pressure orders. Additionally, the **parallel execution** of R and R+ calls may introduce subtle timing or rate-limiting differences compared to the sequential nature of T12b.

2. **Rule Broken:** **Rule 5 (Same conditions for every vendor)** is violated. While the rule allows for different defaults if tuned identically, the transition from a fixed temperature (0) in the baseline to a variable default in the repeat changes the fundamental "settings" of the experiment. This makes it a different test rather than a direct replication.

3. **Exact changes before running:**
*   **Fix Temperature:** Explicitly set the temperature for the Claude Haiku resident to 0 (if the API allows) or document the specific default value used to ensure it is applied identically across all arms (S, R, R+).
*   **Standardize Execution:** Run the R and R+ arms sequentially rather than in parallel to match the T12b execution pattern and eliminate concurrency as a variable.
