# Roadmap

Ordered for leverage. Earlier phases unblock later ones. Do not treat this as a commitment to build everything at once.

## Phase 0 — Foundation

Docs, repo structure, runnable scaffolds, Judge0 compose plan.

## Phase 1a — Demo slice

Guest + 3 quests + Judge0 + reflection + unlock. See `01_PRD.md`.

## Phase 1b — Core DSA campaign

10 quests, thicker tests, hint ladder, thin Codex v1, deploy sketch.

## Phase 2 — Auth & sync

Clerk or Supabase Auth; merge guest progress; cloud persistence.

## Phase 3 — Full Pattern Codex & mastery

Codex notebook, mastery %, prerequisites for advanced chapters.

## Phase 4 — AI mentor (optional)

Static hints already in content → BYO API key mentoring. AI explains/questions; never owns curriculum or reveals full solutions. See `06_AI_STRATEGY.md`.

## Phase 5 — Analytics

Completion, attempts, hints, drop-off, time-to-solve — feed content iteration.

## Phase 6 — Adaptive difficulty

Adjust recommendations from mastery and attempt signals (deterministic rules first).

## Phase 7 — Community campaign builder

Educators publish campaigns → review → moderation → distribution.

## Phase 8 — Story pack marketplace

Multiple themes over the same curriculum; downloadable story packs.

## Phase 9 — Additional curricula

SQL, system design, design patterns, networking, AI engineering, etc. Engine unchanged; new content packs.

## Phase 10 — Platforms & generation

Mobile companion, educator dashboard, AI-assisted curriculum generation **with mandatory human review** before publish.

## Architecture invariant across phases

```
Curriculum → Campaign → Chapter → Quest
                              ├── Story (theme layer)
                              ├── Pattern (canon)
                              ├── Hints
                              ├── Tests
                              └── Rewards / Reflection
```

Story and curriculum remain independent so themes can reuse the same educational content.
