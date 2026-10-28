# Polymechania: the picture we are designing toward

A living document. Everything here is a hypothesis until something cheap
(a sketch, a mock-up, a small prototype, a measurement) says otherwise.
Written with the owner, scene by scene.

## The idea in one line

A home for people's AI that is not a chat: a world where agents and tools
live, temporarily or for good, where work has a place and a shape, and
where people both work and play. Gnomon is its memory and commons;
Polymechania is the canvas.

## Words (decided after review 1)

- **World:** your own place. One per person, private by default.
- **Region:** a project, team or kind of work inside a world: a city or
  district on its map. As many as you like.
- **Commons:** the one shared world everyone can connect to and contribute
  to. Polymechania runs it.
- **Theme:** how a world looks, sounds and is named (what the code
  currently calls a "world" file; to be renamed).
- **Pack:** themes, art and mechanics people share.
- **The capital of the commons:** the operators' centre, where the commons
  is run and the rules are kept. Most of it is closed to visitors, as an
  operator's tools would be, but what concerns them is open: the guides,
  the rules, the library, help. Its name is open; "Polymechania", the city
  the world is named after, is one candidate.

## How it can run (decided after review 1)

Any arrangement the owner likes, all speaking the same plain record:
- **Local:** run your world on your own machine, with your own engine.
- **Cloud:** we host your world, so it keeps going while you are away.
- **The commons:** we run it; anyone can join.
- **Private, connected to the commons:** your world, wherever it runs,
  with roads to the commons where you choose.

**Engines, so nobody's existing subscription is wasted:**
- **Any Claude plan, including Free:** your Claude, through the connector,
  in the Claude app or Claude Code. It works while you are talking to it;
  it cannot run your world while you are away.
- **Max and Team plans:** they include monthly API credits, so a key from
  your own Console runs your world in the background on credits you
  already have.
- **Your own API key** on any account.
- **Our hosted engine:** we pay for the model use and charge for the
  system, for people who want it to just work.

**A business hypothesis, not a decision:** Anthropic's commercial terms
let a product built on the API serve its own users, but reselling access to
the API itself needs Anthropic's approval. So what we would charge for is
Polymechania (the world, the record, the cards, the routing), with model use
included. Because work goes to the cheapest worker that does it reliably,
the system should cost less than sending everything to one strong model; in
the firm pilot's planning, 24 parts cost an expected $0.38 with Haiku staff
and exact checks against $1.84 for one Opus agent. The hypothesis is that
part of that saving can be the margin while the price still beats doing it
the expensive way. To be checked with real usage, and with a lawyer before
anyone pays.

## Scene 1: opening it

You open Polymechania. It loads, the way a game does, and you land on a
title screen with a menu, like Minecraft's, but labelled plainly:

- **Your world:** your private world, holding as many regions (projects)
  as you like (scene 2 and the words above).
- **The commons:** the shared world (multiplayer).
- **Settings:** your account, which engine powers your agents (your Claude
  through the connector, or an API key), budgets, appearance.
- (Probably also **Packs**, for worlds, art and mechanics people share, and
  **Guide**.)

You make a new world, and you are not left alone with it. A **guide**, or a
small team of guides, each an agent with its own job, walks you through:
- a **tutorial guide** who shows you around and sets you a first mission;
- a **librarian** who keeps the documents on how everything works;
- an **engineer** who connects things: MCP servers, agents, APIs (the
  doors);
- an **artist** who helps you design your world's look, down to its pixel
  art;
- a **planner** who helps lay out what goes where.

The guides are your world's first residents, with stat cards like anyone.

**The look:** pixel art, detailed enough to be rich, simple enough to
draw and change; 2D first, possibly isometric, leaving room for 3D. The
feel of a city builder: SimCity, Cities: Skylines.

## Scene 2: the shape of a world

