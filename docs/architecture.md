# Architecture: a hypothesis

Status: **hypothesis**, written 2026-10-28 for an independent attack
(`docs/architecture-review-1.md`). Nothing here is built beyond what
already exists in this repo and in Gnomon. Every claim says what supports
it and how to test it cheaply; a claim that fails its test changes here.

## In three lines

1. **No long-lived agents.** Work happens in short, bounded runs. A run
   starts from the record, does one piece of work, writes its result and a
   handoff, and ends. Nothing survives a run except what it wrote.
2. **One plain protocol.** Every engine (a person's own Claude through the
   connector, Claude Code on a schedule, our API engine, a local model)
   speaks the same small set of calls to the same record. No engine holds
   state of its own.
3. **Everything else is a worker or a view.** A worker takes a work order
   and returns a result (models, tools, scripts, checks). A view reads
   events and shows them (the terminal, the map, notifications, a guide's
   voice). Neither keeps a private copy of the truth.

The record is Gnomon: an append-only, hash-chained log with writers,
compartments, verdicts and handoffs (`gnomon/spec/claim-protocol-v0.1.md`).

## 1. No long-lived agents

**What it means.** A *resident* of a world (a guide, a Lead, an Engineer)
is not a running process. It is a title in an organisation (`position`,
`appoint` in spec section 2), a stat card, and a chain of handoffs. When
there is work for it, a **run** is started:

- **Identity:** a fresh Gnomon writer, an instance of the title holder's
  template (Gnomon 2a), so every run is attributable on its own.
- **Grant:** the compartments it may read and write, the tools (doors) it
  may call, and a budget: tokens, dollars and wall time, with a deadline.
- **Start:** a resume packet for its work order, fitted to a token budget
  (Gnomon 13): the latest handoff, what changed under it, open questions.
- **End:** a result (a claim answering the work order), a handoff, and its
  usage. Or, if the budget runs out, a handoff saying where it stopped,
  which never counts against it (spec section 1).

The resident "continues" only in the sense a shift worker does: the next
run reads the last handoff.

