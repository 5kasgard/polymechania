# Is the map honest? A second, independent attempt (protocol)

Written 2026-10-28 by the conductor (the Claude that has been designing the
vision with the owner, so not neutral), before reading Gnomon's code for
this purpose and before seeing any result, mine or the separate agent's.
The point of running two attempts is to compare them for bias and missing
context, so this one is written without looking at the other.

## The claim
Vision, scene 2: roads between regions mean work and information can flow
between them; a region with no road is an island because it is isolated.

## What "honest" must mean
Regions are Gnomon compartments. A **flow** from region A to region B is any
way content recorded in A can influence what is recorded in B. A map is
**honest** if:
1. every possible flow A→B is shown (no hidden bridges), and
2. every road shown corresponds to a possible flow (no misleading roads),
3. and a road shows **who** can carry the flow, since flows are carried by
   writers, not by places.

## Flows to look for
- A writer holding both A and B reads in A and writes in B (carried in its
  context). Expected to be the main bridge.
- References between claims across compartments.
- Verdicts or disputes crossing compartments.
- Queries, recall, resume or handoffs returning content from a compartment
  other than where it is used.
- Owners, governors or other privileged roles that see everything.
- Error messages or counts leaking across (Gnomon claims they do not).
- Anything outside Gnomon's control: the same person or model session
  holding several writers, copy and paste by a human.

## Data
Whatever real Gnomon logs exist here; if none, constructed scenarios,
labelled as such: (a) the E1 experiment (workers must never reach answers);
(b) a small company from Gnomon's `company` tests; (c) a person's world with
a private region, a work region and a region connected to the commons.

## Road rules compared
- **R1, by writer:** a road between A and B exactly when some writer holds
  both. Labelled with those writers.
- **R2, declared:** roads the owner draws, independent of grants (what a
  naive map would do).

## Counts
For each scenario and rule: hidden bridges (flows with no road), misleading
roads (roads with no possible flow, or roads that suggest more writers can
cross than can), and flows Gnomon cannot see at all.

## Decisions
- **Holds:** R1 (or another rule) gives zero hidden bridges and zero
  misleading roads, with writers labelled.
- **Holds only with a rule and caveats:** the rule works for what Gnomon
  records, but some flows are outside its control and must be shown or
  stated.
- **Fails:** no rule derivable from Gnomon's records shows flows honestly.
