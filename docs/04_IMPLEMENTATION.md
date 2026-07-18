# Implementation plan

Phased build. Do not skip ahead of the active phase without an explicit scope change.

## Phase 0 — Repo & docs

- [x] `docs/` SoT (this tree)
- [x] Root `AGENTS.md` + Cursor rules/skills
- [x] Remove duplicate root roadmaps (`IMPLEMENTATION.md`, `TASKS.md`, `FUTURE_ROADMAP.md`, `AGENTS (1).md`)
- [x] `content/` placeholder + authoring README
- [ ] Scaffold `frontend/`, `backend/`, `docker/` (Judge0 compose)

## Phase 1a — Tomorrow demo (active MVP cut)

### Goal

Guest completes 3 quests: story → Monaco → Judge0 → reflection → unlock.

### Tasks

1. **Scaffold**
   - [ ] Vite React TS frontend + Tailwind + shadcn baseline
   - [ ] FastAPI backend + SQLite + health route
   - [ ] Docker Compose for Judge0 CE
2. **Content (3 quests)**
   - [ ] Canon + story for Two Sum, Contains Duplicate, Valid Anagram
   - [ ] ≥8 hidden tests each (expand to 15–20 in 1b)
   - [ ] Detective Academy beats B1–B3 (`STORY_BIBLE.md`)
3. **Gameplay UI**
   - [ ] Landing → campaign → quest story screen
   - [ ] Monaco (py/js/ts) + Run/Submit
   - [ ] Results panel
   - [ ] Reflection screen (XP + pattern reveal + next unlock)
4. **Backend**
   - [ ] Load quest content server-side
   - [ ] `CodeExecutor` + Judge0 implementation
   - [ ] Submit endpoint; guest progress (localStorage ± API)
5. **Verify acceptance** in `01_PRD.md` Phase 1a

### Explicitly deferred from 1a

Auth, full Codex, AI, analytics, 10 quests, multi-theme packs, cosmetics, adaptive difficulty.

## Phase 1b — Core DSA campaign

- [ ] Quests 4–10 + story bible beats B4–B10
- [ ] 15–20 tests per quest
- [ ] Hint ladder L1–L5 in UI
- [ ] Thin Codex v1 (unlocked patterns list)
- [ ] Harden progress model
- [ ] Deploy notes (Vercel + API host + Judge0)

## Phase 2+ 

See `07_ROADMAP.md`. Do not start unless Phase 1b acceptance is met or scope is renegotiated.

## Task board (living)

### High priority (1a)

- Initialize frontend / backend
- Judge0 Docker + adapter
- Campaign + quest pages
- Monaco + submit flow
- XP + unlock + reflection
- Three authored quests

### Nice to have (after 1a)

- Wizard/NPC dialogue polish
- Sound effects
- Simple motion on reflection/unlock

## MVP success (1a)

A learner can complete three quests as a guest and unlock through the chapter with real Judge0 execution and mandatory reflection.
