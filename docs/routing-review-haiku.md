# Review of routing.md by Claude Haiku 5.5 (sub-agent on the owner's Pro plan), 2026-10-29

Kept as received (lightly formatted).

1. Missing routing dimensions (section 2): sample size behind each card value (an estimate from 3 verdicts should not route like one from 300); version drift (when a card is re-tested after a model revision or deprecation).
2. Bias that still gets in (section 3): rule 7 only declares the author's bias, so prompts per arm should be drafted or reviewed by someone else; rule 3 requires a different family but not a comparable price tier, so a strong judge can favour expensive answers; rule 4 hides labels, not style, and has no length control though the padding finding is cited; rule 5 lets the author "state" each vendor's settings, which reopens tuning.
3. Contradictions and vagueness: CLAUDE.md item 3 routes judging to Claude sub-agents while item 6 and rule 3 forbid a worker's own family judging alone; rule 8 "where possible" and rule 2 do not say when a model judge is allowed for open-ended work; "when the record shows a gain" has no threshold; rule 1 "amend before data" against section 1 "adjusted by the record" is unclear; rule 9 sets no ceiling or method for the cost bound.
