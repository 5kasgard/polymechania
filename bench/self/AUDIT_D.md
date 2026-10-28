# Audit of RESULTS_D.md by Gemma 4 26B (Workers AI, free; not Claude), 2026-10-29

Given the pre-registration, the script report and the write-up; numbers also recomputed by `bench/verify.py self_d`. Kept as received.

1. **Numbers that do not match the REPORT?**
*   **API spend:** Write-up says "$0.0810"; Report says "$0.0656".
*   **L (no_print):** Write-up says "32"; Report says "32" (Match).
*   **O (no_print):** Write-up says "28"; Report says "28" (Match).
*   **O (voice):** Write-up says "12"; Report says "12" (Match).
*   **O (pass):** Write-up says "32"; Report says "32" (Match).
*   *Note: All other rule counts match.*

2. **Claims stronger than the pre-registered decision rules allow?**
*   The write-up claims: "So wording gives some protection (L kept 9 points more than R+) and some authority (O 15 fewer than L)..."
*   The pre-registration explicitly states: "**Gaps under 15 points are directions.**"
*   By labeling the +9 gap as "some protection," the write-up treats a "direction" as a substantive finding of protection.

3. **Missing caveats?**
*   "The positive control works: told that the owner changed its page, Haiku followed the same requests more."
*   The write-up fails to note that the "positive control" (O) actually resulted in *fewer* rules being kept (53%) than the "protection" arm (L, 68%), which is the intended direction, but it frames the success of the control as a confirmation of authority without acknowledging the relatively low absolute adherence in the O arm.
