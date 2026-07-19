# PatternForge — Product

| Doc | Purpose |
|---|---|
| [PRODUCT.md](PRODUCT.md) | Vision, shipped scope, roadmap |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Stack, API, Judge0, auth |
| [CONTENT.md](CONTENT.md) | Quest schema, authoring, AI boundaries |
| [STORY_BIBLE.md](STORY_BIBLE.md) | Detective Academy Chapter 1 beats |
| [VISUAL_STYLE.md](VISUAL_STYLE.md) | UI / art direction |
| [themes/](themes/) | Per-theme lexicon packs |

Root [`AGENTS.md`](../AGENTS.md) is the short always-on agent entrypoint. Local run, deploy, and verify: root [`README.md`](../README.md).

---

## Vision

PatternForge teaches **pattern recognition** through story-driven quests — not problem memorization. It is not a LeetCode clone. DSA is the first curriculum; the long-term engine is reusable for other technical subjects.

**Loop:** Story → Discover → Think → Build → Reflect → Master pattern → Apply again.

**Prioritize:** pattern recognition, curiosity, discovery, reflection, incremental mastery.  
**Avoid:** memorization, editorial copying, AI solving problems, spoiler hints, grinding.

Reveal the pattern **after** discovery. Story motivates; it never replaces educational canon.

## Personas

| Persona | Need |
|---|---|
| Guest learner | Play without an account (progress ephemeral on reload) |
| Signed-in learner | Email+password; durable XP / unlocks / Codex |
| Content author / agent | Author canon + story from Blind-75 sources — no invented curriculum |
| Platform operator | Local Judge0; public Render + RapidAPI |

## Shipped (Phases 1a–1c)

| Slice | Status |
|---|---|
| **1a** — Guest + 3 quests + Judge0 + reflection + unlock | Done |
| **1b** — 10 quests, hint ladder, thin Codex, email/password auth | Done |
| **1c** — Render Docker (SPA+API) + Postgres + RapidAPI Judge0 | Done (one-VM bundled Judge0 deferred) |

### Product goals (still true)

1. Prove story → code → judge → reflection for DSA.
2. Keep content as data so themes/curricula can swap later.
3. Ship incrementally; do not build future phases early.

### Languages

Python, JavaScript, TypeScript (via Judge0).

### Non-goals

- Competing on problem count with LeetCode.
- AI that reveals full solutions or authors curriculum at runtime.
- Building a custom code sandbox (use Judge0).

## Future roadmap

Ordered for leverage — not a commitment to build everything at once.

| Phase | Focus |
|---|---|
| 2 | Hosted auth (Clerk/Supabase), OAuth / reset, optional guest→account merge |
| 3 | Full Pattern Codex & mastery % |
| 4 | BYO API key AI mentor (optional; never owns curriculum) |
| 5 | Analytics for content iteration |
| 6 | Adaptive difficulty (deterministic rules first) |
| 7 | Community campaign builder |
| 8 | Story pack marketplace / alternate themes |
| 9 | Additional curricula (SQL, system design, …) |
| 10 | Mobile / educator dashboard; AI-assisted authoring **with human review** |

**Invariant:** Curriculum → Campaign → Chapter → Quest (`canon` + `story`). Story and curriculum stay independent.
