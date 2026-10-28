# T2b audit

Independent audit by a separate agent, 2026-10-29. No network calls; `t2b.py report` only.

## Checks

- **Order:** the pre-registration was committed at `aea57d1` (05:03:42), and the results at `d2ba5be` (05:05:23). The commit order fits "registered before run". Git dates cannot prove when the run happened.
- **Regrade:** all 12 files in `solutions/haiku/D/` PASS under `hard/grade.py`. None is empty, none hit `max_tokens`, and every call logged 0 thinking tokens with text-only blocks. The dollar figures, recomputed from tokens at `run.py` prices, total $0.005968, which matches the logged $0.0060.
- **Baseline:** T2 Haiku arm B on the hard tasks scored 10/12 at $0.0126. Both failures (regex, approx) are 0-byte files that stopped at `max_tokens` with output 4,096. Confirmed.
- **Hashes:** `t2b.py` does not check hashes itself. The `self.md` and `packet.txt` hashes do match those fixed in `prereg/t2-thin-boot.md`, and git shows neither file changed since T2. The claim holds.
- **Decisions:** the empties rule is applied exactly as written. The "default" rule was written as D against E, and E never ran, so the rule cannot be applied. The write-up says this openly and calls D's selection "on this evidence". That is acceptable, but this choice is outside the pre-registration, not a pre-registered decision.
- **Arm E deviation:** reported honestly. The refusal text is not kept in the raw data. "No arm-E call was made" is slightly loose: a request was sent and refused (and not charged).

## Overclaims and missing caveats

1. **"With thinking off … every one of the pilot's 24 tasks" is wrong.** T2's easy arm B (12/12, $0.0094) ran with no `thinking` field, which is the model's default, not thinking off. Only the 12 hard tasks were run with thinking off.
2. **"$0.0006 per hard task" is wrong.** $0.005968 / 12 = **$0.0005**.
3. **The mechanism is inferred, not measured.** T2 did not log thinking tokens, so "failures were output spent on thinking" depends on T11 and on the D contrast. One attempt per task cannot rule out sampling variance.
4. The 12/12 vs 10/12 gap is two passes, which the pre-registration itself rules is "not evidence". The bold **disabled** wording in the decisions section should carry that qualifier directly.
5. The architecture bullets (the cascade escalated "mostly because of these empties"; Sonnet as "the exception") were not tested in T2b and should be labelled as hypotheses.

**Verdict:** the data, grades and costs are sound. Fix items 1 and 2. Items 3–5 are wording and caveats.
