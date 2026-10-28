# Polymechania v0.1

The rules of Polymechania: how work is shared between models, solvers,
scripts and checks; how an organisation is shaped and judged; and how it is
shown in any world a person likes. Gnomon keeps the record; this spec
covers what is done with it.

## 1. The principle

Every part of a piece of work goes to the cheapest worker that does it
reliably on the record, and is checked by something other than the worker.

- **Workers are not only models.** A calculator, a theorem prover, a test
  suite, a script written once or a swarm of tiny learners is a worker. A
  model is the worker of last resort for what nothing cheaper can do, and
  the toolmaker for what something cheaper could do if it were built.
- **Checks are not the worker.** No one grades their own work, no model
  judges its own model's work, and copies of one model are one witness.
- **The record decides.** Who does what follows verdicts on past work from
  outside each worker's group, kept in Gnomon. Escalating, asking for help
  or reporting a part undone never counts against anyone.
- **Plain underneath.** Everything is recorded in the plain vocabulary of
  section 4. A world (section 5) changes only how it is shown.

## 2. The planner: who does each part

A request that can be split is work for an organisation. `polymechania.plan`
(`mekh plan`) shapes one: who does each part, who checks it, who it
escalates to, how many managers on how many floors, and what that is
expected to cost and risk next to one top-tier agent doing it all.

| A firm has | Here it is |
|---|---|
| Pay grades | Tiers priced from the published per-token prices (Haiku, Sonnet, Opus), read on the date in `PRICES_READ`. |
| Desks | Context windows. Staff desks stay under Haiku's 100,000-token price rise; a manager's desk sets how many reports fit on it. |
| Floors | Levels of management: a new floor when one floor of managers would have more than a desk's worth of reports. |
| The executive | The top tier plans the split and integrates the parts: a mistake there costs every part. |
| Quality control | An exact check (tests, arithmetic, dates: free and certain), a reviewing tier (priced, with a stated catch and false-alarm rate), or none. |
| Escalation | A cascade: the cheapest tier first, the next only when a check fails. |
| The night shift | Work that is not urgent goes to the Batch API at half price. |
| Work orders | A question in a `firm/<kind>` frame, posted by whoever assigns the work. |
| Track records and promotion | A result is a claim in the same frame, by a model, that `answers` a work order posted by someone outside the worker's group. It counts once, settled by the verdicts on it from groups other than the worker's: one vote per group, majority wins, ties count for nothing. Per tier and kind of work, these update a Beta prior; who is hired for what follows the record. |
| Integrity | No one posts their own work orders or judges their own model's work; only writers of kind `model` whose model id starts with a tier's prefix (`claude-haiku-`, …) count; the record is only what the reader can see. Gnomon refuses a party's verdict on its own party's claims, so models that review each other must be registered as parties of their own. |
| Shift changes | Gnomon's handoffs (its spec, section 13). |

**Organisations in the record.** Three of Gnomon's events make an organisation's
structure part of the verified log, with authority checked by the gate:

- `position` {compartment, org, title, reports_to?, duties}: defines a
  title and whom it reports to (none: the owners). One organisation lives
  in one compartment; no position reports, through others, to itself.
- `appoint` {compartment, org, title, holder}: puts a writer of that
  compartment in a position. Many may hold one title; no one holds it twice
  at once.
- `dismiss` {appointment, reason}: ends an appointment.

Owners and governors may do all three. Anyone else acts only on positions
below one they currently hold (directly or through others): a Lead hires
Engineers, an Engineer hires no one, and a dismissed Lead has no authority
left. No one appoints themselves; anyone may resign. Queries see
`position(O, T, ReportsTo)`, `holds(W, O, T)`, `appointed(A, W, O, T)` and
`dismissed(A, E)`, and the views `above(O, T, U)` and `oversees(B, W)`;
the independent checker establishes `position` and `holds` by folding the
log itself, so a holding that has since ended no longer checks.

