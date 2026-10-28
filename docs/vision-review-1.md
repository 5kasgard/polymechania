# Independent review of the vision, 1

By a separate agent (Claude Opus 5.5) that wrote none of `vision.md`,
2026-10-28, after scene 5. Kept as received (lightly formatted); decisions
on each point are made with the owner and recorded in `vision.md`.

## Contradictions

1. Major: "world" means three things: a theme file (README, spec), a
   workspace (scene 1), one per person (scene 2). Pick separate nouns.
2. Major: the scene 1 menu ("My worlds", "Servers") was never updated to
   scene 2's one world plus one commons.
3. Major: "the map is the security diagram" must not replace the plain
   view: a plain permissions table one tap away.
4. Major: roads are not the same shape as compartments. Access is granted
   per session; an agent holding two compartments is a bridge with no road;
   a road suggests every agent can cross. Needs a rule such as "a road
   exists if and only if some session holds both compartments".
5. Moderate: is the map a view or a control? If drawing a road grants
   access, it is a permissions editor and needs confirmations and an audit
   trail.
6. Major: a Claude connector cannot run a world while you are away, keep
   time, or push notifications; background work needs an API key and a
   server: real cost, and a place where data lives.
7. Moderate: guides "with stat cards like anyone": tutorial, library and art
   work has no checkable verdicts, so their cards would be empty or invented.
8. Moderate: does the guide only take requests in, or choose who does them?
   The spec has the planner assign by the record.
9. Moderate: sprites cannot be checked the way text is; every shown event
   must open to its plain event.
10. Moderate: the commons is a public record of claims, not a place; a map
    that grows as people arrive places claims with no reason.
11. Minor: a "busy" reply written by the working agent breaks its context
    anyway; something else must answer for it.

## First ten minutes

Labels split one thing two ways; five guides at once is too many (start
with one); "one front door" against "talk to anyone"; an empty new world
gives the god's-eye view nothing to show; engine, budget and region are not
explained before first use.

## First week (missing)

Cost estimates before work runs and hard stops; privacy and where contents
are stored; what happens when the engine runs out (pause with handoff, fail,
or fall back); undo, and which actions need approval first; trusting other
owners' agents; sharing with a collaborator; moderation in the commons;
accessibility (screen readers, colour, reduced motion); phones (44 pt tap
targets, battery); offline and export.

## Outside evidence

- City metaphor: CodeCity (Wettel et al., ICSE 2011) helped program
  comprehension against Eclipse plus Excel, on static structure; evidence
  for managing live agents is thin.
- 2D against 3D and realism: 3D helps rough layout, hurts precise relative
  judgements (Tory et al. 2006; St. John et al. 2001); more realistic
  displays often worsen performance though people prefer them (Smallman and
  Cook 2011). Supports 2D first and argues against rich detail for anything
  monitored.
- Gamification: small effects; game fiction not a significant moderator
  (Sailer and Homner 2020); context-dependent (Hamari et al. 2014). Games
  with a purpose work when the game is the task (von Ahn and Dabbish 2008).
- Notification fatigue: 49-96% of drug alerts overridden (van der Sijs
  2006); 74-99% of monitor alarms needed no action (Paine 2016); but removing
  notifications caused anxiety (Pielot 2017). Key number: the share of
  notifications that needed a decision.
- Interruption: people compensate with speed at the cost of stress (Mark et
  al. 2008); LLMs struggle to recover from mid-task changes (InterruptBench,
  arXiv 2604.00892).
- Prior art: Gas Town (a town with a Mayor as the single front door; used
  mostly through its plain feed) and Pixel Agents (coding agents as
  pixel-art office characters, stuck agents flagged visually).
- Not found: controlled studies of spatial views against dashboards for
  supervising agents, or of isometric pixel art on phones.

## Cheapest tests first

1. Nouns: a 5-person card sort. 2. Menu labels: a static image, "where would
you start a project?". 3. Compartments against roads: draw the road graph
from real Gnomon session grants and count bridges with no road. 4.
Notification volume: replay pilot logs with and without routing up the
chain. 5. Map against permissions table: paper prototype, 5-8 people. 6.
Interview Pixel Agents users. 7. Scaled clock: estimate durations from a
mock. 8. One guide against five against a document. 9. Engine feasibility:
an agent overnight on a Pro plan through the connector. 10. Interruptions
with and without handoff on bench tasks. 11. City against dashboard for
bottlenecks, only after 1-5 pass.
