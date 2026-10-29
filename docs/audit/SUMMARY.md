# Complexity audit: what three independent audits agree on (2026-10-29)

Audits: the session's own (Claude Opus, `audit-opus.md`, committed first), a separate Claude
(Sonnet, `audit-sonnet.md`, blind to it), and Gemini Argon (`audit-gemini.md`, a different family,
via the owner's chat). Baseline counts: `inventory-2026-10-29.json`.

## All three agree

| Finding | Opus | Sonnet | Gemini |
|---|---|---|---|
| The product is small and the apparatus around it is large; no resident has done one real task end to end | yes | yes | yes |
| The habit: every finding becomes a mechanism, a doc and a queue item at once; every test gets the full ceremony | yes | yes | yes |
| Merge Gnomon #57 (backed by T12b-d) | yes | yes | yes |
| Fold #58 into #57 (one change, not two versions) | yes | yes | yes |
| Drop or park #59 (leases): no scheduler exists to use them | park | park | drop |
| Merge #47 (removes the duplicated firm code): the cheapest cut | yes | yes | yes |
| Rules: one thing at a time; build only what the next working thing needs; a size cap on additions | yes | yes | yes |
| Track whether a resident finishes real work | implied | yes | first number |

## Where they differ

- **Protocol versions.** Gemini: stop bumping versions until an agent runs end to end. Opus and
  Sonnet: one bump for #57+#58 (version gating keeps existing logs replaying the same).
- **Raw benchmark outputs.** Gemini: untrack them. Opus: archive them (`verify.py` recomputes
  results from them, so they are the evidence).
- **Sonnet only:** the costliest security work serves the Paid, unattended version, which has no
  demand test or legal answer yet; the border score is self-scored, and B4/B9 mean revocation
  and leases bind only honest writers.
- **Gemini only:** Gnomon's organisation and court concepts (appoint, dismiss, appeal; 40 error
  codes) were built before any worker; the O(N) append re-read (q34) defeats the Rust core's
  purpose; Claude treats writing Markdown about work as doing work.

## Proposal for the owner (nothing is built until you choose)

1. **One goal until it is met:** one resident completes one real task end to end (a cheap model,
   a task you set, through Gnomon's packet, work, handoff and an outside check). Everything else
   waits unless that run needs it.
2. **Gnomon:** merge #47; fold #58 into #57 as one change; close #59 (keep the branch).
3. **A cleanup pass first** (a Sonnet sub-agent, reviewed): archive finished experiments under
   `bench/archive/` with one summary; fold review files into their pre-registrations; merge
   duplicate docs; prune the queue to what serves the goal.
4. **Rules:** one open PR and one experiment at a time; additions over 400 net lines need a
   reason; no new docs or event kinds unless the goal's run needs them; small tests get one file.
5. **Weekly numbers** (by `docs/audit/inventory.py`): real tasks completed, Markdown words, open
   queue items, Gnomon concepts (event kinds + error codes + capabilities), net lines added.
