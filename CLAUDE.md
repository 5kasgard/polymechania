# Working in Polymechania (read first, every session)

1. **Start from the record:** read `HANDOFF.md`, then `docs/vision.md`.
2. **Never impose a design.** Every decision is a hypothesis; taste and
   adjust with numbers from this project and outside research.
3. **Route your own work** by `docs/routing.md` section 4: published
   results and existing data first; scripts for anything exact; free
   engines (Cloudflare Workers AI through the door's `/ai`, sub-agents on
   the owner's Pro plan) for bulk work and judging; the cheapest Claude
   tier that passes for short judgement (set `model` on sub-agents); the
   strongest model only for planning, design and integration. Log each
   part in `bench/ledger.jsonl`.
4. **Test without bias** by `docs/routing.md` section 3: pre-register and
   commit first; exact checks before model judges; judges from another
   family, blind and shuffled; same conditions for every vendor; open and
   cheap options as arms; audit numbers with `bench/verify.py`.
5. **Budget:** see `HANDOFF.md` ("Budget"). API credit is scarce; every
   pre-registration states its API cost bound.
6. **Judge your own work with separate agents.** When Claude did the work,
   at least one judge is not Claude (Workers AI's Llama or Gemma through
   the door is free); a Claude judge, at the cheapest tier that does the
   job, may be one of several.
7. Keep replies short and plain (the owner reads on a phone). Keep the
   owner's real name out of the repositories.
