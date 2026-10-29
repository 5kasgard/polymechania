You are an independent auditor (a different AI family from the one that built this). Be blunt and specific; mark guesses as guesses.

The owner of two linked software projects feels "complexity debt" growing. He thinks the goals are fine but HOW they are being built is the problem. Most of the work was done by an AI coding agent (Claude) over two days, with the owner directing from a phone.

PROJECTS
- Polymechania: a "lab" of AI agents (residents) and tools, with experiments that test how to run them cheaply and reliably. No resident has yet done real work end to end.
- Gnomon: a verifiable memory for people and AI models (an append-only, hash-chained log with compartments and a gate that checks every write). Rust core plus Python.

EXACT COUNTS (made by a script today)
{
"date": "2026-10-29",
"polymechania": {
"tracked_files": 802,
"python_lines": 31293,
"rust_lines": 0,
"js_lines": 172,
"html_lines": 636,
"markdown_files": 69,
"markdown_words": 54901,
"test_files": 9,
"commits": 76,
"preregistrations": 23,
"docs": [
"architecture-review-1.md",
"architecture.md",
"engines.md",
"evidence-model.md",
"evidence.md",
"gnomon-50-options.md",
"licensing.md",
"queue.md",
"routing-review-haiku.md",
"routing-review-llama.md",
"routing.md",
"security.md",
"start-packet-gate.md",
"vision-review-1.md",
"vision.md"
],
"queue_items": 34,
"queue_by_status": {
"done": 10,
"in-progress": 1,
"open": 15,
"parked": 2,
"scheduled": 1,
"waiting-owner": 5
},
"bench_folders": [
"boot",
"border",
"cards",
"demo",
"eext",
"floor",
"long",
"map",
"map-mine",
"pilot",
"self",
"speed"
]
},
"gnomon_main": {
"tracked_files": 307,
"python_lines": 20734,
"rust_lines": 17496,
"js_lines": 0,
"html_lines": 0,
"markdown_files": 31,
"markdown_words": 48220,
"test_files": 24,
"commits": 171,
"event_kinds": [
"register",
"position",
"appoint",
"dismiss",
"episode",
"claim",
"verdict",
"supersede",
"resolve",
"appeal",
"schema_change",
"handoff"
],
"error_codes": [
"E_APPEAL",
"E_ATTRIBUTION",
"E_BODY",
"E_CAPABILITY",
"E_CLOCK",
"E_COMPARTMENT",
"E_CONSENT",
"E_DUPLICATE",
"E_ENVELOPE",
"E_EVENT_ID",
"E_EVIDENCE",
"E_FINAL",
"E_FORK",
"E_FUTURE",
"E_GENESIS",
"E_HASH",
"E_HIDDEN_CHARS",
"E_IDENTITY",
"E_KIND",
"E_NO_RESOLVER",
"E_OPEN_DISPUTE",
"E_ORG",
"E_PREV",
"E_QUOTE",
"E_REF",
"E_REFERENCE",
"E_RESOLVE",
"E_RESOLVE_PARTY",
"E_ROLE_CONFLICT",
"E_SAME_PARTY_VERIFY",
"E_SCHEMA_VERSION",
"E_SELF_DISPUTE",
"E_SELF_VERIFY",
"E_SEQ",
"E_SPAWN",
"E_STAKE",
"E_TIME_FORMAT",
"E_UNKNOWN_WRITER",
"E_WRITER",
"E_WRITER_SEQ"
],
"protocol_version": 3,
"spec_words": 12386,
"python_modules": [
"__init__.py",
"__main__.py",
"_jcs.py",
"_native.py",
"checkers.py",
"company.py",
"consolidate.py",
"firm.py",
"forms.py",
"hook.py",
"ingest.py",
"mcp.py",
"parity.py",
"proofs.py",
"rank.py",
"session.py",
"situation.py"
],
"open_prs": [
{
"number": 59,
"title": "Leases: time-bounded, fenced holds on a frame (#54)"
},
{
"number": 58,
"title": "Revocation: the owner can end a writer's access to compartments (#49)"
},
{
"number": 57,
"title": "Start-packet frames: only the owner writes a resident's self and standing instructions (#55)"
},
{
"number": 47,
"title": "Teams of models move to Polymechania"
}
]
}
}

OPEN GNOMON PULL REQUESTS
- PR #57: protocol v4. Only the owner writes an agent's self and standing instructions; only the agent writes its own work notes; packet() builds an agent's start packet from those. Based on a measured result (keeping another writer's request out of the packet kept 86-92% of an agent's rules, against 51-59% when carried).
- PR #58: protocol v5. The owner can revoke a writer's access to compartments.
- PR #59: protocol v6. Leases: time-bounded holds on a piece of work with a fencing token. No scheduler that would use them exists yet.
All three were opened on the same afternoon, stacked on each other.

