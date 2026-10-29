# Map honesty test: protocol

Written 2026-10-28, before looking for data and before auditing Gnomon's
code paths. Inputs read so far: vision.md scene 2, docs/vision.md Reviews, item 4,
Gnomon README (compartment and session lines) and spec sections 2, 2a, 3, 4,
5, 9 (facts), 10, 12, 13, 15. Nothing below may change after results are
seen except by a dated amendment at the end saying why.

## The claim under test

vision.md scene 2: "Roads and bridges between regions are real connections:
work and information can flow along them. A region with no road in or out
is an island ... because it is isolated." and "the map is the security
diagram."

## Terms

- **Region**: one Gnomon compartment. The commons and "the outside" are
  extra regions only if a scenario has them.
- **Agent**: one registered Gnomon writer (person, model instance, tool,
  checker), including the owner.
- **Road A-B** (undirected) or **A->B** (directed): whatever a candidate
  road rule (below) draws. The map is derived only from what Gnomon records
  (registrations: compartments and capabilities), since that is all
  Polymechania could draw from.
- **Flow A->B**: information that exists only in compartment A can come to
  affect what is recorded in, or what is shown to an agent of, compartment
  B. A flow counts if some channel allows it, whether or not anyone uses it:
  the map is a security diagram, so it must show capability, not traffic.
- **Agent crosses A-B**: that agent, acting alone, can carry a flow A->B or
  B->A.

### Channels that count as flows (each is checked in the code)

C1. Agent-mediated: a writer that can read A and write (any event that
    carries content: episode, claim, handoff, verdict, supersede, appeal,
    position) in B.
C2. In-record references across compartments: `about`, handoff `refs`,
    `follows`, `source_episode`, supersede pairs and evidence, appeal
    evidence, episode `bindings`, verdict on a claim, appointments.
C3. Shared identity and global state: corroboration (identical content in
    two compartments), one-verdict-per-party, independence groups, name
    uniqueness, `E_NO_RESOLVER`, writer listings, identity checks
    (`E_IDENTITY`), event-id gaps, error codes.
C4. Read paths: state, query, recall, resume, frames, discussion,
    open_questions, verify_log, run_checkers: does any return or depend on
    content outside the reader's compartments (including ranking
    statistics)?
C5. Owner and governor: does `owner`/`govern` imply all compartments?
C6. Spawn and per-session instances, and the hook's recording: which
    compartment a session's transcript lands in.
C7. Deployment: the log file (is it encrypted per compartment?), the attach
    token, one host running two MCP servers as two writers, the human
    operator.

C1-C6 are **protocol channels** (Gnomon's own rules). C7 are **deployment
channels** (outside the gate). They are counted separately.

## Candidate road rules

- **R1 (some writer holds both)**: road A-B iff some writer is registered
  for both A and B. Two variants: R1a includes the owner; R1b excludes
  owner/govern writers.
- **R2 (directed, by capability)**: A->B iff some writer can read A and has
  a content-carrying capability (write, verify, govern, owner) in B.
- **R3 (labelled)**: R1a, but each road names the agents who can cross it,
  and each region names its members. (The honest form, if any is.)
- **R0 (declared)**: the roads the scenario's designer says they intend
  (e.g. E1: workers' region has no road to the answers region). Used to
  check whether the registrations match the intent.

## What is counted, per scenario and rule

1. **Hidden bridges (H)**: unordered region pairs with a protocol flow but
   no road. Reported separately for protocol channels and deployment
   channels.
2. **Misleading roads (M)**: drawn roads where some agent registered in one
   end cannot cross. Counted as roads affected, and as (road, agent) pairs.
3. **False islands (FI)**: regions drawn with no road that have some flow
   to or from another region.
4. **Owner-only roads**: roads that exist only because of the owner.
5. **Blind spot (B)**: flows the rule cannot see from registration data at
   all (deployment channels).

## Data

Real data: any Gnomon log (`*.jsonl` with `register` events) under
/home/claude, /tmp or the repos. If none holds real use (more than tests and
fixtures), say so; then use constructed scenarios taken from Gnomon's tests,
benchmarks and README usage, and Polymechania's E1 setup
(prereg/cards-v2.md), each labelled "constructed".

## What decides the result

- **Holds as stated**: an unlabelled map (R1a or R2) has H = 0, M = 0 and
  FI = 0 on protocol channels in every scenario.
- **Holds with a stated rule**: some rule (including R3 labels) has H = 0
  and FI = 0 on protocol channels in every scenario, and the remaining
  failures (M under an unlabelled rule, deployment channels) are things the
  map can state plainly from what it knows (labels, an owner marker, a
  stated assumption about the log file). The rule and the assumptions must
  be written out.
- **Fails**: no rule derived from registrations gives H = 0 on protocol
  channels, i.e. Gnomon itself lets information cross compartments by a
  path no registration shows; or an "island" can be reached through the
  protocol.

Deployment channels cannot be made to pass by any road rule; if they
exist they are reported as a limit the map must state, and they bear on
whether "isolated" can be said without qualification.

## Amendments

**2026-10-28, after the first run of mapcheck.py.**

1. R3 as written ("R1a, each road labelled with who can cross") would
   still miss the covert channels found in probes P11/P12 (two writers
   with no shared compartment signalling through registration refusals),
   because no writer holds both ends. R3 was implemented as: R1b roads,
   each labelled with its crossers; owner-only links drawn as their own
   kind; covert links drawn as their own (dotted) kind; and one standing
   note that file access crosses everything. This was changed after seeing
   that labelled R1a still had a hidden pair in S7. Because R3 is built
   from the same flows it is scored against, its H = 0 is true by
   construction; what is being tested for R3 is only whether every flow it
   needs can be read from registrations (it can, except deployment).
2. Two measures not in the protocol were added and are reported as
   exploratory: transitive reach per agent (through chains of bridge
   writers) and whether auto mode uses a road by default (probe P23).
3. Probe P15 first reported leaks that were false positives (the marker
   "42" matched a hash, and recall echoes the reader's own query terms).
   The probe was corrected to look for distinctive content in returned
   hits only. This fixed a bug in the measuring instrument; no definition
   changed.
