# Stat cards with cost and speed, from T2, T2b and T2c (q16)

Built by `bench/cards/t2_cards.py` from the saved runs; nothing typed in. One attempt
per task, 12 tasks per set, so intervals are wide and gaps of one pass are directions.
Verdicts are the hidden graders (a script: outside every model family). The two
expected-cost columns are examples of `expected_cost` with a wrong result costing
1 cent or 10 cents (to redo or to catch); the right loss depends on the work.

| Worker | Settings | Kind | Passes | Success (90%) | $ per run | $ per success | p50 s | p90 s | Expected $ (loss 1c / 10c) |
|---|---|---|---|---|---|---|---|---|---|
| haiku A | start packet in the prompt, default thinking | code-easy | 12/12 | 0.93 (0.79-1.00) | 0.00082 | 0.00089 | 7.0 | 14.9 | 0.0015 / 0.0080 |
| haiku A | start packet in the prompt, default thinking | code-hard | 9/12 | 0.71 (0.51-0.89) | 0.00136 | 0.00190 | 7.8 | 21.2 | 0.0042 / 0.0299 |
| haiku B | start packet cached, default thinking | code-easy | 12/12 | 0.93 (0.79-1.00) | 0.00078 | 0.00085 | 7.5 | 12.6 | 0.0015 / 0.0079 |
| haiku B | start packet cached, default thinking | code-hard | 10/12 | 0.79 (0.59-0.93) | 0.00105 | 0.00134 | 8.2 | 19.9 | 0.0032 / 0.0225 |
| haiku D | cached, thinking off | code-hard | 12/12 | 0.93 (0.79-1.00) | 0.00050 | 0.00054 | 3.5 | 9.2 | 0.0012 / 0.0076 |
| haiku DL | cached, thinking off, low effort | code-hard | 11/12 | 0.86 (0.68-0.97) | 0.00048 | 0.00056 | 4.0 | 6.9 | 0.0019 / 0.0148 |
| haiku L | cached, adaptive thinking, low effort | code-hard | 11/12 | 0.86 (0.68-0.97) | 0.00092 | 0.00107 | 6.2 | 16.5 | 0.0023 / 0.0152 |
| sonnet A | start packet in the prompt, default thinking | code-easy | 12/12 | 0.93 (0.79-1.00) | 0.01292 | 0.01391 | 6.8 | 15.9 | 0.0136 / 0.0201 |
| sonnet A | start packet in the prompt, default thinking | code-hard | 11/12 | 0.86 (0.68-0.97) | 0.01736 | 0.02026 | 8.9 | 17.7 | 0.0188 / 0.0316 |
| sonnet B | start packet cached, default thinking | code-easy | 12/12 | 0.93 (0.79-1.00) | 0.01024 | 0.01103 | 6.8 | 15.1 | 0.0110 / 0.0174 |
| sonnet B | start packet cached, default thinking | code-hard | 12/12 | 0.93 (0.79-1.00) | 0.01399 | 0.01507 | 9.0 | 16.3 | 0.0147 / 0.0211 |
