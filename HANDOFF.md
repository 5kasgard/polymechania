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
  `prereg/review-v1.md`, `review-v2.md`). Mechanism in `polymechania/cards.py`
  (audit-corrected estimate, tested). **E1 has not run.**
- Map honesty: `bench/map` (independent), `bench/map-mine` (conductor),
  `bench/map/COMPARISON.md`. Claim fails as written; holds with a rule.
- Engines by plan: `docs/engines.md`. Free has no unattended option; Pro can
  wake on Claude Code scheduled tasks (hourly at most, on its own usage);
  Max and Team include API credits; subscription logins may not be used by
  third-party apps.
- Live test passed (issue #1): a scheduled task on the owner's Pro plan woke
  unattended, read the repo and reported correctly.
- Vision reviewed independently: `docs/vision-review-1.md` (contradictions,
  first-week gaps, evidence, cheapest tests).

## Budget (owner, 2026-10-29)

About **$4.25 of API credit** is left (after about $0.72 spent on T2, T2b,
T2c and T11), then $0.03 on T12c and $0.08 on T12d: about **$4.14 left**. Workers AI used about 7,700
neurons of the 10,000 free on 2026-10-28 UTC. Spend it only on what only the API can measure (Claude's
caching, Claude's own pass rates). Use first, in this order: published
results; Cloudflare Workers AI through the door's `/ai` route (free
allowance 10,000 neurons a day; Gemma 4 26B about 9k neurons per million
input tokens, 27k per million output); sub-agents on the owner's Pro plan
(usage, not dollars). Hugging Face is a free account: papers and datasets,
not inference. Every pre-registration states its API cost bound.

## Open, in rough order

Rules for every session: `CLAUDE.md` (routing, unbiased testing, budget).
Owner's saved skills (any chat): route-and-test, taste-and-adjust,
session-handoff, careful-live-changes.

**Done 2026-10-28/29 (all audited, records in `bench/`):** T12d (`bench/self/RESULTS_D.md`: labels barely protect, +9; keeping requests out of the packet does, 89% vs 68%; owner label followed more, +15; $0.08); a task-loader bug fixed (second call returned hard tasks as easy; earlier results checked clean); Gnomon #55 (start-packet authority) filed; T12c (`bench/self/RESULTS_C.md`: T12b holds with a Claude Haiku resident, +33 points, $0.03; Llama judge scheduled after the free reset); T2 thin boot
(1,486 tokens; caching holds; cached Haiku-then-Sonnet cascade 24/24 at a
quarter of Sonnet's price); T2b/T2c (set thinking explicitly; off for Haiku
on this work); T11 runaway caps hold; T12b (`bench/self/RESULTS_B.md`: a
fresh context did not keep the resident in character; *not writing a
non-owner's conflicting requests into its next start packet* did, +35
points); S1 (`bench/speed/RESULTS.md`: 8 model calls at once 8.9x faster for
free; Actions has 4 CPUs but pays only for long jobs; Codespaces not
reachable from these sessions); `docs/routing.md` (reviewed by Haiku and
Llama); `bench/verify.py` (exact half of every audit, free); CI green again.

**The open list now lives in one place: `queue.json`** (rendered as
`docs/queue.md` by `python bench/queue.py`; CI checks it). Every open item,
with its status, blocker, cost, who it needs and next step. Update it when
you start or finish something; do not keep a second list here.

**Note for sessions:** on 2026-10-29 a duplicate run of the same session
worked in this folder at the same time (same session id; it committed
work this session was about to do). Before writing, check `git log` and
`git status` for changes you did not make.

## Things left running or pending

- **The door:** Cloudflare Worker `polymechania-door` (code in
  `bench/cards/door/`), behind Cloudflare Access (app `polymechania-door`,
  service token expiring in 90 days) and a door token. **The Anthropic key
  IS set** (2026-10-28, by the owner, in a Console workspace
  `polymechania-e1` with a monthly spend limit); checked: `/health` reports
  it set, one Haiku message went through (26 tokens), and a request with
  tools was refused (400). The door's own credentials are not in the repo:
  a new session issues fresh ones through the Cloudflare connector (a new
  Access service token on the `polymechania-door` policy, and a new
  `DOOR_TOKEN` secret uploaded with `keep_bindings` so the owner's key is
  kept), then revokes the old service token. (2026-10-28 evening: one
  session rotated the existing service token's secret and set a new
  `DOOR_TOKEN`; both live only in that session's scratch folder, so the
  next session issues its own again.) Delete the Worker, Access app and token
  if the door is abandoned.
- **Gnomon PR #47** (teams of models move out) is open, awaiting the owner.
- **Gnomon issues #48-#51** (side channels, no revocation, plain-text log
  with unauthenticated appends, auto mode across compartments).
- The scheduled heartbeat task ran once and is finished.
