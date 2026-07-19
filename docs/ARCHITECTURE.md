# PatternForge — Architecture

## Stack

| Layer | Choice | Scale path |
|---|---|---|
| Frontend | React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco + Framer Motion | Optional later: Lottie / PixiJS / Rive |
| Backend | FastAPI + SQLAlchemy | Same |
| DB | SQLite (local) / PostgreSQL (Render) | Same |
| Execution | Judge0 CE (`Judge0Executor`) | Self-hosted Docker **or** RapidAPI |
| Auth | Email + password (JWT); guests ephemeral | Clerk / Supabase later |
| Deploy | Root [README.md](../README.md) | Render (FE+API Docker) + Postgres + RapidAPI Judge0 |

## Repository layout

```
docs/                 # Product & engineering SoT
frontend/             # Vite React app
backend/              # FastAPI
content/              # Curriculum + campaigns (data, not code)
docker/               # Judge0 compose
refer_problems/       # Blind-75 source stubs (authoring input)
scripts/              # Validators, verify scripts
e2e/                  # Playwright
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

- Only `Judge0Executor` in current phases.
- Swap host/URL via env (`JUDGE0_BASE_URL`, etc.) without changing routes.
- Do not build a custom sandbox.

## Content as data

Quests live under `content/campaigns/...` as YAML with separated `canon` and `story` keys. UI renders those files; it does not hardcode problems in React. Schema and authoring: [CONTENT.md](CONTENT.md).

Art assets are **committed static files**. Never generate artwork at runtime. See [VISUAL_STYLE.md](VISUAL_STYLE.md).

## Auth & progress

1. **Guest:** may play without an account. Progress is **ephemeral** (reload resets).
2. **Register / login:** `POST /api/auth/register`, `POST /api/auth/login` → JWT. `GET /api/auth/me`.
3. **Logged-in progress:** SQLite/Postgres `user_progress` keyed by `user_id` + `campaign_id`.
4. Submit with `Authorization: Bearer …` persists completions; guest submit returns ephemeral progress in the response only.
5. Hosted Auth (Clerk/Supabase), email verify, and password reset are later.

## API sketch

All routes under `/api` (Vite proxies locally; production serves SPA + `/api` from one process).

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
| POST | `/api/submit` | Judge run/submit |
| GET/PUT | `/api/progress` | Authenticated progress sync |

Hidden tests stay server-side when possible. Hints are served progressively by level.

## Data model

- `users(id, email, password_hash, created_at)`
- `user_progress(user_id, campaign_id, xp, unlocked_quest_ids_json, completed_quest_ids_json, last_language, updated_at)`
- `submissions(id, user_id?, guest_id?, quest_id, language, mode, passed, created_at)`

Canon/story content is files, not DB rows, in current phases.

## Judge0 CE

- Local: compose under `docker/`.
- Cloud: RapidAPI Judge0 CE via `JUDGE0_BASE_URL` + `JUDGE0_RAPIDAPI_KEY`.
- Languages: Python, JS, TS (ids mapped in one adapter module).
- Self-hosted ↔ RapidAPI via env only; routes unchanged.

## Deploy & verify

Operator steps live in the root README (single place — do not duplicate here):

- **Local + publish:** [README.md — Local development](../README.md#local-development) and [Publish on Render](../README.md#publish-on-render-public-url)
- **Verify / e2e:** [README.md — Verify](../README.md#verify)

## Engineering principles

- Build incrementally; keep the app runnable.
- Reuse OSS (Monaco, Judge0, shadcn).
- Prefer deterministic curriculum over AI novelty.
- Separate curriculum from presentation; separate AI from business logic.
- Configuration over hardcoding.
