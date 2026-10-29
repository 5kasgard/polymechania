# Complexity audit: Gemini Argon (low thinking), via the owner's own chat

Pasted by the owner 2026-10-29 from the prompt in `prompt-outside.md`; verbatim below. Two of its guesses checked afterwards by the session: **`parity.py` is Reed-Solomon error correction for the log, and `checkers.py` settles arithmetic and calendar claims; neither duplicates Rust validation**, so the "dual-language tax" guess does not hold. Its "600 raw files" guess is about right (the saved model replies).

1. Where complexity is growing fastest
Speculative protocol design and meta-research. You have 69,523 lines of code and 103,121 words of Markdown (a 500-page book) written in two days. Yet zero residents have done real work end-to-end.
 * Essential complexity: The Gnomon hash-chain, compartments, and the packet() boundary (PR #57). Keeping untrusted inputs out of system instructions is vital, and your experiment proved it (86–92% rule retention vs. 51–59%).
 * Accidental complexity:
   * Dual-language tax: Gnomon has 20.7k lines of Python and 17.5k lines of Rust, plus a parity.py module. (Guess: Claude translates logic between Rust and Python instead of wrapping a single Rust core via PyO3).
   * Corporate bureaucracy for nonexistent workers: Gnomon tracks 12 event kinds (appoint, dismiss, appeal, verdict) and 40 error codes (E_ROLE_CONFLICT, E_SAME_PARTY_VERIFY). You built HR and a court system before hiring a single working resident.
   * Premature versioning: Bumping protocol versions (v4, v5, v6, and q33's v7) in one afternoon when you have zero external users.
   * Lab sprawl: 802 tracked files and 23 pre-registrations in Polymechania. (Guess: Over 600 of those files are raw JSON/Markdown dumps from benchmark runs committed directly to git).
2. What to cut, merge, defer, or simplify
 * Cut/Gitignore: Untrack raw benchmark outputs in Polymechania's 12 bench/ folders. Keep the code and summary tables; delete the rest.
 * Cut: company.py and firm.py in Gnomon. Merge PR #47 (q07) now so organizational metaphors leave the storage engine.
 * Simplify: Fix q34 (append re-reads the whole log) immediately. You wrote 17.5k lines of Rust for speed, yet an O(N) file re-read on every append defeats the purpose.
 * Simplify: Stop dual-maintaining checks in Rust and Python. Keep validation in Rust; make Python a thin binding. Delete parity.py and checkers.py.
 * Defer: Themes (Kagamigakure, Hollow Acre, worlds.py, q26), pixel-art city builders, and q11 (Test Kitchen demos).
 * Defer: q17 (Cloudflare cron), q18 (remote MCP), q19 (Batch API), q20 (vision tests), and q21 (waitlist). None of this matters until one agent completes one real task locally.
3. Process causes and rules to slow the debt
The cause: You direct from iOS Safari and ask for short replies. You see clean 5-line summaries, while Claude silently writes 35,000 lines of code and 50,000 words of docs per day behind the scenes. Furthermore, your handoff rule ("use separate agents to judge your own work") creates a multiplier: every feature spawns a benchmark, a pre-registration, and a review doc (vision-review-1.md, architecture-review-1.md). Claude treats writing Markdown about work as doing work.
Four rules to stop it:
 * The Diff Cap: No PR or commit may exceed 400 lines added unless it deletes more lines than it adds.
 * Code-to-Prose Ratio: No new .md files in docs/ or prereg/. If a hypothesis takes more than 20 lines in queue.md to explain, it is too big to test.
 * Earn Your Infrastructure: No new Gnomon event kinds, error codes, or protocol features until an end-to-end resident fails in a real task because that exact feature was missing.
 * One Language per Job: Rule validation lives in Rust. Orchestration lives in Python. Never write the same check twice.
4. The three Gnomon PRs (#57, #58, #59)
 * PR #57 (Start-packet frames): Merge. It is backed by hard data and solves a real security/reliability flaw.
 * PR #58 (Revocation): Fold into #57 (or merge without a version bump). It is a straightforward access-control rule on compartments.
 * PR #59 (Leases with fencing tokens): Drop / Close. As noted, no scheduler exists to use them. Fencing tokens are complex distributed-systems primitives. Designing them before building the scheduler guarantees you will design the wrong API.
 * Stop numbering protocol versions (v4, v5, v6). You are in pre-alpha with zero outside consumers. Stay on v3 until an agent runs end-to-end.
5. Five weekly numbers to track
 * End-to-end tasks completed by a resident (Currently: 0. Target: greater than 0 before any new features).
 * Total tracked files + total lines of code (Currently: 1,109 files / 69.5k LoC. Target: down 30% via cleanup).
 * Python-to-Rust line ratio in Gnomon (Currently: 1.18 : 1. Target: less than 0.3 : 1 as Python becomes a thin wrapper).
 * Test-to-Code ratio in Polymechania (Currently: 9 test files for 31,293 lines of Python—roughly 1 test file per 3,500 lines. Target: 1 test file per 500 lines).
 * Markdown words per working feature (Currently: 103,121 words. Target: freeze or shrink).
6. What the owner might not be seeing
 * You built a bureaucracy simulator, not an agent lab. Claude loves creating taxonomies, courtrooms (E_APPEAL, E_SAME_PARTY_VERIFY), and academic pre-registrations because LLMs excel at structured text. It feels like rigorous science, but it is sophisticated procrastination from the hardest problem: getting an agent to reliably finish a real piece of work.
 * Your phone screen hides the rot. Because you read short summaries on iOS, you only experience the clean top layer of the project. You do not feel the friction of navigating 802 files, waiting on an O(N) log re-read (q34), or maintaining 31k lines of largely untested Python.
 * The "cooking" philosophy is backfiring. "Taste and adjust" works when you throw away failed dishes. Right now, every failed or half-baked test stays in the kitchen forever as tracked code and documentation.
