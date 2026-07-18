# PatternForge Architecture

## Stack

| Layer | Choice | Scale path |
|---|---|---|
| Frontend | React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco + Framer Motion | Optional later: Lottie / PixiJS / Rive |
| Backend | FastAPI + SQLAlchemy | Same |
| DB | SQLite | PostgreSQL |
| Execution | Self-hosted Judge0 CE (Docker) | Pooled / remote Judge0 |
| Auth | None (guest) in Phase 1a | Clerk or Supabase later |
| Deploy (later) | Vercel + Railway/Render | Dockerize API + Judge0 |

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
Browser (guest_id)
  → Frontend (story UI, Monaco)
  → Backend API (progress, submit)
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

## Guest progress

1. On first visit, frontend creates `guest_id` (UUID) in `localStorage`.
2. Progress: unlocked quest ids, completions, XP, last language — stored locally for 1a reliability.
3. Optional: backend `POST /progress` keyed by `guest_id` for submissions audit (anonymous row in SQLite).
4. Phase 2: auth links guest → user and syncs cloud progress.

## API sketch (Phase 1a)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness |
| GET | `/campaigns/{id}` | Campaign + chapter metadata |
| GET | `/quests/{id}` | Quest canon (public fields) + story slots |
| POST | `/submit` | `{ guest_id, quest_id, language, source }` → judge results |
| GET/PUT | `/progress/{guest_id}` | Optional sync |

Hidden tests never ship to the client in full if avoidable; prefer server-side evaluation. If MVP ships tests in content files loaded by the server only, keep them off the public quest payload.

## Data model (SQLite, minimal)

- `guests(id, created_at)`
- `progress(guest_id, campaign_id, xp, unlocked_quest_ids_json, updated_at)`
- `submissions(id, guest_id, quest_id, language, passed, created_at)` — optional for 1a

Canon/story content is files, not necessarily DB rows, in early phases.

## Judge0 CE (Docker)

- Compose under `docker/` (Phase 0/1a implementation).
- Backend env points at local Judge0.
- Languages enabled: Python, JS, TS (map to Judge0 language ids in one adapter module).

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
