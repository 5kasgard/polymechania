# μ polymechania

**The right worker for every part of the work: models, solvers, scripts and checks, organised by price and track record.**

![Python: standard library only](https://img.shields.io/badge/python-standard%20library%20only-informational)
![Record: Gnomon](https://img.shields.io/badge/record-gnomon-informational)

*Polymechania* (πολυμηχανία) is the Greek word for the gift of many devices.
It is what Homer gave Odysseus: he won not by strength but by reaching for
the right contrivance every time.

Most agent systems send everything to the strongest model and hope.
Polymechania does the opposite. Each part of a job goes to the cheapest
worker that does it reliably on the record, and is checked by something
other than the worker:

- **Arithmetic goes to a calculator,** a proof to a prover, a test to a
  test runner. They are never wrong about what they check, and nearly free.
- **A repeated chore goes to a script** a model writes once. On spam
  filtering, a linear model matched Claude Haiku for almost nothing.
- **What only judgement can do goes to a model,** the cheapest tier first,
  escalating only when a check fails. On 24 exactly specified tasks,
  Haiku got every one right.
- **Nobody grades their own work.** Copies of one model count as one
  witness. Every order, result and verdict goes into
  [Gnomon](https://github.com/5kasgard/gnomon), and who does what next
  follows that record.

## One organisation, any world

Everything happens in plain terms. How it is *shown* is up to you: a
**world** renames everything, retells it in its own voice and gives it its
own look. Here is the same plan three times.

Plain:

```
μ polymechania
task: 24 part(s) of 'code', moderate ($5.00 at stake each), check: checked exactly
  planner: 1 × Opus
  worker: 24 × Haiku
  escalation: 10 × Sonnet
  each part: Haiku then Sonnet then Opus then Fable, checked exactly (right 99.96%)
  expected: $1.44 on tokens + $0.0480 lost = $1.49; 6 round(s) at most
  one Opus alone: $16.38; 24.0 round(s) expected
```

Kagamigakure, the Village Hidden in the Mirror:

```
鏡 polymechania · Kagamigakure
📜 A B-rank mission reaches the gate: 24 scroll(s) of 'code', $5.00 at stake on each, sealed by the Soroban clan.
  strategist: 1 × jōnin
  squad: 24 × genin
  reinforcements: 10 × chūnin
  each scroll: genin backed by chūnin backed by jōnin backed by sōke, sealed by the Soroban clan. Chance of success 99.96%.
  the treasury expects $1.44 in tokens, $0.0480 in losses: $1.49 in all, within 6 round(s).
  a lone jōnin would cost $16.38 and take 24.0 round(s).
```

Hollow Acre, a farm:

```
🌾 polymechania · Hollow Acre
🌱 New job on the board: 24 row(s) of 'code' (harvest, $5.00 riding on each), weighed on the scales.
  crew: 24 × farmhand
  second pass: 10 × foreman
  each row: farmhand then foreman then farm manager then agronomist, weighed on the scales; 99.96% come up good.
  seed and feed $1.44, spoilage $0.0480: $1.49 for the lot, done in 6 pass(es).
```

A world can rename anything, retell anything and look like anything. It
cannot change a number, leave out a fact or touch a rule:

- **Every retold event must state every fact.** A world whose cost line
  drops the losses is refused.
- **Numbers are never reworded.** The tests render every event of real
  plans in every world and check that each value appears unchanged.
- **Rules are not read from worlds at all.** A world can give "no one
  grades their own work" a line of its own ("No ninja grades their own
  mission"), never a different meaning.
- **Plain is always underneath.** `--both` prints every line in the
  world's words with the plain line under it; `--plain` drops the world.

Make your own with `mekh world new`: you get a file listing every concept,
event and rule in its plain form, ready to rename. Make it a pirate crew,
a hospital, a newsroom or a tea house. Polymechania is the world; each
organisation is a region in it, and the map (next) will show them side by
side, each in its own style.

## Quick start

Python 3.11 or later. Nothing else for planning, forms and worlds.

```bash
git clone https://github.com/5kasgard/polymechania && cd polymechania
pip install -e .                  # puts `mekh` on your path

mekh plan code --parts 24 --input 20000 --output 3000 --stakes 5 --check exact
mekh form --parts 24 --check exact --families 3 --locatable
mekh rules --world kagamigakure
mekh worlds
mekh world show kagamigakure
mekh world use kagamigakure       # make it your default
mekh world new my-world           # start your own
```

`--json` on any command gives the plan or design and its plain events.

Running an organisation with titles, staff and verdicts (`polymechania.org`)
keeps its books in Gnomon. Build Gnomon beside this folder, or set
`GNOMON_PYTHON` to its `python/` folder.

## Measured

Everything below was measured while this lived inside Gnomon, and is
reproducible from `bench/`.

### The pilot: real work, graded by the computer

Twenty-four Python tasks with exact specifications went to Claude
sub-agents, one task per agent. Half were routine (slugs, Roman numerals,
intervals, an LRU cache) and half hard (a linear-time regex engine, a
Sudoku solver for minimal puzzles, exact linear algebra, UTF-8 decoding
with maximal-subpart replacement, maximum flow, best rational
approximation to 10^18). Hidden tests, checked against reference
solutions, graded each result (`bench/pilot`).

| | Routine | Hard | Median time |
|---|---|---|---|
| Claude Haiku 5.5 | 12/12 | 12/12 | 22 s |
| Claude Sonnet 5.5 | 12/12 | 12/12 | 12 s |

On work this well specified, and checkable this exactly, the cheapest
model did everything right, at a fortieth of Opus's price per token. The
firm's job here is not to pay for more model than the work needs. Every
result and verdict is recorded in a memory as the firm's books, and
the planner then plans from them (`python bench/pilot/run.py`).
For 24 more such parts, it expects Haiku staff with exact checks and
escalation to cost $0.38 in tokens, against $0.92 for one Sonnet agent
and $1.84 for one Opus agent.

What the pilot does not show yet is where escalation earns its keep: no
task here defeated Haiku. That needs longer, vaguer, multi-step work, and
it is the next measurement.

### The floor: many cheap workers, measured

Can lots of very cheap workers do the grunt work instead of one capable
model? Measured on three real, human-labelled workloads (`bench/floor`,
protocol fixed in advance in `bench/floor/PROTOCOL.md`): 5,574 SMS
messages (spam or not), 10,000 Yelp reviews (which star rating, 1-5), and
the same reviews as positive or negative. The cheap workers: a program
written once from general knowledge, naive Bayes (every word a dumb
voter), a swarm of 300 boosted one-question stumps, Mycel's dumb nuclei
(github.com/5kasgard/mycel, in the configuration its own protocol froze),
and a linear model. The capable worker: Claude Haiku, reading and judging
300 items of each. Cheap workers are scored on 2,600-4,800 items none of
them trained on.

| | Spam | Stars (exact) | Sentiment | Cost per million items |
|---|---|---|---|---|
| Program, no labels | 98.5% | 37.4% | 86.1% | under 1 cent (12,000-100,000 items per CPU-second) |
| Swarm of 300 stumps, all labels | 97.2% | 45.1% | 87.9% | under 1 cent |
| Mycel, all labels | 97.4% | 44.3% | 86.9% | under 1 cent |
| Linear model, 1,000 human labels | 98.7% | 48.8% | 90.5% | about 1 cent |
| Linear model trained on 300 Haiku labels only | 97.9% | 44.6% | 85.4% | about 1 cent, plus under 1 cent of labelling |
| Claude Haiku, every item | 99.7% (98.1-99.9) | 66.0% (60.5-71.1) | 92.5% (88.6-95.2) | $9.81 spam, $23.09 reviews (Opus: $392, $924) |
| **Floor**, escalation share chosen on half the probe, scored on the other | 99.7%, nothing escalated | no saving: it escalates everything | 92.5% at $3.46 | |

What this says, and how sure it is:
- **Narrow, easy work: the floor wins outright.** On spam the linear model
  alone matched Haiku on the probe for almost nothing (on the larger
  evaluation set it scored a point lower, so the probe flatters it a
  little).
- **Fuzzy work: no free lunch.** On star ratings no cheap worker came close,
  and the floor's choice, made out of sample, was to send everything up.
- **In between, it depends on details.** On sentiment the floor matched
  Haiku at a seventh of the cost, but Haiku was asked for stars and said
  "3" on 18 of the 254 items; counted as wrong, that lowers Haiku to 92.5%.
  Read as positive, Haiku scores 98.0% and the floor falls short (96.1% at
  $8.08); read as negative, they tie (94.1% and 94.5% at $4.62). An
  independent review caught this; all three readings are in
  `results.json`.
- **Many dumb nodes do not beat one simple model on text.** The swarm of
  stumps and Mycel's nuclei landed together, a point or more below one
  linear model. A first Mycel configuration of our own choosing barely
  learnt at all (it is still reported, as `mycel-1st`); Mycel's own frozen
  configuration did far better, so how it is set up matters more than
  anything here. Mycel was built for numeric streams, not text.
- **Cautions.** 300 items per probe gives intervals of ±2-5 points; the
  spam program was written by a model that may have seen this dataset;
  Haiku's price makes per-item calls already cheap, so the floor's case is
  strongest against higher tiers and at very large volume.

The 2026 literature says the same at larger scale: an agent that builds a
cheap artifact for a workload can keep 95% of its quality at 889x lower
cost, but most agents lost a quarter or more and many lost to a naive
distilled 0.6B model (arXiv 2610.08775); a small model running an adapter
compiled by a bigger one beat prompting a 32B model per input
(2607.02512); two tiers beat one by 2-8 points but a third adds nothing
(2605.06350); batching 25-100 items per request cuts cost by 80% for under
2 points (2604.03684).

So the firm now has a toolmaker, a floor and batching among its forms
(`T`, `F`, `N`): for a workload, build the cheap worker once, check it on a
probe the model labels, let it answer what it is sure of, and send the rest
to one capable tier in batches. `mekh form --repeats` proposes this whenever there
are thousands of items under one instruction.

### Agents are not people

Organisation science was written for people. Models have different
strengths and weaknesses, and the forms follow the measurements, not the
analogy:

| Cheap for models | Hard for models | So the firm |
|---|---|---|
| Cloning a worker, instantly, any number | Copies of one model are not independent: they fail together | draws on several model families, and counts copies of one model once |
| Changing role mid-task (no retraining) | Judging their own work: self-critique lost to simply sampling again at equal cost | never lets a worker grade itself; counts votes, runs a check, or asks someone outside |
| Writing a program for a repetitive job | Knowing when they are wrong (confidence is a weak signal) | builds the cheap worker, then measures it on a probe before trusting it |
| Reading fast, working in parallel without fatigue | Deferring to an expert: teams average the expert away | routes to the expert instead of holding a meeting |
| Starting fresh, without fatigue or grudges | Remembering anything between sessions | keeps its memory in the record |

### Forms: an alphabet, not one org chart

How a team should be organised depends on the work, and 2026's controlled
studies of model teams say a good deal about when each arrangement helps.
`polymechania.forms` turns that into nineteen letters (divide, assign, propose
independently, select by a check, route to the expert, take turns,
aggregate, critique, debate, bid, coordinate through the record, evolve,
floors, escalate, independent assurance, solo, and for workloads a toolmaker, a floor of cheap workers, and batching), each with when it helps,
when it hurts, and its evidence. A task's profile and five dials (effort,
breadth, scrutiny, speed, thrift) spell a word:

```
exact check, 24 parallel parts, 3 model families:
  C·D[16]·P[3]·V·K·X·I    assign up front; 16 at once (Amdahl's knee); 3 independent attempts
                          across families; the tests pick; one repair if a test names the fault;
                          cheapest tier first; assurance outside the workers' group
open-ended design, Opus available:
  Q[4]·A·I                four agents in turn, each reading the others' finished work and
                          choosing its own role or abstaining; a draft from another family
                          merged in; one independent reviewer
six tightly coupled steps, Opus, reviewed:
  S·P[2]·X·I[3]           one context (splitting loses detail a strong model would use);
                          two attempts; three reviewers from distinct groups, majority rule
```

Each choice names the finding behind it, and the design lists what it
rejected: no debate when there is an exact check (reading each other's
full solutions erased model diversity within one round), no deliberation
around a known expert (teams fell 6-41% short of their best member), no
more than four voices, no self-claiming of work. The rules are priors: a
contextual bandit (`Learner`) chooses among a short list of candidate
forms and moves off the prior as the firm's record shows another paying
better. Sources and the full rules are in the
[spec, section 3](spec/polymechania-v0.1.md#3-forms-an-alphabet-not-one-chart).

## What's in it

| | |
|---|---|
| **The planner** | `plan`: prices every way to do a part (each tier alone, each rising cascade, under each check the work allows) as tokens plus expected loss plus waiting, from published prices and the verdicts on record. Shapes the team: staff, managers by span of control, a planner, escalations, reviews. Compares it with one agent doing everything alone. |
| **Forms** | `forms`: nineteen letters, each with when it helps, when it hurts and its evidence, spelt into a word for each piece of work, and a learner that moves off the rules as the record shows another form paying better. |
| **Organisations** | `org`: a company in the Gnomon record, founded with its powers kept apart, staffed by hiring model instances into titles, reviewed from independently judged results. |
| **Worlds** | `concepts`, `events`, `worlds`: the plain vocabulary, the events every view reads, and TOML worlds that change the telling and nothing else. |
| **mekh** | The terminal view. |

The full rules are in the [spec](spec/polymechania-v0.1.md).

## Roadmap

- [x] **The planner, forms and organisations,** moved from Gnomon with
  their history, tests and benchmarks.
- [x] **Worlds and `mekh`:** Plain, Kagamigakure, Hollow Acre; make your own.
- [ ] **The runtime:** a register of workers (calculators, test runners,
  solvers, provers, scripts, models), dispatch by the planner, every
  order, result and verdict in Gnomon.
- [ ] **The dashboard:** a running organisation, full screen in the terminal.
- [ ] **The map:** Polymechania as a graphical world, every organisation a
  region drawn in its own style.
- [ ] **Measured against one agent alone** on long, vague, multi-step work.

## Layout

```
polymechania/   plan, forms, org, concepts, events, worlds, cli (mekh)
  worlds/       plain, kagamigakure, hollow-acre
tests/          the planner, forms (and stress), organisations, worlds and mekh
bench/pilot/    24 tasks given to Haiku and Sonnet, graded by hidden tests
bench/floor/    cheap workers against Haiku on SMS spam and Yelp reviews
spec/           the rules
```

```bash
python3 -m unittest discover -s tests
```

## Licence

Not yet chosen. Until a licence is added, the code is visible but no
permission to copy, modify or redistribute it is granted.
