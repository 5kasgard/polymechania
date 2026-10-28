# The evidence model: how Polymechania knows which worker is best for what

Status: **hypothesis**, 2026-10-29, written with the owner. It says how
external evidence (benchmarks, leaderboards, papers, vendors' claims) and
internal evidence (our own pre-registered tests, and the record of real
work) combine into the stat cards that routing reads (`docs/routing.md`,
`polymechania/cards.py`).

## What the outside research says (the starting point)

- **Benchmarks disagree, most at the top.** Across 40+ benchmarks, the top
  three models are almost never in the same order; agreement checks need
  10 or more models to be stable ([BenchBench, arXiv
  2407.13696](https://arxiv.org/abs/2407.13696)).
- **Contamination raises scores but rarely reorders them.** A leaderboard
  and a paraphrase-controlled one correlated at 0.997 in rank (47 public
  models; [arXiv 2609.02899](https://arxiv.org/abs/2609.02899)), though
  some single models gain up to 14 points on leaked items
  ([Li et al. 2024](https://aclanthology.org/2024.findings-emnlp.30.pdf)).
- **Matching the test to the real work is what makes it predictive.**
  Benchmark items chosen to resemble real user queries agreed with human
  preference at 0.96 ([MixEval, NeurIPS
  2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/b1f34d7b4a03a3d80be8e72eb430dd81-Paper-Conference.pdf)).
- **Item response theory puts different tests on one scale**: each item
  has a difficulty and a discrimination, each model an ability; 1,000
  well-chosen items ranked models nearly as a full arena did (Kendall's
  0.90; [AAAI 2026](https://doi.org/10.1609/aaai.v40i41.40814)).
- **Model judges are biased** (position, length, self-preference;
  `docs/routing.md` section 3), so judged scores are evidence of a weaker
  kind than exact checks.

## The model

1. **Every piece of evidence is an entry in the record**, with: source;
   kind of work; metric; number of items; model and version; date; who
   ran it and whether they had a stake (a vendor scoring itself); how it
   was checked (exact, judged by which family, human); and contamination
   risk (public items, age).
2. **One scale per kind of work.** A worker's ability on "exact Python
   functions", "summaries", "routing decisions" and so on is a single
   estimate, fitted from every result that bears on it (IRT-style:
   abilities for workers, difficulties for items), not a separate number
   per benchmark.
3. **External evidence is the prior; ours moves it.** External results set
   the starting ability and its uncertainty; each internal verdict from
   outside the worker's family updates it (the Beta update already in
   `cards.py` is the simplest case).
4. **Weight by relevance.** A result counts in proportion to how much its
   items resemble our work orders (MixEval's lesson), measured by
   embedding similarity or by hand-labelled kind of work.
5. **Sources have stat cards too.** A benchmark, leaderboard or reviewer
   whose past predictions matched our internal results gets more weight;
   one that did not gets less. This is how the system learns whom to
   believe, rather than being told.
6. **Order over level.** Use rankings and gaps from external sources more
   than absolute scores, since contamination shifts level more than order.
7. **Spend only where a test could change the decision.** If external
   evidence already separates the candidates for a kind of work by more
   than its uncertainty, route without testing. If the decision hinges on
   models close at the top (where benchmarks disagree most), test on our
   own work, cheapest engine first. This is the budget rule made
   principled (value of information).
8. **Exact beats judged beats claimed:** an exact check counts fully; a
   blind judge from another family counts less, more with two families
   agreeing; a vendor's own claim is a prior only.

## What we have today

Internal: T2 (Haiku and Sonnet on 24 pilot tasks, exact), T2b/T2c, T12b-d
(two model families, exact plus two blind judges), S1 (speed), the pilot
and floor benches. External: none recorded yet as entries.

## First test

**E-ext** (`queue.json` q03): do public benchmark rankings predict our own
results on the pilot tasks, across 6-10 models (most free on Workers AI)?
If they do, external evidence can carry more weight and fewer internal
tests are needed; if not, internal tests on our own kinds of work are
where the budget should go.
