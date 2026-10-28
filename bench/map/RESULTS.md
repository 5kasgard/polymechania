# Map honesty test: results

2026-10-28. Protocol: `PROTOCOL.md` (one dated amendment). Code: `probes.py`
(23 live probes against the real Gnomon library, output `probes.json`),
`scenarios.py`, `mapcheck.py` (output `results.json`). Rerun with
`python3 probes.py && python3 mapcheck.py` in this folder.

## Verdict

**The claim holds only with a stated rule, and with two plain caveats.
As written ("a region with no road in or out is an island because it is
isolated") it fails.**

- No unlabelled road rule is honest. Each one either draws roads that most
  agents cannot cross, or hides bridges that exist.
- A labelled map (R3) can be made honest about everything Gnomon itself
  allows, using only registration data. Its labels say who crosses each
  road, mark the owner as able to build any road, and draw covert links.
- Two things no map drawn from Gnomon can make true:
  - **The owner is a bridge to everything.** Under the honest rule there
    are no true islands, only regions that no one except the owner
    crosses.
  - **Isolation holds only inside Gnomon's gate.** The log is one plaintext
    file, and appends are not authenticated.

Confidence: high on the mechanism findings, which come from the code and
were confirmed by live probes. Moderate on how often each failure would
happen in practice, because **there is no real usage data**. All 8
scenarios are constructed.

## Data

I found no Gnomon log with `register` events under /home/claude, /tmp or
either repo. The only `.jsonl` files are benchmark answers and labels.
The 8 scenarios (`scenarios.py`) are constructed, each from a named
source:

| Scenario | Source |
| --- | --- |
| S1 | README quick start |
| S2 | test_mcp.py, including the review fixture where a checker is in lab and private |
| S3 | test_identity.py |
| S4a | E1 from cards-v2, mapped onto compartments |
| S4b | E1 as actually designed |
| S5 | test_company.py, extended to two firms |
| S6 | a scene-2 world in auto mode |
| S7 | one Claude template per region |

## How information crosses compartments in Gnomon (code + probes)

**Sealed.** The gate refuses every in-record reference across
compartments, and it refuses a missing item and a hidden item with the
same error code:

| Probe | What was tried | Refused with |
| --- | --- | --- |
| P3 | `about` pointing into another compartment | `E_REF` |
| P4 | handoff `refs` into another compartment | `E_REF` |
| P5 | `source_episode` in another compartment | `E_COMPARTMENT` |
| P6 | supersession across compartments | `E_COMPARTMENT` |
| P7 | verdict on a claim the writer cannot see | `E_REF` |
| P8 | binding a name to a writer outside the compartment | `E_IDENTITY` (same as no such writer) |

The checks are in `crates/gnomon-core/src/ledger.rs`: `need_compartment`,
`visible_claim`, `visible_item_compartment`, and the handoff and
supersede branches. Other probes:

- **P9:** identical words in two compartments are two separate claims, so
  they do not corroborate each other.
- **P15:** a reader in B only gets nothing from A through state, query,
  recall, frames, resume or discussion.
- **P22:** recall scores for that reader do not change when A grows.
- **P16:** an owner cannot write directly into a compartment it is not in.

**Open channels:**

| # | Channel | Probe | Who | Bandwidth |
| --- | --- | --- | --- | --- |
| F1 | A writer registered for A and B reads both and writes into both (also through MCP, P21) | P1, P2, P21 | any writer holding both | full content with `write`; verdict results only with `verify` alone (the note is not shown in scoped state) |
| F1' | Spawned session instances get **all** of the template's compartments | P18 | every session of a template that holds two compartments | full |
| F1'' | Auto mode records a session's whole conversation into **one** compartment (`--compartment`, or the template's first). A session that read health is recorded into work. | P23 | default behaviour | full, and used **without anyone choosing to** |
| F2 | B's readers see the id of a writer's operator even when the operator is only in A | P10 | set by the owner | small (metadata) |
| F3 | Two `spawn` templates of the same party and surface in different compartments can signal through `E_IDENTITY` refusals on session ids. Sent `[1,0,1,1]`, decoded `[1,0,1,1]`. | P11 | e.g. the S7 setup | 1 bit per attempt; needs direct library access, since no MCP tool registers |
| F3b | The same through instance-id squatting (`c` against `c-x`) and `E_DUPLICATE` | P12 | writer ids that are prefixes of each other | 1 bit per attempt |
| F3c | Gaps in a writer's visible sequence show that it acted elsewhere (a known limit, spec section 5) | P14 | any bridge writer | counts only |
| O | An owner can register a new identity of itself in any compartments, and so build any road | P16 | owner | full |
| R | There is no revocation: a writer's compartments never shrink, so a road can never be closed | P17 | | |
| D | The log is plaintext (P20), and appends are not authenticated: any process that can open the file writes as anyone, including the owner (P19) | P19, P20 | anything with file access | full, every region |

