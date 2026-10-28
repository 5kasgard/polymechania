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

## Open, in rough order

1. **Architecture** (`docs/architecture.md`, revision 2, after
   `docs/architecture-review-1.md`). Next: the cheap tests T2 (log the
   token split per run), T8, T9, T11, T12; then T1 (shapes against each
   other, needs longer tasks). Owner ideas folded in: a standing self per
   resident, a free clock (Cloudflare cron) apart from the costed worker,
   a thin boot through the door.
2. **Gnomon blockers before anything runs unattended** (found by probes;
   file as Gnomon issues, this session had no push access to Gnomon):
   one future-dated write locks the whole log (`E_CLOCK`), so time must
   come from the gate; no revocation (#49); handoff chains fork silently;
   lease/release with fencing epochs as event kinds; the gate is only on
   the MCP path (#50); remote MCP for the Free version.
3. Cheapest vision tests from `docs/vision-review-1.md`: the words card
   sort, the menu as a picture, notification volume from logs.
4. E1 (can cards be gamed), when the owner chooses: needs the Anthropic key
   in the door (below) or the Pro-plan route with data held in the door
   (amendment 3, not yet written).
5. Cost fields on cards (fixed cost per call, marginal cost, setup, where it
   runs) and budgeting to plan limits; replay pilot and floor data.
6. Waitlist test for Free and Paid.
7. Rename "world" files to "themes" in the code.

## Things left running or pending

- **The door:** Cloudflare Worker `polymechania-door` (code in
  `bench/cards/door/`), behind Cloudflare Access (app `polymechania-door`,
  service token expiring in 90 days) and a door token. The Anthropic key is
  NOT set. Credentials are not in the repo; a new session must make its own
  or the owner must re-issue them. Delete the Worker, Access app and token
  if the door is abandoned.
- **Gnomon PR #47** (teams of models move out) is open, awaiting the owner.
- **Gnomon issues #48-#51** (side channels, no revocation, plain-text log
  with unauthenticated appends, auto mode across compartments).
- The scheduled heartbeat task ran once and is finished.
