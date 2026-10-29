# Two attempts at the same test, compared

Run at the owner's request: the same question, answered by two
investigators at opposite ends of the bias spectrum, without seeing each
other's work.

- **Independent:** a separate agent that neither proposed the test nor
  helped design the vision (`bench/archive/map/`, unedited).
- **Conductor:** the Claude designing the vision with the owner, so the one
  at risk of wanting the claim to hold (`bench/archive/map-mine/`; its protocol was
  committed to GitHub, b65d59c, before it read any code, and its files were
  kept out of the independent agent's folder while it worked).

## Where they agree

- **Draw roads from grants, never from intention.** Both found hidden
  crossings whenever roads are drawn by what the owner means rather than by
  what is granted.
- **Label every road with who can cross it.** Both found that bare roads
  suggest more agents can cross than can.
- **The owner bridges everything.** Both: a world with its owner in it has
  no true islands; the honest wording is "no one but you crosses".
- **Isolation holds only inside Gnomon's gate.** Both: the log is one plain
  file holding every region.
- **Inside the record, references never cross compartments.** Both, from
  the code; the independent agent also confirmed it with live probes.
- **No real usage data exists;** both used constructed scenarios.
- **Verdict:** the claim fails as written and holds only with a stated rule
  and caveats.

## What only the independent agent found

It ran 23 live probes against the real library; the conductor only read
code. That found four things the conductor missed:
1. **Auto mode crosses without anyone choosing:** it files a whole session's
   conversation into one compartment, so what Claude read in one region is
   recorded in another.
2. **A covert one-bit channel:** two setups with no compartment in common
   passed bits to each other through refused registrations (sent
   `[1,0,1,1]`, decoded `[1,0,1,1]`). It needs direct library access, not
   the MCP server.
3. **Access cannot be revoked:** there is no way to remove a compartment
   from a writer, so roads cannot be closed.
4. **The log is writable, not only readable:** appends are not
   authenticated, so anything that can open the file can write as anyone.

It also judged more strictly that E1's isolation is the harness's, not
Gnomon's, so no Gnomon map can be E1's security diagram; the conductor
said the map would show the harness's road, which is true but weaker.

## Bias or missing context?

**The evidence points to bias on the conductor's side, in the form of
trusting the claim.** Its own protocol listed "error messages or counts
leaking across (Gnomon claims they do not)" as a flow to look for, then
never tested it; it read the code and took the gate's refusals at their
word. The independent agent tested, and found a leak. The conductor also
framed its verdict more gently ("holds only with a rule and caveats")
where the independent agent led with "fails as written". Effort differed
too (the independent agent spent about 28 minutes and 65 tool calls), so
part of the gap is thoroughness, but the specific misses are the ones a
motivated reader would skip.

**No sign of missing context on the independent side:** it found and used
the E1 design, Gnomon's tests and the vision, and stated its own
weaknesses (its best rule's zero is partly built in, since it was drawn
from the same flows it was scored against).

## What follows

- For the vision: the map's rule is the independent agent's R3 (labelled
  roads, owner shown as able to build any road, covert links dotted,
  verdict-only roads marked, auto-mode recording shown, roads that cannot
  be closed marked), with a plain permissions table one tap away.
- For Gnomon: four issues worth fixing, independent of Polymechania: the
  covert channel through refused registrations; no revocation of
  compartments; unauthenticated appends to the log; auto mode filing
  across compartments.
- For method: when the conductor tests its own design, it should probe, not
  only read, and an independent run should stay the default.
