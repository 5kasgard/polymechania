# Architecture: a hypothesis

Status: **hypothesis, revision 2** (2026-10-28). Revision 1 was attacked by
a separate agent (Reviews, at the end of this file); this revision takes its
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

**Measured (T12b, `bench/archive/self/RESULTS_B.md`, 2026-10-29):** with Gemma 4
26B as the resident, fresh runs did *not* keep the self better than one
long session when the same instructions were in view (51% of rules kept
against 65%, a direction). What kept it (86%) was that conflicting
requests from a non-owner were not written into what the next run read.
So the lever is **what may be written into a resident's start packet**:
the owner may change the self; another writer's request applies to its
order unless the owner makes it standing. Gnomon's gate could enforce
that. Not yet tested with Claude residents (T12c).

### Who may write into a start packet (hypothesis, from T12b)

A run's start packet has three layers, and each has its own writers:

| Layer | What it holds | Who may write it | How long it lasts |
|---|---|---|---|
| **The self** | identity, values, rules, how to answer | the owner (or the world's theme, which the owner chose) | until the owner changes it |
| **Standing instructions** | requests that apply to every future order | the owner, or someone the owner has granted that power for this resident | until withdrawn |
| **The order** | this piece of work, with any requests attached | whoever may post work orders | this run only |

So a Lead's "from now on, use emojis" is part of *its order* and is not
copied forward into the next run's packet unless the owner (or a grant)
makes it standing. The handoff carries what was done and what is open,
never another writer's requests as if they were rules. In Gnomon this is a
gate rule: a claim in a resident's `standing` frame is accepted only from
the owner or a holder of a grant for it; the resume packet carries that
frame plus the handoff, nothing else as instruction.

**Why:** in T12b, fresh runs whose packet repeated the Lead's conflicting
requests kept 51% of the self's rules; fresh runs whose packet did not
kept 86%; one long session kept 65%. **Measured since:** T12c (Claude
Haiku resident) gave the same pattern (92%, 71%, 58%; +33 points); T12d
found that *labelling* a carried request ("the Lead's, does not change
your page") helped only by a direction (+9), while keeping it out of the
packet kept 89% against 68%, and an "owner's standing instruction" label
was followed more (+15) but still only about half the time. So the rule
belongs in the gate (Gnomon #55), and a real change to a resident belongs
in its self, not in a carried note.

**Evidence (before T12b).** In long chats, models drift from their given instructions
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

**Measured (T2, `bench/boot/RESULTS.md`, audited in `bench/boot/AUDIT.md`,
2026-10-28):** through the door, boot was **1,486 tokens** (1.9% of the
harness's ~79,000), and from the second call on, 1,480 of them were read
from cache, on both Haiku and Sonnet. One-shot runs with no tools passed
43/48 (Haiku) and 47/48 (Sonnet) of the pilot's tasks; all failures hit
the door's 4,096-token cap (five of Haiku's were empty, probably unasked-for
thinking). A cached Haiku-then-Sonnet cascade passed 24/24 at $0.0034 per
pass, a quarter of Sonnet alone (escalating on the hidden grader, so an
upper bound on what visible checks would catch). Against the pilot harness
with a warm cache the saving per call is small (about 12% on Haiku, even
on Sonnet, with the pilot's output bounded from its solution files); the
large saving (9 to 14 times) is for runs too far apart to keep the
harness's start-up cached, which is what scheduled runs are. Thin boot
holds; whether it holds on long work is T1.

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
(`bench/archive/map/RESULTS.md`): "no one but you crosses". Notifications are a
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
| T2 | Boot share per engine: input, output, cache-read, cache-write tokens per run (the pilot logged totals only). | **done** (door): boot 1,486, cache holds; `bench/boot` |
| T3 | Interruption: inject mid-task changes into multi-step pilot tasks, with and without stop-at-safe-point and handoff. InterruptBench found harm from in-place interruption rare, which weakens the premise. | cheap |
| T4 | Two engines, one world: Claude Code over stdio and an API run through the door against one log; a third resumes either. | Claude app blocked on remote MCP |
| T5 | Grant enforcement: writes outside the grant, after release, past the deadline, future-dated, and straight to the file or library. | **fails today** (probes) |
| T6 | Double lease: a second run on one frame is refused. | fails today (forks) |
| T7 | Scheduler crash mid-lease: no orphan run, no double delivery. | needs leases |
| T8 | Resume adequacy: does a work-order-driven packet hold what resumed work needs? (push_scale: 54-96% of questions at 2,000 tokens with the question known) | cheap |
| T9 | Free latency and usage per run on Pro (pilot median 15 s even for trivial tasks). | cheap |
| T10 | Cost per resident-month from logged usage, and the share of free-clock wake-ups that needed a model. | needs a running world |
| T11 | Runaway: a run that ignores its budget is stopped by an engine-side cap (`max_tokens`, Managed Agents per-run budget). | **done**: door refuses over-cap, stops at 4,096 |
| T12 | The self: one character across many runs against one long session; how often each drifts from its identity and stated lessons. | cheap |

## Blocking before anything runs unattended

In Gnomon: revocation (#49), gate-assigned time (#52), lease and release
as event kinds with fencing epochs (#54), a single-successor rule for
handoff chains (#53), file-level write protection or all access via MCP
(#50), and remote MCP for the Free version.

## Reviews

Folded in on the cleanup pass (2026-10-29), condensed to the points made; the full text of each review file is in git history at `fa517d6`.

One independent review of revision 1 by a separate agent that wrote none of this document (2026-10-28), with probe scripts run on throwaway logs against a copy of the Gnomon core; neither repo was modified. Revision 2 (this one) takes its corrections; handling is not itemised per point. Line numbers below refer to revision 1.

**Wrong or unsupported claims.**
1. "Nothing on a subscription can keep an agent alive" (l.64-67) is overstated: `docs/engines.md` lists Claude Code cloud sessions that keep running with the laptop closed, and desktop `/loop` down to a minute, both on Pro. What is real is narrower: the unattended scheduled path is hourly and starts fresh.
2. The Anthropic harness is misread (l.50-56): "a new session declaring the job done" is a failure of fresh sessions, not long ones; the article says compaction "isn't sufficient", not that it fails; its sessions each build one feature end to end, nothing like an 80k-token micro-run.
3. Gas Town (l.57-58) keeps "git worktree-based storage that persists agent state", which is per-agent state, the thing this design rules out.
4. The push_scale citation (l.93-100) overstates cold-start risk: "1 in 12" was Gemma (Claude pulls, with good targeted queries); "0 to 3.5%" is an exploratory diagnosis, "not a result", of a push chosen without the question; a run always has a work order, and the question-dependent push holds the evidence for 54-96% of questions at 2,000 tokens.
5. Pilot numbers are correct but under-specified (l.77-83): n=48, min 79,827, max 96,743, median 81,399, mean 82,563, all PASS; 80k tokens cost $0.008 on Haiku and $0.16 on Sonnet; cache reads are 1/10 (Haiku) and 1/20 (Sonnet). But `tokens` is one total, so the "uncached" price may not be the price paid; a regression gives an intercept of 79,431 (97.6% of the median), an inference not a measurement.
6. Cache lifetime (l.87-88): default 5 minutes; 1 hour costs 2x on write; a hit refreshes. An exactly-hourly wake-up misses even the 1-hour cache, so uncached is the realistic case at hourly cadence.
7. "The connector is how the Free version works at all" (l.138-139) skips that Claude app connectors are remote MCP servers; Gnomon's is stdio only and HTTP transport is not built.
8. "A misbehaving engine cannot write beyond its grant" (l.141-143) holds only on the MCP path: `Memory.append(writer, ...)` takes the writer id as a plain argument, so any engine that reaches the file can write as anyone (issue #50, noted at l.153, but the "why" paragraph still claimed the stronger thing).
9. The island row (l.205) conflicts with `bench/archive/map/RESULTS.md:21-26`: even with revocation "the owner is a bridge to everything", so no true islands.
10. Issues #48-#51 could not be checked (GitHub access refused in that session).

**What probing showed (real core).**
- The compartment gate works: a write outside the compartment gave `E_COMPARTMENT`; spawning into a compartment the parent lacks gave `E_SPAWN`.
- No revocation: event kind `revoke` gives `E_KIND`; re-registering narrower gives `E_DUPLICATE`; an empty compartment list gives `E_BODY`; a dismissed writer still wrote a claim and a handoff, both accepted.
- No deadline, and the clock can be poisoned: the gate only checks `record_time` does not go backwards; one claim stamped 2099-01-01 was accepted, and every later write by anyone then failed with `E_CLOCK`.
- One identity per run already exists for any engine that starts its own MCP process (two `--per-session` starts became `eng-4`, `eng-5`; `org.hire` already uses `instance_for`); the l.149-151 gap is about the Claude app's single connection.
- Concurrency is safe for appends (four processes, 25 claims each, chain verified) but not for the work: two runs that both `follows` the same handoff were both accepted (silent fork; `resume` showed only the newer branch); two leases on one frame lose work with no error.
- Scale is not a problem: after 2,000 per-run writers and handoffs (1.5 MB), `resume` took 0.05 s and an append about 1 ms.
- The MCP tool list matches the table at l.121-128 (`resume`, `handoff`, `query`, `remember`, `give_verdict`; no `lease`, `release`, `deliver`); `org.deliver` is a wrapper over `remember` with no usage field.

**Design weaknesses.**
- Major: leases are a distributed lock and need fencing tokens ([Kleppmann 2016](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)); a `run/...` frame claim cannot do this, so the "undecided" question is decided: new event kinds; time cannot come from writers.
- Major: the scheduler is the most privileged component and a single point of failure; "no judgement, so it can be tested exhaustively" ignores time, crashes, retries and duplicate delivery. If it is down the world stops; if compromised, everything is.
- Major: partial results and idempotency are not handled (a run killed by a hard budget cannot write its handoff, so the scheduler must write "abandoned"; a run that delivered but died before its handoff will deliver twice; work outside the record is not rolled back). Work orders need idempotency keys.
- Major: the Free version contradicts the principle (the chat is one long-lived context; nothing switches writers mid-connection; with remote MCP not built it has no engine at all).
- Major: cost of the Paid version: start-up alone, hourly, at 80k tokens uncached is $3.84 a day, about $115 a month per Sonnet resident, about $5.76 on Haiku; on Pro about 1.9M tokens a day from the usage window. The doc never stated a cost per resident-month.
- Moderate: contradicts vision scene 4 (residents "answer for themselves", "pause properly"); "end at the next safe point" is undefined and only a hard kill enforces it; splitting alone does not reduce errors under a constant-hazard model ([Ord 2025](https://arxiv.org/pdf/2505.05115)), so independent checks at run boundaries must be part of the claim; a resume packet carries other writers' text into a fresh context (cross-run injection), and a model-callable `lease` tool would let a run lease itself more (issue leases out of band).
- Minor: pilot median wall time 15 s (max 75 s), no Free latency target; engines.md says Free gets one custom connector.

**Missing alternatives.** A long-lived process per resident with durable checkpoints (Temporal/LangGraph-style durable execution; the cache stays warm); one long session per frame with compaction, recording at each compaction (Gnomon's PreCompact hook; `plan.py` already prices this as the baseline, which the architecture rejected without measuring); a hybrid with runs sized to a frame (hours), fresh starts only at frame boundaries or on failure.

**Tests.** T1: right test, underpowered, missing arm (c) one session with compaction; compare dollars at actual cache use; fix tasks and runs ahead; justify the 1.5x threshold. T2: needs input, output, cache-read and cache-write tokens per run. T3: InterruptBench needs WebArena; inject mid-task changes into the pilot's multi-step tasks instead (InterruptBench found interruptions rarely turned success into failure). T4: good, but blocked for the Claude app until remote MCP exists; run with Claude Code over stdio first. T5: fails today by construction; extend to direct file appends, library calls and a future-dated `record_time`. Add T6 double lease (second must be refused), T7 scheduler crash mid-lease (no orphan, no double delivery), T8 resume adequacy, T9 Free latency and usage per run on Pro, T10 cost per resident-month, T11 runaway stopped by an engine-side hard cap.

**Outside evidence.** [Chroma, context rot](https://www.trychroma.com/research/context-rot) (18 models; reliability falls with input length; focused ~300-token prompts beat full ~113k; argues for small contexts, does not choose between short runs and compaction). [Anthropic, long-running harnesses](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) (no metrics). [Gas Town intro](https://gastown.dev/docs/intro). Ord 2025 (constant hazard). [InterruptBench, arXiv 2604.00892](https://arxiv.org/html/2604.00892v1) (165 WebArena-Lite tasks; no handoff strategy tested). [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (5 min and 1 h, 2x write, refreshed on a hit, workspace-isolated). Kleppmann 2016. Weak and unverified: a measured 436k-token fixed overhead per Claude Code sub-agent (cached share not separated), indicative only.
