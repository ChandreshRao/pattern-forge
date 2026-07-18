# Deploy sketch (Phase 1b)

PatternForge is three pieces: frontend, API, and Judge0. This is a sketch, not a production hardening guide.

## Local (default)

| Piece | How |
|---|---|
| Frontend | `cd frontend && npm run dev` → Vite on `:5173` (proxies `/api` → backend) |
| Backend | `cd backend && uvicorn app.main:app --reload --port 8000` |
| Judge0 CE | `docker compose` under `docker/` (API at `http://localhost:2358`) |
| Content | YAML under `content/` (API `content_root`) |
| Auth | Email + password; JWT secret via `JWT_SECRET` (default is for local only) |

Env (backend `.env` example):

```env
DATABASE_URL=sqlite:///./patternforge.db
JUDGE0_BASE_URL=http://localhost:2358
JWT_SECRET=change-me-in-production
CORS_ORIGINS=["http://localhost:5173"]
```

## Suggested cloud split

| Piece | Host | Notes |
|---|---|---|
| Frontend | **Vercel** | Build `frontend/`; set API base or proxy to the API host |
| API | **Railway** or **Render** | Dockerize FastAPI; persistent volume for SQLite **or** move to Postgres later |
| Judge0 | Self-hosted VM / same compose host, or a managed Judge0-compatible API | Frontend must **never** call Judge0 directly |

### Frontend (Vercel)

1. Root or `frontend/` as project directory.
2. Build command: `npm run build`; output `dist/`.
3. Point `/api` to the API origin (Vercel rewrites or `VITE_API_BASE`).

### API (Railway / Render)

1. Dockerfile: Python 3.11+, `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
2. Mount/copy `content/` into the image or a volume.
3. Set `JWT_SECRET`, `JUDGE0_BASE_URL`, `CORS_ORIGINS` to the Vercel URL.
4. SQLite on ephemeral disks will lose auth/progress on redeploy — use a volume or Postgres before treating as durable.

### Judge0

1. Keep CE behind a private network; only the API talks to it.
2. Resource limits matter (CPU/RAM per submission).
3. Health-check Judge0 from the API before demos.

## Auth note

Phase 1b uses **in-app email + password** (bcrypt + JWT). Guests may play without accounts; their progress is ephemeral. Logged-in users persist XP / unlocks / completions in SQLite (`user_progress`). Hosted Auth (Clerk / Supabase) remains a later upgrade path.

## Smoke after deploy

1. `GET /health` → ok  
2. Register → login → `GET /progress`  
3. Submit a known Python solution for `q01_two_sum` through the API (Judge0 reachable)  
4. Reload: progress still present for that user  
