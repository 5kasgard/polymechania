# T12c audit (Gemma 4 26B, free, not Claude)

**Errors and Fixes:**

1.  **Claim:** "R+ was 12 points below S"
    *   **Status:** Wrong.
    *   **Fact:** R+ (58%) is 13 points below S (71%).
    *   **Fix:** Change "12 points" to "13 points".

2.  **Claim:** "Llama judge... Spearman 0.63 against Gemma's 0.81"
    *   **Status:** Overstated/Misleading.
    *   **Fact:** The Spearman correlation of 0.63 is between Llama and the *rules kept*, not between Llama and Gemma. The 0.81 is Gemma vs the *rules kept*.
    *   **Fix:** "Llama follows the rule checks less closely (Spearman 0.63 vs rules, compared to Gemma's 0.81 vs rules)..."

3.  **Claim:** "R's replies were the shortest"
    *   **Status:** Unsupported.
    *   **Fact:** The table provides mean lengths (S: 1,611; R: 1,255; R+: 1,930), but does not provide the standard deviation or distribution to confirm R is definitively the shortest across the sample, only that its mean is lowest.
    *   **Fix:** "R had the lowest mean length;"

