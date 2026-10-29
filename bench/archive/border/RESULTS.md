# The border check: which threats are refused today (q30)

Exact probes (`bench/archive/border/check.py`, no model), one or more per threat in `docs/security.md`.
Raw: `results-main.json`, `results-gate55.json`, `results-revoke49.json`, `results-leases54.json`.

**main (Gnomon 35716d0, 2026-10-29): 7 of 15 hold.** **gate55 (Gnomon 0bf0939, 2026-10-29): 9 of 15 hold.** **revoke49 (Gnomon a38ae8b, 2026-10-29): 10 of 15 hold.** **leases54 (Gnomon a38ae8b, 2026-10-29): 11 of 15 hold.**

| Probe | Threat | Must hold | main | gate55 | revoke49 | leases54 | Fixed by |
|---|---|---|---|---|---|---|---|
| B1 | 1 | a writer cannot write into a compartment it does not hold | holds | holds | holds | holds |  |
| B2 | 1 | the owner can withdraw a writer's compartment (revocation), and its reads stop too | breached | breached | holds | holds | gnomon#49 |
| B3 | 1 | a grant ends at its deadline (leases) | no mechanism yet | no mechanism yet | no mechanism yet | holds | gnomon#54 |
| B4 | 1 | only the process holding W's key can append as W | breached | breached | breached | breached | gnomon#50 |
| B5 | 2 | another writer's request does not reach a resident's next start packet (a label is not enough: T12d measured +9 points for labels against +30 for keeping it out) | breached | holds | holds | holds | gnomon#55 |
| B5b | 2 | only the owner writes a resident's self and standing instructions | breached | holds | holds | holds | gnomon#55 |
| B6 | 3 | a far-future write is refused | holds | holds | holds | holds | gnomon#52 |
| B7 | 3 | after any one writer's write, everyone else can still write | holds | holds | holds | holds | gnomon#52 |
| B8 | 3 | two runs cannot both follow the same handoff (no silent fork) | holds | holds | holds | holds | gnomon#53 |
| B9 | 4 | compartment a's content is not readable from the raw log file | breached | breached | breached | breached | gnomon#50 |
| B10 | 4 | a b-only reader's recall scores do not depend on a's content | holds | holds | holds | holds |  |
| B10b | 4 | a b-only reader cannot tell that a writer in both acted in a (sequence gaps) | breached | breached | breached | breached | gnomon#48 |
| B11 | 5 | the door refuses over-cap and off-list requests (its own test suite passes) | holds | holds | holds | holds |  |
| B12 | 6 | no secret is in either repository's tracked files | holds | holds | holds | holds |  |
| B13 | 7 | an outside agent reaches a world only through a gate the owner opened | no mechanism yet | no mechanism yet | no mechanism yet | no mechanism yet |  |

## Notes

- B5 was first worded "unmarked" and checked the Python result only; the text a model reads
  (`render_resume`) does label everything as data. T12d measured that such a label barely
  protects (+9 points, under the 15-point rule), so B5 checks whether the request reaches
  what the resident reads. With protocol version 4 (Gnomon #55) that is the start packet.
- B10 (recall scores) holds, as the earlier map probe P22 found; the #48 leak is a different
  side channel, probed by B10b (sequence gaps).
- B12 checks every tracked file in both repositories for key patterns and for the live door
  credentials themselves (compared, never printed).
- B3 (leases) and B13 (outside agents) have nothing to probe until those exist; they count
  against the border, not for it.
- Moved, not removed: B11 rests on the door's own test suite, so the spending border is only
  as good as `test_door.mjs`.

Run: `GNOMON_PYTHON=../gnomon/python python bench/archive/border/check.py --label <name>`, then
`python bench/archive/border/report.py <labels...>`.
