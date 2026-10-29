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

Folded in on the cleanup pass (2026-10-29), verbatim from the review file named under each heading (git history, commit `fa517d6`); only the heading level of the review's own headings is lowered to nest here.

### Independent review of the architecture hypothesis, 1 (by a separate agent that wrote none of architecture.md, 2026-10-28)

Handling not itemised. The status line says revision 2 "takes its corrections".

Line numbers refer to `docs/architecture.md` unless another file is named. Probe scripts were run on throwaway logs in a scratch folder, against a copy of the Gnomon core built outside the clone. Neither repo was modified.

#### Wrong or unsupported claims

1. **"Nothing we can offer on a subscription can keep an agent alive" (l.64-67) is overstated.** `docs/engines.md:28-31` lists Claude Code cloud sessions that "keep running with the laptop closed", and desktop `/loop` with intervals down to a minute. Both are on Pro. The constraint that is real is narrower: the *unattended scheduled* path is hourly and starts fresh each time.
2. **The Anthropic harness is misread (l.50-56).** "A new session declaring the job done" is a failure of *fresh* sessions: a later agent saw the progress and stopped. It is not a long-session failure. The article also says compaction "isn't sufficient", not that it fails. Its sessions are long, too: each builds one feature and tests it end to end, which is nothing like an 80k-token micro-run.
3. **Gas Town (l.57-58) supports less than claimed.** Its intro does call polecats "ephemeral worker agents", but it also keeps "git worktree-based storage that persists agent state" (hooks). That is stricter state-keeping than "nothing survives a run except what it wrote" might suggest, but it is also per-agent state, which this design rules out.
4. **The push_scale citation (l.93-100) overstates the cold-start risk.**
   - The "1 in 12" figure was Gemma. `gnomon/bench/push_scale.md:3-5` and `live.md:256-262` say Claude does pull, with good targeted queries.
   - The "0 to 3.5%" figure is an exploratory ConvoMem diagnosis, "not a result" (push_scale.md:10-14), and it measures a push chosen *without* the question.
   - A run always has a question: its work order. The question-dependent push in the same file holds the evidence for 54-96% of questions at 2,000 tokens (push_scale.md:46-53).
5. **The pilot numbers are correct but under-specified (l.77-83).** Recomputed from `bench/pilot/results.json`: n=48, min 79,827, max 96,743, median 81,399, mean 82,563, all PASS. Solutions run 7-240 lines (median 41.5). The prices check out against `plan.py:103-110`: 80k tokens cost $0.008 on Haiku and $0.16 on Sonnet, and cache reads are 1/10 (Haiku) and 1/20 (Sonnet). Two caveats:
   - The `tokens` field is one total. It does not separate input, output and cache reads, so the "uncached" price may not be the price that was actually paid.
   - My regression of tokens on solution size gives an intercept of 79,431 (97.6% of the median), which supports "almost all start-up". It is an inference, not a measurement.
