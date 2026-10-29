# Independent review of the architecture hypothesis, 1 (by a separate agent that wrote none of architecture.md, 2026-10-28)

Line numbers refer to `docs/architecture.md` unless another file is named. Probe scripts were run on throwaway logs in a scratch folder, against a copy of the Gnomon core built outside the clone. Neither repo was modified.

## Wrong or unsupported claims

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
9. **The island row (l.205) conflicts with `bench/archive/map/RESULTS.md:21-26`.** Even with revocation, "the owner is a bridge to everything", so there are no true islands.
10. **Issues #48-#51 could not be checked.** GitHub access was refused in this session. The issue numbers match `HANDOFF.md:87-88`.

## What probing showed

All of the following was run against the real core (`p1`-`p6` scripts):

- **The compartment gate works.** A run instance writing outside its compartment was refused (`E_COMPARTMENT`), and spawning an instance into a compartment its parent lacks was refused (`E_SPAWN`).
- **There is no revocation.** An event kind `revoke` gives `E_KIND`. Re-registering the same writer with narrower rights gives `E_DUPLICATE`, and an empty compartment list gives `E_BODY`. `dismiss` ends the appointment, but the dismissed writer then wrote a claim and a handoff, and both were accepted. The org layer cannot stand in for revocation.
- **There is no deadline, and the clock can be poisoned.** The gate checks only that `record_time` does not go backwards. A run wrote one claim stamped 2099-01-01, and it was accepted. Every later write by anyone (the owner, and a fresh `--per-session` MCP server registering itself) then failed with `E_CLOCK: record_time is earlier than the previous event`. One bad or clock-skewed engine can lock the whole world. MCP tools do not expose `record_time`, but a direct-library engine or a machine whose clock runs fast does not need them.
- **One identity per run already exists for any engine that starts its own MCP process.** Two `--per-session` server starts became `eng-4` and `eng-5`. `org.hire` already uses `instance_for` (`polymechania/org.py:203`). The l.149-151 gap is about the Claude app's single connector connection, not about our API engine.
- **Concurrency is safe for appends but not for the work.** Four processes appended 25 claims each with no errors, and the chain verified. Two runs that both `follows` the same handoff were both accepted, so the chain forks silently, and `resume` showed only the newer branch. Two leases on one frame lose work with no error.
- **Scale is not a problem.** After 2,000 per-run writers and handoffs (1.5 MB of log), `resume` took 0.05 s and an append about 1 ms.
- **The MCP tool list matches the table at l.121-128.** It has `resume`, `handoff`, `query`, `remember` and `give_verdict`, and no `lease`, `release` or `deliver`. `org.deliver` is a Polymechania wrapper over `remember` (`org.py:238`) with no usage field.

## Design weaknesses

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

## Missing alternatives

- **A long-lived process per resident with durable checkpoints** (durable execution of the Temporal/LangGraph kind). It is possible on the Paid engine, which we control. Handoffs at checkpoints give the same auditability, and the prompt cache stays warm (Sonnet 5.5 cache reads cost 0.05x).
- **One long session per frame with compaction, recording at each compaction.** Gnomon's PreCompact hook already records at that point. `plan.py:40-42,401-420` already prices exactly this as *the baseline*, so the architecture rejects the very thing its own planner compares against, without measuring it.
- **A hybrid:** runs sized to a frame (hours), not to a token budget, with fresh starts only at frame boundaries or on failure.

## Tests

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

## Outside evidence

- [Chroma, context rot](https://www.trychroma.com/research/context-rot): 18 models; reliability falls with input length even on simple tasks; one distractor hurts and four hurt more; focused prompts of about 300 tokens beat full ones of about 113k. This argues for small contexts, but it does not choose between short runs and compaction.
- [Anthropic, long-running harnesses](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents): one feature per session, a JSON feature list, a progress file, git; "compaction isn't sufficient". No metrics reported.
- [Gas Town intro](https://gastown.dev/docs/intro): ephemeral polecats, a Beads ledger, and state kept in git worktrees.
- [Ord 2025, half-life of agent success](https://arxiv.org/pdf/2505.05115): constant hazard; dividing a task does not change total success without recovery between pieces.
- [InterruptBench, arXiv 2604.00892](https://arxiv.org/html/2604.00892v1): 165 WebArena-Lite tasks; Opus adapts to about 50% within 10 actions; harm from interruption is rare. No handoff strategy was tested.
- [Prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): lifetimes of 5 minutes and 1 hour (2x write), refreshed on a hit, isolated per workspace.
- [Kleppmann 2016](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html): leases need fencing tokens.
- Weak and unverified: [a measured 436k-token fixed overhead per Claude Code sub-agent](https://hashnode.com/posts/what-a-claude-code-subagent-actually-costs-measuring-the-436k-token-fixed-overhead/6a79f5b2da080ae395c58f90). The cached share was not separated out, so it is indicative only.
