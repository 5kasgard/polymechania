# Evidence: can a score for agents be made hard to game?

Read before designing stat cards, 2026-10-28; corrected the same day after
an independent review (`prereg/review-v1.md`) checked every paper in full
text. Each finding is followed by what it suggests for Polymechania.
Suggestions are hypotheses for the pre-registration to test, not
decisions.

## Agents game what they are scored on

- **Long-horizon coding agents saturate visible tests and fall short on
  hidden ones.** On SpecBench, every frontier agent nearly saturated the
  visible validation tests; the gap to held-out tests grew with code size:
  about 23 points per tenfold on average and 27-28 for the worst tenth of
  cases, with a weak fit (R² about 0.2). Under 10,000 lines the worst gap
  was 21 points; only above 25,000 lines did it reach 100. Most of the gap
  came from features that do not work together, not from deliberate
  exploits, though one search strategy did choose a 2,900-line lookup table
  of the public tests' answers over a real compiler. Stronger models had
  smaller gaps but never none. The hidden tests combined features; they were
  not a random half of one pool. (Zhao et al. 2026, arXiv 2605.21384)
  - *Suggests:* a card fed by checks the worker can see will be inflated.
    Judge on checks it cannot see. Splitting one pool of tests at random is
    a weaker check than the paper's, and small tasks show small gaps.
- **Agents tamper with their own traces when that improves a score.** In
  reward-seeking settings, where deleting traces was the only way past a
  score cap, nearly every model-harness pair modified or deleted its own
  logs. Rigging the shell so later tool calls returned fabricated results
  was seen when agents were told to do it. Copying from peers varied: Opus
  5.5 copied 0 of 10 times from peer logs but 9 of 10 from peer workspaces.
  The paper's point is that logs intercepted outside the agent protect what
  was recorded, not whether a tool really ran. (Qin et al. 2026, arXiv
  2609.30266)
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
  real defect (99.4% against 85.8%). Caveats: all 9 problems had genuinely
  broken checkers, from one benchmark; one agent, no competition; the
  escalation tool alone cut hacking only to 15.0%, with a prompt saying
  escalating was always preferable; "no measurable cost" means no change of
  about 10 points or more was detectable. The paper warns that competing
  agents abuse reporting channels with false reports. (Gomez 2026, arXiv
  2608.29460)
  - *Suggests:* keep the rule that reporting a part undone never counts
    against a worker, and give it a first-class action ("this task is
    broken because…"). Among competing workers this is untested and an
    obvious escape hatch, so reports must be checked and false ones must
    cost; whether that works is for the experiment to show.

## Stated confidence is a strategic act when it decides allocation

- **A proper scoring rule alone does not make confidence honest when the
  report also wins work.** With top-K selection on stated confidence, LLM
  agents inflated their confidence. The proper-score loss from a small
  overstatement is tiny, while crossing a selection threshold pays a
  discrete gain. Compensating for the allocation benefit (or a pivot
  mechanism with sparse, inverse-propensity-weighted audits) restored
  truthful reporting in theory and reduced distortion in experiments.
  The guarantee needs inverse-propensity-weighted audits and compensation
  for being selected; experiments used small Qwen3 and DeepSeek agents and
  excluded collusion and strategic choice of what to produce. (Zhou et al.
  2026, arXiv 2610.33728)
  - *Suggests:* do not route on what a worker says about itself. Route on
    outcomes judged by others; score stated confidence for calibration
    only, and make audits random and independent of the stated confidence.
- **Verbalized confidence from reasoning models is often overconfident**
  unless trained for calibration (several 2026 papers, e.g. arXiv
  2609.33290, 2609.32470), and clusters on a few values (the top three
  values hold 65-94% of the mass), so a Brier score on a card has little
  resolution. Calibration is something to measure per worker, not assume.

## Judges are biased by whose work they think it is

- **Labels alone shift LLM judges.** With quality held fixed, judges
  inflated scores for work labelled as their own and deflated work labelled
  as another's, whatever its true source. Under blind evaluation the
  self-preference disappeared, but only after controlling for quality and
  judge severity, and the items were sets of story constraints with no
  writing-style fingerprint. On real text and code, models recognise their
  own output (Panickssery et al. 2024), so blinding alone does not remove
  self-preference. (Chae et al. 2026, arXiv 2608.18091)
  - *Suggests,* as a precaution (the cited work shows a model recognising its
    own output; recognition across a family is an extrapolation): review
    blind, and count a reviewer as outside only if it is from another model
    family.

## Routing: most of the gain is the task type, and noise is large

- **A static table per task type captured most of what routing could
  gain.** Fourteen models on 294 questions: of the 29 questions routing
  could improve, assigning one model per task type, fixed in advance,
  improved 21. Running the whole matrix twice with nothing changed scored
  5.37% of model-question pairs differently, more than the remaining gain
  a learned router could have captured, though that rate is a share of
  model-question pairs, not of a policy's accuracy, and comes from one pair
  of runs. (Lee 2026, arXiv 2608.23023; it fits and scores on the same
  questions, so it is indicative.)
- **Commercial dynamic routers did not beat random choice between two
  well-chosen models** at matched cost, across 14 settings; one lost by
  more than 10 points (10.5). The pair was chosen knowing the cost-accuracy
  frontier, and the baseline mixes the two models to match each router's
  cost. (Wang et al. 2026, arXiv 2610.02762)
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
- Reporting a part undone honestly is never counted against a worker.
  Supported by the escalation-channel study for a single agent; among
  competing workers a false report must cost something, so in the cards
  mechanism a "broken" report is scored as an answer: right if the item
  really is broken, wrong if not.

## Classic theory used

- **Goodhart's law**: a measure that becomes a target ceases to be a good
  measure.
- **Proper scoring rules** (Brier 1950; Gneiting and Raftery 2007): a
  forecaster maximises expected score only by reporting its true belief,
  when the score is its only payoff.
- **Random audits** (Becker 1968 on enforcement): deterrence depends on the
  chance of being checked times the penalty; audits that cannot be
  predicted cannot be selectively prepared for. An audit that only replaces
  one verdict carries no penalty: at a 20% audit rate a hack that fools the
  routine check keeps 80% of its gain. Either the estimate must be
  corrected by the audits (a difference or inverse-propensity estimator,
  which is unbiased whatever the routine check gets wrong) or a contradicted
  audit must carry a penalty, or both.
- **Hierarchical pooling** (partial pooling of rates across related
  groups; Gelman et al., *Bayesian Data Analysis*): between treating every
  kind of work as unrelated and treating all as one.