**A company** (`polymechania.org`) runs on these. It is founded with
positions that keep the powers apart: the CEO plans and delivers; the
Chief of Staff allocates work and budget; the Head of People hires and
reviews; the Head of IT keeps the tools. The Head of Assurance reports to
no one but the owners, so the gate lets no one in production appoint or
dismiss it. Staff are instances of a template writer per model tier,
hired into titles by someone above: titles, not models, are held, and the
record decides who keeps them. The company's compartment is its internal
record and memory (work orders, results, memos, decisions, the structure
chosen for each order); a client is a writer outside the company posting a
work order there; a subcontractor is a writer of another party, whose
verdicts count as independent. Personnel reviews propose probation,
dismissal or promotion by stated thresholds over results judged from
outside the worker's group; escalating or saying a part could not be done
is never counted against anyone, and a leaver writes a handoff before the
appointment ends.

**The decision.** For one unit of work, every option is priced: each tier
alone, and each rising cascade under each kind of check the work allows.
Its cost is expected spend on tokens, plus the expected loss
(`stakes_usd` for a wrong result kept unnoticed; `detected_usd`, by default
the same, for a part known not to be done because its last attempt was
flagged), plus `step_usd` for each expected sequential round. The cheapest
total wins; ties go to the option more likely right. A tier whose context
window cannot hold a part is never given it. Parts run in parallel; the
planner (writing work orders in requests of at most 32,000 tokens), the
integrator (reading the top floor) and the floors of managers (each reading
its own reports) are added on top. Inputs are validated: finite, in range,
a known check.

**The baseline** is one top-tier agent doing every part in turn with the
best checks it can use, re-reading its work so far as prompt-cache hits
(compacted to its desk once it outgrows it) and writing each part's prompt
to the cache. Plan and baseline report tokens, loss and rounds separately.

**Stated assumptions**, each to be replaced by the record:

- priors per tier (`PRIORS`, as pseudo-counts);
- reviewers' catch and false-alarm rates (`REVIEW`);
- attempts independent of each other (a part one tier got wrong is taken
  to be no harder for the next, which flatters cascades);
- summaries handed up a floor of 600 tokens.

**The pilot** (`bench/pilot`): 24 exactly specified Python tasks, 12
routine and 12 hard, each given to a Haiku 5.5 and a Sonnet 5.5
sub-agent and graded by hidden tests. All 48 passed. Recorded as work
orders, results and test verdicts, they are the record the planner plans
from. No task needed escalation, so the cascade itself is not yet
measured.

The comparison with the baseline is only as good as these assumptions:
with independent attempts, a cascade with an exact check is close to
certain to win on loss. Real measurements decide.

**Organisations** (positions, appointments, dismissals) belong to their
compartment: the same name in two compartments is two organisations, and
neither can learn of the other. Owners and governors act in an
organisation only if their party founded it; anyone else acts through the
positions they hold. Titles have no leading, trailing, doubled or unusual
spaces.

**Not yet:** running the agents (the host does that: Claude Code's
subagents or the API), learning how failures correlate across tiers,
pricing the risk of a bad plan or integration, latency beyond a price per
round, and measurements of plans against single agents on real work.

## 3. Forms: an alphabet, not one chart

The planner prices which models fill a structure; `polymechania.forms`
(`mekh form`) chooses the structure. A form is a word over nineteen letters, each with a size:

| | Letter | What it does |
|---|---|---|
| S | Solo | one agent, the whole context |
| D | Divide | parts with isolated contexts and short, complete briefs |
| C | Coordinate | a planner assigns parts up front |
| Q | Queue | fixed order; each agent reads earlier finished work, picks its own role or abstains |
| P | Propose | independent attempts, ideally across model families; no one reads another's |
| V | Verify-select | an exact check picks |
| A | Aggregate | one writer merges independent drafts |
| R | Route | send to the clear expert and defer |
| K | Critique-repair | a reviewer names a concrete fault; the author repairs |
| B | Debate | full answers exchanged over rounds |
| M | Market | members bid with their own estimates; abstaining is free |
| G | Ground | coordination through the record: scores, failure causes, never full solutions |
| E | Evolve | a scored population over generations |
| H | Hierarchy | floors of managers for more parts than one planner can brief |
| X | Escalate | cheapest capable tier first, up on a failed check |
| T | Toolmaker | a capable model builds a cheap artifact (program, small model) once for a workload |
| F | Floor | cheap workers answer what they are sure of; the rest go to one capable tier |
| N | Batch | many items, and several questions per item, in one request |
| I | Independent assurance | judges outside the workers' group, majority of distinct groups |

Each letter records when it helps, when it hurts, and its evidence with a
strength: *measured* (controlled experiments with language-model teams),
*theory* (Amdahl, Ashby, Galbraith, Mintzberg, Condorcet, Conway, Goodhart,
Hayek, stigmergy) or *hypothesis*. `compose(profile, dials)` spells a word
by rules that each cite their evidence:

- **Split only what a short brief can carry.** Low coupling: divide, with
  as many workers as reach the knee of Amdahl's curve (60% of the best
  speed-up at speed 0, 95% at speed 1). High coupling with a strong model:
  one context (splitting cost the strongest model 0.23 on hard
  constraints; Yu et al. 2026, 2607.16133).
- **Assign; do not let workers claim.** Pre-assigned teams ran 1.36x
  faster at the median against 0.88x for self-claiming ones (Mieczkowski
  et al. 2026, 2603.12229).
- **With an exact check, propose independently and select.** Reading each
  other's full solutions erased model diversity within one round; debate
  and critique lost with mixed families, selection kept a +0.19 diversity
  gain (Ann et al. 2026, 2608.23541). Critique is added only when a failed
  check names the fault.
- **Defer to a known expert.** Deliberating teams fell 6-41% short of their
  best member even when told who it was (Pappu et al. 2026, 2602.01011).
- **Open-ended work: strong models take turns, weak ones get structure.**
  Fixed order with self-chosen roles beat a coordinator by 14% on three
  models; below a capability threshold the effect reverses (Dochkina 2026,
  2603.28990). Never more than four voices: returns peak at 2-5 agents
  (Li et al. 2026, 2606.00655).
- **A workload gets a toolmaker, a floor and batches.** With thousands
  of items under one instruction, the cheap worker is built once and
  checked on a probe the model labels; it answers what it is confident
  about and the rest go to one capable tier, 25-100 items per request.
  Never more than two tiers (a third added nothing in 118 of 135
  comparisons; arXiv 2605.06350). Measured in `bench/floor`: on spam a
  linear model matched Claude Haiku for almost nothing; on five-star
  reviews no cheap worker came close, and the floor saved only what it
  gave up.
- **Count, do not self-judge.** At equal tokens, repeated sampling with a
  vote beat every method where a model assessed its own work (arXiv
  2607.28576); selection by a computer check or an outside comparator
  recovers most of what sampling exposes (2605.14163).
- **Floors only past one planner's reach**, escalation when a check can
  see failure, and assurance from outside the workers' group always.

The dials, each 0 to 1: effort (attempts, members), breadth (model
families), scrutiny (reviewers: 1, or 3 with majority), speed (workers),
thrift (escalation, and the weight of cost in the reward). Every design
lists what it rejected and why, and warns where the evidence runs out.

**Learning which form pays.** The rules are priors: winners change with
model bindings (Chen et al. 2026, 2607.25446), and the useful space is a
short list of about six topologies whose winner varies per task (Yu et
al. 2026, 2609.02264). `candidates` gives that short list (the composed
form at lower and higher effort, and one agent alone), and `Learner`
(LinUCB over ten interpretable task features) chooses among them,
starting on the composed form and moving off it as the record shows
another paying better, with reward = quality - thrift x cost / budget.
`mekh form` returns a design.

