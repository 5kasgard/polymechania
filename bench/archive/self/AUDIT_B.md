# Audit of RESULTS_B.md by Llama 3.3 70B (Workers AI, free; not Claude), 2026-10-29

Given the pre-registration, the script report and the write-up. Numbers were also recomputed by `bench/verify.py self` (all match). Kept as received.

Here are the audit results:
1. The write-up states "R+ was 14 points *below* S" which matches the REPORT's calculation of "fresh context (R+ - S): -14 points".
2. The write-up claims "Carrying instructions costs the self (R at least 15 points above R+): **holds**, by 35 points" which is supported by the REPORT's calculation of "carrying instructions (R - R+): +35 points; holds: True". However, the write-up also states "the hypothesis in `docs/architecture.md` (a fresh run from a fixed self stays closer to it) is not supported as stated" which may be an overstatement since the pre-registration only defined a "fresh context" as R+ being at least 15 points above S, and the results show R+ being 14 points below S.
3. The write-up mentions some caveats, such as "One open model (Gemma 4 26B) at temperature 0; 12 easy tasks, three sequences... A Claude resident, other pressure, or a richer handoff could come out differently." However, it does not mention that the pre-registration defined a gap below 15 points as a direction, not a result, which could be seen as a missing caveat. Additionally, the write-up quotes the pre-registration's decision rules, but does not explicitly state that the results should be interpreted in the context of those rules.
