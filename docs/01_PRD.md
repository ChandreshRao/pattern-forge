# PatternForge PRD

## Personas

| Persona | Need |
|---|---|
| Guest learner | Play a story campaign, write code, get judged, reflect — no account |
| Future signed-in learner | Sync progress, Codex, AI mentor (later phases) |
| Content author / agent | Author canon + story slots from Blind-75 sources without inventing curriculum |
| Platform operator | Run Judge0 locally (MVP), deploy later |

## Product goals

1. Prove story → code → judge → reflection works for DSA.
2. Keep content as data so themes and curricula can swap later.
3. Ship a demoable MVP fast; phase everything else.

## Phase 1a — Tomorrow demo (acceptance)

### In scope

- Guest play (no auth); progress via `guest_id` in `localStorage` (optional anonymous SQLite row).
- One campaign, one chapter, **3** fully working quests (Detective Academy theme).
- Story briefing → Monaco editor (Python + JS + TS) → Run/Submit via **self-hosted Judge0 CE** (Docker).
- Mandatory reflection after each solve: XP, pattern name revealed, short “why”, unlock next quest.
- Thin “pattern discovered” on reflection only (not full Pattern Codex UI).
- Static content committed to repo (no runtime story/curriculum generation).

### Success criteria (must all pass)

1. A guest opens the app and enters the Detective Academy campaign without signing up.
2. The guest completes **all 3** quests in **Python**.
3. At least **one** quest is also successfully submitted in **JS or TS**.
4. Each solve shows a reflection screen with XP and the discovered pattern name.
5. Completing quest *n* unlocks quest *n+1*; progress survives a page refresh (guest storage).
6. Code execution goes through the backend → Judge0 adapter (frontend never talks to Judge0 directly).

### Out of scope for Phase 1a

- Auth (Clerk / Supabase)
- Full Pattern Codex notebook UI
- AI mentor / BYO API keys
- Analytics dashboard
- 10-quest campaign (stubs/beats may be documented; not all playable)
- Story packs / multiple live themes
- Cosmetics, rich achievements, side quests, boss battles
- Adaptive difficulty
- Community campaigns / marketplace
- Live AI story or curriculum generation

## Phase 1b — Core DSA campaign (near-term)

### In scope

- Expand to **10** playable quests; thicken tests toward **15–20** each.
- Hint ladder L1–L5 in content metadata.
- Hardened SQLite guest/progress model.
- Thin Codex v1: list of unlocked patterns.
- Deploy sketch: Vercel (FE) + Railway/Render (API) + hosted/self-hosted Judge0.

### Success criteria

- Guest (or later auth user) can complete all 10 chapter-1 quests with reflection and unlocks.
- Each quest has ≥15 tests and a full static hint ladder.
- Codex v1 lists patterns discovered so far.

## Problem selection

| Phase | Count | Sources (`refer_problems/`) | Patterns |
|---|---|---|---|
| 1a | 3 | `arrays/two_sum.py`, `arrays/contains_duplicate.py`, `strings/valid_anagram.py` | Hash map / set / frequency |
| 1b | +7 → 10 total | Curated Blind-75 arrays/strings/linked lists (see `CONTENT_GUIDE.md`) | Expand coverage; still chapter-1 coherent |

## Languages

MVP judge languages: **Python**, **JavaScript**, **TypeScript**.

## Non-goals (product)

- Competing on problem count with LeetCode.
- AI that reveals full solutions or authors curriculum at runtime.
- Building a custom code sandbox (use Judge0).

## Metrics (later — Phase analytics)

Quest completion, attempts, hint usage, drop-off, submission count, time-to-solve, common mistakes. Not instrumented in 1a beyond whatever is needed to demo.
