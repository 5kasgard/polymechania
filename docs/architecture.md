# Architecture: a hypothesis

Status: **hypothesis, revision 2** (2026-10-28). Revision 1 was attacked by
a separate agent (`docs/architecture-review-1.md`); this revision takes its
corrections and adds three ideas from the owner (a standing self, a free
clock, a thin boot). Nothing here is built beyond what exists in this repo
and in Gnomon. Every claim says what supports it and how to test it; a
claim that fails its test changes here.

## In four lines

1. **Characters persist; processes do not.** A resident is a standing
   *self* in the record (who it is, what it has learned, its card, its
   train of thought). Work is done in runs, each starting from that self
   and the work's handoff and ending by writing back to both. How long a
   run lasts is a dial to be measured, not a principle.
2. **One plain protocol.** Every engine (the owner's own Claude, Claude
   Code, our API engine, a local model) speaks the same calls to the same
   record, and the record's gate, not the engine, enforces what a run may
   do.
3. **A free clock, a costed worker.** Waking up, checking what is due and
   deciding whether anything needs a model is done by plain code that
   costs no model usage. Tokens are spent only when there is work.
4. **Everything else is a worker or a view.** Workers take work orders
   and return results; views read events and show them. Neither keeps a
   private copy of the truth.

The record is Gnomon: an append-only, hash-chained log with writers,
compartments, verdicts and handoffs (`gnomon/spec/claim-protocol-v0.1.md`).

## 1. Characters persist; processes do not

### The self

A handoff says where a piece of work stands. It is not who did it. The
owner's idea: each resident has a **self** that every one of its runs
starts from, so the character reads as one person who carries on, grows
and gets better, like a train of thought, though each run is new.

A self would hold (each part a hypothesis):
- **Identity:** name, role, voice, values; fixed by the owner or the
  world's theme, never by the resident itself.
- **Lessons:** what it has learned, each a claim in its own frame, kept
  only while outside verdicts support it. So it learns what held up, not
  whatever it once believed. Superseded lessons are dropped, with history.
- **Its card:** its record of results and verdicts (`cards.py`).
- **Its journal:** a short running account in its own words, the thread
  between runs (`org.journal` exists already).

A run's start packet is then: the self (small, stable, cacheable) + the
work's handoff and what changed under it (Gnomon 13) + the work order.

