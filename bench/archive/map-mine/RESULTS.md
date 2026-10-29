# Is the map honest? The conductor's own results

Written 2026-10-28, before seeing the separate agent's results. The author
has been designing the vision with the owner, so read with that bias in
mind; the comparison with the independent attempt is the check.

## What Gnomon allows (from its code, not only its docs)

- Every write requires the writer to hold the target compartment.
  References, citations, supersession, dispute evidence and handoff
  references across compartments are refused by the gate. An agent instance
  cannot enter a compartment its parent is not in.
- Every read through the API (query, recall, resume, the list of writers)
  is scoped to the reader's own compartments. There is no owner bypass.
- Capabilities belong to a writer, not to a compartment: a writer that can
  write in one of its compartments can write in all of them (claims,
  questions, and verdicts with a free-text method).

So **inside Gnomon, content crosses from one region to another only through
a writer that holds both and can write**: it reads in one and writes in the
other. Crossings chain over time (A to B by one writer, then B to C by
another is A to C).

**Outside Gnomon's view:** anything that can read the log file (plain JSONL
holding every compartment), one program or person holding several writers'
credentials, and a person copying by hand.

## Results (constructed scenarios; no real usage logs exist here)

`map_check.py`, output in `output.txt`. Three scenarios: a personal world,
the E1 experiment, and grants taken from Gnomon's own tests.

| | Personal world | E1 | Grants from tests |
|---|---|---|---|
| Roads by writer (R1) | 3, all carried by the owner; 1 also by an agent | 1, carried by the conductor | 3, one by the owner, two by agents |
| Islands under R1 | none | none | none |
| Islands for agents only | the commons link | none | lab |
| Hidden bridges if roads are drawn by intention (R2) | 2 | 1 | 3 |
| Roads that mislead if unlabelled | 3 | 1 | 3 |

## What this says

**The claim holds only with a rule and caveats.**
1. **Draw roads from grants, never from intention.** A road exists exactly
   when some writer that can write holds both regions (R1). Then nothing
   recorded crosses without a road, by construction. Drawing roads by what
   the owner intends (R2) hid real crossings in every scenario.
2. **Label every road with who can carry across it.** A bare road suggests
   anyone can cross; in every scenario most writers on either side cannot.
3. **People are everywhere.** An owner who holds all their regions bridges
   them all, so a world with its owner in it has no islands. Islands are
   meaningful for agents: draw people apart (you are present in every
   region you hold) and draw roads for agents.
4. **An experiment's island is not an island to the operator.** In E1 the
   conductor holds both items and answers, so an honest map shows that road,
   carried by the harness. That is correct and worth seeing: it says whom
   the island's isolation depends on.
5. **The map only covers what Gnomon controls.** The log file holds every
   compartment in plain text, so any agent that can read the file ignores
   every road. Islands are real only if agents reach the record through the
   gate (the MCP server, the door) and never the file. That is the same
   lesson E1 taught about shells. Gnomon's planned encryption of
   compartments (its M10) would close part of this.

## Limits

Constructed scenarios only; writer kinds were assigned by me; reading
counts as access whether or not an agent uses what it read; the analysis
trusts the gate's code as read, not as tested adversarially.