**Why (outside evidence).**
- Long single sessions degrade. Chroma's context-rot study tested 18
  models and found accuracy falls as input grows, even on simple tasks, and
  each added distractor lowers it further
  ([Chroma 2025](https://www.trychroma.com/research/context-rot)).
- Anthropic's own harness for long-running coding agents is this shape:
  an initializer, then many sessions that each make one incremental change
  and leave a clean state, with a JSON feature list, a progress file and
  git as the memory. Failures they report were the long-session ones:
  running out of context mid-feature, compaction losing instructions, a
  new session declaring the job done
  ([Anthropic 2025](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- Gas Town keeps work state in a git-backed ledger and treats its worker
  agents as ephemeral ([gastown.dev](https://gastown.dev/docs/intro)).
- Older engineering says the same: state in a log, processes disposable
  (event sourcing; Erlang's supervision and "let it crash"; twelve-factor
  stateless processes).

**Why (this project).**
- The engines force it anyway. Pro's unattended option is a scheduled
  task, hourly at most, each a fresh session (`docs/engines.md`); the
  Free version moves only while the person is talking. Nothing we can
  offer on a subscription can keep an agent alive.
- Spec section 1's integrity rules (no one grades their own work,
  independent verdicts) are checked on the record. A long-lived agent's
  private context is a place where that cannot be checked.
- Vision review point 11 (a "busy" reply written by the working agent
  breaks its context) dissolves: a run is never interrupted to chat. The
  "busy" reply comes from the scheduler reading the record ("Engineer is
  on part 3 of 5, due by 14:10"), and "urgent" means: end the run at its
  next safe point with a handoff (Gnomon 13), talk, then start a new run.

**What it costs (measured here).** Starting a run is not free. In the
pilot (`bench/pilot/results.json`, 48 runs as Claude Code sub-agents),
every run used 79,827 to 96,743 tokens, median about 81,000, even for
tasks a few dozen lines long. Almost all of it is the harness's fixed
start-up, not the task. At this repo's prices (`plan.py`), 80,000 input
tokens cost about $0.008 on Haiku and $0.16 on Sonnet uncached, and a
tenth or less of that when read from the prompt cache. So:

- Short runs pay only if the fixed prefix is **small** (a bare API call
  through a door, not a full agent harness) or **cached**. A prompt cache
  that expires between hourly wake-ups saves nothing (cache lifetime to be
  checked against current docs).
- Too short a run spends more on starting than working. There is a knee:
  runs should be sized so start-up is a small share. Hypothesis: start-up
  under 20% of a run's tokens.

**What it risks (measured in Gnomon).** A run knows only what reaches its
context. Gnomon's live tests found that what is pushed into context gets
used and what is merely offered mostly does not (one model called its
memory tools once in 12 chances), and that a 1,500-token push chosen
without the question held the needed evidence for 0 to 3.5% of questions
on large histories (`gnomon/bench/push_scale.md`). A run that starts cold
from a large record may simply not know what it needs. The resume packet
is scoped to one frame (one piece of work), which is the hope; it is not
yet measured on resumed work.

**Tests.**
- **T1, continuity:** the same multi-step bench task done (a) in one
  session, (b) as runs of at most N tokens joined by Gnomon handoffs.
  Measure pass rate, total tokens, and how often a run redoes or undoes
  earlier work. The hypothesis survives if (b) is no worse on pass rate at
  under 1.5x the tokens. The pilot's tasks are too small; it needs the
  longer, vaguer work spec section 7 already calls for.
- **T2, start-up share:** log fixed versus task tokens per run on each
  engine (API door, Claude Code sub-agent, scheduled task). Cheap: the
  usage is already reported.
- **T3, interruption:** InterruptBench-style changes mid-task (arXiv
  2604.00892), with and without end-at-safe-point plus handoff.

## 2. One plain protocol

**What it means.** An engine needs only a few calls, which Gnomon mostly
has already over MCP (Gnomon 10):

| Call | Exists? | What it does |
|---|---|---|
| `resume` | yes (Gnomon 13) | the run's starting packet, to a token budget |
| `query`, `remember`, `give_verdict` | yes | read and write the record through the gate |
| `handoff` | yes | where the work stands |
| `lease` | **no** | the scheduler gives a run its writer, grant, budget and deadline |
| `deliver` | partly (`org.deliver`) | a result answering a work order, with usage |
| `release` | **no** | the run ends; its grant stops working |

The engine is plumbing. The Free version: the person's own Claude, in the
Claude app or Claude Code, connects to their world's MCP server and is
leased runs while they talk. The Paid version: our scheduler leases runs
to our API engine while they are away. Advanced: their own key or their
own machine. Same calls, same record, so a world can move between engines
without losing anything, and a view never needs to know which engine did
the work.

**Why.** MCP is the one interface every Claude surface already speaks; the
connector is how the Free version works at all. Gnomon's MCP server
already fixes identity outside the model ("one identity, fixed by whoever
configures it") and refuses writes the gate would refuse, so a misbehaving
engine cannot write beyond its grant. That is what lets us mix engines we
do not control.

**What is missing, and must exist before anything runs unattended.**
- **Grants that end.** A lease must expire and be revocable. Gnomon has
  no revocation (issue #49); writers are registered for compartments for
  good. Until it does, "a run's grant stops working" is not true.
- **One identity per run across engines.** Auto mode keys writers by the
  host's session id (Gnomon 10). Runs leased to our API engine need the
  same guarantee without Claude Code's hooks.
- **Compartments under auto mode** (issue #51), side channels (#48) and
  the plain-text log with unauthenticated appends (#50) all bear on
  whether the map's islands are real.
- **Where the lease lives.** Either new Gnomon event kinds, or claims in
  a `run/...` frame. Claims need no protocol change but cannot be
  enforced by the gate; event kinds can. Undecided.

**Tests.**
- **T4, two engines, one world:** the same work order done once by a
  Claude Code session through the connector and once by an API run
  through the door, against one log. Pass if both write valid, attributed
  results and a third engine can resume either's handoff.
- **T5, grant enforcement:** a run tries to write outside its grant, past
  its deadline, and after release. Every attempt must be refused by the
  gate, not by the engine's good behaviour.

## 3. Everything else is a worker or a view

**Workers** take a work order and return a result with usage: models by
tier, and tools (calculators, test runners, solvers, scripts the
toolmaker wrote). The planner (`plan.py`, `forms.py`) decides who; the
scheduler starts runs; checks are workers too, always from outside the
worker's group. This is spec section 7's register of workers.

**The scheduler** is a plain program, not a model: it reads open work
orders and budgets from the record, asks the planner, leases runs, and
notices runs that never delivered (deadline passed, no handoff). It has
no judgement to make, so it can be tested exhaustively.

**Views** read events (`events.py`) and show them: the terminal today, the
dashboard and map next, notifications, and the guides' voices. The worlds
contract already forbids a view from changing a fact, number or rule;
this extends it: a view also holds no state the record does not. The
map's roads are drawn from grants (bench/map); a pigeon flies only for a
message event; a resident is shown working only while a lease is live.

**The map is a view, not a control** (vision review point 5). Drawing a
road asks the owner to confirm a grant; the grant is written to the
record; the road appears because the grant exists.

**Notifications** are a view with one rule of their own: one stays until
the record shows it resolved.

## How the vision sits on this

| Vision | Underneath |
|---|---|
| A resident, a guide | a title, a card, a chain of handoffs; runs when there is work |
| "Busy, back when this part is done" | the scheduler reading the live lease |
| "Urgent" | end at the next safe point, handoff, chat, new run |
| A quiet world on your local time | no runs leased; the view animates from the clock |
| Paid keeps working while you are away | our scheduler leasing runs to our API engine |
| Free works while you talk | your Claude, through the connector, takes leases |
| An island | a compartment no live grant crosses (needs revocation to be true) |
| The power grid, brownouts | budgets and limits on leases (spec section 7) |

## What this rules out

- A chat history as the state of anything.
- Agents talking to each other outside the record. A message between
  residents is an episode or claim; that is what the pigeon draws.
- Any engine-specific memory (Claude's own memory, a model's long
  context) as the place a world's work lives.
- A view or theme that keeps its own copy of the truth.

## Where the hypothesis is weakest (for the attack)

- Start-up cost: if T2 finds start-up near the 80,000 tokens of the
  pilot on every engine, short runs may cost more than one long session.
- Cold starts: push_scale's numbers say a run may not learn what it needs.
- Revocation does not exist yet; without it, bounded runs are bounded
  only by convention.
- The Free version's engine is the person's live chat. It can be leased
  runs, but nothing forces it to end one cleanly or to write a handoff
  (auto mode helps only in Claude Code).
- Some work is genuinely one long context (spec section 3: splitting cost
  the strongest model 0.23 on hard, coupled constraints). A run budget
  must be able to be large when the form is Solo.