THE WORK QUEUE (34 items)
- q01 [done] T12c: Llama judge and audit
- q02 [done] Evidence model: how external and internal evidence combine
- q03 [scheduled] E-ext: do public benchmarks predict our own results?
- q04 [done] Door: allow more free Workers AI models on /ai
- q05 [waiting-owner] Start-packet authority as a Gnomon gate rule
- q06 [open] Gnomon blockers before anything runs unattended
- q07 [waiting-owner] Gnomon PR #47 (teams of models move to Polymechania)
- q08 [done] Delete the merged branch door-effort
- q09 [done] Run bench/verify.py in CI
- q10 [open] Language as a routing row; Rust against Python test
- q11 [in-progress] First Test Kitchen demo: one small web demo per hypothesis
- q12 [open] Cascade with visible checks only
- q13 [open] E1: can stat cards be gamed?
- q14 [open] T1: run shapes on long multi-step work
- q15 [done] Longer multi-step tasks with hidden graders
- q16 [done] Cost and speed fields on stat cards
- q17 [open] The free clock (Cloudflare cron) and the scheduler
- q18 [open] Free version engine: remote MCP for Gnomon
- q19 [open] Batch API through the door (half price, non-urgent work)
- q20 [open] Vision cheap tests: card sort, menu picture, notification volume
- q21 [open] Waitlist test for Free and Paid
- q22 [waiting-owner] Legal check of the business model
- q23 [parked] Choose a licence
- q24 [done] Track Workers AI neurons per day
- q25 [done] Route judging to free models by default
- q26 [open] Rename 'world' files to 'themes' in the code
- q27 [waiting-owner] More skills from this work
- q28 [parked] T8, T9, T10 (resume adequacy, Free latency, cost per resident-month)
- q29 [open] Door credentials live only in one session's scratch folder
- q30 [open] The border: security as a world's edge
- q31 [done] Merge Gnomon PR #56 (#52 future writes, #53 forks)
- q32 [open] Record refused crossings in Gnomon (the watchtower)
- q33 [waiting-owner] Gnomon #50: sign appends (protocol 7)
- q34 [open] Gnomon: append re-reads the whole log

HANDOFF NOTE (start of it)
# Handoff: start here

Written 2026-10-28 at the end of the session that founded Polymechania, so
the next session starts from the record instead of from a long chat. Read
this, then `docs/vision.md`.

## How the owner works (apply always)

- Never impose a design: every decision is a hypothesis; taste and adjust,
  like cooking, backed by numbers from this project and outside research.
- Use separate agents to judge your own work. For tests of your own
  design, run an independent agent alongside your own attempt and compare
  (see `bench/map/COMPARISON.md`: the independent run caught the
  conductor's bias). Probe, don't only read.
- The owner works from iOS Safari; keep replies short and plain.
- Keep the owner's real name out of the repositories.

## What Polymechania is

Split out of Gnomon on 2026-10-28: the right worker for every part of the
work (models, tools, scripts, checks), organised by price and track record,
with Gnomon (github.com/5kasgard/gnomon) as its record. The vision has grown
into a world for people's AI that is not a chat: one private world per
person with many regions, a shared commons, guides, a god's-eye pixel-art
view like a city builder, plain underneath with any theme on top.

## Decisions so far

- Name Polymechania; terminal command `mekh`; mark μ.
- Plain core, themes on top: a theme may rename, retell and restyle, never
  change a fact, number or rule (code: `concepts.py`, `events.py`,
  `worlds.py`; themes Plain, Kagamigakure, Hollow Acre).
- Words: world (your place), region (a project), commons (shared), theme
  (the look; code still says "world", to be renamed), pack.
- Two versions for people: Free (their own Claude while they talk) and Paid
  (keeps working while away; we pay model use via our API account);
  Advanced: own key or self-host. Untested.
- Architecture hypothesis (not yet written up): no long-lived agents (short
  bounded runs, state only in the record), one plain protocol any engine
  can speak, everything else a worker or a view.
- The map must be honest: roads drawn from real grants, labelled with who
  can cross; "no one but you crosses", not "isolated"; plain table one tap
  away.
- Economy: earnings minted only from audited work, bounded, not tradable;
  "cheat the method all you like, never the result".

## Evidence and tests done

- Stat cards: research in `docs/evidence.md`; pre-registration
  `prereg/cards-v2.md` with two amendments (after two independent reviews,
  `prereg/review-v1.md`, `revi

VISION (headings)
# Polymechania: the picture we are designing toward
## The idea in one line
## Words (decided after review 1)
## How it can run (decided after review 1)
## Scene 1: opening it
## Scene 2: the shape of a world
## Scene 3: how you see it, and how things move
## Scene 4: attention, interruptions and quiet
## Scene 5: giving work, and getting it back
## A pattern across the scenes
## Why a city builder fits
## Hypotheses to test cheaply
## Lessons from Google's AI Test Kitchen (hypotheses, 2026-10-29)
## Open questions

QUESTIONS (answer each, under 900 words total, plain English, short sentences)
1. Where is complexity growing fastest? Which of it is essential (the goals need it) and which accidental (how it is built)?
2. What would you cut, merge, defer or simplify? Name specific items from the counts, queue and PRs above.
3. What in the working process causes the debt? Give 3-5 simple rules that would slow it.
4. Are all three Gnomon PRs needed now? Merge, fold into one, or drop which?
5. Up to 5 numbers worth tracking weekly to see if complexity is falling.
6. What might the owner not be seeing?