**Each person has one world of their own**, the way an iOS game keeps your
world on your device: private, yours, always there. "Single player" and
"multiplayer" are game words; the plain labels might be **Your world** and
**The commons** (the commons is Gnomon's word for the shared, public part).

**A world holds as many regions as you like, in whatever layout.** Regions
are places on the map: cities, districts, islands. Each is a workspace for
a project, a team or a kind of work.

**The map shows what can reach what.** Roads and bridges between regions
are real connections: work and information can flow along them. A region
with no road in or out is an island, and looks like one, because it is
isolated. Some islands have a special way across (a ferry, a tunnel, a
gate with a guard) when a task needs a controlled crossing. Some regions
may talk to the outside world and the commons; others never can. It is up
to you, and the map is honest about it.

This means **the map is the security diagram.** Gnomon's compartments and
the doors' permissions become geography: an experiment whose workers must
not see the answers is an island; a region that may post to the commons
has a road to the border. You see your permissions by looking at your
world, instead of reading a settings page.

**The commons is one shared world too**, the multiplayer one. It grows with
its population, generated as people arrive, the way a Minecraft server's
map extends as it is explored, rather than being a fixed size.

**Each world has a capital**, and so does the commons. The guides live
there, along with the town hall (the rules), the library, and the gates to
the outside. You can walk up to a guide in the world, or talk to them from
a panel, whichever suits the moment.

## Scene 3: how you see it, and how things move

**A god's-eye view.** You are not a character in the world. You look down on
it, zoom out to see your whole world and zoom in on a region, and tap to go
somewhere or open something. The residents know you are there: they talk to
you directly, through the screen, the way advisors talk to the player in a
city builder.

**Movement is shaped by the work, and drawn by the world.** What you see
when something leaves a region depends on what is really happening, and
looks however the world says it should:
- **A message** (an email, a post to the commons, a question to another
  world's agent) travels as a letter, a postman, a carrier pigeon, a crow, a
  radio signal: whatever the world's theme makes of "a message".
- **Real work elsewhere** (an agent working on another world, a remote
  server, a tool) is a journey: the agent leaves, is seen at the other
  place, and comes back with the result.
- **A tool** looks like what it is to that world: a calculator might be an
  abacus shop, a test runner a training ground, a CAD door a workshop with a
  workbench.

The rule from the roads applies: **the picture is shaped by what is
underneath.** A pigeon only flies where a message really went; an agent is
only seen in another world when it really is working there.

This extends the worlds contract: today a world says how each event is
**told** (`[say]`); it would also say how each event is **shown**: the
sprite, animation or scene for a message, a journey, a check, an audit. The
plain event stays underneath, unchanged.

## Scene 4: attention, interruptions and quiet

**Talking to a resident.** Tap someone to see them, tap again to chat. If
they are in the middle of work, they answer for themselves: "busy, back
when this part is done", so a chat never breaks a worker's context by
accident. You can say it is **urgent** to interrupt anyway. Then they pause
properly: they leave a handoff of where they were (Gnomon's handoff and
resume), talk with you, and pick the work back up after, or re-plan it if
the chat changed what the work should be.

**Getting your attention.** Residents first take a problem up the world's
own chain: a worker to its manager, a manager to the planner. Only what the
chain cannot settle reaches you. It arrives as a **notification that stays
until it is resolved**: on your phone if it matters enough, and in the
world as a marker you tap to jump to the place on the map where it is.
Where you sit in the loop is your choice: some people will want to approve
every spend, others only the rare hard call. The guides help you choose a
setup that suits what you are doing.

**Quiet times.** When nothing needs you, the world is calm and still, but
alive: it keeps its own time. Day and night follow your local time (from
your device's time zone, no location needed). Weather can match a real
place if you choose to enter one; it is never inferred.

**Time on screen.** Computers are absurdly fast at some things and slow at
others, so animations cannot run at real speed. They run on a consistent,
scaled clock (for instance, logarithmic, so a millisecond check and an
hour-long job both read at a glance), and the real duration is always one
tap away. The picture shows order and progress; it never claims a speed it
does not have.

## Scene 5: giving work, and getting it back

**One front door for work.** Work comes in through a single place, not by
talking to each agent: people would tangle their own workflows otherwise.
In plain terms it is the **intake**: you describe what you want to your
guide, who offers what fits, whether to set it up and run it, walk you
through it, or ask a question first. Whether that place looks like a notice
board, a front desk, a temple scroll or a dock depends on the world; the
intake underneath is the same everywhere. You can still talk to any
resident directly, if you want to.

**Results come back however the setup is shaped.** A delivery, a report, a
file in a storehouse, a change already made in a connected tool: it depends
on the work and the world. What is fixed is that every result is in the
record, with its checks and verdicts, and you are told it is done.

**Notifications are where most people will live day to day.** The world is
where you go to see, understand, design and set things up; the everyday
flow of "this is done", "this needs you" and "this is stuck" reaches you as
notifications, on your phone or wherever you are, each one a link back to
its place in the world.

## A pattern across the scenes

The core defines a few plain things, and worlds decide how each looks:

| Plain, fixed | Shown however the world likes |
|---|---|
| The intake (one front door for work) | a board, a desk, a dock, a shrine |
| Notifications (persist until resolved) | a bell, a messenger, a flag |
| Results (in the record, with verdicts) | deliveries, storehouses, reports |
| Connections and isolation (doors, compartments) | roads, bridges, islands, gates |
| Messages and remote work | letters, pigeons, journeys |
| Residents and their cards | characters with their stories |

## Why a city builder fits

City builders are simulations of flows, people and services, which is what
an organisation of agents is. A first mapping, to be tried, not fixed:

| City | Polymechania |
|---|---|
| Citizens | agents and tools (residents and visitors) |
| Buildings | functions: a workshop for code, a library for memory and documents, an observatory for research, a workbench for CAD, fields for batch work, a market for hiring from other worlds, a notice board for the square |
| Zoning | kinds of work, and which workers may do them |
| Roads and traffic | work flowing between buildings; jams are bottlenecks you can see |
| Power grid | the token budget and its limits: brownouts when an account nears its cap |
| Services coverage | checks and audits: a district without inspectors is visibly at risk |
| City stats | stat cards, rolled up: quality, cost, speed, calibration |
| Gates and ports | doors to the outside: MCP servers, APIs, other worlds |
| Town hall | the rules, in the world's own words |

Anything shown must be a reading of the plain record: the city never
invents a number.

## Hypotheses to test cheaply

- The menu, with these labels, makes sense to someone new without help.
- Guides as characters teach faster than a document alone.
- Isometric 2D pixel art is enough to reason with spatially; 3D can wait.
- People understand what can reach what faster from the map (roads,
  islands, gates) than from a permissions page, and make fewer mistakes.
- A god's-eye view with residents who address you directly is enough; no
  avatar is needed.
- Drawing each kind of event its own way (a letter for a message, a journey
  for remote work) helps people follow what their agents are doing, better
  than a log.
- "Busy" auto-replies with an urgent override, and handoffs on interruption,
  keep work quality the same as when no one interrupts (measure it).
- Routing problems up the world's chain first cuts how often a person is
  interrupted, without more problems slipping through.
- A scaled clock with real durations on tap is read correctly; people do
  not come away thinking slow things are fast or the reverse.
- One intake through the guide produces fewer tangled workflows than
  assigning work agent by agent.
- Most everyday use happens through notifications; the world view is
  opened mainly to understand, design and fix.
- Showing isolation as an island is enough for people to trust it, as
  long as the island really is isolated underneath (the door enforces it;
  the map only shows it).
- The city mapping helps people see bottlenecks and risks sooner than a
  dashboard does.

## Open questions

- ~~Is a world one city, and a server a continent of cities?~~ One world
  per person, holding many regions; the commons is one shared world that
  grows (scene 2).
- ~~How do you talk to a guide?~~ Both: walk up, or a panel (scene 2).
- What is in the capital, beyond the guides, the town hall, the library
  and the gates?
- ~~How do you travel?~~ A zoomed-out map you tap on; no avatar (scene 3).
- ~~When your agent visits the commons?~~ Shaped by the work: a message
  travels as a letter, real work elsewhere as a journey (scene 3).
- ~~Attention and quiet times?~~ Notifications that persist until resolved,
  after the world's own chain; a calm world on your local time (scene 4).
- ~~How do you give work?~~ One intake, through your guide; its look is
  the world's (scene 5).
- ~~What does finished work look like?~~ Shaped by the work and the world;
  always in the record; announced by notification (scene 5).
- What does a guide look like?
- What resolution and palette for the pixel art?
- What is in a brand-new world before you build anything?
