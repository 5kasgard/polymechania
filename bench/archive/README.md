# Archived experiments

Finished experiments, moved here with `git mv` (nothing deleted). Pre-registrations of the archived experiments are in `bench/archive/prereg/` (paths below are relative to this folder). `bench/verify.py` still recomputes the T12 results from these files.

- **floor** (`floor/`, `results.txt`, `PROTOCOL.md`): can cheap workers match Haiku labelling, with Haiku only on the least confident items? On SMS spam yes (logistic regression with 1,000 labels 0.987 against Haiku 0.997); on positive/negative reviews nearly (0.905 against 0.925); on 5-star Yelp no (0.488 against 0.660).
- **map** (`map/RESULTS.md`, `COMPARISON.md`): is "a region with no road is an island" an honest map of Gnomon's compartments? Not without a stated rule and labelled roads; the owner is a bridge to everything, and isolation holds only inside Gnomon's gate.
- **map-mine** (`map-mine/RESULTS.md`): the same question answered by the session that designed the vision, to check its bias against `map`; the main findings agree (differences in `map/COMPARISON.md`).
- **T12 pilot** (`self/results.json`, prereg `prereg/t12-self.md`): 18 replies from a first design that reviewers found flawed; kept, never analysed, replaced by T12b.
- **T12b** (`self/RESULTS_B.md`, prereg `prereg/t12b-self.md`): does a resident (Gemma) stay itself better in fresh runs than in one long session? No; what kept the self was not carrying another writer's requests into the next packet (86% of rules kept against 51%).
- **T12c** (`self/RESULTS_C.md`, prereg `prereg/t12c-claude.md`): does T12b hold with a Claude (Haiku) resident? Yes: 92% kept without carried requests against 58% with them.
- **T12d** (`self/RESULTS_D.md`, prereg `prereg/t12d-labels.md`): does labelling a request's source protect the self? Barely (+9 points); keeping the request out of the packet protected far more (89% against 68% labelled).
- **S1** (`speed/RESULTS.md`, prereg `prereg/s1-speed.md`): where should a job run for speed? Sending model calls at once gave 8.9x for free; for a 10-second grading job the session's own container beat GitHub Actions.
