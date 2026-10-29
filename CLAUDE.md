# Working in Polymechania (read first, every session)

1. **Start from the record:** read `HANDOFF.md`, then `docs/audit/SUMMARY.md`. Read other docs
   only when the task in hand needs them. Until the owner has answered the decision at the top
   of `HANDOFF.md`, ask it before building anything.
2. **Never impose a design.** Every decision is a hypothesis; taste and adjust with numbers
   from this project and outside research.
3. **Route your own work** (`docs/routing.md` section 4): published results and existing data
   first; scripts for anything exact; free engines (the door's `/ai`) for bulk work and
   judging; **sub-agents with `model` set (Sonnet or Haiku) for building**; the strongest
   model only for planning, briefs, review and integration. Log each part in `bench/ledger.jsonl`.
4. **Test without bias** (`docs/routing.md` section 3): pre-register first; exact checks before
   model judges; judges from another family, blind; same conditions for every vendor. Small
   tests get one file; the full ceremony only when the answer changes a decision.
5. **Budget:** see `HANDOFF.md`. API credit is scarce; every pre-registration states its cost bound.
6. **Judge your own work with separate agents,** at least one not Claude (free: Gemma 4 26B,
   Llama 3.3 70B via `/ai`; or a prompt file the owner pastes into another family's chat).
7. **Keep complexity down:** one open PR and one experiment at a time; every addition is needed
   now or replaces something; no new doc when a line in an existing one will do.
8. Keep replies short and plain (the owner reads on a phone). Keep the owner's real name out
   of the repositories.
