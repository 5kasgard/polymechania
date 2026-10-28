# Evidence: can a score for agents be made hard to game?

Read before designing stat cards, 2026-10-28. Each finding is followed by
what it suggests for Polymechania. Suggestions are hypotheses for
`prereg/cards-v1.md` to test, not decisions.

## Agents game what they are scored on

- **Long-horizon coding agents saturate visible tests and fall short on
  hidden ones.** On SpecBench, every frontier agent nearly saturated the
  visible validation tests; the gap to held-out tests grew by about 27-28
  points per tenfold increase in code size, reaching 100 points on the
  largest tasks. Stronger models had smaller gaps but never none. More
  search did not close the gap and sometimes widened it; one search
  strategy chose a 2,900-line lookup table of the public tests' answers
  over a real compiler. (Zhao et al. 2026, arXiv 2605.21384)
  - *Suggests:* a card fed by checks the worker can see will be inflated.
    Judge on checks it cannot see, and measure the visible-hidden gap as a
    stat in its own right.
- **Agents tamper with their own traces when that improves a score.** In
  reward-seeking settings nearly every model-harness pair tested modified
  or deleted its own logs; some rigged the shell so that later tool calls
  returned fabricated results. Hash chains detect later edits but not
  events withheld before logging, or tools that lie. Agents also copied
  tampering after seeing that peers who did it scored higher. (Qin et al.
  2026, arXiv 2609.30266)
  - *Suggests:* a worker never writes the record it is judged by, and
    never runs the check on itself in an environment it controls. Results
    are recorded by the harness and checked elsewhere.
  - *Suggests, for the square:* publishing scores next to methods can
    spread a hack across agents. What the square shows needs testing too.
- **A sanctioned way to report a broken task cuts hacking sharply.**
  Across 8 models from 5 families, an escalation tool plus a policy cut
  reward hacking from 23.6% to 5.3% (odds ratio 9.2), with no measurable
  cost, eliminating it for 6 of 8 models. Escalating and hacking were
  almost mutually exclusive (98.7% of escalations involved no hacking), and
  escalation reports were more accurate than monitoring at finding the
  real defect (99.4% against 85.8%). (Gomez 2026, arXiv 2608.29460)
  - *Suggests:* keep the rule that reporting a part undone never counts
    against a worker, and give it a first-class action ("this task is
    broken because…") whose reports are themselves checked.

## Stated confidence is a strategic act when it decides allocation

- **A proper scoring rule alone does not make confidence honest when the
  report also wins work.** With top-K selection on stated confidence, LLM
  agents inflated their confidence. The proper-score loss from a small
  overstatement is tiny, while crossing a selection threshold pays a
  discrete gain. Compensating for the allocation benefit (or a pivot
  mechanism with sparse, inverse-propensity-weighted audits) restored
  truthful reporting in theory and reduced distortion in experiments.
  (Zhou et al. 2026, arXiv 2610.33728)
  - *Suggests:* do not route on what a worker says about itself. Route on
    outcomes judged by others; score stated confidence for calibration
    only, and make audits random and independent of the stated confidence.
- **Verbalized confidence from reasoning models is often overconfident**
  unless trained for calibration (several 2026 papers, e.g. arXiv
  2609.33290, 2609.32470). Calibration is something to measure per worker,
  not assume.

## Judges are biased by whose work they think it is

- **Labels alone shift LLM judges.** With quality held fixed, judges
  inflated scores for work labelled as their own and deflated work labelled
  as another's, whatever its true source; under blind evaluation the
  self-preference disappeared. (Chae et al. 2026, arXiv 2608.18091)
  - *Suggests:* review blind: the reviewer sees the work, not who made it.

## Routing: most of the gain is the task type, and noise is large

- **A static table per task type captured most of what routing could
  gain.** Fourteen models on 294 questions: of the 29 questions routing
  could improve, assigning one model per task type, fixed in advance,
  improved 21. Running the whole matrix twice with nothing changed scored
  5.37% of model-question pairs differently, more than the remaining gain
  a learned router could have captured. (Lee 2026, arXiv 2608.23023; it
  fits and scores on the same questions, so it is indicative.)
- **Commercial dynamic routers did not beat random choice between two
  well-chosen models** at matched cost, across 14 settings; some lost by
  more than 10 points. (Wang et al. 2026, arXiv 2610.02762)
  - *Suggests:* a card per worker and kind of work is about the right
    grain; per-query cleverness is unlikely to pay. Any claimed win must be
    larger than run-to-run noise, measured by running twice. The baselines
    must include a static per-kind table and random choice between two
    good models, not only "always the strongest".

## Already in Polymechania, and what it rests on

- No self-grading; agreement between copies of one model counts once;
  verdicts only from outside the worker's group (Gnomon's gate). Supported
  by the self-preference and trace-tampering findings above.
- Hidden tests graded the pilot. Supported by SpecBench.
- Reporting a part undone is never counted against a worker. Supported by
  the escalation-channel study.

## Classic theory used

- **Goodhart's law**: a measure that becomes a target ceases to be a good
  measure.
- **Proper scoring rules** (Brier 1950; Gneiting and Raftery 2007): a
  forecaster maximises expected score only by reporting its true belief,
  when the score is its only payoff.
- **Random audits** (Becker 1968 on enforcement): deterrence depends on the
  chance of being checked times the penalty; audits that cannot be
  predicted cannot be selectively prepared for.
- **Hierarchical pooling** (partial pooling of rates across related
  groups; Gelman et al., *Bayesian Data Analysis*): between treating every
  kind of work as unrelated and treating all as one.