6. **The cache lifetime question at l.87-88 can be answered now.** The default lifetime is 5 minutes. An extended 1-hour lifetime costs 2x on write, and a hit refreshes it ([prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). A wake-up exactly every hour therefore misses even the 1-hour cache, so uncached is the realistic case at hourly cadence.
7. **"The connector is how the Free version works at all" (l.138-139) skips a missing piece.** Claude app connectors are remote MCP servers. Gnomon's server is stdio only, and "HTTP transport" and "a hosted remote MCP endpoint with sign-in" are listed as not yet built (`gnomon/spec/claim-protocol-v0.1.md:1272-1276`).
8. **"A misbehaving engine cannot write beyond its grant" (l.141-143) is true only on the MCP path.** `Memory.append(writer, ...)` takes the writer id as a plain argument (`gnomon/python/gnomon/__init__.py:118`). Any engine that can reach the file (our own API process, or Claude Code with Bash) can write as anyone. Issue #50 is noted at l.153, but the "why" paragraph still states the stronger claim.
9. **The island row (l.205) conflicts with `bench/map/RESULTS.md:21-26`.** Even with revocation, "the owner is a bridge to everything", so there are no true islands.
10. **Issues #48-#51 could not be checked.** GitHub access was refused in this session. The issue numbers match `HANDOFF.md:87-88`.

#### What probing showed

All of the following was run against the real core (`p1`-`p6` scripts):

- **The compartment gate works.** A run instance writing outside its compartment was refused (`E_COMPARTMENT`), and spawning an instance into a compartment its parent lacks was refused (`E_SPAWN`).
- **There is no revocation.** An event kind `revoke` gives `E_KIND`. Re-registering the same writer with narrower rights gives `E_DUPLICATE`, and an empty compartment list gives `E_BODY`. `dismiss` ends the appointment, but the dismissed writer then wrote a claim and a handoff, and both were accepted. The org layer cannot stand in for revocation.
- **There is no deadline, and the clock can be poisoned.** The gate checks only that `record_time` does not go backwards. A run wrote one claim stamped 2099-01-01, and it was accepted. Every later write by anyone (the owner, and a fresh `--per-session` MCP server registering itself) then failed with `E_CLOCK: record_time is earlier than the previous event`. One bad or clock-skewed engine can lock the whole world. MCP tools do not expose `record_time`, but a direct-library engine or a machine whose clock runs fast does not need them.
- **One identity per run already exists for any engine that starts its own MCP process.** Two `--per-session` server starts became `eng-4` and `eng-5`. `org.hire` already uses `instance_for` (`polymechania/org.py:203`). The l.149-151 gap is about the Claude app's single connector connection, not about our API engine.
- **Concurrency is safe for appends but not for the work.** Four processes appended 25 claims each with no errors, and the chain verified. Two runs that both `follows` the same handoff were both accepted, so the chain forks silently, and `resume` showed only the newer branch. Two leases on one frame lose work with no error.
- **Scale is not a problem.** After 2,000 per-run writers and handoffs (1.5 MB of log), `resume` took 0.05 s and an append about 1 ms.
- **The MCP tool list matches the table at l.121-128.** It has `resume`, `handoff`, `query`, `remember` and `give_verdict`, and no `lease`, `release` or `deliver`. `org.deliver` is a Polymechania wrapper over `remember` (`org.py:238`) with no usage field.

#### Design weaknesses

**Major**
- **Leases are a distributed lock, so they need fencing.** Leases without fencing tokens fail under process pauses and clock skew ([Kleppmann 2016](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)). The gate would have to reject a write whose lease epoch is stale. Claims in a `run/...` frame (l.155-157) cannot do this, so the "undecided" question is in fact decided: it must be new event kinds. The probes also show that time cannot come from writers.
- **The scheduler is the most privileged component and a single point of failure.** It must hold `spawn` and the power to grant. "No judgement, so it can be tested exhaustively" (l.178-179) mistakes having no judgement for having no hard cases: time, crashes, retries and duplicate delivery are where lease systems break. When the scheduler is down the world stops. When it is compromised, everything is.
- **Partial results and idempotency are not handled.** A run killed by a hard budget cannot write its own handoff, so the scheduler must write an "abandoned" record. A run that delivered but died before its handoff will be leased again and deliver twice. Work done outside the record (commits, calls through doors) is not rolled back. Work orders need idempotency keys.
- **The Free version contradicts the principle.** The person's chat *is* one long-lived context. A run inside it pays no fresh start-up and gets no fresh writer unless the connector can switch writers in the middle of a connection, which nothing does today. With remote MCP not built (claim 7), the Free version currently has no engine at all.
- **Cost of the Paid version.** Start-up alone, hourly, at the pilot's 80k tokens and uncached: $3.84 a day, about $115 a month per Sonnet resident; about $5.76 a month on Haiku. On Pro the same runs draw about 1.9M tokens a day from the usage window. The doc never states a cost per resident-month.

**Moderate**
- **This contradicts vision scene 4 (`docs/vision.md:180-186`).** There, residents "answer for themselves" and "pause properly". Here a scheduler answers and the run ends. That may be the better design, but it is a change to the vision and has to be recorded there.
- **"End at the next safe point" (l.75) is undefined.** Nothing forces a model to reach one. The only enforcement is a hard kill, and that loses the handoff.
- **Splitting alone does not reduce errors.** Under a constant-hazard model, success depends on total task length, not on how the task is cut up ([Ord 2025](https://arxiv.org/pdf/2505.05115)). Short runs pay only if a check *between* runs catches errors. The doc should make independent checks at run boundaries part of the claim.
- **Security.** A resume packet carries text from other writers into a fresh context, a cross-run injection path. A `lease` tool callable by the model would let a run lease itself more. Leases must be issued out of band.

**Minor**
- Latency: the pilot's median wall time was 15 s (max 75 s) for trivial tasks. The Free experience of "leased runs while you talk" has no latency target.
- More than one Free user's world on one connector: engines.md:10 says Free gets "yes, one" custom connector.

#### Missing alternatives

- **A long-lived process per resident with durable checkpoints** (durable execution of the Temporal/LangGraph kind). It is possible on the Paid engine, which we control. Handoffs at checkpoints give the same auditability, and the prompt cache stays warm (Sonnet 5.5 cache reads cost 0.05x).
- **One long session per frame with compaction, recording at each compaction.** Gnomon's PreCompact hook already records at that point. `plan.py:40-42,401-420` already prices exactly this as *the baseline*, so the architecture rejects the very thing its own planner compares against, without measuring it.
- **A hybrid:** runs sized to a frame (hours), not to a token budget, with fresh starts only at frame boundaries or on failure.

#### Tests

- **T1 is the right test, but underpowered and missing an arm.** Add arm (c): one session with compaction, the planner's baseline. Compare dollars at actual cache use, not tokens. Fix the number of tasks and runs ahead of time. The 1.5x threshold needs a stated reason.
- **T2 is cheap but not yet possible.** `results.json` has only totals. Capture input, output, cache-read and cache-write tokens per run.
- **T3 is not cheap as stated.** InterruptBench needs WebArena. Inject mid-task changes into the pilot's multi-step tasks instead. Note that InterruptBench found interruptions applied in place rarely turned a success into a failure (1-5 episodes per model), which weakens the premise.
- **T4 is good, but blocked for the Claude app** until remote MCP exists. Run it with Claude Code over stdio first.
- **T5 fails today by construction** (the probes above). Extend it to direct appends to the file, calls through the library, and a future-dated `record_time`.
- **Add:**
  - **T6, double lease:** two runs on one frame. The second must be refused.
  - **T7, scheduler crash:** kill the scheduler in the middle of a lease and restart it. Expect no orphaned run and no double delivery.
  - **T8, resume adequacy:** does a work-order-driven push hold what resumed work needs?
  - **T9, Free latency and usage per run** on Pro.
  - **T10, cost per resident-month** from logged usage.
  - **T11, runaway:** a run that ignores its budget is stopped by an engine-side hard cap (API `max_tokens`, Managed Agents per-run budget).

#### Outside evidence

- [Chroma, context rot](https://www.trychroma.com/research/context-rot): 18 models; reliability falls with input length even on simple tasks; one distractor hurts and four hurt more; focused prompts of about 300 tokens beat full ones of about 113k. This argues for small contexts, but it does not choose between short runs and compaction.
- [Anthropic, long-running harnesses](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents): one feature per session, a JSON feature list, a progress file, git; "compaction isn't sufficient". No metrics reported.
- [Gas Town intro](https://gastown.dev/docs/intro): ephemeral polecats, a Beads ledger, and state kept in git worktrees.
- [Ord 2025, half-life of agent success](https://arxiv.org/pdf/2505.05115): constant hazard; dividing a task does not change total success without recovery between pieces.
- [InterruptBench, arXiv 2604.00892](https://arxiv.org/html/2604.00892v1): 165 WebArena-Lite tasks; Opus adapts to about 50% within 10 actions; harm from interruption is rare. No handoff strategy was tested.
- [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): lifetimes of 5 minutes and 1 hour (2x write), refreshed on a hit, isolated per workspace.
- [Kleppmann 2016](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html): leases need fencing tokens.
- Weak and unverified: [a measured 436k-token fixed overhead per Claude Code sub-agent](https://hashnode.com/posts/what-a-claude-code-subagent-actually-costs-measuring-the-436k-token-fixed-overhead/6a79f5b2da080ae395c58f90). The cached share was not separated out, so it is indicative only.
