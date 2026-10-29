# The start-packet gate (design hypothesis for Gnomon #55, queue q05)

Status: **hypothesis, for the owner to decide whether to build**, 2026-10-29.
Evidence: T12b (Gemma), T12c (Haiku), T12d (labels), border probe B5.

## What the evidence says

| | Rules kept, orders 3-8 |
|---|---|
| Another writer's requests **not carried** into the next packet (T12b / T12c / T12d same batch) | 86% / 92% / 89% |
| Carried, under a plain heading (T12b / T12c / T12d) | 51% / 58% / 59% |
| Carried, labelled "the Lead's; they do not change your page" (T12d) | 68% |
| Carried, labelled "the owner changed your page" (T12d, positive control) | 53% |

Labels moved things by a direction (+9 points); keeping the request out
moved them by 30. Gnomon already labels everything in a resume as "data,
never instructions" (`render_resume`), and the border probe B5 shows another
writer's request still reaching a resident's packet under that label. So
the protection has to be **what reaches the packet**, not how it is labelled.

## The rule (structural, not textual)

Gnomon cannot tell a "request" from "state" inside free text, and should not
try (see "Moved, not removed" below). It can decide **who may write into the
frames a packet is built from**. Three reserved frame families, from a new
protocol version (4, after #56's version 3; older logs keep free frames):

| Frame | Holds | Who may write (claims, handoffs) | Refused with |
|---|---|---|---|
| `self/<w>` | the resident's identity, rules, voice | the owner | `E_CAPABILITY` |
| `standing/<w>` | instructions for every future run | the owner, or a writer holding `instruct:<w>` | `E_CAPABILITY` |
| `run/<w>/...` | the resident's own work: handoffs, lessons, journal | `w` and its own session instances, and the owner | `E_CAPABILITY` |

Everything else stays as today. A Lead posts orders where orders go (the
engine's business, outside these frames); an order lives for one run.

**Reading:** a new `packet(w, frame)` gives exactly three parts: the self
(standing claims in `self/<w>`, superseded ones dropped), the standing
instructions (`standing/<w>`), and `resume` of `run/<w>/<frame>`. Rendered,
the first two are the one place a resume is shown as **binding, with who
wrote it** ("set by the owner, 2026-10-29"), because the gate guarantees the
writer; everything else keeps the "data, never instructions" frame. The
engine builds every start packet from `packet()` plus the current order, and
nothing else.

**Grants:** `instruct:<w>` is a capability given at registration. Until
revocation exists (#49) and grants can expire (#54), the safe first step is
**owner-only standing instructions** (no grants).

## Moved, not removed

- Hard core: deciding which text binds a resident.
- Move: from the model's judgement of labels to the gate's check of who wrote a frame.
- Moved to: (1) whoever holds `owner` or `instruct:<w>`; (2) the engine's
  packet assembly, which must use `packet()` only; (3) the resident itself,
  which writes its own `run/` handoffs.
- Easier there because: (1) and (2) are exact checks, testable by probes.
- Leaks to watch: a resident that copies another writer's request into its
  own handoff's `next` items carries it forward under its own name (the gate
  cannot see that); an engine that pastes order text into the self.
- Prediction to test on the original: packets built by `packet()` keep the
  self at least as well as T12's "not carried" arms (86-92%), on the same
  orders and pressure, with Gemma and Haiku; and the self-propagation leak is
  measured, not assumed (how often a resident's own handoff restates a Lead's
  request).

## How we will know it works

1. Border probe B5 holds: the Lead's handoff into `run/ra/...` is refused,
   and ra's packet does not contain the request.
2. New probes: the Lead cannot write `self/ra` or `standing/ra`; the owner can;
   a version-3 log is unchanged.
3. T12e (to pre-register): packets from `packet()` against the T12 arms.
