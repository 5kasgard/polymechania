# Review of eext-benchmarks.md by @cf/google/gemma-4-26b-a4b-it (Workers AI, free; not Claude), 2026-10-29

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
