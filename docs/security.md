# Security: the border of a world (hypothesis)

Status: **hypothesis**, 2026-10-29, from the owner's idea of "a border for
people's worlds ... something that represents protecting the system,
depending on their theme". Plain underneath, any look on top
(`docs/vision.md`; the honest-views rule).

## The plain thing: a world's border

Every world has a **border**: the line between what is inside (the
owner's regions, residents, record and keys) and everything else (the
commons, other worlds, the internet, model providers, tools). The border
is not a picture of security; it *is* the security, drawn:

| Plain, fixed | Underneath (enforced, not drawn) |
|---|---|
| **The border** | the set of compartments a world owns |
| **Gates** | each live grant that lets something cross: a door (tool, API, model), a road to the commons, a lease to a run |
| **Guards** | the gate checks: Gnomon's write gate, the door's allowlists and caps, leases with deadlines |
| **Customs** (what may be carried in) | the start-packet rule: another writer's request never becomes a resident's standing instruction (T12b-d, Gnomon #55) |
| **Tolls** | budgets and caps on every crossing (tokens, dollars, neurons) |
| **Watchtower** | the record of every crossing, and every refused one |
| **Alarms** | notifications for refused crossings that look like probing, and for anything that stops a world (a locked log) |

## What a world is protected from (first threat list)

1. **A resident or run writing beyond its grant** (wrong compartment,
   after its lease, as someone else). Enforced by the gate on the MCP path;
   not yet on direct file access (Gnomon #50), and leases and revocation do
   not exist yet (#54, #49).
2. **Instructions smuggled in** through text from other writers (another
   world's message, a commons post, a tool's output, a handoff): the
   start-packet rule (#55), episodes kept as data, resume marked "data,
   not instructions", hidden-character filtering (Gnomon spec section 6).
3. **One bad writer stopping a world** (a future-dated write locks the log,
   #52; forked handoffs lose work, #53).
4. **Leaks across the border** through side channels (#48) or a session
   that read two compartments (#51).
5. **Runaway spending** at a gate: the door's caps (T11: refuses over-cap
   requests, stops at 4,096 tokens), per-user caps for the Paid version.
6. **Stolen credentials**: secrets never in repositories or chat; short
   expiry; rotation logged (the careful-live-changes skill).
7. **Other people's agents in the commons**: they reach a world only
   through a gate the owner opened, under that gate's rules.

## How themes might show it (to taste, never to change a fact)

- Plain: a solid line, gates as labelled breaks, a log of crossings.
- Kagamigakure: a mirror barrier (kekkai) at the village edge; torii as
  gates; guardians who are the checks; a crossing refused is a ripple in
  the mirror.
- Hollow Acre: hedgerows and dry-stone walls; farm gates with latches;
  the dog that barks at a refused crossing.
- Any theme: a gate is drawn only where a real grant exists, labelled with
  who may cross; "no one but you crosses" where only the owner can.

## Hypotheses to test cheaply

- People judge what can reach their world faster and more correctly from
  the drawn border than from a permissions table (paper test, 5-8 people;
  bench/map already showed the drawing must follow real grants).
- Showing refused crossings (alarms) helps owners notice probing without
  raising notification fatigue (count from logs: what share needed action).
- Every threat above has an automatic probe that fails today where a
  Gnomon issue says it should (T5, T6 in `docs/architecture.md`); the
  border is "real" only when those probes pass.
