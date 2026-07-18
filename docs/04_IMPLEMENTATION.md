# Implementation plan

Phased build. Do not skip ahead of the active phase without an explicit scope change.

## Phase 0 — Repo & docs

- [x] `docs/` SoT (this tree)
- [x] Root `AGENTS.md` + Cursor rules/skills
- [x] Remove duplicate root roadmaps (`IMPLEMENTATION.md`, `TASKS.md`, `FUTURE_ROADMAP.md`, `AGENTS (1).md`)
- [x] `content/` placeholder + authoring README
- [x] Scaffold `frontend/`, `backend/`, `docker/` (Judge0 compose)

## Phase 1a — Tomorrow demo (active MVP cut)

### Goal

Guest completes 3 quests: story → Monaco → Judge0 → reflection → unlock.

### Tasks

1. **Scaffold**
   - [x] Vite React TS frontend + Tailwind + shadcn baseline
   - [x] FastAPI backend + SQLite + health route
   - [x] Docker Compose for Judge0 CE
2. **Content (3 quests)**
   - [x] Canon + story for Two Sum, Contains Duplicate, Valid Anagram
   - [x] ≥8 hidden tests each (expand to 15–20 in 1b)
   - [x] Detective Academy beats B1–B3 (`STORY_BIBLE.md`)
3. **Gameplay UI**
   - [x] Landing → campaign → quest story screen
   - [x] Monaco (py/js/ts) + Run/Submit
   - [x] Results panel
   - [x] Reflection screen (XP + pattern reveal + next unlock)
4. **Backend**
   - [x] Load quest content server-side
   - [x] `CodeExecutor` + Judge0 implementation
   - [x] Submit endpoint; guest progress (localStorage ± API)
5. **Verify acceptance** in `01_PRD.md` Phase 1a
   - [x] `scripts/verify_phase1a.py` (3 Python + JS re-solve + progress)
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

- [x] Initialize frontend / backend
- [x] Judge0 Docker + adapter
- [x] Campaign + quest pages
- [x] Monaco + submit flow
- [x] XP + unlock + reflection
- [x] Three authored quests

### Nice to have (after 1a)

- Wizard/NPC dialogue polish
- Sound effects
- Simple motion on reflection/unlock

## MVP success (1a)

A learner can complete three quests as a guest and unlock through the chapter with real Judge0 execution and mandatory reflection.