## Results per rule (8 scenarios)

H = pairs of regions with a flow but no road (hidden bridges).
M = roads drawn where some member of an end cannot cross, counted as
roads and as (road, agent) pairs. False islands = regions drawn with no
road that still have a flow.

| Rule | H (protocol) | H (content) | M roads / pairs | Scenarios with a false island |
| --- | --- | --- | --- | --- |
| R1a: road if any writer (owner included) holds both | 0 | 0 | **15 / 46** | 0 |
| R1b: road if any non-owner writer holds both | **8** | 8 | 7 / 28 | **5** |
| R2: road if any non-owner `write` holder holds both | **9** | 9 | 6 / 25 | **6** |
| R3: R1b, labelled with crossers, plus owner and covert links | 0* | 0* | 0 / 0 | 0 |

\* R3's H = 0 holds by construction (see the protocol amendment). What
the test shows is that R3 can be built from registrations alone.

### Examples

- **R1a is a complete graph.** The owner holds every compartment in every
  scenario, so every pair of regions gets a road and there are never any
  islands. In S6 that is all 6 pairs. On the finance-work road, 5 of the
  6 agents cannot cross: only alex can.
- **R1a misleads on E1 (S4a).** It draws a road between answers and work,
  but haiku-1, sonnet-1, gemma and opus-judge cannot cross it. Only alex,
  conductor and audit can.
- **R1b hides the owner (S1, S3, S4b, S6, S7).** In S1, private is drawn
  as an island, yet john reads it and writes into work.
- **R2 hides a verify-only bridge (S2).** The calc2 checker is in lab and
  private, but because it lacks `write`, R2 draws private as an island.
- **Covert links have no road under any registration rule (S7).**
  "claude" (work) and "claude-private" (private) share no compartment, so
  no road is drawn. They can still signal through P11 and P12. The safe
  way to set this up (two templates) is exactly the setup that opens the
  covert channel.
- **The real E1 design is off the map (S4b).** E1 keeps the answers away
  from workers by holding them in the conductor's context and calling
  workers through a harness with no tools (cards-v2 amendment B). That
  carrier is not a Gnomon writer, so no rule can show it. E1's isolation
  is the harness's, not Gnomon's.
- **Roads chain (exploratory).** Gnomon enforces only direct access. In
  S4a, through the conductor and audit bridges, a worker's region
  connects to answers and archive. In S5, both firms connect through the
  client and the test runner. Whether information crosses depends on the
  bridge agents, which Gnomon cannot control.
- **Auto mode uses a road by default (S6).** Claude's template holds work
  and health, and its conversations are recorded into work. Health
  content lands in work, visible to gpt and herald, and from there it is
  one hop from the commons.

## What the map must show to be honest

1. **On every road, who can cross it.** Agents should be named or
   counted, with sessions grouped under their template. A road is a set
   of agents, not a property of the land.
2. **The owner, as able to build any road.** No region is an island to
   the owner. The plain word is "no one but you crosses", not "isolated".
3. **What crosses: content or verdicts only.** A verify-only checker
   carries much less than a writer.
4. **Covert links, drawn dotted:** same-party `spawn` templates on the
   same surface in different regions, and writer ids that are prefixes of
   one another. Better still, Gnomon could close these channels.
5. **Where auto mode records.** A region whose conversations are filed
   into another region has a road that is used by default.
6. **That roads cannot be closed.** Gnomon has no revocation. A map that
   lets people draw roads should say that erasing one does not take
   access away.
7. **A standing caveat:** isolation is enforced by Gnomon's gate, not by
   encryption. Anything that can open the log file reads and writes every
   region. This should hold until the encryption the spec plans (section
   16) is in place.
8. **Carriers outside the record,** such as a conductor or harness, are
   invisible to any map built from Gnomon. Where an experiment depends on
   one, the map cannot be its security diagram.

## Limits of this test

- **No observed data.** The counts describe constructed setups. Real
  worlds may use more or fewer bridges, so the numbers show the shapes
  that can fail, not how often they fail.
- **Capability, not traffic.** A flow counts if a channel allows it. The
  test does not measure whether agents use it.
- **Model behaviour is not tested.** A bridge agent that never repeats
  anything would be safe in practice. That depends on the model, and
  Gnomon cannot enforce it.
- **Narrow channels may be missing.** These were not probed: timing,
  log size seen from outside the gate, the `--checker` process, and
  every MCP tool one by one. Only recall, as a bridge writer, was run
  over MCP.
- **The covert channels need direct library access.** No MCP tool
  registers writers, so a model that has only MCP cannot use F3. Code on
  the same machine can.
- **R3's honesty is partly circular** (see the protocol amendment). The
  independent part is that it needs only registration data.
- **No usability check.** I did not check whether people can read a
  labelled map. The review's plain permissions table is still the
  baseline to compare against.
