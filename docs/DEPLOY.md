# Deploy

Public MVP: **one Docker image on Render** (SPA + FastAPI) + **Render Postgres** + **RapidAPI Judge0 CE**. Local day-to-day still uses self-hosted Judge0 under `docker/`.

Frontend never talks to Judge0. All execution goes through `/api` → `Judge0Executor`.

## Local (default)

| Piece | How |
|---|---|
| Frontend | `cd frontend && npm run dev` → `:5173` (proxies `/api` → API) |
| Backend | `cd backend && uvicorn app.main:app --reload --port 8000` → `/api/...` |
| Judge0 CE | `docker compose` under `docker/judge0-v1.13.1` → `http://localhost:2358` |
| DB | SQLite (`DATABASE_URL=sqlite:///./patternforge.db`) |
| Content | YAML under `content/` (`CONTENT_ROOT`) |

Env: [backend/.env.example](../backend/.env.example) / root [.env.example](../.env.example).

Leave `JUDGE0_RAPIDAPI_KEY` empty locally.

## Public (Render + RapidAPI)

Step-by-step (including Blueprint): root [README.md](../README.md#publish-on-render-public-url).

| Piece | Host |
|---|---|
| FE + API | Render Web Service (root `Dockerfile`) |
| DB | Render Postgres (`DATABASE_URL`) |
| Judge | RapidAPI Judge0 CE |

Required cloud env:

| Variable | Example |
|---|---|
| `DATABASE_URL` | Render internal Postgres URL (`postgres://` is normalized to `postgresql+psycopg://`) |
| `JWT_SECRET` | strong secret |
| `JUDGE0_BASE_URL` | `https://judge0-ce.p.rapidapi.com` |
| `JUDGE0_RAPIDAPI_KEY` | RapidAPI key |
| `JUDGE0_RAPIDAPI_HOST` | `judge0-ce.p.rapidapi.com` |
| `CONTENT_ROOT` | `/app/content` |
| `STATIC_ROOT` | `/app/static` |
| `CORS_ORIGINS` | `["https://your-service.onrender.com"]` |

[render.yaml](../render.yaml) wires Blueprint + free Postgres; set `JUDGE0_RAPIDAPI_KEY` and `CORS_ORIGINS` in the dashboard.

### Smoke after deploy

1. `GET /api/health` → ok  
2. Register → login → `GET /api/progress`  
3. Submit a known Python solution for `q01_two_sum` (Judge0 via RapidAPI)  
4. Reload: progress still present for that user  

## Switching to self-hosted Judge0 (later)

Same app image/process; only env changes:

```env
JUDGE0_BASE_URL=http://<judge0-host>:2358
JUDGE0_RAPIDAPI_KEY=
```

Keep Judge0 on a private network. Use a VM with privileged Docker (Oracle / Hetzner / etc.) when available. Full one-VM compose bundling Judge0 + app is deferred.

## Future split hosting

Vercel FE + separate API host remains optional later. Prefer one origin (this Dockerfile) for MVP simplicity.

## Auth note

Email + password (bcrypt + JWT). Guests ephemeral; logged-in progress in SQLite (local) or Postgres (Render).
