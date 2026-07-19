# PatternForge Architecture

## Stack

| Layer | Choice | Scale path |
|---|---|---|
| Frontend | React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco + Framer Motion | Optional later: Lottie / PixiJS / Rive |
| Backend | FastAPI + SQLAlchemy | Same |
| DB | SQLite (local) / PostgreSQL (Render) | Same |
| Execution | Judge0 CE (`Judge0Executor`) | Self-hosted Docker **or** RapidAPI |
| Auth | Email + password (JWT) in Phase 1b; guests ephemeral | Clerk / Supabase later |
| Deploy | See `DEPLOY.md` | Render (FE+API Docker) + Postgres + RapidAPI Judge0 |

## Repository layout (target)

```
docs/                 # Product & engineering SoT
frontend/             # Vite React app
backend/              # FastAPI
content/              # Curriculum + campaigns (data, not code)
  campaigns/
  themes/
docker/               # Judge0 compose
refer_problems/       # Blind-75 source stubs (authoring input)
scripts/              # Validators, content tools (later)
.cursor/rules/
.cursor/skills/
```

## High-level flow

```
Browser (guest session OR JWT)
  → Frontend (story UI, Monaco, hints, thin Codex)
  → Backend API (auth, progress, submit, hints, codex)
  → CodeExecutor port
  → Judge0 CE
```

Frontend never calls Judge0 directly. Backend owns timeouts, language ids, and test harness wrapping.

## CodeExecutor port

```text
submit(source: str, language: "python" | "javascript" | "typescript", tests: TestCase[])
  → { status, passed, failed, results[], stdout?, stderr?, time_ms? }
```

- Phase 1: only `Judge0Executor` implementation.
- Swap host/URL via env (`JUDGE0_BASE_URL`, etc.) without changing routes.
- Do not build a custom sandbox.

## Content as data

Quests live under `content/campaigns/...` as YAML/JSON with separated keys:

- `canon` — pattern, signatures, tests, hint facts, reflection teaching points
- `story` — slots filled from theme + story bible beats

UI renders canon I/O and story slots; it does not hardcode problems in React components.

Art assets (portraits, expressions, environments, icons) are **committed static files** served by the frontend. Never generate artwork at runtime. See `08_VISUAL_STYLE.md` and `06_AI_STRATEGY.md`.

See `05_CONTENT_ENGINE.md` for schema.

## Auth & progress (Phase 1b)

1. **Guest:** may play without an account. Progress is **ephemeral** (in-memory on the client; reload resets).
2. **Register / login:** `POST /api/auth/register`, `POST /api/auth/login` → JWT. `GET /api/auth/me`.
3. **Logged-in progress:** SQLite/Postgres `user_progress` keyed by `user_id` + `campaign_id` (XP, unlocks, completions, last language).
4. Submit with `Authorization: Bearer …` persists completions; guest submit returns ephemeral progress in the response only.
5. Hosted Auth (Clerk/Supabase), email verify, and password reset are later.

## API sketch (Phase 1b)

All routes are under the `/api` prefix (Vite proxies `/api` locally; production serves SPA + `/api` from one process).

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness |
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | JWT |
| GET | `/api/auth/me` | Current user |
| GET | `/api/campaigns/{id}` | Campaign + chapter metadata |
| GET | `/api/quests/{id}` | Quest canon (public fields) + story slots |
| GET | `/api/quests/{id}/hints?max_level=` | Progressive hint ladder |
| GET | `/api/codex` | Thin pattern list for completed quests |
| POST | `/api/submit` | Judge run/submit (+ optional guest snapshot fields) |
| GET/PUT | `/api/progress` | Authenticated progress sync |

Hidden tests never ship to the client in full if avoidable; prefer server-side evaluation. Hints are served progressively by level.

## Data model (SQLite, Phase 1b)

- `users(id, email, password_hash, created_at)`
- `user_progress(user_id, campaign_id, xp, unlocked_quest_ids_json, completed_quest_ids_json, last_language, updated_at)`
- `submissions(id, user_id?, guest_id?, quest_id, language, mode, passed, created_at)`

Canon/story content is files, not necessarily DB rows, in early phases.

## Judge0 CE

- Local: compose under `docker/` (Phase 0/1a).
- Cloud: RapidAPI Judge0 CE via `JUDGE0_BASE_URL` + `JUDGE0_RAPIDAPI_KEY` (headers added when key is set).
- Languages enabled: Python, JS, TS (map to Judge0 language ids in one adapter module).
- Swap self-hosted ↔ RapidAPI with env only; routes unchanged.

## Scaling notes

- SQLite → Postgres: SQLAlchemy URL change; keep models thin.
- Single Judge0 → multiple workers / remote CE: still behind `CodeExecutor`.
- Themes / curricula: new content packs; same APIs.
- AI mentor (later): separate abstraction behind backend; never inlines into judge or unlock logic.

## Engineering principles

- Build incrementally; keep the app runnable.
- Reuse OSS (Monaco, Judge0, shadcn).
- Prefer deterministic curriculum over AI novelty.
- Separate curriculum from presentation; separate AI from business logic.
- Configuration over hardcoding.