## 4. The plain vocabulary

`polymechania/concepts.py` is the contract between the core and every
world. It has three tables:

- **Concepts**: everything that can be named (the organisation, the record,
  tiers, kinds of worker, roles, kinds of check, ranks of stakes), each with
  a plain name and a meaning that never change.
- **Rules**: what the core enforces (section 1). A world may give each a
  line of its own; rules are never read from a world, so none can be added,
  dropped or softened.
- **Events**: everything a view can show (a task arriving, a post on the
  team, how each part is done, the expected cost, the lone-agent baseline,
  a note, a rule), each with a plain template and its required facts.

The core speaks only through events (`polymechania/events.py`). An event
carries **names**, as concept keys, which a world may rename, and
**values**, already written out (costs, chances, counts), which no world
may reword. A chance short of certain is printed with enough digits never
to read as 100%.

## 5. Worlds

A world is one TOML file with up to six sections: `[world]` (id, name,
title, region, tagline), `[names]` (concept → its name here), `[say]`
(event → its template here), `[precepts]` (rule → its line here),
`[style]` (accent, ok, fail and dim colours, a glyph, spinner phrases) and
`[lore]` (a story). Anything left out is said plainly.

A world is refused, with every reason listed, if it:

- has a section, field, concept, event, rule or fact the contract lacks;
- retells an event without stating every required fact;
- has a malformed id, colour, glyph, spinner or template.

Worlds are found in `MEKH_WORLDS` (a path list), then
`~/.config/polymechania/worlds/`, then the built-in folder; a person's own
world of the same id wins. `mekh world new` writes a file with every
concept, event and rule commented out in its plain form; `mekh world
check` explains what a file gets wrong; `mekh world use` sets the default.

Three worlds ship: **Plain**, **Kagamigakure** (the Village Hidden in the
Mirror: a ninja village whose myths come from Shinto and Buddhism) and
**Hollow Acre** (a farm). They show the range, and that it is one
organisation underneath: the tests render every event of real plans in
every world and check that every value appears unchanged.

## 6. Views and the map

Every view reads the same events. Three are planned:

- **The terminal** (`mekh`, now): lines in the world's voice and colours.
  `--both` prints each line twice, in the world's words and plainly;
  `--plain` drops the world; `--json` gives the events themselves.
- **The dashboard** (next): a full-screen terminal view of a running
  organisation (who holds which post, parts in flight, checks passed and
  failed, spend against the lone-agent baseline), styled by the world.
- **The map** (after): a graphical world. Polymechania is the world; each
  organisation is a **region** in it, drawn in its own world's style, so a
  person's agent farm, office tower and ninja village sit on one map.
  Posts are buildings, workers are figures, tasks travel as they are
  passed on. Work crossing a border is shown in the receiving region's
  style, because what crosses is the plain event.

What a world may add to the map is the same as what it may add to the
terminal: names, voice, look and story, never facts or rules.

## 7. Next: the runtime

v0.1 plans and designs; the host (Claude Code's subagents, the API) runs
the work. Next, Polymechania runs it itself:

- **A register of workers**, models and tools alike, each with what it can
  do, its price, how to call it and its record: calculators and calendars
  (from Gnomon's checkers), test runners, SAT and SMT solvers, proof
  assistants, scripts the toolmaker wrote, and models by tier.
- **Dispatch by the planner**: each part to the cheapest capable worker,
  the check run by something outside it, escalation on failure, every
  order, result and verdict written to Gnomon.
- **Measurements against one agent alone** on longer, vaguer, multi-step
  work, where the pilot could not yet show when escalation pays.

## 8. Not yet in v0.1

Running workers (section 7), the dashboard and the map (section 6),
learning how failures correlate across tiers, pricing the risk of a bad
plan or integration, and sharing worlds between people.
