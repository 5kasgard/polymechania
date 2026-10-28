# Routing: every part of the work to the worker that fits it best

Status: **hypothesis**, written with the owner 2026-10-29; revised the same
day after two separate reviews (`docs/routing-review-haiku.md`,
`docs/routing-review-llama.md`). Applies to
Polymechania's planner *and* to how any session (any chat, any engine)
does its own work: the session is an organisation too. Every rule here is
to be tasted and adjusted by the record, never imposed.

## 1. Who can be a worker

Not only Anthropic's models, and not only models:
- **Closed models** from any provider (Claude tiers, others), each a
  different family with different strengths.
- **Open-weight models** (Gemma, Llama, Qwen and others), run on Workers
  AI, Hugging Face, or the owner's machine; base models, fine-tunes,
  adapters and quantised versions are different workers.
- **Small learners** trained or fitted for one workload (a linear model, a
  classifier); `bench/floor` found one matching Haiku on spam for almost
  nothing.
- **Tools, downloaded or built:** solvers, provers, test runners,
  calculators, parsers, search. Built-or-downloaded is itself priced
  (below).
- **Scripts written once** by a toolmaker for a recurring job.
- **People:** the owner, collaborators.

## 2. What decides the route

Each is a field on a worker's stat card, measured where possible and
stated as an assumption where not.

| Dimension | Question | Measured by |
|---|---|---|
| **Strength by kind of work** | How often does it get *this kind* right? | verdicts from outside its group, per frame (`cards.py`) |
| **Reliability and calibration** | When it says it is sure, is it? Does it fail loudly (empty, refused) or quietly (wrong)? | Brier score; T2's empty answers are a loud failure |
| **Cost** | fixed per call (boot), marginal per token, setup (building or downloading), upkeep | logged usage; `bench/boot` |
| **Build or download** | Is a tool that exists cheaper over its lifetime than one built here? | setup + upkeep + licence against build cost |
| **Speed** | time to a result, and rate limits | logged wall time; plan limits (`docs/engines.md`) |
| **Context and modality** | Does the part fit its window? Text, code, images? | spec; refuse if not |
| **Settings** | thinking, effort, temperature, prompt: part of *which worker* it is | T2b/T2c: Haiku with thinking off is a different worker from Haiku by default |
| **Character and voice** | Does the work need a voice (a guide, a letter) or none (code)? Which personality fits? | judged blind (T12) |
| **Where it runs and privacy** | May this data leave the machine? Whose account pays? | compartment rules; the owner's choice |
| **Licence and terms** | May it be used this way? | the provider's terms |
| **Independence** | For a *check*, is it from a different family than the worker? | family on the card |
| **Availability and load** | Is it up, within limits, affordable this window, and how much is already queued on it? | live headroom and queue (spec section 7) |
| **Evidence behind the card** | How many verdicts is each value built on? A strength from 3 verdicts does not route like one from 300 | the count on every card value; the Beta prior's width |
| **Version** | Is the card about this exact model or tool version? | re-test on any model revision, deprecation or tool upgrade; old verdicts kept, marked |

**The decision** stays the planner's (spec section 2). The dimensions are
its inputs: some are hard limits (fits, allowed, may run here,
independent check, available), the rest are priced into one number, the
expected cost plus the expected loss from a wrong result. The lowest
total wins. Cheapest is the tie-break, not the goal: a cheap worker that
is often wrong costs more.

**Start simple.** A large routing benchmark found many routers, commercial
ones included, did not reliably beat a simple baseline, with a large gap
left to a perfect router mostly from picking the wrong model
([LLMRouterBench, arXiv 2601.07206](https://arxiv.org/abs/2601.07206)).
So the first router is the cascade by kind of work, measured (T2: cached
Haiku then Sonnet passed 24/24 at a quarter of Sonnet's price), and it
earns complexity only when the record shows a gain at least as large as
the threshold its pre-registration names.

## 3. Unbiased testing (applies to every test)

Model judges are biased: GPT-4 kept its verdict only 65% of the time when
two answers were swapped; Claude-v1 rated its own answers about 25 points
higher, and padded answers fooled weaker judges 91% of the time
([Zheng et al. 2023, arXiv 2306.05685](https://arxiv.org/pdf/2306.05685)).
So:

1. **Pre-register** question, arms, measures, decisions and the threshold
   for a gain before any run; commit it first. A test is amended only
   before its data. Adjusting a hypothesis by what the record shows
   happens *between* tests: the adjusted hypothesis gets a new
   pre-registered test, never a rewritten old one.
2. **Exact checks first:** tests, graders, arithmetic and scripts decide
   whatever they can. A model judges only what nothing exact can (voice,
   clarity, whether a claim is overstated), and then under rules 3 and 4.
3. **Judges from another family** than every worker judged, and at least
   two families when a model judges; never a worker's own family alone.
   When a Claude worker is judged, at least one judge is not Claude; a
   Claude judge may be one of several, never the only one. Each judge's
   tier is stated, and where the answer could depend on it, a cheap judge
   is run beside a strong one, so a strong judge's taste for expensive
   answers shows.
4. **Blind and shuffled:** judges never see which arm, model or vendor
   produced a reply; order randomised with a fixed seed; pairwise judging
   run both ways round. Labels are hidden but style is not, so length is
   recorded with every judged reply and reported beside the scores; where
   lengths differ much, judge length-matched pairs or say the score may
   reward padding.
5. **Same conditions for every vendor:** same prompt, budget, caps and
   retries; settings (thinking, effort, temperature) are fixed in the
   pre-registration, not chosen after seeing results. Where settings are
   tuned for one vendor, they are tuned the same way for every vendor, or
   each vendor is run at its documented default as well.
6. **Include the cheap and open options** as arms, not only the tiers of
   one provider; report every arm, including those that lose.
7. **The author's bias is stated and checked:** who wrote the prompts,
   knowing what (T2's self was written knowing the tasks); prompts are
   identical across arms, and the prompts and pre-registration are
   reviewed by someone other than the author before the run.
8. **Audit separately:** numbers by script (`bench/verify.py`), always;
   judgement by an agent of a different family or tier than the author,
   and its findings applied in the open.
9. **Budget is a condition:** each pre-registration states its API cost
   bound and which free engines it uses. Without the owner's approval, no
   single test spends more than a tenth of the API credit left (see
   `HANDOFF.md`, "Budget").

## 4. This session as an organisation

Any session doing this work routes its own parts the same way: published
results and existing data first; scripts for anything exact; free engines
(Workers AI, the owner's Pro sub-agents) for bulk and judging; the
cheapest Claude tier that passes for short judgement; the strongest
model only for planning, design and integration. Each part done is
logged (`bench/ledger.jsonl`: what, which worker, cost, verdict) so the
session's own work becomes data for the cards.
