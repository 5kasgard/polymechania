# Independent review of `cards-v2.md`

A second separate agent (Claude Opus 5.5) checked v2 against the first
review, the mechanism code and the power simulation, before any data, and
edited nothing. 18 findings: 7 must fix, 8 should fix, 3 minor. Summarised
here; how each was handled is amendment 1 of `cards-v2.md`.

**First review's must-fix items:** 3, 15, 16, 21, 22 adequate; 5, 9, 10, 12,
13, 17 partly; 11 not.

1. **(2.1, must)** A "broken" report the judge accepted was dropped from the
   card and never audited: an attacker could call every hard item broken.
   Planted items had no defined audit truth; a false report on a planted
   item deflated honest workers.
2. **(2.2, must)** Declining: inflation is zero by definition for an agent
   that declines its hard items; the code counted declines as failures while
   the text left them out.
3. **(2.3, must)** Answers can still reach workers: session transcripts on
   disk hold the conductor's context (the key, the audit secret, earlier
   answers); the Yelp source file is fetchable over the network (HTTP 200
   checked), and item ids are row numbers; the W2 generator with a public
   seed regenerates answers; the pre-registration tells honest workers they
   are in an experiment.
4. **(2.4, should)** Fooling the routine check adds noise, and noise is a gain
   under top-K assignment or retirement.
5. **(2.5, should)** Under the designed card, expected inflation on answered
   items is exactly zero by construction; H1b can only fail through broken
   reports and declines. Compute it exactly.
6. **(2.6, should)** Planted W1 items (unrelated passages) are trivially
   detectable.
7. **(2.7, should)** The power claim was a closed formula without the
   reviewer's own errors; for the no-audit arm the smallest detectable
   difference is nearer 8 points than 4-5.
8. **(2.8, should)** H1a can be met trivially under -D2 (copy the visible
   check); require a non-trivial channel and correct across ablations.
9. **(2.9, must)** Economy arms: in W2 an audit can never contradict an exact
   routine check, so penalties never trigger; one run per arm with no
   paid-honest control; an Opus judge of Claude transcripts breaks D1 and
   cannot be blind; Gemma is weak on long transcripts.
10. **(2.10, must)** Steering: no external timestamp (*the reviewer did not
    find the git history: the pre-registration is committed and pushed to
    GitHub, commits a9863df and 98f7795, which is an external timestamp*);
    attacker prompts not fixed in advance; no trigger for the Gemma-to-Llama
    switch; "defeated" undefined in the rounds rule; no rule if W2
    calibration misses 65%, Sonnet may be at ceiling; the reviewer's
    disagreement rate not measured in advance.
11. **(2.11, minor)** What the reviewer sees for malformed output; stale
    docstring; declining runs not paired with honest runs.
12. **(3.1-3.3)** "Models recognise their own family's output" is an
    extrapolation (a precaution, not a fact); "fooling gains nothing" holds
    only for answered items and ignores selection effects; evidence.md's
    "never counted against" conflicts with D5's false-report failure.