**Evidence.** In long chats, models drift from their given instructions
and persona noticeably within eight rounds; attention to the system prompt
falls between turns ([Li et al. 2024](https://arxiv.org/html/2402.10962v4)).
A fresh run that re-reads a fixed self may stay *more* like itself than one
long session. Untested here.

**Risks.** Lessons written by a resident about itself are a self-grading
loop unless verdicts come from outside its group (spec section 1). A self
that grows without bound becomes the long context it was meant to avoid;
it needs a budget, like the resume packet. Text in a self or handoff from
other writers is an injection path into every later run.

### Runs, and how long they should be

A run gets: a fresh writer (an instance of the resident's template, which
`org.hire` already does with `instance_for`), a **lease** (below) with its
grant and budget, and a start packet. It ends with a result, a handoff and
its usage, or it is ended and the scheduler records it as abandoned.

Revision 1 said runs should be *short*. The review showed the evidence
does not support "short" by itself:
- Anthropic's long-running harness uses sessions of one whole feature
  each, tested end to end; its "a new session declared the job done"
  failure is a failure of *fresh* sessions, not long ones; and it says
  compaction is not sufficient, not that it fails
  ([Anthropic](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- Under a constant-hazard model, cutting a task into pieces does not
  change its chance of success unless something catches errors *between*
  the pieces ([Ord 2025](https://arxiv.org/pdf/2505.05115)).
- Context does hurt: 18 models lost reliability as input grew, even on
  simple tasks ([Chroma](https://www.trychroma.com/research/context-rot)).
  That argues for small contexts, but not for short runs over compaction.

So the claim is narrower: **a run boundary is worth its cost only where an
independent check sits on it.** Three candidate shapes, to be measured
against each other (T1):

| Shape | Run lasts | Fresh start when |
|---|---|---|
| (a) Bounded runs | a token budget | every budget |
| (b) Frame-sized runs | one piece of work (hours) | frame ends, a check fails, or a crash |
| (c) One session with compaction | as long as needed | never; recorded at each compaction (Gnomon's PreCompact hook) |

(c) is what `plan.py` already prices as the baseline, so it must be an arm
of the test, not rejected unmeasured. Durable execution of the Temporal or
LangGraph kind (a long-lived process with checkpoints) is a fourth option
on the Paid engine, which we control.

**"Busy" and "urgent"** (vision scene 4). The "busy" reply comes from the
scheduler reading the live lease, so a chat never enters a working run's
context (vision review point 11). "Urgent" asks the run to stop at its next
safe point; nothing yet forces a model to reach one, and a hard kill loses
its handoff, so the scheduler must write the abandoned record itself. This
changes scene 4 ("they answer for themselves") and is recorded there.

## 2. One plain protocol, enforced by the gate

| Call | Exists? | What it does |
|---|---|---|
| `resume`, `handoff`, `query`, `remember`, `give_verdict` | yes (Gnomon MCP, probed) | read and write the record through the gate |
| `lease` | **no** | issued **out of band** by the scheduler, never callable by a run: writer, grant, budget, deadline, epoch |
| `deliver` | partly (`org.deliver` wraps `remember`, no usage field) | a result answering a work order, with usage and an idempotency key |
| `release` | **no** | ends a lease; the gate refuses the run's writes after it |

**Leases must be event kinds the gate enforces**, not claims in a frame.
A lease is a distributed lock, and locks need fencing tokens: every write
carries the lease's epoch and the gate refuses a stale one
([Kleppmann 2016](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)).
Claims cannot do that.

**What the probes found in Gnomon** (review, scripts run on scratch logs):
- The compartment gate works: writes and spawns outside a writer's
  compartments are refused.
- **No revocation:** no `revoke` kind; re-registering is refused; a
  dismissed writer can still write claims and handoffs. Gnomon issue #49.
- **The clock can be poisoned:** a write stamped 2099 was accepted, after
  which every write by anyone failed `E_CLOCK`. One skewed or hostile
  engine can lock a whole world. Time must come from the gate, not
  writers. Gnomon #52.
- **Handoff chains fork silently:** two runs that both follow one handoff
  are both accepted, and `resume` shows only the newer branch (#53).
- **The gate is only on the MCP path:** `Memory.append(writer, ...)`
  takes the writer as an argument, so any engine that can reach the file
  can write as anyone (issue #50). A misbehaving engine is contained only
  if it reaches the record through MCP, never the file.
- Scale is fine: 2,000 run writers and handoffs, `resume` 0.05 s, append
  about 1 ms.

**The engines** (`docs/engines.md`):
- **Free:** the owner's own Claude through a connector. The Claude app's
  connectors are remote MCP servers, and Gnomon's is stdio only (remote
  MCP with sign-in is listed as not built), so **the Free version has no
  engine yet**. And the owner's chat is itself one long context: runs
  inside it get no fresh start and no fresh writer unless the connector
  can switch writers mid-connection. Free is honestly shape (c).
- **Pro:** Claude Code scheduled tasks (hourly, its own usage), cloud
  sessions that keep running with the laptop closed, and `/loop` on the
  owner's machine.
- **Paid and Advanced:** our API engine or the owner's key, where we
  control the boot and caching.

## 3. A free clock, a costed worker

The owner's idea: separate the **clock** from the **worker**. Checking
what is due costs nothing if it is plain code:
- A Cloudflare Worker cron on the free plan: 5 triggers, 10 ms of CPU
  each, 100,000 requests a day
  ([limits](https://developers.cloudflare.com/workers/platform/limits)).
  The door already runs on Cloudflare.
- GitHub Actions schedules, free on public repos.

The clock reads the record, asks the planner whether anything needs a
model, and only then leases a run. Hypothesis: most wake-ups need no
model at all, so most cost nothing (T10 measures it).

The limit: a free clock cannot spend Pro subscription usage on the owner's
behalf (only Claude's own scheduled tasks may, `docs/engines.md`). So on
Pro, the free clock can decide and the Claude scheduled task can do; on
the API, the free clock can do both.

**The scheduler is the most privileged part** (it holds `spawn` and grants)
and a single point of failure. Its hard cases are time, crashes, retries
and duplicate delivery, so it needs fencing, idempotency keys on work
orders, an abandoned record for runs that die, and the crash test T7.
When it is down, the world pauses with every handoff intact.

## 4. A thin boot

Every pilot run used 79,827 to 96,743 tokens (median 81,399, n=48), even
for tasks of a few dozen lines; a regression on solution size puts the
fixed part near 79,000. That is Claude Code's sub-agent start-up, not the
work. The owner's question: can boot be near zero?

- **Through the door (bare API call):** boot is the self + handoff +
  order. Hypothesis: 2,000 to 4,000 tokens, 20 to 40 times less.
- **Cached:** the self is stable, so it can be the cached prefix. Cache
  lifetimes are 5 minutes (default) or 1 hour at 2x the write price,
  timed from the last request and refreshed on a hit; reads cost 0.1x on
  Haiku and 0.05x on Sonnet and Opus 5.5
  ([prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).
  A wake-up exactly hourly just misses even the 1-hour cache; a cadence
  under an hour keeps it warm, but only worth it if there is work.
- **No model at all:** calculators, test runners, scripts and the clock
  itself boot for nothing.

**Cost per resident-month of start-up alone** (prices from `plan.py`,
hourly runs, 720 a month, uncached):

| Boot | Haiku | Sonnet |
|---|---|---|
| 80,000 tokens (pilot harness) | $5.76 | $115 |
| 3,000 tokens (thin, guess) | $0.22 | $4.32 |
| 3,000 tokens, cached at 0.1x / 0.05x | about $0.02 | about $0.22 |

On Pro, 80,000-token hourly runs would draw about 1.9M tokens a day of
the owner's usage. These are estimates until T2 and T10 log real usage.

## 5. Everything else is a worker or a view

**Workers** take a work order and return a result with usage: models by
tier, and tools. The planner decides who; checks are workers from outside
the worker's group, and per section 1 they belong on run boundaries.

**Views** read events (`events.py`). A view holds no state the record
does not. The map is a view, not a control: drawing a road asks the owner
to confirm a grant; the road appears because the grant exists. The owner
can cross anywhere, so no region is an island to the owner
(`bench/map/RESULTS.md`): "no one but you crosses". Notifications are a
view that stays until the record shows the thing resolved.

## How the vision sits on this

| Vision | Underneath |
|---|---|
| A resident, a guide | a self (identity, lessons, card, journal) and runs when there is work |
| It grows and learns | lessons as claims, kept while outside verdicts hold |
| "Busy, back when this part is done" | the scheduler reading the live lease |
| "Urgent" | stop at a safe point, handoff, chat, new run (changes scene 4) |
| A quiet world | the free clock finds nothing due; no model runs |
| Paid keeps working while you are away | free clock + our API engine |
| Free works while you talk | your Claude through a remote connector (not built yet) |
| No one but you crosses | a compartment no live lease crosses (needs revocation) |
| Brownouts | budgets and limits on leases (spec section 7) |

## What this rules out

- A chat history, or any engine's own memory, as the place a world's work
  lives.
- Residents talking outside the record (the pigeon draws a real message).
- A run that can lease itself, extend its own budget or set its own clock.
- A view or theme with its own copy of the truth.

## Tests

| | Test | Status |
|---|---|---|
| T1 | Shapes (a), (b), (c) on the same multi-step tasks, fixed in advance; dollars at actual cache use, pass rate, redone work. The pilot's tasks are too small. | needs longer tasks |
| T2 | Boot share per engine: input, output, cache-read, cache-write tokens per run (the pilot logged totals only). | cheap; needs logging |
| T3 | Interruption: inject mid-task changes into multi-step pilot tasks, with and without stop-at-safe-point and handoff. InterruptBench found harm from in-place interruption rare, which weakens the premise. | cheap |
| T4 | Two engines, one world: Claude Code over stdio and an API run through the door against one log; a third resumes either. | Claude app blocked on remote MCP |
| T5 | Grant enforcement: writes outside the grant, after release, past the deadline, future-dated, and straight to the file or library. | **fails today** (probes) |
| T6 | Double lease: a second run on one frame is refused. | fails today (forks) |
| T7 | Scheduler crash mid-lease: no orphan run, no double delivery. | needs leases |
| T8 | Resume adequacy: does a work-order-driven packet hold what resumed work needs? (push_scale: 54-96% of questions at 2,000 tokens with the question known) | cheap |
| T9 | Free latency and usage per run on Pro (pilot median 15 s even for trivial tasks). | cheap |
| T10 | Cost per resident-month from logged usage, and the share of free-clock wake-ups that needed a model. | needs a running world |
| T11 | Runaway: a run that ignores its budget is stopped by an engine-side cap (`max_tokens`, Managed Agents per-run budget). | cheap |
| T12 | The self: one character across many runs against one long session; how often each drifts from its identity and stated lessons. | cheap |

## Blocking before anything runs unattended

In Gnomon: revocation (#49), gate-assigned time (#52), lease and release
as event kinds with fencing epochs (#54), a single-successor rule for
handoff chains (#53), file-level write protection or all access via MCP
(#50), and remote MCP for the Free version.
