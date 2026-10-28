# Review of t12d-labels.md by @cf/google/gemma-4-26b-a4b-it (Workers AI, free; not Claude), 2026-10-29

Kept as received.

1. **Confounds?** Yes. The experiment compares a new run (L and O arms) against a previous run (R and R+ arms). Because the T12c arms were "run in another batch" with "sampling default, one attempt," any difference in results could be attributed to stochastic variance (sampling noise) or changes in the API environment rather than the labels themselves.

2. **Any testing rule broken?** 
   - **Rule 4 (Blind and Shuffled):** While the design mentions orders, it does not explicitly state that the comparison between the new batch and the old batch is blinded or that the "one attempt" per arm prevents bias in a single-sample comparison.
   - **Rule 8 (Audit separately):** The comparison relies on a single-run delta against historical data rather than a controlled, simultaneous comparison, which weakens the auditability of the "15 point" threshold.

3. **Exact changes before running:** 
   - Increase the number of attempts per arm (e.g., run each arm 5-10 times) to ensure the 15-point threshold is statistically significant and not a result of sampling noise.
   - Run L, O, R, and R+ in the same batch/session to ensure identical API conditions.
