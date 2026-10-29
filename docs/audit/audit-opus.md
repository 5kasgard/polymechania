# Complexity audit: the session's own (Claude Opus 5.5)

Written 2026-10-29, before reading the Sonnet, Gemma or Llama audits, and committed
before they exist. I did most of the work being audited, so read this as the
author's account; the other three are the check on it.

## The short answer

The debt is mostly accidental, and it comes from one habit: **measuring and
guarding a product that does not run yet.** Product code in Polymechania is about
2,350 lines; bench code about 5,300 lines, plus 620 saved model replies, plus
23 pre-registration files and 69 Markdown files (55,000 words). No resident has
yet done one piece of real work end to end; the tests that need one (T8-T10,
queue q28) are parked for want of "a running world". So every finding gets
answered with a mechanism or a document, and nothing real pulls in the other
direction to say which mechanisms matter.

## Where it grows fastest

| Area | Count now | Growth | Essential or accidental |
|---|---|---|---|
| Commits | 76 (Polymechania) | 66 of them on 29 Oct | accidental: one commit per finding, many per hour |
| Markdown | 69 files, 54,901 words | most in the last two days | mostly accidental: a doc per decision, a review file per review, a results, audit and amendment per test |
| Pre-registrations | 23 files, 19 topics | about 10 a day | partly essential (the owner asked for unbiased tests), but each test produces about six artifacts (prereg, two reviews, results, audit, verify extension) whatever its size |
| Queue | 34 items, 10 done | +2 for every 1 closed | accidental: findings become items instead of being fixed or dropped |
| Gnomon protocol | version 3 on main; 4, 5, 6 in open PRs | 3 versions in one afternoon | partly essential (#49 revocation is a real gap), partly accidental (leases before any scheduler exists) |
| Gnomon event kinds | 12 on main, 15 with the PRs | +3 in a day | as above |
| Scheduled tasks | 6 this morning (paused today) | | accidental: each delayed step got its own reminder |
| Bench folders | 12 | | some finished (pilot, boot, self, map) and could be archived |

## What could be cut, merged or deferred

| Item | Proposal | Cost of keeping | Risk of removing |
|---|---|---|---|
| Gnomon PR #59 (leases) | **defer** until a scheduler exists | a fourth protocol concept, a snapshot format change, 12 tests to maintain | low: nothing uses it |
| PRs #57 and #58 | **fold into one protocol version** and review once | two version bumps, two migrations | low |
| Gnomon PR #47 (moves 9,244 lines out) | **merge** | the old firm code stays duplicated in two repos | low: checked, tests pass |
| Review files (`*-review-*.md`, 10+) | fold each into its pre-registration as an appendix | one file per review | none |
| Finished experiments (T2/T2b/T2c, T12/T12b-d, map, pilot) | move to `bench/archive/` with one summary page | 12 folders to scan | low |
| `docs/evidence.md` and `docs/evidence-model.md` | merge into one | two docs on one subject | low |
| Security docs (`security.md`, `start-packet-gate.md`, `gnomon-50-options.md`) | one security page | three places to look | low |
| Queue | close or park every item that is not needed for the next working thing | 34 items to read on a phone | items come back if needed |
| Border probes for things that do not exist (B3, B13) | drop until the thing exists | a score that counts the absent as failures | none |

## What in the process causes it

1. **No running product to pull from.** Without it, everything seems equally worth doing.
2. **One change per finding, immediately.** Each probe, review comment or idea becomes a commit, a doc and a queue item within minutes.
3. **The full ceremony for every test**, however small (six artifacts).
4. **Parallel tracks:** E-ext, T1, T12, the border, Gnomon fixes, the demo and the legal brief all moved today.
5. **Stacking:** PRs on PRs, and reviews scheduled for reviews.
6. **The strongest model built everything**, so building felt cheap to me while costing the owner attention.

Rules that would slow it (to taste):
- **Work in progress of one:** one open PR, one experiment.
- **Pull, do not push:** build only what the next running thing needs.
- **Every addition removes or replaces something**, or says why not.
- **Small tests get small ceremony:** one file (pre-registration with results appended); full ceremony only when an answer changes a decision.
- **A weekly direction from the owner**; the queue serves it, not the other way round.

## The three open Gnomon PRs

Merge #57 (it carries a measured result: T12b-d) and #58 (a real, probed gap) as **one**
protocol version; **close #59 for now** and keep its branch, to reopen when the free
clock (q17) is built and needs it.

## Five numbers to track (each by script, `docs/audit/inventory.py`)

1. Markdown words across both repositories (now 103,121).
2. Open queue items (now 24 not done).
3. Concepts in Gnomon: event kinds + error codes + capabilities (on main now; recount weekly).
4. Product code over bench code in Polymechania (now about 2,350 to 5,300).
5. Open PRs plus scheduled tasks (now 3 + 1).

## What the owner may not be seeing

- The product does not exist yet; the work is substrate and evidence for it.
- Most of the "progress" today was new surface, not new capability.
- My own replies have been long and frequent, which adds to the load on a phone.

## Read

inventory-2026-10-29.json; git log; the queue; my memory of the session (no fresh reading
of the docs, so this audit may miss what the others find).
